"""Structural checks for Project Steward specialist handoff packets."""

from __future__ import annotations

from typing import Any


SCHEMA_ID = "lumiverse-toolkit.specialist-handoff/v1"
SPECIALISTS = {"forge-lumiverse-lorebooks", "lumiverse-preset-converter"}
RETURN_ITEMS = {
    "completed_artifact",
    "artifact_passport",
    "validation_findings",
    "proposed_record_changes",
    "unresolved_questions",
}


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def validate_specialist_handoff(handoff: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(handoff, dict):
        return [_finding("invalid-handoff-type", "$", "Handoff must be an object.", "blocker")]

    for field in (
        "schema",
        "task_id",
        "specialist",
        "operation",
        "artifact",
        "evidence",
        "constraints",
        "dependencies",
        "policies",
        "specialist_requirements",
        "preserve",
        "return_contract",
    ):
        if field not in handoff:
            findings.append(_finding("missing-required-field", f"$.{field}", f"Missing '{field}'."))

    if handoff.get("schema") != SCHEMA_ID:
        findings.append(_finding("unsupported-schema", "$.schema", f"Expected '{SCHEMA_ID}'."))

    specialist = handoff.get("specialist")
    if specialist not in SPECIALISTS:
        findings.append(_finding("unsupported-specialist", "$.specialist", "Unknown specialist contract."))

    artifact = handoff.get("artifact")
    if not isinstance(artifact, dict) or not artifact.get("id") or not artifact.get("type"):
        findings.append(_finding("invalid-artifact-reference", "$.artifact", "Artifact needs stable id and type."))

    evidence = handoff.get("evidence")
    if not isinstance(evidence, dict) or not evidence.get("source_authority"):
        findings.append(
            _finding("missing-source-authority", "$.evidence.source_authority", "Ordered source authority is required.")
        )

    requirements = handoff.get("specialist_requirements")
    if specialist == "forge-lumiverse-lorebooks":
        tests = requirements.get("activation_tests") if isinstance(requirements, dict) else None
        if not isinstance(tests, dict) or not all(tests.get(name) for name in ("positive", "negative", "collision")):
            findings.append(
                _finding(
                    "missing-lorebook-tests",
                    "$.specialist_requirements.activation_tests",
                    "Lorebook handoff needs positive, negative, and collision trigger snippets.",
                )
            )

    if specialist == "lumiverse-preset-converter" and isinstance(requirements, dict):
        if requirements.get("preset_kind") == "generic_roleplay" and requirements.get("tracker") not in (None, "unselected"):
            findings.append(
                _finding(
                    "generic-preset-tracker-coupling",
                    "$.specialist_requirements.tracker",
                    "Generic roleplay presets must remain tracker-agnostic until a tracker is selected.",
                )
            )

    for index, policy in enumerate(handoff.get("policies", [])):
        if not isinstance(policy, dict) or policy.get("id") != "policy-real-frank":
            continue
        applies_to = policy.get("applies_to")
        if not isinstance(applies_to, dict) or applies_to.get("artifact_type") != "loom_preset":
            findings.append(
                _finding(
                    "unscoped-real-frank-policy",
                    f"$.policies[{index}].applies_to",
                    "Real Frank policy must be scoped to matching Loom presets.",
                )
            )

    returned = handoff.get("return_contract")
    missing = RETURN_ITEMS - set(returned if isinstance(returned, list) else [])
    if missing:
        findings.append(
            _finding(
                "incomplete-return-contract",
                "$.return_contract",
                "Missing return items: " + ", ".join(sorted(missing)) + ".",
            )
        )

    return findings

