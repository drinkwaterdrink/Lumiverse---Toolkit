---
name: lumiverse-preset-converter
description: Convert, audit, repair, and certify SillyTavern Chat Completion presets as import-ready Lumiverse Loom presets, including prompt order, macros, variable lifetime, randomness, completion settings, embedded Regex, dependencies, and Dry Run review. Use for SillyTavern-to-Lumiverse preset migration or compatibility work; do not use for non-Chat-Completion preset families or unrelated native preset authoring.
---

# Lumiverse Preset Converter

Work only on **SillyTavern Chat Completion → Lumiverse** preset migration. Convert the source's effective behavior, not merely its JSON keys.

## Evidence and references

Use this order when evidence conflicts:

1. Current observed Lumiverse Dry Run/runtime behavior.
2. Current observed SillyTavern runtime behavior.
3. Current official or user-supplied Lumiverse documentation.
4. Current official or user-supplied SillyTavern documentation.
5. A fresh native Lumiverse export from the user's target build.
6. Creator notes and extension documentation.
7. Clearly labeled inference.

Never turn inference or historical serialization into a platform fact. Preserve conflicts and label the uncertainty.

- For a new full conversion or deep audit, read [references/SOP.md](references/SOP.md) completely before editing.
- For target-envelope and embedded-Regex decisions, also read [references/NATIVE_REFERENCE.md](references/NATIVE_REFERENCE.md).
- For a Dry Run review, read [references/DRY_RUN_REVIEW.md](references/DRY_RUN_REVIEW.md) and the relevant source preset.
- Use [assets/CONVERSION_REPORT.md](assets/CONVERSION_REPORT.md) and [assets/DRY_RUN_FIXTURE.md](assets/DRY_RUN_FIXTURE.md) as reusable output templates when useful.

## Inputs

Prefer the source preset JSON, companion Regex, creator notes, source and target model/provider, a fresh native Loom export from the target Lumiverse build, and representative Dry Run output. Continue best-effort when optional evidence is missing, but state exactly what cannot be proven. If exact importable serialization cannot be established without a fresh export, ask for one instead of inventing the envelope.

Respect the user's latest target export as authoritative for current settings and selections. Preserve project-specific filename, internal-name, version-increment, and bundled-Regex naming rules. Never impose one project's naming convention on another.

## Choose the operating mode

### Convert

1. Freeze and hash the source artifacts.
2. Run `scripts/audit_st_chat_completion.py` on the source JSON.
3. Reconstruct every effective `prompt_order` variant; definition-array order is not authoritative.
4. Inventory prompts, roles, placements, depths, triggers, utility behavior, samplers, macros, variables, randomness, reasoning, Regex, and external dependencies.
5. Build a source-to-target manifest and behavior graph before editing.
6. Clone the current native Lumiverse envelope and build a behaviorally faithful parity version.
7. Validate the target with `scripts/validate_lumiverse_preset.py` and validate Regex syntax with `scripts/validate_regex.mjs`.
8. Bundle/link converted Regex inside the actual Loom export when the fresh native schema supports it. Produce a standalone Regex file only when requested or required by the target workflow.
9. After parity is sound, add requested native organization or controls such as groups, Prompt Variables, placement selectors, profiles, model adapters, triggers, or Regex Actions.
10. Revalidate and provide the import-ready artifact plus a concise evidence-backed report.

### Audit or repair

Inspect first. Compare the source and target manifests, run the validators, and report exact P0/P1/P2/P3 findings by block or script. Patch only proven failures and requested enhancements, preserve unrelated settings, then rerun validation.

### Dry Run review

Compare the assembled messages and final PARAMETERS with the converted JSON. Check unresolved macros, duplicate structural data, block order, role/position/depth, route-specific blocks, variable lifetime, RNG caching, reasoning boundaries, state carry, Regex effects, and selected profiles/Prompt Variables. Separate **PASS**, **FAIL**, **UNPROVEN**, and **RUNTIME TEST REQUIRED**.

## Conversion invariants

- Preserve source blocks, defaults, enabled states, prompt boundaries, and user-agency contract unless a change is required or requested; document every semantic change.
- Keep preset-authored Main Prompt text separate from the character `system_prompt` structural field. Apply the same distinction to preset Post-History Instructions and card overrides.
- Classify every SillyTavern local variable by intended lifetime before rewriting it. Use Lumiverse `.` only for one-evaluation scratch state, `@` for per-chat persistence, `$` for cross-chat state, and Prompt Variables for human-selected preset options.
- Audit every `random`, `pick`, and `roll`. Preserve categorical versus numeric behavior, emulate stable source picks when required, and cache one logical draw once.
- Do not place live macro syntax in examples intended to reach the model literally.
- Keep stored text, provider-visible text, response-saved text, display-rendered text, and memory-ingested text distinct. Use only Regex placements/targets verified in the current target build.
- Do not assume an unknown extension macro, extension ID, Regex Script ID, provider feature, or model-name pattern.
- Do not redesign prose or optimize token use before parity is established.
- Treat static scripts as diagnostics, not proof of runtime parity.

## Deliverables and certification

For a full conversion, provide the import-ready Loom preset, embedded Regex when supported, source-to-target manifest, audit/validation summary, dependencies, semantic changelog, known limitations, and Dry Run test plan. Produce separate Parity and Native files when native enhancements materially differ; otherwise avoid redundant files.

Never certify a preset as native or parity-complete with an unresolved P0 such as malformed serialization, dangling references, missing/duplicate structural data, false persistence, unresolved mandatory macros, changed random stability, destructive Regex-plane mismatch, duplicated reasoning boundaries, or a missing required dependency. Without a representative Lumiverse Dry Run, label runtime certification as pending rather than claiming full success.
