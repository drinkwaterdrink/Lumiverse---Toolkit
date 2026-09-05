#!/usr/bin/env python3
"""Static inventory for SillyTavern Chat Completion preset exports."""

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

MACRO_RE = re.compile(r"\{\{\s*([A-Za-z0-9_.$@/-]+)(?:::[\s\S]*?)?\}\}")
SET_RE = re.compile(r"\{\{(?:setvar|setchatvar|setglobalvar)::([^}:]+)")
GET_RE = re.compile(r"\{\{(?:getvar|getchatvar|getglobalvar)::([^}:]+)")
RNG_RE = re.compile(r"\{\{(random|pick|roll)::([^}]*)\}\}")


def load_bytes(path):
    raw = Path(path).read_bytes()
    return raw, json.loads(raw.decode("utf-8"))


def prompt_id(value):
    if isinstance(value, dict):
        return value.get("identifier") or value.get("id")
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("preset")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()

    raw, data = load_bytes(args.preset)
    if not isinstance(data, dict):
        raise SystemExit("Preset root must be a JSON object")

    prompts = data.get("prompts", [])
    orders = data.get("prompt_order", [])
    if isinstance(orders, dict):
        orders = [orders]
    if not isinstance(prompts, list) or not isinstance(orders, list):
        raise SystemExit("Expected prompts and prompt_order to be arrays")

    ids = [prompt_id(p) for p in prompts]
    idset = {x for x in ids if x}
    counts = collections.Counter(ids)
    duplicate_or_blank = sorted(str(k) for k, v in counts.items() if not k or v > 1)
    dangling = []
    effective_orders = []
    referenced = set()

    for order_index, order_record in enumerate(orders):
        entries = order_record.get("order", []) if isinstance(order_record, dict) else []
        variant = {
            "index": order_index,
            "character_id": order_record.get("character_id") if isinstance(order_record, dict) else None,
            "entries": [],
        }
        for position, entry in enumerate(entries):
            pid = prompt_id(entry)
            enabled = entry.get("enabled") if isinstance(entry, dict) else None
            variant["entries"].append(
                {"position": position, "identifier": pid, "enabled": enabled}
            )
            if pid:
                referenced.add(pid)
            if not pid or pid not in idset:
                dangling.append(
                    {"variant": order_index, "position": position, "identifier": pid}
                )
        effective_orders.append(variant)

    text = "\n".join(str(p.get("content", "")) for p in prompts if isinstance(p, dict))
    macros = collections.Counter(m.group(1) for m in MACRO_RE.finditer(text))
    setters = collections.Counter(m.group(1).strip() for m in SET_RE.finditer(text))
    getters = collections.Counter(m.group(1).strip() for m in GET_RE.finditer(text))
    rng = [
        {"kind": m.group(1), "args": m.group(2), "offset": m.start()}
        for m in RNG_RE.finditer(text)
    ]

    high_risk = []
    if re.search(r"\{\{random::[^}\n]+::[^}\n]+::[^}\n]+", text):
        high_risk.append("categorical random: source/target semantics require review")
    if "{{pick::" in text:
        high_risk.append("pick: verify SillyTavern stable-pick behavior and target reroll policy")
    if "{{getvar::" in text or "{{setvar::" in text:
        high_risk.append("local variables: classify build-only versus cross-turn lifetime")
    if "<think>" in text or "</think>" in text:
        high_risk.append("literal reasoning wrapper found")
    if not orders:
        high_risk.append("no prompt_order found; effective Prompt Manager order is unproven")

    setting_keys = [key for key in data if key not in {"prompts", "prompt_order"}]
    report = {
        "source": args.preset,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "prompt_count": len(prompts),
        "prompt_order_variants": len(orders),
        "duplicate_or_blank_prompt_ids": duplicate_or_blank,
        "dangling_order_references": dangling,
        "unordered_prompt_ids": sorted(idset - referenced),
        "effective_orders": effective_orders,
        "macro_counts": dict(macros),
        "setter_keys": dict(setters),
        "getter_keys": dict(getters),
        "rng_occurrences": rng,
        "high_risk": high_risk,
        "non_prompt_setting_keys": sorted(setting_keys),
        "top_level_keys": sorted(data.keys()),
    }
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
