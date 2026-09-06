# Lumi Tools v0.4 Quality Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a tested v0.4 plugin with shared quality/evidence contracts, safer build and embedding validation, and upgraded specialist routing.

**Architecture:** Shared references remain canonical and concise skill entrypoints route to them. Dependency-free Python validators enforce process and artifact invariants; artifact-specific skills retain their own authoring logic. Existing v0.3 schemas remain readable while new v1 contracts add optional evidence structures.

**Tech Stack:** Markdown Codex skills, JSON Schema 2020-12, Python 3.10+ standard library, `unittest`, Codex plugin manifest.

**Spec:** `docs/superpowers/specs/2026-09-06-v04-quality-foundation-design.md`

## Global Constraints

- Lumiverse documentation and contemporary native exports outrank third-party conventions.
- Preserve all six skill names and existing public script entrypoints.
- Preserve unknown JSON fields and CHARX archive members.
- Simple requests create then refine; Interview and Idea Lab are optional.
- Preset creation remains separate from world packages.
- Adult intimacy design is optional and separately routed.
- No runtime/import/certification claim without matching evidence.
- Use dependency-free Python for shared validators.

---

### Task 1: Shared contracts and references

**Files:**
- Create: `shared/references/lumiverse-capability-map.md`
- Create: `shared/references/creative-quality-kernel.md`
- Create: `shared/references/agency-contract.md`
- Create: `shared/references/source-authority.md`
- Create: `shared/references/artifact-ownership.md`
- Create: `shared/references/evidence-model.md`
- Create: `shared/schemas/capability-receipt.schema.json`
- Create: `shared/validators/capability_receipt.py`
- Test: `tests/test_quality_foundation_contracts.py`

**Interfaces:**
- Produces: `validate_capability_receipt(record) -> list[dict[str, str]]`.
- Produces: shared reference paths consumed by all six skills.

- [ ] Write tests for valid receipts, missing evidence, invalid maturity, unsupported certification, normalized agency terms, and required shared-reference content.
- [ ] Run the new test file and confirm failures are caused by missing files/APIs.
- [ ] Add the six focused references, schema, and minimal validator.
- [ ] Run the new tests and the existing suite.
- [ ] Commit the task.

### Task 2: Build ledger and profile-aware packages

**Files:**
- Create: `shared/schemas/build-ledger.schema.json`
- Create: `shared/validators/build_ledger.py`
- Modify: `shared/validators/project_record.py`
- Modify: `shared/validators/world_package.py`
- Modify: `shared/schemas/project-record.schema.json`
- Modify: `shared/schemas/world-package-manifest.schema.json`
- Test: `tests/test_build_ledger_contract.py`
- Test: `tests/test_project_record_contract.py`
- Test: `tests/test_world_package_contract.py`

**Interfaces:**
- Produces: `validate_build_ledger(ledger, root=None) -> list[dict[str, str]]`.
- Preserves: `validate_project_record` and `validate_world_package` signatures.

- [ ] Write failing tests for artifact/anchor gates, skip reasons, dependency order, normalized agency, single-character requirements, and preset independence.
- [ ] Run targeted tests and confirm expected failures.
- [ ] Implement validators and schemas with precise finding paths.
- [ ] Run targeted and full tests.
- [ ] Commit the task.

### Task 3: Honest activation and embedded-book evidence

**Files:**
- Modify: `skills/forge-lumiverse-lorebooks/scripts/simulate_activation.py`
- Modify: `skills/forge-lumiverse-lorebooks/scripts/compile_character_book.py`
- Modify: `skills/forge-lumiverse-lorebooks/references/export.md`
- Modify: `skills/forge-lumiverse-lorebooks/references/audit.md`
- Test: `tests/test_activation_evidence.py`
- Modify: `tests/test_embedded_character_book.py`

**Interfaces:**
- `compile_character_book(source, book_id, allow_reduced_fidelity=False)` returns `(book, manifest)` and raises `ValueError` on unsafe omissions without opt-in.
- Activation case results expose `status` in `{PASS, FAIL, UNPROVEN}`; CLI exit codes are 0/1/2.

- [ ] Write failing tests for vector uncertainty, probability, weighted groups, sticky/cooldown/delay, and unsafe omitted settings.
- [ ] Run targeted tests and confirm correct RED failures.
- [ ] Implement the minimal status model and reduced-fidelity gate.
- [ ] Update the two references to explain evidence and opt-in behavior.
- [ ] Run targeted and full tests.
- [ ] Commit the task.

### Task 4: Specialist upgrades and dynamic scenarios

**Files:**
- Modify: all six `skills/*/SKILL.md`
- Modify: `skills/lumiverse-scenario-forge/references/modes-and-output.md`
- Modify: `skills/lumiverse-character-forge/references/authoring-and-audit.md`
- Modify: `skills/forge-lumiverse-lorebooks/references/workflow.md`
- Modify: `skills/lumiverse-world-forge/references/build-workflow.md`
- Modify: `skills/lumiverse-project-steward/references/change-validation-release.md`
- Test: `tests/test_skill_quality_routing.py`

**Interfaces:**
- Skills route to shared references with valid relative paths.
- Scenario modes follow the dynamic-section contract from the spec.

- [ ] Write failing contract tests for draft-first behavior, optional interview/Idea Lab, separate preset routing, optional intimacy routing, shared references, and dynamic sections.
- [ ] Run the test and confirm existing rigid guidance fails.
- [ ] Update one skill at a time, validating after each skill edit.
- [ ] Update focused supporting references without duplicating shared content.
- [ ] Run skill validation, link checks, targeted tests, and full tests.
- [ ] Commit the task.

### Task 5: Version, documentation, release evidence, and publication

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `INSTALL.md`
- Create: `docs/v0.4-verification-report.md`
- Modify: `docs/source-provenance.md`
- Test: `tests/test_marketplace_contract.py`
- Create: `tests/test_v04_release_contract.py`

**Interfaces:**
- Publishes plugin version `0.4.0+codex.<timestamp>` consistently across manifest and marketplace.
- Documents exact test counts and unresolved runtime boundaries.

- [ ] Write failing release-contract tests for version consistency, six-skill registration, reference integrity, and required v0.4 documentation.
- [ ] Run the tests and confirm they fail before version/docs changes.
- [ ] Update version, changelog, README, installation guidance, provenance, and verification report.
- [ ] Run all unit tests, strict JSON parsing, relative-link checks, skill validation, plugin validation, suspicious macro/settings searches, and clean-tree review.
- [ ] Commit the verified release candidate.
- [ ] Push the feature branch and merge/publish only with user-authorized integration handling.
