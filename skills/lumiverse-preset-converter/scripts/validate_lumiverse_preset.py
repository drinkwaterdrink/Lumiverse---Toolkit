#!/usr/bin/env python3
"""Conservative static checks for a native Lumiverse preset export.

The native envelope is version-sensitive. This validator checks stable invariants and
reports the observed envelope; it does not replace import or Dry Run tests.
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

VALID_ROLES = {"system", "user", "assistant", "user_append", "assistant_append"}
VALID_POSITIONS = {"pre_history", "post_history", "in_history"}
VALID_MARKERS = {
    None,
    "category",
    "char_description",
    "char_personality",
    "scenario",
    "persona",
    "mes_examples",
    "system_prompt",
    "post_history_instructions",
    "chat_history",
    "world_info_before",
    "world_info_after",
}
VAR_RE = re.compile(r"\{\{var::([A-Za-z0-9_]+)\}\}")
NAME_RE = re.compile(r"^[A-Za-z0-9_]+$")


def unwrap(raw):
    if isinstance(raw, dict) and isinstance(raw.get("preset"), dict):
        return raw["preset"], "preset"
    if (
        isinstance(raw, dict)
        and isinstance(raw.get("data"), dict)
        and isinstance(raw["data"].get("preset"), dict)
    ):
        return raw["data"]["preset"], "data.preset"
    return raw, "root"


def embedded_regex_scripts(preset):
    extensions = preset.get("extensions")
    if not isinstance(extensions, dict):
        return []
    scripts = extensions.get("regex_scripts")
    return scripts if isinstance(scripts, list) else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("preset")
    args = ap.parse_args()

    raw = json.loads(Path(args.preset).read_text(encoding="utf-8"))
    preset, envelope = unwrap(raw)
    errors = []
    warnings = []
    if not isinstance(preset, dict):
        errors.append("preset payload must be a JSON object")
        preset = {}

    blocks = preset.get("blocks", [])
    if not isinstance(blocks, list):
        errors.append("blocks must be an array")
        blocks = []
    if not blocks:
        errors.append("preset contains no prompt blocks")

    ids = [block.get("id") for block in blocks if isinstance(block, dict)]
    counts = collections.Counter(ids)
    bad_ids = sorted(str(key) for key, count in counts.items() if not key or count > 1)
    if bad_ids:
        errors.append(f"duplicate or blank block IDs: {bad_ids}")
    id_to_block = {
        block.get("id"): block
        for block in blocks
        if isinstance(block, dict) and block.get("id")
    }

    definitions = {}
    variable_ids = []
    for index, block in enumerate(blocks):
        if not isinstance(block, dict):
            errors.append(f"block {index}: must be an object")
            continue
        name = block.get("name") or f"block {index}"
        role = block.get("role")
        position = block.get("position")
        marker = block.get("marker")
        if role not in VALID_ROLES:
            errors.append(f"{name}: invalid role {role!r}")
        if position not in VALID_POSITIONS:
            errors.append(f"{name}: invalid position {position!r}")
        if marker not in VALID_MARKERS:
            errors.append(f"{name}: unknown marker {marker!r}")
        group = block.get("group")
        if group:
            parent = id_to_block.get(group)
            if parent is None:
                errors.append(f"{name}: missing group block {group}")
            elif parent.get("marker") != "category":
                warnings.append(f"{name}: group target {group} is not a category marker")
        if position == "in_history":
            depth = block.get("depth")
            if not isinstance(depth, (int, float)) or isinstance(depth, bool) or depth < 0:
                errors.append(f"{name}: in_history requires a non-negative numeric depth")
        for list_key in ("injectionTrigger", "characterTagTrigger"):
            if list_key in block and not isinstance(block.get(list_key), list):
                errors.append(f"{name}: {list_key} must be an array")

        variables = block.get("variables", []) or []
        if not isinstance(variables, list):
            errors.append(f"{name}: variables must be an array")
            continue
        for variable in variables:
            if not isinstance(variable, dict):
                errors.append(f"{name}: variable definition must be an object")
                continue
            var_name = variable.get("name")
            var_id = variable.get("id")
            if not var_name or not NAME_RE.fullmatch(str(var_name)):
                errors.append(f"{name}: invalid Prompt Variable name {var_name!r}")
                continue
            if not var_id:
                warnings.append(f"{name}/{var_name}: missing variable ID")
            else:
                variable_ids.append(var_id)
            prior = definitions.get(var_name)
            if prior and prior.get("defaultValue") != variable.get("defaultValue"):
                warnings.append(f"Prompt Variable {var_name} has conflicting defaults")
            definitions[var_name] = variable

            minimum = variable.get("min")
            maximum = variable.get("max")
            default = variable.get("defaultValue")
            if isinstance(minimum, (int, float)) and isinstance(maximum, (int, float)):
                if minimum > maximum:
                    errors.append(f"{name}/{var_name}: min exceeds max")
                if isinstance(default, (int, float)) and not minimum <= default <= maximum:
                    errors.append(f"{name}/{var_name}: default is outside min/max")
            options = variable.get("options")
            if isinstance(options, list):
                option_ids = [opt.get("id") for opt in options if isinstance(opt, dict)]
                option_values = [opt.get("value") for opt in options if isinstance(opt, dict)]
                if len(set(option_ids)) != len(option_ids) or any(x is None for x in option_ids):
                    errors.append(f"{name}/{var_name}: option IDs must be unique and nonblank")
                if default is not None and default not in option_values and default not in option_ids:
                    errors.append(f"{name}/{var_name}: default does not match an option")

    duplicate_variable_ids = sorted(
        str(key) for key, count in collections.Counter(variable_ids).items() if count > 1
    )
    if duplicate_variable_ids:
        errors.append(f"duplicate Prompt Variable IDs: {duplicate_variable_ids}")

    persisted = preset.get("promptVariables", {}) or {}
    if not isinstance(persisted, dict):
        errors.append("promptVariables must be an object keyed by block ID")
        persisted = {}
    for block_id, values in persisted.items():
        block = id_to_block.get(block_id)
        if block is None:
            errors.append(f"promptVariables references missing block {block_id}")
            continue
        if not isinstance(values, dict):
            errors.append(f"promptVariables[{block_id}] must be an object")
            continue
        block_names = {
            variable.get("name")
            for variable in (block.get("variables") or [])
            if isinstance(variable, dict)
        }
        for var_name in values:
            if var_name not in block_names:
                errors.append(
                    f"promptVariables[{block_id}] contains undefined variable {var_name}"
                )

    active = "\n".join(
        str(block.get("content", ""))
        for block in blocks
        if isinstance(block, dict) and block.get("enabled", True)
    )
    refs = set(VAR_RE.findall(active))
    missing = sorted(refs - set(definitions))
    if missing:
        errors.append("undefined Prompt Variables: " + ", ".join(missing))

    reasoning_prefixes = len(
        re.findall(r"\{\{reasoningPrefix(?:::[^}]*)?\}\}", active)
    )
    reasoning_suffixes = len(
        re.findall(r"\{\{reasoningSuffix(?:::[^}]*)?\}\}", active)
    )
    if reasoning_prefixes != reasoning_suffixes:
        errors.append(
            f"reasoning boundary mismatch: {reasoning_prefixes} prefix / "
            f"{reasoning_suffixes} suffix"
        )
    if re.search(r"\{\{random::[^}\n]+::[^}\n]+::[^}\n]+", active):
        warnings.append("categorical random syntax found; verify source/target semantics")

    regex_scripts = embedded_regex_scripts(preset)
    report = {
        "preset": preset.get("name"),
        "schema_version": preset.get("schemaVersion"),
        "envelope": envelope,
        "blocks": len(blocks),
        "enabled": sum(
            bool(block.get("enabled", True)) for block in blocks if isinstance(block, dict)
        ),
        "prompt_variable_definitions": len(definitions),
        "persisted_prompt_variable_blocks": len(persisted),
        "embedded_regex_scripts": len(regex_scripts),
        "reasoning_prefixes": reasoning_prefixes,
        "reasoning_suffixes": reasoning_suffixes,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
