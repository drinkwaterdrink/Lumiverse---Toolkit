# Project Record Contract v1

Use the authoritative identifier `lumiverse-toolkit.project/v1`. The machine schema lives at `shared/schemas/project-record.schema.json`; structural checks live at `shared/validators/project_record.py`.

## Required top-level collections

Every record contains these keys, even when a collection is empty:

```json
{
  "schema": "lumiverse-toolkit.project/v1",
  "project": {},
  "authority": {},
  "preferences": {},
  "agency": {},
  "policies": [],
  "entities": [],
  "canon": [],
  "artifacts": [],
  "dependencies": [],
  "validation": {"status": "not_run", "findings": [], "last_run": null},
  "release": {"status": "unreleased", "manifest": null},
  "decisions": [],
  "unresolved": []
}
```

Additional fields are allowed and must survive round trips.

## Project and authority

`project` requires:

- `id`: generated stable administrative ID;
- `name`: user-supplied or explicitly marked provisional;
- `version`: record version, not an artifact version;
- `status`: `planning`, `active`, `paused`, `releasing`, `released`, or `archived`;
- `target.application`: `Lumiverse`;
- `target.documentation_snapshot`: supplied documentation version/date, or `null` when unknown.

Set `authority.source_order` to:

1. `user`
2. `approved_project`
3. `lumiverse_docs_technical`
4. `external_reference`
5. `generated`

Lumiverse documentation governs technical behavior but does not invent story canon. Record fact status as `canon`, `provisional`, `disputed`, or `deprecated`. Keep source, status, and approval evidence on each canon fact.

## User values and proposals

Every creative or consequential item records `origin`: `user`, `approved_project`, `lumiverse_docs_technical`, `external_reference`, or `generated`.

- Generated IDs, timestamps, and empty ledgers are administrative structure, not creative canon.
- Generated names, attachment targets, ownership choices, versions, relationships, and story facts are `provisional` until approved.
- If a required value has no evidence, use `null` and add an `unresolved` item instead of guessing.

## Preferences and agency

Keep content density separate from injection cost:

```json
"preferences": {
  "detail": "rich",
  "always_injected": "lean",
  "primary_surface": "android-mobile"
}
```

The complete agency contract is:

```json
"agency": {
  "protected_subject": "{{user}}",
  "reserved": [
    "actions", "dialogue", "thoughts", "feelings",
    "attraction", "consent", "decisions", "backstory"
  ]
}
```

## Stable records

All policies, entities, canon facts, artifacts, and dependency edges need unique stable `id` values.

Artifact records use:

- `id`, `type`, `status`, `origin`;
- `display_name`, `filename`, and `version` when known, otherwise `null`;
- `owner` for the authoritative artifact when known;
- `passport` after an artifact is created, imported, converted, or revised.

Artifact status: `planned`, `draft`, `ready`, `validated`, `released`, `deprecated`, or `deferred`.

Dependency records use `id`, `from`, `to`, `type`, `status`, and `origin`. Both endpoints must be artifact IDs. Allowed types:

- `references`
- `embeds`
- `activates`
- `assumes`
- `mirrors`
- `installs_before`
- `generated_from`

Use dependency status `canon`, `provisional`, `broken`, or `deprecated`.

Do not create a dependency merely because one seems likely. Put the missing decision in `unresolved`.

## Policies, validation, and release

Policy `applies_to` must state its actual scope. Real Frank naming, `+0.1` versioning, bundled regex, and settings preservation apply only to the matching Loom preset—not globally. Do not invent its starting version.

Finding severity is `blocker`, `major`, `minor`, or `info`. A finding records `id`, `severity`, `code`, `path`, `message`, and evidence when available.

Release begins as `{"status":"unreleased","manifest":null}`. A release manifest lists artifacts by stable ID, version, checksum when calculated, install order, validation evidence, and rollback guidance.
