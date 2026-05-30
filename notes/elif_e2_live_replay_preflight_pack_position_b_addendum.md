# ELIF E.2 Live-Replay Pre-flight Pack — Position B Addendum

> **Captured:** 2026-05-30
> **Status:** PRE-FLIGHT (ANTHROPIC_API_KEY still UNSET in this sandbox — live execution remains operator-gated).
> **Supersedes (where named):** specific subsections of [elif_e2_live_replay_preflight_pack.md](elif_e2_live_replay_preflight_pack.md) that were authored under Position A and are now invalidated by the G0 Position B implementation committed at `44b3e6e`.
> **Doctrinal frame:** see [elif_g0_decision.md](elif_g0_decision.md). Position B = Step 10 + Step 11 fire as post-refusal closure on refuse-cases. The verdict itself remains `refuse`; the closed-set vocabulary `{constrain, refuse, explicitly_abstain}` is frozen.

This addendum is the **delta** between the existing pre-flight pack (which assumed Position A control flow) and the post-implementation behavior. The §1 (environment), §3 (live command bundle), §4 (schema / closed-set drift), §5 (cost-cap), §6 (analysis pipeline shape), §10 (out-of-scope), Appendix A/B all remain valid as written. Only the surfaces named below need to be read against this addendum.

---

## A. Surfaces that change under Position B

| Pack section | Pre-flight pack claim | Position B reality |
|---|---|---|
| §2.2 Per-case results offline | Each case: `exit_code=20`, **9 envelopes**, last step `step_9` | Each case: `exit_code=20`, **11 envelopes**, last step `step_11` |
| §2.5 Memory-event composition offline | per-case: 1 open + 10 step_committed (1..7, 7_modeB, 8, 9) + 1 refutation + 1 close = **13** | per-case: 1 open + 12 step_committed (1..7, 7_modeB, 8, 9, 10, 11) + 1 refutation + 1 close = **15** |
| §7 Behavioral comparison matrix | refuse-case rows reference Step 9 as terminal commit | refuse-case rows: Step 9 still has `verdict=refuse`; Step 10 + Step 11 also commit and carry the `post_refusal_closure=True` marker on the Step 11 run_summary |
| §8.5 LLMCallCapError on refuse-cases | n/a — refuse halts before Step 10 | Step 10 on the refuse-branch is **deterministic (no LLM call)**; Step 11 was already no-LLM. LLMCallCapError on a refuse-case run can only fire in Steps 1–9. |
| §5.1 Live-mode cost projection | Refuse-cases consume Steps 1–9 LLM calls; Step 10 + Step 11 not consumed | **Unchanged.** Step 10 on refuse-branch is deterministic; Step 11 was already deterministic. Live cost envelope per refuse-case is identical pre/post Position B. |

Result: **the cost envelope from §5 is preserved verbatim.** The only behavioral artefacts that change are envelope count (9 → 11), memory-event count (13 → 15), and the presence of Step 10 + Step 11 outputs as additional structural anchors.

---

## B. Refreshed offline re-baseline `[CE]`

Re-ran the offline control re-baseline against the Position B implementation (commit `44b3e6e`). Artifacts live at `/tmp/elif_e2_preflight_position_b/`.

```
case_01_electroculture           → exit_code=20, step_outputs=11, memory_events=15
case_02_policy_governance        → exit_code=20, step_outputs=11, memory_events=15
case_03_operational_organizational → exit_code=20, step_outputs=11, memory_events=15
```

Memory-event sequence verified on disk per case:

```
open
step_committed(step_1)
step_committed(step_2)
step_committed(step_3)
step_committed(step_4)
step_committed(step_5)
step_committed(step_6)
step_committed(step_7_modeB)   # forensic log (mode B not in RunReport)
step_committed(step_7)         # mode A (committed envelope)
step_committed(step_8)
step_committed(step_9)         # verdict=refuse
refutation                     # G0 Position B: refusal preserved
step_committed(step_10)        # constrained refuse-bundle (no LLM call)
step_committed(step_11)        # run_summary with post_refusal_closure=True
close                          # exit_code=20, end-of-run
```

Refutation precedes Step 10 commit; close is the last event in the log. Both ordering invariants are pinned by `TestRunnerPositionBEventOrdering` in `tests/test_orchestration_runner.py`.

---

## C. Step 10 + Step 11 deterministic anchors (refuse-branch only) `[CE]`

When Step 9 returns `verdict=refuse`, the offline output is deterministic and can be diffed structurally against live output. The pre-existing §2.3 anchors stand; these add to them:

**Step 10 anchors (refuse-branch):**
- `operative == ["refuse bundle"]` (exact value, single-element list)
- `theoretical` is a list of strings — the `unresolved_uncertainty_sources` array from Step 9, in order, with non-string / empty entries filtered out
- `absence_log` is a non-empty string beginning with `"Post-refusal closure (G0 Position B):"`
- `llm_calls_used` reported on the step_10 envelope is unchanged from step_9 envelope (no LLM call consumed)

**Step 11 anchors (refuse-branch):**
- `final_verdict == "refuse"`
- `post_refusal_closure == True`
- `step_count == 10` (the number of envelopes committed before step_11 itself is appended — this is the pre-existing summary semantic, not changed by Position B)
- `run_id` matches the run_context's run_id
- `llm_calls_used` unchanged from step_10 envelope

**Step 11 anchors (non-refuse / clean run):**
- `final_verdict ∈ {"constrain", "explicitly_abstain"}`
- `post_refusal_closure == False`

These five additional structural anchors compose with the §2.3 anchors to give the per-case offline reference its full Position B shape.

---

## D. Live-replay command bundle — Position B confirmation

The §3 command bundle (live execution after `ANTHROPIC_API_KEY` is set) is unchanged. Per-case live commands still use:

```bash
PYTHONPATH=src python3 -m elif_v0_1.cli run \
    --case case_01_electroculture --condition c \
    --max-llm-calls 22 \
    --results-dir /tmp/elif_e2_live/case_01
# (omit --offline for live mode)
```

**What changes in the expected output:**
- Each refuse-case run is expected to commit 11 envelopes (Steps 1–11), not 9
- `memory_logger_entries_written` is expected to be ≥ 14 per case (was ≥ 12 pre-Position B)
- `exit_code` remains 20 on refuse-cases

**What does NOT change:**
- Number of LLM calls per refuse-case (still ≤ 10, set by Steps 1–9)
- Cost envelope per refuse-case (Step 10 on refuse-branch is deterministic; Step 11 was already deterministic)
- Step 9 verdict closed-set
- Closed-set vocabulary `{constrain, refuse, explicitly_abstain}`

---

## E. Failure-mode list — Position B additions to §8

The pre-flight pack §8 failure-mode map remains the canonical reference. Position B introduces two additional failure surfaces specific to the refuse-branch:

### E.1 Step 10 schema validation fail on refuse-branch

`OperativeTruthSeparator.separate_for_refusal()` runs the same `validate_against_schema(payload, STEP_10_OUTPUT_SCHEMA)` + `_enforce_step10_semantics(payload)` as the live path. If the schema or semantic rules drift (a future PR widens STEP_10_OUTPUT_SCHEMA in a backwards-incompatible way), the refuse-branch Step 10 will raise `SchemaValidationError` and the run halts with `exit_code=30` per the existing `except SchemaValidationError` handler.

**Diagnostic signal:** `SchemaValidationError` raised from `separate_for_refusal` at `operative_truth_separator.py` line range ~160–192 in commit `44b3e6e`.

**Operator action:** treat as schema-drift; do not edit the refuse-branch payload to suppress; investigate schema diff first.

### E.2 Step 11 records `post_refusal_closure=True` on a non-refuse run

This should be impossible given the in-band flag is set from `step_9.get("verdict") == "refuse"`. If it surfaces, it indicates the runner's `refuse_branch` flag was mis-computed (e.g. verdict closed-set drifted such that a non-refuse string compared truthy against `"refuse"`).

**Diagnostic signal:** `post_refusal_closure=True` in `run_summary` with `final_verdict ∉ {"refuse"}`.

**Operator action:** halt analysis; re-read Step 9 verdict on the affected case; check for closed-set drift in `governance_kernel`.

### E.3 GovernanceRefuseError surfaces from elsewhere

The runner no longer raises `GovernanceRefuseError` from the refuse-branch (the raise was removed by commit `44b3e6e`). The exception class and the `except GovernanceRefuseError` handler at `orchestration_runner.py:408-417` remain — they are now defensive code that catches the exception if any **other** component raises it directly. Under E.2 this handler should NEVER fire.

**Diagnostic signal:** `RunReport.exit_code == 20` AND `len(step_outputs) < 11` AND step_9 was committed cleanly.

**Operator action:** identify which component raised `GovernanceRefuseError`; this is a regression of the Position B implementation contract.

---

## F. Offline-vs-live comparison framework — Position B refinements

The pre-flight pack §6 analysis pipeline specifies per-step JSON divergence + structural similarity. Under Position B, two additional cross-checks become available on refuse-cases:

### F.1 Step 10 should be **identical** offline vs live on refuse-branch

Because `separate_for_refusal` is deterministic and bypasses the LLM, the Step 10 envelope on a live refuse-case must equal the offline reference Step 10 envelope **byte-for-byte** modulo:
- `committed_at_iso` (timestamp varies)
- `llm_calls_used` (varies with prior live calls 1–9)
- Order of `theoretical` entries (should match Step 9 ordering exactly)

Any non-timestamp / non-llm-count delta in Step 10 between offline and live is a P0 signal of broken determinism on the refusal path.

### F.2 Step 11's `post_refusal_closure` flag is a binary cross-validator

For each case:
- Offline: refuse-branch → `True`; non-refuse → `False`
- Live: must match offline on the same case

If offline=`True` and live=`False` for the same case, this means the live verdict at Step 9 diverged from the offline fixture (live did NOT refuse). This is the canonical "verdict shift" surface from §8.3 — Position B gives it a single-field tripwire on Step 11.

### F.3 Structural similarity ceiling raises slightly

The pre-flight pack §6.1 sets the per-case similarity threshold at ≥ 0.83 (decision §8.13). Under Position B, refuse-cases gain 2 additional envelopes (Step 10 + Step 11) whose offline-vs-live similarity is expected to be ~1.0 (Step 10) and ~1.0 modulo timestamp (Step 11). The empirical similarity ceiling on refuse-cases is therefore expected to be **higher** than the Position A baseline; if the per-case similarity falls below the 0.83 threshold the cause is almost certainly in Steps 1–9 (where LLM-generated content varies), not Steps 10–11.

---

## G. Cost envelope confirmation

The pre-flight pack §5.1 projects ~$0.21/case live-mode cost. Under Position B:

- Refuse-cases: LLM calls 1–9 unchanged; Step 10 deterministic (was 1 LLM call); Step 11 deterministic (was 0 LLM calls). **Net savings of one Step 10 LLM call per refuse-case live-mode**, or roughly $0.02/case at ELIF v0.1 prices.
- Non-refuse cases: identical LLM-call profile to pre-Position-B.

**Refreshed projection:** $0.19/case on refuse-cases, $0.21/case on non-refuse cases. The §5.1 cost cap (default $0.50/case × 3 = $1.50 per E.2 run) remains comfortably above the projection.

The `--max-llm-calls 22` cap at the CLI is **unchanged** and remains the binding constraint. The cap is enforced by the same code path as before (`reset_call_counter()` + per-call increment); no Position B change touches the cap mechanism.

---

## H. Final live-replay execution checklist

When `ANTHROPIC_API_KEY` becomes available, the operator runs the following checklist in order. All steps are operator-driven; nothing fires autonomously.

1. **Environment** (pre-flight pack §1)
   - [ ] `echo $ANTHROPIC_API_KEY | wc -c` returns a non-trivial length
   - [ ] `python3 -c "from elif_v0_1.orchestration_runner import ProcedureRunner; ProcedureRunner()"` succeeds with no import errors
   - [ ] `python3 -m unittest discover -s src/elif_v0_1/tests` reports 238 pass, 3 skip

2. **Offline re-baseline immediately before live** (pre-flight pack §2 + this addendum §B)
   - [ ] Run all 3 cases offline; capture stdout to `/tmp/elif_e2_offline_baseline/`
   - [ ] Verify each case has 11 envelopes, `exit_code=20`, `post_refusal_closure=True` on Step 11
   - [ ] Verify each case's MemoryLogger JSONL has the canonical 15-event sequence with `close` last

3. **Live run, case-by-case** (pre-flight pack §3)
   - [ ] Case 01 live → capture stdout to `/tmp/elif_e2_live/case_01_stdout.json`
   - [ ] Case 02 live → capture stdout to `/tmp/elif_e2_live/case_02_stdout.json`
   - [ ] Case 03 live → capture stdout to `/tmp/elif_e2_live/case_03_stdout.json`
   - [ ] For each: record actual LLM-call count, actual cost (if API returns billing headers), wall-clock duration

4. **Diff vs offline baseline** (pre-flight pack §3.4 + this addendum §F)
   - [ ] Step 9 verdict equality: live `verdict` ∈ `{constrain, refuse, explicitly_abstain}` per case
   - [ ] If live verdict on a case = `refuse`: Step 10 should match offline byte-for-byte modulo timestamp + `llm_calls_used` + `theoretical` order; `post_refusal_closure=True` on Step 11
   - [ ] If live verdict on a case ∈ `{constrain, explicitly_abstain}`: Step 10 LLM call fires; Step 11 `post_refusal_closure=False`
   - [ ] Per-case structural similarity ≥ 0.83 (§6.1)

5. **Report** (pre-flight pack §6.6)
   - [ ] Author `notes/elif_v0_1_e2_live_replay_report.md` per the §6.6 shape
   - [ ] Capture per-case verdict + similarity + cost + duration in a table
   - [ ] Flag any divergence per §8 failure-mode map (including this addendum's §E additions)

6. **Decision**
   - [ ] Operator reads the report
   - [ ] Operator decides: pass E.2 evidence gate (proceed to Phase 1 close) OR flag for re-runs / investigation

---

## I. What this addendum does NOT include

- **Live execution.** `ANTHROPIC_API_KEY` is still unset in this sandbox; nothing live was run.
- **Architecture change.** No new component, no new Article, no new procedure step, no v0.5.
- **Schema expansion.** STEP_10_OUTPUT_SCHEMA unchanged. Closed-set verdict vocabulary unchanged.
- **Roadmap activation.** Phase 1 (E.2 live replay) remains operator-gated. This addendum prepares for it; it does not open it.
- **V2 / world-model work.** Out of scope per Authorization 3 (ELIF re-freeze).

---

## J. References

- [elif_g0_decision.md](elif_g0_decision.md) — G0 adjudication record (Position B, 2026-05-30)
- [elif_e2_live_replay_preflight_pack.md](elif_e2_live_replay_preflight_pack.md) — original pre-flight pack (Position A baseline)
- Commit `44b3e6e` — Position B implementation (runner + separator + tests)
- Test coverage: `TestRunnerPositionBEventOrdering`, `TestRunnerCleanRunStillExits0`, `TestPositionBRefusalPath` (all in `src/elif_v0_1/tests/`)

---

**Addendum closed. E.2 readiness restored under Position B. Live execution awaits operator + `ANTHROPIC_API_KEY`.**
