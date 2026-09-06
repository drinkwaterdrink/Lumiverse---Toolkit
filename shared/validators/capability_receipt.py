"""Validate evidence maturity claims in Lumi Tools capability receipts."""

from __future__ import annotations

from typing import Any


SCHEMA_ID = "lumiverse-toolkit.capability-receipt/v1"
MATURITY = {
    "concept", "static_validated", "simulated", "runtime_observed",
    "certified_for_build",
}
OBSERVATION_KINDS = {"user_reported", "captured_diagnostics"}


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def validate_capability_receipt(record: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(record, dict):
        return [_finding("invalid-receipt", "$", "Capability receipt must be an object.", "blocker")]
    if record.get("schema") != SCHEMA_ID:
        findings.append(_finding("unsupported-schema", "$.schema", f"Expected '{SCHEMA_ID}'."))
    if not isinstance(record.get("artifact_id"), str) or not record.get("artifact_id"):
        findings.append(_finding("missing-artifact-id", "$.artifact_id", "artifact_id is required."))
    target = record.get("target")
    if not isinstance(target, dict) or target.get("application") != "Lumiverse":
        findings.append(_finding("invalid-target", "$.target", "Target application must be Lumiverse."))
        target = {}
    capabilities = record.get("capabilities")
    if not isinstance(capabilities, list):
        return findings + [_finding("invalid-capabilities", "$.capabilities", "capabilities must be an array.", "blocker")]

    seen: set[str] = set()
    for index, capability in enumerate(capabilities):
        path = f"$.capabilities[{index}]"
        if not isinstance(capability, dict):
            findings.append(_finding("invalid-capability", path, "Capability must be an object."))
            continue
        capability_id = capability.get("id")
        if not isinstance(capability_id, str) or not capability_id:
            findings.append(_finding("missing-capability-id", f"{path}.id", "Capability id is required."))
        elif capability_id in seen:
            findings.append(_finding("duplicate-capability-id", f"{path}.id", f"Duplicate capability id '{capability_id}'."))
        else:
            seen.add(capability_id)
        maturity = capability.get("maturity")
        if maturity not in MATURITY:
            findings.append(_finding("unsupported-maturity", f"{path}.maturity", "Unknown evidence maturity."))
            continue
        evidence = capability.get("evidence")
        if maturity != "concept" and (not isinstance(evidence, list) or not evidence):
            findings.append(_finding("missing-capability-evidence", f"{path}.evidence", "This maturity requires evidence."))
        if maturity in {"runtime_observed", "certified_for_build"} and capability.get("observation_kind") not in OBSERVATION_KINDS:
            findings.append(_finding("missing-observation-kind", f"{path}.observation_kind", "Runtime evidence must be user_reported or captured_diagnostics."))
        if maturity == "certified_for_build":
            if not isinstance(target.get("lumiverse_build"), str) or not target.get("lumiverse_build"):
                findings.append(_finding("missing-target-build", "$.target.lumiverse_build", "Certification requires a named Lumiverse build.", "blocker"))
            kinds = {item.get("kind") for item in evidence if isinstance(item, dict)} if isinstance(evidence, list) else set()
            if "repeatable_runtime_diagnostic" not in kinds:
                findings.append(_finding("insufficient-certification-evidence", f"{path}.evidence", "Certification requires repeatable runtime diagnostic evidence.", "blocker"))
        for field in ("dependencies", "limitations"):
            if not isinstance(capability.get(field), list):
                findings.append(_finding("invalid-capability-field", f"{path}.{field}", f"{field} must be an array."))
    return findings
