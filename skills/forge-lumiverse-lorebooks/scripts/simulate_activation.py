#!/usr/bin/env python3
"""Run deterministic activation tests against a LoreForge specification.

This is a deliberately bounded simulator. It tests literal/regex keyword and
secondary logic plus a simplified group and budget pass. It cannot reproduce
embeddings, persistent timing state, probability rolls, or Lumiverse internals.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Evaluation:
    active: list[dict[str, Any]] = field(default_factory=list)
    uncertain: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: cannot read {path}: {exc}")


def keyword_matches(text: str, keyword: str, entry: dict[str, Any]) -> bool:
    flags = 0 if entry.get("case_sensitive") else re.IGNORECASE
    if entry.get("use_regex"):
        try:
            return re.search(keyword, text, flags) is not None
        except re.error:
            return False
    pattern = re.escape(keyword)
    if entry.get("match_whole_words"):
        pattern = rf"(?<!\w){pattern}(?!\w)"
    return re.search(pattern, text, flags) is not None


def recent_text(messages: list[str], scan_depth: int | None) -> str:
    selected = messages if scan_depth is None else messages[-scan_depth:]
    return "\n".join(selected)


def logic_matches(entry: dict[str, Any], text: str) -> bool:
    primary = any(keyword_matches(text, key, entry) for key in entry.get("keywords", []))
    secondary_hits = [
        keyword_matches(text, key, entry) for key in entry.get("secondary_keywords", [])
    ]
    any_secondary = any(secondary_hits)
    all_secondary = bool(secondary_hits) and all(secondary_hits)
    logic = entry.get("selective_logic")
    if logic == "and":
        matched = primary and (any_secondary if secondary_hits else True)
    elif logic == "or":
        matched = primary or any_secondary
    elif logic == "not":
        matched = primary and not any_secondary
    elif logic == "not_all":
        matched = primary and not all_secondary
    else:
        matched = False
    return matched


def entry_matches(entry: dict[str, Any], messages: list[str], evaluation: Evaluation) -> bool:
    state = entry.get("state")
    stable_id = str(entry.get("stable_id"))
    if state == "disabled" or entry.get("delay_until_recursion"):
        return False
    if state == "constant":
        return True

    text = recent_text(messages, entry.get("scan_depth"))
    matched = logic_matches(entry, text)

    if not matched and entry.get("vectorized"):
        evaluation.uncertain.append(stable_id)
        evaluation.notes.append(f"{stable_id}: embedding similarity cannot be simulated")
    if matched and entry.get("use_probability") and entry.get("probability", 100) < 100:
        evaluation.uncertain.append(stable_id)
        evaluation.notes.append(f"{stable_id}: probability gate is nondeterministic")
        return False
    if matched and (entry.get("sticky") or entry.get("cooldown") or entry.get("delay")):
        evaluation.uncertain.append(stable_id)
        evaluation.notes.append(f"{stable_id}: persistent timing state requires Lumiverse live testing")
    return matched


def apply_recursion(
    all_entries: list[dict[str, Any]],
    active: list[dict[str, Any]],
    max_passes: int,
    evaluation: Evaluation,
) -> list[dict[str, Any]]:
    active_by_id = {entry["stable_id"]: entry for entry in active}
    frontier = list(active)
    for pass_number in range(1, max_passes + 1):
        source_parts = [
            entry.get("content", "")
            for entry in frontier
            if not entry.get("prevent_recursion") and not entry.get("exclude_recursion")
        ]
        source_text = "\n".join(source_parts)
        if not source_text:
            break
        discovered: list[dict[str, Any]] = []
        for entry in all_entries:
            stable_id = entry["stable_id"]
            if stable_id in active_by_id or entry.get("state") in {"disabled", "constant"}:
                continue
            if logic_matches(entry, source_text):
                if entry.get("use_probability") and entry.get("probability", 100) < 100:
                    evaluation.uncertain.append(stable_id)
                    evaluation.notes.append(
                        f"{stable_id}: recursion matched but probability gate is nondeterministic"
                    )
                    continue
                discovered.append(entry)
                active_by_id[stable_id] = entry
                evaluation.notes.append(
                    f"recursion pass {pass_number} activated {stable_id}"
                )
        if not discovered:
            break
        frontier = discovered
    return list(active_by_id.values())


def choose_groups(entries: list[dict[str, Any]], evaluation: Evaluation) -> list[dict[str, Any]]:
    ungrouped: list[dict[str, Any]] = []
    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        group = entry.get("group")
        if group:
            groups.setdefault(group, []).append(entry)
        else:
            ungrouped.append(entry)
    for group, candidates in groups.items():
        overrides = [x for x in candidates if x.get("group_override")]
        if overrides:
            winner = sorted(overrides, key=lambda x: (-x.get("priority", 0), x["stable_id"]))[0]
        else:
            winner = sorted(
                candidates,
                key=lambda x: (-x.get("group_weight", 100), -x.get("priority", 0), x["stable_id"]),
            )[0]
            if len(candidates) > 1:
                evaluation.uncertain.extend(x["stable_id"] for x in candidates)
                evaluation.notes.append(
                    f"group {group}: real weighted selection is random; simulator chose {winner['stable_id']}"
                )
        ungrouped.append(winner)
    return ungrouped


def apply_budget(
    entries: list[dict[str, Any]],
    max_entries: int | None,
    max_tokens: int | None,
    min_priority: int,
    evaluation: Evaluation,
) -> list[dict[str, Any]]:
    constants = [x for x in entries if x.get("state") == "constant"]
    conditional = [
        x for x in entries if x.get("state") != "constant" and x.get("priority", 0) >= min_priority
    ]
    conditional.sort(key=lambda x: (-x.get("priority", 0), x.get("order", 0), x["stable_id"]))
    kept = list(constants)
    if max_entries is not None:
        room = max(0, max_entries - len(constants))
        dropped = conditional[room:]
        conditional = conditional[:room]
        if dropped:
            evaluation.notes.append("entry cap dropped: " + ", ".join(x["stable_id"] for x in dropped))
    candidates = kept + conditional
    if max_tokens is None:
        return candidates

    final: list[dict[str, Any]] = []
    used = 0
    for entry in candidates:
        cost = (len(entry.get("content", "")) + 3) // 4
        if entry.get("state") == "constant" or used + cost <= max_tokens:
            final.append(entry)
            used += cost
        else:
            evaluation.notes.append(f"token budget dropped: {entry['stable_id']}")
    if used > max_tokens:
        evaluation.notes.append(
            f"constants alone force estimated use to {used} tokens above budget {max_tokens}"
        )
    return final


def evaluate_case(spec: dict[str, Any], case: dict[str, Any]) -> Evaluation:
    evaluation = Evaluation()
    selected_books = set(case.get("books") or [book["id"] for book in spec.get("books", [])])
    messages = case.get("messages", [])
    all_entries: list[dict[str, Any]] = []
    for book in spec.get("books", []):
        if book.get("id") not in selected_books:
            continue
        all_entries.extend(book.get("entries", []))
    entries = [entry for entry in all_entries if entry_matches(entry, messages, evaluation)]
    runtime = spec.get("recommended_runtime", {})
    entries = apply_recursion(
        all_entries,
        entries,
        runtime.get("max_recursion_passes", 3),
        evaluation,
    )
    entries = choose_groups(entries, evaluation)
    entries = apply_budget(
        entries,
        case.get("max_activated_entries", runtime.get("max_activated_entries")),
        case.get("max_token_budget", runtime.get("max_token_budget")),
        runtime.get("min_priority", 0),
        evaluation,
    )
    evaluation.active = sorted(entries, key=lambda x: (x.get("position", 0), x.get("order", 0)))
    return evaluation


def assess_case(evaluation: Evaluation, case: dict[str, Any]) -> dict[str, Any]:
    """Classify one bounded case without treating uncertainty as success."""
    active = [entry["stable_id"] for entry in evaluation.active]
    uncertain = sorted(set(evaluation.uncertain))
    failures: list[str] = []
    for stable_id in case.get("expected_active", []):
        if stable_id not in active and stable_id not in uncertain:
            failures.append(f"expected active but absent: {stable_id}")
    for stable_id in case.get("expected_inactive", []):
        if stable_id in active and stable_id not in uncertain:
            failures.append(f"expected inactive but active: {stable_id}")
    if failures:
        status = "FAIL"
    elif uncertain:
        status = "UNPROVEN"
    else:
        status = "PASS"
    return {
        "active": active,
        "uncertain": uncertain,
        "failures": failures,
        "notes": evaluation.notes,
        "status": status,
    }


def render_report(spec_path: Path, tests_path: Path, results: list[dict[str, Any]]) -> str:
    failures = sum(1 for result in results if result["status"] == "FAIL")
    unproven = sum(1 for result in results if result["status"] == "UNPROVEN")
    overall = "FAIL" if failures else "UNPROVEN" if unproven else "PASS"
    lines = [
        "# Activation Test Report",
        "",
        f"- Spec: `{spec_path.name}`",
        f"- Tests: `{tests_path.name}`",
        f"- Status: {overall}",
        f"- Cases: {len(results)}",
        f"- Failing cases: {failures}",
        f"- Unproven cases: {unproven}",
        "",
        "> This bounded simulator does not reproduce semantic embeddings, probability rolls, persistent sticky/cooldown/delay state, or Lumiverse internals. Confirm with Dry Run and World Book Diagnostics.",
        "",
    ]
    for result in results:
        lines.extend(
            [
                f"## {result['name']}",
                "",
                f"- Active: {', '.join(result['active']) or '(none)'}",
                f"- Uncertain: {', '.join(result['uncertain']) or '(none)'}",
                f"- Result: {result['status']}",
            ]
        )
        if result["failures"]:
            lines.append("- Failures: " + "; ".join(result["failures"]))
        if result["notes"]:
            lines.append("- Notes: " + "; ".join(dict.fromkeys(result["notes"])))
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("tests", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    spec = load_json(args.spec)
    tests = load_json(args.tests)
    if tests.get("schema") != "loreforge.activation-tests.v1":
        raise SystemExit("ERROR: unsupported activation test schema")

    results: list[dict[str, Any]] = []
    failed = False
    unproven = False
    for index, case in enumerate(tests.get("cases", [])):
        if not isinstance(case, dict) or not isinstance(case.get("messages"), list):
            raise SystemExit(f"ERROR: tests case {index} is malformed")
        evaluation = evaluate_case(spec, case)
        result = assess_case(evaluation, case)
        result["name"] = case.get("name", f"Case {index + 1}")
        failed = failed or result["status"] == "FAIL"
        unproven = unproven or result["status"] == "UNPROVEN"
        results.append(result)

    report = render_report(args.spec, args.tests, results)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)
    return 1 if failed else 2 if unproven else 0


if __name__ == "__main__":
    sys.exit(main())
