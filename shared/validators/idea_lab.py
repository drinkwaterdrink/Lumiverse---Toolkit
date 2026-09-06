"""Validate Idea Lab divergence, selection, and agency evidence."""

from __future__ import annotations

from typing import Any


SCHEMA_ID = "lumiverse-toolkit.idea-lab/v1"
ROUTES = {"direct", "variants", "interview", "anti_generic", "combine"}
CANDIDATE_STATUSES = {"provisional", "approved", "rejected"}


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def validate_idea_lab(record: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(record, dict):
        return [_finding("invalid-idea-lab", "$", "Idea Lab record must be an object.", "blocker")]
    if record.get("schema") != SCHEMA_ID:
        findings.append(_finding("unsupported-schema", "$.schema", f"Expected '{SCHEMA_ID}'."))
    route = record.get("route")
    if route not in ROUTES:
        findings.append(_finding("invalid-route", "$.route", "Unknown Idea Lab route."))
    if not isinstance(record.get("brief"), str) or not record.get("brief", "").strip():
        findings.append(_finding("missing-brief", "$.brief", "The user's preserved brief is required."))

    candidates = record.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        return findings + [_finding("missing-candidates", "$.candidates", "At least one candidate is required.", "blocker")]
    if route == "variants" and len(candidates) < 3:
        findings.append(_finding("insufficient-variants", "$.candidates", "Variant route requires at least three candidates."))

    ids: set[str] = set()
    signatures: set[str] = set()
    dimensions: set[str] = set()
    agency_risk_ids: set[str] = set()
    for index, candidate in enumerate(candidates):
        path = f"$.candidates[{index}]"
        if not isinstance(candidate, dict):
            findings.append(_finding("invalid-candidate", path, "Candidate must be an object."))
            continue
        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, str) or not candidate_id:
            findings.append(_finding("missing-candidate-id", f"{path}.id", "Candidate id is required."))
        elif candidate_id in ids:
            findings.append(_finding("duplicate-candidate-id", f"{path}.id", f"Duplicate candidate id '{candidate_id}'."))
        else:
            ids.add(candidate_id)
        if candidate.get("status") not in CANDIDATE_STATUSES:
            findings.append(_finding("invalid-candidate-status", f"{path}.status", "Unknown candidate status."))
        for field in ("premise", "foundation", "deviation", "scene_engine", "recurring_pressure", "world_motion", "artifact_profile"):
            if not isinstance(candidate.get(field), str) or not candidate.get(field, "").strip():
                findings.append(_finding("missing-candidate-field", f"{path}.{field}", f"{field} is required."))
        signature = candidate.get("direction_signature")
        if not isinstance(signature, str) or not signature.strip():
            findings.append(_finding("missing-direction-signature", f"{path}.direction_signature", "Direction signature is required."))
        elif signature.casefold() in signatures:
            findings.append(_finding("duplicate-direction", f"{path}.direction_signature", "Candidate duplicates another direction."))
        else:
            signatures.add(signature.casefold())
        dims = candidate.get("divergence_dimensions")
        if not isinstance(dims, list) or not all(isinstance(item, str) and item for item in dims):
            findings.append(_finding("invalid-divergence-dimensions", f"{path}.divergence_dimensions", "Divergence dimensions must be strings."))
        else:
            dimensions.update(item.casefold() for item in dims)
        for field in ("player_positions", "agency_risks"):
            if not isinstance(candidate.get(field), list):
                findings.append(_finding("invalid-candidate-list", f"{path}.{field}", f"{field} must be an array."))
        if candidate.get("agency_risks") and isinstance(candidate_id, str):
            agency_risk_ids.add(candidate_id)

    if route == "variants" and len(dimensions) < 2:
        findings.append(_finding("insufficient-divergence", "$.candidates", "Variant set must diverge across at least two meaningful dimensions."))

    selected = record.get("selected_candidate_id")
    if selected is not None and selected not in ids:
        findings.append(_finding("unknown-selected-candidate", "$.selected_candidate_id", "Selected candidate does not exist."))
    for index, candidate in enumerate(candidates):
        if isinstance(candidate, dict) and candidate.get("status") == "approved" and candidate.get("id") != selected:
            findings.append(_finding("canonized-unselected-candidate", f"$.candidates[{index}].status", "Only the selected candidate may become approved canon."))

    comparison = record.get("comparison")
    if not isinstance(comparison, list):
        findings.append(_finding("invalid-comparison", "$.comparison", "Comparison must be an array."))
        comparison = []
    compared = {item.get("candidate_id") for item in comparison if isinstance(item, dict)}
    if route == "variants" and compared != ids:
        findings.append(_finding("incomplete-comparison", "$.comparison", "Comparison must cover every candidate exactly by id."))
    for index, item in enumerate(comparison):
        if not isinstance(item, dict) or item.get("candidate_id") not in ids:
            findings.append(_finding("unknown-comparison-candidate", f"$.comparison[{index}]", "Comparison references an unknown candidate."))
        elif not isinstance(item.get("strengths"), list) or not isinstance(item.get("tradeoffs"), list):
            findings.append(_finding("invalid-comparison-evidence", f"$.comparison[{index}]", "Comparison needs strengths and tradeoffs arrays."))

    validation = record.get("validation", {})
    validation_findings = validation.get("findings", []) if isinstance(validation, dict) else []
    blocked_ids = {
        item.get("candidate_id") for item in validation_findings
        if isinstance(item, dict) and item.get("severity") == "blocker"
    }
    for candidate_id in agency_risk_ids - blocked_ids:
        findings.append(_finding("unblocked-agency-risk", "$.validation.findings", f"Agency risk for '{candidate_id}' requires a blocker.", "blocker"))
    return findings
