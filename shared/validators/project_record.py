"""Deterministic structural checks for Lumiverse Toolkit project records."""

from __future__ import annotations

from typing import Any


SCHEMA_ID = "lumiverse-toolkit.project/v1"
REQUIRED_TOP_LEVEL = (
    "schema",
    "project",
    "authority",
    "preferences",
    "agency",
    "policies",
    "entities",
    "canon",
    "artifacts",
    "dependencies",
    "validation",
    "release",
    "decisions",
    "unresolved",
)
RESERVED_USER_AGENCY = {
    "actions",
    "dialogue",
    "thoughts",
    "feelings",
    "attraction",
    "consent",
    "decisions",
    "backstory",
}
COLLECTIONS_WITH_IDS = ("policies", "entities", "canon", "artifacts", "dependencies")


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def validate_project_record(record: Any) -> list[dict[str, str]]:
    """Return precise structural findings. An empty list means the contract passes."""

    findings: list[dict[str, str]] = []
    if not isinstance(record, dict):
        return [_finding("invalid-record-type", "$", "Project record must be an object.", "blocker")]

    for field in REQUIRED_TOP_LEVEL:
        if field not in record:
            findings.append(
                _finding("missing-required-field", f"$.{field}", f"Required field '{field}' is missing.")
            )

    if record.get("schema") != SCHEMA_ID:
        findings.append(
            _finding("unsupported-schema", "$.schema", f"Expected schema identifier '{SCHEMA_ID}'.")
        )

    project = record.get("project")
    if isinstance(project, dict):
        for field in ("id", "name", "version", "status", "target"):
            if field not in project:
                findings.append(
                    _finding("missing-required-field", f"$.project.{field}", f"Project field '{field}' is missing.")
                )
    elif "project" in record:
        findings.append(_finding("invalid-field-type", "$.project", "Project must be an object."))

    seen_ids: dict[str, str] = {}
    for collection_name in COLLECTIONS_WITH_IDS:
        collection = record.get(collection_name, [])
        if not isinstance(collection, list):
            findings.append(
                _finding("invalid-field-type", f"$.{collection_name}", "Collection must be an array.")
            )
            continue
        for index, item in enumerate(collection):
            path = f"$.{collection_name}[{index}]"
            if not isinstance(item, dict):
                findings.append(_finding("invalid-item-type", path, "Collection item must be an object."))
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id.strip():
                findings.append(_finding("missing-stable-id", f"{path}.id", "Item needs a non-empty stable ID."))
                continue
            if item_id in seen_ids:
                findings.append(
                    _finding(
                        "duplicate-id",
                        f"{path}.id",
                        f"ID '{item_id}' is already used at {seen_ids[item_id]}.",
                    )
                )
            else:
                seen_ids[item_id] = f"{path}.id"

    artifact_ids = {
        item.get("id")
        for item in record.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for index, edge in enumerate(record.get("dependencies", [])):
        if not isinstance(edge, dict):
            continue
        for endpoint, code in (
            ("from", "missing-dependency-source"),
            ("to", "missing-dependency-target"),
        ):
            value = edge.get(endpoint)
            if value not in artifact_ids:
                findings.append(
                    _finding(
                        code,
                        f"$.dependencies[{index}].{endpoint}",
                        f"Dependency endpoint '{value}' does not reference an artifact ID.",
                    )
                )

    agency = record.get("agency")
    if isinstance(agency, dict):
        reserved = agency.get("reserved", [])
        missing = RESERVED_USER_AGENCY - set(reserved if isinstance(reserved, list) else [])
        if agency.get("protected_subject") != "{{user}}" or missing:
            details = ", ".join(sorted(missing)) if missing else "protected_subject"
            findings.append(
                _finding(
                    "incomplete-agency-contract",
                    "$.agency",
                    f"User agency contract is incomplete: {details}.",
                    "blocker",
                )
            )

    for index, policy in enumerate(record.get("policies", [])):
        if not isinstance(policy, dict) or policy.get("id") != "policy-real-frank":
            continue
        applies_to = policy.get("applies_to")
        if not isinstance(applies_to, dict) or applies_to.get("artifact_type") != "loom_preset":
            findings.append(
                _finding(
                    "unscoped-project-policy",
                    f"$.policies[{index}].applies_to",
                    "Real Frank rules must be scoped to Loom presets, not applied globally.",
                )
            )

    return findings

