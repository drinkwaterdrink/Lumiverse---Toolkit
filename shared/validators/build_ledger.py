"""Validate durable phase state and artifact gates for connected builds."""

from __future__ import annotations

from pathlib import Path
from typing import Any


SCHEMA_ID = "lumiverse-toolkit.build-ledger/v1"
LEDGER_STATUSES = {"planning", "in_progress", "paused", "blocked", "complete"}
PHASE_STATUSES = {"pending", "in_progress", "complete", "skipped", "blocked"}


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def _safe_relative(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and not Path(value).is_absolute() and ".." not in Path(value).parts


def validate_build_ledger(ledger: Any, root: Path | None = None) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(ledger, dict):
        return [_finding("invalid-ledger", "$", "Build ledger must be an object.", "blocker")]
    if ledger.get("schema") != SCHEMA_ID:
        findings.append(_finding("unsupported-schema", "$.schema", f"Expected '{SCHEMA_ID}'."))
    if not isinstance(ledger.get("project_id"), str) or not ledger.get("project_id"):
        findings.append(_finding("missing-project-id", "$.project_id", "project_id is required."))
    if ledger.get("status") not in LEDGER_STATUSES:
        findings.append(_finding("invalid-ledger-status", "$.status", "Unknown ledger status."))
    phases = ledger.get("phases")
    if not isinstance(phases, list):
        return findings + [_finding("invalid-phases", "$.phases", "phases must be an array.", "blocker")]

    by_id: dict[str, dict[str, Any]] = {}
    index_by_id: dict[str, int] = {}
    for index, phase in enumerate(phases):
        path = f"$.phases[{index}]"
        if not isinstance(phase, dict):
            findings.append(_finding("invalid-phase", path, "Phase must be an object."))
            continue
        phase_id = phase.get("id")
        if not isinstance(phase_id, str) or not phase_id:
            findings.append(_finding("missing-phase-id", f"{path}.id", "Phase id is required."))
            continue
        if phase_id in by_id:
            findings.append(_finding("duplicate-phase-id", f"{path}.id", f"Duplicate phase id '{phase_id}'."))
        else:
            by_id[phase_id] = phase
            index_by_id[phase_id] = index
        status = phase.get("status")
        if status not in PHASE_STATUSES:
            findings.append(_finding("invalid-phase-status", f"{path}.status", "Unknown phase status."))
        if not isinstance(phase.get("dependencies"), list):
            findings.append(_finding("invalid-phase-dependencies", f"{path}.dependencies", "dependencies must be an array."))
        if not isinstance(phase.get("evidence"), list):
            findings.append(_finding("invalid-phase-evidence", f"{path}.evidence", "evidence must be an array."))
        if status == "skipped" and (not isinstance(phase.get("skip_reason"), str) or not phase.get("skip_reason", "").strip()):
            findings.append(_finding("missing-skip-reason", f"{path}.skip_reason", "Skipped phases require a reason."))
        if status == "complete":
            artifact = phase.get("artifact")
            anchor = phase.get("signoff_anchor")
            if not _safe_relative(artifact):
                findings.append(_finding("invalid-phase-artifact", f"{path}.artifact", "Complete phase needs a safe relative artifact path."))
            if not isinstance(anchor, str) or not anchor:
                findings.append(_finding("missing-signoff-anchor", f"{path}.signoff_anchor", "Complete phase needs a sign-off anchor."))
            if root is not None and _safe_relative(artifact):
                artifact_path = root / artifact
                if not artifact_path.is_file() or artifact_path.stat().st_size == 0:
                    findings.append(_finding("missing-phase-artifact", f"{path}.artifact", f"Complete phase artifact is missing or empty: {artifact}.", "blocker"))
                elif isinstance(anchor, str) and anchor not in artifact_path.read_text(encoding="utf-8"):
                    findings.append(_finding("missing-signoff-anchor", f"{path}.signoff_anchor", f"Artifact does not contain sign-off anchor '{anchor}'.", "blocker"))

    for phase_id, phase in by_id.items():
        index = index_by_id[phase_id]
        for dependency in phase.get("dependencies", []):
            dep = by_id.get(dependency)
            if dep is None:
                findings.append(_finding("unknown-phase-dependency", f"$.phases[{index}].dependencies", f"Unknown phase dependency '{dependency}'."))
            elif phase.get("status") == "complete" and dep.get("status") not in {"complete", "skipped"}:
                findings.append(_finding("unresolved-phase-dependency", f"$.phases[{index}].dependencies", f"Completed phase depends on unresolved phase '{dependency}'.", "blocker"))

    current = ledger.get("current_phase")
    if current is not None and current not in by_id:
        findings.append(_finding("unknown-current-phase", "$.current_phase", "current_phase does not reference a phase id."))
    if ledger.get("status") == "complete":
        unresolved = [pid for pid, phase in by_id.items() if phase.get("status") not in {"complete", "skipped"}]
        if unresolved or current is not None:
            findings.append(_finding("incomplete-ledger", "$", "Complete ledger still has unresolved phases or a current phase.", "blocker"))
    return findings
