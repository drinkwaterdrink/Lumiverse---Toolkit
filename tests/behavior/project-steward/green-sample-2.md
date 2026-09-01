Here is the reusable project record. The record version is an administrative starting value; artifact versions, names, ownership, attachment target, and story canon remain unset until you approve them.

```json
{
  "schema": "lumiverse-toolkit.project/v1",
  "project": {
    "id": "project-nightshift-house-001",
    "id_origin": "generated",
    "name": "Nightshift House",
    "name_origin": "user",
    "version": "0.1.0",
    "version_origin": "generated",
    "version_purpose": "administrative project-record revision",
    "status": "planning",
    "target": {
      "application": "Lumiverse",
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
        "id": "authority-user-notes",
        "origin": "user",
        "rule": "User-supplied notes are canon unless the user revises or deprecates them."
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
        "rule": "External and generated material may propose additions but cannot silently overwrite original-world canon."
      }
    ]
  },
  "preferences": {
    "origin": "user",
    "detail": "rich",
    "always_injected": "lean",
    "conditional": "deep",
    "primary_surface": "android-mobile"
  },
  "agency": {
    "origin": "user",
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
    ]
  },
  "policies": [
    {
      "id": "policy-real-frank",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "artifact_type": "loom_preset",
        "series": "Real Frank",
        "project": "project-nightshift-house-001"
      },
      "rules": {
        "display_name_and_filename": "🧟 Real Frank vX.X — Lumi Native",
        "release_version_increment": 0.1,
        "regex": "Bundle and link the regex inside the actual Lumiverse preset export, using matching versioned naming and metadata.",
        "preservation": "Preserve settings and selections from the latest user-supplied Lumiverse version."
      },
      "starting_version": null
    },
    {
      "id": "policy-generic-loom-tracker-agnostic",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "artifact_id": "artifact-generic-loom-preset"
      },
      "rules": {
        "tracker_mode": "agnostic",
        "selected_tracker": null,
        "activation_condition": "A tracker integration may be added only after the user explicitly selects one."
      }
    },
    {
      "id": "policy-context-density",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "project_id": "project-nightshift-house-001"
      },
      "rules": {
        "content_detail": "rich",
        "always_injected_context": "lean",
        "conditional_context": "deep"
      }
    },
    {
      "id": "policy-mobile-primary",
      "origin": "user",
      "status": "canon",
      "applies_to": {
        "project_id": "project-nightshift-house-001"
      },
      "rules": {
        "primary_surface": "android-mobile",
        "interaction_guidance": "Keep user-facing controls, summaries, and install guidance compact and touch-friendly."
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
        "target_artifact_id": null
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
      "id": "artifact-generic-loom-preset",
      "type": "loom_preset",
      "status": "planned",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "tracker_agnostic": true,
      "selected_tracker": null
    },
    {
      "id": "artifact-optional-simtracker-preset",
      "type": "simtracker_preset",
      "status": "deferred",
      "origin": "user",
      "display_name": null,
      "filename": null,
      "version": null,
      "owner": null,
      "selection_required": true
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
  "decisions": [],
  "unresolved": [
    {
      "id": "unresolved-documentation-snapshot",
      "origin": "generated",
      "question": "What version or date identifies the supplied Lumiverse documentation snapshot?",
      "blocks": [
        "technical certification against a named documentation snapshot"
      ],
      "blocking_now": false
    },
    {
      "id": "unresolved-world-book-attachment",
      "origin": "generated",
      "question": "Which artifact should own or attach the World Book?",
      "blocks": [
        "confirmed attachment dependency",
        "final install order"
      ],
      "blocking_now": false
    },
    {
      "id": "unresolved-story-canon",
      "origin": "generated",
      "question": "What user-approved world, cast, relationship, timeline, and scenario facts should populate the entity and canon ledgers?",
      "blocks": [
        "content generation for the planned cards, World Book, and scenario seeds"
      ],
      "blocking_now": false
    },
    {
      "id": "unresolved-artifact-identity",
      "origin": "generated",
      "question": "What names, filenames, ownership boundaries, and starting versions should the planned artifacts use?",
      "blocks": [
        "release-ready artifact passports and manifest"
      ],
      "blocking_now": false
    },
    {
      "id": "unresolved-real-frank-starting-version",
      "origin": "generated",
      "question": "If a Real Frank preset is added, what user-approved version should be treated as the latest starting version?",
      "blocks": [
        "a correctly incremented Real Frank release"
      ],
      "blocking_now": false
    },
    {
      "id": "unresolved-simtracker-selection",
      "origin": "generated",
      "question": "Should the optional SimTracker preset remain deferred, and if activated later, which tracker contract and compatibility requirements should govern it?",
      "blocks": [
        "SimTracker-specific dependencies and integration"
      ],
      "blocking_now": false
    }
  ]
}
```

No dependency edges are asserted yet: the World Book is known to require attachment, but its target has not been supplied. No artifact creation, Lumiverse import, or release validation is claimed.
