# Baseline Results: Rename Propagation

Five fresh agents were given only `rename-propagation.prompt.md` without a Project Steward skill.

| Sample | Score | Result | Main gap |
|---|---:|---|---|
| 1 | 9/10 | Pass | Did not explicitly discuss retaining the old name as a compatibility alias. |
| 2 | 9/10 | Pass | Did not explicitly discuss retaining the old name as a compatibility alias. |
| 3 | 9/10 | Pass | Did not explicitly discuss retaining the old name as a compatibility alias. |
| 4 | 9/10 | Pass | Did not explicitly discuss retaining the old name as a compatibility alias. |
| 5 | 9/10 | Pass | Did not explicitly discuss retaining the old name as a compatibility alias. |

Conclusion: do not add heavy rename-specific instructions. The base model already identifies the blast radius, preserves stable IDs and unknown extension data, avoids false completion claims, and proposes stale-reference validation. Alias retention belongs in a concise change-policy reference, not the skill's core instructions.

