# Lumiverse Toolkit

An installable personal ChatGPT/Codex plugin for creating, revising, auditing, and coordinating Lumiverse roleplay artifacts.

[Installation guide](INSTALL.md) · [Changelog](CHANGELOG.md) · [Verification report](docs/v0.5-verification-report.md)

Current version: `0.5.0+codex.20260906074039`.

## v0.5 bundled skills

- **Lumiverse Project Steward** — shared canon, project records, cross-artifact changes, specialist routing, validation, and release coordination.
- **Lumiverse Character Forge** — source-faithful character creation, revision, conversion, module planning, agency audits, and preservation passports.
- **Lumiverse Scenario Forge** — open scenario seeds, pressure graphs, agency-safe openings, conditional clocks, and modular expansion.
- **Lumiverse World Forge** — narrator worlds, ensemble scenarios, character-plus-world cards, and multi-card shared settings.

Also included in the same installation:

- **Forge Lumiverse Lorebooks** for World Books;
- **Lumiverse Preset Converter** for SillyTavern Chat Completion → Lumiverse Loom migration.

## Try it

- “Start a reusable Lumiverse project for this idea and tell me which artifacts and skills it needs.”
- “Create a rich Lumiverse character card from this brief. Keep new ideas provisional.”
- “Turn this premise into a RICH SANDBOX Lumiverse scenario seed.”
- “Rename this character across my card, World Book, scenario, preset prompts, and tracker references.”
- “Audit this connected Lumiverse project and package a release manifest.”

Self-contained artifact requests route directly to the matching specialist. Project Steward activates when continuity, source conflicts, propagation, staged resumption, or release coordination matters.

Create then refine is the default. Interview and Idea Lab paths are optional for
discovery-heavy work. World packages do not require a dedicated preset, and
native preset creation remains a separate roadmap module.

The Idea Lab can generate and compare genuinely divergent directions or improve
a generic premise without forcing a questionnaire. Source ingestion can organize
wikis, franchise material, excerpts, notes, cards, World Books, and mixed source
sets with provenance, temporal snapshots, spoiler/knowledge partitions,
conflicts, adaptations, and grounded downstream suggestions.

## Safety and evidence boundaries

- User canon outranks generated/external suggestions.
- `{{user}}` agency violations are blockers.
- Unknown schema fields and settings are preserved during revisions.
- Import, runtime, and round-trip claims require actual evidence.
- Generic roleplay presets remain tracker-agnostic unless a tracker is selected.
- Real Frank rules are project/artifact-scoped, never global defaults.

## Verification

V3 CHARX packaging includes embedded-resource checks. See
[CHARX packaging](skills/lumiverse-character-forge/references/charx-packaging.md).
Python 3.10+ runs the validators/exporter; Node.js runs the converter's JavaScript
Regex checker. No personal specialist installation is required. The Preset
Converter covers migration/audit/repair; a native Preset Studio is still planned.

The repository contains baseline and GREEN behavior samples, deterministic validators, fixtures, and result reports under `tests/`. Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The v0.5 verification report records the current deterministic suite. These
checks cover plugin structure, contracts, validators, packaging logic, and
static evidence boundaries—not future artifacts that have not been imported or
exercised in Lumiverse.

World Forge's embedded Character Book compiler targets the observed V3 CHARX
subset. It now blocks silent loss of advanced activation settings unless the
user explicitly accepts reduced fidelity. It does not claim full-fidelity native
World Book serialization without a contemporary native Lumiverse template.

## Roadmap

Next planned: native Preset Studio, followed by Prompt & Regex Laboratory,
Tracker Forge, LumiScript Workshop, and Spindle Extension Forge as separately
routed modules.

## Provenance and licensing

See [source provenance](docs/source-provenance.md). No third-party WorldBuilder code was copied into this repository. No general reuse license is granted yet; all rights remain with the repository owner unless a license is added later.
