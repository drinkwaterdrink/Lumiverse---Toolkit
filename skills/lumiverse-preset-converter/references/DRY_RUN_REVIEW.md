# Dry Run Review Protocol

## Principle
Dry Run is evidence of the **assembled request**, not merely the stored preset.

## First pass — immediate failures
Search for:
- unintended literal `{{...}}`;
- duplicate card/persona/scenario/history/world data;
- malformed XML/HTML wrappers;
- duplicated reasoning wrappers;
- mutually exclusive modes both present;
- missing final task-tail blocks;
- route-only blocks on the wrong generation type.

## Structural sentinel fixture
Use unmistakable values:
- `DRYRUN_DESCRIPTION_SENTINEL`
- `DRYRUN_PERSONALITY_SENTINEL`
- `DRYRUN_SCENARIO_SENTINEL`
- `DRYRUN_PERSONA_SENTINEL`
- `DRYRUN_EXAMPLE_SENTINEL`
- `DRYRUN_WI_BEFORE_SENTINEL`
- `DRYRUN_WI_AFTER_SENTINEL`
- previous chat sentinel

Each expected datum should occur once unless duplication is explicitly intended.

## State/RNG
Check:
- one scene-tempo result;
- one value per logical random draw;
- cached values reused consistently;
- no cross-turn state falsely derived from transient local vars;
- newest ledger survives;
- old ledger cleanup begins only at intended depth.

## Reasoning
Check:
- one selected reasoning route;
- no nested/double boundary;
- no instruction to draft sample prose inside a no-draft audit;
- no full-ruleset recital that defeats a compact reasoning leash;
- final prose follows after the boundary.

## Parameters
The Dry Run PARAMETERS block is the runtime truth for that request.
Compare it to the stored Loom sampler overrides and connection settings. Report differences instead of assuming which layer is wrong.

## Result labels
- PASS — directly proven by Dry Run.
- FAIL — directly contradicted by Dry Run.
- UNPROVEN — fixture lacks the necessary source data.
- RUNTIME TEST REQUIRED — cannot be proven without accepting a generation and advancing turns.
