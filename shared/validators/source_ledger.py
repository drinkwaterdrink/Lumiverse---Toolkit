"""Validate source provenance, temporal snapshots, and knowledge ownership."""

from __future__ import annotations

from typing import Any


SCHEMA_ID = "lumiverse-toolkit.source-ledger/v1"
SOURCE_TYPES = {"official", "wiki", "fan_wiki", "user_notes", "novel_text", "transcript", "character_card", "world_book", "database_reference", "mixed"}
AUTHORITIES = {"primary", "secondary", "user", "adaptation_reference"}
RELEVANCE = {"include", "exclude", "review"}
FACT_STATUSES = {"CANON", "USER_CANON", "PROVISIONAL", "INFERRED", "CONFLICTED", "ADAPTATION_CHOICE"}
VISIBILITY = {"public", "character_known", "rumor", "gm_truth"}


def _finding(code: str, path: str, message: str, severity: str = "major") -> dict[str, str]:
    return {"code": code, "path": path, "message": message, "severity": severity}


def _ids(items: Any) -> set[str]:
    return {item.get("id") for item in items if isinstance(item, dict) and isinstance(item.get("id"), str)} if isinstance(items, list) else set()


def validate_source_ledger(record: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(record, dict):
        return [_finding("invalid-source-ledger", "$", "Source ledger must be an object.", "blocker")]
    if record.get("schema") != SCHEMA_ID:
        findings.append(_finding("unsupported-schema", "$.schema", f"Expected '{SCHEMA_ID}'."))
    if record.get("status") not in {"draft", "review", "final"}:
        findings.append(_finding("invalid-ledger-status", "$.status", "Unknown source ledger status."))
    snapshot = record.get("snapshot")
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("order"), (int, float)):
        findings.append(_finding("invalid-temporal-snapshot", "$.snapshot", "Snapshot needs a comparable numeric order."))
        snapshot_order = None
    else:
        snapshot_order = snapshot["order"]

    sources = record.get("sources")
    if not isinstance(sources, list):
        return findings + [_finding("invalid-sources", "$.sources", "sources must be an array.", "blocker")]
    source_ids: set[str] = set()
    hash_owner: dict[str, str] = {}
    sources_by_id: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(sources):
        path = f"$.sources[{index}]"
        if not isinstance(source, dict):
            findings.append(_finding("invalid-source", path, "Source must be an object."))
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id:
            findings.append(_finding("missing-source-id", f"{path}.id", "Source id is required."))
            continue
        if source_id in source_ids:
            findings.append(_finding("duplicate-source-id", f"{path}.id", f"Duplicate source id '{source_id}'."))
        source_ids.add(source_id)
        sources_by_id[source_id] = source
        if source.get("type") not in SOURCE_TYPES:
            findings.append(_finding("invalid-source-type", f"{path}.type", "Unknown source type."))
        if source.get("authority") not in AUTHORITIES:
            findings.append(_finding("invalid-source-authority", f"{path}.authority", "Unknown source authority."))
        relevance = source.get("relevance")
        if relevance not in RELEVANCE:
            findings.append(_finding("invalid-source-relevance", f"{path}.relevance", "Unknown relevance decision."))
        if relevance in {"exclude", "review"} and not str(source.get("relevance_reason", "")).strip():
            findings.append(_finding("missing-relevance-reason", f"{path}.relevance_reason", "Excluded/review sources require a reason."))
        content_hash = source.get("content_hash")
        if isinstance(content_hash, str) and content_hash:
            prior = hash_owner.get(content_hash)
            alias_of = source.get("alias_of")
            if prior is not None and alias_of != prior:
                findings.append(_finding("duplicate-source-content", f"{path}.content_hash", f"Content duplicates '{prior}' without an alias."))
            else:
                hash_owner.setdefault(content_hash, source_id)

    for index, source in enumerate(sources):
        if isinstance(source, dict) and source.get("alias_of") is not None:
            alias = source.get("alias_of")
            if alias not in source_ids or alias == source.get("id"):
                findings.append(_finding("invalid-source-alias", f"$.sources[{index}].alias_of", "alias_of must reference another source."))

    entities = record.get("entities")
    if not isinstance(entities, list):
        return findings + [_finding("invalid-entities", "$.entities", "entities must be an array.", "blocker")]
    entity_ids: set[str] = set()
    for index, entity in enumerate(entities):
        path = f"$.entities[{index}]"
        if not isinstance(entity, dict) or not isinstance(entity.get("id"), str):
            findings.append(_finding("invalid-entity", path, "Entity needs an id."))
            continue
        if entity["id"] in entity_ids:
            findings.append(_finding("duplicate-entity-id", f"{path}.id", "Duplicate entity id."))
        entity_ids.add(entity["id"])
        for source_id in entity.get("source_ids", []):
            if source_id not in source_ids:
                findings.append(_finding("unknown-entity-source", f"{path}.source_ids", f"Unknown source '{source_id}'."))

    facts = record.get("facts")
    if not isinstance(facts, list):
        return findings + [_finding("invalid-facts", "$.facts", "facts must be an array.", "blocker")]
    fact_ids: set[str] = set()
    conflicted_fact_ids: set[str] = set()
    facts_by_id: dict[str, dict[str, Any]] = {}
    for index, fact in enumerate(facts):
        path = f"$.facts[{index}]"
        if not isinstance(fact, dict) or not isinstance(fact.get("id"), str):
            findings.append(_finding("invalid-fact", path, "Fact needs an id."))
            continue
        fact_id = fact["id"]
        if fact_id in fact_ids:
            findings.append(_finding("duplicate-fact-id", f"{path}.id", "Duplicate fact id."))
        fact_ids.add(fact_id)
        facts_by_id[fact_id] = fact
        if fact.get("subject_id") not in entity_ids:
            findings.append(_finding("unknown-fact-subject", f"{path}.subject_id", "Fact subject is not inventoried."))
        status = fact.get("status")
        if status not in FACT_STATUSES:
            findings.append(_finding("invalid-fact-status", f"{path}.status", "Unknown fact status."))
        if status == "CONFLICTED":
            conflicted_fact_ids.add(fact_id)
        provenance = fact.get("source_ids")
        if status != "PROVISIONAL" and (not isinstance(provenance, list) or not provenance):
            findings.append(_finding("missing-fact-provenance", f"{path}.source_ids", "Non-provisional fact requires source provenance."))
        for source_id in provenance if isinstance(provenance, list) else []:
            if source_id not in source_ids:
                findings.append(_finding("unknown-fact-source", f"{path}.source_ids", f"Unknown source '{source_id}'."))
        if fact.get("visibility") not in VISIBILITY:
            findings.append(_finding("invalid-fact-visibility", f"{path}.visibility", "Unknown visibility partition."))
        valid_from = fact.get("valid_from")
        if fact.get("active_at_snapshot") and snapshot_order is not None and isinstance(valid_from, dict) and isinstance(valid_from.get("order"), (int, float)) and valid_from["order"] > snapshot_order:
            findings.append(_finding("future-knowledge-leak", f"{path}.active_at_snapshot", "Fact begins after the selected snapshot.", "blocker"))
        owner = fact.get("owner")
        if fact.get("visibility") == "gm_truth" and fact.get("active_at_snapshot") and isinstance(owner, str) and owner.startswith("character:"):
            owner_id = owner.split(":", 1)[1]
            knowers = fact.get("knowers", [])
            if owner_id not in knowers:
                findings.append(_finding("hidden-truth-owner-leak", f"{path}.owner", "GM truth cannot enter an unknowing character owner.", "blocker"))
        for knower in fact.get("knowers", []):
            if knower not in entity_ids:
                findings.append(_finding("unknown-fact-knower", f"{path}.knowers", f"Unknown knower '{knower}'."))

    conflicts = record.get("conflicts", [])
    conflict_fact_ids: set[str] = set()
    for index, conflict in enumerate(conflicts if isinstance(conflicts, list) else []):
        path = f"$.conflicts[{index}]"
        if not isinstance(conflict, dict):
            findings.append(_finding("invalid-conflict", path, "Conflict must be an object."))
            continue
        ids = conflict.get("fact_ids", [])
        conflict_fact_ids.update(item for item in ids if isinstance(item, str))
        if any(item not in fact_ids for item in ids):
            findings.append(_finding("unknown-conflict-fact", f"{path}.fact_ids", "Conflict references an unknown fact."))
        if record.get("status") == "final" and conflict.get("status") == "unresolved":
            findings.append(_finding("unresolved-source-conflict", path, "Final ledger cannot retain an unresolved source conflict.", "blocker"))
        if conflict.get("status") == "resolved" and not str(conflict.get("resolution", "")).strip():
            findings.append(_finding("missing-conflict-resolution", f"{path}.resolution", "Resolved conflict needs a resolution."))
    for fact_id in conflicted_fact_ids - conflict_fact_ids:
        findings.append(_finding("orphan-conflicted-fact", "$.facts", f"Conflicted fact '{fact_id}' lacks a conflict record."))

    adaptations = record.get("adaptations", [])
    for index, adaptation in enumerate(adaptations if isinstance(adaptations, list) else []):
        path = f"$.adaptations[{index}]"
        source_fact_ids = adaptation.get("source_fact_ids", []) if isinstance(adaptation, dict) else []
        if not source_fact_ids or any(item not in fact_ids for item in source_fact_ids):
            findings.append(_finding("unknown-adaptation-source-fact", f"{path}.source_fact_ids", "Adaptation needs valid source facts."))
        statement = adaptation.get("statement") if isinstance(adaptation, dict) else None
        if isinstance(statement, str) and source_fact_ids and all(facts_by_id.get(item, {}).get("statement") == statement for item in source_fact_ids):
            findings.append(_finding("undifferentiated-adaptation", f"{path}.statement", "Adaptation must state how roleplay differs from source canon."))

    suggestions = record.get("entry_suggestions", [])
    for index, suggestion in enumerate(suggestions if isinstance(suggestions, list) else []):
        path = f"$.entry_suggestions[{index}]"
        entity_refs = suggestion.get("entity_ids", []) if isinstance(suggestion, dict) else []
        fact_refs = suggestion.get("fact_ids", []) if isinstance(suggestion, dict) else []
        if not entity_refs and not fact_refs:
            findings.append(_finding("ungrounded-entry-suggestion", path, "Entry suggestion needs entity or fact grounding."))
        if any(item not in entity_ids for item in entity_refs) or any(item not in fact_ids for item in fact_refs):
            findings.append(_finding("unknown-entry-grounding", path, "Entry suggestion references unknown grounding."))
    return findings
