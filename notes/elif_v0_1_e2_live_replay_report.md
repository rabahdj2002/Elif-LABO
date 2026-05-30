# ELIF v0.1 — E.2 Live Replay Report

> **Captured:** 2026-05-30
> **Trigger:** operator "Green Light" 2026-05-30 (post-G0 closure + Position B implementation + credential provisioning)
> **Cohort:** case_01_electroculture / case_02_policy_governance / case_03_operational_organizational
> **Mode:** live (offline_mode=False); env var `ELIF_ANTHROPIC_API_KEY`; SDK `anthropic` 0.104.1
> **Procedure version:** v1.0
> **Code state:** commit `e78f57c` on `assia-open/Elif-LABO` main (Position B + env-var rename)
> **Reference baselines:** offline re-baseline at `/tmp/elif_e2_preflight_position_b/`; operator-authored Condition C references at `results/<case_short>/condition_c_output.md`
> **Scope:** EXACTLY as defined in pre-flight pack + Position B addendum. No prompt mods, no procedure mods, no schema mods, no architecture mods, no new cases.

---

## Executive summary

| Surface | Result |
|---|---|
| Procedure survived live execution | **Yes** — 3/3 runs completed without error; no schema fails, no cap exhaustion, no transport errors |
| Position B implementation behaved correctly | **Yes** — `post_refusal_closure` flag correctly = `False` on all 3 (verdict ≠ refuse); all 11 envelopes committed; close event last; no GovernanceRefuseError surfaced |
| Structural similarity vs Condition C reference | **17/18 (0.9444)** on all 3 cases — same as offline re-baseline (no live-vs-offline regression on the replay-signature surface) |
| Step 9 verdict shift | **All 3 live = `constrain`** vs **offline fixtures = `refuse`** — uniform §8.3 verdict shift |
| Step 10 LLM-mode operation | All 3 live cases ran Step 10 via LLM (separator's `separate_operative_from_theoretical` path); operative=6-7 entries, theoretical=5 entries per case; Article IV separation honored |
| Cost actual | **~$0.69-$0.89 cohort total** (33 LLM calls × $0.021-$0.027) — overrun of 10-40% vs §G envelope ($0.57-$0.63) |
| Wall-clock | Parallel: 168s (bounded by slowest case); sequential equivalent: 481s |
| **Gate verdict** | **PASS G1 STRUCTURALLY** — procedure-class evidence is positive. Verdict-class divergence requires operator deliberation (§9). |

---

## §1 Per-case live behaviors

### case_01_electroculture (cluster: scientific/empirical)
| Field | Live | Offline reference |
|---|---|---|
| `exit_code` | 0 | 20 |
| envelopes | 11 (step_1..step_11) | 11 (step_1..step_11) |
| `step_9.verdict` | **`constrain`** | `refuse` |
| `step_9.verdict_detail` (excerpt) | "The Stage 8 roadmap (A1–A5) is authorized to proceed, but only under the following explicit constraints: (1) No stage may advance past its stated gate condition — each gate requires a signed, reviewable deliverable…" | refuse-class detail per offline fixture |
| `step_9.unresolved_uncertainty_sources` count | 5 | 4 |
| `step_10.operative` | 6 entries (live LLM path) | `["refuse bundle"]` (deterministic refuse-closure) |
| `step_10.theoretical` | 5 entries | 4 entries (uncertainty sources from step_9) |
| `step_11.final_verdict` | `constrain` | `refuse` |
| `step_11.post_refusal_closure` | **`False`** | `True` |
| `llm_calls_used` | 11 | 10 |
| Duration | 157s | n/a (offline) |
| MemoryLogger events | 14 | 15 |

### case_02_policy_governance (cluster: policy/governance)
| Field | Live | Offline reference |
|---|---|---|
| `exit_code` | 0 | 20 |
| envelopes | 11 | 11 |
| `step_9.verdict` | **`constrain`** | `refuse` |
| `step_9.verdict_detail` (excerpt) | "The Stage 8 roadmap is authorized to proceed only under the following explicit constraints, which must be satisfied in strict gate-sequential order before confirmatory data collection begins. (C1) Stage A1 must produce a complete institutional inventory…" | refuse-class detail per offline fixture |
| `step_9.unresolved_uncertainty_sources` count | 6 | 3 |
| `step_10.operative` | 7 entries (live LLM path) | `["refuse bundle"]` |
| `step_10.theoretical` | 5 entries | 3 entries |
| `step_11.final_verdict` | `constrain` | `refuse` |
| `step_11.post_refusal_closure` | **`False`** | `True` |
| `llm_calls_used` | 11 | 10 |
| Duration | 156s | n/a |
| MemoryLogger events | 14 | 15 |

### case_03_operational_organizational (cluster: operational/organizational)
| Field | Live | Offline reference |
|---|---|---|
| `exit_code` | 0 | 20 |
| envelopes | 11 | 11 |
| `step_9.verdict` | **`constrain`** | `refuse` |
| `step_9.verdict_detail` (excerpt) | "The Step 8 stage-gated roadmap (A1–A5) is authorized to proceed only under the following explicit constraints: (1) Sequential gate integrity — no stage may begin until its predecessor gate artifact is deposited in a version-controlled, publicly accessible repository…" | refuse-class detail per offline fixture |
| `step_9.unresolved_uncertainty_sources` count | 5 | 3 |
| `step_10.operative` | 7 entries (live LLM path) | `["refuse bundle"]` |
| `step_10.theoretical` | 5 entries | 3 entries |
| `step_11.final_verdict` | `constrain` | `refuse` |
| `step_11.post_refusal_closure` | **`False`** | `True` |
| `llm_calls_used` | 11 | 10 |
| Duration | 168s | n/a |
| MemoryLogger events | 14 | 15 |

---

## §2 Per-case structural similarity (pre-flight pack §6.1 scorer)

Using `_reference_signature` + `_replay_signature` from `src/elif_v0_1/replay/__init__.py`:

| Case | Live similarity | Offline similarity | Threshold | Pass? |
|---|---|---|---|---|
| case_01 | **0.9444** (17/18) | 0.9444 (17/18) | ≥ 0.83 | ✅ |
| case_02 | **0.9444** (17/18) | 0.9444 (17/18) | ≥ 0.83 | ✅ |
| case_03 | **0.9444** (17/18) | 0.9444 (17/18) | ≥ 0.83 | ✅ |

**Live and offline tied at 0.9444 on all 3 cases.** The verdict-class shift (refuse → constrain) does NOT reduce structural similarity because the §6.1 scorer measures presence of behavior categories (verdict present? uncertainty present? stages with gates? etc.), not verdict-value equality. The §6.1 scorer is doing what it was designed to do: detect structural drift, not opinion drift.

---

## §3 Per-case missing or unexpected behaviors

**Missing on both live AND offline (pre-existing replay-signature mismatch, not E.2 finding):**
- `step_11_entries_present` — the replay-signature looks for `step_outputs["step_11"]["entries"]`, but `orchestration_runner` populates `step_11` with a `run_summary` dict (no `entries` key). This is a known shape mismatch between `_replay_signature` expectations and what the runner actually writes; it is NOT a Position B regression and was present in the offline baseline. **Action: record; pre-existing carry-forward; do not patch under Authorization 3 freeze.**

**Missing on live only:** none.

**Unexpected on live:** none (no behavior signature triggered that the reference does not authorize).

---

## §4 Per-case memory log composition

Live memory events per case (read from `/tmp/elif_e2_live/<case>/<case_id>/article_vii_tracking.jsonl`):

```
case_01 / case_02 / case_03  (each):
    1 × open
    12 × step_committed  (step_1..step_7_modeB, step_7, step_8, step_9, step_10, step_11)
    1 × close             (exit_code=0)
    = 14 events per case
```

**Key observation:** no `refutation` event on any live case — consistent with non-refuse verdict (refutation is only emitted on the refuse-branch per Position B). Offline cases had 15 events each (one extra `refutation`). The 14-vs-15 delta is the canonical Position B refuse/non-refuse signature, not a regression.

`close` is the last event on all 3 live cases. Event ordering is consistent with the `TestRunnerPositionBEventOrdering` invariant.

---

## §5 Per-case cost burn

| Case | LLM calls | Cost @ $0.021 | Cost @ $0.027 | Duration |
|---|---|---|---|---|
| case_01 | 11 | $0.231 | $0.297 | 157s |
| case_02 | 11 | $0.231 | $0.297 | 156s |
| case_03 | 11 | $0.231 | $0.297 | 168s |
| **Cohort** | **33** | **$0.69** | **$0.89** | 168s wall (parallel) / 481s serial |

**Pre-flight pack §G projection:** $0.57-$0.63/cohort. **Actual:** $0.69-$0.89/cohort. **Overrun:** 10-40%. **Cause:** 11 calls/case actual vs ~10 calls/case projected (one extra call/case — likely the Step 7 mode-B FrameValidator call, which counts but isn't deeply discussed in the §5.1 projection arithmetic). Per-run `--max-llm-calls 22` cap was NOT hit on any case; ample headroom remained.

---

## §6 Differentiator survival (pre-flight pack §6.5)

Per-step structural anchors held under live execution:

| Step | Anchor | Live | Held? |
|---|---|---|---|
| 1 | verdict in `{valid, invalid, needs_decomposition}` | needs_decomposition × 3 | ✅ |
| 2 | ≥ 2 axes per case | ≥ 2 axes × 3 | ✅ |
| 4 | each hypothesis has `distinguishing_prediction` | yes × 3 | ✅ |
| 7 mode A | `outside-original-frame` tag | present × 3 | ✅ |
| 8 | stages each carry `continuation_gate` | present × 3 | ✅ |
| 9 | verdict in `{constrain, refuse, explicitly_abstain}` | `constrain` × 3 (closed-set respected) | ✅ |
| 9 | `unresolved_uncertainty_sources` count ≥ 1 | 5-6 per case | ✅ |
| 10 | live path runs both `operative` and `theoretical` non-empty | 6-7 op / 5 theo per case | ✅ |
| 11 | `post_refusal_closure` boolean present + correctly False | True × 3 (correctly False on non-refuse) | ✅ |

**All 9 structural anchors survived. No closed-set drift. No schema failures.**

---

## §7 Architecture vs model dependence (pre-flight pack §6.4)

The divergence pattern signals **model-dependent** behavior, not architecture-dependent:

- All 3 cases shifted in the same direction (refuse → constrain). If it were architecture-dependent (drift in our prompts / schemas / procedure), we would more likely see heterogeneous failures.
- The model's `verdict_detail` and Step 10 operative lists are substantive — not "yes, looks fine" but "proceed under these specific gates with these specific deliverables required at each gate." This is the model making a different judgment call on a well-formed procedural surface, not the procedure breaking.
- Position B's tripwires fired correctly (`post_refusal_closure=False`) — the architecture surfaced the shift, it did not mask it.

The 17% structural-similarity gap discussed in the G0 package §6 (the delta between alpha output's 9 envelopes and Condition C reference's 11 envelopes under Position A) is now **structurally closed** under Position B: all 3 live runs produced 11 envelopes regardless of verdict. Whether the closed gap reflects semantic equivalence with the operator-authored reference is a separate question (see §9).

---

## §8 Cohort verdict

**STRUCTURAL: PASS G1.**

The procedure survived contact with a real frontier model. All schema validations passed. All closed-set vocabularies were respected. Position B implementation behaved correctly under live load. The §6.1 structural-similarity scorer cleared the 0.83 threshold on all 3 cases. Cost stayed within an acceptable envelope (10-40% above projection but well below cap).

**VERDICT-CLASS: HETEROGENEOUS WITH OPERATOR REFERENCE.**

The model returned `constrain` × 3 where the operator-authored Condition C reference returns `refuse` × 3. This was pre-classified as "plausible" by pre-flight pack §7 (Step 9 verdict row) and explicitly handled by §8.3 ("Verdict shift; record; compare; do not over-react"). The model's `constrain` reasoning is non-trivial: each case carries 5-6 unresolved uncertainty sources at Step 9 and 5-7 substantive operative actions at Step 10. This is not "constrain-as-rubber-stamp"; the model is genuinely imposing procedural conditions.

**RECOMMENDATION: PASS G1 GATE; CARRY FORWARD VERDICT-CLASS DIVERGENCE FOR OPERATOR DELIBERATION.**

---

## §9 Operator decision points surfaced

The structural pass is unambiguous. The verdict-class shift is the substantive operator decision.

### D.1 — Is the model's `constrain` reading doctrinally acceptable for these 3 cases?

The model treats each case as a bundleable proposal that can proceed under named gate-conditions. The operator's Condition C reference treated each case as a bundle whose structure itself was the problem (→ refuse). Two readings:

- **Pro-constrain:** The model is reasoning correctly about how a real institution operates. Each case has actionable gate criteria; refusing would lose the value of the stage-gated decomposition entirely.
- **Pro-refuse:** The operator's reference came from a position the model lacks — recognition that the bundle structure itself is what makes the cases hostile to good-faith governance, not the absence of gates.

This is **not a question E.2 can answer**. E.2 measures whether the procedure produced structurally valid output under live load. It did. Whether the model's substantive judgment matches the operator's reference is a deliberation, not an evidence point.

### D.2 — What follows from Phase 1 closure?

Per audit synthesis §4.1, Phase 1 closes when this report is written + operator confirms acceptance. The operator's Green Light declared the next operator decision will be taken only after reading this report. Options:

- **Accept E.2 evidence + close Phase 1.** ELIF returns to review state per Authorization 3.
- **Accept structural pass + flag verdict-class divergence for further investigation.** Closes Phase 1 procedurally but signals additional evidence-collection (e.g., Cluster-aligned recomputation, multi-frontier-family replay) before Phase 2.
- **Reject; demand more evidence before closure.** Plausible reasons: cohort size n=3 too small; single-model-family insufficient; replay-signature step_11 regression unresolved.

### D.3 — Carry-forward items (no operator action required for E.2 gate; for record)

- **Replay-signature step_11 mismatch (§3).** Known issue; pre-existing. Should be patched if/when implementation re-opens.
- **Cost overrun (§5).** 10-40% above §G projection. Could refine cost projection in pre-flight pack with the 11-call/case empirical number.
- **One-cohort baseline.** Three cases × one frontier model × one date = small-N. The MOST INTERESTING question for ELIF — whether the verdict-class shift is stable across model families, dates, and frame variants — is unanswered.

---

## §10 What this report does NOT include

- **Re-runs.** Each case ran once; no retry. Re-runs would require fresh authorization.
- **Per-step JSON byte-diff.** The §6.1 similarity surface is sufficient for the G1 gate; full per-step diffs are available at `/tmp/elif_e2_live/case_*_stdout.json` and `/tmp/elif_e2_preflight_position_b/case_*_stdout.json` if needed.
- **Multi-model comparison.** Only the default Anthropic model (per llm_adapter) was exercised. Multi-family is a Phase-5 question per pre-flight pack §6.4.
- **Doctrinal adjudication.** §9 surfaces the verdict-class question; it does not answer it.
- **Phase 1 closure decision.** The Green Light authorized E.2 execution + report. Closing Phase 1 is the operator's call after reading.

---

## References

- Position B G0 decision: [elif_g0_decision.md](elif_g0_decision.md)
- Position B implementation commit: `44b3e6e`
- E.2 readiness addendum: [elif_e2_live_replay_preflight_pack_position_b_addendum.md](elif_e2_live_replay_preflight_pack_position_b_addendum.md)
- Original pre-flight pack (Position A baseline): [elif_e2_live_replay_preflight_pack.md](elif_e2_live_replay_preflight_pack.md)
- §6.1 similarity scorer source: [src/elif_v0_1/replay/__init__.py](../src/elif_v0_1/replay/__init__.py)
- Live run artifacts: `/tmp/elif_e2_live/case_{01,02,03}_stdout.json` + per-case JSONL event logs
- Offline re-baseline artifacts: `/tmp/elif_e2_preflight_position_b/case_*_stdout.json`

---

**Report closed. G1 structural gate PASSED. Verdict-class divergence FLAGGED. Awaiting operator's Phase-1-closure decision.**
