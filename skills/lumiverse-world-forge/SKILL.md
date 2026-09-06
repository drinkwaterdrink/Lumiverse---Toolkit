---
name: lumiverse-world-forge
description: Use when creating a Lumiverse narrator world, ensemble scenario, character with an embedded lorebook, multi-card shared world, or a complete setting package rather than only one character.
---

# Lumiverse World Forge

World Forge coordinates `lumiverse-character-forge`, `lumiverse-scenario-forge`,
`forge-lumiverse-lorebooks`, and `lumiverse-project-steward` to build complete
roleplay worlds while keeping each artifact's ownership clear.

## Profiles

Choose exactly one: `single_character`, `character_with_world`, `narrator_world`,
`ensemble_scenario`, or `multi_card_world`. Route a plain single-character
request to Character Forge and a standalone World Book request to Lorebook Forge.
Use World Forge when the request connects two or more of those artifacts.

## Workflow

1. Read `references/profiles-and-routing.md` and classify the interaction model.
2. Establish approved canon, provisional additions, temporal facts, relationship
   claims, and the complete `{{user}}` agency contract.
3. Present a compact blueprint when the selected profile changes the output.
4. Delegate scenario structure to Scenario Forge, card fields to Character Forge,
   and lore entries to Forge Lumiverse Lorebooks.
5. Validate the world project record with `shared/validators/world_project.py`.
6. Compile the LoreForge book with `scripts/compile_character_book.py` when an
   embedded book is required.
7. Put the compiled object at `data.character_book` and package V3 CHARX through
   Character Forge's `scripts/package_charx.py`.
8. Produce the CHARX, card JSON, neutral LoreForge source, Character Book backup,
   compilation manifest, import guide, and artifact passport.

## Narrator contract

The narrator may set scenes, describe the environment, and voice non-user
characters. It never supplies `{{user}}`'s thoughts, feelings, dialogue,
decisions, consent, abilities, backstory, or next voluntary action. NPC autonomy
does not become control over the user. Activated lore is canon for the world, not
automatic knowledge for every character.

## Evidence boundary

The embedded compiler targets the observed Character Card V3 subset only. Its
manifest reports omitted advanced settings. Static validation does not certify
Lumiverse import, World Book activation, rendering, or model behavior.

Read the linked references before generating. Preserve complete source archives
when revising; never overwrite an existing export.
