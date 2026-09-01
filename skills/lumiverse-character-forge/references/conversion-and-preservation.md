# Conversion and Preservation

## Supported documented formats

Lumiverse imports `.png`, `.json`, and `.charx` character files. It auto-detects Character Card Specification v1, v2, and v3.

Export roles:

- **JSON:** clean, smallest, universal data file;
- **PNG:** avatar image with embedded character data; standard and most portable sharing format;
- **CHARX:** most complete bundle; includes expressions, alternate fields, avatars, and other assets.

Choose CHARX when those modules/assets must travel together. Do not claim an attached World Book survives a particular export until a documented or tested round trip confirms it.

## Safe conversion sequence

1. Preserve the original file unchanged.
2. Identify source format/spec version and the exact target supported by evidence.
3. Inventory all base fields, alternate greetings, unknown keys, extensions, macros, embedded World Book data, images, expressions, and alternate modules.
4. Map source fields only where the target behavior is documented.
5. Preserve unknown fields and opaque extension data when editing an existing structure.
6. Record every transform, loss, unsupported feature, and unresolved mapping.
7. Validate syntax and required fields.
8. Import into a clean Lumiverse test environment when possible.
9. Export again and compare fields, modules, assets, macros, World Book link/entry count, and selected behavior.

If exact serialization is unavailable, stop at a complete authoring package plus placement map. Never reverse-engineer confident-looking JSON keys from UI labels.

## Revision behavior

For a narrow edit, patch only the requested field and required dependent references. Retain ordering, unknown properties, extension payloads, media references, and unrelated settings. A rename may require alias, example, greeting, World Book keyword, relationship, filename, or tracker-reference updates; report unavailable artifacts as unverified.

## Artifact passport

Return:

```yaml
artifact_id: stable ID or administrative proposal
operation: create | revise | audit | convert
source_format: exact format or null
target_format: exact format or null
preserved: [verified items]
transformed: [verified changes]
lost: [known losses]
unknown: [not checked or undocumented behavior]
validation: [checks actually run and results]
assumptions: [provisional or approved assumptions]
```

Do not use `lost: []` as a universal losslessness claim; qualify it by the checks actually run.

