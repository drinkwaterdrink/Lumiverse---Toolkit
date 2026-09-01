# Lumiverse Character Contract

This reference reflects the supplied Lumiverse character documentation. Do not extrapolate undocumented serialization keys from UI field names.

## Base fields

| Field | Purpose | Model relationship |
|---|---|---|
| Name | Chat identity; `{{char}}` resolves to it | Model-facing identity |
| Description | Main always-known definition: appearance, background, traits, relationships, essential facts | Model-facing; highest character-detail priority |
| Personality | Focused trait/behavior summary | Model-facing and inserted separately; avoid Description repetition |
| Scenario | Starting location, situation, and context | Model-facing; avoid general biography duplication |
| First Message | Opening tone, voice, setting, and response opportunity | Becomes the selected opening chat message |
| Example Messages | Voice/tone training examples | Referenced as examples; not historical chat events |
| System Prompt | Direct instructions about how to play/write the character | Model-facing instruction before history |
| Post-History Instructions | Late direct reminder | Injected after chat history before generation |
| Creator Notes | Usage tips, settings, changelog, creator information | Never sent to the model |
| Tags | Character Browser organization/filtering | Organizational metadata |

Only Name is required by the creation UI. A polished authoring package may intentionally leave another field empty, but must say why.

Use `<START>` between independent example conversations:

```text
<START>
{{user}}: Example user line
{{char}}: Example character response
```

Alternate greetings are separate First Messages. Lumiverse asks which greeting to use when starting a new chat.

## Alternate fields

Only these fields have documented alternate variants:

- Description
- Personality
- Scenario

Create variants in the character editor with **Add Variant**. Select them per chat with **Alternate Fields** in the input action bar. Other chats retain their own selections.

During prompt assembly, the selected variant replaces its base field before macro resolution:

- `{{description}}` resolves to the selected Description variant;
- `{{personality}}` resolves to the selected Personality variant;
- `{{scenario}}` resolves to the selected Scenario variant.

Alternate fields live in character extensions data; selections live in chat metadata. Exact internal schema is not supplied. CHARX export includes alternate fields in `lumiverse_modules.json`, but its internal shape is not documented here.

## Alternate avatars

Alternate avatars represent outfits, art styles, or story phases. Add them through **Add Alternate Avatar**. In chat, choose one from the character portrait/avatar switcher. Selection is per chat.

Alternate avatars are not expression sprites. They change the selected base portrayal; expressions map mood labels to dynamic portrait images. CHARX export includes alternate avatars in `lumiverse_modules.json`; do not invent that file's schema.

## Expressions

Expressions are labeled mood sprites. Setup methods are ZIP import, Gallery mapping, or manual **Add Expression**. ZIP filenames become labels. Use a coherent small set—often 4–6 is enough—and transparent PNGs when practical.

`expressionDetection` modes:

- **Auto:** a lightweight sidecar call selects an expression after generation;
- **Council:** detection runs as a Council tool when Council is active;
- **Off:** no automatic detection; the default expression remains.

Do not invent trigger syntax or sidecar prompts. In group chats, each character can have its own set and the portrait panel shows the focused character's expression.

## Embedded World Books and modules

On import, a card's embedded lorebook is created as a separate World Book, linked to the character, and activated in that character's chats. The import summary reports its name and entry count. The World Books panel is where it can be viewed and edited.

CHARX can carry expressions, alternate fields, and alternate avatars; Lumiverse imports and attaches those modules automatically and reports what was included. This documentation does not define partial-failure behavior or the `lumiverse_modules.json` schema.

