"""Load-bearing JSON Schemas pinning the v0.1 contract.

These schemas are the canonical contract between the procedure runner and
the seven components. Schema drift is a doctrinal change requiring operator
approval (per CLAUDE.md closed-set discipline).

Schemas (Draft 2020-12 dialect):
    INPUT_FRAME_SCHEMA
    PROCEDURE_STEP_OUTPUT_SCHEMA
    ARTICLE_VII_TRACKING_SCHEMA
    MEMORY_LOGGER_EVENT_SCHEMA
    MEMORY_LOGGER_CORRECTION_SCHEMA
"""

from __future__ import annotations

from typing import Any, Dict

JSON_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"


INPUT_FRAME_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "InputFrame",
    "type": "object",
    "required": [
        "id",
        "text",
        "locked_at_iso",
        "doctrinal_scope_tag",
        "companion_case",
    ],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "text": {"type": "string", "minLength": 1},
        "locked_at_iso": {"type": "string", "format": "date-time"},
        "doctrinal_scope_tag": {"type": "string", "minLength": 1},
        "companion_case": {"type": "string"},
    },
    "additionalProperties": False,
}


PROCEDURE_STEP_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "ProcedureStepOutput",
    "type": "object",
    "required": ["step_id", "content", "committed_at_iso", "time_box_status"],
    "properties": {
        "step_id": {
            "type": "string",
            "enum": [f"step_{i}" for i in range(1, 12)],
        },
        "content": {},  # opaque; per-step contract elsewhere
        "committed_at_iso": {"type": "string", "format": "date-time"},
        "time_box_status": {
            "type": "string",
            "enum": ["within_budget", "exceeded_budget", "aborted"],
        },
    },
    "additionalProperties": False,
}


ARTICLE_VII_TRACKING_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "ArticleVIITrackingRecord",
    "type": "object",
    "required": [
        "case_id",
        "prior_structures_referenced",
        "reuse_count_total",
        "patterns_recognized",
        "time_delta_vs_prior_similar",
    ],
    "properties": {
        "case_id": {"type": "string"},
        "prior_structures_referenced": {
            "type": "array",
            "items": {"type": "string"},
        },
        "reuse_count_total": {"type": "integer", "minimum": 0},
        "patterns_recognized": {
            "type": "array",
            "items": {"type": "string"},
        },
        "time_delta_vs_prior_similar": {"type": "number"},
    },
    "additionalProperties": False,
}


MEMORY_LOGGER_EVENT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "MemoryLoggerEvent",
    "type": "object",
    "required": ["case_id", "event_type", "committed_at_iso", "payload"],
    "properties": {
        "case_id": {"type": "string"},
        "event_type": {
            "type": "string",
            "enum": [
                "step_committed",
                "frame_locked",
                "verdict_emitted",
                "uncertainty_recorded",
                "reuse_detected",
            ],
        },
        "committed_at_iso": {"type": "string", "format": "date-time"},
        "payload": {"type": "object"},
    },
    "additionalProperties": False,
}


MEMORY_LOGGER_CORRECTION_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "MemoryLoggerCorrection",
    "type": "object",
    "required": [
        "case_id",
        "target_event_committed_at_iso",
        "correction_kind",
        "rationale",
        "committed_at_iso",
    ],
    "properties": {
        "case_id": {"type": "string"},
        "target_event_committed_at_iso": {
            "type": "string",
            "format": "date-time",
        },
        "correction_kind": {
            "type": "string",
            "enum": [
                "outcome_recorded",
                "prediction_falsified",
                "reuse_pattern_refuted",
            ],
        },
        "rationale": {"type": "string", "minLength": 1},
        "committed_at_iso": {"type": "string", "format": "date-time"},
    },
    "additionalProperties": False,
}


__all__ = [
    "JSON_SCHEMA_DIALECT",
    "INPUT_FRAME_SCHEMA",
    "PROCEDURE_STEP_OUTPUT_SCHEMA",
    "ARTICLE_VII_TRACKING_SCHEMA",
    "MEMORY_LOGGER_EVENT_SCHEMA",
    "MEMORY_LOGGER_CORRECTION_SCHEMA",
]
