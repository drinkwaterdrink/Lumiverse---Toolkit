# Lumi Tools v0.3 — World Forge and Card Types Design

Status: approved architecture, implementation not started  
Target release: `0.3.0`  
Prepared: 2026-09-05

## 1. Outcome

Lumi Tools v0.3 will add a sixth bundled specialist, **Lumiverse World Forge**, and make the plugin capable of producing more than single-person cards. A user will be able to describe a person, household, cast, scenario, setting, or complete roleplay world and receive the appropriate ready-to-import artifact rather than being forced into one card shape.

The primary new deliverable is a Lumiverse-ready V3 CHARX narrator or ensemble card with an embedded `character_book`. The same build also retains editable source artifacts and validation evidence so the CHARX is not the only recoverable copy.

This release builds on the v0.2 evidence:

- the installed Character Forge generated a V3 CHARX;
- the user successfully imported that generated CHARX into Lumiverse;
- the current packager preserves complete supplied card JSON and opaque archive members;
- Lorebook Forge and Preset Converter are already bundled.

The release does not claim undocumented Lumiverse-native World Book schema support, automatic attachment of multiple books through a standard CHARX, or runtime behavior that has not been observed.

## 2. Scope

### Included

1. A new `lumiverse-world-forge` skill.
2. Five card/package profiles sharing one canon model.
3. A compiler from Lorebook Forge's neutral entry model to an embedded Character Card V3 `character_book`.
4. Narrator-card and ensemble-card field-placement rules.
5. Embedded-lorebook CHARX packaging, validation, and readable backup output.
6. Alternate greetings as distinct entry points into a world or scenario.
7. Large-cast batching, resumable checkpoints, temporal audits, and relationship audits.
8. Updated Project Steward routing and release evidence.

### Excluded from v0.3

- Preset Studio and model-specific preset tuning.
- Prompt & Regex Laboratory mechanics.
- Tracker, LumiScript, and Spindle Extension generation.
- Invented `lumiverse_modules.json` fields for alternate fields, avatars, or expressions.
- Image generation or automatic avatar creation.
- A graphical wizard or MCP server.
- Automatic conversion of one embedded book into multiple Lumiverse-native bound books.
- Full-fidelity standalone Lumiverse World Book export without a current native export template.

Those exclusions keep v0.3 focused on authoring and packaging card-shaped roleplay worlds.

## 3. Product model

### 3.1 One canon core, several deliverables

All profiles use a shared project record containing:

- approved and provisional facts;
- stable entity IDs and aliases;
- temporal status and location when relevant;
- relationship claims from each participant's perspective;
- user-agency constraints;
- artifact ownership for each fact;
- source provenance;
- unresolved decisions;
- validation evidence.

The project record is the coordination source, not content injected into every prompt. Each compiler selects only the facts needed by its target artifact.

### 3.2 Profiles

| Profile ID | User intent | Primary output | Lore handling |
|---|---|---|---|
| `single_character` | Chat with one person | One CHARX | No embedded book unless explicitly useful and approved |
| `character_with_world` | One person needs supporting setting/history | One CHARX | Embedded character book linked on import |
| `narrator_world` | Chat with a setting/world through a narrator | One narrator CHARX | Embedded rules, setting, NPC, faction, location, item, and history entries |
| `ensemble_scenario` | One card runs a household, group, location, or scenario cast | One narrator/ensemble CHARX | Embedded cast and scenario-support entries |
| `multi_card_world` | Several independently playable characters share a world | Multiple CHARX files plus shared book artifacts | Shared lore is not duplicated into every card; each card remains intelligible alone |

A standalone World Book request continues to route directly to Lorebook Forge. World Forge may coordinate that specialist when the book belongs to a larger card package.

### 3.3 Routing decision

World Forge infers a recommended profile from the requested interaction model:

- “I want to chat with this person” → `single_character`.
- “This character needs their setting bundled” → `character_with_world`.
- “The AI should narrate and run the whole world” → `narrator_world`.
- “The AI should play this family/cast/household” → `ensemble_scenario`.
- “I want separate playable cards in the same setting” → `multi_card_world`.

If two profiles would create materially different files, World Forge presents the recommendation and one concise alternative before generation. It does not force the user through a long mode menu when the request is already clear.

## 4. Specialist boundaries

### World Forge

Owns profile selection, world/narrator architecture, shared canon distribution, build checkpoints, cross-artifact assembly, and final package completeness.

### Character Forge

Owns person-specific fields, narrator-card field authoring, preservation of existing cards, and final CHARX archive packaging. Its existing `package_charx.py` remains the archive writer.

### Scenario Forge

Owns the playable opening, unresolved pressures, alternate entry points, and agency-safe scenario framing. A Scenario Forge seed is design input; it is not pasted wholesale into a card.

### Lorebook Forge

Owns entry content, keywords, activation policy, position/depth/priority recommendations, collision tests, and the canonical neutral lore specification. A new embedded-book compiler maps the verified Character Card V3 subset.

### Project Steward

Owns stable IDs, canon precedence, cross-artifact dependencies, change propagation, validation records, and release coordination.

No specialist reproduces another specialist's full instructions. World Forge exchanges bounded handoff records and merges results by stable ID.

## 5. Authoring contracts

### 5.1 Narrator world card

The narrator card is the interface to the world, not a disguised lead character.

| Card field | Content |
|---|---|
| `name` | World or scenario title |
| `description` | Lean premise, narrator scope, and the world's relationship to `{{user}}` |
| `personality` | Narration voice, emotional register, descriptive habits, and NPC differentiation |
| `scenario` | Current open situation, temporal frame, starting constraints, and unresolved pressures |
| `first_mes` | A playable opening scene that does not decide `{{user}}`'s voluntary actions or feelings |
| `mes_example` | Short examples demonstrating narration, distinct NPC voices, quiet scenes, and pressure without puppeting the user |
| `system_prompt` | Empty by default; used only when the user requests it or verified source behavior requires it |
| `post_history_instructions` | Empty by default; preservation-first for revisions |
| `creator_notes` | Human-facing use notes, package scope, and evidence limits |
| `alternate_greetings` | Distinct entry points differing by place, time, role, or inciting circumstance |

The card explicitly establishes that it may narrate the environment and voice non-user characters while `{{user}}` retains their own thoughts, dialogue, feelings, decisions, consent, history, abilities, and voluntary actions.

### 5.2 Ensemble scenario card

An ensemble card uses the same narrator contract but gives the recurring cast greater emphasis. It must:

- keep each cast member's voice, knowledge, motives, and relationships distinct;
- allow characters to act offscreen or pursue their own goals without converting that autonomy into control over `{{user}}`;
- distinguish established facts from provisional generated details;
- avoid collapsing all cast members into a single shared mind;
- keep deep cast profiles in the embedded book instead of repeating them in always-loaded card fields.

### 5.3 Character-with-world card

The person remains the primary conversational identity. The embedded book provides relevant places, history, NPCs, factions, items, and setting rules. It must not turn the character into an omniscient narrator or grant them knowledge merely because an entry activated.

### 5.4 Multi-card world

Each playable character receives only character-specific identity and viewpoint. Shared setting facts have one canonical home in the shared book source. Relationships are written from each character's perspective and audited for intentional or accidental asymmetry.

The first implementation outputs:

- one CHARX per playable character;
- one canonical neutral LoreForge specification;
- one Character Book-compatible shared backup;
- setup instructions explaining that automatic attachment of the shared standalone book has not been claimed.

The build does not embed duplicate copies of the shared book into every character unless the user explicitly chooses one-file portability over centralized maintenance.

## 6. Embedded book design

### 6.1 One-file import shape

The standard one-file narrator, ensemble, or character-with-world package contains one `data.character_book` with an `entries` array. Lumiverse documentation states that an embedded `character_book` is extracted, created as a separate World Book, linked to the imported character, and activated in that character's chats.

For v0.3, the one embedded book contains logical entry categories rather than pretending a standard CHARX can automatically bind several distinct books:

- governance and agency;
- setting rules;
- NPC/cast profiles;
- locations;
- factions and organizations;
- items;
- history and events;
- concepts and systems.

### 6.2 Activation policy

Activation settings are authored per entry. The compiler does not force recursion, constant faction anchors, fixed order bands, or identical depth on every world.

Defaults are conservative:

- governance entries may be constant when always needed;
- ordinary lore is conditional;
- keywords are specific natural aliases;
- secondary/selective conditions are added for collisions;
- recursion is enabled only when an intended and tested dependency chain needs it;
- sticky, cooldown, delay, groups, vectorization, and probability are opt-in based on an explicit use case;
- budget and priority decisions are recorded in the LoreForge specification.

The current Lumiverse docs do not publish every native JSON property. The compiler maps only fields supported by the supplied V3 Character Book reference and observed CHARX structure. Unsupported neutral-spec properties remain documented in the manifest rather than being silently invented or discarded.

### 6.3 Editable backups

Every embedded-book build produces:

1. the ready-to-import CHARX;
2. the complete card JSON used for packaging;
3. the canonical neutral LoreForge specification;
4. an extracted Character Book-compatible JSON backup matching the embedded book;
5. an import guide and artifact passport.

The backup is labeled **Character Book-compatible**, not “full-fidelity native Lumiverse,” unless it was created from and checked against a native Lumiverse export template.

## 7. WorldBuilder concepts and disposition

The design incorporates useful concepts from the supplied local review copy of `PoweringManipulation2/WorldBuilder` without copying its code or story content.

| WorldBuilder concept | v0.3 decision |
|---|---|
| Character, world, lorebook, group, persona, and style modes | Adopt the useful routing concept; implement the five card/package profiles above. Persona and style extraction remain separate future features. |
| Source-first research | Adopt with user canon first. Outside/current research occurs only when requested or required and is labeled separately. |
| Temporal accuracy | Adopt as a canon audit and per-entity temporal status. |
| Relationship reciprocity | Adopt while permitting deliberate one-sided beliefs and misconceptions. |
| Batch generation | Adopt for large casts/books with saved checkpoints and validation between batches. |
| Large-cast tiers | Adopt as detail-allocation guidance, never as permission to omit user-requested fields. |
| Alternate world entry points | Adopt through `alternate_greetings`. |
| Thin world card plus deep lore | Adopt; keep the narrator contract and open situation in the card, deep reusable facts in the book. |
| Recursive tree always enabled | Reject as a universal rule; recursion must have a designed chain and tests. |
| Constant faction/cast anchors | Reject as a universal rule because always-loaded anchors can waste budget. |
| Fixed insertion-order tiers | Reject as a universal rule; use Lumiverse semantics and project-specific priorities. |
| Strip the world card's scenario field | Reject; the supplied Lumiverse card evidence uses `scenario`, and the field has a distinct useful role. |
| SillyTavern V1 backfill and schema assumptions | Do not make global Lumiverse requirements. Preserve them only when converting a source that needs them. |

## 8. Build workflow

### Stage 1 — Intake and profile

World Forge identifies the requested interaction model, existing sources, expected scale, canon authority, desired output, and whether the user wants guided, fast, or full-detail authoring.

### Stage 2 — Canon inventory

The build records supplied facts, protected user-character facts, provisional additions, conflicts, temporal constraints, and stable entity IDs. Existing cards/books are inventoried whole before editing.

### Stage 3 — Blueprint

The user receives a compact build blueprint: profile, narrator/player boundary, core premise, cast tiers, proposed book categories, entry-point plan, and major unresolved decisions. Fast mode collapses this to one approval checkpoint; guided mode asks one decision at a time.

### Stage 4 — Specialist authoring

Scenario Forge produces the open play structure. Character Forge authors card or character fields. Lorebook Forge creates the neutral entry specification and activation tests. Project Steward reconciles shared facts and relationships.

Large projects are written in bounded batches. Each batch records completed stable IDs and may resume without regenerating accepted entries.

### Stage 5 — Compile and package

The embedded-book compiler creates the verified V3 `character_book` subset. Character Forge packages the complete card JSON and assets into a new CHARX filename. Existing source CHARX archives are preservation sources, never overwritten.

### Stage 6 — Validate and hand off

The toolkit validates JSON, IDs, fields, assets, book references, keyword collisions, canon, temporal state, relationships, agency, and artifact hashes. It distinguishes deterministic checks, user-reported import results, and unperformed runtime checks.

## 9. File and interface changes

Planned additions:

```text
skills/lumiverse-world-forge/
  SKILL.md
  agents/openai.yaml
  references/
    profiles-and-routing.md
    narrator-and-ensemble-contract.md
    build-workflow.md
    worldbuilder-concepts-review.md
    validation-and-release.md
  assets/
    world-project.template.json
    package-manifest.template.json

skills/forge-lumiverse-lorebooks/scripts/
  compile_character_book.py

shared/schemas/
  world-project.schema.json
  world-package-manifest.schema.json

tests/
  test_world_profiles.py
  test_embedded_character_book.py
  test_world_package_contract.py
  fixtures/world_forge/
```

Planned updates:

- Project Steward routing and handoff documentation;
- Character Forge workflow and CHARX packaging reference;
- `package_charx.py` validation only where new verified invariants are required;
- README, changelog, marketplace version, provenance, and verification report;
- deterministic and behavior tests.

## 10. Error handling and preservation

- If the requested profile is ambiguous and changes the deliverable, ask one focused question.
- If a source archive exists, preserve unknown card keys, extensions, assets, and archive members.
- If the compiler cannot map a requested advanced book setting, fail that mapping visibly and keep it in the neutral spec.
- If a referenced embedded asset is missing, refuse packaging and identify the exact archive path.
- If duplicate stable IDs, supported serialized entry IDs, or conflicting canon are found, stop assembly until reconciled.
- If the project exceeds one reliable generation batch, save a checkpoint and resume by stable ID.
- If an existing Lumiverse World Book name may collide on import, warn that the provided docs do not specify conflict behavior.
- Never report import, attachment, activation, or roleplay success from static validation alone.
- Never overwrite source cards or prior exports.

## 11. Testing strategy

### Deterministic tests

1. All five profiles route to the correct artifact set.
2. Embedded `character_book.entries` is an array of objects; the editable source and compiler manifest retain unique stable IDs, while serialized entry IDs are emitted only when supported by the selected target structure.
3. Constant and conditional entries retain their intended states.
4. Unsupported neutral properties are reported in the package manifest.
5. CHARX integrity, exclusive output, traversal defense, size limits, and asset references continue to pass.
6. Existing single-character Mara packaging remains backward compatible.
7. Source revisions preserve unknown JSON and archive members.
8. Multi-card packages do not duplicate shared canon by default.
9. Relationship and temporal contradictions produce actionable findings.
10. Agency violations are release blockers.

### Synthetic fixtures

- a small narrator world with rules, two NPCs, and two locations;
- a household ensemble with four distinct adults;
- a character-with-world card with one supporting location and NPC;
- a three-character multi-card package with a shared setting;
- a preservation fixture containing unknown extensions and embedded assets.

The supplied *Chained Crown* card remains private reference evidence. Its story content and artwork are not committed as test fixtures. Synthetic fixtures test equivalent structure without redistributing the attachment.

### Behavior samples

Behavior tests check that World Forge:

- selects or explains the appropriate profile;
- keeps narrator and single-character roles distinct;
- protects `{{user}}` agency;
- does not make every lore entry constant;
- labels provisional additions;
- produces distinct alternate greetings rather than paraphrases;
- distributes shared and character-specific facts correctly.

### Release verification

Before publishing v0.3:

1. run the full existing and new unit-test suite;
2. run plugin validation;
3. install from the published marketplace in a fresh Codex session;
4. verify all six bundled skills load and all references resolve;
5. generate one synthetic narrator-world package using the installed plugin;
6. verify its CHARX structure and embedded book statically.

After publishing, one user-observed Lumiverse smoke test imports the narrator CHARX and confirms that the import summary reports the embedded World Book and entry count. A short runtime conversation is useful evidence but is not a blocker for the authoring/export milestone because output behavior varies with preset and model.

## 12. Acceptance criteria

v0.3 is complete when:

- one plugin installation exposes World Forge and the existing five specialists;
- a clear brief can produce the correct profile without unnecessary questioning;
- narrator and ensemble builds produce complete V3 CHARX files with embedded books;
- imported-source revisions preserve unknown content;
- every build includes editable card/book sources and evidence records;
- deterministic tests and plugin validation pass;
- the published package matches the verified source;
- limitations around native World Book fidelity and untested runtime behavior remain explicit;
- no third-party WorldBuilder code, prose, artwork, or fixed SillyTavern assumptions are distributed.

## 13. Subsequent roadmap

After v0.3, the recommended order remains:

1. Preset Studio for native creation, editing, and auditing.
2. Prompt & Regex Laboratory.
3. Tracker Forge.
4. LumiScript Workshop.
5. Spindle Extension Forge.

Persona Forge, prose-style extraction, a visual workbench, and broader Weaver package integration can be added when they have a concrete user workflow and verified target format.
