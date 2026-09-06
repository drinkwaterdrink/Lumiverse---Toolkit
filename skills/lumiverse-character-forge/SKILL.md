---
name: lumiverse-character-forge
description: Use when creating, revising, expanding, converting, or auditing a Lumiverse character card or character authoring package, including greetings, example messages, alternate fields, alternate avatars, expressions, embedded World Books, import/export planning, and preservation checks. Also use when adapting a character card from another platform to Lumiverse. Do not use for a standalone scenario or World Book with no character-card deliverable.
---

# Lumiverse Character Forge

Build playable characters while preserving the source, user agency, and Lumiverse-native behavior.

When a request asks for a narrator world, ensemble scenario, or connected
multi-card package, delegate profile selection and cross-artifact assembly to
`lumiverse-world-forge`; Character Forge remains responsible for card fields and
CHARX packaging.

Use **create then refine** by default: draft a coherent first version from a
sufficient brief, audit it, and invite focused revision. Offer an **Interview**
or **Idea Lab** path when the user asks for discovery help or a choice would
materially change the character; do not force questionnaires on clear requests.

## Shared contracts

Read [Creative Quality Kernel](../../shared/references/creative-quality-kernel.md),
[Agency Contract](../../shared/references/agency-contract.md),
[Source Authority](../../shared/references/source-authority.md), and
[Evidence Model](../../shared/references/evidence-model.md). Use
[Artifact Ownership](../../shared/references/artifact-ownership.md) and the
[Lumiverse Capability Map](../../shared/references/lumiverse-capability-map.md)
when field placement, linked lore, or native feature claims matter.

## Workflow

1. **Classify the operation.** Create, revise, audit, convert, or style-profile. Identify the desired deliverable: field content, authoring package, revised source file, or verified export.
2. **Establish evidence.** Separate approved canon, source fields, technical documentation, provisional proposals, and unresolved choices. If a Project Steward record exists, use its relevant canon subset and stable artifact ID.
3. **Preserve before editing.** For imported cards, inventory the format, unknown keys, extensions, embedded World Book, assets, alternate modules, macros, and current values. Never rebuild a source record from a reduced field list.
4. **Author by field purpose.** Follow [Lumiverse Character Contract](references/lumiverse-character-contract.md) and [Authoring and Audit](references/authoring-and-audit.md). Apply the shared quality kernel; build decisions, behavior, voice, knowledge limits, and lived details rather than adjective lists. Keep Description, Personality, Scenario, examples, and direct instructions functionally distinct.
5. **Add optional modules deliberately.** Alternate fields, alternate avatars, expressions, and a World Book solve different problems. Use only requested or useful modules and preserve their documented selection/activation behavior.
6. **Package to the available evidence.** Default created cards to V3 CHARX using [CHARX Packaging](references/charx-packaging.md) and its bundled helper. For revisions, edit the complete source JSON and retain archive resources. For undocumented modules, report the limitation instead of inventing extension keys. Follow [Conversion and Preservation](references/conversion-and-preservation.md).
7. **Audit the result.** Check field completeness, agency, knowledge boundaries, temporal state, relationship reciprocity, repetition, token cost, macro syntax, module mapping, asset presence, and preservation. Return an artifact passport with checks actually run.

## Invariants

- Treat approved user facts as canon. Mark new creative material `provisional` until approved.
- Reserve `{{user}}` actions, dialogue, thoughts, feelings, attraction, consent, decisions, relationships, abilities, backstory, and next voluntary action for the user.
- Never convert a visual brief or example transcript into unmarked biography or historical canon.
- Keep always-injected identity useful and lean; move reusable setting depth to an attached World Book when appropriate.
- Do not certify importability, losslessness, attachment, or round-trip preservation without evidence.

Use concise chat summaries and place long authoring packages or card files in downloadable artifacts.
