# Lumiverse Capability Map

This is a routing map, not a serialization schema. Verify current documentation
and a contemporary native export before emitting version-sensitive fields.

## Character surfaces

Current supplied Lumiverse guidance documents Description, Personality,
Scenario, First Message, Alternate Greetings, Example Messages, System Prompt,
Post-History Instructions, Creator Notes, tags, avatar handling, alternate
description/personality/scenario fields, alternate avatars, expressions,
embedded lorebooks, and CHARX modules. Import/export coverage includes PNG,
JSON, and CHARX paths, but exact envelopes and module keys remain
version-sensitive.

## World Books

Current supplied guidance documents primary and secondary keywords, selective
logic, regex and matching options, scan depth, constant/disabled state,
probability, positions, depth, role, order, priority, sticky/cooldown/delay,
groups and weights, recursion controls, activation limits, token budget,
vectorization, attachment scopes, import/export, Dry Run, and diagnostics.
Entry settings must be chosen by activation intent rather than defaulted from
book size.

## Prompt and state capabilities

Current Lumiverse macro guidance distinguishes identity/character/chat macros,
numeric random and categorical choice, logic, strings, formatting, retrieval,
Council/Lumia, and Prompt Variables. Variable scopes are not interchangeable:
`.` is evaluation-local, `@` is chat-persisted, `$` is global, and
`var::name` is a user-facing preset Prompt Variable. Repeated random macros are
not assumed to cache; store a draw deliberately when reuse is required.

## Related systems

- World Books: static or conditionally activated structured lore.
- Databank: large uploaded reference sources and RAG-oriented documents.
- Long-Term Memory: recalled events from actual chat history.
- Memory Cortex: evolving entity, relationship, and arc memory when enabled.
- Loom Summary: compressed narrative continuity.
- Personas: user-selected identity context and attachments.
- Council/Lumia: optional sidecar deliberation and analysis.
- Weaver: native world authoring with thin narrator and bound-book patterns.
- Spindle: optional future runtime/UI functionality, never required for ordinary
  static artifacts.

## Foreign terminology

Terms such as “Lore Buffer / Context %,” “Retrieval Mode,” “Embeddings Hook,”
or “Lore Recall Tree Structure” may describe useful concepts from another tool.
**No direct documented Lumiverse equivalent** should be claimed solely from the
foreign name. Map it to the actual current Lumiverse feature when documented;
otherwise state: “No direct documented Lumiverse equivalent; no field was
serialized.”
