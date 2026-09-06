# Profiles and routing

| Profile | Use when | Output |
|---|---|---|
| `single_character` | One person in isolation | One CHARX |
| `character_with_world` | A person needs supporting setting depth | One CHARX with embedded book |
| `narrator_world` | The user chats with a world through a narrator | Narrator CHARX with embedded book |
| `ensemble_scenario` | One card runs a household, group, or cast | Ensemble CHARX with embedded book |
| `multi_card_world` | Several independently playable people share a setting | Multiple CHARX files plus shared book |

WorldBuilder-inspired modes are routing aids, not SillyTavern schemas. Ask one
focused question only when the interaction model changes the deliverable.
