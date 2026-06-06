"""ELIF v0.1 LLM adapter — single frontier-LLM call boundary.

Per `notes/elif_v0_1_build_plan.md` §1.2: one adapter file, no multi-family
yet. Per Step 8 decision package §8.1: model = `claude-3-5-sonnet-20240620`.
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
        - issues an API call to DeepSeek (OpenAI-compatible) with `response_format`
          enforced for JSON mode.
        - requires `ELIF_DEEPSEEK_API_KEY` in the environment
        - raises `LLMAdapterError` on any transport / parsing failure
    * Both modes raise `LLMCallCapError` BEFORE attempting the call if
      `_call_counter() + 1 > max_calls`.

This module ships with NO DeepSeek/OpenAI SDK hard dependency. The SDK is imported
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
from .model_registry import MODEL_REGISTRY, resolve_model_id

# ---- Model + paths ---------------------------------------------------------
# Operator-approved switch to DeepSeek 2026-06-06.
DEFAULT_MODEL_ID: str = MODEL_REGISTRY["deepseek-reasoner"]

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


def _call_anthropic(
    prompt: str,
    output_schema: Dict[str, Any],
    *,
    model_id: str,
) -> Dict[str, Any]:
    """Issue an Anthropic API call and return the parsed JSON output."""
    api_key = os.environ.get("ELIF_ANTHROPIC_API_KEY")
    if not api_key:
        raise LLMAdapterError(
            "offline_mode=False requires ELIF_ANTHROPIC_API_KEY in environment"
        )
    try:
        import anthropic
    except ImportError as exc:
        raise LLMAdapterError(
            "anthropic SDK not installed; pip install anthropic"
        ) from exc

    client = anthropic.Anthropic(api_key=api_key)
    
    # We include the schema in the system prompt
    system_prompt = (
        "You are a specialized ELIF cognitive component tasked with high-fidelity, extreme-depth reasoning. "
        "ELIF demands unparalleled architectural complexity and semantic density. "
        "Your response MUST be a single valid JSON object strictly matching this schema:\n"
        f"{json.dumps(output_schema)}\n"
        "### DOCTRINAL DEPTH REQUIREMENTS:\n"
        "1. EXHAUSTIVE ANALYSIS: In every free-text field, provide multi-layered, highly detailed reasoning. Avoid brevity.\n"
        "2. SEMANTIC DENSITY: Use precise, high-information terminology. Do not summarize or simplify.\n"
        "3. REASONING TRACE: Fully expose the logic behind every decision or object created.\n"
        "4. JSON FORMAT: Return ONLY the JSON object. Do not include markdown blocks or preamble."
    )

    try:
        # Sonnet 3.5/4.5 is very good at JSON if you pre-fill the opening brace
        # but for simplicity we'll just use the standard call here.
        response = client.messages.create(
            model=model_id,
            max_tokens=8192,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
    except Exception as exc:
        raise LLMAdapterError(f"Anthropic API call failed: {exc}") from exc

    # Usage tracking
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    complete_structured.last_usage = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "model_id": model_id
    }

    raw_content = response.content[0].text
    try:
        # Some versions of Claude might include markdown blocks, let's strip if present
        if raw_content.strip().startswith("```json"):
            raw_content = raw_content.strip().replace("```json", "").replace("```", "").strip()
        
        payload = json.loads(raw_content)
        if not isinstance(payload, dict):
            raise LLMAdapterError("Anthropic returned valid JSON but it is not an object")
        return payload
    except json.JSONDecodeError as exc:
        raise LLMAdapterError(f"Anthropic response was not valid JSON: {raw_content[:200]}...") from exc


# ---- Live (DeepSeek) branch ----------------------------------------------
def _call_deepseek_json_mode(
    prompt: str,
    output_schema: Dict[str, Any],
    *,
    model_id: str,
) -> Dict[str, Any]:
    """Issue a DeepSeek API call and return the parsed JSON output.

    Uses DeepSeek's OpenAI-compatible endpoint with json_mode enabled.
    """
    api_key = os.environ.get("ELIF_DEEPSEEK_API_KEY")
    if not api_key:
        raise LLMAdapterError(
            "offline_mode=False requires ELIF_DEEPSEEK_API_KEY in environment"
        )
    try:
        import openai
    except ImportError as exc:
        raise LLMAdapterError(
            "openai SDK not installed; either `pip install openai` "
            "or use offline_mode=True"
        ) from exc

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    # Wrap the prompt to ensure it understands the JSON requirement
    system_prompt = (
        "You are a specialized ELIF cognitive component tasked with high-fidelity, extreme-depth reasoning. "
        "ELIF demands unparalleled architectural complexity and semantic density. "
        "Your response MUST be a single valid JSON object strictly matching this schema:\n"
        f"{json.dumps(output_schema)}\n"
        "### DOCTRINAL DEPTH REQUIREMENTS:\n"
        "1. EXHAUSTIVE ANALYSIS: In every free-text field, provide multi-layered, highly detailed reasoning. Avoid brevity.\n"
        "2. SEMANTIC DENSITY: Use precise, high-information terminology. Do not summarize or simplify.\n"
        "3. REASONING TRACE: Fully expose the logic behind every decision or object created.\n"
        "4. JSON FORMAT: Return ONLY the JSON object. Do not include markdown blocks (```json) or preamble."
    )

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=8192,
            temperature=0.6 # Increased for deeper reasoning exploration in R1
        )
    except Exception as exc:
        raise LLMAdapterError(f"DeepSeek API call failed: {exc}") from exc

    # Usage tracking
    input_tokens = getattr(response.usage, "prompt_tokens", 0)
    output_tokens = getattr(response.usage, "completion_tokens", 0)
    complete_structured.last_usage = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "model_id": model_id
    }

    raw_content = response.choices[0].message.content or ""
    try:
        payload = json.loads(raw_content)
        if not isinstance(payload, dict):
            raise LLMAdapterError("DeepSeek returned valid JSON but it is not an object")
        return payload
    except json.JSONDecodeError as exc:
        raise LLMAdapterError(f"DeepSeek response was not valid JSON: {raw_content[:200]}...") from exc

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
        active_id = resolve_model_id(model_id or DEFAULT_MODEL_ID)
        
        # Branch based on model prefix
        if "claude" in active_id:
            payload = _call_anthropic(
                prompt,
                output_schema,
                model_id=active_id,
            )
        else:
            payload = _call_deepseek_json_mode(
                prompt,
                output_schema,
                model_id=active_id,
            )

    validate_against_schema(payload, output_schema)
    return payload


__all__ = [
    "DEFAULT_MODEL_ID",
    "complete_structured",
    "reset_call_counter",
    "validate_against_schema",
]
