---
name: lumiverse-project-steward
description: Use when coordinating two or more connected Lumiverse artifacts, preserving project canon across revisions, propagating renames or other cross-artifact changes, resuming a staged build, or auditing and packaging a multi-artifact release. Also use when conflicting sources need explicit resolution. Do not use for a self-contained character, scenario, lorebook, or preset task with no continuity requirement.
---

# Lumiverse Project Steward

Coordinate the project while specialist skills create or transform artifacts.

## Workflow

1. **Route the request.** If it is self-contained, invoke the matching specialist and stop. If it affects multiple artifacts, continuity, or a release, continue as Steward.
2. **Load or initialize the record.** Follow [Project Record Contract](references/project-record-contract.md). Use `lumiverse-toolkit.project/v1` exactly. Administrative IDs may be generated; label creative suggestions `provisional`, and leave unsupported choices in `unresolved`.
3. **Normalize authority.** Treat user statements as highest project authority. Preserve approved project canon. Use current supplied Lumiverse documentation for technical behavior. External and generated material may propose but never silently overwrite canon.
4. **Map the change.** Identify affected entities, artifacts, dependency edges, ownership boundaries, activation links, and downstream assumptions before editing. Unknown edges become validation findings or unresolved questions—not invented links.
5. **Prepare focused handoffs.** Give each specialist only its artifact, the relevant canon subset, user constraints, dependencies, and required return contract. Follow [Routing and Handoffs](references/routing-and-handoffs.md).
6. **Merge evidence.** Update the record from returned artifacts and passports. Preserve unknown fields and untouched settings. Record losses, transforms, unresolved items, decisions, and validation findings explicitly.
7. **Audit or release.** Follow [Changes, Validation, and Releases](references/change-validation-release.md). A blocker prevents certification; a major prevents release unless the user explicitly accepts it. Never claim an edit, validation, import test, or install succeeded without evidence.

## Invariants

- Reserve `{{user}}` actions, dialogue, thoughts, feelings, attraction, consent, decisions, and backstory for the user. Violations are blockers.
- Keep rich world detail separate from lean always-injected context.
- Scope naming, versioning, regex, tracker, and style policies to the project or artifact they actually govern.
- Keep generic presets tracker-agnostic unless a tracker is selected.
- Use stable IDs for identity; names and aliases may change.
- Present consequential assumptions for approval. Do not silently choose canon, attachment targets, ownership, or starting versions.

Use compact mobile-friendly summaries in chat. Put large records, manifests, and artifacts in files.
