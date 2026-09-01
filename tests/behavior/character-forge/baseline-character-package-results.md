# Baseline Results: Lumiverse Character Package

Five fresh agents were given only `lumiverse-character-package.prompt.md`, without a Character Forge skill, the rubric, or the Lumiverse character documentation.

| Sample | Score | Result | Repeated failures |
|---|---:|---|---|
| 1 | 10/18 | Fail | Incomplete base-field set; no exact alternate macro/per-chat behavior; no expression modes; incomplete export distinctions; no documented embedded-book import behavior. |
| 2 | 9/18 | Fail | Same gaps, plus missing `<START>` separators in the actual example blocks. |
| 3 | 10/18 | Fail | Incomplete base-field set and source-backed module/export behavior. |
| 4 | 10/18 | Fail | Incomplete base-field set and source-backed module/export behavior. |
| 5 | 10/18 | Fail | Incomplete base-field set and source-backed module/export behavior. |

## Behavior already strong

The baseline consistently produced vivid, distinct greetings; protected `{{user}}` agency; kept unapproved appearance and incident details provisional; separated Description, Personality, and Scenario reasonably well; avoided inventing serialization; and supplied useful preservation reports.

Character Forge should not bloat those already-strong behaviors with generic prose-writing advice.

## Skill requirement derived from RED

The missing capability is a compact source-backed Lumiverse contract:

- the complete base-field set and which fields are model-facing;
- exact example-message syntax;
- alternate Description/Personality/Scenario override and per-chat selection behavior;
- alternate-avatar versus expression behavior;
- Auto, Council, and Off expression modes;
- JSON, PNG, and CHARX export roles;
- embedded World Book and CHARX-module import behavior;
- a safe boundary between an authoring package and a genuinely import-tested artifact.
