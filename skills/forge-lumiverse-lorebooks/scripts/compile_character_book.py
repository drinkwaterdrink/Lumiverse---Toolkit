#!/usr/bin/env python3
"""Compile a validated LoreForge book to the observed embedded Character Book subset."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("validate_spec", HERE / "validate_spec.py")
validate_spec = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validate_spec)

ADVANCED_DEFAULTS = {
    "secondary_keywords": [], "selective_logic": "or", "case_sensitive": False,
    "match_whole_words": False, "use_regex": False, "scan_depth": None,
    "probability": 100, "use_probability": False, "position": 0, "depth": None,
    "role": "system", "priority": 0, "sticky": 0, "cooldown": 0, "delay": 0,
    "group": None, "group_override": False, "group_weight": 100,
    "prevent_recursion": False, "exclude_recursion": False,
    "delay_until_recursion": False, "vectorized": False,
}


def compile_character_book(
    source: dict[str, Any],
    book_id: str,
    allow_reduced_fidelity: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    findings = validate_spec.validate_spec(source)
    if findings.errors:
        raise ValueError("LoreForge source has errors: " + "; ".join(findings.errors))
    books = [book for book in source["books"] if book.get("id") == book_id]
    if len(books) != 1:
        raise ValueError(f"Expected exactly one book with id '{book_id}'")
    book = books[0]
    entries: list[dict[str, Any]] = []
    stable_id_map: dict[str, int] = {}
    omitted: dict[str, list[str]] = {}
    for index, entry in enumerate(book["entries"]):
        stable_id = entry["stable_id"]
        stable_id_map[stable_id] = index
        entries.append({
            "keys": list(entry["keywords"]),
            "content": entry["content"],
            "constant": entry["state"] == "constant",
            "enabled": entry["state"] != "disabled",
            "insertion_order": entry["order"],
        })
        non_default = [key for key, default in ADVANCED_DEFAULTS.items() if entry.get(key) != default]
        if entry.get("priority") == entry.get("order"):
            non_default = [key for key in non_default if key != "priority"]
        if non_default:
            omitted[stable_id] = non_default
    if omitted and not allow_reduced_fidelity:
        details = "; ".join(f"{stable_id}: {', '.join(keys)}" for stable_id, keys in omitted.items())
        raise ValueError(
            "Embedded Character Book would require reduced fidelity because activation-semantic "
            f"settings are not represented by the observed subset ({details}). "
            "Pass allow_reduced_fidelity=True only after explicit approval."
        )
    return {"entries": entries}, {
        "schema": "lumiverse-toolkit.character-book-compilation/v1",
        "source_schema": "loreforge.lumiverse.v1",
        "book_id": book_id,
        "book_name": book.get("name", ""),
        "target": "character_card_v3_embedded_book_observed_subset",
        "stable_id_map": stable_id_map,
        "omitted_settings": omitted,
        "reduced_fidelity_approved": bool(omitted and allow_reduced_fidelity),
        "native_lumiverse_full_fidelity": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--book-id", required=True)
    parser.add_argument("--out-book", type=Path, required=True)
    parser.add_argument("--out-manifest", type=Path, required=True)
    parser.add_argument("--allow-reduced-fidelity", action="store_true")
    args = parser.parse_args()
    if args.out_book.exists() or args.out_manifest.exists():
        raise SystemExit("ERROR: output already exists")
    try:
        source = json.loads(args.spec.read_text(encoding="utf-8"))
        book, manifest = compile_character_book(
            source, args.book_id, allow_reduced_fidelity=args.allow_reduced_fidelity
        )
        args.out_book.write_text(json.dumps(book, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        args.out_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}")
    print(args.out_book)
    print(args.out_manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
