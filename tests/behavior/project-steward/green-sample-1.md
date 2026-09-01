Here is the complete reusable project record. I left unsupported names, attachment targets, ownership, documentation version, and artifact versions unresolved instead of guessing.

```json
{
  "schema": "lumiverse-toolkit.project/v1",
  "project": {
    "id": "project-nightshift-house",
    "name": "Nightshift House",
    "name_origin": "user",
    "version": "0.1.0",
    "version_origin": "generated",
    "status": "planning",
    "target": {
      "application": "Lumiverse",
      "documentation_snapshot": null,
      "documentation_source": "current project-supplied Lumiverse documentation",
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
        "id": "authority-user-notes",
        "origin": "user",
        "rule": "User-supplied project notes are canon unless the user later revises them."
      },
      {
        "id": "authority-approved-project",
        "origin": "user",
        "rule": "Approved project canon remains authoritative across future artifacts and revisions."
      },
      {
        "id": "authority-lumiverse-docs",
        "origin": "user",
        "rule": "Current supplied Lumiverse documentation governs technical behavior but cannot invent story canon."
      },
      {
        "id": "authority-external-generated",
        "origin": "user",
        "rule": "External and generated material may propose ideas but cannot silently overwrite original-world canon."
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
      "emotions",
      "attraction",
      "romance",
      "consent",
      "decisions",
      "relationships",
      "abilities",
      "backstory",
      "next_voluntary_action"
    ],
    "origin": "user"
  },
  "policies": [
    {
      "id": "policy-provisional-ai-content",
      "name": "Unapproved AI content remains provisional",
      "status": "canon",
      "origin": "user",
      "applies_to": {
        "project_id": "project-nightshift-house"
      },
      "rules": {
        "generated_creative_content_status": "provisional",
        "canon_requires_user_approval": true
      }
    },
    {
      "id": "policy-generic-loom-tracker-agnostic",
      "name": "Generic Loom preset remains tracker-agnostic",
      "status": "canon",
      "origin": "user",
      "applies_to": {
        "project_id": "project-nightshift-house",
        "artifact_id": "artifact-loom-roleplay-preset",
        "artifact_type": "loom_preset"
      },
      "rules": {
        "tracker_integration": "none_unless_user_selects_tracker",
        "simtracker_is_optional": true
      }
    },
    {
      "id": "policy-real-frank",
      "name": "Real Frank release policy",
      "status": "canon",
      "origin": "user",
      "applies_to": {
        "project_id": "project-nightshift-house",
        "artifact_type": "loom_preset",
        "preset_family": "Real Frank"
      },
      "rules": {
        "display_name_and_filename_template": "🧟 Real Frank vX.X — Lumi Native",
        "release_version_increment": 0.1,
        "starting_version": null,
        "regex": "bundle and link inside the Lumiverse preset export using matching release naming and metadata",
        "preserve": [
          "latest Lumiverse settings",
          "latest Lumiverse selections"
        ]
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
      "owner": null
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
      "independent": true
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
      "attachment": {
        "required": true,
        "target_artifact_id": null,
        "status": "unresolved",
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
      "owner": null
    },
    {
      "id": "artifact-scenario-seed-02",
      "type": "scenario_seed",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null
    },
    {
      "id": "artifact-scenario-seed-03",
      "type": "scenario_seed",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null
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
      "id": "decision-artifact-plan",
      "status": "approved",
      "origin": "user",
      "summary": "Plan one narrator/world card, four independent character cards, one attached World Book, three scenario seeds, one generic Loom roleplay preset, and an optional SimTracker preset later."
    },
    {
      "id": "decision-content-density",
      "status": "approved",
      "origin": "user",
      "summary": "Prefer rich detail while keeping always-injected content lean and placing depth in conditional content."
    },
    {
      "id": "decision-primary-surface",
      "status": "approved",
      "origin": "user",
      "summary": "Design project-facing instructions and outputs primarily for Android/mobile use."
    }
  ],
  "unresolved": [
    {
      "id": "unresolved-documentation-snapshot",
      "status": "open",
      "origin": "generated",
      "path": "project.target.documentation_snapshot",
      "question": "What version or date identifies the current project-supplied Lumiverse documentation?",
      "blocking": false
    },
    {
      "id": "unresolved-world-book-attachment",
      "status": "open",
      "origin": "generated",
      "path": "artifacts[artifact-world-book].attachment.target_artifact_id",
      "question": "Which artifact should own or attach the World Book?",
      "blocking": true
    },
    {
      "id": "unresolved-artifact-identities",
      "status": "open",
      "origin": "generated",
      "path": "artifacts[*]",
      "question": "What approved names, filenames, versions, and ownership assignments should the planned artifacts use?",
      "blocking": false
    },
    {
      "id": "unresolved-real-frank-starting-version",
      "status": "open",
      "origin": "generated",
      "path": "policies[policy-real-frank].rules.starting_version",
      "question": "If a Real Frank preset is created, what existing/latest version establishes its first project release number?",
      "blocking": false
    },
    {
      "id": "unresolved-simtracker-selection",
      "status": "open",
      "origin": "generated",
      "path": "artifacts[artifact-simtracker-preset]",
      "question": "Will a SimTracker preset be selected later, and if so, which preset and confirmed dependencies should be added?",
      "blocking": false
    }
  ]
}
```
