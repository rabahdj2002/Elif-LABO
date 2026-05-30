# ELIF E.2 Live-Replay Pre-flight Pack

> **Captured:** 2026-05-30
> **Author role:** subagent under operator-authorized 100-hour ELIF sprint.
> **Status:** PRE-FLIGHT. `ANTHROPIC_API_KEY` is UNSET in this sandbox; the
> agent did NOT execute live mode. Live execution is staged for the
> operator under §3. The offline re-baseline of §2 was actually run by
> this agent and is captured under `/tmp/elif_e2_preflight/`.
> **Non-expansionary stance:** this pack proposes NO new component, NO new
> Article, NO procedure mutation, NO architecture change. It instruments
> the E.2 evidence event named in `notes/elif_audit_synthesis.md` §4.1 so
> the result reads against the offline reference without ambiguity.
> **Doctrine constraint:** the procedure is FROZEN for E.2. Per audit
> synthesis §4.1 "do not modify the procedure during E.2", prompt tuning
> during the run is the canonical fix-the-verdict-by-tweaking-the-prompt
> failure mode (B §B-non-recommendations 8). If divergence appears, this
> pack tells the operator how to read it, not how to react during it.

## Epistemic status legend

- **[CE]** Current Evidence — verified in this session against the
  working tree at capture time; anchored to file:line or stdout.
- **[PF]** Plausible Future — consistent with CE + audits, contingent
  on live run.
- **[SP]** Speculation — outside what offline can support.

---

## 1. Environment pre-flight (API key check + Python env + CLI smoke)

### 1.1 ANTHROPIC_API_KEY check `[CE]`

Sandbox check at capture time returned `NO`. The adapter reads the env
var lazily inside `_call_anthropic_tool_use` at
`src/elif_v0_1/llm_adapter.py:178-182`:

```
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise LLMAdapterError(
        "offline_mode=False requires ANTHROPIC_API_KEY in environment"
    )
```

Failure surfaces at the first non-fixture call (Step 2 — ObjectDecomposer
per `STEP_OWNER` in `orchestration_runner.py:51`). **Gate G-Env-1:**
operator exports a working key before running §3.

### 1.2 Python environment `[CE]`

- `elif_v0_1` lives at `src/elif_v0_1/`; the CLI must be invoked with
  `PYTHONPATH=src` (no editable install in tree).
- `anthropic` SDK is imported LAZILY at `llm_adapter.py:184-190`; missing
  SDK raises `LLMAdapterError`.
- `jsonschema` is imported LAZILY at `llm_adapter.py:105-111`. If absent,
  a structural fallback runs (required-keys + `type=object`) that does
  NOT catch enum drift. **Gate G-Env-2:** confirm both packages installed
  via `pip show anthropic jsonschema`.

### 1.3 CLI smoke (offline) `[CE]`

Argparse surface in `cli.py:42-85`:

| flag | type | default | notes |
|---|---|---|---|
| `--case` | str | required | case directory under `cases/` |
| `--condition` | a / b / c | required | benchmark column |
| `--procedure-version` | v1.0 / v1.1 | v1.0 | v1.1 not authorized in v0.1 |
| `--offline` | flag | False | omit to select live |
| `--max-llm-calls` | int | 22 | operator-locked per Step 8 §8.4 |
| `--results-dir` | str | None | MemoryLogger persistence dir |

Exit-code semantics (`cli.py:15-19` + `runner.py:124-128`):

| code | meaning | raise site |
|---|---|---|
| 0 | clean close (all 11 steps committed) | `_emit_close(...exit_code=0)` |
| 10 | `FrameInvalidError` (Step 1 verdict=invalid) | `runner.py:229` |
| 20 | `GovernanceRefuseError` (Step 9 verdict=refuse) | `runner.py:337` |
| 30 | `SchemaValidationError` or `LLMCallCapError` | `runner.py:418-451` |

**Gate G-Env-3:** confirm CLI is reachable via
`PYTHONPATH=src python -m elif_v0_1.cli run --help`.

---

## 2. Offline control re-baseline (actually run in this session)

This re-baseline was executed by the pack author at capture time.

### 2.1 Commands executed `[CE]`

```
mkdir -p /tmp/elif_e2_preflight
cd /home/dev/elif-lab
PYTHONPATH=src python -m elif_v0_1.cli run \
    --case case_01_electroculture --condition c --offline \
    --results-dir /tmp/elif_e2_preflight/case_01_memory \
    > /tmp/elif_e2_preflight/case_01_stdout.json \
    2> /tmp/elif_e2_preflight/case_01_stderr.txt
# same for case_02_policy_governance, case_03_operational_organizational
```

### 2.2 Per-case results `[CE]`

All three exited with code 20 (GovernanceRefuseError), matching the
alpha replay report's `partially` verdict at structural similarity 0.83.

| case | exit | stdout bytes | memory JSONL bytes | committed steps | memory events |
|---|---|---|---|---|---|
| case_01_electroculture | 20 | 10,650 | 4,293 | 9 | 13 |
| case_02_policy_governance | 20 | 9,413 | 4,325 | 9 | 13 |
| case_03_operational_organizational | 20 | 9,061 | 4,437 | 9 | 13 |

Memory file name is fixed at `memory_logger.py:72` (`_EVENTS_FILENAME =
"article_vii_tracking.jsonl"`); each case directory holds one such
JSONL.

### 2.3 Deterministic structural anchors offline `[CE]`

These are the per-case structural commitments the live run will be
compared against. Deterministic offline because fixtures are operator-locked.

| case | step_9 verdict | step_2 axes | step_4 hyp | step_7 trajs | step_8 stages | step_9 uncertainty |
|---|---|---|---|---|---|---|
| case_01 | refuse | 2 | 3 | 4 | 5 | 4 |
| case_02 | refuse | 2 | 3 | 3 | 4 | 3 |
| case_03 | refuse | 2 | 3 | 3 | 4 | 3 |

Target for live: structural commitments survive (same verdict + same
counts within tolerance per §6.1 scorer).

### 2.4 Fields that vary between runs (NOT divergence signals) `[CE]`

Excluded from any offline/live diff:

- `run_context.run_id` (UUID, `runner.py:71-73`)
- `run_context.started_at_iso` + `completed_at_iso` (UTC, `runner.py:140` + `cli.py:141`)
- per-step `committed_at_iso` (`runner.py:192`)
- MemoryLogger `event_id` (UUID, `memory_logger.py:85-87`) + per-event timestamp

### 2.5 Memory-event composition offline (per case) `[CE]`

13 events per case = 1 `open` + 9 `step_committed` (steps 1-9) + 1
`step_committed` for step_7_modeB (FrameValidator side-channel,
`runner.py:288-303`) + 1 `refutation` (governance_refuse,
`runner.py:328-333`) + 1 `close` (exit_code=20).

Step 11 content events (`judgment_act`, `pattern_engaged`,
`capacity_change`) are NOT emitted offline because the runner halts at
Step 9 — the G0 (refuse-halt adjudication) signal named in audit
synthesis §1.3. **E.2 will reproduce this halt unless G0 is closed
Position B AND the runner is modified BEFORE E.2.** Per audit synthesis
§4.0 ("do NOT run E.2 before G0 closes"), conventional sequencing is G0
first, then E.2. This pack does not adjudicate G0; it instruments E.2
under either position.

---

## 3. Live execution command bundle (operator runs after setting key)

The bundle below is what the operator runs once `ANTHROPIC_API_KEY` is
exported. The pack author did NOT run it.

### 3.1 Pre-run shell setup

```bash
export ANTHROPIC_API_KEY="sk-..."
[ -n "$ANTHROPIC_API_KEY" ] && echo "API key set" || { echo "MISSING"; exit 1; }
python -c "import anthropic, jsonschema; print('anthropic', anthropic.__version__)" \
    || { echo "MISSING DEPS"; exit 1; }
mkdir -p /tmp/elif_e2_live
cd /home/dev/elif-lab
```

### 3.2 Per-case live runs (one command per case)

`reset_call_counter()` at `runner.py:132` resets the 22-call cap at the
start of each run, so each case has its own budget.

```bash
# CASE 01 — electroculture
PYTHONPATH=src python -m elif_v0_1.cli run \
    --case case_01_electroculture --condition c \
    --max-llm-calls 22 \
    --results-dir /tmp/elif_e2_live/case_01_memory \
    > /tmp/elif_e2_live/case_01_live_stdout.json \
    2> /tmp/elif_e2_live/case_01_live_stderr.txt
echo "case_01 exit_code=$?" | tee -a /tmp/elif_e2_live/exit_codes.log

# CASE 02 — policy-governance
PYTHONPATH=src python -m elif_v0_1.cli run \
    --case case_02_policy_governance --condition c \
    --max-llm-calls 22 \
    --results-dir /tmp/elif_e2_live/case_02_memory \
    > /tmp/elif_e2_live/case_02_live_stdout.json \
    2> /tmp/elif_e2_live/case_02_live_stderr.txt
echo "case_02 exit_code=$?" | tee -a /tmp/elif_e2_live/exit_codes.log

# CASE 03 — operational-organizational
PYTHONPATH=src python -m elif_v0_1.cli run \
    --case case_03_operational_organizational --condition c \
    --max-llm-calls 22 \
    --results-dir /tmp/elif_e2_live/case_03_memory \
    > /tmp/elif_e2_live/case_03_live_stdout.json \
    2> /tmp/elif_e2_live/case_03_live_stderr.txt
echo "case_03 exit_code=$?" | tee -a /tmp/elif_e2_live/exit_codes.log
```

### 3.3 Cost-cap early-halt sentinel

The 22-call cap lives in `llm_adapter.py:253-258` (`LLMCallCapError`).
The runner catches at `runner.py:435-451` → exit_code 30. For a BASH-level
trap on cost overrun across the bundle:

```bash
set -e
trap 'echo "HALT: nonzero exit. See exit_codes.log."; cat /tmp/elif_e2_live/exit_codes.log' ERR
# (cases as in §3.2 — sequential; trap fires on first nonzero exit NOT in {0,20})
```

Acceptable exit codes:
- `0` — clean close (Position B path, only if G0=B and runner updated)
- `20` — `GovernanceRefuseError` (Position A path; expected per offline)

UNACCEPTABLE (halt + investigate):
- `10` — `FrameInvalidError` (offline returns `needs_decomposition`,
  never `invalid`; live `invalid` is a load-bearing divergence)
- `30` — `SchemaValidationError` or `LLMCallCapError` (schema drift OR
  cap exhaustion; both are E.2-stop conditions per synthesis §4.1)

### 3.4 Post-run diff vs offline baseline

```bash
canonicalize() {
    python -c "
import json, sys
r = json.load(sys.stdin)
ctx = r.get('run_context', {})
for k in ('run_id', 'started_at_iso'):
    ctx.pop(k, None)
r.pop('completed_at_iso', None)
for env in r.get('step_outputs', []):
    env.pop('committed_at_iso', None)
print(json.dumps(r, indent=2, sort_keys=True))
"
}

for c in case_01 case_02 case_03; do
    echo "=== $c ==="
    canonicalize < /tmp/elif_e2_preflight/${c}_stdout.json \
        > /tmp/elif_e2_live/${c}_offline_canon.json
    canonicalize < /tmp/elif_e2_live/${c}_live_stdout.json \
        > /tmp/elif_e2_live/${c}_live_canon.json
    diff -u /tmp/elif_e2_live/${c}_offline_canon.json \
            /tmp/elif_e2_live/${c}_live_canon.json \
        > /tmp/elif_e2_live/${c}_diff.txt
    echo "  diff bytes: $(wc -c < /tmp/elif_e2_live/${c}_diff.txt)"
done
```

A zero-byte diff would be SUSPICIOUS (live ≠ fixture is expected). A
diff in the 1KB–10KB range with structural anchors preserved is the
expected shape; §6 specifies the scoring pipeline.

---

## 4. Schema + closed-set drift surfaces

### 4.1 Schema validation enforcement points `[CE]`

| Surface | Where | Behavior |
|---|---|---|
| Adapter post-call validation | `llm_adapter.py:270` | runs on EVERY structured-output call |
| `jsonschema` branch | `llm_adapter.py:105-111` | Draft 2020-12; ValidationError wrapped as `SchemaValidationError` |
| Structural fallback | `llm_adapter.py:116-127` | required keys + type=object only; weaker than full schema |
| Runner catch | `runner.py:418-434` | `SchemaValidationError` → `_emit_refutation('schema_violation')` → exit 30 |

If the LLM emits structurally valid JSON that violates an enum, only
the `jsonschema` branch catches it. **G-Env-2 is the substrate for
closed-set enforcement.**

### 4.2 Exceptions that surface drift in live mode `[CE]`

| Exception | Raise site | Exit | Meaning |
|---|---|---|---|
| `FrameInvalidError` | `runner.py:229` | 10 | Step 1 verdict=invalid (Article II tie) |
| `GovernanceRefuseError` | `runner.py:337` | 20 | Step 9 verdict=refuse (Articles V/VI/VII) |
| `SchemaValidationError` | `llm_adapter.py:111`, `base.py:96` | 30 | Structured-output shape drift (Step 8 §8.7 freeze violated) |
| `LLMCallCapError` | `llm_adapter.py:256` | 30 | Per-run cap exhausted (Step 8 §8.4) |
| `LLMAdapterError` | `llm_adapter.py:138,148,154,160,181,188,220,225` | uncaught | Transport / SDK / fixture-loader plumbing |

NOTE: `LLMAdapterError` has no runner catch; a network outage propagates
to CLI as traceback. Known thin-spot; not in E.2 scope to fix.

### 4.3 Closed-set vocabularies checked in live mode `[CE]`

| Vocabulary | Closed set | Where checked |
|---|---|---|
| Step 1 verdict | `{valid, invalid, needs_decomposition}` | `schemas/__init__.py:209-212` |
| Step 7 mode tag | `{outside-original-frame, deeper-frame-rejection}` | `schemas/__init__.py:353` + `bre.py:47` |
| Step 9 verdict | `{constrain, refuse, explicitly_abstain}` | `schemas/__init__.py:395-398` + `gk.py:65` |
| MemoryLogger event_type | 11 values (`open, close, step_committed, frame_locked, verdict_emitted, uncertainty_recorded, reuse_detected, pattern_recognized, refutation, capacity_change, correction`) | `memory_logger.py:47-59`, validated at `write_event` line 211-216 |
| MemoryLogger change_type | 5 values (`arbitration_shortcut_added, framework_candidate_emerged, composition_path_discovered, pattern_recognition_added, judgment_act_logged`) | `memory_logger.py:63-69` |
| Step 11 content kinds | `{capacity_change, pattern_engaged, pattern_deprecated, judgment_act}` | `schemas/__init__.py:444-449` |
| Component / step / Article / failure-pole registries | 7 / 11 / 7 / 4 — all frozen | `base.py:22-60`, asserted at `runner.py:89-91` |

**Interpretation rule:** if the live run completes schema validation,
the closed-sets above were preserved. If `SchemaValidationError` fires
on a closed-set field, the live LLM drifted from operator-locked
vocabulary. Per audit synthesis §1.2, schema drift is a FINDING, not a
procedural-modification prompt.

### 4.4 Semantic post-validation (beyond JSON schema) `[CE]`

Three components run post-schema semantic checks:

| Component | Check | Raises |
|---|---|---|
| ObjectDecomposer | >=2 distinct scales; >=2 families per axis | `SchemaValidationError` |
| HypothesisValidator | distinguishing_prediction non-empty; fails_if non-empty | `SchemaValidationError` |
| FrameValidator | reformulated_frame required when verdict != valid (`frame_validator.py:231-237`) | `SchemaValidationError` |

Live mode that produces schema-clean but semantically-thin output WILL
be caught here. Intended.

---

## 5. Cost-cap + budget tuning

### 5.1 Live-mode projection (from existing cost report) `[CE]`

Per `elif_v0_1_alpha_cost_complexity_report.md` §1: per case ~10–12
calls × (2k input + 1k output tokens) → **~$0.21/case** at sonnet list
pricing ($3.00/MTok input, $15.00/MTok output). Three-case cohort:
**~$0.63**. $20 baseline subsumes ~95 cohort runs.

Under refuse-halt at Step 9, only steps 2–9 with LLM calls fire (~10
calls). Under Position B (Step 10 + Step 11 execute) cost rises by
~$0.02/case.

### 5.2 Cap code path (operator may tune)

| Lever | File:line | Effect |
|---|---|---|
| CLI default | `cli.py:77` (`default=22`) | per-run cap |
| Runner default | `runner.py:103` (`max_llm_calls: int = 22`) | per-run cap when called programmatically |
| Adapter check | `llm_adapter.py:253-258` | raises `LLMCallCapError` — actual enforcement |
| Component fallback | `governance_kernel.py:57` (`_DEFAULT_MAX_CALLS = 22`) | if a component runs outside the runner |

Tuning notes (documentation only; do NOT change for E.2):
- Below ~12 calls Step 9 cannot execute under refuse path.
- Above 22 is a no-op offline; provides headroom under Position B.
- The cap is a CALL count, not a DOLLAR count. If a future component
  doubles tokens, dollar projection drifts even though cap doesn't.

### 5.3 What the cap does NOT cover

Cap is per-PROCESS, reset each invocation. To cap COHORT cost, the
operator runs the §3.4 diff between cases and aborts on anomaly. Cap
also does NOT cover SDK retries of transient 5xx (wire-cost paid
twice, slot consumed once); upstream SDK behavior; not in E.2 scope.

---

## 6. Post-execution analysis pipeline (specification — not run)

Per audit synthesis §4.1, the deliverable is
`notes/elif_v0_1_e2_live_replay_report.md`. The pipeline below specifies
how to populate it.

### 6.1 Per-case structural similarity computation

Target ≥ 0.83 (alpha offline floor; audit synthesis §4.1).

```python
def structural_similarity(live_report: dict, offline_report: dict) -> float:
    checks = []
    live_steps = {s['step_id']: s['structured_output_dict']
                  for s in live_report['step_outputs']}
    off_steps = {s['step_id']: s['structured_output_dict']
                 for s in offline_report['step_outputs']}
    # 1. Step 1 verdict matches
    checks.append(live_steps['step_1'].get('verdict') ==
                  off_steps['step_1'].get('verdict'))
    # 2. Step 2 axis count >= offline
    checks.append(len(live_steps['step_2'].get('axes', [])) >=
                  len(off_steps['step_2'].get('axes', [])))
    # 3. Step 2 families per axis >= 2
    checks.append(all(len(a.get('families', [])) >= 2
                      for a in live_steps['step_2'].get('axes', [])))
    # 4. Step 3 assumptions >= 2
    checks.append(len(live_steps['step_3'].get('assumptions', [])) >= 2)
    # 5. Step 4 hypotheses >= 2
    checks.append(len(live_steps['step_4'].get('hypotheses', [])) >= 2)
    # 6. Every hypothesis has distinguishing_prediction
    checks.append(all(h.get('distinguishing_prediction')
                      for h in live_steps['step_4'].get('hypotheses', [])))
    # 7. Step 5 failure_conditions present per hypothesis
    checks.append(all(h.get('fails_if')
                      for h in live_steps['step_5'].get('hypotheses', [])))
    # 8. Step 6 scales >= 2
    checks.append(len(live_steps['step_6'].get('scales', [])) >= 2)
    # 9. Step 7 mode A tag preserved
    trajs = live_steps['step_7'].get('trajectories', [])
    checks.append(all(t.get('tag') == 'outside-original-frame' for t in trajs))
    # 10. Step 8 stages with continuation_gate
    stages = live_steps['step_8'].get('stages', [])
    checks.append(len(stages) >= 1
                  and all(s.get('continuation_gate') for s in stages))
    # 11. Step 9 verdict in closed set
    checks.append(live_steps['step_9'].get('verdict')
                  in {"constrain", "refuse", "explicitly_abstain"})
    # 12. Step 9 unresolved_uncertainty_sources >= 1
    checks.append(len(live_steps['step_9']
                      .get('unresolved_uncertainty_sources', [])) >= 1)
    return sum(1 for c in checks if c) / len(checks)
```

Score < 0.83 = load-bearing finding. Operator must NOT modify the
procedure to chase 0.83 (audit synthesis §4.1 prompt-tuning prohibition);
they record the gap and adjudicate via §8.

### 6.2 Per-step JSON divergence

For each step, classify every top-level key:

```python
def per_step_divergence(live_step: dict, off_step: dict) -> dict:
    drift = {'identical': [], 'value_changed': [], 'added': [], 'removed': []}
    for k in set(live_step.keys()) | set(off_step.keys()):
        if k not in off_step:    drift['added'].append(k)
        elif k not in live_step: drift['removed'].append(k)
        elif live_step[k] == off_step[k]: drift['identical'].append(k)
        else:                    drift['value_changed'].append(k)
    return drift
```

`added` / `removed` are strong signals (LLM produced or omitted a
top-level field). `value_changed` shows where the LLM differs from the
operator-authored fixture.

### 6.3 Cost burn vs $0.21/case projection

1. Read Anthropic SDK `message.usage` (input/output token counts per
   call). The CLI does NOT capture this today — deliberate
   non-expansion; runner does not aggregate usage.
2. Sum input + output tokens per case.
3. cost = (input × $3.00/MTok) + (output × $15.00/MTok).
4. Compare to $0.21/case projection. Divergence > 2× is a finding;
   driver is most likely output tokens.

Per non-expansion rule, do NOT add usage tracking to the runner during
E.2. Capture from stderr only.

### 6.4 Architecture-dependent vs model-dependent signature

**Architecture-dependent (should be identical / near-identical):**

- `run_context.case_id, condition, procedure_version, offline_mode, max_llm_calls`
- count of `step_outputs` entries (determined by halt path)
- `step_9.verdict` ∈ closed set (schema-enforced)
- `step_7.trajectories[*].tag == "outside-original-frame"` (schema + BRE)
- MemoryLogger event_type sequence pattern (runner-determined)

**Model-dependent (will vary; OK):**

- per-step prose fields (`step_9.verdict_detail`, axis names,
  hypothesis statements, uncertainty source strings)
- counts within tolerance bounds named in §6.1

Drift in architecture-dependent = regression; drift in
model-dependent = expected. Tabulate per case.

### 6.5 Differentiator survival analysis

Differentiators distinguish ELIF outputs from a bare-LLM baseline (per
long-range roadmap Phase 1). For E.2 (three-case live):

| Differentiator | Survival criterion (live) |
|---|---|
| Multi-axis decomposition | step_2 has >= 2 axes |
| Hypotheses carry distinguishing predictions | step_4 every hyp has non-empty `distinguishing_prediction` |
| Failure conditions per hypothesis | step_5 every hyp has non-empty `fails_if` |
| Cross-scale relations surfaced | step_6 has >= 2 scales + non-empty cross-scale relations |
| Outside-original-frame trajectories (mode A) | step_7 trajectories[*].tag == "outside-original-frame" |
| Stage-gated roadmap with continuation gates | step_8 each stage has `continuation_gate` |
| Closed-set governance verdict + named uncertainty | step_9 verdict ∈ closed set + uncertainty count >= 1 |

Per differentiator: SURVIVED / DEGRADED / FAILED. Target: ≥ 7/7
SURVIVED. DEGRADED is a finding; FAILED is a regression.

### 6.6 Deliverable shape (`elif_v0_1_e2_live_replay_report.md`)

Recommended TOC (mirrors offline report):

- §1 Per-case live behaviors (Steps 1-9 +/- 10-11 if Position B)
- §2 Per-case structural similarity (§6.1)
- §3 Per-case missing or unexpected behaviors
- §4 Per-case memory log composition
- §5 Per-case cost burn (§6.3)
- §6 Differentiator survival (§6.5)
- §7 Architecture vs model dependence (§6.4)
- §8 Cohort verdict (acceptable / partially / refuse-flag)
- §9 Operator decision points surfaced

The report closes G1 (audit synthesis §5 gate table); per §4.1, Phase 1
closes when the report is written and operator confirms acceptance.

---

## 7. Expected behavioral comparison matrix

| Surface | Offline [CE] | Expected live [PF] | Would surprise [SP] |
|---|---|---|---|
| Step 1 verdict | `needs_decomposition` × 3 | same (frames ARE bundled per case design) | `valid` (LLM treats frame as well-formed) or `invalid` (rejects outright) |
| Step 2 axis count | 2 / case | 2-4 / case; semantic check enforces >=2 | 1 axis (semantic failure) or >5 (overdecomposition; fragmentation pole) |
| Step 4 hypotheses | 3 / case | 2-5 / case, each with prediction | hyp without prediction (Article I regression) |
| Step 7 mode A tag | `outside-original-frame` always | same (schema-enforced) | tag drift = `SchemaValidationError` |
| Step 8 stages | 4-5 / case, with continuation_gate | 3-6 / case | stages without continuation_gate (Article VI regression) |
| Step 9 verdict | `refuse` × 3 | `refuse` × 3 expected; `constrain` plausible; `explicitly_abstain` rare | verdict outside closed set = `SchemaValidationError` |
| Step 9 uncertainty count | 3-4 / case | 1-6 / case; semantic check enforces >=1 | empty `unresolved_uncertainty_sources` (Article VII regression) |
| Steps 10 + 11 (Position A) | NOT executed | NOT executed (runner halts at Step 9 refuse) | they execute under Position A (= runner code drift) |
| Steps 10 + 11 (Position B) | NOT executed | EXECUTED if G0=B AND runner modified | same: depends on G0 |
| MemoryLogger event count | 13 / case (Position A) | 13 / case (A); 15-17 / case (B) | significant deviation = structural-anchor finding |
| Exit code | 20 × 3 (refuse) | 20 × 3 under A; 0 × 3 under B | 10 (frame_invalid), 30 (schema or cap) = E.2-stop |

Notes:
- Matrix assumes Position A unless G0 has explicitly closed B AND
  runner is updated (the runner update is part of G0 closure per audit
  synthesis §4.0, NOT E.2 preparation).
- "Plausible live" entries reflect model-dependent latitude (§6.4);
  the §6.1 scorer is the pass/fail surface.
- "Would surprise" are diagnostic markers; §8 classifies each.

---

## 8. Failure-mode map (what each divergence implies)

Per audit synthesis §1.2, correct response to a failure mode is NEVER
to add a component or Article; record the finding and propagate to the
next phase's evidence gate.

### 8.1 Closed-set drift (verdict / tag / event_type)

Surfaces as `SchemaValidationError` at adapter; exit 30. The live LLM
violated an operator-locked closed-set vocabulary. Per `base.py`
doctrine, closed sets are load-bearing; silent expansion = closed-set
capture failure mode. **Action:** record. Do NOT expand. Investigate
prompt clarification at Phase 2, NOT during E.2.

### 8.2 Semantic drift (axis < 2; missing distinguishing_prediction; empty uncertainty)

Surfaces as `SchemaValidationError` (post-validation raises); exit 30.
Live output structurally thin in a way that violates the Article tie:
missing distinguishing_prediction weakens Article I; empty uncertainty
weakens Article VII. **Action:** record. Known thin spot per
`what_remains.md` §5.2 (Article I alpha-untested in drift direction).

### 8.3 Verdict shift (offline=refuse, live=constrain or explicitly_abstain)

Schema passes; runner only halts on `verdict == "refuse"`
(`runner.py:327`). `constrain` and `explicitly_abstain` continue past
Step 9 — live `constrain` would exercise Steps 10 + 11 for the first
time in any replay. Doctrinal meaning: model judges the case
differently from the operator's fixture. NOT architectural drift.
**Action:** record. Compare verdict shift to case
`doctrinal_scope_tag` (Cluster A/B/C). Most interesting
Phase-1-evidence-event; do not over-react.

### 8.4 Frame-invalid surprise (Step 1 verdict=invalid in live)

`FrameInvalidError`; exit 10. Operator-locked frames have replayed
offline with `needs_decomposition`, never `invalid`. A live `invalid`
is a strong, surprising signal: either (a) genuine input_frame.md
ill-formedness fixture-replay couldn't surface, or (b) Step 1 prompt
drift. **Action:** STOP the cohort, read `verdict_detail`, investigate
before continuing.

### 8.5 LLMCallCapError

Exit 30. Run consumed > 22 calls before finishing. Under refuse-halt,
10-12 calls is the floor; 22 is comfortable. Hitting cap = a component
re-issued calls (retry?) or Step 9 fired Position-B-style additional
calls. **Action:** read per-step `llm_calls_used` on committed
envelopes; identify the step that consumed > 1 call.

### 8.6 LLMAdapterError (transport / SDK)

Uncaught by runner; propagates to CLI as traceback. Plumbing, NOT an
architecture finding. **Action:** check `ANTHROPIC_API_KEY` + SDK
install + retry.

### 8.7 Structural similarity < 0.83 with no exception raised

§6.1 scorer < 0.83. Schema + semantic checks pass but live output is
thinner: fewer axes / hypotheses / trajectories / stages / uncertainty
sources. Procedure ran, output less decomposed. **Action:** record
per-case score. Acceptable response is to write the finding into the
report. PROHIBITED response is to re-prompt for thicker output during
E.2.

### 8.8 Structural similarity >= 0.83 with cost > $0.50/case

Procedure preserves structure; token burn higher than projected. Cost
is model-dependent; not a procedural finding. **Action:** record cost.
Adjust projection in cost-complexity report if delta > 2×.

### 8.9 All three cases pass with similarity >= 0.83, exit codes consistent

G1 (audit synthesis §5) closes. v0.4 architecture survives live LLM
pressure on the three reference cases. **Action:** write the report,
mark G1 closed, queue Phase 2 (V1 surface) per synthesis §4.2.

---

## 9. Operator decisions queued

1. **G0 sequencing.** Audit synthesis §4.0 names G0 (refuse-halt
   adjudication) as a hard prerequisite for E.2. This pack does NOT
   resolve G0. Operator decides whether to run E.2 under Position A
   (current runner; halts at Step 9 on refuse) or close G0 first and
   run under Position B (modified runner; Steps 10 + 11 execute even
   on refuse). §3 works under either; §7 tabulates expected behavior.

2. **Cap setting.** §3.2 uses `--max-llm-calls 22` (Step 8 §8.4
   default). Operator may set lower for a tight cost ceiling; practical
   floor is ~12 (below: Step 9 cannot execute under refuse) and ~14
   (below: Position B Step 10 cannot execute).

3. **Cost ceiling.** No dollar ceiling enforced by pack. Projection
   $0.63/cohort; even at 10× drift stays < $7. Operator may pre-set
   ceiling via §3.3 trap.

4. **jsonschema dependency.** Validator falls back to structural-only
   check if `jsonschema` missing. Operator must confirm installed
   BEFORE run; otherwise closed-set drift will not surface (§4.1).

5. **E.2 report shape.** §6.6 proposes TOC mirroring offline report.
   Operator may compress (preferred per audit synthesis §1.2
   "no expansion") or expand.

6. **Failure-stop policy.** §3.3 lists `{0, 20}` as acceptable. Operator
   may relax (continue on 30 to capture more data) or tighten. Pack
   recommends `set -e` + trap.

7. **Position-B runner modification.** If G0 = Position B, runner needs
   a one-line change at `runner.py:327` (remove or modify the
   refuse-halt). Pack does NOT make this change. Per audit synthesis
   §4.0, runner update is part of G0 closure, NOT E.2 preparation.

---

## 10. What this pre-flight pack does NOT include

1. **Does NOT run live mode.** `ANTHROPIC_API_KEY` unset; §1.1
   documents the verification; §3 provides commands the operator runs.

2. **Does NOT modify any source file.** No edits to `cli.py`,
   `orchestration_runner.py`, `llm_adapter.py`, any component, any
   schema. Pack is markdown + offline re-baseline artifacts under
   `/tmp/elif_e2_preflight/`.

3. **Does NOT propose a new component / Article / step.** Per audit
   synthesis §1.2 and sprint constraint, no v0.5, no new component,
   no new Article.

4. **Does NOT adjudicate G0.** Audit synthesis §4.0 names G0 as
   operator-only. Pack tabulates expected behavior under both
   positions in §7; does not advocate.

5. **Does NOT specify a Step 10 / Step 11 implementation path.** If
   Position B is chosen, runner update is one line; broader Step 10/11
   prompt + schema work is Phase 5 (audit synthesis §4.5), NOT E.2.

6. **Does NOT capture cost burn during the live run.** §6.3 specifies
   post-run cost computation. Runner does not instrument usage today;
   pack does not propose adding instrumentation (non-expansion stance).

7. **Does NOT propose V1 / V2 / V3 surface design.** Audit synthesis
   §4.2 places V1 surface AFTER G1 closes. Pack is upstream of that.

8. **Does NOT propose changes to the cap, the model id
   (`claude-sonnet-4-6`), the schema_version, or the closed-set
   vocabularies.** All operator-locked; §4.3 enumerates them so drift
   can be DETECTED, not so they can be expanded.

9. **Does NOT propose a multi-model live run.** Audit synthesis §1.10
   confirms anti-monoculture is Phase 5+; E.2 is single-family.

10. **Does NOT propose pre-Phase-7 world-model work.** Audit synthesis
    §4.3 item 6 is the permanent prohibition.

11. **Does NOT commit to V3 (multi-operator).** Per audit synthesis
    §4.9, V3 is SPECULATION.

12. **Does NOT propose audio / video / chatbot / LLM-prose summary
    surfaces.** Audit synthesis §1.4 + §1.5 permanently exclude.

13. **Does NOT cross-couple to OSG runtime.** Audit synthesis §1.7
    permanent prohibition.

14. **Does NOT add a UI surface.** §3 is bash; §6 is python
    pseudo-code; no HTML, no dashboard, no rendering layer.

15. **Does NOT promote any case to reference status.** Audit synthesis
    §4.3 names case promotion as a Phase 3 concern.

---

## Appendix A — File / line index of load-bearing anchors

| Anchor | File:line |
|---|---|
| `ANTHROPIC_API_KEY` env-read | `src/elif_v0_1/llm_adapter.py:178-182` |
| Model id (`claude-sonnet-4-6`) | `src/elif_v0_1/llm_adapter.py:56` |
| Cap default (22) | `cli.py:77` + `orchestration_runner.py:103` |
| Cap enforcement | `llm_adapter.py:253-258` |
| Schema validation entry | `llm_adapter.py:270` |
| jsonschema branch | `llm_adapter.py:105-111` |
| Structural fallback | `llm_adapter.py:116-127` |
| Step 1 verdict enum | `schemas/__init__.py:209-212` |
| Step 7 tag enum | `schemas/__init__.py:353` |
| Step 9 verdict enum | `schemas/__init__.py:395-398` |
| Step 11 kind enum | `schemas/__init__.py:444-449` |
| MemoryLogger event_type set | `memory_logger.py:47-59` |
| MemoryLogger change_type set | `memory_logger.py:63-69` |
| Closed-set component registry | `base.py:22-30` |
| Closed-set step registry | `base.py:35-47` |
| Refuse-halt branch | `orchestration_runner.py:327-339` |
| Frame-invalid halt branch | `orchestration_runner.py:218-231` |
| Schema/cap exception handlers | `orchestration_runner.py:418-451` |
| BRE mode A tag constant | `components/branching_roadmap_engine.py:47` |
| Governance verdict vocab constant | `components/governance_kernel.py:65` |

## Appendix B — Offline re-baseline artifacts (captured this session)

| Artifact | Path | Bytes |
|---|---|---|
| case_01 stdout | `/tmp/elif_e2_preflight/case_01_stdout.json` | 10,650 |
| case_01 stderr | `/tmp/elif_e2_preflight/case_01_stderr.txt` | 0 |
| case_01 memory JSONL | `/tmp/elif_e2_preflight/case_01_memory/case_01_electroculture/article_vii_tracking.jsonl` | 4,293 |
| case_02 stdout | `/tmp/elif_e2_preflight/case_02_stdout.json` | 9,413 |
| case_02 stderr | `/tmp/elif_e2_preflight/case_02_stderr.txt` | 0 |
| case_02 memory JSONL | `/tmp/elif_e2_preflight/case_02_memory/case_02_policy_governance/article_vii_tracking.jsonl` | 4,325 |
| case_03 stdout | `/tmp/elif_e2_preflight/case_03_stdout.json` | 9,061 |
| case_03 stderr | `/tmp/elif_e2_preflight/case_03_stderr.txt` | 0 |
| case_03 memory JSONL | `/tmp/elif_e2_preflight/case_03_memory/case_03_operational_organizational/article_vii_tracking.jsonl` | 4,437 |

These artifacts are the operator's offline baseline for E.2 comparison.
They should be preserved (e.g. copied to `notes/e2_offline_baseline/`)
before the live run begins, so §3.4's diff has a stable reference.

---

**End of pre-flight pack.**
