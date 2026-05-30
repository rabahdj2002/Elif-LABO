"""ELIF v0.1 LLM adapter — single frontier-LLM call boundary.

Per `notes/elif_v0_1_build_plan.md` §1.2: one adapter file, no multi-family
yet. Per Step 8 decision package §8.1: model = `claude-sonnet-4-6`.
Per §8.4: per-run cost cap implemented as `max_calls` ceiling (default 22).
Per §8.8: offline fixture mode is shipped in v0.1; fixtures are deterministic.
Per §8.9: each LLM call starts fresh (no sub-behavior state retention).

Public surface:
    complete_structured(
        prompt: str,
        output_schema: dict,
        *,
        max_calls: int,
        offline_mode: bool = False,
        offline_fixture_id: str = "",
    ) -> dict

Behavioral contract:
    * offline_mode=True
        - loads `offline_fixtures/<fixture_id>.json` deterministically
        - validates the loaded fixture against `output_schema` (if shape can be
          validated — see `validate_against_schema`)
        - never makes a network call
        - still consumes one call slot from the per-process counter so that
          cap-exhaustion tests work identically online and offline
    * offline_mode=False
        - issues an Anthropic tool-use call with `output_schema` as
          `input_schema` of a single declared tool, forces the tool, and
          returns the parsed tool input as a dict
        - requires `ELIF_ANTHROPIC_API_KEY` in the environment
        - raises `LLMAdapterError` on any transport / parsing failure
    * Both modes raise `LLMCallCapError` BEFORE attempting the call if
      `_call_counter() + 1 > max_calls`.

This module ships with NO Anthropic SDK hard dependency. The SDK is imported
lazily inside the live branch so that offline mode works on any machine.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, Optional

from .base import (
    LLMAdapterError,
    LLMCallCapError,
    SchemaValidationError,
)

# ---- Model + paths ---------------------------------------------------------
# Operator-approved per Step 8 §8.1.
DEFAULT_MODEL_ID: str = "claude-sonnet-4-6"

# Tool name used in tool-use forcing. Single tool; deterministic.
_STRUCTURED_TOOL_NAME: str = "emit_structured_output"

_FIXTURES_DIR: Path = Path(__file__).resolve().parent / "offline_fixtures"


# ---- Per-process call counter ---------------------------------------------
# The counter is process-global on purpose: the per-run cap is enforced at
# the orchestrator level, and tests reset it between runs via `reset_call_counter`.
_call_counter_lock = threading.Lock()
_call_counter_value: int = 0


def _call_counter() -> int:
    """Return the current call count (process-scoped)."""
    with _call_counter_lock:
        return _call_counter_value


def _increment_call_counter() -> int:
    """Atomic increment; returns the new value."""
    global _call_counter_value
    with _call_counter_lock:
        _call_counter_value += 1
        return _call_counter_value


def reset_call_counter() -> None:
    """Reset the per-process call counter to 0.

    Intended for: test setup, new run boundary. Idempotent.
    """
    global _call_counter_value
    with _call_counter_lock:
        _call_counter_value = 0


# ---- Schema validation -----------------------------------------------------
def validate_against_schema(payload: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """Validate `payload` against `schema`.

    If the `jsonschema` package is installed we use Draft 2020-12. Otherwise
    we do a structural fallback: required keys present, type=object honored.
    Drift raises `SchemaValidationError` rather than `jsonschema`-native errors
    so callers depend on a single error type.
    """
    try:
        import jsonschema  # type: ignore

        try:
            jsonschema.validate(payload, schema)
            return
        except Exception as exc:  # jsonschema.ValidationError or schema error
            raise SchemaValidationError(str(exc)) from exc
    except ImportError:
        pass

    # Fallback: structural checks only.
    if not isinstance(payload, dict):
        raise SchemaValidationError(
            f"payload must be a dict; got {type(payload).__name__}"
        )
    if schema.get("type") == "object" and not isinstance(payload, dict):
        raise SchemaValidationError("schema declares type=object; payload is not")
    required = schema.get("required") or []
    missing = [k for k in required if k not in payload]
    if missing:
        raise SchemaValidationError(
            f"payload missing required keys: {missing}"
        )


# ---- Offline fixture loader -----------------------------------------------
def _load_offline_fixture(fixture_id: str) -> Dict[str, Any]:
    """Load `offline_fixtures/<fixture_id>.json` deterministically.

    `fixture_id` is the bare stem (no extension, no path). The function
    refuses path-escaping fixture ids and missing files with
    `LLMAdapterError`.
    """
    if not fixture_id:
        raise LLMAdapterError(
            "offline_mode=True requires a non-empty offline_fixture_id"
        )
    if "/" in fixture_id or "\\" in fixture_id or ".." in fixture_id:
        raise LLMAdapterError(
            f"offline_fixture_id must be a bare stem; got {fixture_id!r}"
        )
    fixture_path = _FIXTURES_DIR / f"{fixture_id}.json"
    if not fixture_path.is_file():
        raise LLMAdapterError(
            f"offline fixture not found: {fixture_path}"
        )
    try:
        with fixture_path.open("r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except json.JSONDecodeError as exc:
        raise LLMAdapterError(
            f"offline fixture is not valid JSON: {fixture_path} ({exc})"
        ) from exc
    if not isinstance(payload, dict):
        raise LLMAdapterError(
            f"offline fixture must be a JSON object: {fixture_path}"
        )
    return payload


# ---- Live (Anthropic) branch ----------------------------------------------
def _call_anthropic_tool_use(
    prompt: str,
    output_schema: Dict[str, Any],
    *,
    model_id: str,
) -> Dict[str, Any]:
    """Issue a tool-use call and return the parsed tool input.

    The schema is supplied as `input_schema` of a single forced tool;
    Anthropic guarantees the model emits a tool_use block whose `input`
    matches the schema. We parse that input and return it as a dict.
    """
    # ELIF reads its own dedicated env var so its credentials are isolated
    # from the OpenStudyGo supervisor's `OPENSTUDYGO_LLM_API_KEY_ANTHROPIC`
    # pool. Operator directive 2026-05-30.
    api_key = os.environ.get("ELIF_ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMAdapterError(
            "offline_mode=False requires ELIF_ANTHROPIC_API_KEY in environment"
        )
    try:
        # Lazy import: SDK must not be required in offline mode.
        import anthropic  # type: ignore
    except ImportError as exc:
        raise LLMAdapterError(
            "anthropic SDK not installed; either `pip install anthropic` "
            "or use offline_mode=True"
        ) from exc

    client = anthropic.Anthropic(api_key=api_key)
    tool = {
        "name": _STRUCTURED_TOOL_NAME,
        "description": (
            "Emit the structured output for this ELIF v0.1 procedure step. "
            "Populate every required field. Do not include keys not in the schema."
        ),
        "input_schema": output_schema,
    }
    try:
        message = client.messages.create(  # type: ignore[attr-defined]
            model=model_id,
            max_tokens=4096,
            tools=[tool],
            tool_choice={"type": "tool", "name": _STRUCTURED_TOOL_NAME},
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        raise LLMAdapterError(f"anthropic API call failed: {exc}") from exc

    # Find the tool_use block; pull its `input`.
    content_blocks = getattr(message, "content", None) or []
    for block in content_blocks:
        block_type = getattr(block, "type", None)
        if block_type == "tool_use":
            payload = getattr(block, "input", None)
            if not isinstance(payload, dict):
                raise LLMAdapterError(
                    "tool_use block did not contain a dict input"
                )
            return payload
    raise LLMAdapterError(
        "model response contained no tool_use block; refusing to guess shape"
    )


# ---- Public surface --------------------------------------------------------
def complete_structured(
    prompt: str,
    output_schema: Dict[str, Any],
    *,
    max_calls: int,
    offline_mode: bool = False,
    offline_fixture_id: str = "",
    model_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Single LLM call boundary for ELIF v0.1.

    See module docstring for the full contract. Returns the parsed JSON
    dict in both modes; raises `LLMCallCapError`, `LLMAdapterError`, or
    `SchemaValidationError` on the documented failure modes.
    """
    if not isinstance(max_calls, int) or max_calls < 1:
        raise LLMAdapterError(
            f"max_calls must be a positive int; got {max_calls!r}"
        )
    if not isinstance(output_schema, dict):
        raise LLMAdapterError("output_schema must be a dict")
    if not isinstance(prompt, str):
        raise LLMAdapterError("prompt must be a str")

    # Cap check BEFORE consuming a slot. Operator §8.4: hard halt.
    current = _call_counter()
    if current + 1 > max_calls:
        raise LLMCallCapError(
            f"LLM call cap exceeded: already used {current}/{max_calls}"
        )
    _increment_call_counter()

    if offline_mode:
        payload = _load_offline_fixture(offline_fixture_id)
    else:
        payload = _call_anthropic_tool_use(
            prompt,
            output_schema,
            model_id=model_id or DEFAULT_MODEL_ID,
        )

    validate_against_schema(payload, output_schema)
    return payload


__all__ = [
    "DEFAULT_MODEL_ID",
    "complete_structured",
    "reset_call_counter",
    "validate_against_schema",
]
