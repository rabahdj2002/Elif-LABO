"""ELIF v0.1 alpha replay harness.

Purpose:
    Drive the v0.1 procedure against case_01 / case_02 / case_03 inputs in
    offline (fixture) mode and produce a structural acceptance report. This
    layer is the alpha acceptance gate: it answers the question "does the
    procedure produce output that is structurally comparable to the
    hand-authored Condition C reference?" rather than "is the text the same."

Design contract:
    * Reads case inputs from `cases/<case_id>/input_frame.md`.
    * Reads reference Condition C outputs from
      `results/<case_id_short>/condition_c_output.md`, where the short form
      strips the trailing prose token (e.g. `case_01_electroculture` ->
      `case_01`).
    * Attempts to run the orchestration runner with offline_mode=True. If
      the runner refuses (scaffold `NonSelfPropagationError`), the harness
      falls back to a direct per-component replay using the same offline
      fixtures. This preserves the contract that the alpha replay is
      runnable even while the runner is being implemented in parallel
      (decision 8.10: separate workstreams).
    * Compares structurally — count of axes / families / hypotheses / etc.
      and the presence of load-bearing closed-set tokens. Never does exact
      text equality against the reference markdown (the reference is
      hand-authored prose; fixtures emit structured JSON).
    * Returns a frozen `ReplayResult` per case + an `AcceptanceReport` per
      cohort, plus a CLI entry-point for the smoke test.

Public surface:
    replay_case(case_id, *, offline_mode=True) -> ReplayResult
    replay_all_cases(*, offline_mode=True)     -> AcceptanceReport

The harness DOES NOT mutate any reference artifact. It writes nothing to
disk by default; the orchestrator chooses where to persist reports.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from ..base import (
    ELIFError,
    InputFrame,
    NonSelfPropagationError,
)
from ..llm_adapter import reset_call_counter
from ..run_context import RunContext, RunReport, StepOutputEnvelope
from ..schemas import schema_for

# ---- Paths ----------------------------------------------------------------
_REPO_ROOT: Path = Path(__file__).resolve().parents[3]
_CASES_DIR: Path = _REPO_ROOT / "cases"
_RESULTS_DIR: Path = _REPO_ROOT / "results"

# ---- Closed-set verdicts ---------------------------------------------------
ACCEPTANCE_VERDICTS: Tuple[str, ...] = (
    "works",
    "partially",
    "missing",
    "blocked",
    "requires_redesign",
)

# Canonical case IDs the alpha cohort covers.
ALPHA_CASE_IDS: Tuple[str, ...] = (
    "case_01_electroculture",
    "case_02_policy_governance",
    "case_03_operational_organizational",
)


_CASE_TOKEN_RE = re.compile(r"(case_\d+)")


def _case_short(case_id: str) -> str:
    """Return the canonical `case_NN` short token from a case_id string."""
    match = _CASE_TOKEN_RE.search(case_id)
    if not match:
        raise ELIFError(
            f"case_id does not contain a `case_NN` token: {case_id!r}"
        )
    return match.group(1)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---- Frozen result dataclasses --------------------------------------------
@dataclass(frozen=True)
class ReplayResult:
    """Per-case replay result.

    Fields:
        case_id                       — full case id (e.g. case_01_electroculture)
        offline_mode                  — whether the replay ran in fixture mode
        run_report                    — `RunReport` produced by the runner or
                                        constructed by the per-component
                                        fallback (always populated)
        structural_similarity_score   — 0..1 — fraction of reference behaviors
                                        the replay reproduced
        missing_behaviors             — load-bearing behaviors present in
                                        reference but absent in replay
        unexpected_behaviors          — replay artifacts that diverge from
                                        the reference (additional non-equivalent
                                        structures); typically empty in offline
                                        mode but populated when fixtures drift
        behavioral_acceptance_verdict — closed-set in ACCEPTANCE_VERDICTS
        runner_path                   — "orchestration_runner" or
                                        "per_component_fallback"; surfaces the
                                        blocker honestly
        notes                         — free-text observations attached to the
                                        run for the report writer
    """

    case_id: str
    offline_mode: bool
    run_report: RunReport
    structural_similarity_score: float
    missing_behaviors: Tuple[str, ...] = field(default_factory=tuple)
    unexpected_behaviors: Tuple[str, ...] = field(default_factory=tuple)
    behavioral_acceptance_verdict: str = "blocked"
    runner_path: str = "per_component_fallback"
    notes: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.behavioral_acceptance_verdict not in ACCEPTANCE_VERDICTS:
            raise ValueError(
                "behavioral_acceptance_verdict must be in "
                f"{ACCEPTANCE_VERDICTS}; got {self.behavioral_acceptance_verdict!r}"
            )
        if not (0.0 <= self.structural_similarity_score <= 1.0):
            raise ValueError(
                "structural_similarity_score must be in [0,1]; got "
                f"{self.structural_similarity_score!r}"
            )


@dataclass(frozen=True)
class AcceptanceReport:
    """Cohort acceptance report — per-case ReplayResult tuple."""

    generated_at_iso: str
    offline_mode: bool
    per_case: Tuple[ReplayResult, ...]

    def overall_verdict(self) -> str:
        """Roll up per-case verdicts to a cohort verdict."""
        if not self.per_case:
            return "missing"
        verdicts = [r.behavioral_acceptance_verdict for r in self.per_case]
        if all(v == "works" for v in verdicts):
            return "works"
        if any(v == "requires_redesign" for v in verdicts):
            return "requires_redesign"
        if any(v == "blocked" for v in verdicts):
            return "blocked"
        if any(v == "missing" for v in verdicts):
            return "partially"
        return "partially"


# ---- Reference loading -----------------------------------------------------
def _load_input_frame(case_id: str) -> InputFrame:
    """Load the case input_frame.md into an InputFrame dataclass.

    The markdown is canonical operator-locked content. We read the verbatim
    body and synthesize the InputFrame metadata fields the procedure needs.
    """
    fp = _CASES_DIR / case_id / "input_frame.md"
    if not fp.is_file():
        raise ELIFError(f"input_frame.md not found: {fp}")
    text = fp.read_text(encoding="utf-8")
    return InputFrame(
        id=case_id,
        text=text,
        locked_at_iso="2026-05-28T00:00:00Z",
        doctrinal_scope_tag=_scope_tag_for(case_id),
        companion_case="",
    )


def _scope_tag_for(case_id: str) -> str:
    """Best-effort doctrinal scope tag per case (used downstream only)."""
    short = _case_short(case_id)
    return {
        "case_01": "scientific-evidential-ambiguity",
        "case_02": "policy-governance-bundle",
        "case_03": "operational-organizational-bundle",
    }.get(short, "alpha-replay")


def _reference_text(case_id: str) -> str:
    """Load reference Condition C markdown; empty string if absent."""
    fp = _RESULTS_DIR / _case_short(case_id) / "condition_c_output.md"
    if not fp.is_file():
        return ""
    return fp.read_text(encoding="utf-8")


def _load_fixture(step_id: str, case_id: str) -> Dict[str, Any]:
    """Load an offline fixture for a (step, case) pair."""
    step_n = int(step_id.split("_")[1])
    fixture_name = f"step_{step_n:02d}__{_case_short(case_id)}.json"
    fp = (
        _REPO_ROOT
        / "src"
        / "elif_v0_1"
        / "offline_fixtures"
        / fixture_name
    )
    if not fp.is_file():
        raise ELIFError(f"offline fixture not found: {fp}")
    return json.loads(fp.read_text(encoding="utf-8"))


# ---- Reference behavior extraction ----------------------------------------
# Behaviors are LOAD-BEARING structural signatures: Step 1 verdict equals
# `needs decomposition`, Step 2 emits >=2 axes, Step 9 verdict in
# {constrain, refuse, explicitly_abstain}, etc. These are the contract the
# v0.1 procedure must reproduce regardless of prose styling.

REFERENCE_BEHAVIORS: Tuple[Tuple[str, str], ...] = (
    ("step_1_verdict_present", "Step 1 emits a verdict in the closed set"),
    ("step_1_needs_decomposition", "Step 1 returns needs_decomposition"),
    ("step_2_axes_present", "Step 2 emits >= 1 axis"),
    ("step_2_axes_multiple", "Step 2 emits >= 2 axes"),
    ("step_2_families_per_axis_ge_2", "Each Step 2 axis carries >= 2 families"),
    ("step_3_assumptions_ge_2", "Step 3 surfaces >= 2 declarative assumptions"),
    ("step_4_hypotheses_present", "Step 4 emits >= 1 hypothesis"),
    ("step_4_distinguishing_predictions", "Each Step 4 hypothesis has a distinguishing prediction"),
    ("step_5_failure_conditions_present", "Step 5 emits failure conditions"),
    ("step_6_scales_ge_2", "Step 6 emits >= 2 scales"),
    ("step_6_cross_scale_relations_ge_1", "Step 6 emits >= 1 cross-scale relation"),
    ("step_7_trajectories_ge_1", "Step 7 emits >= 1 outside-frame trajectory"),
    ("step_8_stages_ge_1", "Step 8 emits >= 1 stage with continuation gate"),
    ("step_9_verdict_present", "Step 9 emits a closed-set verdict"),
    ("step_9_uncertainty_ge_1", "Step 9 names >= 1 unresolved uncertainty source"),
    ("step_10_operative_present", "Step 10 emits an operative list"),
    ("step_10_theoretical_present", "Step 10 emits a theoretical list"),
    ("step_11_entries_present", "Step 11 emits >= 1 memory logger entry"),
)


def _reference_signature(reference_text: str) -> Dict[str, bool]:
    """Extract structural behaviors from the reference markdown.

    The reference is prose; we apply load-bearing regex/string checks for
    each behavior so the comparison is deterministic.
    """
    sig: Dict[str, bool] = {key: False for key, _ in REFERENCE_BEHAVIORS}
    if not reference_text:
        return sig
    lower = reference_text.lower()

    # Step 1 — verdict
    if "step 1" in lower:
        sig["step_1_verdict_present"] = any(
            v in lower for v in ("valid", "invalid", "needs decomposition")
        )
        sig["step_1_needs_decomposition"] = (
            "needs decomposition" in lower or "needs_decomposition" in lower
        )

    # Step 2 — axes
    if "decomposition axis 1" in lower:
        sig["step_2_axes_present"] = True
        sig["step_2_axes_multiple"] = "decomposition axis 2" in lower
        # Heuristic: at least two **Family X — ...** markers per axis section.
        sig["step_2_families_per_axis_ge_2"] = (
            len(re.findall(r"\*\*family [a-z]", lower)) >= 4
        )

    # Step 3 — assumptions
    if "step 3" in lower:
        # Count numbered enumerated assumptions e.g. "1. The proposal...".
        enum = re.findall(r"\n\d+\.\s+", reference_text)
        sig["step_3_assumptions_ge_2"] = len(enum) >= 2

    # Step 4 — hypotheses
    if "step 4" in lower:
        sig["step_4_hypotheses_present"] = bool(
            re.search(r"\*\*h\d+\.\*\*", lower)
        )
        sig["step_4_distinguishing_predictions"] = (
            "distinguishing prediction" in lower
        )

    # Step 5 — failure conditions
    if "step 5" in lower:
        sig["step_5_failure_conditions_present"] = (
            "fails if" in lower or "failure condition" in lower
        )

    # Step 6 — scales + relations
    if "step 6" in lower:
        sig["step_6_scales_ge_2"] = lower.count("scale") >= 3
        sig["step_6_cross_scale_relations_ge_1"] = (
            "cross-scale" in lower or "cross scale" in lower
        )

    # Step 7 — trajectories
    if "step 7" in lower:
        sig["step_7_trajectories_ge_1"] = (
            "outside-original-frame" in lower
            or "outside original frame" in lower
            or "trajectory" in lower
        )

    # Step 8 — stages
    if "step 8" in lower:
        sig["step_8_stages_ge_1"] = (
            "continuation gate" in lower or "stage" in lower
        )

    # Step 9 — verdict + uncertainty
    if "step 9" in lower:
        sig["step_9_verdict_present"] = any(
            v in lower for v in ("constrain", "refuse", "explicitly abstain")
        )
        sig["step_9_uncertainty_ge_1"] = "uncertainty" in lower

    # Step 10 — operative/theoretical split (the reference Step 10 in case_01)
    if "step 10" in lower:
        sig["step_10_operative_present"] = "operative" in lower
        sig["step_10_theoretical_present"] = "theoretical" in lower
    elif "step 11" in lower and (
        "operative" in lower and "theoretical" in lower
    ):
        # Older numbering used Step 11 for op/theoretical split in some cases.
        sig["step_10_operative_present"] = True
        sig["step_10_theoretical_present"] = True

    # Step 11 — memory logger entries
    if "memory logger" in lower or "entry 1" in lower or "step 11" in lower:
        sig["step_11_entries_present"] = (
            "entry 1" in lower
            or "[judgment_act]" in lower
            or "[pattern_engaged]" in lower
            or "[capacity_change]" in lower
        )

    return sig


# ---- Replay step content signature -----------------------------------------
def _replay_signature(step_outputs: Mapping[str, Dict[str, Any]]) -> Dict[str, bool]:
    """Extract structural behaviors from the replay step outputs.

    `step_outputs` is keyed by step_id ("step_1", ..., "step_11"); each
    value is the parsed structured output dict (matches the per-step schema).
    """
    sig: Dict[str, bool] = {key: False for key, _ in REFERENCE_BEHAVIORS}

    s1 = step_outputs.get("step_1") or {}
    verdict_1 = s1.get("verdict")
    if isinstance(verdict_1, str):
        sig["step_1_verdict_present"] = verdict_1 in (
            "valid",
            "invalid",
            "needs_decomposition",
        )
        sig["step_1_needs_decomposition"] = verdict_1 == "needs_decomposition"

    s2 = step_outputs.get("step_2") or {}
    axes = s2.get("axes") or []
    if isinstance(axes, list):
        sig["step_2_axes_present"] = len(axes) >= 1
        sig["step_2_axes_multiple"] = len(axes) >= 2
        sig["step_2_families_per_axis_ge_2"] = all(
            isinstance(a, Mapping)
            and isinstance(a.get("families"), list)
            and len(a["families"]) >= 2
            for a in axes
        ) and len(axes) >= 1

    s3 = step_outputs.get("step_3") or {}
    assumptions = s3.get("assumptions") or []
    if isinstance(assumptions, list):
        sig["step_3_assumptions_ge_2"] = len(assumptions) >= 2

    s4 = step_outputs.get("step_4") or {}
    hyps = s4.get("hypotheses") or []
    if isinstance(hyps, list):
        sig["step_4_hypotheses_present"] = len(hyps) >= 1
        sig["step_4_distinguishing_predictions"] = all(
            isinstance(h, Mapping) and h.get("distinguishing_prediction")
            for h in hyps
        ) and len(hyps) >= 1

    s5 = step_outputs.get("step_5") or {}
    failures = s5.get("failure_conditions") or []
    if isinstance(failures, list):
        sig["step_5_failure_conditions_present"] = len(failures) >= 1

    s6 = step_outputs.get("step_6") or {}
    scales = s6.get("scales") or []
    relations = s6.get("cross_scale_relations") or []
    if isinstance(scales, list):
        sig["step_6_scales_ge_2"] = len(set(scales)) >= 2
    if isinstance(relations, list):
        sig["step_6_cross_scale_relations_ge_1"] = len(relations) >= 1

    s7 = step_outputs.get("step_7") or {}
    trajectories = s7.get("trajectories") or []
    if isinstance(trajectories, list):
        sig["step_7_trajectories_ge_1"] = len(trajectories) >= 1

    s8 = step_outputs.get("step_8") or {}
    stages = s8.get("stages") or []
    if isinstance(stages, list):
        sig["step_8_stages_ge_1"] = len(stages) >= 1

    s9 = step_outputs.get("step_9") or {}
    v9 = s9.get("verdict")
    if isinstance(v9, str):
        sig["step_9_verdict_present"] = v9 in (
            "constrain",
            "refuse",
            "explicitly_abstain",
        )
    uncertainty = s9.get("unresolved_uncertainty_sources") or []
    if isinstance(uncertainty, list):
        sig["step_9_uncertainty_ge_1"] = len(uncertainty) >= 1

    s10 = step_outputs.get("step_10") or {}
    operative = s10.get("operative")
    theoretical = s10.get("theoretical")
    sig["step_10_operative_present"] = isinstance(operative, list) and len(operative) >= 1
    sig["step_10_theoretical_present"] = isinstance(theoretical, list) and len(theoretical) >= 1

    s11 = step_outputs.get("step_11") or {}
    entries = s11.get("entries") or []
    if isinstance(entries, list):
        sig["step_11_entries_present"] = len(entries) >= 1

    return sig


# ---- Per-component fallback path -------------------------------------------
def _per_component_replay(case_id: str) -> Dict[str, Dict[str, Any]]:
    """Run the procedure by loading per-step fixtures directly.

    Used when the orchestration runner is unavailable (scaffold-stage refusal
    or in-progress implementation). Honors decision 8.8: offline fixture mode
    is the alpha truth-source. Honors decision 8.9: each step output is loaded
    independently — no inter-step state propagates beyond the structured
    output the prior step committed.
    """
    step_outputs: Dict[str, Dict[str, Any]] = {}
    for step_id in (
        "step_1",
        "step_2",
        "step_3",
        "step_4",
        "step_5",
        "step_6",
        "step_7",
        "step_8",
        "step_9",
        "step_10",
        "step_11",
    ):
        try:
            payload = _load_fixture(step_id, case_id)
        except ELIFError:
            # Missing fixture is honest data, not a fatal halt; carry forward
            # as an empty dict and let signature extraction record the miss.
            payload = {}
        step_outputs[step_id] = payload
    return step_outputs


def _envelopes_from_step_outputs(
    step_outputs: Mapping[str, Dict[str, Any]],
) -> Tuple[StepOutputEnvelope, ...]:
    """Wrap raw per-step dicts into StepOutputEnvelopes for the run report."""
    ts = _utc_now_iso()
    envs: List[StepOutputEnvelope] = []
    for step_id, content in step_outputs.items():
        envs.append(
            StepOutputEnvelope(
                step_id=step_id,
                content=content,
                committed_at_iso=ts,
                llm_calls_used=1 if content else 0,
                time_box_status="within_budget",
                structured_output_dict=dict(content) if isinstance(content, dict) else {},
            )
        )
    return tuple(envs)


# ---- Verdict synthesis -----------------------------------------------------
def _synthesize_verdict(
    similarity: float,
    missing: Tuple[str, ...],
    runner_path: str,
    blocker_present: bool,
) -> str:
    """Map (similarity, missing, runner_path) to acceptance verdict."""
    if blocker_present and runner_path == "per_component_fallback":
        # Runner is the load-bearing integration; if we had to fall back,
        # the alpha is at best `partially` regardless of similarity.
        if similarity >= 0.85:
            return "partially"
        if similarity >= 0.5:
            return "partially"
        return "blocked"
    if similarity >= 0.9 and not missing:
        return "works"
    if similarity >= 0.7:
        return "partially"
    if similarity >= 0.4:
        return "missing"
    if similarity > 0.0:
        return "requires_redesign"
    return "blocked"


# ---- Public surface --------------------------------------------------------
def replay_case(
    case_id: str,
    *,
    offline_mode: bool = True,
) -> ReplayResult:
    """Replay one case and return a frozen ReplayResult.

    Always returns a result. Internal failures of the runner are reported
    via `runner_path="per_component_fallback"` + notes; only structural-shape
    invariants (e.g. missing input_frame.md) raise.
    """
    if case_id not in ALPHA_CASE_IDS:
        raise ELIFError(
            f"alpha replay supports {ALPHA_CASE_IDS}; got {case_id!r}"
        )

    input_frame = _load_input_frame(case_id)
    run_context = RunContext(
        case_id=case_id,
        condition="c",
        procedure_version="v1.0",
        offline_mode=offline_mode,
        max_llm_calls=22,
        started_at_iso=_utc_now_iso(),
        run_id=f"alpha_replay__{_case_short(case_id)}__{_utc_now_iso()}",
    )

    # Reset the per-process LLM cap counter so cohort-level replays of all
    # three cases don't compound counts across runs. Decision §8.4 makes the
    # cap per-run, not per-process.
    reset_call_counter()

    runner_path = "orchestration_runner"
    notes: List[str] = []
    step_outputs: Dict[str, Dict[str, Any]] = {}
    blocker_present = False

    try:
        # Lazy import — the runner module exists but its run() may raise.
        from ..orchestration_runner import ProcedureRunner

        runner = ProcedureRunner()
        report = runner.run(
            case_id=case_id,
            condition="c",
            input_frame=input_frame,
            offline_mode=offline_mode,
            max_llm_calls=22,
            procedure_version="v1.0",
        )
        # The legacy RunReport shape from the scaffold may differ; if it
        # has a `step_outputs` tuple, materialize it.
        outputs = getattr(report, "step_outputs", ()) or ()
        for env in outputs:
            sid = getattr(env, "step_id", None)
            content = getattr(env, "structured_output_dict", None) or getattr(env, "content", None)
            if sid and isinstance(content, dict):
                step_outputs[sid] = content
        if not step_outputs:
            # Runner returned but produced no step outputs we can use.
            runner_path = "per_component_fallback"
            blocker_present = True
            notes.append(
                "orchestration_runner returned but produced no usable step outputs; "
                "falling back to per-component fixture replay"
            )
            step_outputs = _per_component_replay(case_id)
    except NonSelfPropagationError as exc:
        runner_path = "per_component_fallback"
        blocker_present = True
        notes.append(
            f"orchestration_runner refused (scaffold stage): {exc}; "
            "falling back to per-component fixture replay"
        )
        step_outputs = _per_component_replay(case_id)
    except Exception as exc:  # noqa: BLE001 — wide net to keep harness alive
        runner_path = "per_component_fallback"
        blocker_present = True
        notes.append(
            f"orchestration_runner raised {type(exc).__name__}: {exc}; "
            "falling back to per-component fixture replay"
        )
        step_outputs = _per_component_replay(case_id)

    # Construct a RunReport from whatever we have.
    envelopes = _envelopes_from_step_outputs(step_outputs)
    run_report = RunReport(
        run_context=run_context,
        step_outputs=envelopes,
        memory_logger_entries_written=len(
            (step_outputs.get("step_11") or {}).get("entries", []) or []
        ),
        exit_code=0 if not blocker_present else 1,
        completed_at_iso=_utc_now_iso(),
    )

    # Compare structurally.
    ref_text = _reference_text(case_id)
    ref_sig = _reference_signature(ref_text)
    replay_sig = _replay_signature(step_outputs)

    total_expected = sum(1 for v in ref_sig.values() if v)
    matched = sum(
        1
        for key, expected in ref_sig.items()
        if expected and replay_sig.get(key)
    )
    similarity = (matched / total_expected) if total_expected else 0.0

    missing = tuple(
        desc
        for (key, desc) in REFERENCE_BEHAVIORS
        if ref_sig.get(key) and not replay_sig.get(key)
    )
    unexpected = tuple(
        desc
        for (key, desc) in REFERENCE_BEHAVIORS
        if replay_sig.get(key) and not ref_sig.get(key)
    )

    verdict = _synthesize_verdict(similarity, missing, runner_path, blocker_present)

    if not ref_text:
        notes.append(
            f"reference Condition C output not found at "
            f"results/{_case_short(case_id)}/condition_c_output.md"
        )

    return ReplayResult(
        case_id=case_id,
        offline_mode=offline_mode,
        run_report=run_report,
        structural_similarity_score=round(similarity, 4),
        missing_behaviors=missing,
        unexpected_behaviors=unexpected,
        behavioral_acceptance_verdict=verdict,
        runner_path=runner_path,
        notes=tuple(notes),
    )


def replay_all_cases(*, offline_mode: bool = True) -> AcceptanceReport:
    """Run replay_case across all alpha cases and return the cohort report."""
    per_case = tuple(
        replay_case(case_id, offline_mode=offline_mode)
        for case_id in ALPHA_CASE_IDS
    )
    return AcceptanceReport(
        generated_at_iso=_utc_now_iso(),
        offline_mode=offline_mode,
        per_case=per_case,
    )


__all__ = [
    "ACCEPTANCE_VERDICTS",
    "ALPHA_CASE_IDS",
    "REFERENCE_BEHAVIORS",
    "ReplayResult",
    "AcceptanceReport",
    "replay_case",
    "replay_all_cases",
]
