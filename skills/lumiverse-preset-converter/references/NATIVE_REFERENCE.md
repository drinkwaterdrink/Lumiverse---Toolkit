# Native Lumiverse Reference Notes

Use a **fresh export from the user's current Lumiverse build** as the serializer reference.

Contemporary native presets can include:
- prompt blocks with role/position/depth/marker/group;
- Prompt Variables attached to blocks;
- radio/checkbox category organization;
- placement binding controlled by a block-local dropdown;
- generation triggers such as Swipe and Regenerate;
- character-tag triggers;
- prompt behavior and completion settings;
- sampler overrides;
- Preset Profiles / saved Prompt Variable selections;
- bundled Regex scripts and Regex Actions.

Do not copy a historical reference export as a timeless schema. Use it to understand patterns, then serialize against the current target build.

Native enhancement comes **after parity**.

## Evidence boundary for Regex placements

The canonical uploaded Regex guide lists these placements: **User Input**, **AI Output**, **World Info**, and **Reasoning**, with **Prompt**, **Response**, and **Display** targets. Some migration notes in the SOP discuss a separate Memory quarantine plane. Treat that capability as **version-sensitive and unverified** unless the user's current Lumiverse build, current official documentation, or a fresh native export demonstrates it. When it is unavailable, report the limitation and use another explicitly supported ownership/filtering strategy; never invent a serialized Memory placement.
