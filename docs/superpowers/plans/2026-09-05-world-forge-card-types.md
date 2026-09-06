# Lumi Tools v0.3 World Forge and Card Types Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bundled Lumiverse World Forge that creates five distinct card/package profiles, compiles verified embedded Character Books, and packages narrator or ensemble worlds as validated V3 CHARX artifacts.

**Architecture:** World Forge is a coordinating skill, not a second implementation of Character Forge, Scenario Forge, Lorebook Forge, or Project Steward. A small world-build contract selects the output profile and artifact plan; Lorebook Forge remains the canonical source for entry semantics; a conservative compiler maps only the observed Character Book subset; Character Forge's existing packager writes the final archive.

**Tech Stack:** Markdown Codex skills, JSON contracts/templates, Python 3.10+ standard library, `unittest`, Character Card V3 JSON, ZIP/CHARX, existing plugin validator and marketplace packaging.

**Spec:** `docs/superpowers/specs/2026-09-05-world-forge-card-types-design.md`

## Global Constraints

- Target release is `0.3.0`; generate its cachebuster with the plugin-creator helper rather than hand-authoring a timestamp.
- Keep the current plugin ID `lumiverse-toolkit` and marketplace ID `lumiverse-toolkit-marketplace`.
- Keep Python compatibility at 3.10+ and add no third-party runtime dependency.
- Preserve unknown card keys, extensions, assets, and archive members during revisions.
- The five profile IDs are exactly `single_character`, `character_with_world`, `narrator_world`, `ensemble_scenario`, and `multi_card_world`.
- Standard narrator, ensemble, and character-with-world output is Character Card V3 (`chara_card_v3` / `3.0`) with one embedded `data.character_book`.
- User canon outranks generated material; new creative additions remain `provisional` until approved.
- `{{user}}` retains actions, dialogue, thoughts, feelings, attraction, consent, decisions, relationships, abilities, backstory, and next voluntary action.
- Do not invent `lumiverse_modules.json`, native World Book keys, serialized entry IDs, or advanced settings unsupported by the selected target structure.
- Do not force recursion, constant faction anchors, fixed order tiers, vectorization, probability, groups, sticky, cooldown, or delay.
- Label standalone book backups Character Book-compatible unless a current native Lumiverse template was supplied and checked.
- Do not commit the supplied Chained Crown card, its artwork, or its story content.
- Static checks never certify Lumiverse import, attachment, activation, rendering, or model behavior.

---

## File map

### New files

| Path | Responsibility |
|---|---|
| `skills/lumiverse-world-forge/SKILL.md` | Main routing and coordinated build workflow |
| `skills/lumiverse-world-forge/agents/openai.yaml` | Skill display metadata |
| `skills/lumiverse-world-forge/references/profiles-and-routing.md` | Five profiles and ambiguity policy |
| `skills/lumiverse-world-forge/references/narrator-and-ensemble-contract.md` | Field placement and agency boundary |
| `skills/lumiverse-world-forge/references/build-workflow.md` | Intake through packaging stages |
| `skills/lumiverse-world-forge/references/worldbuilder-concepts-review.md` | Adopt/reject record for supplied WorldBuilder ideas |
| `skills/lumiverse-world-forge/references/validation-and-release.md` | Required checks and evidence language |
| `skills/lumiverse-world-forge/assets/world-project.template.json` | Reusable world-build record |
| `skills/lumiverse-world-forge/assets/package-manifest.template.json` | Reusable package evidence manifest |
| `shared/schemas/world-project.schema.json` | Machine-readable world-build contract |
| `shared/schemas/world-package-manifest.schema.json` | Machine-readable package manifest contract |
| `shared/validators/world_project.py` | Dependency-free world-build validation |
| `shared/validators/world_package.py` | Dependency-free output-manifest validation |
| `skills/forge-lumiverse-lorebooks/scripts/compile_character_book.py` | Neutral LoreForge spec to conservative embedded Character Book compiler |
| `tests/test_world_project_contract.py` | Profile and build-contract tests |
| `tests/test_embedded_character_book.py` | Compiler mapping and omission-evidence tests |
| `tests/test_world_package_contract.py` | Profile-specific output-set and hash tests |
| `tests/test_world_forge_acceptance.py` | End-to-end compile/package/preservation test |
| `tests/fixtures/world_forge/narrator-world-valid.json` | Small narrator-world build record |
| `tests/fixtures/world_forge/narrator-loreforge-valid.json` | Small valid LoreForge source |
| `tests/fixtures/world_forge/narrator-card-valid.json` | Synthetic V3 narrator card shell |
| `tests/fixtures/world_forge/multi-card-valid.json` | Multi-card build record |
| `tests/behavior/world-forge/world-profile.prompt.md` | Profile-routing behavior prompt |
| `tests/behavior/world-forge/world-profile.rubric.md` | Profile-routing behavior rubric |
| `docs/v0.3-verification-report.md` | Release evidence and remaining limits |

### Modified files

| Path | Change |
|---|---|
| `skills/lumiverse-project-steward/references/routing-and-handoffs.md` | Route world/card packages to World Forge |
| `skills/lumiverse-project-steward/SKILL.md` | Recognize multi-artifact world builds |
| `skills/lumiverse-character-forge/SKILL.md` | Delegate world-profile selection while retaining card ownership |
| `skills/lumiverse-character-forge/references/charx-packaging.md` | Document compiled embedded-book workflow |
| `skills/lumiverse-scenario-forge/SKILL.md` | Return scenario material as bounded World Forge input |
| `skills/forge-lumiverse-lorebooks/SKILL.md` | Expose embedded Character Book compile mode |
| `skills/forge-lumiverse-lorebooks/references/export.md` | Document conservative mapping and omission manifest |
| `README.md` | Describe six bundled skills and v0.3 profiles |
| `INSTALL.md` | Update installed-skill list and smoke-test prompt |
| `CHANGELOG.md` | Add v0.3 release notes and boundaries |
| `.codex-plugin/plugin.json` | Cachebuster/version and product description |

---

### Task 1: World build contract and profile validation

**Files:**
- Create: `shared/schemas/world-project.schema.json`
- Create: `shared/validators/world_project.py`
- Create: `tests/fixtures/world_forge/narrator-world-valid.json`
- Create: `tests/fixtures/world_forge/multi-card-valid.json`
- Create: `tests/test_world_project_contract.py`

**Interfaces:**
- Consumes: no new code; profile rules come from the approved spec.
- Produces: `validate_world_project(record: Any) -> list[dict[str, str]]`, `PROFILE_OUTPUT_RULES: dict[str, dict[str, int | bool]]`, and schema ID `lumiverse-toolkit.world-project/v1`.

- [ ] **Step 1: Write the failing contract tests**

Create tests that load the validator by file path, load both fixtures, and assert these exact behaviors:

```python
def test_narrator_world_requires_one_card_and_embedded_book(self):
    record = load_fixture("narrator-world-valid.json")
    self.assertEqual(self.validator.validate_world_project(record), [])
    record["artifacts"] = [a for a in record["artifacts"] if a["type"] != "embedded_character_book"]
    codes = {f["code"] for f in self.validator.validate_world_project(record)}
    self.assertIn("profile-output-mismatch", codes)

def test_multi_card_world_requires_two_cards_and_shared_book(self):
    record = load_fixture("multi-card-valid.json")
    self.assertEqual(self.validator.validate_world_project(record), [])
    record["artifacts"] = record["artifacts"][:1]
    codes = {f["code"] for f in self.validator.validate_world_project(record)}
    self.assertIn("profile-output-mismatch", codes)

def test_user_agency_contract_is_blocking(self):
    record = load_fixture("narrator-world-valid.json")
    record["agency"]["reserved"].remove("consent")
    finding = next(f for f in self.validator.validate_world_project(record)
                   if f["code"] == "incomplete-agency-contract")
    self.assertEqual(finding["severity"], "blocker")
```

Also test an unsupported profile, duplicate artifact IDs, a missing `project_id`, invalid status, unknown top-level `extensions` preservation, a contradictory temporal snapshot, and an unreviewed one-sided relationship.

```python
def test_conflicting_temporal_snapshots_fail(self):
    record = load_fixture("narrator-world-valid.json")
    record["temporal"].extend([
        {"id": "time-1", "entity_id": "entity-mara", "era": "opening", "status": "alive", "location": "entity-station"},
        {"id": "time-2", "entity_id": "entity-mara", "era": "opening", "status": "dead", "location": "entity-station"},
    ])
    codes = {f["code"] for f in self.validator.validate_world_project(record)}
    self.assertIn("temporal-conflict", codes)

def test_unreviewed_relationship_asymmetry_warns(self):
    record = load_fixture("narrator-world-valid.json")
    record["relationships"] = [{
        "id": "relation-mara-dispatch",
        "from": "entity-mara", "to": "entity-dispatcher",
        "summary": "Mara trusts the dispatcher.",
        "reciprocal_id": None, "intentional_asymmetry": False,
    }]
    finding = next(f for f in self.validator.validate_world_project(record)
                   if f["code"] == "unreviewed-relationship-asymmetry")
    self.assertEqual(finding["severity"], "minor")
```

- [ ] **Step 2: Run the focused tests and confirm RED**

Run:

```bash
python3 -m unittest tests.test_world_project_contract -v
```

Expected: import/file-not-found failure because `shared/validators/world_project.py` and fixtures do not exist.

- [ ] **Step 3: Add the JSON Schema and two complete fixtures**

Use this required top-level shape in both the schema and fixtures:

```json
{
  "schema": "lumiverse-toolkit.world-project/v1",
  "project_id": "project-saltmere",
  "build": {
    "id": "build-saltmere-world",
    "operation": "create",
    "profile": "narrator_world",
    "mode": "guided",
    "status": "approved"
  },
  "interaction": {
    "primary_identity": "world_narrator",
    "narrator_scope": "environment_and_non_user_characters",
    "user_role": "open"
  },
  "agency": {
    "protected_subject": "{{user}}",
    "reserved": ["actions", "dialogue", "thoughts", "feelings", "attraction", "consent", "decisions", "relationships", "abilities", "backstory", "next_voluntary_action"]
  },
  "entity_ids": ["entity-mara", "entity-dispatcher", "entity-station"],
  "temporal": [],
  "relationships": [],
  "artifacts": [
    {"id": "artifact-card", "type": "character_card", "owner": "lumiverse-character-forge"},
    {"id": "artifact-book", "type": "embedded_character_book", "owner": "forge-lumiverse-lorebooks"}
  ],
  "batches": [],
  "validation": {"status": "not_run", "findings": []},
  "extensions": {}
}
```

The multi-card fixture uses profile `multi_card_world`, at least two `character_card` artifacts, one `shared_character_book` artifact, and no `embedded_character_book` artifact by default.

- [ ] **Step 4: Implement the dependency-free validator**

Implement exact profile rules:

```python
PROFILE_OUTPUT_RULES = {
    "single_character": {"character_card": 1, "embedded_character_book": 0},
    "character_with_world": {"character_card": 1, "embedded_character_book": 1},
    "narrator_world": {"character_card": 1, "embedded_character_book": 1},
    "ensemble_scenario": {"character_card": 1, "embedded_character_book": 1},
    "multi_card_world": {"character_card_min": 2, "shared_character_book": 1},
}

def validate_world_project(record: Any) -> list[dict[str, str]]:
    """Return path-addressed findings; an empty list means the contract passes."""
```

Follow the existing `_finding(code, path, message, severity)` shape. Validate schema ID, required objects, operation in `create|revise|audit|convert`, mode in `guided|fast|full_detail`, status in `draft|approved|building|complete`, profile output counts, unique artifact IDs, string entity IDs, and the full agency reservation set.

Validate `temporal` snapshots by stable ID and referenced entity ID. Two snapshots for the same `entity_id` and `era` with different `status` or `location` produce `temporal-conflict`. Validate `relationships` by stable ID and existing `from`/`to` entity IDs. A claim without `reciprocal_id` produces minor `unreviewed-relationship-asymmetry` unless `intentional_asymmetry` is true; a supplied reciprocal must exist and reverse the endpoints or it produces major `relationship-reciprocal-mismatch`.

- [ ] **Step 5: Run focused and full tests**

Run:

```bash
python3 -m unittest tests.test_world_project_contract -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all new tests pass and the previous 31 tests remain green.

- [ ] **Step 6: Commit Task 1**

```bash
git add shared/schemas/world-project.schema.json shared/validators/world_project.py tests/fixtures/world_forge tests/test_world_project_contract.py
git commit -m "feat: add World Forge project contract"
```

---

### Task 2: Conservative embedded Character Book compiler

**Files:**
- Create: `skills/forge-lumiverse-lorebooks/scripts/compile_character_book.py`
- Create: `tests/fixtures/world_forge/narrator-loreforge-valid.json`
- Create: `tests/test_embedded_character_book.py`
- Modify: `skills/forge-lumiverse-lorebooks/references/export.md`

**Interfaces:**
- Consumes: `validate_spec(data: Any) -> Findings` from `skills/forge-lumiverse-lorebooks/scripts/validate_spec.py` and a `loreforge.lumiverse.v1` source object.
- Produces: `compile_character_book(spec: dict[str, Any], book_id: str) -> tuple[dict[str, Any], dict[str, Any]]`; CLI arguments `spec`, `--book-id`, `--out-book`, and `--out-manifest`.

- [ ] **Step 1: Write failing compiler tests**

Use a synthetic fixture containing one constant governance entry, one ordinary conditional NPC entry, and one conditional location entry with deliberately non-default `sticky: 3`. Test:

```python
book, manifest = compiler.compile_character_book(source, "world")
self.assertEqual(set(book), {"entries"})
self.assertEqual(book["entries"][0], {
    "keys": [],
    "content": "The narrator controls the environment and NPCs, never {{user}}.",
    "constant": True,
    "enabled": True,
    "insertion_order": 0,
})
self.assertEqual(book["entries"][1]["keys"], ["Mara Vale", "Mara"])
self.assertEqual(manifest["stable_id_map"]["world.mara"], 1)
self.assertIn("sticky", manifest["omitted_settings"]["world.location"])
```

Also test: missing book ID fails; invalid LoreForge input fails; stable IDs remain unique; disabled entries become `enabled: false`; non-default advanced settings are listed under their stable ID; default advanced values are not falsely reported as omissions; source order is preserved.

- [ ] **Step 2: Run the compiler tests and confirm RED**

```bash
python3 -m unittest tests.test_embedded_character_book -v
```

Expected: file-not-found failure for `compile_character_book.py`.

- [ ] **Step 3: Implement the pure compiler**

The only serialized entry keys in base mode are:

```python
def compile_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "keys": list(entry["keywords"]),
        "content": entry["content"],
        "constant": entry["state"] == "constant",
        "enabled": entry["state"] != "disabled",
        "insertion_order": entry["order"],
    }
```

Record unsupported non-default settings in the manifest using this baseline:

```python
ADVANCED_DEFAULTS = {
    "secondary_keywords": [], "selective_logic": "or", "case_sensitive": False,
    "match_whole_words": False, "use_regex": False, "scan_depth": None,
    "probability": 100, "use_probability": False, "position": 0,
    "depth": None, "role": "system", "priority": 0, "sticky": 0,
    "cooldown": 0, "delay": 0, "group": None, "group_override": False,
    "group_weight": 100, "prevent_recursion": False,
    "exclude_recursion": False, "delay_until_recursion": False,
    "vectorized": False,
}
```

Treat `priority` as omitted only when it differs from the entry's `order`, because identical priority/order expresses no additional base-mode behavior. The compiler manifest shape is:

```json
{
  "schema": "lumiverse-toolkit.character-book-compilation/v1",
  "source_schema": "loreforge.lumiverse.v1",
  "book_id": "world",
  "book_name": "Station World",
  "target": "character_card_v3_embedded_book_observed_subset",
  "stable_id_map": {"world.governance": 0},
  "omitted_settings": {},
  "native_lumiverse_full_fidelity": false
}
```

Import `validate_spec.py` relative to `__file__` so the CLI works from any current directory. Refuse compilation when the source validator reports errors.

- [ ] **Step 4: Add the CLI and exclusive output behavior**

Write JSON with UTF-8, `ensure_ascii=False`, `indent=2`, and a trailing newline. Refuse to overwrite either output path:

```python
for path in (args.out_book, args.out_manifest):
    if path.exists():
        raise SystemExit(f"ERROR: output already exists: {path}")
```

- [ ] **Step 5: Document what the compiler does not serialize**

Add an “Embedded Character Book mode” section to `references/export.md` naming the five mapped entry keys, the omission manifest, the unique-stable-ID guarantee, and the rule that advanced settings require a verified target template or later compiler support.

- [ ] **Step 6: Run focused and full tests**

```bash
python3 -m unittest tests.test_embedded_character_book -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: compiler tests and all earlier tests pass.

- [ ] **Step 7: Commit Task 2**

```bash
git add skills/forge-lumiverse-lorebooks/scripts/compile_character_book.py skills/forge-lumiverse-lorebooks/references/export.md tests/fixtures/world_forge/narrator-loreforge-valid.json tests/test_embedded_character_book.py
git commit -m "feat: compile embedded Character Books"
```

---

### Task 3: World package manifest and output validation

**Files:**
- Create: `shared/schemas/world-package-manifest.schema.json`
- Create: `shared/validators/world_package.py`
- Create: `skills/lumiverse-world-forge/assets/package-manifest.template.json`
- Create: `tests/test_world_package_contract.py`

**Interfaces:**
- Consumes: profile IDs from Task 1 and compiler-manifest schema from Task 2.
- Produces: `validate_world_package(manifest: Any, root: Path | None = None) -> list[dict[str, str]]` and schema ID `lumiverse-toolkit.world-package/v1`.

- [ ] **Step 1: Write failing package-manifest tests**

Test a complete narrator package with these artifact roles: `charx`, `card_source`, `loreforge_source`, `character_book_backup`, `compilation_manifest`, `import_guide`, and `artifact_passport`.

```python
findings = validator.validate_world_package(valid_manifest(), root=self.root)
self.assertEqual(findings, [])

manifest = valid_manifest()
manifest["artifacts"] = [a for a in manifest["artifacts"] if a["role"] != "charx"]
self.assertIn("missing-required-artifact", {f["code"] for f in validator.validate_world_package(manifest)})
```

Also test duplicate paths, invalid SHA-256, a missing file under `root`, a mismatched computed hash, `native_lumiverse_full_fidelity: true` without `native_template_evidence`, and a multi-card manifest with fewer than two `charx` artifacts.

- [ ] **Step 2: Run the package tests and confirm RED**

```bash
python3 -m unittest tests.test_world_package_contract -v
```

Expected: file-not-found failure for `shared/validators/world_package.py`.

- [ ] **Step 3: Implement schema, validator, and template**

Each artifact record has this exact shape:

```json
{
  "id": "artifact-station-charx",
  "role": "charx",
  "path": "station-world.charx",
  "sha256": "64 lowercase hexadecimal characters",
  "status": "generated",
  "evidence": "static_validation"
}
```

Allow evidence values `static_validation`, `user_reported_import`, `observed_runtime`, and `not_run`. When `root` is supplied, reject absolute paths and `..`, require each file, and compare `hashlib.sha256(path.read_bytes()).hexdigest()` to the manifest.

The template uses empty `artifacts`, `findings`, and `native_template_evidence` arrays and `native_lumiverse_full_fidelity: false`; it must itself validate structurally after the user fills the required project/profile/build IDs and artifacts.

- [ ] **Step 4: Run focused and full tests**

```bash
python3 -m unittest tests.test_world_package_contract -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit Task 3**

```bash
git add shared/schemas/world-package-manifest.schema.json shared/validators/world_package.py skills/lumiverse-world-forge/assets/package-manifest.template.json tests/test_world_package_contract.py
git commit -m "feat: validate World Forge packages"
```

---

### Task 4: World Forge skill and authoring references

**Files:**
- Create: `skills/lumiverse-world-forge/SKILL.md`
- Create: `skills/lumiverse-world-forge/agents/openai.yaml`
- Create: `skills/lumiverse-world-forge/references/profiles-and-routing.md`
- Create: `skills/lumiverse-world-forge/references/narrator-and-ensemble-contract.md`
- Create: `skills/lumiverse-world-forge/references/build-workflow.md`
- Create: `skills/lumiverse-world-forge/references/worldbuilder-concepts-review.md`
- Create: `skills/lumiverse-world-forge/references/validation-and-release.md`
- Create: `skills/lumiverse-world-forge/assets/world-project.template.json`
- Create: `tests/test_world_profiles.py`

**Interfaces:**
- Consumes: `validate_world_project`, `compile_character_book`, `package_charx.py`, `validate_world_package`, and the existing specialist names.
- Produces: installed skill `lumiverse-world-forge` with the five exact profiles and a deterministic reference-loading map.

- [ ] **Step 1: Write failing static skill tests**

Test that `SKILL.md` exists, names all five profiles, links every reference and asset, calls the four existing specialists by exact directory name, and contains the required output/evidence distinction. Test the OpenAI metadata:

```python
self.assertIn('display_name: "Lumiverse World Forge"', agent_text)
self.assertIn('short_description:', agent_text)
```

Test the template by running `validate_world_project` and confirming the only failures are deliberately empty project/build identity fields, never invalid profile or incomplete agency.

- [ ] **Step 2: Run the profile tests and confirm RED**

```bash
python3 -m unittest tests.test_world_profiles -v
```

Expected: failure because the skill directory does not exist.

- [ ] **Step 3: Write `SKILL.md` with the six-stage workflow**

Use this routing skeleton:

```markdown
1. Classify the interaction model and choose one profile from profiles-and-routing.md.
2. Establish source authority, stable IDs, temporal state, and the {{user}} agency contract.
3. Present one compact blueprint checkpoint unless revising an already-approved build.
4. Delegate bounded authoring to Scenario Forge, Character Forge, and Lorebook Forge.
5. Validate the neutral lore spec, compile the embedded Character Book, then package through Character Forge.
6. Validate the package and report static, user-reported, observed, and unperformed checks separately.
```

The description must trigger on narrator cards, world cards, scenario cards, household/cast cards, ensemble cards, embedded-lorebook characters, multi-card worlds, and “a whole scenario instead of one character.” It must not take standalone single-character or standalone lorebook requests away from their direct specialists.

- [ ] **Step 4: Write profile and narrator contracts**

Copy the profile IDs and field-placement table from the approved specification. Include these blocking narrator invariants verbatim in meaning:

- narrator controls environment and non-user characters;
- narrator never supplies the user's thoughts, feelings, dialogue, decisions, consent, abilities, backstory, or next voluntary action;
- NPC autonomy does not become control over the user;
- activated lore is world truth, not automatic NPC knowledge;
- a narrator card does not collapse into one lead character.

- [ ] **Step 5: Write build, WorldBuilder-review, and validation references**

The WorldBuilder review must include the exact adopt/reject table from the specification. The build workflow must define `guided`, `fast`, and `full_detail`, plus stable-ID batch checkpoints. The validation reference must require the seven package artifacts and prohibit import/runtime certification from static checks.

- [ ] **Step 6: Add the complete world-project template and metadata**

Base the template on the valid narrator fixture, but leave identity strings empty and preserve the complete agency reservation list. Set `profile` to `narrator_world`, `mode` to `guided`, and `status` to `draft` as recommended starting values.

- [ ] **Step 7: Run focused and full tests**

```bash
python3 -m unittest tests.test_world_profiles -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all tests pass.

- [ ] **Step 8: Commit Task 4**

```bash
git add skills/lumiverse-world-forge tests/test_world_profiles.py
git commit -m "feat: add Lumiverse World Forge skill"
```

---

### Task 5: Existing-specialist integration and routing

**Files:**
- Modify: `skills/lumiverse-project-steward/SKILL.md`
- Modify: `skills/lumiverse-project-steward/references/routing-and-handoffs.md`
- Modify: `skills/lumiverse-character-forge/SKILL.md`
- Modify: `skills/lumiverse-character-forge/references/charx-packaging.md`
- Modify: `skills/lumiverse-scenario-forge/SKILL.md`
- Modify: `skills/forge-lumiverse-lorebooks/SKILL.md`
- Modify: `tests/test_connected_project_acceptance.py`

**Interfaces:**
- Consumes: World Forge profile/build contract and embedded compiler from Tasks 1–4.
- Produces: unambiguous direct-versus-coordinated routing across all six skills.

- [ ] **Step 1: Add failing routing assertions**

Extend the acceptance test to assert:

```python
self.assertIn("lumiverse-world-forge", routing_text)
self.assertIn("narrator_world", routing_text)
self.assertIn("ensemble_scenario", routing_text)
self.assertIn("compile_character_book.py", charx_reference)
self.assertIn("compile_character_book.py", lorebook_skill)
```

Add negative assertions that Character Forge does not claim standalone World Books and World Forge does not claim Preset Converter, tracker, LumiScript, or Spindle work.

- [ ] **Step 2: Run the acceptance test and confirm RED**

```bash
python3 -m unittest tests.test_connected_project_acceptance -v
```

Expected: failure because current routing does not mention World Forge.

- [ ] **Step 3: Update Project Steward routing**

Add one row:

```markdown
| Narrator world, ensemble scenario, embedded-lorebook card, or multi-card world | World Forge | world-project record, canon subset, agency contract, selected profile, intended outputs |
```

State that a plain character remains direct to Character Forge and a standalone book remains direct to Lorebook Forge. A connected character-plus-book request routes through World Forge, with Steward used only when wider project continuity or release coordination is required.

- [ ] **Step 4: Update the three specialist handoff boundaries**

Character Forge retains final ownership of card fields and `package_charx.py`. Scenario Forge returns CORE/USER/NPC/CONFLICT/OPENING/EXPANSION material without assuming field placement. Lorebook Forge exposes the exact command:

```bash
python3 scripts/compile_character_book.py 03_LoreForge_Spec.json --book-id world --out-book character_book.json --out-manifest character_book.compilation.json
```

Then Character Forge places the compiled object at `data.character_book` before packaging.

- [ ] **Step 5: Run focused and full tests**

```bash
python3 -m unittest tests.test_connected_project_acceptance -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit Task 5**

```bash
git add skills/lumiverse-project-steward skills/lumiverse-character-forge skills/lumiverse-scenario-forge skills/forge-lumiverse-lorebooks tests/test_connected_project_acceptance.py
git commit -m "feat: route connected world packages"
```

---

### Task 6: End-to-end narrator package and preservation acceptance

**Files:**
- Create: `tests/fixtures/world_forge/narrator-card-valid.json`
- Create: `tests/test_world_forge_acceptance.py`
- Modify: `tests/test_charx.py`

**Interfaces:**
- Consumes: `compile_character_book`, Character Forge `package(card, output, source=None, assets_dir=None)`, and both new validators.
- Produces: deterministic evidence that a neutral lore spec becomes an embedded-book CHARX without damaging card content or source archive members.

- [ ] **Step 1: Write the synthetic narrator card**

Use a neutral railway-station world with no copied Chained Crown content. The card must contain all ten authored fields, two alternate greetings, an empty assets list, an empty extensions object, and no embedded book before compilation.

- [ ] **Step 2: Write the failing acceptance test**

The test performs the whole static pipeline:

```python
book, compilation = compiler.compile_character_book(lore_spec, "world")
card["data"]["character_book"] = book
charx.package(card, output)
archive = charx.read_archive(output)
round_trip = json.loads(archive["card.json"])
self.assertEqual(round_trip, card)
self.assertEqual(len(round_trip["data"]["character_book"]["entries"]), 3)
self.assertFalse(compilation["native_lumiverse_full_fidelity"])
```

Add a revision case whose source archive contains `extra.bin`, an unknown root object, and an embedded icon. Patch only `data.scenario`, package with `source=source_charx`, and assert all unknown bytes and JSON properties remain equal.

- [ ] **Step 3: Run the acceptance test and confirm RED if integration gaps remain**

```bash
python3 -m unittest tests.test_world_forge_acceptance -v
```

Expected: RED only for actual compiler/package integration gaps; if prior tasks already satisfy it, record that the integration test starts green and continue without weakening assertions.

- [ ] **Step 4: Add CHARX validation only for evidence-backed invariants**

If required by the test, modify `package_charx.validate` to reject a non-list `character_book.entries` and non-object entries; retain the existing behavior that does not require serialized entry IDs. Do not add advanced entry-field validation.

- [ ] **Step 5: Run all deterministic tests**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all previous and new tests pass with no network access.

- [ ] **Step 6: Commit Task 6**

```bash
git add tests/fixtures/world_forge/narrator-card-valid.json tests/test_world_forge_acceptance.py tests/test_charx.py skills/lumiverse-character-forge/scripts/package_charx.py
git commit -m "test: cover narrator CHARX pipeline"
```

---

### Task 7: World Forge behavior evidence

**Files:**
- Create: `tests/behavior/world-forge/world-profile.prompt.md`
- Create: `tests/behavior/world-forge/world-profile.rubric.md`
- Create: `tests/behavior/world-forge/README.md`

**Interfaces:**
- Consumes: installed World Forge instructions.
- Produces: a repeatable five-sample behavior evaluation contract; results remain evidence files, not unit-test claims.

- [ ] **Step 1: Write the behavior prompt**

Use this exact request:

```text
Create a realistic domestic slice-of-life setup centered on an eccentric adult family,
two neighbors, and {{user}} arriving for a three-day stay. The AI should run the household
and all non-user characters rather than represent one lead character. Everyone is 18+.
Keep relationships and {{user}} reactions open. Recommend the correct Lumi Tools card
profile and give the pre-generation blueprint only; do not generate the final files.
```

- [ ] **Step 2: Write the scoring rubric**

Score seven binary criteria: selects `ensemble_scenario`; identifies narrator scope; reserves complete user agency; proposes an embedded cast/support book; separates established and provisional facts; avoids forced romance/bonds; stops at the requested blueprint. Passing is 7/7 with zero agency blocker.

- [ ] **Step 3: Document sample collection**

The README requires five fresh executions in a new session, verbatim capture, per-criterion scoring, model/preset identification when available, and separation between behavior evidence and deterministic tests. Do not fabricate sample outputs during implementation.

- [ ] **Step 4: Run link and placeholder checks**

```bash
rg -n 'TB''D|TO''DO|FIX''ME|\[TO''DO:' tests/behavior/world-forge skills/lumiverse-world-forge
```

Expected: no matches.

- [ ] **Step 5: Commit Task 7**

```bash
git add tests/behavior/world-forge
git commit -m "test: define World Forge behavior evaluation"
```

---

### Task 8: Documentation, versioning, verification, and publication

**Files:**
- Modify: `README.md`
- Modify: `INSTALL.md`
- Modify: `CHANGELOG.md`
- Modify: `.codex-plugin/plugin.json`
- Create: `docs/v0.3-verification-report.md`
- Modify: `.agents/plugins/marketplace.json` only if the cachebuster helper changes a supported marketplace field; do not hand-edit it.

**Interfaces:**
- Consumes: completed Tasks 1–7 and all test output.
- Produces: installable `0.3.0+codex.<cachebuster>` release, published commit, and explicit laptop update instructions.

- [ ] **Step 1: Update user documentation before versioning**

README must list all six skills and the five profiles. INSTALL must include this smoke-test prompt:

```text
Use Lumiverse World Forge to create a small narrator_world blueprint with one setting,
two NPCs, and two alternate greetings. Stop before generation and report which specialist
will own the card, scenario, lore, and package validation.
```

CHANGELOG must add `v0.3.0 — World Forge and Card Types` with Added, Changed, Evidence, and Boundaries subsections.

- [ ] **Step 2: Run the full test suite and record the exact count**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v | tee /tmp/lumiverse-toolkit-v0.3-tests.txt
```

Expected: exit 0. Copy the actual test count into `docs/v0.3-verification-report.md`; do not predict the count in advance.

- [ ] **Step 3: Run plugin and link validation**

Run the plugin validator from its installed skill root:

```bash
cd /root/.codex/skills/.system/plugin-creator
python3 scripts/validate_plugin.py /workspace/scratch/0377277f6ce7/lumiverse-toolkit
```

Then from the repository root run a short Python link check that resolves every relative Markdown link in `skills/lumiverse-world-forge` and fails on missing targets. Record the exact results in the verification report.

- [ ] **Step 4: Update the plugin cachebuster with the supported helper**

From the same plugin-creator skill root:

```bash
python3 scripts/update_plugin_cachebuster.py /workspace/scratch/0377277f6ce7/lumiverse-toolkit
```

Verify `.codex-plugin/plugin.json` starts with `0.3.0+codex.`. If the helper only bumps the cachebuster without changing the semantic version, set the semantic version to `0.3.0` first with `apply_patch`, then rerun the helper.

- [ ] **Step 5: Re-run verification after version changes**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git status --short
```

Expected: tests pass, diff check is empty, and status lists only intended v0.3 files.

- [ ] **Step 6: Commit the release candidate**

```bash
git add README.md INSTALL.md CHANGELOG.md .codex-plugin/plugin.json .agents/plugins/marketplace.json docs/v0.3-verification-report.md
git commit -m "release: prepare Lumiverse Toolkit v0.3"
```

- [ ] **Step 7: Verify the complete commit before publishing**

```bash
git status --short
git log --oneline --decorate -10
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: clean worktree and passing suite. Compare the repository tree against the v0.3 verification report; correct the report and recommit if any claim lacks command evidence.

- [ ] **Step 8: Publish and verify the remote commit**

```bash
git push origin main
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: push succeeds and local/remote commit IDs match. If authentication or network access blocks publication, stop with the fully committed local release and report the exact blocker; do not claim publication.

- [ ] **Step 9: Prepare the explicit laptop update handoff**

Give the user these instructions with the actual final version substituted from `.codex-plugin/plugin.json`:

```text
1. Open the laptop Codex task used for Lumi Tools maintenance.
2. Run: plugin marketplace upgrade lumiverse-toolkit-marketplace
3. Update/reinstall: lumiverse-toolkit@lumiverse-toolkit-marketplace
4. Start a new Codex session.
5. Verify lumiverse-world-forge appears and report the installed version.
```

Do not request another Mara roleplay test. The first post-release functional check is one small narrator-world generation and one Lumiverse import confirming the embedded World Book name/entry count shown by the import summary.

---

## Completion definition

Implementation is complete only after Tasks 1–8 have passed their stated checks, the repository is clean, and the remote commit matches the verified local release. Successful static packaging is reported separately from the later user-observed Lumiverse narrator-card import.
