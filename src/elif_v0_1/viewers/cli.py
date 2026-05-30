"""CLI entrypoint for the four V1 viewers.

Read-only. No LLM calls. No side effects beyond stdout / optional file
write of the rendered Markdown.

Usage:
    python -m elif_v0_1.viewers.cli decision-room --run-report <path>
    python -m elif_v0_1.viewers.cli exploration --run-report <path>
    python -m elif_v0_1.viewers.cli object-drift --run-report <path>
            [--input-frame <path>] [--no-reading-lens]
    python -m elif_v0_1.viewers.cli memory-timeline --case-id <id> --jsonl <path>
    python -m elif_v0_1.viewers.cli offline-vs-live --offline <path> --live <path>
    python -m elif_v0_1.viewers.cli article-vii --jsonl <path> [--jsonl <path> ...]

Optional `--out <path>` writes the Markdown to a file instead of stdout.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import (
    render_article_vii_observations,
    render_decision_room,
    render_exploration_lens,
    render_memory_timeline,
    render_object_chain,
    render_offline_vs_live_diff,
    render_replay_table,
)


def _load_report(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _emit(rendered: str, out_path: Path | None) -> None:
    if out_path is None:
        sys.stdout.write(rendered + "\n")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="elif-viewer",
        description=(
            "Read-only V1 viewers over existing ELIF substrate artifacts. "
            "Reveal, do not extend. See notes/elif_v1_viewer_audit_and_spec.md."
        ),
    )
    sub = p.add_subparsers(dest="command", required=True)

    dr = sub.add_parser("decision-room", help="Render Step 9/10/11 from a RunReport.")
    dr.add_argument("--run-report", type=Path, required=True)
    dr.add_argument("--out", type=Path, default=None)

    el = sub.add_parser("exploration", help="Render Exploration Lens (5 territories).")
    el.add_argument("--run-report", type=Path, required=True)
    el.add_argument("--out", type=Path, default=None)

    od = sub.add_parser("object-drift", help="Render Step 1→9 object chain.")
    od.add_argument("--run-report", type=Path, required=True)
    od.add_argument("--input-frame", type=Path, default=None)
    od.add_argument(
        "--no-reading-lens",
        action="store_true",
        help="Strict-minimum mode: omit constant reading-lens annotations.",
    )
    od.add_argument("--out", type=Path, default=None)

    mt = sub.add_parser("memory-timeline", help="Render MemoryLogger JSONL events.")
    mt.add_argument("--case-id", required=True)
    mt.add_argument("--jsonl", type=Path, required=True)
    mt.add_argument("--out", type=Path, default=None)

    ol = sub.add_parser(
        "offline-vs-live", help="Render per-field diff of offline vs live runs."
    )
    ol.add_argument("--offline", type=Path, required=True)
    ol.add_argument("--live", type=Path, required=True)
    ol.add_argument("--out", type=Path, default=None)

    av = sub.add_parser(
        "article-vii", help="Render capacity_change events across JSONLs."
    )
    av.add_argument("--jsonl", type=Path, action="append", required=True)
    av.add_argument("--out", type=Path, default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "decision-room":
        rendered = render_decision_room(_load_report(args.run_report))
    elif args.command == "exploration":
        rendered = render_exploration_lens(_load_report(args.run_report))
    elif args.command == "object-drift":
        rendered = render_object_chain(
            _load_report(args.run_report),
            input_frame_path=args.input_frame,
            with_reading_lens=not args.no_reading_lens,
        )
    elif args.command == "memory-timeline":
        rendered = render_memory_timeline(args.case_id, args.jsonl)
    elif args.command == "offline-vs-live":
        rendered = render_offline_vs_live_diff(
            _load_report(args.offline),
            _load_report(args.live),
        )
    elif args.command == "article-vii":
        rendered = render_article_vii_observations(args.jsonl)
    else:
        raise SystemExit(f"unknown command: {args.command!r}")

    _emit(rendered, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
