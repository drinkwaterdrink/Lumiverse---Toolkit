# CHARX packaging

For created cards, default to a downloadable `.charx` plus a short passport. Use
the V3 envelope `{"spec":"chara_card_v3","spec_version":"3.0","data":{...}}`.
Author the ten base fields by the existing Character Contract; use exact keys:
name, description, personality, scenario, first_mes, mes_example, system_prompt,
post_history_instructions, creator_notes, tags. Tags are a string array. The
other nine are strings. Optional alternate_greetings and group_only_greetings
are string arrays; assets is an array; extensions is an opaque object.

Run from this skill directory:

```sh
python3 scripts/package_charx.py card.json output.charx
python3 scripts/package_charx.py edited-card.json revised.charx --source-charx original.charx
python3 scripts/package_charx.py card.json output.charx --assets-dir resources
```

The resources directory mirrors paths inside the archive (for example
`resources/assets/icon/1.webp`). Asset declarations use archive-relative
`embeded://assets/icon/1.webp` URIs, as observed in the supplied V3 example.
The helper checks declared embedded resources, not image decoding or rendering.
External URIs are preserved, never downloaded or certified as available.

When revising, read the complete source card.json and patch only requested keys;
pass the complete edited object and original archive to the helper. The helper
preserves archive members but replaces card.json with the supplied JSON; it
cannot recover JSON properties omitted by its caller. Compare before/after
objects, book entries and asset bytes and report intentional differences.

Embedded character_book objects contain an entries array. Preserve unfamiliar
entry keys. Use the bundled lorebook specialist for authoring, but do not insert
its neutral project spec directly into character_book. Obtain a supported card
book template or map verified entry fields explicitly and report limitations.

Evidence: a generated base V3 Mara card was imported and re-exported by the user;
ten authored fields compared equal, with Lumiverse adding its library-scope
extension. This is base-card evidence, not a guarantee for every module or build.
Synthetic tests cover packaging and opaque book/assets preservation. Advanced
alternate modules, runtime activation, and media rendering remain separately
unverified. Never invent extension keys for those features.

Requires Python 3.10+. Outputs are exclusive: choose a new filename if one exists.
