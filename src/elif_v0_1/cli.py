"""ELIF v0.1 CLI — scaffold entry point.

Usage:
    elif run --case <id> --condition <a|b|c> [--procedure-version v1.0|v1.1]

SCAFFOLD: prints a notice and exits 0. No procedure executes; no state
is written. Operator build authorization is required to wire this to
ProcedureRunner.run().
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="elif",
        description="ELIF v0.1 scaffold CLI (not implemented).",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_p = subparsers.add_parser("run", help="Run a case (scaffold).")
    run_p.add_argument("--case", required=True, help="Case ID")
    run_p.add_argument(
        "--condition",
        required=True,
        choices=("a", "b", "c"),
        help="Benchmark condition",
    )
    run_p.add_argument(
        "--procedure-version",
        default="v1.0",
        choices=("v1.0", "v1.1"),
        help="Procedure version to operate under",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    print("ELIF v0.1 scaffold — not implemented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
