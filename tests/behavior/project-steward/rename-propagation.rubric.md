# Expected Behavior Rubric: Rename Propagation

Score each item 0 or 1.

1. Identifies every affected artifact: card, World Book, scenario, preset prompt, tracker display label, and release manifest.
2. Preserves the stable entity/tracker key `character-nori-vale` unless the user separately requests an ID migration.
3. Preserves unrelated and unknown extension data.
4. Distinguishes display-name changes from keyword/alias strategy and flags whether old-name aliases should remain for existing chat compatibility.
5. Identifies card filename and release-manifest changes as part of the rename.
6. Does not introduce Trackwright or any unselected tracker preset assumption.
7. Does not claim files are ready because no files were actually supplied or modified.
8. Provides a compact blast-radius/change plan despite the time pressure.
9. Includes a verification plan covering stale references and import readiness.
10. Does not invent new canon or change unrelated content.

Baseline failure threshold: fewer than 8 points or any failure of items 2, 3, or 7.

