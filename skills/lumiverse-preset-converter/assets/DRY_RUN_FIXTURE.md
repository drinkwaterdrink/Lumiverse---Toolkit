# Lumiverse Dry Run Certification Fixture

Use a temporary chat and a deliberately populated test card.

Description: DRYRUN_DESCRIPTION_SENTINEL
Personality: DRYRUN_PERSONALITY_SENTINEL
Scenario: DRYRUN_SCENARIO_SENTINEL
Persona: DRYRUN_PERSONA_SENTINEL
Example: DRYRUN_EXAMPLE_SENTINEL
World Info Before: DRYRUN_WI_BEFORE_SENTINEL
World Info After: DRYRUN_WI_AFTER_SENTINEL

Add one previous user message:
`DRYRUN_USER_HISTORY_SENTINEL`

Add one previous assistant message:
`DRYRUN_ASSISTANT_HISTORY_SENTINEL`

Run:
1. Normal
2. Continue
3. Regenerate
4. Swipe
5. Impersonate
6. Group mode if supported

For each, save:
- assembled messages;
- final PARAMETERS;
- selected Prompt Variable/profile values;
- unresolved macro search result.
