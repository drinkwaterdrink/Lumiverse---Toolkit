#!/usr/bin/env python3
"""Validate the platform-neutral LoreForge specification.

This validator checks the documented Lumiverse concepts represented by the
neutral spec. It does not validate an undocumented native Lumiverse schema.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ALLOWED_SCOPES = {"character", "persona", "global", "manual"}
ALLOWED_STATES = {"conditional", "constant", "disabled"}
ALLOWED_ROLES = {"system", "user", "assistant"}
ALLOWED_LOGIC = {"and", "or", "not", "not_all"}
ALLOWED_SHAPES = {"focused", "tiered", "arc", "sandbox", "weaver_companion"}
ALLOWED_CREATIVE_AUTHORITY = {
    "ask_before_new_canon",
    "proposals_only",
    "creative_license",
}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: file not found: {path}")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"ERROR: {path} is not valid UTF-8: {exc}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: JSON parse failure in {path}: {exc}")


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def potential_keyword_match(content: str, keyword: str, entry: dict[str, Any]) -> bool:
    flags = 0 if entry.get("case_sensitive") else re.IGNORECASE
    if entry.get("use_regex"):
        try:
            return re.search(keyword, content, flags) is not None
        except re.error:
            return False
    pattern = re.escape(keyword)
    if entry.get("match_whole_words"):
        pattern = rf"(?<!\w){pattern}(?!\w)"
    return re.search(pattern, content, flags) is not None


def audit_recursion_graph(findings: Findings, entries: list[dict[str, Any]]) -> None:
    usable = {
        entry.get("stable_id"): entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("stable_id"), str)
    }
    graph: dict[str, set[str]] = {stable_id: set() for stable_id in usable}
    for source_id, source in usable.items():
        if source.get("state") == "disabled" or source.get("prevent_recursion") or source.get("exclude_recursion"):
            continue
        content = source.get("content", "")
        for target_id, target in usable.items():
            if target_id == source_id or target.get("state") in {"disabled", "constant"}:
                continue
            if any(
                potential_keyword_match(content, keyword, target)
                for keyword in target.get("keywords", [])
            ):
                graph[source_id].add(target_id)
        if len(graph[source_id]) > 5:
            findings.warn(
                source_id,
                f"content may fan out recursively to {len(graph[source_id])} entries",
            )

    visited: set[str] = set()
    stack: list[str] = []
    on_stack: set[str] = set()
    cycles: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        visited.add(node)
        stack.append(node)
        on_stack.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visit(neighbor)
            elif neighbor in on_stack:
                start = stack.index(neighbor)
                cycle = tuple(stack[start:] + [neighbor])
                cycles.add(cycle)
        stack.pop()
        on_stack.remove(node)

    for node in graph:
        if node not in visited:
            visit(node)
    for cycle in sorted(cycles):
        findings.warn("recursion graph", "potential cycle: " + " -> ".join(cycle))


def require_text(findings: Findings, where: str, obj: dict[str, Any], key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        findings.error(where, f"{key!r} must be non-empty text")
        return ""
    return value.strip()


def require_string_list(
    findings: Findings, where: str, obj: dict[str, Any], key: str
) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
        findings.error(where, f"{key!r} must be an array of strings")
        return []
    cleaned = [x.strip() for x in value if x.strip()]
    if len(cleaned) != len(set(x.casefold() for x in cleaned)):
        findings.warn(where, f"{key!r} contains duplicate values")
    return cleaned


def validate_entry(
    findings: Findings,
    book_id: str,
    entry: Any,
    stable_ids: set[str],
    keyword_owners: dict[str, list[str]],
) -> tuple[int, bool]:
    if not isinstance(entry, dict):
        findings.error(book_id, "entry must be an object")
        return 0, False

    stable_id = require_text(findings, book_id, entry, "stable_id")
    where = f"{book_id}/{stable_id or '<missing-id>'}"
    if stable_id in stable_ids:
        findings.error(where, "stable_id is duplicated")
    elif stable_id:
        stable_ids.add(stable_id)

    require_text(findings, where, entry, "title")
    content = require_text(findings, where, entry, "content")
    require_text(findings, where, entry, "content_rationale")
    require_text(findings, where, entry, "activation_rationale")

    state = entry.get("state")
    if state not in ALLOWED_STATES:
        findings.error(where, f"state must be one of {sorted(ALLOWED_STATES)}")

    keywords = require_string_list(findings, where, entry, "keywords")
    secondary = require_string_list(findings, where, entry, "secondary_keywords")
    vectorized = entry.get("vectorized") is True
    if state == "conditional" and not keywords and not vectorized:
        findings.error(where, "conditional entry needs a keyword or vectorized intent")
    if state == "constant" and keywords:
        findings.warn(where, "constant entries do not need activation keywords")
    if vectorized and not keywords:
        findings.warn(where, "keep exact names as keywords even when vectorized")

    logic = entry.get("selective_logic")
    if logic not in ALLOWED_LOGIC:
        findings.error(where, f"selective_logic must be one of {sorted(ALLOWED_LOGIC)}")
    if logic in {"and", "not", "not_all"} and not secondary:
        findings.warn(where, f"{logic} logic has no secondary keywords")

    for key in keywords:
        keyword_owners[key.casefold()].append(stable_id)

    for flag in (
        "case_sensitive",
        "match_whole_words",
        "use_regex",
        "use_probability",
        "group_override",
        "prevent_recursion",
        "exclude_recursion",
        "delay_until_recursion",
        "vectorized",
    ):
        if not isinstance(entry.get(flag), bool):
            findings.error(where, f"{flag!r} must be boolean")

    scan_depth = entry.get("scan_depth")
    if scan_depth is not None and (not isinstance(scan_depth, int) or scan_depth < 1):
        findings.error(where, "scan_depth must be null or an integer >= 1")

    probability = entry.get("probability")
    if not is_number(probability) or not 0 <= probability <= 100:
        findings.error(where, "probability must be between 0 and 100")
    if entry.get("use_probability") is False and probability != 100:
        findings.warn(where, "probability differs from 100 while use_probability is false")

    position = entry.get("position")
    if not isinstance(position, int) or position not in range(7):
        findings.error(where, "position must be an integer from 0 through 6")
    depth = entry.get("depth")
    if position == 4:
        if not isinstance(depth, int) or depth < 0:
            findings.error(where, "At Depth entries require a nonnegative integer depth")
        elif depth <= 2 and entry.get("category") not in {
            "current_state",
            "quest",
            "danger",
            "directive",
        }:
            findings.warn(where, "depth 0–2 is unusually strong for background lore")
    elif depth is not None:
        findings.warn(where, "depth is ignored unless position is 4")

    if entry.get("role") not in ALLOWED_ROLES:
        findings.error(where, f"role must be one of {sorted(ALLOWED_ROLES)}")
    elif entry.get("role") != "system":
        findings.warn(where, "non-System role needs an explicit message-like effect")

    for key in ("order", "priority"):
        value = entry.get(key)
        if not isinstance(value, int) or value < 0:
            findings.error(where, f"{key!r} must be a nonnegative integer")

    for key in ("sticky", "cooldown", "delay"):
        value = entry.get(key)
        if not isinstance(value, int) or value < 0:
            findings.error(where, f"{key!r} must be a nonnegative integer")

    group = entry.get("group")
    if group is not None and (not isinstance(group, str) or not group.strip()):
        findings.error(where, "group must be null or non-empty text")
    weight = entry.get("group_weight")
    if not isinstance(weight, int) or weight <= 0:
        findings.error(where, "group_weight must be a positive integer")
    if entry.get("group_override") and group is None:
        findings.warn(where, "group_override has no effect without a group")
    tests = entry.get("tests")
    if not isinstance(tests, dict):
        findings.error(where, "tests must be an object")
    else:
        positive = require_string_list(findings, where, tests, "positive")
        negative = require_string_list(findings, where, tests, "negative")
        require_string_list(findings, where, tests, "collision")
        if state == "conditional" and not positive:
            findings.error(where, "conditional entry needs at least one positive test")
        if state == "conditional" and not negative:
            findings.error(where, "conditional entry needs at least one negative test")

    estimated_tokens = (len(content) + 3) // 4
    if estimated_tokens > 500:
        findings.warn(where, f"entry is large at roughly {estimated_tokens} tokens")
    return estimated_tokens, state == "constant"


def validate_spec(data: Any) -> Findings:
    findings = Findings()
    if not isinstance(data, dict):
        findings.error("root", "spec must be a JSON object")
        return findings
    if data.get("schema") != "loreforge.lumiverse.v1":
        findings.error("root", "schema must be 'loreforge.lumiverse.v1'")

    project = data.get("project")
    if not isinstance(project, dict):
        findings.error("project", "project must be an object")
    else:
        require_text(findings, "project", project, "name")
        shape = project.get("build_shape")
        if shape not in ALLOWED_SHAPES:
            findings.error("project", f"build_shape must be one of {sorted(ALLOWED_SHAPES)}")
        creative_authority = project.get("creative_authority")
        if creative_authority not in ALLOWED_CREATIVE_AUTHORITY:
            findings.error(
                "project",
                "creative_authority must be one of "
                f"{sorted(ALLOWED_CREATIVE_AUTHORITY)}",
            )
        if not isinstance(project.get("source_authority"), list):
            findings.error("project", "source_authority must be an array")

    runtime = data.get("recommended_runtime")
    if not isinstance(runtime, dict):
        findings.error("recommended_runtime", "recommended_runtime must be an object")
        runtime = {}
    for key in ("global_scan_depth", "max_activated_entries", "max_token_budget"):
        value = runtime.get(key)
        if value is not None and (not isinstance(value, int) or value < 1):
            findings.error("recommended_runtime", f"{key} must be null or an integer >= 1")
    passes = runtime.get("max_recursion_passes")
    if not isinstance(passes, int) or passes < 0:
        findings.error("recommended_runtime", "max_recursion_passes must be >= 0")
    min_priority = runtime.get("min_priority")
    if not isinstance(min_priority, int) or min_priority < 0:
        findings.error("recommended_runtime", "min_priority must be >= 0")

    books = data.get("books")
    if not isinstance(books, list) or not books:
        findings.error("books", "books must be a non-empty array")
        return findings

    book_ids: set[str] = set()
    stable_ids: set[str] = set()
    keyword_owners: dict[str, list[str]] = defaultdict(list)
    all_entries: list[dict[str, Any]] = []
    constant_tokens = 0
    constant_count = 0
    for index, book in enumerate(books):
        where = f"books[{index}]"
        if not isinstance(book, dict):
            findings.error(where, "book must be an object")
            continue
        book_id = require_text(findings, where, book, "id")
        if book_id in book_ids:
            findings.error(where, "book id is duplicated")
        elif book_id:
            book_ids.add(book_id)
        require_text(findings, where, book, "name")
        require_text(findings, where, book, "description")
        scope = book.get("scope_recommendation")
        if scope not in ALLOWED_SCOPES:
            findings.error(where, f"scope_recommendation must be one of {sorted(ALLOWED_SCOPES)}")
        entries = book.get("entries")
        if not isinstance(entries, list) or not entries:
            findings.error(where, "entries must be a non-empty array")
            continue
        for entry in entries:
            if isinstance(entry, dict):
                all_entries.append(entry)
            tokens, is_constant = validate_entry(
                findings, book_id or where, entry, stable_ids, keyword_owners
            )
            if is_constant:
                constant_tokens += tokens
                constant_count += 1

    for keyword, owners in sorted(keyword_owners.items()):
        unique = sorted(set(owners))
        if keyword and len(unique) > 1:
            findings.warn("keyword collision", f"{keyword!r} is owned by {', '.join(unique)}")

    audit_recursion_graph(findings, all_entries)

    max_entries = runtime.get("max_activated_entries")
    max_tokens = runtime.get("max_token_budget")
    if isinstance(max_entries, int) and constant_count > max_entries:
        findings.error(
            "recommended_runtime",
            f"{constant_count} constants exceed max_activated_entries {max_entries}; constants are never evicted",
        )
    if isinstance(max_tokens, int) and constant_tokens > max_tokens:
        findings.error(
            "recommended_runtime",
            f"constants total roughly {constant_tokens} tokens, above max_token_budget {max_tokens}",
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--json", action="store_true", help="emit machine-readable findings")
    args = parser.parse_args()

    findings = validate_spec(load_json(args.spec))
    if args.json:
        print(json.dumps({"errors": findings.errors, "warnings": findings.warnings}, indent=2))
    else:
        for item in findings.errors:
            print(f"ERROR: {item}")
        for item in findings.warnings:
            print(f"WARNING: {item}")
        print(f"SUMMARY: {len(findings.errors)} error(s), {len(findings.warnings)} warning(s)")
    return 1 if findings.errors else 0


if __name__ == "__main__":
    sys.exit(main())
