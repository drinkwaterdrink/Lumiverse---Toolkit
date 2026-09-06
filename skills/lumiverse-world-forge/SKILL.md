---
name: lumiverse-world-forge
description: Use when creating a Lumiverse narrator world, ensemble scenario, character with an embedded lorebook, multi-card shared world, or a complete setting package rather than only one character.
---

# Lumiverse World Forge

World Forge coordinates `lumiverse-character-forge`, `lumiverse-scenario-forge`,
`forge-lumiverse-lorebooks`, and `lumiverse-project-steward` to build complete
roleplay worlds while keeping each artifact's ownership clear.

Use **create then refine** by default. Produce the smallest coherent connected
blueprint, audit it, and refine selected parts. Offer an **Interview** or **Idea Lab**
route for discovery-heavy requests, vague premises, or meaningful source
conflicts without making it mandatory.

Preset creation is separate from World Forge. A package may recommend preset
needs or hand off conversion work, but it must remain usable with a compatible
user-selected preset unless the user explicitly commissions a preset artifact.

## Shared contracts

Read [Creative Quality Kernel](../../shared/references/creative-quality-kernel.md),
[Agency Contract](../../shared/references/agency-contract.md),
[Source Authority](../../shared/references/source-authority.md),
[Evidence Model](../../shared/references/evidence-model.md),
[Artifact Ownership](../../shared/references/artifact-ownership.md), and the
[Lumiverse Capability Map](../../shared/references/lumiverse-capability-map.md).
Use [Idea Lab](../../shared/references/idea-lab.md) for discovery and
[Source Ingestion](../../shared/references/source-ingestion.md) for franchise,
wiki, novel, card, World Book, or mixed-source projects.

## Profiles

Choose exactly one: `single_character`, `character_with_world`, `narrator_world`,
`ensemble_scenario`, or `multi_card_world`. Route a plain single-character
request to Character Forge and a standalone World Book request to Lorebook Forge.
Use World Forge when the request connects two or more of those artifacts.

## Workflow

1. Read [Profiles and Routing](references/profiles-and-routing.md) and classify the interaction model; also read [Build Workflow](references/build-workflow.md).
2. Establish approved canon, provisional additions, temporal facts, relationship
   claims, the source ledger when applicable, and the complete `{{user}}` agency
   contract.
3. Present a compact blueprint when the selected profile changes the output.
4. Delegate scenario structure to Scenario Forge, card fields to Character Forge,
   and lore entries to Forge Lumiverse Lorebooks.
5. Maintain and validate a build ledger for staged or connected projects, then validate the world project record with `shared/validators/world_project.py`.
6. Compile the LoreForge book with `scripts/compile_character_book.py` when an
   embedded book is required.
7. Put the compiled object at `data.character_book` and package V3 CHARX through
   Character Forge's `scripts/package_charx.py`.
8. Produce the CHARX, card JSON, neutral LoreForge source, Character Book backup,
   compilation manifest, import guide, and artifact passport.

Keep large source corpora in Databank when retrieval is more appropriate than
conditional lore; World Books receive concise playable facts and activation
intent. Do not scrape through access controls. Mark inaccessible sources
unavailable and request an export or excerpt only when needed.

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
