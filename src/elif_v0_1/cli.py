"""ELIF v0.1 CLI — operator-driven entry point.

Usage:
    elif run --case <case_id> --condition <a|b|c>
             [--procedure-version v1.0|v1.1]
             [--offline]
             [--max-llm-calls 22]
             [--results-dir <path>]

Reads the case's input frame from
    /home/dev/elif-lab/cases/<case_id>/input_frame.md
(if `--case` is the directory name) or accepts the path directly via the
`ELIF_CASES_DIR` environment variable override.

Prints the `RunReport` as JSON to stdout. Exit code matches RunReport.exit_code:
    0  — successful close
    10 — FrameInvalidError
    20 — GovernanceRefuseError
    30 — SchemaValidationError or LLMCallCapError
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import InputFrame
from .orchestration_runner import ProcedureRunner
from .run_context import RunContext, RunReport, StepOutputEnvelope

# Default cases directory; override with ELIF_CASES_DIR.
_DEFAULT_CASES_DIR: Path = Path("/home/dev/elif-lab/cases")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="elif",
        description="ELIF v0.1 procedure runner.",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_p = subparsers.add_parser(
        "run", help="Execute the 11-step procedure for a case."
    )
    run_p.add_argument(
        "--case",
        required=True,
        help="Case directory name under cases/, e.g. case_01_electroculture",
    )
    run_p.add_argument(
        "--condition",
        required=True,
        choices=("a", "b", "c"),
        help="Benchmark condition column",
    )
    run_p.add_argument(
        "--procedure-version",
        default="v1.0",
        choices=("v1.0", "v1.1"),
        help="Procedure version (v1.0 default; v1.1 not authorized in v0.1)",
    )
    run_p.add_argument(
        "--offline",
        action="store_true",
        help="Run in offline mode using bundled fixtures (no Anthropic call)",
    )
    run_p.add_argument(
        "--max-llm-calls",
        type=int,
        default=22,
        help="Per-run LLM call cap (operator §8.4 default: 22)",
    )
    run_p.add_argument(
        "--results-dir",
        type=str,
        default=None,
        help="Optional results directory for MemoryLogger persistence",
    )
    return parser


def _cases_dir() -> Path:
    """Return the cases directory; respects ELIF_CASES_DIR override."""
    override = os.environ.get("ELIF_CASES_DIR")
    if override:
        return Path(override)
    return _DEFAULT_CASES_DIR


def _load_input_frame(case_dir_name: str) -> InputFrame:
    """Load `cases/<case_dir_name>/input_frame.md` and lock it as InputFrame."""
    base = _cases_dir() / case_dir_name
    if not base.is_dir():
        raise FileNotFoundError(
            f"case directory not found: {base}"
        )
    frame_path = base / "input_frame.md"
    if not frame_path.is_file():
        raise FileNotFoundError(
            f"input_frame.md not found in {base}"
        )
    text = frame_path.read_text(encoding="utf-8")
    locked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return InputFrame(
        id=case_dir_name,
        text=text,
        locked_at_iso=locked_at,
        doctrinal_scope_tag=case_dir_name,
        companion_case="",
    )


def _envelope_to_dict(env: StepOutputEnvelope) -> Dict[str, Any]:
    return {
        "step_id": env.step_id,
        "committed_at_iso": env.committed_at_iso,
        "llm_calls_used": env.llm_calls_used,
        "time_box_status": env.time_box_status,
        "structured_output_dict": env.structured_output_dict,
    }


def _run_context_to_dict(ctx: RunContext) -> Dict[str, Any]:
    return dataclasses.asdict(ctx)


def _report_to_dict(report: RunReport) -> Dict[str, Any]:
    return {
        "run_context": _run_context_to_dict(report.run_context),
        "step_outputs": [
            _envelope_to_dict(env) for env in report.step_outputs
        ],
        "memory_logger_entries_written": report.memory_logger_entries_written,
        "exit_code": report.exit_code,
        "completed_at_iso": report.completed_at_iso,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "run":
        parser.print_help()
        return 0

    try:
        input_frame = _load_input_frame(args.case)
    except FileNotFoundError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 30

    runner = ProcedureRunner()
    results_dir = Path(args.results_dir) if args.results_dir else None
    report = runner.run(
        case_id=args.case,
        condition=args.condition,
        input_frame=input_frame,
        offline_mode=bool(args.offline),
        max_llm_calls=int(args.max_llm_calls),
        procedure_version=args.procedure_version,
        results_dir=results_dir,
    )
    print(json.dumps(_report_to_dict(report), indent=2, sort_keys=True))
    return int(report.exit_code)


if __name__ == "__main__":
    sys.exit(main())
