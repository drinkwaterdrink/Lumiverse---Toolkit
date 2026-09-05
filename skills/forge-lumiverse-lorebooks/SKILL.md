---
name: forge-lumiverse-lorebooks
description: Create, expand, convert, revise, or audit high-quality Lumiverse World Books/lorebooks from a world idea, roleplay material, reference files, an existing lorebook, or a Weaver world. Use for guided World Forge-style lore development, entry architecture, keyword and selective-logic design, prompt position/depth/role choices, sticky/cooldown/delay/groups/recursion/vectorization planning, activation tests, token-budget audits, stable-UID revisions, and import-ready lorebook packages. Do not use for generic worldbuilding with no Lumiverse target or for character-card/preset work unless it directly supplies lorebook content.
---

# Forge Lumiverse Lorebooks

Build a source-faithful, activation-engineered lorebook package through short mobile-friendly interviews, explicit quality gates, deterministic validation, and resumable project files.

## Start correctly

1. Read `references/lumiverse-runtime.md` before making any Lumiverse claim or field recommendation.
2. Read `references/workflow.md` for a new build, source conversion, Weaver companion build, expansion, or revision.
3. Read `references/authoring.md` before drafting entries.
4. Read `references/audit.md` before approving or revising entries.
5. Read `references/export.md` before promising or creating import files.
6. Treat supplied Lumiverse documentation and a user-supplied Lumiverse export as more authoritative than these bundled references. Preserve conflicts and say which source controls.

Do not import SillyTavern assumptions merely because the inspiration pipeline targets SillyTavern. In particular, use Lumiverse's documented position names/codes and its lower-order-first rule.

## Select the operation

- **New build**: develop an idea into one or more World Books.
- **Source conversion**: extract canon from chats, notes, cards, presets, stories, wikis, or other files without carrying over unsupported assumptions.
- **Weaver companion**: deepen or audit the lore, NPC, or rules books around an existing Weaver world; preserve the thin-narrator-card boundary.
- **Expand**: add lore without silently rewriting hand-edited entries.
- **Revise**: make a scope-locked change and preserve stable entry identities where possible.
- **Audit**: diagnose content quality, activation behavior, runtime position, budgets, and conflicts without modifying the source unless asked.

If the operation is ambiguous, ask one short question with 2–3 choices. On mobile, ask at most three questions at once and normally one. Offer concrete directions when the user has only a vibe, but never replace their taste with an unsolicited house style.

## Maintain resumable project state

Create or continue this artifact set:

```text
[Project]/
├── 00_Project_State.json
├── 01_Lore_Seed.md
├── 02_Master_Lore_Design.md
├── 03_LoreForge_Spec.json
├── 04_Activation_Tests.json
└── Export/
    ├── Manifest.json
    ├── Runtime_Audit.md
    ├── Activation_Test_Report.md
    ├── Import_Guide.md
    └── [BookName].json
```

Copy `assets/project-state.template.json`, `assets/lore-seed.template.md`, `assets/loreforge-spec.template.json`, and `assets/activation-tests.template.json` as starting points. Save a checkpoint after each completed phase. Read the state file before resuming. Never claim a phase is complete until its artifact exists and passes its gate.

## Run the pipeline

### Phase 0 — Discover

Capture the user's raw wording before synthesis. Establish:

- intended play experience and hard boundaries
- target: standalone, existing character/persona, shared global setting, or Weaver world
- activation scope recommendation: Character, Persona, or Global
- build shape: focused book, tiered pack, arc pack, or standing sandbox pack
- canon sources and their authority order
- three to five scenes the lorebook must support

Use `references/workflow.md` for the interview and gate. Do not over-interview details that will not affect entries or activation.

### Phase 1 — Refine

Build `02_Master_Lore_Design.md` as the locked source of truth:

- normalize entities and aliases without erasing user phrasing
- separate permanent world truth, permanent entity/persona truth, and mutable arc/state truth
- assign each fact to exactly one canonical home
- record contradictions, secrets, point-of-view limits, dependencies, and unresolved gaps
- define book boundaries by activation scope and mutability, not by arbitrary size

Stop for material contradictions or missing choices. Do not silently invent canon to close them.
Record the user's creative-authority choice before adding substantive names, rules, history, relationships, or secrets. With `ask_before_new_canon`, pause for approval. With `proposals_only`, keep inventions visibly unapproved and exclude them from export. Only `creative_license` permits consistent new canon without item-by-item confirmation.

### Phase 2 — Architect

Draft `03_LoreForge_Spec.json` using the bundled template. For every entry, author content and runtime metadata together. Require:

- one retrieval concept per entry
- dense, playable content rather than decorative encyclopedia prose
- primary keywords, aliases, and optional secondary logic with false-positive review
- documented state: conditional, constant, or disabled
- documented position, depth when applicable, role, order, priority, budget behavior, timing, grouping, recursion, and vectorization intent
- a short content rationale and activation rationale
- positive, negative, and collision tests

Do not equate lore tier with prompt position. Choose position by the effect required at runtime.

### Phase 3 — Audit and repair loop

Audit read-only first. Write findings to `Export/Runtime_Audit.md`; only then repair the spec if the user asked for a build or fix. Apply `references/audit.md`.

Run:

```bash
python3 scripts/validate_spec.py 03_LoreForge_Spec.json
python3 scripts/simulate_activation.py 03_LoreForge_Spec.json 04_Activation_Tests.json --report Export/Activation_Test_Report.md
```

Re-run until no blocking errors remain. Treat simulator results as deterministic keyword/logic tests, not a substitute for Lumiverse Dry Run, embedding similarity, or live model behavior.

### Phase 4 — Export

Follow `references/export.md`.

- Prefer **native-template mode** when the user supplies one harmless Lumiverse-exported World Book JSON. Preserve its schema, top-level settings, unknown fields, and value types. Do not guess undocumented native keys.
- Otherwise emit a **portable compatibility JSON** plus `Import_Guide.md`. Label it honestly: the provided Lumiverse docs establish JSON import and full-fidelity Lumiverse export, but do not specify the native JSON schema.
- Always retain `03_LoreForge_Spec.json` as the platform-neutral canonical source.

For the portable fallback, run:

```bash
python3 scripts/compile_portable.py 03_LoreForge_Spec.json --out-dir Export/portable
```

Validate every generated JSON with a strict parser. Never put Markdown fences or comments inside JSON.

### Phase 5 — Handoff

Provide:

- the files
- which books attach to Character, Persona, or Global scope
- which books are always active or manually swapped
- recommended World Info budget starting points, clearly labeled as recommendations
- a short Lumiverse verification pass: import, attach, run Dry Run, inspect World Book Diagnostics, then adjust false positives or budget pressure
- any schema or feature limitations that remain

## Protect important boundaries

- Keep rules/governance, deep setting lore, NPC profiles, and mutable scene/arc state separable when the world benefits from those boundaries.
- Use constants sparingly; they are never evicted and can crowd out conditional lore.
- Preserve stable IDs during revision. Replace an entry in place instead of stacking a paraphrase beside it.
- Keep audit and apply separate. An auditor first reports; a writer then changes.
- Keep expansion append-only unless the user explicitly authorizes changes to existing entries.
- Do not claim vectorized activation works until embeddings are configured; do not simulate semantic similarity as exact keyword behavior.
- Do not claim import fidelity for an undocumented schema.

## Attribution

The phase gates, locked master design, tier discipline, audit/apply separation, runtime audit, stable-identity revision, and activation testing are adapted conceptually from AndreiNicu/World-Forge (MIT). This skill rewrites them for Lumiverse's documented World Book behavior and ChatGPT Work rather than copying its SillyTavern-specific contracts.
