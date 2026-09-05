#!/usr/bin/env node
import fs from "fs";

const file = process.argv[2];
if (!file) {
  console.error("Usage: node validate_regex.mjs <regex-export-or-loom.json>");
  process.exit(2);
}

const raw = JSON.parse(fs.readFileSync(file, "utf8"));

function locateScripts(value) {
  if (Array.isArray(value)) return { scripts: value, path: "root" };
  const candidates = [
    [value?.extensions?.regex_scripts, "extensions.regex_scripts"],
    [value?.preset?.extensions?.regex_scripts, "preset.extensions.regex_scripts"],
    [value?.data?.preset?.extensions?.regex_scripts, "data.preset.extensions.regex_scripts"],
    [value?.regex_scripts, "regex_scripts"],
    [value?.regexScripts, "regexScripts"],
    [value?.scripts, "scripts"],
  ];
  for (const [scripts, path] of candidates) {
    if (Array.isArray(scripts)) return { scripts, path };
  }
  return { scripts: [], path: null };
}

const { scripts, path } = locateScripts(raw);
const ids = new Set();
const errors = [];
const warnings = [];
const documentedPlacements = new Set(["user_input", "ai_output", "world_info", "reasoning"]);
const documentedTargets = new Set(["prompt", "response", "display"]);

if (path === null) warnings.push("no Regex script array found in a recognized container");

for (let index = 0; index < scripts.length; index += 1) {
  const script = scripts[index];
  const label = script?.name || `script ${index}`;
  if (!script || typeof script !== "object" || Array.isArray(script)) {
    errors.push(`${label}: script must be an object`);
    continue;
  }
  const id = script.script_id || script.id;
  if (!id) errors.push(`${label}: missing script_id/id`);
  else if (ids.has(id)) errors.push(`${label}: duplicate script ID ${id}`);
  else ids.add(id);

  const pattern = script.find_regex ?? script.findRegex ?? "";
  const flags = script.flags ?? "";
  if (typeof pattern !== "string") errors.push(`${label}: find regex must be a string`);
  if (typeof flags !== "string") errors.push(`${label}: flags must be a string`);
  if (typeof pattern === "string" && typeof flags === "string") {
    try {
      new RegExp(pattern, flags);
    } catch (error) {
      errors.push(`${label}: ${error.message}`);
    }
  }

  const placements = script.placement ?? script.placements;
  if (placements !== undefined && !Array.isArray(placements)) {
    errors.push(`${label}: placement must be an array`);
  } else if (Array.isArray(placements)) {
    for (const placement of placements) {
      if (!documentedPlacements.has(placement)) {
        warnings.push(`${label}: placement ${placement} is version-sensitive; verify in the target build`);
      }
    }
  }

  const targets = script.target ?? script.targets;
  if (targets !== undefined && !Array.isArray(targets)) {
    errors.push(`${label}: target must be an array`);
  } else if (Array.isArray(targets)) {
    for (const target of targets) {
      if (!documentedTargets.has(target)) warnings.push(`${label}: unknown target ${target}`);
    }
  }
}

console.log(JSON.stringify({
  source: file,
  container: path,
  scripts: scripts.length,
  unique_ids: ids.size,
  errors,
  warnings,
}, null, 2));
process.exit(errors.length ? 1 : 0);
