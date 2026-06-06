"""
Serverless Entry Point for ELIF Engine.
This handler allows individual steps to be executed in a FaaS (Function-as-a-Service) 
environment like AWS Lambda or Google Cloud Functions.

IMPORTANT: This file does NOT modify the engine logic; it only unbundles the 
existing ProcedureRunner for stateless execution.
"""

import json
import os
from typing import Any, Dict, Optional
from pathlib import Path

# Import existing engine logic
from .orchestration_runner import ProcedureRunner
from .base import InputFrame
from .run_context import RunContext

def handle_step_request(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates a Serverless Function handler.
    Expected event body:
    {
        "step_id": "step_4",
        "case_id": "CASE_123",
        "condition": "c",
        "input_frame": {...},
        "prior_outputs": {...},
        "run_context_data": {...},
        "model_id": "sonnet",
        "offline_mode": false
    }
    """
    
    # 1. Rehydrate InputFrame
    frame_data = event.get("input_frame", {})
    input_frame = InputFrame(
        id=frame_data.get("id"),
        text=frame_data.get("text"),
        locked_at_iso=frame_data.get("locked_at_iso"),
        doctrinal_scope_tag=frame_data.get("doctrinal_scope_tag"),
        companion_case=frame_data.get("companion_case"),
        language_instruction=frame_data.get("language_instruction", "")
    )

    # 2. Rehydrate RunContext (the "memory" of the run)
    ctx_data = event.get("run_context_data", {})
    run_context = RunContext(
        case_id=event.get("case_id"),
        condition=event.get("condition", "c"),
        procedure_version=ctx_data.get("procedure_version", "v1.0"),
        offline_mode=event.get("offline_mode", False),
        max_llm_calls=ctx_data.get("max_llm_calls", 22),
        model_id=event.get("model_id", "sonnet"),
        started_at_iso=ctx_data.get("started_at_iso"),
        run_id=ctx_data.get("run_id"),
        language_instruction=ctx_data.get("language_instruction", "")
    )

    # 3. Instantiate Runner (Pure-Stateless)
    runner = ProcedureRunner()
    
    # 4. Initialize Components for THIS specific step
    # We use the existing logic to get context and components without modification
    _, components = runner.get_context_and_components(
        case_id=run_context.case_id,
        condition=run_context.condition,
        input_frame=input_frame,
        offline_mode=run_context.offline_mode,
        max_llm_calls=run_context.max_llm_calls,
        model_id=run_context.model_id,
        language_instruction=run_context.language_instruction
    )

    # 5. Execute the specific step
    step_id = event.get("step_id")
    prior_outputs = event.get("prior_outputs", {})
    
    print(f"[SERVERLESS] Executing {step_id} for Run {run_context.run_id}")
    
    payload, usage = runner.execute_step(
        step_id=step_id,
        run_context=run_context,
        components=components,
        input_frame=input_frame,
        prior_outputs=prior_outputs
    )

    return {
        "status": "success",
        "step_id": step_id,
        "payload": payload,
        "usage": usage,
        "run_id": run_context.run_id
    }
