# Export contract

## Contents

1. Non-negotiable schema rule
2. Native-template mode
3. Portable compatibility mode
4. Required handoff files
5. Import verification

## 1. Non-negotiable schema rule

The provided Lumiverse documentation names supported import/export workflows and says the Lumiverse export format preserves full fidelity, but it does not publish the exact native JSON schema. Do not invent native property names, enum values, or defaults.

Keep `03_LoreForge_Spec.json` as the canonical platform-neutral artifact. It records documented concepts using readable labels.

## 2. Native-template mode

Use when the user provides a harmless World Book exported directly from their current Lumiverse installation.

1. Parse it strictly.
2. Identify book-level and entry-level shapes from actual data.
3. Preserve unknown keys, value types, and top-level metadata.
4. Create entries by cloning an entry shape when available; if the template has no entry, ask for an export containing one disposable sample entry.
5. Map only fields whose meaning is established by the template/UI or docs.
6. Preserve the user's template as an unchanged source file.
7. Validate strict JSON and compare structural keys with the source template.

Do not assume a SillyTavern field has the same name or enum in native Lumiverse.

## 3. Portable compatibility mode

Use only when no native template exists. The bundled compiler emits a standalone lorebook structure modeled on the audited World-Forge/SillyTavern compatibility shape. Lumiverse documentation establishes SillyTavern import/migration as supported, but direct full-fidelity behavior of every advanced property is not guaranteed by the supplied docs.

The portable file is a convenience artifact, not the source of truth. Include this limitation in `Import_Guide.md` and tell the user to test one book before bulk import.

The portable compiler deliberately omits undocumented Lumiverse-only fields and carries readable source metadata under `extensions.loreforge`. It maps plain selective labels only where the compatibility schema has a known representation. Unsupported combinations remain documented in the extension metadata for manual/native-template application.

The compatibility shape follows SillyTavern's higher-order-first convention, while the canonical LoreForge spec follows Lumiverse's documented lower-order-first convention. The compiler rank-inverts the portable `order` values and retains every original value as `extensions.loreforge.entries[*].lumiverse_order`. Never copy a neutral-spec order value directly into this compatibility field.

## 4. Required handoff files

- `Manifest.json`: books, scope recommendations, build mode, source files, status.
- `Runtime_Audit.md`: findings, repairs, assumptions, limitations.
- `Activation_Test_Report.md`: tested phrases and expected/observed sets.
- `Import_Guide.md`: format, attachment scope, manual settings, and verification steps.
- one JSON per book.
- canonical `03_LoreForge_Spec.json` outside or alongside Export.

## 5. Import verification

1. Back up or export the current Lumiverse data relevant to the test.
2. Import one book.
3. Inspect entry count, titles, content, and settings.
4. Attach it to the intended Character, Persona, or Global scope.
5. Run Dry Run with at least three positives and two near misses.
6. Inspect World Book Diagnostics for activation, cooldown, and delay state.
7. Confirm prompt position and budget behavior.
8. Only then import the rest of the pack.

If fields are dropped or remapped, request one native export from the current Lumiverse version and rebuild in native-template mode.
