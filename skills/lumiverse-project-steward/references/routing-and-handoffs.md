# Routing and Handoffs

## Direct versus coordinated work

Route directly to a specialist when the request produces or changes one self-contained artifact and the user does not ask for continuity, propagation, staged resumption, or release packaging.

Use Project Steward when any of these is true:

- two or more artifacts share canon or assumptions;
- a rename, timeline change, relationship change, or world rule may propagate;
- sources conflict;
- work must resume across stages;
- the user requests a project audit, bundle, install order, certification, or release.

## Specialist routing

| Work | Specialist | Minimum handoff |
|---|---|---|
| Character card | Character Forge | artifact record, relevant entities/canon, agency contract, ownership, output mode |
| Scenario seed | Scenario Forge | relevant cast/world facts, temporal state, agency contract, desired mode |
| World Book/lorebook | Lorebook Forge | canon subset, ownership, activation targets, budget, source evidence |
| Preset conversion/audit | Preset Converter | source preset, target docs snapshot, scoped policies, tracker selection, preservation requirements |
| Narrator world, ensemble scenario, embedded-lorebook card, or multi-card world | World Forge | world-project record, canon subset, agency contract, selected profile, intended outputs |

All four specialists in this table are bundled in v0.2 under the plugin's skills directory. Route World Books to `forge-lumiverse-lorebooks` and ST Chat Completion migration to `lumiverse-preset-converter`. Native preset creation remains outside the converter's scope. If a skill fails to load or no matching specialist exists for other work, retain the task as `unresolved` or use an explicitly approved manual workflow.

## Handoff packet

For Lorebook Forge and Preset Converter, use the validated shared contract at `shared/contracts/specialist-handoffs.md` and `lumiverse-toolkit.specialist-handoff/v1`. Each packet contains:

```yaml
task_id: stable administrative ID
artifact_id: target artifact ID
operation: create | revise | audit | convert
source_authority: ordered sources relevant to this task
canon_subset: only facts the artifact needs
constraints: agency, mobile, token, style, compatibility
dependencies: confirmed incoming and outgoing edges
preserve: unknown fields, settings, assets, macros, or metadata
return:
  - completed artifact or explicit blocker
  - artifact passport
  - validation findings
  - proposed canon or dependency changes
  - unresolved questions
```

## Merge rules

Accept returned creative additions as `provisional` unless the user previously approved them. Merge by stable ID. Keep a change log and preserve unfamiliar fields. If a specialist reports an unsupported transform or loss, add a finding and passport note; do not hide it behind a successful-file claim.

Do not reproduce specialist internals inside Steward. Invoke `forge-lumiverse-lorebooks` for World Books and `lumiverse-preset-converter` for SillyTavern Chat Completion preset migration. The specialist remains usable without a project record; Steward only adds cross-artifact context and merges the returned evidence.

Plain single-character requests remain direct to Character Forge. Standalone World
Book requests remain direct to Forge Lumiverse Lorebooks. World Forge coordinates
only when the requested package connects multiple artifacts.
