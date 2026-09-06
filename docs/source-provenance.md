# Source Provenance

## Primary technical authority

- User-supplied Lumiverse documentation snapshot in the project source set.
- User-supplied SillyTavern-to-Lumiverse conversion SOP and converter kit for the existing Preset Converter integration.

These sources govern Lumiverse technical behavior. User instructions and approved project material govern creative canon and project policy.

v0.5's source-ingestion workflow records third-party and user-supplied material
by source ID, authority, relevance, temporal boundary, and adaptation status. It
does not bundle scraped source content or treat a source ledger as proof that the
underlying source is accurate.

## Reviewed inspiration

### AndreiNicu/World-Forge

- Source: <https://github.com/AndreiNicu/World-Forge>
- License reported in the reviewed project: MIT
- Code copied: none

Adapted as original Lumiverse Toolkit concepts: staged discovery and
architecture, resumable ledgers, independent audit and compile passes, arc versus
sandbox planning, activation-test thinking, and capability-based handoffs.
SillyTavern schemas, runtime assumptions, field names, and prompt syntax remain
compatibility evidence only and were not promoted to Lumiverse facts.

### PoweringManipulation2/WorldBuilder

- Source: <https://github.com/PoweringManipulation2/WorldBuilder>
- Inspected commit: `37ee589ba09f4f1032cb66fb4e5f05e5a05bc4a2`
- License found at inspected root: none
- Code copied: none

Adapted as original Lumiverse Toolkit concepts:

- tailored versus reusable World Book intent;
- temporal and inventory consistency ledgers;
- resumable batch manifests;
- relationship reciprocity checks with intentional asymmetry;
- artifact ownership boundaries;
- activation-graph and post-generation audit ideas;
- style profiling as a shared mode rather than a standalone generator.

Rejected or replaced:

- SillyTavern-specific schemas and field assumptions;
- forced recursive activation and constant anchors;
- large startup menus that are poor on mobile;
- silent correction or silent attachment/ownership guesses;
- validators whose reported coverage exceeds their implemented checks;
- merge behavior that overwrites duplicate keys after only warning.

The repository is treated as untrusted inspiration. No third-party script was executed or included in this plugin.
