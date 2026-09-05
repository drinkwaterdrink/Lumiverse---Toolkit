#!/usr/bin/env python3
"""Compile a LoreForge neutral spec to portable compatibility lorebook JSON.

The output is modeled on the audited standalone SillyTavern lorebook shape.
It is not represented as Lumiverse's undocumented full-fidelity native schema.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_spec import load_json, validate_spec


ROLE_CODES = {"system": 0, "user": 1, "assistant": 2}
LOGIC_CODES = {"and": 0, "not_all": 1, "not": 2}


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip()).strip("._")
    return cleaned or "Lorebook"


def compile_entry(
    entry: dict[str, Any], uid: int, portable_order: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    logic = entry["selective_logic"]
    primary = list(entry.get("keywords", []))
    secondary = list(entry.get("secondary_keywords", []))
    mapping_note = "direct"
    if logic == "or" and secondary:
        primary.extend(key for key in secondary if key not in primary)
        secondary = []
        selective = False
        selective_code = 0
        mapping_note = "OR secondary keywords merged into portable primary keywords"
    elif logic in LOGIC_CODES and secondary:
        selective = True
        selective_code = LOGIC_CODES[logic]
    else:
        selective = False
        selective_code = LOGIC_CODES.get(logic, 0)

    compiled = {
        "uid": uid,
        "comment": entry["title"],
        "key": primary,
        "keysecondary": secondary,
        "selectiveLogic": selective_code,
        "content": entry["content"],
        "position": entry["position"],
        # The audited compatibility shape is SillyTavern-style (higher order
        # first), while the canonical LoreForge/Lumiverse spec is lower first.
        # Use a rank mapping instead of copying the value and reversing intent.
        "order": portable_order,
        "depth": entry["depth"] if entry["position"] == 4 else 4,
        "role": ROLE_CODES[entry["role"]],
        "selective": selective,
        "constant": entry["state"] == "constant",
        "probability": entry["probability"],
        "useProbability": entry["use_probability"],
        "addMemo": True,
        "disable": entry["state"] == "disabled",
        "ignoreBudget": entry["state"] == "constant",
        "vectorized": entry["vectorized"],
        "group": entry["group"] or "",
        "groupOverride": entry["group_override"],
        "groupWeight": entry["group_weight"],
        "scanDepth": entry["scan_depth"],
        "caseSensitive": entry["case_sensitive"],
        "matchWholeWords": entry["match_whole_words"],
        "useGroupScoring": None,
        "excludeRecursion": entry["exclude_recursion"],
        "preventRecursion": entry["prevent_recursion"],
        "delayUntilRecursion": entry["delay_until_recursion"],
        "sticky": entry["sticky"],
        "cooldown": entry["cooldown"],
        "delay": entry["delay"],
        "displayIndex": uid,
    }
    metadata = {
        "stable_id": entry["stable_id"],
        "lumiverse_order": entry["order"],
        "portable_order": portable_order,
        "category": entry.get("category"),
        "priority": entry["priority"],
        "use_regex": entry["use_regex"],
        "selective_logic": logic,
        "selective_mapping": mapping_note,
        "content_rationale": entry["content_rationale"],
        "activation_rationale": entry["activation_rationale"],
        "tests": entry["tests"],
    }
    return compiled, metadata


def compile_book(spec: dict[str, Any], book: dict[str, Any]) -> dict[str, Any]:
    runtime = spec.get("recommended_runtime", {})
    entries: dict[str, Any] = {}
    source_metadata: dict[str, Any] = {}
    unique_orders = sorted({entry["order"] for entry in book["entries"]})
    portable_orders = {
        value: len(unique_orders) - index
        for index, value in enumerate(unique_orders)
    }
    for uid, entry in enumerate(book["entries"]):
        compiled, metadata = compile_entry(entry, uid, portable_orders[entry["order"]])
        entries[str(uid)] = compiled
        source_metadata[str(uid)] = metadata

    output: dict[str, Any] = {
        "name": book["name"],
        "description": book["description"],
        "extensions": {
            "loreforge": {
                "schema": "loreforge.portable-metadata.v1",
                "format_notice": "Portable compatibility output; not documented as native Lumiverse full-fidelity JSON.",
                "scope_recommendation": book["scope_recommendation"],
                "activation_policy": book.get("activation_policy"),
                "canonical_order_semantics": "Lumiverse: lower values first",
                "portable_order_semantics": "Compatibility output: higher values first",
                "portable_order_mapping": "Rank-inverted from canonical Lumiverse order; original value retained per entry as lumiverse_order",
                "recommended_runtime": runtime,
                "entries": source_metadata,
            }
        },
        "entries": entries,
    }
    if runtime.get("global_scan_depth") is not None:
        output["scan_depth"] = runtime["global_scan_depth"]
    if runtime.get("max_token_budget") is not None:
        output["token_budget"] = runtime["max_token_budget"]
    output["recursive_scanning"] = runtime.get("max_recursion_passes", 0) > 0
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    spec = load_json(args.spec)
    findings = validate_spec(spec)
    if findings.errors:
        for error in findings.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("ERROR: portable compile refused because the neutral spec is invalid", file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "loreforge.portable-manifest.v1",
        "project": spec["project"]["name"],
        "format": "portable_compatibility",
        "native_lumiverse_full_fidelity": False,
        "books": [],
        "warnings": findings.warnings,
    }
    for book in spec["books"]:
        filename = safe_name(book["name"]) + ".json"
        path = args.out_dir / filename
        compiled = compile_book(spec, book)
        path.write_text(json.dumps(compiled, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        json.loads(path.read_text(encoding="utf-8"))
        manifest["books"].append(
            {
                "id": book["id"],
                "name": book["name"],
                "file": filename,
                "scope_recommendation": book["scope_recommendation"],
                "entry_count": len(book["entries"]),
            }
        )
        print(path)

    manifest_path = args.out_dir / "Manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(manifest_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
