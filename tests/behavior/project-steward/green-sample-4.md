Here is the reusable project record. It uses the established `lumiverse-toolkit.project/v1` contract. No artifact names, artifact versions, attachment targets, or dependency edges have been invented.

```json
{
  "schema": "lumiverse-toolkit.project/v1",
  "project": {
    "id": "project-nightshift-house-01",
    "name": "Nightshift House",
    "name_origin": "user",
    "version": "0.1.0",
    "version_origin": "generated",
    "version_note": "Administrative project-record version; not an artifact release version.",
    "status": "planning",
    "target": {
      "application": "Lumiverse",
      "documentation_snapshot": null,
      "documentation_basis": "Current documentation supplied with the project",
      "origin": "user"
    }
  },
  "authority": {
    "source_order": [
      "user",
      "approved_project",
      "lumiverse_docs_technical",
      "external_reference",
      "generated"
    ],
    "fact_statuses": [
      "canon",
      "provisional",
      "disputed",
      "deprecated"
    ],
    "rules": [
      {
        "id": "authority-user-canon",
        "origin": "user",
        "rule": "User-supplied original-world notes are canon unless the user revises them."
      },
      {
        "id": "authority-approved-project",
        "origin": "user",
        "rule": "Previously approved project canon is preserved across artifacts and revisions."
      },
      {
        "id": "authority-lumiverse-docs",
        "origin": "user",
        "rule": "Supplied current Lumiverse documentation governs technical behavior but does not create story canon."
      },
      {
        "id": "authority-external-generated",
        "origin": "user",
        "rule": "External and generated material may propose additions but may not silently overwrite original-world canon."
      }
    ]
  },
  "preferences": {
    "detail": "rich",
    "always_injected": "lean",
    "conditional": "deep",
    "primary_surface": "android-mobile",
    "origin": "user"
  },
  "agency": {
    "protected_subject": "{{user}}",
    "reserved": [
      "actions",
      "dialogue",
      "thoughts",
      "feelings",
      "attraction",
      "consent",
      "decisions",
      "backstory",
      "romance",
      "relationships",
      "abilities",
      "next_voluntary_action"
    ],
    "origin": "user"
  },
  "policies": [
    {
      "id": "policy-real-frank",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "project_id": "project-nightshift-house-01",
        "artifact_type": "loom_preset",
        "name_family": "Real Frank"
      },
      "rules": {
        "display_name_template": "🧟 Real Frank vX.X — Lumi Native",
        "filename_template": "🧟 Real Frank vX.X — Lumi Native",
        "bundled_regex_name_template": "🧟 Real Frank vX.X — Lumi Native",
        "release_increment": 0.1,
        "bundle_linked_regex_inside_preset": true,
        "preserve_latest_lumiverse_settings_and_selections": true,
        "starting_version": null
      },
      "note": "This policy applies only if a Real Frank Loom preset is added to this project. It does not govern the generic Loom preset or other artifacts."
    },
    {
      "id": "policy-generic-loom-tracker",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "artifact_id": "artifact-loom-roleplay-preset-01"
      },
      "rules": {
        "tracker_agnostic": true,
        "selected_tracker": null,
        "do_not_assume_trackwright_or_simtracker": true
      }
    },
    {
      "id": "policy-context-density",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "project_id": "project-nightshift-house-01"
      },
      "rules": {
        "world_detail": "rich",
        "always_injected_context": "lean",
        "conditional_context": "deep"
      }
    },
    {
      "id": "policy-mobile-primary",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "project_id": "project-nightshift-house-01"
      },
      "rules": {
        "primary_surface": "android-mobile",
        "instructions": "compact",
        "filenames": "clear"
      }
    }
  ],
  "entities": [],
  "canon": [],
  "artifacts": [
    {
      "id": "artifact-narrator-world-card-01",
      "type": "narrator_world_card",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null
    },
    {
      "id": "artifact-character-card-01",
      "type": "character_card",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "independent": true
    },
    {
      "id": "artifact-character-card-02",
      "type": "character_card",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "independent": true
    },
    {
      "id": "artifact-character-card-03",
      "type": "character_card",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "independent": true
    },
    {
      "id": "artifact-character-card-04",
      "type": "character_card",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "independent": true
    },
    {
      "id": "artifact-world-book-01",
      "type": "world_book",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "attachment_target": null
    },
    {
      "id": "artifact-scenario-seed-01",
      "type": "scenario_seed",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null
    },
    {
      "id": "artifact-scenario-seed-02",
      "type": "scenario_seed",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null
    },
    {
      "id": "artifact-scenario-seed-03",
      "type": "scenario_seed",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null
    },
    {
      "id": "artifact-loom-roleplay-preset-01",
      "type": "loom_preset",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "purpose": "generic_roleplay",
      "tracker_binding": null
    },
    {
      "id": "artifact-simtracker-preset-01",
      "type": "simtracker_preset",
      "status": "deferred",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "optional": true
    }
  ],
  "dependencies": [],
  "validation": {
    "status": "not_run",
    "findings": [],
    "last_run": null
  },
  "release": {
    "status": "unreleased",
    "manifest": null
  },
  "decisions": [
    {
      "id": "decision-source-authority-01",
      "origin": "user",
      "status": "approved",
      "decision": "User notes are canon; AI proposals remain provisional; external material cannot overwrite original-world canon."
    },
    {
      "id": "decision-agency-01",
      "origin": "user",
      "status": "approved",
      "decision": "The user exclusively controls the protected aspects listed in the agency contract."
    },
    {
      "id": "decision-tracker-agnostic-01",
      "origin": "user",
      "status": "approved",
      "decision": "The generic Loom roleplay preset remains tracker-agnostic unless a tracker is explicitly selected."
    },
    {
      "id": "decision-project-surface-01",
      "origin": "user",
      "status": "approved",
      "decision": "Android/mobile is the primary surface, with rich detail stored conditionally and lean always-injected context."
    }
  ],
  "unresolved": [
    {
      "id": "unresolved-documentation-snapshot-01",
      "origin": "user",
      "status": "open",
      "question": "What exact version or date identifies the supplied current Lumiverse documentation snapshot?",
      "current_value": null,
      "impact": "Capture before technical implementation or certification so future audits can reproduce the documentation basis."
    },
    {
      "id": "unresolved-world-book-attachment-01",
      "origin": "user",
      "status": "open",
      "question": "Which artifact should own or attach the World Book?",
      "current_value": null,
      "candidates": [
        "artifact-narrator-world-card-01",
        "one or more character cards",
        "another explicitly selected Lumiverse attachment target"
      ],
      "impact": "No dependency edge is created until the user approves the attachment target. This blocks World Book attachment and final certification, not project-record creation."
    }
  ]
}
```

The record is ready for future specialist handoffs. Its next consequential decisions are the exact Lumiverse documentation snapshot and the World Book attachment target; everything else can remain in planning without inventing canon.
