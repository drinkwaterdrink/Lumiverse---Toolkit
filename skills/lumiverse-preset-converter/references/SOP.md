# SillyTavern Chat Completion → Lumiverse Preset Conversion SOP
## One-Shot Forensic Migration Standard v1.1

**Research baseline:** August 30, 2026
**Purpose:** Convert a SillyTavern **Chat Completion** preset into a Lumiverse-native Loom preset with behavioral parity first, then optional Lumiverse-native improvements.
**Target quality:** A conversion should not be considered complete merely because Lumiverse imports the JSON. It must preserve the source preset's effective prompt, execution semantics, state behavior, generation routing, sampling/completion behavior, regex behavior, and external dependencies—or explicitly document where exact parity is impossible.

---

# 0. Executive rule

The single most important rule is:

> **Convert the behavior, not the JSON keys.**

SillyTavern and Lumiverse overlap heavily in concepts and macro syntax, but the same-looking construct can have a different lifetime, execution order, randomization behavior, or injection meaning. A mechanical search-and-replace can produce a preset that imports, generates prose, and still be wrong in subtle ways.

A professional conversion therefore has six separate success levels:

1. **Import parity** — Lumiverse accepts the file.
2. **Structural parity** — the same logical prompt components are present.
3. **Macro parity** — macros resolve to equivalent values.
4. **Behavioral parity** — prompt order, state, randomness, routing, and card overrides behave the same.
5. **Operational parity** — regexes, extensions, reasoning, group-chat behavior, utility prompts, and provider settings still work.
6. **Native Lumiverse edition** — after parity is proven, Lumiverse-native controls and features are added without changing the source's intended behavior unless the change is deliberate and documented.

Do not call a conversion “Lumiverse-native” at levels 1–4.

---

# 1. Source-of-truth and evidence policy

## 1.1 Evidence hierarchy

When two pieces of evidence disagree, use this priority:

1. **Observed current Lumiverse Dry Run / runtime behavior**
2. **Observed current SillyTavern runtime behavior**
3. **Current official Lumiverse documentation**
4. **Current official SillyTavern documentation**
5. **A current native Lumiverse export from the same Lumiverse version**
6. **The source preset's own README/comments**
7. **Known extension documentation/source**
8. **Inference**

Never silently promote an inference into a platform fact.

## 1.2 Version discipline

Both applications evolve. Treat internal export JSON as **version-sensitive serialization**, not a timeless public schema.

Before generating a new Lumiverse JSON:

- export one ordinary working Lumiverse preset from the **same Lumiverse build** that will import the conversion;
- use that export as the envelope/skeleton;
- preserve wrapper fields and serializer conventions from that current export;
- modify documented semantic fields;
- avoid inventing internal fields from memory.

This matters because a native export may contain wrapper metadata, compatibility fields, cached Prompt Variable selections, profile data, regex bundles, and duplicated convenience export fields that are not fully described by conceptual documentation.

A fresh native reference export from the user's target build is useful precisely for this reason: it can demonstrate contemporary prompt blocks, Prompt Variables, placement binding, generation triggers, character-tag triggers, completion settings, sampler overrides, and embedded regex scripts. It is a **reference implementation**, not a universal schema contract.

## 1.3 Required finding labels

Every audit finding should be classified as one of:

- **PASS**
- **PASS WITH ASSUMPTION**
- **REQUIRED FIX**
- **ENVIRONMENT DEPENDENCY**
- **INTENT DECISION**
- **PERFORMANCE RISK**
- **VERSION-SENSITIVE**
- **UNSUPPORTED / NO DIRECT EQUIVALENT**

Severity:

- **P0 / Critical** — can corrupt prompt assembly, state, role, or stored content.
- **P1 / High** — materially changes behavior or a major feature.
- **P2 / Medium** — feature degrades under certain routes/models.
- **P3 / Low** — cleanup, UX, maintainability, cosmetic parity.

---

# 2. Scope — SillyTavern Chat Completion presets

This SOP is intentionally scoped to **SillyTavern Chat Completion presets**, i.e. presets built around the Prompt Manager and Chat Completion APIs.

A Chat Completion preset's effective behavior may include more than its visible prompt text:

- prompt definition pool;
- active `prompt_order`;
- prompt enabled/disabled state;
- System / User / Assistant roles;
- Relative vs In-Chat placement;
- depth and same-depth order;
- generation triggers;
- Main Prompt / Auxiliary Prompt / Post-History Instructions;
- Persona / Character Description / Personality / Scenario / Example / Chat History slots;
- World Info before/after;
- utility prompts;
- Group Nudge;
- Continue Nudge / Continue Prefill / Continue Postfix;
- Replace Empty Message;
- character-name behavior;
- Prompt Post-Processing;
- reasoning settings;
- web search / function calling / inline media toggles where relevant;
- sampler and context settings;
- custom stop strings / assistant prefill;
- Regex scripts;
- extension-registered macros;
- tracker/image/summary/other extension dependencies.

The conversion target is not “the JSON imports.” The target is **the same effective Chat Completion behavior in Lumiverse**, followed by an optional Lumiverse-native UX/runtime enhancement pass.

## 2.1 Hybrid / extension-driven Chat Completion presets

Some presets depend heavily on:

- Regex;
- STscript or Quick Replies;
- Image Generation;
- vector/database extensions;
- summary extensions;
- tracker extensions;
- model router/proxy behavior;
- custom macros registered by extensions;
- external sidecar generations.

These must be converted as a **system**, not as prompt text alone.

## 2.2 Provider-specific Chat Completion packages

Some presets contain model-specific workarounds such as:

- hard-coded reasoning wrappers;
- provider-specific assistant prefills;
- quantization workarounds;
- model-family “leash” prompts;
- source-specific prompt-post-processing assumptions.

Preserve the *intent*, but do not assume provider framing tokens or transport workarounds should survive unchanged when moving to a different Lumiverse connection.

---

# 3. Mandatory input packet

A “one-shot” converter should request or gather as much of the following as exists.

## 3.1 Always obtain

- source Chat Completion preset JSON;
- source preset name/version;
- target model/provider;
- source model/provider for which it was designed;
- source enabled/disabled defaults;
- companion Regex exports;
- creator README/setup notes if available;
- at least one representative character card for testing;
- target Lumiverse version or a fresh native Loom export.

## 3.2 For SillyTavern Chat Completion

Also capture:

- active `prompt_order`, including every character/order variant;
- Prompt Manager utility prompts;
- Prompt Post-Processing mode;
- reasoning settings;
- Start Reply With / assistant prefill;
- custom stopping strings;
- connection profile if the preset is provider-coupled;
- character Main Prompt/Post-History override behavior if used.

## 3.3 External dependencies

Build a dependency table:

| Dependency | Source | Required? | Lumiverse equivalent | Migration status |
|---|---|---:|---|---|
| Regex pack | ST Regex | Yes/No | Lumiverse Regex | |
| Summary macro | extension/core | | Summary/Loom/Memory decision | |
| Tracker | extension | | Spindle/native tracker | |
| Image generation | extension | | Lumiverse Image Generation | |
| Quick Reply/STscript | extension/script | | Quick Reply / Regex Action / Spindle | |
| Custom macro | extension | | Native macro / extension macro | |
| World Info | lorebook | | Lumiverse World Book | |
| Web search | backend/extension | | connection / Lumiverse web search | |

If a dependency is missing, do not advertise that feature as working.

---

# 4. Freeze the source before touching it

Create a migration workspace:

```text
/source
  source-preset.json
  source-regex.json
  source-context-template.json
  source-instruct-template.json
  source-sysprompt.json
  source-notes.md

/reference
  current-native-lumiverse-export.json

/output
  preset-parity.json
  preset-native.json
  regex-native.json
  audit-report.md
  validation-report.txt
  changelog.md
```

Calculate hashes of all source Chat Completion artifacts.

Record:

- source block count;
- source prompt IDs;
- source effective prompt order;
- enabled count;
- macro count;
- variable set/get count;
- random call count;
- regex count.

**Never “clean up” the prose before the mechanical/semantic audit.** First reproduce what the source does. Optimize only after parity.

---

# 5. Phase I — Forensic source inventory

## 5.1 Parse the JSON without interpretation

Inventory every root key.

Do not delete unknown fields because they “look unused.”

Classify each as:

- sampler;
- completion behavior;
- prompt definition;
- prompt-order control;
- provider behavior;
- display/UI metadata;
- extension metadata;
- unknown.

## 5.2 Build a prompt-definition table

For every source prompt record capture:

| Field | Record |
|---|---|
| identifier / ID | exact |
| name | exact |
| content hash | SHA-256 or similar |
| role | system/user/assistant |
| enabled | source state |
| source order | array index |
| effective order | from prompt order |
| position | Relative / In-Chat |
| depth | if In-Chat |
| order | tie-breaking order |
| triggers | Normal/Continue/etc. |
| marker flags | if present |
| system-prompt flags | if present |
| override flags | e.g. forbid overrides |
| custom/unknown keys | preserve for analysis |

## 5.3 The critical SillyTavern order rule

For Chat Completion, the Prompt Manager is the authoritative prompt-building surface. Prompts nearer the top are sent earlier; the bottom is later, commonly ending with Post-History Instructions. Pinned/default prompt types cannot be removed in ST, but they can be disabled.


For Chat Completion, **do not assume the `prompts` array is the final order**.

Treat:

- the prompt records as a **definition pool**;
- the active Prompt Manager ordering / `prompt_order` as the **effective layout**.

If multiple `prompt_order` variants exist (for example character-specific order sets), do not collapse them into the first variant.

Possible Lumiverse targets:

- separate Preset Profiles;
- separate exported presets;
- a Prompt Variable / placement selector;
- documented manual variants.

## 5.4 Detect orphaned and dangling records

Fail static validation if:

- an active order entry references a nonexistent prompt;
- one prompt ID is duplicated unexpectedly;
- two different prompt bodies share an ID;
- a required default/structural slot is missing with no documented reason;
- a source order variant has incompatible enable states and the target silently chooses one.

## 5.5 Build an execution-feature inventory

Search every prompt for:

- all `{{...}}` macros;
- local variable setters/getters;
- global variables;
- STscript scoped `{{var::...}}`;
- `random`;
- `pick`;
- `roll`;
- `if`, `switch`, logical operators;
- `<think>` and other reasoning wrappers;
- HTML/XML output contracts;
- `<details>`;
- image prompt tags;
- hidden tracker tags;
- commands shown in prompt examples;
- extension macro names;
- World Info references;
- summary/memory references;
- model-name checks;
- generation-type checks;
- user/character/group macros.

Create a machine-readable macro inventory before rewriting anything.

---

# 6. Phase II — Reconstruct the source behavior graph

Do not map blocks until you understand the graph.

For every source prompt, answer:

1. **What data does it consume?**
2. **What variables does it write?**
3. **What later blocks depend on it?**
4. **What generation types use it?**
5. **Does it need to be before or after history?**
6. **Does it need to be at a precise in-chat depth?**
7. **Does its role matter?**
8. **Does it require a prior regex transformation?**
9. **Does it expect output to persist to future context?**
10. **Does it depend on a model/provider?**

Represent dependencies as edges:

```text
Block A --sets .mode--> Block C
Block B --sets random seed--> Block D
Regex X --strips HUD from prompt--> next generation
Tracker Y --provides macro--> Block E
```

This catches problems that a block-by-block converter misses.

---

# 7. Phase III — Establish the Lumiverse target skeleton

## 7.1 Do not hand-invent the outer JSON

Take a freshly exported working Lumiverse preset from the target installation and use it as the serializer reference.

Current Lumiverse-native exports may contain concepts such as:

- type/schema wrapper;
- preset metadata;
- `blocks`;
- Prompt Variable persisted selections;
- model/profile metadata;
- prompt behavior;
- advanced settings;
- sampler overrides;
- completion settings;
- passthrough metadata;
- extension bundles / regex exports;
- compatibility metadata.

The exact envelope is version-sensitive.

## 7.2 Semantic block model

A Lumiverse prompt block conceptually has:

- name;
- content;
- role;
- enabled state;
- position;
- depth;
- marker;
- color;
- locked state;
- injection trigger;
- group;
- Prompt Variables;
- optional placement selector/binding;
- optional character-tag triggers.

Use the **current native export** to determine how these are serialized.

## 7.3 Native roles

Lumiverse documents:

- `system`
- `user`
- `assistant`
- `user_append`
- `assistant_append`

Do not automatically “upgrade” ordinary ST user/assistant prompts into append roles. Append roles are a native tool for cases where joining the previous message is intentionally desired.

## 7.4 Native positions

Lumiverse documents:

- `pre_history`
- `post_history`
- `in_history`

`depth` matters for `in_history`.

---

# 8. Phase IV — Classify every source prompt semantically

Each source prompt must be assigned one target class:

1. **Structural marker**
2. **Ordinary pre-history content**
3. **Ordinary post-history content**
4. **True in-history injection**
5. **Utility behavior**
6. **Category / organizational UI**
7. **Disabled documentation**
8. **External dependency adapter**
9. **Provider/model adapter**

Do **not** map SillyTavern integer fields blindly.

---

# 9. Structural marker mapping

Lumiverse’s documented structural markers are:

| Lumiverse marker | Expands to |
|---|---|
| `char_description` | Character Description |
| `char_personality` | Character Personality |
| `scenario` | Character Scenario |
| `persona` | Persona description |
| `mes_examples` | Example Messages |
| `system_prompt` | Character System Prompt |
| `post_history_instructions` | Character post-history instructions |
| `chat_history` | Chat history |
| `world_info_before` | activated World Info before bucket |
| `world_info_after` | activated World Info after bucket |

## 9.1 Safe direct mappings from typical ST identifiers

Common ST pinned prompt concepts can map as:

| SillyTavern concept | Lumiverse |
|---|---|
| World Info Before | `world_info_before` |
| Persona Description | `persona` |
| Character Description | `char_description` |
| Character Personality | `char_personality` |
| Scenario | `scenario` |
| World Info After | `world_info_after` |
| Chat Examples | `mes_examples` |
| Chat History | `chat_history` |

## 9.2 Main Prompt is NOT automatically `system_prompt`

This distinction is extremely important.

A preset’s **Main Prompt text** is preset-authored instruction content.

Lumiverse’s `system_prompt` structural marker is character/card data.

Do not replace the preset’s Main Prompt with `system_prompt` merely because the words sound similar.

Instead:

- keep the preset Main Prompt as an ordinary content block;
- separately preserve character System Prompt override behavior if the source environment uses it;
- test with a character that has a System Prompt and one that does not.

## 9.3 Post-History Instructions require the same care

A source preset’s default Post-History Instructions content is not necessarily identical to the **character’s** post-history instruction field.

If ST runtime permits a character-card override:

- test source behavior with and without an override;
- build Lumiverse so exactly one intended instruction path reaches the provider;
- do not send both the preset default and card override unless the source does so.

## 9.4 Duplicate injection audit

A structural datum should normally enter the prompt once.

Flag combinations such as:

- `persona` marker **plus** an ordinary `{{persona}}` block;
- `char_description` marker plus `{{description}}`;
- `chat_history` marker plus a custom transcript macro;
- World Info marker plus an explicit aggregate macro;

unless the duplication is deliberate.

---

# 10. Phase V — Placement, role, depth, and order conversion

## 10.1 SillyTavern Relative prompts

ST Relative prompts are ordered by the Prompt Manager list.

For each:

- if before Chat History → normally `pre_history`;
- if after Chat History → normally `post_history`.

Preserve block order.

## 10.2 SillyTavern In-Chat prompts

ST documents:

- depth 0 = after latest message;
- depth 1 = before latest message;
- depth 2 = before second-latest;
- and so on.

For exact parity, use Lumiverse `in_history` and preserve role/depth.

**Do not automatically convert every ST depth-0 In-Chat block to `post_history`.**

A depth-0 message and a post-history block can be close in recency but are not conceptually identical. Use `post_history` only when:

- the source prompt is clearly a “last-mile” instruction rather than a historical injection; and
- Dry Run shows the resulting message sequence matches the desired intent.

Mark that as **NATIVE SEMANTIC ADAPTATION**, not a mechanical copy.

## 10.3 Same-depth order

ST has an explicit order value for prompts sharing role/depth.

Lumiverse’s block order and role/position rules must be tested in Dry Run.

When several source prompts occupy the same in-history depth:

- preserve their relative order explicitly;
- inspect final message order in Dry Run;
- never assume raw array order is sufficient.

## 10.4 Generation triggers

Map by meaning:

- Normal → `normal`
- Continue → `continue`
- Swipe → `swipe`
- Regenerate → `regenerate`
- Impersonate → `impersonate`
- Quiet → `quiet`

Empty trigger list means all routes on both platforms.

### Group-chat caveat

SillyTavern documents that the **Regenerate** trigger is not used in group chats: group regeneration deletes the last group reply and queues messages using the **Normal** generation type according to the selected group reply strategy. Therefore a source block that is `regenerate`-only in solo may not run during group regeneration.

Do not blindly translate the solo trigger and assume identical group behavior. Create explicit group tests and, when necessary, give the Lumiverse port an intentional group route rather than reproducing an accidental gap.

---

# 11. Phase VI — Utility prompt and completion-behavior conversion

Inventory separately from prompt blocks:

- Continue Nudge
- Group Nudge
- New Chat prompt
- New Group Chat prompt
- New Example Chat prompt
- Replace Empty Message / empty-send behavior
- Impersonation prompt
- Continue Postfix
- Continue Prefill
- character names behavior
- assistant prefill / Start Reply With
- use system prompt
- squash/merge system behavior
- inline media
- web search
- function calling
- reasoning request/effort
- prompt post-processing
- custom stopping strings

Use the current Lumiverse export’s `promptBehavior`, completion, reasoning, and connection fields as the target serializer reference.

## 11.1 Do not turn utility behavior into ordinary blocks unless necessary

A Continue Nudge should remain Continue-specific behavior if Lumiverse has a native field for it.

An ordinary block with no trigger would leak it into every request.

## 11.2 Provider capability audit

A source can request settings the target provider ignores.

For each completion feature report:

- supported and preserved;
- supported but moved to connection;
- unsupported by target provider;
- intentionally disabled.

---

# 12. Phase VII — Macro migration: the compatibility pass

This is the most important part of the conversion.

Create a table of **every distinct macro name** and **every occurrence that has side effects**.

For each macro assign:

- source semantics;
- target semantics;
- same/different;
- rewrite;
- test case.

---

# 13. The critical variable-scope difference

## 13.1 SillyTavern

Current ST docs state:

- local variables are saved to the current chat’s metadata;
- they survive later script executions until flushed;
- globals live across the application.

Therefore source `setvar/getvar` may be persistent story state.

## 13.2 Lumiverse

Current Lumiverse docs state:

- `.` / `setvar/getvar` = transient, one evaluation;
- `@` / `setchatvar/getchatvar` = persisted per chat;
- `$` / global variables = cross-chat.

## 13.3 Consequence

**Never mechanically preserve ST `setvar/getvar` or `.foo`.**

Same syntax does not mean same lifetime.

## 13.4 State-lifetime classifier

For every source local variable, classify it:

### A — Scratch variable

Evidence:

- set before every read on every generation;
- used only to compute this assembled prompt;
- random cached only for this request;
- explicitly reset every build.

Lumiverse target: `.` / local.

### B — Cross-turn story state

Evidence:

- read on future turns;
- not initialized every request;
- relationship score;
- quest state;
- turn counter;
- notebook;
- inventory;
- persistent mode;
- “remember this next turn” semantics.

Lumiverse target: `@` / chat-persisted, **or** an explicitly designed serialized ledger/tracker.

### C — Cross-chat preference

Evidence:

- source global variable;
- intended to affect multiple chats.

Lumiverse target: `$` global.

### D — User-configurable preset option

Evidence:

- creator expects a human-facing toggle/slider/choice;
- not dynamic narrative state.

Lumiverse target: Prompt Variable, not a persistent chat variable.

### E — Model-authored structured state

Evidence:

- source asks model to output a ledger each turn;
- regex retains newest ledger/removes old ledgers.

Target options:

- preserve model-authored ledger;
- migrate selected deterministic fields to `@`;
- use external tracker/Memory Cortex;
- split ownership.

Do not maintain the same field in two authoritative systems without reconciliation rules.

---

# 14. State ownership protocol

For every state field write exactly one owner:

| State | Owner |
|---|---|
| temporary roll | local variable |
| user's preset setting | Prompt Variable |
| HP / numerical quest step | chat variable |
| rich model-authored scene ledger | tracker/assistant ledger |
| durable factual memory | Memory Cortex / LTM |
| static lore | World Book |
| UI selection | Regex action chat state |
| extension-owned structured data | extension |

If two components can write the same fact, define precedence.

Example:

```text
SimTracker owns current structured scene state.
Memory owns durable narrative facts.
Preset local vars own only this-generation calculations.
No block independently rewrites tracker fields.
```

---

# 15. ST `{{var::...}}` is context-sensitive

Do not confuse two unrelated ideas.

In STscript closures, `{{var::x}}` can refer to a scoped script variable.

In Lumiverse presets, `{{var::x}}` is primarily a **Prompt Variable** lookup.

Therefore every source `{{var::...}}` must be classified by context. Never assume it is portable because the spelling matches.

---

# 16. Randomness migration — high-risk semantic area

## 16.1 SillyTavern current semantics

ST documents:

- `{{random::a::b::c}}` = random selection and rerolls each use;
- `{{pick::a::b::c}}` = stable random selection, consistent per chat and position;
- `{{roll::1d20}}` = dice.

## 16.2 Lumiverse current semantics

Lumiverse documents:

- `{{random::min::max}}` = random integer range (and can take an item list);
- `{{pick::...}}` = a random option;
- each generation can pick a different option;
- random/generator calls are not cached automatically.

## 16.3 Critical examples

### ST categorical random

Source:

```text
{{random::NEUTRAL::STEADY::DRIVE}}
```

Lumiverse parity:

```text
{{pick::NEUTRAL::STEADY::DRIVE}}
```

### ST `random::1::100`

Do **not** blindly leave this unchanged.

In ST, current docs define `random` as selection: with arguments `1` and `100`, the runtime meaning is selection between those arguments.

In Lumiverse, `random::1::100` is an integer range.

This is an example where identical syntax can radically change behavior.

If the creator *intended* 1–100 but the source actually only selected 1 or 100, mark an **INTENT DECISION**:

- parity edition = reproduce source runtime;
- corrected native edition = implement intended range and document the fix.

## 16.4 ST stable `pick` has no verified blind equivalent

ST `pick` is stable per chat and position.

Lumiverse documents `pick` as random per generation.

Do not invent an existence-test macro to emulate it. The bundled Lumiverse
snapshot establishes chat-persisted `@` variables and conditional blocks, but it
does not establish a `haschatvar` macro or the exact uninitialized-value
semantics needed for a safe initializer. A parity implementation therefore
requires a fresh native example or observed Dry Run/runtime evidence.

When that evidence exists, use a unique persistent key derived from:

- source prompt ID;
- ordinal occurrence.

This approximates ST “per chat and position” stability.

## 16.5 Cache logical draws

If one logical roll is referenced three times, generate once:

```text
{{.weatherRoll = {{roll::1d20}}}}
...
{{.weatherRoll}}
...
{{.weatherRoll}}
```

Never repeat the generator macro and assume the value is reused.

## 16.6 Define Swipe/Regenerate RNG policy

For every random system decide:

- reroll on Swipe?
- reroll on Regenerate?
- preserve candidate-independent state?
- preserve across Continue?
- persist only after selected response?

This is a behavioral design decision and must be tested.

---

# 17. Macro execution-order audit

Lumiverse executes prompt macros with strict state flow: earlier side effects can affect later reads; a later setter cannot retroactively change an earlier getter.

For every target local dependency:

```text
setter index < getter index
```

Check both:

- within a block;
- across blocks.

A local setter in a disabled block does not exist.

A setter in an unselected conditional branch does not execute.

## 17.1 Conditional side effects

Lumiverse resolves only the selected branch of `if`/`switch`.

This is good, but it means an initialization hidden inside a conditional cannot be assumed to run for other branches.

Static validator rule:

> Every active read must have a reachable prior initialization on every control-flow path, or an intentional empty/default behavior.

---

# 18. Literal macro examples are executable

Markdown code fences do not inherently make macro syntax inert.

If an instruction says:

```text
To persist the note, output {{setvar::note::...}}
```

the macro evaluator may execute it before the model sees the instruction.

Options:

1. escape the braces using a platform-supported literal strategy;
2. rewrite the example in plain language;
3. split the tokens so they cannot parse as a macro;
4. use comments if the content is for humans only and should never reach the model.

Audit:

- README blocks;
- debug commands;
- pseudo-code;
- examples;
- “the model should output this macro” instructions.

This is a frequent source of silent corruption.

---

# 19. Unknown and extension macros

Lumiverse deliberately leaves unknown macros as literal `{{name}}` text.

That makes unknown-macro detection easy—and important.

For every non-core macro:

1. search current Lumiverse macro docs;
2. search installed extension docs;
3. verify exact extension identifier if using `hasExtension`;
4. verify exact regex Script ID if using `regexInstalled`;
5. test Dry Run with dependency installed;
6. test Dry Run without dependency if portable operation is expected.

Do not guess an extension ID.

If a dependency is mandatory, place a disabled README/setup block stating it.

---

# 20. Core identity/card macros

Common identity macros often port cleanly, but still test edge cases:

- `{{user}}`
- `{{char}}`
- `{{description}}`
- `{{personality}}`
- `{{scenario}}`
- `{{persona}}`
- group macros
- time/date macros
- recent-message macros

Fixture tests must include:

- empty personality;
- empty scenario;
- narrator character;
- solo;
- group;
- alternate card fields;
- renamed persona;
- multi-character/group mode.

---

# 21. Group and multiplayer conversion

Do not assume `{{char}}` means the same conceptual object in every group mode.

Audit:

- solo;
- focused/swap group;
- merged/ensemble group;
- muted group members;
- group names;
- speaker identity;
- character descriptions/personality in merged contexts;
- Group Nudge behavior;
- regeneration route.

A high-quality Lumiverse-native preset can branch on `groupCardMode` and use group-specific macros instead of treating a group as one character blob.

Do not add this complexity before parity unless the source already supports groups.

---

# 22. Reasoning / chain-of-thought migration

Search for:

- literal `<think>` and `</think>`;
- provider-specific reasoning tokens;
- fake reasoning messages;
- “write reasoning first” instructions;
- ST reasoning prefix/suffix macros;
- regex that strips reasoning;
- connection reasoning settings.

Classify each reasoning wrapper as one of:

## A — provider framing

It exists because the source backend expects a special wrapper.

Target: move to Lumiverse connection/reasoning configuration or `{{reasoningPrefix}}` / `{{reasoningSuffix}}` where appropriate.

## B — deliberately visible/fake reasoning prompt

It is part of the preset’s strategy, not provider framing.

Preserve only if this behavior is intentionally required on the target model.

## C — reasoning cleanup/display transform

Migrate to Lumiverse Reasoning placement/regex target as appropriate.

## 22.1 Never stack wrappers casually

Audit the target for multiple live `reasoningPrefix` / `reasoningSuffix` pairs.

Only one deliberate reasoning envelope should surround a given reasoning payload unless the target provider explicitly requires nesting.

## 22.2 Model-specific placement

Lumiverse Prompt Variable Placement Selectors can route one block differently for different model profiles.

This is useful when, for example:

- one model needs a `user_append` post-history adherence prompt;
- another needs system pre-history;
- another performs best in-history.

Do this only after model tests justify it.

A current native export may demonstrate this pattern; verify the exact placement-binding serialization in the user's target build.

---

# 23. Phase VIII — Convert the selection/toggle architecture

Many ST presets encode UX conventions only in headings:

```text
= PICK ONE POV =
[ ] First Person
[x] Third Person
[ ] Hybrid
```

Lumiverse can make that structural.

## 23.1 Mutually exclusive blocks

Use a Radio group.

Examples:

- POV;
- prose mode;
- reasoning mode;
- narrative drive;
- adult-mode variant;
- agency mode.

Validation:

- no more than one enabled member;
- preserve source default.

## 23.2 Stackable modules

Use a Checkbox group or ordinary independent blocks.

Examples:

- anti-slop modules;
- optional time header;
- combat;
- dialogue coloring;
- tracker support.

## 23.3 Category markers

Use category markers for visual organization only.

Category markers do not send prompt content.

Do not put required initialization macros solely in a category block unless you have verified category content actually executes in the current implementation. Prefer ordinary always-enabled control/setup blocks for runtime initialization.

---

# 24. Phase IX — Prompt Variables

Prompt Variables are a Lumiverse-native UX layer. They should be added **after parity**.

Good candidates:

- target word count;
- dialogue ratio;
- pacing bias;
- POV selection when represented as one block;
- agency mode;
- strictness;
- model adapter mode;
- feature switches;
- optional formatting.

Lumiverse documents seven types:

- Text;
- Text Area;
- Number;
- Slider;
- Dropdown;
- On/Off;
- Multi-select.

## 24.1 Design rules

- variable names: stable, alphanumeric/underscore;
- one semantic control = one canonical variable;
- defaults must reproduce the source default;
- options should contain user-friendly labels;
- saved values must be tested;
- avoid defining the same variable with conflicting defaults in several simultaneously enabled blocks.

## 24.2 Visibility rule

Lumiverse’s Prompt Variables modal only shows variables attached to currently enabled blocks.

Therefore controls that must always be available should live on an always-enabled control block.

## 24.3 Placement Selector

Only a Dropdown on the same block can control that block’s placement.

For every option configure:

- role;
- position;
- depth when needed.

Always provide a safe ordinary placement fallback.

---

# 25. Phase X — Prompt profile conversion

SillyTavern may carry multiple prompt-order state variants.

Lumiverse Preset Profiles can capture:

- preset choice;
- enabled/disabled block state;
- Prompt Variable selections;

and can bind to:

- Default;
- Character;
- Persona;
- Chat.

Use profiles when source variants are contextual configurations rather than fundamentally different preset contents.

Certification must test the **effective profile**, because profile state can override raw block defaults.

---

# 26. Phase XI — Sampler conversion

Never copy only “temperature.”

Inventory all source sampler fields.

Typical conceptual mapping:

| SillyTavern | Lumiverse concept |
|---|---|
| temperature | Temperature |
| top_p | Top P |
| min_p | Min P |
| top_k | Top K |
| frequency_penalty | Frequency Penalty |
| presence_penalty | Presence Penalty |
| repetition_penalty | Repetition Penalty |
| max context | Context Size |
| max response tokens | Max Tokens |
| streaming | Streaming |
| seed | Seed |
| custom stops | Custom Stop Strings |

Use the current native export to determine exact JSON field spelling.

## 26.1 Override discipline

Lumiverse can treat sampler values as preset overrides over connection defaults.

For each source field:

- if the preset explicitly controls it → enable override;
- if the source leaves it “default/none” → prefer leaving Lumiverse override disabled so the connection owns it;
- if target provider does not support it → document that it cannot have effect.

## 26.2 Context size

Do not blindly retain huge context limits if the target model/connection does not support them.

Validate:

- target model context;
- reserved response tokens;
- actual Dry Run token budget.

---

# 27. Phase XII — Regex migration

Regex migration is a behavioral transformation problem, not a find/replace copy.

## 27.1 Inventory every ST script

Capture:

- name;
- pattern;
- replacement;
- trim strings;
- flags;
- scope;
- disabled state;
- run on edit;
- macro substitution mode;
- minimum depth;
- maximum depth;
- Affects targets;
- ephemerality;
- order;
- external callers by name.

## 27.2 SillyTavern source planes

ST Affects can include:

- User Input;
- AI Response;
- Slash Commands;
- World Info;
- Reasoning.

Its ephemerality controls whether transformation:

- modifies stored chat;
- only modifies display;
- only modifies outgoing prompt;
- or affects both ephemeral planes.

## 27.3 Lumiverse model

Lumiverse separates:

### Placement

- User Input;
- AI Output;
- World Info;
- Reasoning;
- Memory.

### Target

- Prompt — what provider sees;
- Response — AI output before database save;
- Display — render-only.

This separation is powerful but requires semantic mapping.

## 27.4 Mapping by intent

### Display-only styling

ST:

- AI Response;
- display ephemerality only.

Lumiverse:

- Placement: AI Output
- Target: Display

### Destructive AI output cleanup

ST:

- AI Response;
- neither ephemeral box.

Lumiverse:

- Placement: AI Output
- Target: Response

Since the transformed value is saved, future prompts naturally inherit the transformed stored content; do not automatically add a Prompt target too.

### Model-only cleanup of historical AI output

ST:

- AI Response;
- Alter Outgoing Prompt.

Lumiverse:

- Placement: AI Output
- Target: Prompt
- preserve depth limits.

### Display + outgoing prompt, stored original

Lumiverse:

- AI Output
- targets Prompt + Display

### World Info preprocessing

Lumiverse:

- World Info placement;
- Prompt target;
- preserve scope/depth semantics as applicable.

### Reasoning

Use Reasoning placement and choose Prompt/Response/Display according to whether the source modifies:

- later model context;
- stored reasoning;
- UI rendering.

### Memory quarantine (version-sensitive)

The canonical uploaded Regex guide lists User Input, AI Output, World Info, and Reasoning placements, but does not list a Memory placement. Some newer or variant Lumiverse builds may expose a separate memory-ingestion plane. Use it only when the user's current build, current official documentation, or a fresh native export proves that capability.

When verified, it can keep:

- trackers;
- HUD XML;
- hidden model state;
- image prompt metadata;
- diagnostic blocks;

out of Long-Term Memory / Memory Cortex embeddings while preserving the visible response. When not verified, report the limitation and use only documented prompt/response/display behavior or another explicitly supported state-ownership strategy.

## 27.5 Slash-command regex

If source functionality depends on ST’s Slash Commands/STscript plane, there may be no direct one-field regex mapping.

Replace with:

- Lumiverse Quick Replies;
- associative Regex Actions;
- Spindle extension logic;
- another explicit workflow.

Do not silently drop it.

---

# 28. Regex syntax audit

Both ecosystems rely on JavaScript-style regex behavior, but export formatting can differ.

For each script:

1. separate pattern from flags;
2. confirm the target expects flags in its own field;
3. compile with JavaScript `new RegExp(pattern, flags)`;
4. run positive fixtures;
5. run negative fixtures;
6. run multiline fixtures;
7. run nested-HTML/XML fixtures;
8. test message depth;
9. test Continue;
10. test Edit if `run_on_edit`.

## 28.1 Replacement token audit

ST supports capture groups `$1`, `$2`, etc.

ST also documents extension-specific `{{match}}` for full match.

Do not assume `{{match}}` is a Lumiverse replacement token. Convert full-match intent to the target’s documented JavaScript replacement form such as `$&` when appropriate.

## 28.2 Greediness and nested HTML

Patterns like:

```regex
<details>[\s\S]*?</details>
```

can fail on nested `<details>`.

Test representative nested output rather than accepting compilation as proof of correctness.

---

# 29. Phase XIII — UI, HTML, CSS, and interactive output

Classify every generated UI surface:

- narrative HTML;
- tracker;
- Scene Card;
- phone UI;
- map;
- CYOA;
- status bar;
- tooltips;
- hidden metadata.

## 29.1 Preserve three separate truths

1. **stored text**
2. **model-visible text**
3. **display-rendered text**

A pretty Display regex should not automatically alter the model’s continuity data.

A hidden machine-state block may need:

- stored original;
- prompt-visible newest snapshot;
- old snapshots stripped from Prompt;
- Memory stripped;
- Display transformed.

Design each plane explicitly.

## 29.2 Interactive replacements

Lumiverse Regex Actions can turn display elements into:

- Send actions;
- Append-hidden-prompt actions;
- Effects-only actions;
- multi-select actions;
- persistent chat-state updates;
- forks/drafts.

If an ST preset used JavaScript/Quick Replies to create interactive cards, a Lumiverse-native rewrite may be more reliable using these actions.

Add this only in the Native Edition unless interaction is required for source parity.

---

# 30. Phase XIV — Context-filter audit

Lumiverse applies context filters late in assembly and can strip:

- HTML;
- `<details>`;
- Loom-related tags;

from older messages based on keep depth.

This can break presets that treat old formatted assistant messages as machine state.

For every output-state system ask:

- Does continuity require the latest state only?
- How many generations deep must it remain intact?
- Will `<details>` stripping destroy information the model needs?
- Is a Prompt regex already stripping old snapshots?
- Is a chat variable a better persistence owner?

Test with several turns beyond the configured keep depth.

---

# 31. Phase XV — Memory / Summary / Databank / World Book boundary

Never treat these as interchangeable.

## 31.1 World Book

Static/conditional lore and triggered entries.

If migrating ST World Info separately, preserve:

- primary keys;
- secondary/selective keys;
- logic;
- scan depth;
- probability;
- priority/order;
- depth position;
- groups;
- recursion controls;
- character/persona attachment;
- vectorization;
- budget behavior.

Do not embed an entire lorebook into the Loom preset to “make it work.”

## 31.2 Long-Term Memory / Memory Cortex

Durable recalled narrative facts/state.

Do not have a hidden tracker and memory both inventing the authoritative value of the same field.

## 31.3 Databank

Reference-document retrieval, not story-state persistence.

## 31.4 Summary / Loom Summary

Compressed continuity.

Do not duplicate a summary both automatically and explicitly without checking final Dry Run.

## 31.5 Placement vs enablement

Some Lumiverse retrieval macros can control **placement** of already active retrieval rather than acting as a master on/off switch for the subsystem.

Do not label a Prompt Variable “Enable Memory” unless it truly disables the underlying retrieval subsystem. If the preset merely removes its explicit placement macro and Lumiverse falls back to automatic placement, call it a placement control.

---

# 32. Phase XVI — Model/provider adapters

Source presets frequently contain blocks labeled:

- Claude fix;
- Gemini fix;
- Chinese model leash;
- Mistral format;
- Mimo quant hardening;
- thinking off/on;
- proxy jailbreak.

Never enable all of them globally in the converted default.

For every adapter:

1. identify intended model family;
2. preserve source default;
3. determine if the behavior is still needed on target provider;
4. gate by Prompt Variable or `{{model}}` condition;
5. consider Placement Selector if role/position must differ;
6. create model matrix tests.

Do not infer model training lineage as a platform fact.

---

# 33. Phase XVII — Character-tag triggers

Lumiverse can activate blocks by character tags.

This is useful for source modules that only apply to:

- anthro;
- monster;
- robot;
- vampire;
- alien;
- setting genres.

Native tag triggers are preferable to sending all specialist rules to every character.

However:

- only add them when the source semantics clearly define the trigger;
- do not make up tags;
- test cards with and without tags.

A current native reference may demonstrate this with specialist tag groups, but the converter must verify exact tag-trigger serialization in the user's target build.

---

# 34. Phase XVIII — Swipe and Regenerate routing

Swipes are not just “another normal response” when a preset uses candidate-divergence logic.

Lumiverse provides:

- generation triggers;
- `lastGenerationType`;
- swipe/message identifiers;
- rejected-generation information.

For every source feature decide:

- should it run on Normal?
- Continue?
- Swipe?
- Regenerate?
- Impersonate?
- Quiet?

Typical examples:

- tracker generation: Normal/Swipe/Regenerate, maybe not Continue;
- divergence router: Swipe/Regenerate only;
- new-scene initializer: Normal only;
- Continue nudge: Continue only.

## 34.1 Continuity quarantine

Do not treat rejected/swiped-away candidate-only information as canon.

If the source uses retrieved memory or trackers, ensure candidate-only material cannot become authoritative state merely because it existed in a rejected generation.

---

# 35. Phase XIX — Continue semantics

Continue is a special route.

Audit:

- Continue Nudge;
- Continue Prefill;
- Continue Postfix;
- source regex depth handling;
- terminal trackers;
- end-of-message XML;
- assistant prefill.

If an existing assistant message ends in a terminal tracker and Continue appends prose to that same message, the tracker may no longer be terminal at the complete-message level.

Document platform-level limitations instead of pretending a prompt can move already-stored content.

---

# 36. Phase XX — Native enhancement pass

Only begin after the **Parity Port** passes.

Recommended outputs:

1. `Preset — Lumiverse Parity.json`
2. `Preset — Lumiverse Native.json`

Native enhancements can include:

- category organization;
- radio/checkbox groups;
- Prompt Variables;
- Placement Selectors;
- Preset Profiles;
- model adapters;
- character-tag triggers;
- generation triggers;
- Lumiverse reasoning wrappers;
- Memory/Cortex integration;
- Council/Lumia hooks;
- Loom/Sovereign Hand;
- bundled Regex;
- interactive Regex Actions;
- native swipe divergence;
- UI controls.

Every native enhancement gets a changelog entry.

---

# 37. Static Validation Pass 1 — Source integrity

Run before conversion.

Checklist:

- [ ] source JSON parses;
- [ ] source hashes recorded;
- [ ] every prompt ID unique unless documented;
- [ ] prompt-order references all resolve;
- [ ] all prompt-order variants captured;
- [ ] effective source order reconstructed;
- [ ] enabled states recorded;
- [ ] role/position/depth/order recorded;
- [ ] generation triggers recorded;
- [ ] root sampler values recorded;
- [ ] utility/completion settings recorded;
- [ ] macro inventory complete;
- [ ] setter/getter graph complete;
- [ ] random/pick/roll inventory complete;
- [ ] reasoning wrapper inventory complete;
- [ ] regex inventory complete;
- [ ] extension dependencies complete;

If any required source artifact is absent, mark the conversion’s evidence limit before proceeding.

---

# 38. Static Validation Pass 2 — Target schema

Check:

- [ ] target JSON parses;
- [ ] wrapper matches a current native Lumiverse export;
- [ ] schema/version fields are not guessed;
- [ ] block IDs unique;
- [ ] every group reference resolves;
- [ ] roles valid;
- [ ] positions valid;
- [ ] in-history depth numeric/valid;
- [ ] markers use documented names;
- [ ] each required structural datum injected once;
- [ ] categories do not accidentally become prompt text;
- [ ] radio groups have at most one active option;
- [ ] Prompt Variable names valid;
- [ ] Prompt Variable defaults valid;
- [ ] dropdown selected option exists;
- [ ] placement binding references its own dropdown;
- [ ] placement option IDs exist;
- [ ] generation triggers valid;
- [ ] character tag triggers deliberate;
- [ ] completion behavior copied intentionally;
- [ ] sampler overrides intentional;
- [ ] regex Script IDs unique/stable.

---

# 39. Static Validation Pass 3 — Macro semantics

Build a macro linter.

Fail on:

- [ ] unresolved ST-only macro with no dependency note;
- [ ] ST persistent state left as Lumiverse local;
- [ ] Lumiverse `@` used for scratch-only state without reason;
- [ ] getter before setter for local variable;
- [ ] local initialization only in unreachable branch;
- [ ] repeated generator call where one logical draw is required;
- [ ] source stable `pick` replaced by fresh Lumiverse `pick`;
- [ ] source categorical `random` accidentally converted to numeric range;
- [ ] executable pseudo-macro examples;
- [ ] duplicate reasoning wrappers;
- [ ] Prompt Variable referenced but undefined;
- [ ] Prompt Variable hidden on disabled block when it must be user-configurable;
- [ ] extension macro not guarded/documented;
- [ ] model-specific macro condition using unverified model-name pattern.

Unknown `{{...}}` appearing in the final Dry Run is an error unless intentionally literal.

---

# 40. Static Validation Pass 4 — Regex

For every script:

- [ ] JavaScript compilation succeeds;
- [ ] flags valid;
- [ ] replacement captures valid;
- [ ] full-match token converted correctly;
- [ ] scope correct;
- [ ] placement correct;
- [ ] Prompt/Response/Display target correct;
- [ ] depth correct;
- [ ] run-on-edit correct;
- [ ] macro substitution mode correct;
- [ ] order correct;
- [ ] memory placement considered;
- [ ] positive test passes;
- [ ] negative test passes;
- [ ] multiline test passes;
- [ ] nested-HTML/XML test passes if relevant.

Compilation alone is not enough.

---

# 41. Dry Run validation matrix

Lumiverse Dry Run is the authoritative inspection tool for assembled prompt behavior.

Use a fixture matrix.

## 41.1 Base fixtures

### Fixture A — minimal solo

- character name;
- description;
- empty personality;
- empty scenario;
- persona;
- no World Info;
- short chat.

### Fixture B — fully populated solo

- description;
- personality;
- scenario;
- example messages;
- card System Prompt;
- card Post-History Instructions;
- World Info before and after;
- Author’s Note.

### Fixture C — group

- at least three members;
- distinct personality;
- muted member if supported;
- group nudge.

### Fixture D — long history

- enough turns to trigger context filtering;
- HTML/details/tracker blocks in older messages.

### Fixture E — extension dependencies

- required extensions installed;
- then missing/disabled if graceful degradation is intended.

## 41.2 Generation-route matrix

For each required configuration run:

- [ ] Normal
- [ ] Continue
- [ ] Swipe
- [ ] Regenerate
- [ ] Impersonate
- [ ] Quiet, if used

## 41.3 Model/profile matrix

For every supported model family:

- select correct Prompt Variable/profile;
- verify effective role;
- verify effective position;
- verify reasoning wrapper;
- verify sampler/connection.

## 41.4 Dry Run assertions

Check:

- no unresolved macro braces;
- no duplicate card fields;
- exactly one chat history;
- World Info correct positions;
- post-history blocks actually after history;
- in-history block correct depth;
- roles correct;
- conditional branches correct;
- source default modes preserved;
- variable values resolve;
- local variables do not falsely persist;
- chat variables visible where expected;
- cached random values consistent inside one build;
- stable-random emulation remains stable;
- utility prompts only appear on correct routes;
- no disabled docs enter prompt;
- expected context filters applied;
- final sampler values correct.

---

# 42. Runtime validation matrix

A static Dry Run cannot prove everything.

## 42.1 Persistence test

Use a fresh chat.

- turn 1: establish state;
- turn 2: modify it;
- turn 3: verify it;
- reload page;
- turn 4: verify it.

Test:

- relationship state;
- counters;
- notebook;
- persistent selections;
- tracker state.

## 42.2 Regenerate test

- generate;
- record state/random;
- regenerate;
- inspect whether the state should persist or reroll;
- ensure rejected candidate data is not canonized.

## 42.3 Swipe test

Same as regenerate, plus active swipe selection and return to older swipe.

## 42.4 Continue test

Verify:

- nudge;
- postfix;
- no unwanted tracker duplication;
- regex depth;
- completion starts naturally.

## 42.5 Group test

Verify:

- speaker;
- group nudge;
- group macros;
- no identity merging;
- generation-trigger quirks.

## 42.6 Edit test

If regex `run_on_edit` or stored structured data depends on edits:

- edit assistant response;
- inspect stored text;
- inspect display;
- inspect next prompt.

## 42.7 Memory test

If output contains tracker/UI metadata:

- let memory ingest several messages;
- inspect recalled content;
- verify machine/UI blocks are excluded where intended.

---

# 43. Regression invariants

Turn the source’s core behavior into assertions.

Examples:

```text
INV-01: User agency block is enabled by default.
INV-02: Exactly one POV mode is active.
INV-03: The last-mile contrast gate is after chat history.
INV-04: World Info appears once.
INV-05: Relationship state survives a page reload.
INV-06: One logical d20 is not rerolled when referenced twice.
INV-07: Display renderer does not alter stored narrative.
INV-08: Old tracker snapshots are removed from provider context after depth N.
INV-09: Swipe-only router never runs on normal sends.
INV-10: Missing extension macro never silently becomes model instruction.
```

A one-shot converter should emit an invariant list alongside the JSON.

---

# 44. Performance and context-budget audit

A conversion can be correct and still become unusably slow or expensive.

Measure:

- total enabled static characters;
- estimated static tokens;
- number of active blocks;
- nested macro complexity;
- repeated large modules;
- duplicated card/world data;
- repeated reasoning instructions;
- model-authored ledgers;
- HTML UI token cost;
- regex-stripped vs provider-visible text;
- retrieved memory/WI size.

Flag:

- duplicated system rules;
- giant repeated examples;
- multiple full reasoning protocols;
- optional modules enabled on irrelevant models;
- hidden trackers retained in every historical turn.

Optimization comes **after** semantic parity.

---

# 45. Release gates

Do not release until:

## P0

- [ ] target imports;
- [ ] JSON valid;
- [ ] correct native wrapper/version;
- [ ] prompt order correct;
- [ ] required structural markers correct;
- [ ] no duplicate history/card data;
- [ ] persistent state semantics correct;
- [ ] no unresolved mandatory macros;
- [ ] regex destructive/display/prompt planes correct.

## P1

- [ ] all required generation routes tested;
- [ ] all supported model profiles tested;
- [ ] all external dependencies documented;
- [ ] source stable randomness reproduced;
- [ ] reasoning routing verified;
- [ ] group behavior verified if supported;

## P2

- [ ] Prompt Variables usable;
- [ ] native groups clean;
- [ ] Memory contamination controlled;
- [ ] performance acceptable;
- [ ] changelog complete.

Release verdict:

```text
PASS — Native certified
PASS — Parity certified, native enhancements pending
PASS WITH DEPENDENCIES
BEST-EFFORT — incomplete source packet
FAIL — unresolved P0
```

---

# 46. Full conversion output package

A professional conversion should produce:

1. **Parity preset JSON**
2. **Native-enhanced preset JSON** (if materially different)
3. **Regex bundled/linked inside the actual Loom export** when the current native schema supports it; provide a standalone companion export only when requested or required by the target workflow
4. **Audit report**
5. **Validation report**
6. **Dependency manifest**
7. **Changelog**
8. **Known limitations**
9. **Source-to-target prompt map**
10. **Dry Run test matrix/results**

Do not hand the user only a JSON file and call the migration finished.

---

# 47. Source → target block map template

```markdown
| Src ID | Src Name | Enabled | ST Role | ST Position | Depth | Trigger | Target ID | LV Role | LV Position | LV Marker | Change | Status |
|---|---|---:|---|---|---:|---|---|---|---|---|---|---|
```

Every source prompt must appear exactly once in this manifest as:

- converted;
- intentionally omitted;
- merged;
- externalized.

Nothing disappears silently.

---

# 48. Variable migration manifest template

```markdown
| Variable | ST scope/runtime | Read sites | Write sites | Intended lifetime | LV owner | Rewrite |
|---|---|---|---|---|---|---|
| bond_A_B | local/chat-persistent | ... | ... | cross-turn | @ chatvar | @bond_A_B |
| temp_roll | local/chat-persistent | ... | ... | build-only | . local | .temp_roll |
| theme | global | ... | ... | cross-chat | $ global | $theme |
| prose_mode | manual source toggle | ... | UI | user setting | Prompt Variable | var::prose_mode |
```

---

# 49. Randomness manifest template

```markdown
| Occurrence | Source macro | ST behavior | Target behavior needed | Reroll policy | Cache/persistence |
|---|---|---|---|---|---|
| block17#1 | random::A::B | fresh categorical | fresh categorical | each request | .pick |
| block22#2 | pick::A::B | stable chat+position | stable | never until reset | @mig_pick_22_2 |
| block30#1 | roll::1d20 | fresh dice | one logical roll | each normal turn | .d20 |
```

---

# 50. Regex migration manifest template

```markdown
| Script | ST Affects | ST Ephemeral | ST Depth | LV Placement | LV Target | Memory? | Test |
|---|---|---|---|---|---|---|---|
| UI Render | AI Response | Display | all | AI Output | Display | no | PASS |
| Context Saver | AI Response | Outgoing | min3 | AI Output | Prompt | optional | PASS |
| Cleaner | AI Response | destructive | all | AI Output | Response | optional | PASS |
```

---

# 51. Dependency manifest template

```yaml
preset:
  name:
  source_version:
  target_version:
  target_model:

required:
  regex: []
  extensions: []
  world_books: []
  connections: []
  image_generation: []
  memory: []

optional:
  council: []
  trackers: []
  web_search: []

graceful_degradation:
  supported: true/false
  behavior:
```

---

# 52. “One-shot” conversion algorithm

Use the following algorithm for an automated or AI-assisted converter.

```text
INPUT:
  source Chat Completion artifacts
  current Lumiverse native export skeleton
  target provider/model
  optional runtime fixture

1. CLASSIFY source family.
2. FREEZE source and calculate hashes.
3. PARSE every source artifact.
4. RECONSTRUCT effective ST prompt order.
5. INVENTORY all prompts/settings/macros/variables/RNG/regex/dependencies.
6. BUILD behavior graph.
7. BUILD source-to-target manifest before editing.
8. CLONE current native Lumiverse envelope.
9. MAP structural data.
10. MAP ordinary blocks by semantic placement.
11. MAP generation triggers.
12. MAP utility/completion behavior.
13. CLASSIFY every variable by lifetime.
14. REWRITE persistent ST locals to Lumiverse @ where required.
15. REWRITE ST random/pick semantics.
16. CACHE repeated logical generators.
17. REWRITE/guard extension macros.
18. REWRITE reasoning/provider framing.
19. CONVERT regex by behavior plane.
20. COPY sampler settings as deliberate overrides.
21. PRODUCE PARITY build.
22. STATIC VALIDATE.
23. DRY RUN matrix.
24. RUNTIME state/swipe/continue tests.
25. FIX parity issues.
26. FREEZE parity build + hash.
27. ADD native categories/groups/Prompt Variables/profiles/tag triggers/actions.
28. RE-RUN all validation.
29. EXPORT the native build with bundled/linked regex when supported; export a standalone companion regex only when requested or required.
30. WRITE audit, validation, dependencies, changelog.

OUTPUT only when no unresolved P0 remains.
```

---

# 53. Automated validator specification

A converter should be able to run these machine checks.

## 53.1 JSON

- parser success;
- nonempty blocks;
- unique IDs;
- valid parent/group IDs;
- no circular group structure;
- expected wrapper.

## 53.2 Markers

Allowed set from current docs:

```text
char_description
char_personality
scenario
persona
mes_examples
system_prompt
post_history_instructions
chat_history
world_info_before
world_info_after
category
null
```

Flag unknown markers.

## 53.3 Roles

Allowed current documented roles:

```text
system
user
assistant
user_append
assistant_append
```

## 53.4 Positions

```text
pre_history
post_history
in_history
```

Require depth for `in_history`.

## 53.5 Prompt Variables

Check:

- names;
- types;
- min/max/step;
- defaults;
- option IDs unique;
- selected values valid;
- placement binding points to dropdown on same block;
- each binding option exists.

## 53.6 Macros

Extract parser-like tokens rather than simplistic regex if possible.

Check:

- known core macros;
- intentional extension macros;
- unknown macros;
- variable read/write order;
- lifetime map;
- RNG reuse;
- unmatched scoped tags;
- literal examples.

## 53.7 Source preservation

Compare source IDs against conversion manifest:

```text
converted + merged + intentionally omitted = 100% of source IDs
```

No unexplained loss.

## 53.8 Regex

For every final pattern execute JavaScript compilation.

Run stored fixtures and compare actual replacement output to expected output.

---

# 54. Recommended “strict converter” policy

When the converter is uncertain:

### Do

- preserve source behavior;
- label uncertainty;
- create a disabled compatibility block;
- document dependency;
- test;
- offer a native improvement as separate change.

### Do not

- invent a macro;
- invent a provider;
- invent an extension;
- convert a field based only on its name;
- assume “same syntax = same semantics”;
- rewrite prose while debugging mechanics;
- silently enable more modules;
- silently change sampler values;
- silently alter the user-agency contract.

---

# 55. High-risk patterns library

Immediately flag these during import.

## Pattern A — `setvar/getvar` tracker

Risk: ST persistent → Lumiverse transient.

Action: lifetime analysis.

## Pattern B — `.variable` shorthand

Risk: looks portable, lifetime is not.

Action: lifetime analysis.

## Pattern C — `random::A::B::C`

Risk: categorical semantics differ.

Action: convert to `pick` if fresh categorical choice.

## Pattern D — ST `pick`

Risk: source stable; Lumiverse fresh.

Action: persisted emulation if parity requires stability.

## Pattern E — repeated `roll`

Risk: Lumiverse fresh every call.

Action: cache logical roll.

## Pattern F — macro syntax in debug/example text

Risk: executes before model sees it.

Action: escape/rewrite.

## Pattern G — literal `<think>`

Risk: provider-specific framing / leakage.

Action: classify purpose.

## Pattern H — depth-0 ST prompt

Risk: blindly mapped to pre-history or post-history.

Action: classify Relative vs In-Chat and intent.

## Pattern I — `main` → `system_prompt`

Risk: preset instruction confused with card system field.

Action: separate.

## Pattern J — `jailbreak` → `post_history_instructions`

Risk: preset default confused with character override slot.

Action: separate/test.

## Pattern K — display regex copied as destructive

Risk: stored chat corrupted.

Action: Display target.

## Pattern L — destructive regex copied as Display

Risk: model sees data source intended to be removed.

Action: Response/Prompt target by source intent.

## Pattern M — `<details>` state

Risk: context filter removes state later.

Action: state owner + depth test.

## Pattern N — extension macro

Risk: unknown macro leaks literally.

Action: guard/dependency.


---

# 56. Native reference-export lessons

When the user supplies a current native Lumiverse preset, use it as an implementation reference for modern Lumiverse concepts.

A contemporary export may demonstrate:

- native `lumiverse_preset` wrapper;
- a large `blocks` array;
- `system` and `user` roles;
- `pre_history`, `post_history`, and `in_history`;
- category markers;
- Chat History structural marker;
- Prompt Variables attached to blocks;
- a Placement Selector/binding on a model-type dropdown;
- a Swipe/Regenerate-only block;
- character-tag-triggered specialist blocks;
- prompt behavior for Continue/Group/Impersonation/empty send;
- sampler overrides;
- completion settings;
- regex scripts bundled with the preset;
- rich Display regex rendering.

Use verified fields from the supplied export as examples of what a **native enhancement layer** can look like.

Do not copy its exact outer serialization as a timeless schema; export a fresh target-version preset first.

If a reference is a reconstruction rather than an official creator release, treat it only as a structural serializer example and do not present its content as canonical.

---

# 57. Example: converting a persistent relationship variable

### Source ST

```text
{{setvar::bond_A_B::5}}
...
{{getvar::bond_A_B}}
```

If the source expects that value next turn, the direct Lumiverse copy is wrong.

### Lumiverse persistent equivalent

```text
{{setchatvar::bond_A_B::5}}
...
{{getchatvar::bond_A_B}}
```

or shorthand:

```text
{{@bond_A_B = 5}}
...
{{@bond_A_B}}
```

If the value is initialized every generation and only formats the current prompt, use local instead.

---

# 58. Example: converting ST stable pick

### Source ST

```text
{{pick::red::green::blue}}
```

Source semantics: stable per chat/position.

### Lumiverse parity disposition

Mark `RUNTIME TEST REQUIRED`. Do not serialize an existence-test or initializer
from memory. With a verified native pattern, cache the draw in a unique
chat-persisted `@` variable per occurrence and confirm swipe/regenerate behavior
in Dry Run and runtime.

---

# 59. Example: converting a last-mile block

Source ST:

```text
Role: system
Position: In-Chat
Depth: 0
Trigger: all
```

### Parity build

Use:

```text
role: system
position: in_history
depth: 0
```

### Native adaptation

If the creator’s intent is explicitly “read this after the entire history as a generation-point gate,” test:

```text
role: system
position: post_history
```

Only adopt after comparing Dry Runs and response behavior. Record this as a deliberate adaptation.

---

# 60. Example: converting source “Pick one” modules

Source:

```text
= PICK ONE POV =
Third Person [ON]
First Person [OFF]
Hybrid [OFF]
```

Parity build:

- preserve all three blocks and states.

Native edition:

- create one Radio group;
- Third Person active by default;
- retain all text unchanged.

This improves UX without changing source semantics.

---

# 61. Example: model-dependent CoT placement

If testing shows:

- Chinese SOTA needs late user adherence;
- Gemini needs system pre-history;
- another model needs in-history;

create one Dropdown Prompt Variable and use Lumiverse’s Placement Selector so one block changes role/position/depth without duplicating three nearly identical CoT blocks.

Do not do this based on guesswork. Require test evidence.

---

# 62. Example: source UI state

Suppose AI emits:

```xml
<scenecard>...</scenecard>
```

Desired behavior:

- store XML;
- display a pretty interactive card;
- remove old cards from provider prompt after depth 3;
- exclude from long-term memory.

Lumiverse design:

1. AI Output + Display regex → XML → styled card.
2. AI Output + Prompt regex, min depth 3 → strip old cards.
3. If the current build explicitly supports a memory-ingestion Regex placement, use it to strip the card from memory ingestion; otherwise document the limitation rather than inventing the field.
4. Leave stored XML intact.

This is more precise than a destructive single-plane ST regex.

---

# 63. One-shot conversion completion report template

```markdown
# Conversion Verdict

Source:
Target:
Date:
Source family:
Target model/provider:

## Verdict
PASS / PASS WITH DEPENDENCIES / BEST-EFFORT / FAIL

## Counts
Source prompts:
Target blocks:
Source regex:
Target regex:
Prompt Variables:
External dependencies:

## P0 findings
None / list

## Semantic changes
1.
2.

## Native enhancements
1.
2.

## Known limitations
1.
2.

## Dry Run matrix
Normal:
Continue:
Swipe:
Regenerate:
Impersonate:
Group:

## Persistence tests
Chat variable:
Tracker:
Reload:
Swipe:

## Hashes
Source:
Parity:
Native:
```

---

# 64. Final operator checklist

Use this compact list only after reading the full SOP.

### Acquire

- [ ] source preset
- [ ] regex
- [ ] source provider/model
- [ ] connection profile
- [ ] current Lumiverse native export
- [ ] test card

### Source forensic

- [ ] classify source family
- [ ] hash source
- [ ] reconstruct effective prompt order
- [ ] list roles/positions/depth/triggers
- [ ] inventory samplers/completion
- [ ] inventory macros
- [ ] inventory vars
- [ ] inventory RNG
- [ ] inventory reasoning
- [ ] inventory regex
- [ ] inventory dependencies

### Convert parity

- [ ] clone native envelope
- [ ] map structural slots
- [ ] map ordinary blocks
- [ ] preserve role/placement
- [ ] convert utility prompts
- [ ] classify state lifetime
- [ ] convert persistent vars to @
- [ ] convert random semantics
- [ ] cache rolls
- [ ] convert/guard extension macros
- [ ] convert reasoning
- [ ] convert regex planes
- [ ] map samplers
- [ ] preserve defaults

### Validate parity

- [ ] JSON validation
- [ ] marker validation
- [ ] no duplicate injections
- [ ] no unresolved mandatory macros
- [ ] variable-order validation
- [ ] regex compilation
- [ ] regex behavior fixtures
- [ ] Dry Run fixtures
- [ ] generation-route matrix
- [ ] persistence/reload test
- [ ] swipe/regenerate test
- [ ] Continue test
- [ ] group test
- [ ] memory test

### Native pass

- [ ] categories
- [ ] radio/checkbox groups
- [ ] Prompt Variables
- [ ] Placement Selector
- [ ] Preset Profiles
- [ ] generation triggers
- [ ] character-tag triggers
- [ ] native reasoning wrappers
- [ ] memory/Council/Loom integrations
- [ ] interactive Regex Actions
- [ ] performance cleanup

### Release

- [ ] rerun every test
- [ ] no P0
- [ ] changelog
- [ ] dependency manifest
- [ ] known limitations
- [ ] parity + native hashes
- [ ] final importable files

---

# 65. Definition of done

A SillyTavern → Lumiverse conversion is “done” only when you can answer **yes** to all of these:

1. Can I explain exactly what every source prompt became?
2. Can I reconstruct the final prompt order in both platforms?
3. Are structural/card/world/history fields injected exactly once?
4. Are persistent source variables still persistent?
5. Are scratch variables truly scratch-only?
6. Does every source random construct preserve its intended stability/reroll behavior?
7. Is every model/provider workaround routed only where relevant?
8. Are Continue, Swipe, Regenerate, and Impersonate intentionally handled?
9. Do group chats preserve identity and trigger semantics?
10. Do Regex scripts affect the same conceptual plane?
11. Does stored text differ from displayed/model-visible text only when intentionally designed?
12. Are trackers/UI metadata excluded from memory where appropriate?
13. Are external extensions/macros either working or explicitly listed as dependencies?
14. Does Lumiverse Dry Run show no unexplained literal macros or duplicate data?
15. Does cross-turn runtime state survive reload?
16. Can the preset export and re-import without losing required settings?
17. Have all native enhancements been separated from parity changes in the changelog?
18. Are all P0/P1 findings closed or explicitly accepted?
19. Can another auditor reproduce the result using the report?

If any answer is “no,” the migration is not yet one-shot certified.

---


# 66. Official documentation basis

## Lumiverse

- Presets — Understanding Presets
  https://lumiverse.chat/guides/presets/understanding-presets/

- Presets — Prompt Blocks
  https://lumiverse.chat/guides/presets/prompt-blocks/

- Presets — Prompt Variables
  https://lumiverse.chat/guides/presets/prompt-variables/

- Presets — Sampler Settings
  https://lumiverse.chat/guides/presets/sampler-settings/

- Presets — Preset Profiles
  https://lumiverse.chat/guides/presets/preset-profiles/

- Presets — Macros Reference
  https://lumiverse.chat/guides/presets/macros-reference/

- Presets — Execution Order
  https://lumiverse.chat/guides/presets/execution-order/

- Customization — Regex Scripts
  https://lumiverse.chat/guides/customization/regex-scripts/

## SillyTavern

- Prompt Manager
  https://docs.sillytavern.app/usage/prompts/prompt-manager/

- Macros
  https://docs.sillytavern.app/usage/core-concepts/macros/

- STscript Language Reference
  https://docs.sillytavern.app/usage/st-script/

- Regex
  https://docs.sillytavern.app/extensions/regex/

- Connection Profiles
  https://docs.sillytavern.app/usage/core-concepts/connection-profiles/

---

# 67. Maintenance rule for this SOP

Before using this Chat Completion SOP on a future major Lumiverse or SillyTavern release:

1. re-open both projects’ current Macro docs;
2. re-check variable-scope semantics;
3. re-check RNG semantics;
4. re-check Prompt Block roles/positions/triggers;
5. re-check Regex planes/targets;
6. export one fresh native Lumiverse preset;
7. compare its envelope to the reference used by your converter;
8. update only confirmed differences.

The SOP’s **method** should remain stable even when individual serialization fields change.

---

## End of SOP
