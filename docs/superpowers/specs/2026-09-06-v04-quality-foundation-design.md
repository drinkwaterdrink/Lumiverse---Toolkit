# Lumi Tools v0.4 — Quality Foundation and Honest Evidence

Status: approved for implementation  
Date: 2026-09-06

## Outcome

v0.4 strengthens the six existing specialists through shared creative-quality,
agency, source-authority, capability, ownership, and evidence contracts. It
adds durable process evidence for connected builds, repairs known v0.3
validation weaknesses, and keeps the user experience simple.

Simple requests use **create then refine**: produce a polished draft using
clearly provisional low-risk choices, then revise surgically. Users may request
Interview or Idea Lab mode before drafting. Preset creation stays separate from
character/world packages. Adult intimacy design remains an optional routed
module and is never a default phase.

## Scope

### Included

- Shared references for Lumiverse capability evidence, creative quality,
  agency, source authority, artifact ownership, and evidence maturity.
- A versioned build-ledger schema and deterministic validator for connected or
  large projects.
- Capability receipts on releasable connected packages.
- One normalized agency reservation set across project records.
- Profile-aware package requirements.
- Blocking protection against silently embedding a reduced-fidelity World Book
  when omitted settings materially affect activation.
- Activation simulation that reports uncertainty as `UNPROVEN`, never `PASS`.
- Scenario Forge dynamic sections and the approved draft-first default.
- Character, Lorebook, World, Steward, and Preset specialist routing into the
  shared references without duplicating them.
- Tests, release documentation, version bump, and published-package checks.

### Deferred

- Full Idea Lab and source/wiki ingestion implementation (v0.5).
- Native full-fidelity World Book compiler and activation laboratory (v0.6).
- Full connected-world staged authoring pipeline (v0.7).
- Native Preset Studio and Prompt/Regex Lab (v0.8).
- Trackers, LumiScript, Spindle, and runtime consumers (v0.9+).

## Architecture

### Shared reference layer

Create focused files under `shared/references/`. Specialists link only the
references that change their decisions. The shared files are the canonical
source; skill entrypoints retain concise routing and artifact-specific rules.

### Evidence model

Technical and runtime claims use five maturity levels:

1. `concept`
2. `static_validated`
3. `simulated`
4. `runtime_observed`
5. `certified_for_build`

Every capability receipt names the feature, maturity, evidence source,
dependency, target/build where known, and limitations. `runtime_observed` must
identify whether evidence is user-reported or captured diagnostics.

### Build ledger

Connected/large builds may use `lumiverse-toolkit.build-ledger/v1`. Each phase
records status, expected artifact, sign-off anchor, evidence, and dependencies.
`complete` is valid only when the artifact exists, is nonempty, and contains the
anchor. Optional phases must be explicitly `skipped` with a reason. Simple
self-contained artifacts do not require a ledger.

### Profile-aware packages

- `single_character`: requires CHARX/card source/import guide/passport only.
- `character_with_world`, `narrator_world`, `ensemble_scenario`: additionally
  require LoreForge source, Character Book backup, and compilation manifest.
- `multi_card_world`: requires at least two CHARX files plus shared lore source,
  backup, import guide, and passport; compilation manifests are required for
  each embedded compilation actually present.

Preset files are never required by these profiles.

### Embedded Character Book safety

The observed Character Card V3 subset remains available. Compilation returns an
omission manifest. Packaging must block when omitted non-default settings are
activation-semantic (`selective_logic`, secondary keys, regex, scan depth,
probability, position/depth/role, timing, groups, recursion, vectorization) unless
the caller explicitly chooses reduced fidelity. The override is recorded in the
manifest and artifact passport. Cosmetic/source-only metadata may be omitted
without the override.

### Activation simulation

Each case resolves to `PASS`, `FAIL`, or `UNPROVEN`. Semantic/vector matches,
probability gates, weighted group selection, and persistent timing behavior are
unproven without appropriate runtime evidence. A case with any unresolved
expected result cannot report PASS. CLI exit codes: 0 for all PASS, 1 for any
FAIL, 2 for no FAIL but at least one UNPROVEN.

### Scenario output

Required core is situational, not a rigid six-section template:

- QUICK: CORE, OPENING, EXPANSION NOTES.
- STANDARD: CORE, USER, NPC SEEDS, CONFLICT SEEDS, OPENING, EXPANSION NOTES.
- RICH/SANDBOX: core plus only useful dynamic sections such as world, locations,
  factions, relationships, secrets, clocks, aesthetics, and lorebook flags.
- FRESH START modifies relationship assumptions, not section count.
- Audit-only output need not end with `Seed locked.`; finalized seeds do.

All modes preserve the shared agency contract.

## Error handling

- Unknown or undocumented Lumiverse settings remain unresolved rather than
  serialized.
- Missing ledger artifacts block completion with precise paths.
- Invalid capability maturity, missing evidence, or unsupported certification
  produces a blocker.
- Reduced-fidelity embedding requires an explicit recorded decision.
- Unknown source fields and archive members remain preserved.

## Verification

- Existing 49 tests remain green.
- New tests cover agency normalization, profile-aware artifacts, ledger gates,
  capability receipts, semantic uncertainty, weighted groups, timing state,
  unsafe embedded omissions, dynamic scenario modes, and skill references.
- All six `SKILL.md` files validate and resolve their relative links.
- Plugin manifest and marketplace entry validate.
- Published files match the verified source before release is reported.

## Non-goals

v0.4 does not claim live Lumiverse runtime certification, native serialization
for undocumented modules, semantic similarity simulation, or compatibility
with SillyTavern-only override mechanics.
