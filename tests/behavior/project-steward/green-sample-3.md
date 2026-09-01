Here is the initialized reusable project record. Unknown creative choices remain `null` or unresolved, so this establishes structure without inventing canon, attachment targets, names, or starting versions.

```json
{
  "schema": "lumiverse-toolkit.project/v1",
  "project": {
    "id": "project-nightshift-house",
    "name": "Nightshift House",
    "version": "0.1.0",
    "version_semantics": "project_record_revision",
    "status": "planning",
    "target": {
      "application": "Lumiverse",
      "documentation_snapshot": null
    },
    "field_origins": {
      "id": "generated",
      "name": "user",
      "version": "generated",
      "status": "generated",
      "target.application": "user",
      "target.documentation_snapshot": "generated"
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
        "id": "authority-user-notes",
        "origin": "user",
        "rule": "User-supplied project notes are canon unless the user later revises or deprecates them."
      },
      {
        "id": "authority-approved-project",
        "origin": "user",
        "rule": "Previously approved project canon is preserved across artifacts and revisions."
      },
      {
        "id": "authority-lumiverse-docs",
        "origin": "user",
        "rule": "Current supplied Lumiverse documentation governs technical behavior but cannot invent story canon."
      },
      {
        "id": "authority-external-sources",
        "origin": "user",
        "rule": "External sources may suggest provisional ideas but cannot overwrite original-world canon."
      },
      {
        "id": "authority-generated-material",
        "origin": "user",
        "rule": "AI-generated creative or consequential material remains provisional until explicitly approved."
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
      "backstory"
    ],
    "project_specific_reserved": [
      "romance",
      "relationships",
      "abilities",
      "next_voluntary_action"
    ],
    "origin": "user"
  },
  "policies": [
    {
      "id": "policy-generic-roleplay-tracker-agnostic",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "artifact_id": "artifact-loom-roleplay-preset"
      },
      "rules": {
        "tracker_mode": "agnostic",
        "tracker_binding": null,
        "selection_required_before_binding": true
      }
    },
    {
      "id": "policy-real-frank",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "artifact_type": "loom_preset",
        "project_id": "project-nightshift-house",
        "name_family": "Real Frank"
      },
      "rules": {
        "display_and_filename_pattern": "🧟 Real Frank vX.X — Lumi Native",
        "release_increment": 0.1,
        "linked_regex": "bundled_inside_preset_export",
        "preserve_from_latest_lumiverse_version": [
          "settings",
          "selections"
        ],
        "starting_version": null
      }
    }
  ],
  "entities": [],
  "canon": [],
  "artifacts": [
    {
      "id": "artifact-narrator-world-card",
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
      "passport": null
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
      "passport": null
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
      "passport": null
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
      "passport": null
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
      "attachment": {
        "required": true,
        "target_artifact_id": null,
        "origin": "user"
      }
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
      "id": "artifact-loom-roleplay-preset",
      "type": "loom_preset",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "tracker_compatibility": {
        "mode": "agnostic",
        "selected_tracker_artifact_id": null
      }
    },
    {
      "id": "artifact-simtracker-preset",
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
      "id": "decision-target-lumiverse",
      "origin": "user",
      "status": "approved",
      "decision": "Build the project for Lumiverse."
    },
    {
      "id": "decision-artifact-plan",
      "origin": "user",
      "status": "approved",
      "decision": "Plan one narrator/world card, four independent character cards, one attached World Book, three scenario seeds, one generic Loom roleplay preset, and one optional deferred SimTracker preset."
    },
    {
      "id": "decision-content-budget",
      "origin": "user",
      "status": "approved",
      "decision": "Keep authored detail rich, always-injected context lean, and conditional material deep."
    },
    {
      "id": "decision-primary-surface",
      "origin": "user",
      "status": "approved",
      "decision": "Optimize interaction and instructions for Android/mobile use."
    }
  ],
  "unresolved": [
    {
      "id": "unresolved-documentation-snapshot",
      "origin": "generated",
      "path": "$.project.target.documentation_snapshot",
      "question": "What version, date, or identifier should record the supplied current Lumiverse documentation snapshot?",
      "blocks_current_record": false,
      "blocks_release": true
    },
    {
      "id": "unresolved-world-book-attachment",
      "origin": "generated",
      "path": "$.artifacts[5].attachment.target_artifact_id",
      "question": "Which artifact should the World Book attach to?",
      "blocks_current_record": false,
      "blocks_release": true
    },
    {
      "id": "unresolved-artifact-identities",
      "origin": "generated",
      "path": "$.artifacts",
      "question": "What approved names, identities, owners, filenames, and starting artifact versions should be used as each artifact is created?",
      "blocks_current_record": false,
      "blocks_release": false
    },
    {
      "id": "unresolved-real-frank-starting-version",
      "origin": "generated",
      "path": "$.policies[1].rules.starting_version",
      "question": "If a Real Frank preset is added, what latest approved Lumiverse version should establish its starting release number?",
      "blocks_current_record": false,
      "blocks_release": false
    }
  ]
}
```

No dependency edge is recorded yet because the World Book's attachment target has not been supplied. The optional SimTracker artifact is deferred, and the generic Loom preset remains tracker-agnostic.
