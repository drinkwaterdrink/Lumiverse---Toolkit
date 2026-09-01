Here is the initialized reusable record. Administrative IDs are generated; the unapproved starting record version is explicitly provisional, and no attachment or ownership links have been guessed.

```json
{
  "schema": "lumiverse-toolkit.project/v1",
  "project": {
    "id": "project-nightshift-house",
    "name": "Nightshift House",
    "name_origin": "user",
    "version": "0.1.0",
    "version_origin": "generated",
    "version_status": "provisional",
    "status": "planning",
    "status_origin": "generated",
    "target": {
      "application": "Lumiverse",
      "origin": "user",
      "documentation_snapshot": null,
      "documentation_source": "current documentation supplied with the project"
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
        "rule": "User-supplied project and world notes become canon unless the user marks them otherwise.",
        "origin": "user"
      },
      {
        "rule": "Approved project canon outranks external references and generated material.",
        "origin": "user"
      },
      {
        "rule": "Current supplied Lumiverse documentation governs technical behavior but cannot invent story canon.",
        "origin": "user"
      },
      {
        "rule": "Generated creative material remains provisional until user approval.",
        "origin": "user"
      }
    ]
  },
  "preferences": {
    "detail": "rich",
    "always_injected": "lean",
    "conditional_material": "deep",
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
      "emotions",
      "romance",
      "relationships",
      "abilities",
      "next_voluntary_action"
    ],
    "origin": "user"
  },
  "policies": [
    {
      "id": "policy-user-notes-are-canon",
      "origin": "user",
      "applies_to": {
        "project_id": "project-nightshift-house",
        "content": "user_supplied_notes"
      },
      "rules": {
        "default_fact_status": "canon"
      }
    },
    {
      "id": "policy-generated-proposals",
      "origin": "user",
      "applies_to": {
        "project_id": "project-nightshift-house",
        "content_origin": "generated"
      },
      "rules": {
        "default_fact_status": "provisional",
        "approval_required_for_canon": true
      }
    },
    {
      "id": "policy-external-canon-boundary",
      "origin": "user",
      "applies_to": {
        "project_id": "project-nightshift-house",
        "content_origin": "external_reference"
      },
      "rules": {
        "may_suggest": true,
        "may_silently_overwrite_original_world_canon": false
      }
    },
    {
      "id": "policy-generic-preset-tracker-agnostic",
      "origin": "user",
      "applies_to": {
        "artifact_ids": [
          "artifact-loom-roleplay-preset"
        ]
      },
      "rules": {
        "tracker_agnostic": true,
        "tracker_integration_requires_explicit_selection": true
      }
    },
    {
      "id": "policy-real-frank",
      "origin": "user",
      "applies_to": {
        "project_id": "project-nightshift-house",
        "artifact_type": "loom_preset",
        "name_family": "Real Frank"
      },
      "rules": {
        "filename_and_internal_name": "🧟 Real Frank vX.X — Lumi Native",
        "release_version_increment": 0.1,
        "bundle_linked_regex_inside_preset": true,
        "preserve_latest_lumiverse_settings_and_selections": true,
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
      "id": "artifact-world-book",
      "type": "world_book",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "attachment_required": true,
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
      "id": "artifact-loom-roleplay-preset",
      "type": "loom_preset",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "passport": null,
      "tracker_mode": "agnostic"
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
      "selection_status": "optional_not_selected"
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
      "status": "approved",
      "origin": "user",
      "decision": "Build for Lumiverse using the current supplied project documentation."
    },
    {
      "id": "decision-content-density",
      "status": "approved",
      "origin": "user",
      "decision": "Use rich project detail while keeping always-injected context lean and conditional material deep."
    },
    {
      "id": "decision-mobile-primary",
      "status": "approved",
      "origin": "user",
      "decision": "Treat Android/mobile as the primary usage surface."
    },
    {
      "id": "decision-generic-preset-tracker-mode",
      "status": "approved",
      "origin": "user",
      "decision": "Keep the generic Loom roleplay preset tracker-agnostic unless a SimTracker preset is explicitly selected."
    },
    {
      "id": "decision-real-frank-release-policy",
      "status": "approved",
      "origin": "user",
      "decision": "Apply the scoped Real Frank naming, +0.1 release increment, bundled-regex, and settings-preservation rules to future matching Loom presets."
    }
  ],
  "unresolved": [
    {
      "id": "unresolved-documentation-snapshot",
      "origin": "generated",
      "status": "open",
      "question": "What version or date should identify the current supplied Lumiverse documentation snapshot?",
      "required_before": "technical certification"
    },
    {
      "id": "unresolved-world-book-attachment-target",
      "origin": "generated",
      "status": "open",
      "question": "Which artifact should own or receive the planned World Book attachment?",
      "required_before": "creating the attachment dependency"
    },
    {
      "id": "unresolved-artifact-identities",
      "origin": "generated",
      "status": "open",
      "question": "What approved display names, filenames, and starting versions should the planned artifacts use?",
      "required_before": "artifact release"
    },
    {
      "id": "unresolved-artifact-ownership",
      "origin": "generated",
      "status": "open",
      "question": "Which artifact should authoritatively own each shared fact once entities and canon are defined?",
      "required_before": "creating ownership and dependency edges"
    },
    {
      "id": "unresolved-simtracker-selection",
      "origin": "user",
      "status": "deferred",
      "question": "Will this project later select and build the optional SimTracker preset?",
      "required_before": "adding any SimTracker-specific integration"
    },
    {
      "id": "unresolved-real-frank-starting-version",
      "origin": "generated",
      "status": "open_when_applicable",
      "question": "If a Real Frank preset is added, what approved current or starting version should it use?",
      "required_before": "creating the first Real Frank release"
    }
  ]
}
```
