# Lorebook audit and quality gates

## Contents

1. Severity
2. Blocking checks
3. Activation tests
4. Budget and runtime checks
5. Audit report

## 1. Severity

- **Blocking**: import failure, lost canon, contradiction, wrong scope, no activation path, constant bloat, unsafe recursion, missing required state, or undocumented schema claim.
- **High**: frequent false positives/negatives, incorrect position/depth/role, budget eviction risk, mutually exclusive entries co-activating.
- **Medium**: token inefficiency, weak aliases, shallow consequences, order/priority ambiguity, incomplete tests.
- **Note**: polish that does not affect reliability.

Audit read-only first. Separate findings from repairs.

## 2. Blocking checks

### Canon and ownership

- Every fact has one canonical home.
- No permanent book carries mutable state as timeless truth.
- No entry accidentally reveals a secret as shared knowledge.
- Conflicting sources are resolved by authority or represented as POV disagreement.
- Expansion does not overwrite hand-edited material.
- Revision preserves stable identity for unchanged and modified entries.

### Entry structure

- Every entry has a stable ID, title, state, content, rationale, and tests.
- Conditional entries have a viable primary trigger.
- Constant entries justify constant cost.
- Position codes are 0–6 only.
- At Depth entries have a nonnegative depth.
- Non-depth entries do not pretend depth changes placement.
- Role is System/User/Assistant and non-System use is justified.
- Probability is 0–100 and only meaningful when enabled.
- Timing values are nonnegative.
- Group weights are positive when weighted competition is used.

### Runtime logic

- No recursive loop or uncontrolled fan-out.
- Mutually exclusive variants share a tested group.
- Constants cannot consume the expected budget by themselves.
- High-priority safety/current-state entries survive the planned budget.
- Vectorization is conditional on embeddings.

## 3. Activation tests

For every conditional entry, test:

1. canonical-name positive
2. alias positive
3. near-miss negative
4. case and whole-word behavior
5. selective secondary success/failure when used
6. scan-depth boundary when custom
7. group collision
8. recursion chain when enabled

At pack level, test each user-supplied scene. Build an expected active set and an expected inactive set. Flag missing coverage and irrelevant activation.

The bundled simulator supports literal and Python-regex matching, case sensitivity, whole-word behavior, AND/OR/NOT/NOT All secondary logic, disabled/constant state, bounded recursion, and a simplified group/priority/budget pass. Python regex behavior may differ from Lumiverse's runtime. It does not reproduce semantic embeddings, persistent timers, probability rolls, or Lumiverse's complete internal scanner. Confirm those with Dry Run and Diagnostics.

## 4. Budget and runtime checks

Estimate tokens as characters divided by four because that is the Lumiverse documentation's rough estimate. Report:

- total constant characters/tokens
- likely scene activation characters/tokens
- worst tested collision set
- lowest-priority entries evicted by the planned cap/budget
- books whose combined scope may overlap

Check that position follows desired influence. At Depth 0–2 is a strong intervention; background lore there is a hard failure unless justified.

Check order separately from priority: lower order appears first; higher priority survives.

## 5. Audit report

Use this structure:

```markdown
# Runtime Audit

## Status
PASS | PASS WITH NOTES | BLOCKED

## Sources and assumptions

## Blocking findings

## High and medium findings

## Canon ownership

## Activation precision

## Position, depth, and role

## Budget and priority

## Groups, recursion, timing, and vectorization

## Scenario coverage

## Repairs applied

## Remaining live checks
- Import
- Dry Run
- World Book Diagnostics
```
