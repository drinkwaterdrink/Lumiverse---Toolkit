# Lumi Tools v0.5 Idea Lab and Source Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add reusable, validated Idea Lab and provenance-aware source-ingestion workflows to the six-skill Lumiverse Toolkit.

**Architecture:** Two shared v1 records capture creative divergence and source-derived knowledge. Dependency-free Python validators enforce structural, temporal, provenance, relevance, and agency boundaries; existing specialists route to the shared references without duplicating them.

**Tech Stack:** Markdown Codex skills, JSON Schema 2020-12, Python 3.10+ standard library, `unittest`, Codex plugin manifest.

**Spec:** `docs/superpowers/specs/2026-09-06-v05-idea-source-design.md`

## Global Constraints

- Create then refine remains the default; Interview is optional.
- User/source canon and generated proposals remain distinguishable.
- Preset creation stays separate.
- Adult intimacy remains an optional routed module.
- No bundled scraper bypasses access controls or republishes protected sources.
- No runtime, activation, or factual-certification claim without evidence.
- Existing six skill IDs and public script interfaces remain stable.
- Python remains dependency-free and compatible with 3.10+.

---

### Task 1: Idea Lab record and validator

**Files:**
- Create: `shared/references/idea-lab.md`
- Create: `shared/schemas/idea-lab-record.schema.json`
- Create: `shared/validators/idea_lab.py`
- Create: `tests/fixtures/idea_lab/variants-valid.json`
- Create: `tests/test_idea_lab_contract.py`

**Interfaces:**
- Produces `validate_idea_lab(record) -> list[dict[str, str]]`.
- Uses schema ID `lumiverse-toolkit.idea-lab/v1`.

- [ ] Write failing tests for valid direct/variant records, too few variants,
  duplicate direction signatures, insufficient divergence, selected unknown ID,
  canonized unselected proposals, and agency risk without a blocker.
- [ ] Run the targeted test and confirm RED.
- [ ] Implement the schema, reference, fixture, and minimal validator.
- [ ] Run targeted and full tests.
- [ ] Commit Task 1.

### Task 2: Source ledger and epistemic validator

**Files:**
- Create: `shared/references/source-ingestion.md`
- Create: `shared/schemas/source-ledger.schema.json`
- Create: `shared/validators/source_ledger.py`
- Create: `tests/fixtures/source_ingestion/timeline-valid.json`
- Create: `tests/test_source_ledger_contract.py`

**Interfaces:**
- Produces `validate_source_ledger(record) -> list[dict[str, str]]`.
- Uses schema ID `lumiverse-toolkit.source-ledger/v1`.

- [ ] Write failing tests for valid mixed sources, missing provenance, duplicate
  hashes, excluded page without reason, unresolved conflicts, future-knowledge
  leakage, hidden-truth ownership leakage, adaptation without source distinction,
  dangling entities, and ungrounded entry suggestions.
- [ ] Run the targeted test and confirm RED.
- [ ] Implement the schema, reference, fixture, and minimal validator.
- [ ] Run targeted and full tests.
- [ ] Commit Task 2.

### Task 3: Specialist routing and deterministic workflow fixtures

**Files:**
- Modify: `skills/lumiverse-character-forge/SKILL.md`
- Modify: `skills/lumiverse-scenario-forge/SKILL.md`
- Modify: `skills/forge-lumiverse-lorebooks/SKILL.md`
- Modify: `skills/lumiverse-world-forge/SKILL.md`
- Modify: `skills/lumiverse-project-steward/SKILL.md`
- Modify: `skills/lumiverse-preset-converter/SKILL.md`
- Modify focused specialist references as required.
- Create: `tests/test_v05_skill_routing.py`

**Interfaces:**
- Creative skills link to Idea Lab and source ingestion at their decision points.
- Steward validates both record types for connected projects.

- [ ] Write failing routing/link/behavior-contract tests.
- [ ] Run the targeted test and confirm RED.
- [ ] Update one skill at a time with concise routing and ownership language.
- [ ] Add source-to-card/scenario/book/world mapping and no-scraper boundaries.
- [ ] Validate every skill and run all tests.
- [ ] Commit Task 3.

### Task 4: Release contract, documentation, and publication

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `INSTALL.md`
- Modify: `docs/source-provenance.md`
- Create: `docs/v0.5-verification-report.md`
- Create: `tests/test_v05_release_contract.py`

**Interfaces:**
- Publishes version `0.5.0+codex.<timestamp>` consistently.

- [ ] Write the failing release contract.
- [ ] Update release metadata and docs using the generated cachebuster.
- [ ] Run all tests, strict JSON, compile checks, link checks, skill validation,
  plugin validation, suspicious-macro scans, and clean-tree review.
- [ ] Commit and publish through an authenticated GitHub branch/PR.
