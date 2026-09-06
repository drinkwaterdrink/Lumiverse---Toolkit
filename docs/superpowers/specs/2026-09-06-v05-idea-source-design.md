# Lumi Tools v0.5 — Idea Lab and Source Ingestion

## Goal

Turn vague ideas and supplied fictional sources into strong, traceable,
Lumiverse-native project inputs without adding a monolithic seventh creative
skill or pretending that unverified source claims are canon.

## Approved product behavior

- **Create then refine remains default.** A clear request receives a useful
  first draft. Interview mode is optional and invoked by request or a genuinely
  blocking decision.
- **Preset creation remains separate.** Source ingestion may identify preset
  requirements, but World Forge does not generate a Loom preset implicitly.
- **Adult intimacy remains an optional routed module.** Neither Idea Lab nor
  source ingestion adds intimacy, relationships, or attraction by default.
- Lumiverse documentation and current native exports remain technical authority.
  Third-party projects and foreign formats are inspiration or conversion input.

## Architecture

v0.5 adds shared references and two small machine-readable contracts:

1. `idea-lab-record/v1` records divergent candidates, comparison evidence,
   selected direction, and canon status.
2. `source-ledger/v1` records sources, provenance-bearing facts, temporal and
   spoiler boundaries, conflicts, adaptation choices, entity inventory, and
   proposed downstream entries.

Dependency-free validators enforce structural and epistemic invariants. The
creative skills use the references; Project Steward owns cross-artifact state.
No web scraper is bundled. When browsing or file tools are available, the skill
uses them; otherwise it requests or inventories supplied material and reports
what remains unavailable.

## Idea Lab

### Routes

- `direct`: the brief is clear; draft one direction and refine.
- `variants`: the user asks for ideas or alternatives; generate deliberately
  different candidates.
- `interview`: ask one high-impact question at a time before committing.
- `anti-generic`: preserve the foundation while replacing generic mechanisms.
- `combine`: synthesize several influences through abstract qualities, never
  copied protected expression.

### Candidate contract

Each candidate records:

- stable ID and provisional status;
- concise premise and recognizable foundation;
- meaningful deviation or contradiction;
- scene engine and recurring pressure;
- independent world/NPC motion;
- valid player positions and agency risks;
- discovery/reveal potential;
- likely artifact profile and runtime feasibility;
- divergence dimensions such as scale, institution, relationship topology,
  pressure source, location, timeline, or power distribution.

Variant mode requires at least three candidates and at least two meaningful
divergence dimensions across the set. Candidate comparison uses findings and
trade-offs rather than a decorative numeric score. Selection remains optional;
unselected candidates never become canon.

### Passes

1. Raw divergence.
2. Strange-attractor constraint or contradiction.
3. Roleplay test: scenes, recurring pressure, discoverable truths, replayability.
4. Collision test for renamed duplicates.
5. Convergence recommendation with explicit trade-offs.

## Source ingestion

### Source types

Official source, wiki, fan wiki, user notes, novel/text, transcript, character
card, World Book, structured database/reference, and mixed collection.

### Pipeline

1. Freeze the request, timeframe, spoiler preference, and authority order.
2. Inventory every source with locator or content hash and relevance decision.
3. Extract entities, aliases, locations, factions, rules, events, items,
   institutions, relationships, and terminology.
4. Record each material fact as `CANON`, `USER_CANON`, `PROVISIONAL`,
   `INFERRED`, `CONFLICTED`, or `ADAPTATION_CHOICE`, with supporting source IDs.
5. Apply a temporal snapshot; later facts cannot enter a source-locked artifact.
6. Partition public facts, character-known facts, rumors/beliefs, and GM truth.
7. Record conflicts without silently selecting a winner.
8. Record adaptations separately from source canon.
9. Suggest downstream card fields, scenario facts, World Book entries, or
   Databank documents; suggestions remain provisional until accepted.

### Relevance and duplication

Navigation, disambiguation, empty, inaccessible, duplicated, and unrelated
sources are excluded or marked for review with a reason. Duplicate content hashes
are blocking for a finalized ledger unless one record explicitly aliases the
other. Batch ingestion merges aliases and entity IDs before drafting entries.

### Temporal and spoiler safety

A temporal snapshot may use date, arc, episode, chapter, or a user-defined era.
Every time-sensitive fact records its effective boundary. A fact after the
snapshot is a future-knowledge leak if exported as active canon. Hidden truth is
not injected into a character-facing owner unless that character is listed as a
knower at the snapshot.

## Specialist routing

- Character Forge consumes identity, behavior, voice, relationships, and
  knowledge-limited facts; it may request World Book candidate extraction.
- Scenario Forge consumes timeframe-valid pressures and public/GM partitions.
- Lorebook Forge consumes entry suggestions plus activation and spoiler intent.
- World Forge coordinates a connected project and preserves source artifacts.
- Project Steward owns authority, entity IDs, conflicts, adaptations, and ripple
  effects.
- Preset Converter consumes source material only for migration evidence and is
  not expanded into native preset creation.

## Validation and evidence

Deterministic validators can prove record structure, source references, duplicate
IDs/hashes, unresolved conflicts, temporal exclusion, ownership mismatches, and
complete candidate comparison. They cannot prove a wiki is factually correct,
that a model understood a novel, or that Lumiverse activates an entry correctly.
Those claims remain `UNPROVEN` without appropriate inspection/runtime evidence.

## Deliverables

- Shared Idea Lab and source-ingestion references.
- JSON schemas and dependency-free validators.
- Deterministic fixtures for thin ideation, divergent variants, source conflict,
  temporal leakage, irrelevant/duplicate pages, and source-to-entry suggestions.
- Updated specialist routing, README, changelog, installation guide, provenance,
  and v0.5 verification report.
- Plugin version `0.5.0+codex.<timestamp>`.

## Deferred

- Native preset creation/editing.
- A crawler that bypasses site access controls or robots policies.
- Automatic copyrighted-book redistribution.
- Live Lumiverse activation certification.
- Tracker, LumiScript, Spindle, and visual workbench modules.
