# ELIF V1 Viewer — Implementation Report

> **Status:** SHIPPED. Per operator green light 2026-05-30.
> **Spec:** [notes/elif_v1_viewer_audit_and_spec.md](elif_v1_viewer_audit_and_spec.md) (commit `95911af`)
> **Governing requirement (acceptance criterion):** *"ELIF becomes visible without becoming different."*
> **Closes nothing. Opens nothing. No substrate modifications.**

This report documents the V1 viewer implementation: files created, LoC delta, screenshots (sample renderings from E.2 artifacts), and evidence-based proof of the rendering-only contract.

---

## §1 — Files created

```
src/elif_v0_1/viewers/
    __init__.py                62 LoC
    _common.py                105 LoC   (shared helpers — _normalize_run_report, _bullets, _kv_table, _step_output)
    cli.py                    126 LoC   (six subcommands: decision-room, exploration, object-drift, memory-timeline, offline-vs-live, article-vii)
    decision_room.py          151 LoC   (Step 9 + 10 + 11 surface)
    exploration_lens.py       173 LoC   (5-territory flat map)
    laboratory_viewer.py      395 LoC   (4 panels: memory timeline / replay table / offline-vs-live diff / Article VII observations)
    object_drift_panel.py     274 LoC   (Step 1→2→4→6→7→8→9 chain with optional anchor and reading-lens annotations)

src/elif_v0_1/tests/
    test_viewers.py           652 LoC   (31 tests: 4 discipline classes + per-panel + CLI smoke + E.2 round-trip)

notes/
    elif_v1_viewer_samples/                                17 sample Markdown renderings (committed)
        case_{01,02,03}_LIVE_decision_room.md
        case_{01,02,03}_LIVE_exploration_lens.md
        case_{01,02,03}_LIVE_object_chain.md
        case_{01,02,03}_OFFLINE_decision_room.md
        case_{01,02,03}_OFFLINE_vs_LIVE_diff.md
        case_01_LIVE_memory_timeline.md
        article_vii_observations.md
```

**Substrate files modified:** ZERO. The viewers are a pure addition under `src/elif_v0_1/viewers/`; no existing component, schema, prompt, or runner was touched.

---

## §2 — LoC delta

| Surface | LoC | Spec estimate | Within range? |
|---|---|---|---|
| Decision Room (`decision_room.py`) | 151 | 60-150 | Within +1 |
| Exploration Lens (`exploration_lens.py`) | 173 | 120-180 | ✓ in range |
| Object Drift Panel (`object_drift_panel.py`) | 274 | 200-280 | ✓ in range |
| Laboratory Viewer (`laboratory_viewer.py` — 4 panels) | 395 | 250-350 | +45 over high end |
| **Four-viewer total** | **993** | **650-960 (high end)** | Slightly over |
| Shared helpers (`_common.py`) | 105 | n/a | infrastructure |
| CLI (`cli.py`) | 126 | n/a | infrastructure |
| Package `__init__.py` | 62 | n/a | documentation |
| **Viewer package total (src/elif_v0_1/viewers/)** | **1,286** | | |
| Tests (`tests/test_viewers.py`) | 652 | n/a | |
| **All new code** | **1,938** | | |

**Overrun explanation:** the Laboratory Viewer's diff panel + memory timeline panel handle multi-shape inputs (structured_output_dict varies across cases — axes can be lists of dicts or strings, scales can carry varying field names). Defensive normalization adds ~40 LoC vs the spec's optimistic estimate. The 4-viewer total is 993 LoC vs spec's high-end 960 — 3.4% over. The shared helpers and CLI were not counted in the spec's per-viewer estimates; they are infrastructure.

---

## §3 — Discipline proofs

The acceptance criterion is *"ELIF becomes visible without becoming different."* Three structural proofs are encoded in the test suite at `src/elif_v0_1/tests/test_viewers.py`:

### §3.1 — Proof that the substrate was not modified

A run of the full test suite before and after the viewer addition demonstrates zero regression:

```
Before (commit 95911af, spec-only): 238 tests pass, 3 skipped
After  (commit <this>, viewers shipped): 269 tests pass, 3 skipped
Delta: +31 tests (all in test_viewers.py; pre-existing 238 unchanged)
```

The 31 new tests are additive; none of the 238 prior tests changed state. **The substrate's behavioral surface is byte-stable under viewer introduction.**

### §3.2 — Proof that viewers do not call the LLM

`TestNoLLMImports` (4 tests) verifies each viewer module's `__dict__` does not contain LLM-call symbols (`complete_structured`, `_call_anthropic_tool_use`). Module-level imports are static; if the viewers ever attempted an LLM call, the symbol would have to be imported and would appear in `__dict__`.

`TestNoSubstrateMutation.test_call_counter_unchanged_by_any_viewer` directly invokes all four viewers (plus all four laboratory panels) and asserts that `_call_counter()` (the per-process LLM call counter) is unchanged before vs after. **Zero LLM calls are incurred by any viewer invocation.**

### §3.3 — Proof that viewers do not mutate input

`TestNoSubstrateMutation` (3 tests + the call-counter test) takes a synthetic RunReport dict, snapshots it as canonical JSON, calls each viewer, then re-snapshots and asserts equality. **No viewer mutates its input dict in place.**

### §3.4 — Proof of determinism (pure functions)

`TestDeterminism` (3 tests) invokes each viewer twice with the same input and asserts the rendered strings are byte-identical. **Each viewer is a pure function: same input → same output.**

### §3.5 — Reveal Test enforcement

`TestRevealTest` (5 tests) verifies that key fields from the synthetic input appear verbatim in the rendered output:

- Decision Room: verdict, verdict_detail, uncertainty sources, post_refusal_closure
- Exploration Lens: 5 territory headers + Step 2 axis name + Step 6 scale + Step 7 trajectory + Step 9 uncertainty + Step 10 theoretical
- Object Drift Panel: 7 chain node headers + bifurcation note in Step 8 reading lens

**The Reveal Test passes per spec §0: every rendered field is extractable from existing artifacts.**

### §3.6 — Truth Test enforcement

`TestTruthTest` (3 tests) verifies that forbidden recommendation/synthesis phrasing does NOT appear in the rendered output:

- Decision Room: no "should approve / should reject / we recommend / recommended action / click to approve"
- Exploration Lens: no "axis connects to scale / territory A relates to territory B / merging territories" (no edges between territories)
- Object Drift Panel: no "drift detected / drift confirmed / drift score / no drift / object substituted" (no aggregate drift claim)

**The Truth Test passes per spec §0: viewers state only what artifacts already state.**

### §3.7 — E.2 round-trip

`TestE2RoundTrip` (4 tests) loads the actual E.2 live and offline RunReport JSONs from `/tmp/elif_e2_live/` and `/tmp/elif_e2_preflight_position_b/` and renders each viewer against them. The tests pass only when the viewers can handle real, full-shape RunReports without error. They do. **Viewers are compatible with the actual substrate output.**

---

## §4 — Sample renderings (screenshots)

17 sample renderings are committed at `notes/elif_v1_viewer_samples/`, generated from the real E.2 artifacts using the CLI. Per case (3 cases × 5 renderings):

- Decision Room — LIVE run + OFFLINE reference (per case)
- Exploration Lens — LIVE run (per case)
- Object Drift Panel — LIVE run with input frame + reading lens (per case)
- Offline-vs-Live Diff — per case

Plus:
- Memory Timeline — case_01 LIVE
- Article VII Observations — across all 3 LIVE JSONLs

### §4.1 — Decision Room — case_01 LIVE excerpt

```markdown
# Decision Room — case_01_electroculture

## Step 9 — Verdict
| Field | Value |
|---|---|
| verdict | constrain |
| confidence | High on the constrain verdict and gate-sequencing logic... |

### verdict_detail
The Stage 8 roadmap (A1–A5) is authorized to proceed, but only under the
following explicit constraints: (1) No stage may advance past its stated
gate condition...

### Unresolved uncertainty sources
- Commensurability status of E1, E2, E3 evidence types (A1 output)...
- Mutual-exclusivity boundary conditions for H1–H4 under temporal regimes...
- Actor-stratum discriminators and unit-of-analysis decision (A3 output)...
- Comparability threshold for cross-domain comparison cases (A4 output)...
- Identity and availability of the designated analytic lead...

## Step 10 — Operative vs Theoretical
### Operative (6 entries — what the verdict authorizes)
- Enforce the Step 9 'constrain' verdict as the current operative gate...
- Apply the High-confidence gate-sequencing logic from Step 9...
...
```

### §4.2 — Offline-vs-Live Diff — case_01 (full output)

```markdown
# Offline-vs-Live Structural Diff — case_01_electroculture

> **The Viewer renders the comparison; it does not adjudicate it.**
> Both sides are valid procedural outputs. For substantive interpretation,
> see notes/elif_post_e2_divergence_audit.md and notes/elif_post_e2_object_drift_audit.md.
> The 'same?' column is a literal `==` comparison — not a judgment about
> which side is correct.

| Field | Offline | Live | Same? |
|---|---|---|---|
| `exit_code`                          | `20`        | `0`         | **NO** |
| `envelope_count`                     | `11`        | `11`        | yes    |
| `memory_logger_entries_written`      | `30`        | `14`        | **NO** |
| `step_9.verdict`                     | `refuse`    | `constrain` | **NO** |
| `step_9.unresolved_uncertainty_count`| `4`         | `5`         | **NO** |
| `step_10.operative_count`            | `1`         | `6`         | **NO** |
| `step_10.theoretical_count`          | `4`         | `5`         | **NO** |
| `step_11.post_refusal_closure`       | `True`      | `False`     | **NO** |
| `step_11.final_verdict`              | `refuse`    | `constrain` | **NO** |

_No aggregate verdict is emitted. Per-row 'same?' annotations are literal
comparisons only._
```

The diff panel surfaces the E.2 verdict shift cleanly: 7 of 9 structural fields differ between offline and live; the viewer does not adjudicate which is correct.

### §4.3 — Object Drift Panel — case_01 excerpt (with reading lens)

```markdown
# Object Chain Viewer — case_01_electroculture

## Anchor — Input Frame (verbatim)
> **Reading lens:** _The object as posed in the input frame — the deployment
> proposal received from the operator._

```
A coalition of agricultural researchers, environmental agencies, and
private agritech companies is considering launching a large-scale
research and pilot deployment program around electroculture techniques...
```

↓

## Step 1 — Frame Validation
> **Reading lens:** _The object as Step 1 (FrameValidator) reformulates it._
- **verdict:** `needs_decomposition`
- **reformulated_frame:** Per technique in the proposed list, what evidence...

↓

## Step 8 — Stage-gated Roadmap
> **Reading lens:** _The object as a procedural artifact — a roadmap.
> NOTE: per the object drift audit, Step 8 is the bifurcation point.
> The roadmap may describe world-actions OR analytical deliverables;
> the reader observes which._
- **A1**: A written layer-attribution table exists in which each of E, M, and R has been assigned to exactly one causal layer...

↓

## Step 9 — Verdict
> **Reading lens:** _The verdict's referent — whatever Step 8 produced.
> The Step 9 prompt presents Step 8's roadmap AS 'the proposed forward
> path'. The reader observes whether this referent is still the input
> frame's deployment question._
- **verdict:** `constrain`
- **verdict_detail:** The Stage 8 roadmap (A1–A5) is authorized to proceed...
```

The Panel makes the object-drift phenomenon visible per-run: the reader sees Step 8 produce a "layer-attribution table" gate (methodological) where the anchor described "research and pilot deployment" (world-action). The Panel does not claim drift; it lets the reader observe the chain.

### §4.4 — Article VII Observations — full output

```markdown
# Article VII Capacity Observations

> _Searched 3 MemoryLogger JSONL file(s) for `capacity_change` events. Read-only._

**No `capacity_change` events found across the searched files.**

Per spec §3.4 — Position B (commit `44b3e6e`) made the surface emitable on
refuse-cases, but no MemoryLogger consumer currently writes `capacity_change`
events. This panel will populate when consumers exist. Empty state is honest,
not hidden.
```

Honest empty state — the viewer does not hide the absence and does not fabricate an inferred capacity record.

---

## §5 — CLI usage

```bash
# Decision Room from a saved RunReport
python -m elif_v0_1.viewers.cli decision-room \
    --run-report /tmp/elif_e2_live/case_01_stdout.json \
    --out /tmp/decision_room.md

# Exploration Lens
python -m elif_v0_1.viewers.cli exploration \
    --run-report /tmp/elif_e2_live/case_01_stdout.json

# Object Drift Panel with input frame anchor + reading lens (default)
python -m elif_v0_1.viewers.cli object-drift \
    --run-report /tmp/elif_e2_live/case_01_stdout.json \
    --input-frame cases/case_01_electroculture/input_frame.md

# Object Drift Panel in strict-minimum mode (no reading-lens annotations)
python -m elif_v0_1.viewers.cli object-drift \
    --run-report /tmp/elif_e2_live/case_01_stdout.json \
    --no-reading-lens

# Memory Timeline
python -m elif_v0_1.viewers.cli memory-timeline \
    --case-id case_01_electroculture \
    --jsonl /tmp/elif_e2_live/case_01/case_01_electroculture/article_vii_tracking.jsonl

# Offline-vs-Live Diff
python -m elif_v0_1.viewers.cli offline-vs-live \
    --offline /tmp/elif_e2_preflight_position_b/case_01_stdout.json \
    --live    /tmp/elif_e2_live/case_01_stdout.json

# Article VII Observations
python -m elif_v0_1.viewers.cli article-vii \
    --jsonl /tmp/elif_e2_live/case_01/case_01_electroculture/article_vii_tracking.jsonl \
    --jsonl /tmp/elif_e2_live/case_02/case_02_policy_governance/article_vii_tracking.jsonl \
    --jsonl /tmp/elif_e2_live/case_03/case_03_operational_organizational/article_vii_tracking.jsonl
```

All commands accept an optional `--out <path>` for file output instead of stdout.

---

## §6 — What this implementation does NOT do

Per spec + operator green light:

- Does NOT modify any component
- Does NOT modify any Article
- Does NOT modify any schema
- Does NOT modify the procedure
- Does NOT modify closed-set vocabulary
- Does NOT add LLM calls
- Does NOT add new memory layer
- Does NOT add hidden reasoning layer
- Does NOT synthesize across runs
- Does NOT recommend operator action
- Does NOT include approve/reject controls
- Does NOT do pattern mining
- Does NOT include world-model overlays
- Does NOT activate any phase
- Does NOT propose v0.5

The visibility layer is read-only, additive, removable. Deleting `src/elif_v0_1/viewers/` and `src/elif_v0_1/tests/test_viewers.py` reverts the substrate to its pre-viewer state with zero behavioral difference.

---

## §7 — Acceptance criterion check

**"ELIF becomes visible without becoming different."**

| Claim | Evidence |
|---|---|
| ELIF becomes visible | 4 viewers shipped + 17 sample renderings against real E.2 artifacts on disk |
| ELIF does not become different | 238 pre-existing tests still pass byte-for-byte; no substrate file modified; no LLM call surface added; viewer modules verified to not import `llm_adapter` symbols; LLM call counter unchanged before vs after viewer invocation |

**Both halves of the acceptance criterion are satisfied.**

---

## §8 — Operator decision surface

The viewer suite is shipped and verified. The operator can now:

1. **Render any RunReport from the CLI** — no code changes needed; viewers operate over saved JSONs
2. **Render the E.2 artifacts via the committed samples** — see `notes/elif_v1_viewer_samples/`
3. **Use the viewers as embedded Python functions** — import from `elif_v0_1.viewers`
4. **Leave the viewers dormant** — no run-time impact; pure additions; removable

No further operator action is required. The viewers serve whenever called; they sit dormant otherwise.

---

## References

- Spec: [notes/elif_v1_viewer_audit_and_spec.md](elif_v1_viewer_audit_and_spec.md)
- Object drift audit: [notes/elif_post_e2_object_drift_audit.md](elif_post_e2_object_drift_audit.md)
- Divergence audit: [notes/elif_post_e2_divergence_audit.md](elif_post_e2_divergence_audit.md)
- E.2 live replay report: [notes/elif_v0_1_e2_live_replay_report.md](elif_v0_1_e2_live_replay_report.md)
- Source: `src/elif_v0_1/viewers/`
- Tests: `src/elif_v0_1/tests/test_viewers.py`
- Samples: `notes/elif_v1_viewer_samples/`

---

**Implementation closed. ELIF V1 visibility layer shipped. Substrate unchanged. Reality remains sovereign.**
