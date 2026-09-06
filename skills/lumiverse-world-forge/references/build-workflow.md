# Build workflow

Guided mode uses a compact blueprint checkpoint. Fast mode accepts the supplied
brief and asks only about decisions that change the output. Full-detail mode
expands every requested entity while still using stable-ID batches.

The build stages are intake, canon inventory, blueprint, specialist authoring,
compile/package, and evidence handoff. Large builds save completed stable IDs so
they can resume without regenerating accepted entries.
