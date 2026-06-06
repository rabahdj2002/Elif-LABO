"""Load-bearing JSON Schemas pinning the v0.1 contract.

These schemas are the canonical contract between the procedure runner and
the seven components. Schema drift is a doctrinal change requiring operator
approval (per CLAUDE.md closed-set discipline + Step 8 §8.7 schema freeze
at v0.4.0).

Schemas (Draft 2020-12 dialect):
    INPUT_FRAME_SCHEMA
    PROCEDURE_STEP_OUTPUT_SCHEMA
    ARTICLE_VII_TRACKING_SCHEMA
    MEMORY_LOGGER_EVENT_SCHEMA
    MEMORY_LOGGER_CORRECTION_SCHEMA

Per-step structured-output schemas (one per procedure step, 11 total):
    STEP_SCHEMAS — dict keyed by step_id

Helper:
    schema_for(step_id) -> dict

Article VII schema matches the SHAPE of `results/case_*/article_vii_tracking.json`
files (schema_version "v0.4.0"). The full case files are richer than the
v0.1 runtime contract; the schema captures the load-bearing subset the
Memory Logger must emit per-run. Optional richer fields are permitted by
`additionalProperties` policy per schema.
"""

from __future__ import annotations

from typing import Any, Dict

JSON_SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"

# Pinned per Step 8 §8.7. Used in Article VII tracking emit + Memory Logger.
SCHEMA_VERSION = "v0.4.0"


# ---- Input Frame -----------------------------------------------------------
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


# ---- Procedure Step Output (envelope) --------------------------------------
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
        "content": {},  # opaque; per-step contract in STEP_SCHEMAS below
        "committed_at_iso": {"type": "string", "format": "date-time"},
        "time_box_status": {
            "type": "string",
            "enum": ["within_budget", "exceeded_budget", "aborted"],
        },
    },
    "additionalProperties": False,
}


# ---- Article VII tracking record ------------------------------------------
# Matches the SHAPE of results/case_*/article_vii_tracking.json (v0.4.0).
ARTICLE_VII_TRACKING_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "ArticleVIITrackingRecord",
    "type": "object",
    "required": [
        "schema_version",
        "case_id",
        "procedure_version_used",
        "compositional_reuse",
        "pattern_emergence",
        "article_i_check",
        "article_ii_check",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "case_id": {"type": "string", "minLength": 1},
        "captured_ts": {"type": "string"},
        "execution_phase": {"type": "string"},
        "procedure_version_used": {"type": "string", "minLength": 1},
        "execution_order_note": {"type": "string"},
        "time_to_arbitration": {"type": "object"},
        "compositional_reuse": {
            "type": "object",
            "required": [
                "prior_structures_referenced",
                "reuse_count_total",
            ],
            "properties": {
                "prior_structures_referenced": {"type": "array"},
                "reuse_count_total": {"type": "integer", "minimum": 0},
                "fresh_structures_authored": {"type": "integer", "minimum": 0},
                "fresh_structures_note": {"type": "string"},
                "reuse_ratio": {"type": "number"},
            },
            "additionalProperties": True,
        },
        "pattern_emergence": {
            "type": "object",
            "required": ["patterns_recognized"],
            "properties": {
                "patterns_recognized": {"type": "array"},
                "patterns_deprecated": {"type": "array"},
                "candidate_frameworks": {"type": "array"},
            },
            "additionalProperties": True,
        },
        "memory_logger_capacity_change_records": {"type": "array"},
        "failure_records": {"type": "array"},
        "judgment_acts": {"type": "array"},
        "article_i_check": {"type": "object"},
        "article_ii_check": {"type": "object"},
    },
    "additionalProperties": True,
}


# ---- Memory Logger events + corrections -----------------------------------
MEMORY_LOGGER_EVENT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "MemoryLoggerEvent",
    "type": "object",
    "required": ["case_id", "event_type", "committed_at_iso", "payload"],
    "properties": {
        "case_id": {"type": "string", "minLength": 1},
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
        "case_id": {"type": "string", "minLength": 1},
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


# ---- Per-step structured-output schemas (11 steps) -------------------------
# Each schema is the SHAPE the LLM adapter must return for that step.
# They are deliberately permissive on free-text fields and tight on closed
# sets. See `results/case_01/condition_c_output.md` for reference content.

STEP_1_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step1FrameValidation",
    "type": "object",
    "required": ["verdict", "reasoning"],
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["valid", "invalid", "needs_decomposition"],
        },
        "reasoning": {"type": "string", "minLength": 1},
        "reformulated_frame": {"type": ["string", "null"]},
    },
    "additionalProperties": False,
}

STEP_2_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step2ObjectDecomposition",
    "type": "object",
    "required": ["axes"],
    "properties": {
        "axes": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["axis_name", "families"],
                "properties": {
                    "axis_name": {"type": "string", "minLength": 1},
                    "rationale": {"type": "string"},
                    "families": {
                        "type": "array",
                        "minItems": 2,
                        "items": {
                            "type": "object",
                            "required": ["family_id", "description"],
                            "properties": {
                                "family_id": {"type": "string"},
                                "description": {"type": "string"},
                            },
                            "additionalProperties": True,
                        },
                    },
                },
                "additionalProperties": True,
            },
        },
    },
    "additionalProperties": True,
}

STEP_3_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step3AssumptionSurfacing",
    "type": "object",
    "required": ["assumptions"],
    "properties": {
        "assumptions": {
            "type": "array",
            "minItems": 2,
            "items": {"type": "string", "minLength": 1},
        },
    },
    "additionalProperties": True,
}

STEP_4_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step4Hypotheses",
    "type": "object",
    "required": ["hypotheses"],
    "properties": {
        "hypotheses": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["hypothesis_id", "statement", "distinguishing_prediction"],
                "properties": {
                    "hypothesis_id": {"type": "string"},
                    "statement": {"type": "string"},
                    "distinguishing_prediction": {"type": "string"},
                },
                "additionalProperties": True,
            },
        },
    },
    "additionalProperties": True,
}

STEP_5_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step5FailureConditions",
    "type": "object",
    "required": ["failure_conditions"],
    "properties": {
        "failure_conditions": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["hypothesis_id", "fails_if"],
                "properties": {
                    "hypothesis_id": {"type": "string"},
                    "fails_if": {"type": "string"},
                },
                "additionalProperties": True,
            },
        },
    },
    "additionalProperties": True,
}

STEP_6_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step6MultiScaleMapping",
    "type": "object",
    "required": ["scales", "cross_scale_relations", "synthesis"],
    "properties": {
        "scales": {
            "type": "array",
            "minItems": 2,
            "items": {"type": "string"},
        },
        "cross_scale_relations": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
        },
        "synthesis": {
            "type": "string",
            "minLength": 20,
        },
    },
    "additionalProperties": True,
}

STEP_7_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step7OutsideFrameTrajectories",
    "type": "object",
    "required": ["trajectories"],
    "properties": {
        "trajectories": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["trajectory_id", "tag", "reason"],
                "properties": {
                    "trajectory_id": {"type": "string"},
                    "tag": {
                        "type": "string",
                        "enum": ["outside-original-frame", "deeper-frame-rejection"],
                    },
                    "reason": {"type": "string"},
                },
                "additionalProperties": True,
            },
        },
    },
    "additionalProperties": True,
}

STEP_8_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step8BranchingRoadmap",
    "type": "object",
    "required": ["stages"],
    "properties": {
        "stages": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["stage_id", "description", "continuation_gate"],
                "properties": {
                    "stage_id": {"type": "string"},
                    "description": {"type": "string"},
                    "continuation_gate": {"type": "string"},
                },
                "additionalProperties": True,
            },
        },
    },
    "additionalProperties": True,
}

# Step 9 absorbs old Step 11 (confidence + unresolved uncertainty).
STEP_9_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step9GovernanceKernel",
    "type": "object",
    "required": ["verdict", "confidence", "unresolved_uncertainty_sources"],
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["constrain", "refuse", "explicitly_abstain"],
        },
        "verdict_detail": {"type": "string"},
        "confidence": {"type": "string"},
        "unresolved_uncertainty_sources": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string"},
        },
    },
    "additionalProperties": True,
}

STEP_10_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step10OperativeTruthSeparation",
    "type": "object",
    "required": ["operative", "theoretical"],
    "properties": {
        "operative": {
            "type": "array",
            "items": {"type": "string"},
        },
        "theoretical": {
            "type": "array",
            "items": {"type": "string"},
        },
        "absence_log": {"type": "string"},
    },
    "additionalProperties": True,
}

STEP_11_OUTPUT_SCHEMA: Dict[str, Any] = {
    "$schema": JSON_SCHEMA_DIALECT,
    "title": "Step11MemoryLoggerEntry",
    "type": "object",
    "required": ["entries"],
    "properties": {
        "entries": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["kind", "description"],
                "properties": {
                    "kind": {
                        "type": "string",
                        "enum": [
                            "capacity_change",
                            "pattern_engaged",
                            "pattern_deprecated",
                            "judgment_act",
                        ],
                    },
                    "description": {"type": "string"},
                    "refutable_with": {"type": "string"},
                },
                "additionalProperties": True,
            },
        },
    },
    "additionalProperties": True,
}


STEP_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "step_1": STEP_1_OUTPUT_SCHEMA,
    "step_2": STEP_2_OUTPUT_SCHEMA,
    "step_3": STEP_3_OUTPUT_SCHEMA,
    "step_4": STEP_4_OUTPUT_SCHEMA,
    "step_5": STEP_5_OUTPUT_SCHEMA,
    "step_6": STEP_6_OUTPUT_SCHEMA,
    "step_7": STEP_7_OUTPUT_SCHEMA,
    "step_8": STEP_8_OUTPUT_SCHEMA,
    "step_9": STEP_9_OUTPUT_SCHEMA,
    "step_10": STEP_10_OUTPUT_SCHEMA,
    "step_11": STEP_11_OUTPUT_SCHEMA,
}


def schema_for(step_id: str) -> Dict[str, Any]:
    """Return the structured-output schema for a procedure step."""
    if step_id not in STEP_SCHEMAS:
        raise KeyError(
            f"no schema registered for step_id={step_id!r}; expected one of "
            f"{sorted(STEP_SCHEMAS.keys())}"
        )
    return STEP_SCHEMAS[step_id]


__all__ = [
    "ARTICLE_VII_TRACKING_SCHEMA",
    "INPUT_FRAME_SCHEMA",
    "JSON_SCHEMA_DIALECT",
    "MEMORY_LOGGER_CORRECTION_SCHEMA",
    "MEMORY_LOGGER_EVENT_SCHEMA",
    "PROCEDURE_STEP_OUTPUT_SCHEMA",
    "SCHEMA_VERSION",
    "STEP_1_OUTPUT_SCHEMA",
    "STEP_2_OUTPUT_SCHEMA",
    "STEP_3_OUTPUT_SCHEMA",
    "STEP_4_OUTPUT_SCHEMA",
    "STEP_5_OUTPUT_SCHEMA",
    "STEP_6_OUTPUT_SCHEMA",
    "STEP_7_OUTPUT_SCHEMA",
    "STEP_8_OUTPUT_SCHEMA",
    "STEP_9_OUTPUT_SCHEMA",
    "STEP_10_OUTPUT_SCHEMA",
    "STEP_11_OUTPUT_SCHEMA",
    "STEP_SCHEMAS",
    "schema_for",
]
