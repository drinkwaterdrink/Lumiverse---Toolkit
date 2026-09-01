# Baseline Results: Project Record Contract

Five fresh agents were given only `project-record-contract.prompt.md`, without a Project Steward skill or schema reference.

| Sample | Score | Result | Repeated failures |
|---|---:|---|---|
| 1 | 14/17 | Fail | Invented an unqualified schema; omitted the complete empty-ledger set; introduced unmarked attachment/title defaults. |
| 2 | 14/17 | Fail | Invented an unqualified schema; omitted the complete empty-ledger set; mixed generated organizational defaults with supplied values. |
| 3 | 14/17 | Fail | Invented an unqualified schema and an initial Real Frank version; assumed attachment/title defaults; omitted the complete empty-ledger set. |
| 4 | 14/17 | Fail | Invented an unqualified schema and initial Real Frank version; omitted the complete empty-ledger set. |
| 5 | 14/17 | Fail | Invented an unqualified schema; assumed attachment/title defaults; omitted the complete empty-ledger set. |

## Observed pattern

The agents understood the user's authority, agency, mobile, token, tracker, and Real Frank policies. The failure was **contract consistency**, not general reasoning: every sample created a different record shape, schema label, status vocabulary, edge vocabulary, and collection layout. Several silently selected attachment targets, placeholder titles, or a Real Frank starting version that the user had not supplied.

## Skill requirement derived from RED

Project Steward needs a small authoritative project-record contract and a positive recipe for creating it. The skill should not repeat generic rename, canon, or mobile advice already handled well. It must standardize:

- exact record collections and status vocabularies;
- the distinction between user values, administrative IDs, provisional proposals, and unresolved fields;
- dependency edge types;
- empty ledgers required at project start;
- project-specific policy scoping;
- validation findings and release state.

