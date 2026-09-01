# Authoring and Audit

## Canon layers

Maintain three visible layers:

- **canon:** supplied or explicitly approved facts;
- **provisional:** generated prose, staging, visual direction, branch development, and inferred connections awaiting approval;
- **unresolved:** values that must not be guessed.

Administrative labels and stable IDs may be generated, but label them as administrative. Example-message events demonstrate behavior; they do not establish history. Visual features stay art direction until approved as biography.

## Field recipe

### Description

Include essential identity, appearance when known, background, capabilities and limits, key relationships, knowledge boundaries, behavioral anchors, and facts the model should always know. Prefer observable specifics over adjective piles.

### Personality

Express how traits behave under ordinary conditions, stress, conflict, intimacy, and uncertainty. Do not paste biography or repeat Description sentences.

### Scenario

Define the starting situation, location, immediate pressure, and what remains open. Avoid writing a fixed plot or a voluntary action for `{{user}}`.

### Greetings

Each greeting should demonstrate voice, ground the location, present an actionable opening, and end with space for the user. Alternate greetings should change the situation or pressure—not merely paraphrase the same opening.

Audit every greeting for imposed `{{user}}` movement, dialogue, internal state, attraction, consent, prior bond, ability, history, or next action.

### Examples

Use compact `<START>` blocks to demonstrate voice, boundaries, and behavior across different pressures. User lines are training examples, not events that already occurred.

### Direct instructions

Use System Prompt for durable performance instructions. Use Post-History Instructions only for a short late reminder that benefits from proximity to generation. Do not place lore in either merely to repeat Description.

### Creator Notes and tags

Put usage guidance, source/provisional status, recommended modules/settings, known limitations, and changelog in Creator Notes. These notes are not model-facing. Use a small useful tag set.

## Deeper audits

- **Knowledge:** distinguish narrator knowledge, character knowledge, suspicion, belief, and false belief.
- **Temporal:** record when traits, injuries, outfits, relationships, and alternate states apply.
- **Relationships:** keep each character's perspective independent; intentional asymmetry is valid.
- **Agency:** treat a violation as a blocker.
- **Context cost:** remove repeated biography and move reusable setting detail to a World Book.
- **Macros:** preserve `{{char}}`, `{{user}}`, and documented field macros exactly.
- **Style profile:** when matching a reference, extract voice, rhythm, sensory density, formatting, humor, and boundary patterns; copy no protected prose.

## Output modes

- **QUICK:** essential fields, one greeting, top findings.
- **STANDARD:** complete base fields, requested modules, concise passport.
- **RICH:** complete fields, alternatives, examples, deeper consistency and token audit.
- **AUDIT:** no creative rewrite unless requested; findings, evidence, severity, and suggested fixes.

