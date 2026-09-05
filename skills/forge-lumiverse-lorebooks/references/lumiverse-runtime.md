# Lumiverse World Book runtime reference

## Contents

1. Authority and scope
2. Activation scopes and entry states
3. Keywords and scan behavior
4. Prompt placement
5. Advanced activation
6. Budgets and vectorization
7. Import, export, and diagnostics
8. Design consequences

## 1. Authority and scope

This reference distills the supplied canonical Lumiverse World Books bundle, especially atomic sources `KB.LUMIVERSE.WORLDBOOKS.097` through `.106`. If the user provides newer Lumiverse documentation or a native export, use it as the more specific source. If a detail is absent, say it is not specified rather than importing SillyTavern behavior.

## 2. Activation scopes and entry states

World Books inject relevant context rather than placing all lore in every prompt. Three scopes are documented:

| Scope | Active when |
|---|---|
| Character World Book | Chats use the attached character |
| Persona World Book | The attached persona is active |
| Global World Book | Every chat |

Multiple books may be active together. Lumiverse deduplicates entries automatically.

Entry states:

- **Active (conditional)**: activates when conditions match.
- **Constant**: always included regardless of keywords.
- **Disabled**: never included.

Comments are private to the user and not sent to the model. Content may use macros such as `{{char}}` and `{{user}}`.

## 3. Keywords and scan behavior

Primary keywords are comma-separated words or phrases; any primary match can activate an ordinary conditional entry. Options:

| Option | Documented default | Effect |
|---|---:|---|
| Case Sensitive | Off | Distinguish capitalization |
| Match Whole Words | Off | Avoid substring matches |
| Use Regex | Off | Treat keywords as regex |

Selective mode combines primary and secondary keywords. Documented modes are AND, OR, NOT, and NOT All. Do not invent native enum values from these labels.

Scan depth behavior:

- `null`/default scans all messages in the chat.
- `1` scans the newest message.
- `5` scans the newest five, and so on.
- For transient information, the docs recommend a shorter scan such as 3–5.

Probability is 0–100% and only applies when **Use Probability** is enabled. Use it for genuinely stochastic behavior, not ordinary canon.

Documented activation order:

1. Collect recent messages up to scan depth.
2. Check primary and, when selective, secondary conditions.
3. Apply probability.
4. Check delay and cooldown.
5. Include constants.
6. Apply groups.
7. Sort by priority.
8. Enforce entry and token budgets.
9. Group by prompt position.

Global defaults: Global Scan Depth unlimited, Max Recursion Passes 3, Max Activated Entries unlimited, Max Token Budget unlimited, and Min Priority 0.

## 4. Prompt placement

| Code | Position | Use |
|---:|---|---|
| 0 | Before Main Prompt | Early context before main prompt material |
| 1 | After Main Prompt | Context after main content and before history |
| 2 | Before Author's Note | Immediately before Author's Note injection |
| 3 | After Author's Note | Immediately after Author's Note injection |
| 4 | At Depth | A chosen number of messages back from the end |
| 5 | Before Example Messages | Before example dialogue |
| 6 | After Example Messages | After example dialogue |

For At Depth:

- depth 0–2: critical next-response influence, active quest, immediate danger
- depth 3–5: nearby relationships or current scene context
- depth 6+: background knowledge that should not dominate

Roles are System, User, or Assistant. System is the documented default and recommendation for most entries. Use User or Assistant only for a deliberate message-like effect.

At the same position/depth, **lower order values come first**. **Priority** is separate: higher-priority entries survive budget enforcement before lower-priority entries.

Source examples recommend Before Main Prompt for a location description, After Main Prompt for world rules, At Depth 2 for an active quest, and At Depth 0 for danger. Treat these as examples, not universal type mappings.

## 5. Advanced activation

- **Sticky N** keeps an entry active for N turns after keywords disappear.
- **Cooldown N** prevents reactivation for N turns after deactivation.
- **Delay N** requires keyword presence for N consecutive turns.
- **Group** makes related entries compete.
- **Group Override** makes the matching override win.
- **Group Weight** changes random selection odds when no override wins.
- **Recursion** lets activated entry content trigger other entries.
- **Prevent Recursion** stops an entry's content from triggering others.
- **Exclude Recursion** removes an entry from recursion source text.
- **Delay Until Recursion** permits activation only on recursion passes.

Recursion can loop; Max Recursion Passes defaults to 3.

## 6. Budgets and vectorization

Budget controls:

- **Max Activated Entries** caps total active entries. Constants count but are never evicted.
- **Max Token Budget** is a rough world-info limit, estimated in the docs as characters divided by four.
- **Min Priority** excludes lower-priority entries; constants are exempt.

Enforcement: collect, sort highest priority first, remove lowest-priority conditional entries for the entry cap, then include in priority order until the token budget is full. Never remove constants.

Vectorized entries activate by semantic similarity and require an embedding provider configured in Settings. Documented statuses: `not_enabled`, `pending`, `indexed`, `error`. Do not promise semantic activation without embeddings.

Sticky, cooldown, and delay state is stored per chat in chat metadata. It persists across sessions, differs per chat, and resets if chat metadata is cleared.

## 7. Import, export, and diagnostics

Lumiverse can import a World Book JSON file, extract an embedded `character_book` from a character card, or bulk migrate SillyTavern books with `bun run migrate:st`. After import, attach the book to Character, Persona, or Global scope.

Export formats documented:

- **Lumiverse**: full fidelity, including advanced settings.
- **Character Book**: standard character-card-compatible format.
- **SillyTavern**: SillyTavern world-info-compatible format.

The supplied documentation does not publish the exact native Lumiverse JSON schema. Do not invent native property names. Prefer a user-supplied harmless native export as a structural template.

Use **Dry Run** to test prompt assembly and **World Book Diagnostics** to inspect active, cooling-down, or delayed entries.

## 8. Design consequences

- Keep entries atomic and dense because every activation costs context.
- Use constants only for information that truly must be present every turn.
- Use whole-word matching for common substring-prone terms.
- Treat short scan depth and sticky as a pair for current-scene lore: narrow retrieval, limited persistence.
- Use groups for mutually exclusive variants, not merely for visual organization.
- Use recursion intentionally and test chains.
- Choose prompt position by runtime influence, not by book tier.
