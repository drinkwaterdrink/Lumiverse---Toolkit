# Lorebook Forge workflow

## Contents

1. Operation routing
2. Phase 0 interview
3. Phase 1 master design
4. Phase 2 entry architecture
5. Phase 3 audit loop
6. Phase 4 export and handoff
7. Revision and expansion

## 1. Operation routing

Choose one primary operation:

| Operation | Starting input | Main result |
|---|---|---|
| New build | Idea or short brief | New book or pack |
| Source conversion | Files, chats, wiki, cards, preset | Canon-extracted pack |
| Weaver companion | Weaver world/card/books | Deeper or audited lore/NPC/rules books |
| Expand | Existing book plus new idea | Append-only entries |
| Revise | Existing book plus named change | Scope-locked replacement/addition |
| Audit | Existing book | Findings and optional correction plan |

For a source conversion, establish an authority order. Prefer explicit current canon over older notes, user corrections over inference, and source-grounded facts over plausible filling.

## 2. Phase 0 interview

### Mobile pacing

Ask one question at a time by default. Use two or three only when they form one compact choice. Keep a visible progress phrase such as “World spine 2/6.” Offer two or three concrete directions when the user is unsure, plus free text. Preserve the user's answer before extending it.

### Required spine

Collect only what changes the book:

1. **Purpose**: what play should this lore make possible?
2. **Target**: which character, persona, shared setting, or Weaver world uses it?
3. **Premise and sensory identity**: what makes the setting recognizable in a scene?
4. **Rules with teeth**: cost, limits, enforcement, exceptions, consequences.
5. **Actors**: factions, institutions, species, NPCs, agendas, relationships.
6. **Places and systems**: locations, history, customs, magic/technology/economy.
7. **Mutability**: permanent truth versus current arc/state.
8. **Secrets and epistemics**: who knows what, and what must not become omniscient canon?
9. **Hard boundaries**: unwanted content or behavior.
10. **Test scenes**: three to five moments whose relevant lore must surface.
11. **Creative authority**: ask before new canon, draft unapproved proposals, or creative license.

Do not ask for every possible category. Skip categories irrelevant to the concept. Push when a missing answer would create contradictory or nonfunctional entries; stop when extra detail would be decorative.

Substantive inventions include proper names, rules, costs, history, relationships, factions, secrets, and outcomes. Under `ask_before_new_canon`, ask before adding them. Under `proposals_only`, label them as proposed and keep them out of the canonical spec/export until accepted. Under `creative_license`, invent within the user's boundaries and identify material additions in the handoff. Clarifying prose is not new canon.

### Seed gate

Proceed only when the target, book shape, core canon, mutability, and test scenes are clear. Mark remaining optional gaps. Stop on material contradictions.

## 3. Phase 1 master design

Create a canonical design with:

- source authority order
- creative-authority mode and approval status of any proposed additions
- glossary of canonical names and aliases
- premise and intended experience
- immutable world facts
- entity/persona facts
- mutable current/arc facts
- secret and perspective boundaries
- dependency graph
- book manifest and activation-scope rationale
- unresolved questions
- test-scene coverage matrix

### Book-shape heuristics

- **Focused book**: one topic or modest setting used under one scope.
- **Tiered pack**: world truth + entity/persona truth + mutable state are large enough to manage separately.
- **Arc pack**: immutable base plus one swappable book per arc; never require old and new arc state simultaneously unless explicitly designed.
- **Standing sandbox pack**: immutable base plus an always-available standing situation and conditional world pulse; no fake arc progression.
- **Weaver companion**: keep rules/governance, deep lore, and people profiles in their existing book responsibilities.

The three-tier idea is a content-ownership rule, not a prompt-position rule:

1. permanent world truth
2. permanent entity/persona truth
3. mutable arc/scene/state truth

Every fact gets one canonical home. Cross-reference; do not duplicate paragraphs.

### Master-design gate

Proceed only when every intended fact has a home, contradictions are resolved or intentionally POV-bound, and every book has a scope and activation strategy.

## 4. Phase 2 entry architecture

Write the platform-neutral `LoreForge Spec`. For each entry:

- stable ID and title
- canonical book ID
- category and state
- concise content
- primary and secondary keywords
- selective logic label in plain language
- case/whole-word/regex intent
- scan depth and probability
- position, depth, role, order, priority
- sticky/cooldown/delay
- group behavior
- recursion behavior
- vectorization intent
- content and activation rationales
- tests

Use `references/authoring.md` for entry writing and metadata selection.

## 5. Phase 3 audit loop

Run these independent lenses:

1. Canon and ownership audit.
2. Entry prose and token audit.
3. Activation precision audit.
4. Position/depth/role audit.
5. Budget and priority audit.
6. Recursion/group/timing audit.
7. Scenario coverage audit.
8. Adversarial false-positive and collision tests.

Write findings before changes. Blocking findings return the affected entries to architecture. Repeat validation after repair.

## 6. Phase 4 export and handoff

Retain the neutral spec. Export native-template or portable format per `references/export.md`. Produce the manifest, runtime audit, activation report, import guide, attachment map, and limitations.

Recommend that the user import one book first, attach it, run Dry Run on three expected triggers plus two near misses, inspect Diagnostics, then import the rest. This isolates schema and activation errors.

## 7. Revision and expansion

### Revision

1. Name the exact desired change.
2. Compute the smallest cascade of affected books/entries/tests.
3. Ask before expanding scope.
4. Preserve stable IDs on modified entries.
5. Replace content in place; do not retain the old paragraph as a duplicate.
6. Re-run only affected tests plus global collision and budget checks.

### Expansion

Default to append-only. Never overwrite hand-edited entries. Check whether a proposed new entry belongs as an addition, a replacement, or a cross-reference. Assign a new stable ID only for genuinely new content.
