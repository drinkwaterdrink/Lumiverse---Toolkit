"""Validate World Forge output manifests and optional file hashes."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

SCHEMA_ID = "lumiverse-toolkit.world-package/v1"
PROFILES = {"single_character", "character_with_world", "narrator_world", "ensemble_scenario", "multi_card_world"}
REQUIRED_ROLES = {"charx", "card_source", "loreforge_source", "import_guide", "artifact_passport"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def validate_world_package(manifest: Any, root: Path | None = None) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(manifest, dict):
        return [_finding("invalid-manifest", "$", "Manifest must be an object.", "blocker")]
    if manifest.get("schema") != SCHEMA_ID:
        findings.append(_finding("unsupported-schema", "$.schema", f"Expected '{SCHEMA_ID}'."))
    if not isinstance(manifest.get("project_id"), str) or not manifest["project_id"]:
        findings.append(_finding("missing-project-id", "$.project_id", "project_id is required."))
    if manifest.get("profile") not in PROFILES:
        findings.append(_finding("unsupported-profile", "$.profile", "Unknown World Forge profile."))
    if manifest.get("native_lumiverse_full_fidelity") is True and not manifest.get("native_template_evidence"):
        findings.append(_finding("unsupported-fidelity-claim", "$.native_template_evidence", "Full-fidelity native claims require template evidence.", "blocker"))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return findings + [_finding("invalid-artifacts", "$.artifacts", "artifacts must be an array.", "blocker")]
    roles: set[str] = set()
    paths: set[str] = set()
    ids: set[str] = set()
    for index, artifact in enumerate(artifacts):
        path = f"$.artifacts[{index}]"
        if not isinstance(artifact, dict):
            findings.append(_finding("invalid-artifact", path, "Artifact must be an object."))
            continue
        aid, role, relative = artifact.get("id"), artifact.get("role"), artifact.get("path")
        if not isinstance(aid, str) or not aid:
            findings.append(_finding("missing-artifact-id", f"{path}.id", "id is required."))
        elif aid in ids:
            findings.append(_finding("duplicate-artifact-id", f"{path}.id", "Artifact IDs must be unique."))
        else:
            ids.add(aid)
        if isinstance(role, str):
            roles.add(role)
        else:
            findings.append(_finding("missing-artifact-role", f"{path}.role", "role is required."))
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
            findings.append(_finding("unsafe-artifact-path", f"{path}.path", "Artifact path must be relative and contained."))
            continue
        if relative in paths:
            findings.append(_finding("duplicate-artifact-path", f"{path}.path", "Artifact paths must be unique."))
        paths.add(relative)
        digest = artifact.get("sha256")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            findings.append(_finding("invalid-sha256", f"{path}.sha256", "sha256 must be 64 lowercase hexadecimal characters."))
        if root is not None and isinstance(relative, str) and ".." not in Path(relative).parts and not Path(relative).is_absolute():
            file_path = root / relative
            if not file_path.is_file():
                findings.append(_finding("missing-artifact-file", f"{path}.path", f"File does not exist: {relative}."))
            elif isinstance(digest, str) and SHA256.fullmatch(digest) and hashlib.sha256(file_path.read_bytes()).hexdigest() != digest:
                findings.append(_finding("artifact-hash-mismatch", f"{path}.sha256", f"Hash does not match {relative}."))
    required = set(REQUIRED_ROLES)
    if manifest.get("profile") == "multi_card_world":
        required.add("character_book_backup")
        if sum(1 for a in artifacts if isinstance(a, dict) and a.get("role") == "charx") < 2:
            findings.append(_finding("profile-output-mismatch", "$.artifacts", "multi_card_world requires at least two CHARX artifacts."))
    else:
        required.update({"character_book_backup", "compilation_manifest"})
    for role in sorted(required - roles):
        findings.append(_finding("missing-required-artifact", "$.artifacts", f"Missing artifact role '{role}'."))
    return findings
