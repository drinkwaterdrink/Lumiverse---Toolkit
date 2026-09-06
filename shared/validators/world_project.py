"""Dependency-free validation for Lumi Tools World Forge build records."""

from __future__ import annotations

from typing import Any

SCHEMA_ID = "lumiverse-toolkit.world-project/v1"
PROFILES = {"single_character", "character_with_world", "narrator_world", "ensemble_scenario", "multi_card_world"}
OPERATIONS = {"create", "revise", "audit", "convert"}
MODES = {"guided", "fast", "full_detail"}
STATUSES = {"draft", "approved", "building", "complete"}
RESERVED = {"actions", "dialogue", "thoughts", "feelings", "attraction", "consent", "decisions", "relationships", "abilities", "backstory", "next_voluntary_action"}


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def validate_world_project(record: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(record, dict):
        return [_finding("invalid-record-type", "$", "World project must be an object.", "blocker")]
    if record.get("schema") != SCHEMA_ID:
        findings.append(_finding("unsupported-schema", "$.schema", f"Expected '{SCHEMA_ID}'."))
    if not isinstance(record.get("project_id"), str) or not record["project_id"].strip():
        findings.append(_finding("missing-project-id", "$.project_id", "project_id must be non-empty."))
    build = record.get("build")
    if not isinstance(build, dict):
        findings.append(_finding("invalid-build", "$.build", "build must be an object."))
        build = {}
    profile = build.get("profile")
    if profile not in PROFILES:
        findings.append(_finding("unsupported-profile", "$.build.profile", f"Profile must be one of {sorted(PROFILES)}."))
    if build.get("operation") not in OPERATIONS:
        findings.append(_finding("invalid-operation", "$.build.operation", "Unsupported operation."))
    if build.get("mode") not in MODES:
        findings.append(_finding("invalid-mode", "$.build.mode", "Unsupported authoring mode."))
    if build.get("status") not in STATUSES:
        findings.append(_finding("invalid-status", "$.build.status", "Unsupported build status."))

    interaction = record.get("interaction")
    if not isinstance(interaction, dict):
        findings.append(_finding("invalid-interaction", "$.interaction", "interaction must be an object."))
    agency = record.get("agency")
    if not isinstance(agency, dict) or agency.get("protected_subject") != "{{user}}":
        findings.append(_finding("incomplete-agency-contract", "$.agency", "protected_subject must be {{user}}.", "blocker"))
    else:
        reserved = agency.get("reserved")
        missing = RESERVED - set(reserved if isinstance(reserved, list) else [])
        if missing:
            findings.append(_finding("incomplete-agency-contract", "$.agency.reserved", "Missing: " + ", ".join(sorted(missing)), "blocker"))

    entity_ids = record.get("entity_ids", [])
    if not isinstance(entity_ids, list) or any(not isinstance(x, str) or not x for x in entity_ids):
        findings.append(_finding("invalid-entity-ids", "$.entity_ids", "entity_ids must be non-empty strings."))
        entity_ids = []
    if len(entity_ids) != len(set(entity_ids)):
        findings.append(_finding("duplicate-entity-id", "$.entity_ids", "entity_ids must be unique."))
    entity_set = set(entity_ids)

    artifacts = record.get("artifacts", [])
    if not isinstance(artifacts, list):
        findings.append(_finding("invalid-artifacts", "$.artifacts", "artifacts must be an array."))
        artifacts = []
    artifact_ids: set[str] = set()
    for i, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            findings.append(_finding("invalid-artifact", f"$.artifacts[{i}]", "Artifact must be an object."))
            continue
        aid = artifact.get("id")
        if not isinstance(aid, str) or not aid:
            findings.append(_finding("missing-artifact-id", f"$.artifacts[{i}].id", "Artifact needs an ID."))
        elif aid in artifact_ids:
            findings.append(_finding("duplicate-artifact-id", f"$.artifacts[{i}].id", f"Duplicate artifact ID '{aid}'."))
        else:
            artifact_ids.add(aid)

    counts: dict[str, int] = {}
    for artifact in artifacts:
        if isinstance(artifact, dict) and isinstance(artifact.get("type"), str):
            counts[artifact["type"]] = counts.get(artifact["type"], 0) + 1
    if profile in {"character_with_world", "narrator_world", "ensemble_scenario"}:
        if counts.get("character_card", 0) != 1 or counts.get("embedded_character_book", 0) != 1:
            findings.append(_finding("profile-output-mismatch", "$.artifacts", "This profile requires one character_card and one embedded_character_book."))
    elif profile == "multi_card_world":
        if counts.get("character_card", 0) < 2 or counts.get("shared_character_book", 0) != 1:
            findings.append(_finding("profile-output-mismatch", "$.artifacts", "multi_card_world requires at least two character_card artifacts and one shared_character_book."))
    elif profile == "single_character" and counts.get("character_card", 0) != 1:
        findings.append(_finding("profile-output-mismatch", "$.artifacts", "single_character requires one character_card."))

    temporal = record.get("temporal", [])
    if not isinstance(temporal, list):
        findings.append(_finding("invalid-temporal", "$.temporal", "temporal must be an array."))
        temporal = []
    seen_temporal: dict[tuple[str, str], tuple[Any, Any]] = {}
    for i, item in enumerate(temporal):
        if not isinstance(item, dict) or item.get("entity_id") not in entity_set:
            findings.append(_finding("invalid-temporal-entity", f"$.temporal[{i}]", "Temporal snapshot references an unknown entity."))
            continue
        key = (item["entity_id"], str(item.get("era", "")))
        state = (item.get("status"), item.get("location"))
        if key in seen_temporal and seen_temporal[key] != state:
            findings.append(_finding("temporal-conflict", f"$.temporal[{i}]", f"Conflicting snapshot for {key[0]} in {key[1]}."))
        seen_temporal[key] = state

    relationships = record.get("relationships", [])
    if not isinstance(relationships, list):
        findings.append(_finding("invalid-relationships", "$.relationships", "relationships must be an array."))
        relationships = []
    relation_ids = {r.get("id") for r in relationships if isinstance(r, dict) and isinstance(r.get("id"), str)}
    for i, relation in enumerate(relationships):
        path = f"$.relationships[{i}]"
        if not isinstance(relation, dict) or relation.get("from") not in entity_set or relation.get("to") not in entity_set:
            findings.append(_finding("invalid-relationship-endpoint", path, "Relationship endpoints must reference entities."))
            continue
        if relation.get("from") == relation.get("to"):
            findings.append(_finding("self-relationship", path, "Relationship cannot point to itself."))
        reciprocal = relation.get("reciprocal_id")
        if reciprocal is None and not relation.get("intentional_asymmetry", False):
            findings.append(_finding("unreviewed-relationship-asymmetry", path, "Relationship has no reciprocal review.", "minor"))
        elif reciprocal is not None:
            target = next((r for r in relationships if isinstance(r, dict) and r.get("id") == reciprocal), None)
            if not target or target.get("from") != relation.get("to") or target.get("to") != relation.get("from"):
                findings.append(_finding("relationship-reciprocal-mismatch", path, "Reciprocal relationship must reverse endpoints."))
    return findings
