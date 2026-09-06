# Changes, Validation, and Releases

## Change propagation

1. Identify the changed stable ID and the exact old/new values.
2. Traverse confirmed dependency edges in both directions.
3. Search affected artifacts for names, aliases, IDs, relationship text, timeline facts, world rules, prompt assumptions, tracker keys, activation keywords, and filenames as applicable.
4. Classify each match as an automatic structural edit, a proposed semantic edit, or an intentional historical reference.
5. Preserve backward-compatible aliases when needed for activation, imports, saves, or tracker state.
6. Apply approved edits and record evidence per artifact.
7. Re-run stale-reference, missing-edge, collision, agency, and specialist validation.

Do not report propagation complete while an affected artifact is unavailable or unverified. Record partial completion and remaining blast radius.

## Artifact passport

Each returned artifact carries:

```yaml
artifact_id: stable ID
operation: create | revise | audit | convert
source_format: known format or null
target_format: known format or null
preserved: [verified items]
transformed: [verified changes]
lost: [known losses]
unknown: [unverified behavior or unavailable artifacts]
validation: [checks actually run and results]
assumptions: [approved or provisional assumptions]
```

An empty `lost` list means no loss was observed by the checks that actually ran; it is not proof of universal losslessness.

For staged connected builds, the build ledger is the operational source of
truth for artifact status, anchors, dependencies, skip reasons, and resumable
batch progress. A specialist capability receipt records only what that
specialist produced and which checks support it. Steward merges receipts; it
does not promote `UNPROVEN` or `RUNTIME TEST REQUIRED` into a pass.

## Validation severities

- `blocker`: agency violation, invalid structure preventing use, destructive unresolved loss, or a required user decision. Do not certify.
- `major`: meaningful inconsistency, broken dependency, unsupported conversion, or missing release-critical validation. Do not release unless the user explicitly accepts it.
- `minor`: localized quality or maintainability problem that does not prevent use.
- `info`: observation, suggestion, or deliberately accepted tradeoff.

Each finding needs a path and evidence. Only mark a finding resolved after rechecking the changed artifact.

## Release gate

Before setting `release.status` to `released`:

- all planned release artifacts exist and have stable IDs and versions;
- dependency endpoints resolve and install order is acyclic;
- no unresolved blockers remain;
- majors are fixed or explicitly accepted by the user;
- specialist validation evidence is attached;
- required build-ledger gates are complete and every capability receipt matches
  an actual release artifact;
- manifest, changelog, known limitations, and rollback guidance are complete;
- mobile-facing instructions are concise and filenames are clear.

Certification describes the checks that ran. Never imply a Lumiverse import was tested unless it actually was.
