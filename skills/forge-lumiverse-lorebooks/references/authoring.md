# Lorebook entry authoring

## Contents

1. Atomic entry contract
2. Content design
3. Keyword engineering
4. Runtime metadata
5. Book patterns
6. Recommended starting heuristics

## 1. Atomic entry contract

An entry should retrieve one coherent concept: one location, rule, faction, person, item, event, custom, system, or current state. Split an entry when one trigger would inject facts irrelevant to the current subject. Keep facts together when splitting would force both fragments to activate every time to make sense.

Require two rationales:

- **Content rationale**: why these facts belong together and what play they enable.
- **Activation rationale**: why these triggers and runtime settings surface the entry at the right time.

## 2. Content design

Prefer dense, operational prose:

- identify the thing immediately
- state rules, capabilities, costs, relationships, and scene-visible details
- distinguish public fact, hidden truth, rumor, and character belief
- use names and aliases consistently
- include consequences and exceptions when they drive play
- omit ornamental prose that adds tokens without influencing a scene

Do not:

- repeat the same canon in multiple entries
- encode current arc state as permanent history
- state private secrets as universally known
- add generic genre conventions as world fact
- use instructions where factual lore is enough
- turn an entry into a miniature chapter

## 3. Keyword engineering

For each conditional entry, design:

1. **Canonical names**: exact name, title, abbreviation.
2. **Natural aliases**: what participants actually type.
3. **Selective context**: secondary terms only when primary terms are ambiguous.
4. **Exclusions**: near misses and common substrings.

Avoid generic trigger words such as `city`, `magic`, `mother`, or `school` unless secondary logic makes them precise. Use whole-word matching for common tokens with dangerous substrings. Use regex only when the pattern is simpler and safer than a list of phrases.

Every entry needs:

- a positive test that should activate
- a negative near miss that should not
- a collision test against the most similar entry

## 4. Runtime metadata

### State

- Conditional for most lore.
- Constant only for rules or identity floors that must always be present.
- Disabled for parked material.

### Position and depth

Choose by desired influence:

- Position 0 or 1 for stable context outside recent-message recency.
- Position 4 for immediate quest, danger, or current-scene state; use depth 0–2 only when strong next-response influence is intended.
- Positions 2/3 only when Author's Note adjacency is deliberately useful.
- Positions 5/6 only when example-message adjacency is deliberately useful.

Use System role for ordinary lore. User/Assistant roles need an explicit behavioral reason.

### Order and priority

Lower order values appear first within the same position/depth. Higher priority survives budgets. Do not use order as a substitute for priority.

### Timing

- Short scan depth + modest sticky for scene-local persistence.
- Cooldown for entries that should not immediately repeat.
- Delay for sustained-state activation, not a one-off mention.
- Probability only when randomness is desired.

### Groups and recursion

Use a group for mutually exclusive candidates. Give an override only to a candidate that must always beat siblings. Use weights only when random competition is intended.

Use recursion for explicit dependency chains such as a faction entry surfacing a named leader entry. Mark hub entries to prevent or exclude recursion when their dense content would fan out uncontrollably.

### Vectorization

Recommend vectorization for concept-rich entries whose natural references are too varied for keywords, provided embeddings are configured. Keep exact names as keywords even when vectorized. Do not use vectorization to compensate for vague content.

## 5. Book patterns

### Immutable world book

Rules, factions, species, institutions, standing locations, customs, cosmology, durable history.

### Entity/persona book

Permanent identity, appearance, background, relationships, knowledge boundaries, preferences, stable capabilities. Attach to the relevant character or persona when possible.

### Arc/state book

Current conditions, changed relationships, active threats, quest state, recently revealed facts, live secrets, tonal state. Keep separate when it must be swapped or revised often.

### Weaver companion

- lore book: places, history, factions, customs, triggered deep detail
- NPC book: one profile per person
- rules book: always-on narrator governance and re-anchor

Do not move deep lore into the thin narrator card.

## 6. Recommended starting heuristics

These are recommendations, not documented Lumiverse defaults:

- Keep most entries under roughly 250–450 words; split when retrieval precision improves.
- Use 3–8 deliberate primary keywords rather than a large noisy synonym cloud.
- Use priority bands such as 90 critical, 60 core, 30 flavor when explicit prioritization helps.
- Use order increments of 10 so later insertions fit between entries.
- Begin with recursion off unless a tested dependency needs it.
- Begin with vectorization off unless embeddings are known to be configured.
- Keep constants few enough that they cannot dominate the intended World Info budget.
