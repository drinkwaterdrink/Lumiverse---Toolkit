# GREEN Results: Project Record Contract

Five fresh agents were given `project-record-contract.prompt.md` and the completed Project Steward skill, without the rubric or previous results.

| Sample | Score | Validator | Result |
|---|---:|---:|---|
| 1 | 17/17 | 0 findings | Pass |
| 2 | 17/17 | 0 findings | Pass |
| 3 | 17/17 | 0 findings | Pass |
| 4 | 17/17 | 0 findings | Pass |
| 5 | 17/17 | 0 findings | Pass |

## Verified behavior

Every run:

- used `lumiverse-toolkit.project/v1` rather than inventing a schema;
- produced valid JSON with all required ledgers;
- created eleven stable planned/deferred artifact records and no nonexistent completed artifacts;
- used the same authority and fact-status vocabularies;
- recorded the complete user-agency contract;
- separated rich detail from lean always-injected context;
- kept the generic Loom preset tracker-agnostic and SimTracker optional;
- scoped Real Frank rules to matching Loom presets and left the starting version unresolved;
- left the World Book attachment unresolved instead of inventing an ownership/dependency edge;
- passed `validate_project_record()` with zero findings.

## Baseline-to-GREEN change

The baseline samples reasoned well but invented five incompatible record contracts and silently filled some unknown values. With the skill, all five samples converged on one reusable contract and represented unknown choices explicitly. The skill therefore addresses the demonstrated gap without adding redundant generic reasoning instructions.
