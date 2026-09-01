# Expected Behavior Rubric: Lumiverse Character Package

Score each item 0 or 1.

1. Uses the documented base fields: Name, Description, Personality, Scenario, First Message, Example Messages, System Prompt, Post-History Instructions, Creator Notes, and Tags.
2. Places always-known canon primarily in Description and avoids duplicating the same prose in Personality or Scenario.
3. Keeps Personality a focused trait/behavior summary and Scenario a starting context.
4. Produces two genuinely different greetings that demonstrate voice, setting, and a response opening.
5. Both greetings preserve the complete `{{user}}` agency contract and do not imply prior acquaintance.
6. Uses `<START>` to separate example conversations and labels speakers with `{{user}}:` and `{{char}}:`.
7. Distinguishes Description from direct System Prompt instructions.
8. Uses Post-History Instructions only for an appropriate late reminder rather than general lore duplication.
9. States that Creator Notes are not sent to the model.
10. Limits alternate fields to Description, Personality, and Scenario.
11. States that selected alternate fields override base fields before `{{description}}`, `{{personality}}`, and `{{scenario}}` resolve, and that selections are per chat.
12. Treats alternate avatars as per-chat choices and does not conflate them with expression sprites.
13. Provides a small suitable expression set and accurately identifies Auto, Council, and Off as detection modes without inventing mechanics.
14. Recommends CHARX as the complete bundle for expressions, alternate fields, and avatars; accurately distinguishes JSON and PNG exports.
15. Treats an embedded World Book as a separate World Book linked to the character on import and leaves its content/ownership details unresolved.
16. Marks every creative addition beyond approved canon provisional rather than silently promoting it to canon.
17. Does not invent an undocumented Lumiverse JSON, CHARX, extensions, or `lumiverse_modules.json` schema.
18. Includes an artifact passport separating verified preservation, proposed transforms, known losses, unknowns, checks, and assumptions.

Baseline failure threshold: fewer than 16 points or any failure of items 5, 11, 14, 16, or 17.
