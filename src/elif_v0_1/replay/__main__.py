"""CLI smoke entry for the alpha replay harness.

Usage:
    python -m src.elif_v0_1.replay [--case CASE_ID] [--offline]

Default: replay all three cases in offline mode and print a per-case
verdict line + cohort verdict. This is the smoke surface for the alpha
acceptance gate; it does not write artifacts to disk.
"""

from __future__ import annotations

import argparse
import sys

from . import ALPHA_CASE_IDS, replay_all_cases, replay_case


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m src.elif_v0_1.replay",
        description="ELIF v0.1 alpha replay harness — fixture-driven smoke",
    )
    p.add_argument(
        "--case",
        choices=list(ALPHA_CASE_IDS),
        default=None,
        help="replay only this case; default: all three",
    )
    p.add_argument(
        "--offline",
        action="store_true",
        default=True,
        help="run in offline (fixture) mode; default and currently only mode",
    )
    return p


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    if args.case:
        result = replay_case(args.case, offline_mode=args.offline)
        print(
            f"[{result.case_id}] verdict={result.behavioral_acceptance_verdict} "
            f"similarity={result.structural_similarity_score:.2f} "
            f"runner_path={result.runner_path}"
        )
        for note in result.notes:
            print(f"  note: {note}")
        for missing in result.missing_behaviors:
            print(f"  missing: {missing}")
        return 0 if result.behavioral_acceptance_verdict in {"works", "partially"} else 1

    report = replay_all_cases(offline_mode=args.offline)
    for result in report.per_case:
        print(
            f"[{result.case_id}] verdict={result.behavioral_acceptance_verdict} "
            f"similarity={result.structural_similarity_score:.2f} "
            f"runner_path={result.runner_path}"
        )
    print(
        f"\ncohort_verdict={report.overall_verdict()} "
        f"generated_at={report.generated_at_iso} offline={report.offline_mode}"
    )
    overall = report.overall_verdict()
    return 0 if overall in {"works", "partially"} else 1


if __name__ == "__main__":
    sys.exit(main())
