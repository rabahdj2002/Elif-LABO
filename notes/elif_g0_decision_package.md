# G0 Decision Package — Refuse-Halt Adjudication

> **Captured:** 2026-05-30
> **Status:** Operator decision package. No recommendation. No advocacy. Binary positions surfaced side-by-side; trade-offs anchored to substrate; doctrinal implications named per Article. The operator decides; this document does not.
> **Authority:** Adjudication-staging. Cannot resolve G0; can only present the two positions in maximally legible form against existing Articles, schemas, and runner code.
> **Discipline constraint:** Non-expansionary. No v0.5. No new component. No new Article. No new procedure step. No world-model implementation. No roadmap expansion. No speculative phase activation. No pattern adoption beyond evidence. No architecture inflation.
> **Evidence basis:** v0.1 alpha replay (`elif_v0_1_alpha_replay_report.md`), cost+complexity report (`elif_v0_1_alpha_cost_complexity_report.md`), audits A/B/C, synthesis (`elif_audit_synthesis.md` §1.3, §2.3, §2.7, §4.0).

---

## 1. Question Statement

**G0 (verbatim):** Should ELIF's orchestration runner halt at Step 9 when `verdict=refuse` (Position A — status quo as shipped in v0.1-alpha), or continue running Step 10 + Step 11 as post-refusal closure (Position B)?

### 1.1 The code path under question

In `src/elif_v0_1/orchestration_runner.py`, after `governance_kernel.verdict_with_confidence_and_uncertainty(...)` commits Step 9 (line ~325), the following branch fires:

```
if step_9.get("verdict") == "refuse":
    self._emit_refutation(memory_logger, run_context, trigger="governance_refuse", ...)
    self._emit_close(memory_logger, run_context, exit_code=20)
    raise GovernanceRefuseError("Step 9 returned verdict=refuse; halting run")
```

The exception is caught in the outer `try/except`, which returns a `RunReport` with `exit_code=20`, `step_outputs=tuple(step_envelopes)` (containing envelopes for steps 1–9 only), and `completed_at_iso`. Steps 10 and 11 are not invoked; their `commit_step` calls and `memory_logger.write_event` payloads for those step_ids are never reached.

This is the entire surface of G0. The question is whether to retain this branch, modify it (Position B: continue), or both retain it while permitting Step 10/11 to run as post-refusal closure (the Position B framing that preserves Article V's halt semantics by re-defining what "halt" includes).

### 1.2 Schemas involved

Three schemas are load-bearing for G0:

- **`step_9`** — the governance-kernel output. Closed-set verdict ∈ `{constrain, refuse, explicitly_abstain}`; `unresolved_uncertainty_sources` has `minItems=1`; `confidence_qualifier` is free-text tied to at least one named uncertainty source. Under both Position A and Position B, Step 9's schema is unchanged.
- **`step_10`** — the operative-truth separator output. Validates an object with `operative` list, `theoretical` list, and optional `absence_log`. Fixtures `step_10__case_*.json` exist and validate. Under Position A, this schema is never invoked at runtime in the refuse-path; under Position B, it is.
- **`step_11`** — the memory-logger summary envelope plus the MemoryLogger event payloads. Closed-set `event_types` includes `judgment_act` derivative entries via `change_type` enum `{arbitration_shortcut_added, framework_candidate_emerged, composition_path_discovered, pattern_recognition_added, judgment_act_logged}`. Under Position A, the runner already emits `open`, `step_committed × 9`, `step_7_modeB`, `refutation`, and `close` events for refuse-cases (per alpha replay §case_01.6: 14 events written) — but Step 11's own content-pass (judgment_act / pattern_engaged / capacity_change) does not fire because Step 11 itself is not reached. Under Position B, those content-pass entries become reachable on the refuse-path.

### 1.3 Concrete runtime code changes required by each Position

Under Position A, no code changes are required; the runner is already shipped in this shape.

Under Position B, the minimum runtime code change set is:

1. Restructure the `raise GovernanceRefuseError(...)` in the refuse-branch of `orchestration_runner.py` line ~338. Replace with a flag (`refuse_path=True`) that allows execution to continue into Step 10 + Step 11 while still emitting the `refutation` event.
2. Move the `_emit_close(exit_code=20)` call from inside the refuse-branch to after Step 11 commits, so the close-event timestamp reflects the actual end of the procedure (post-closure rather than mid-procedure).
3. Optionally adjust `_emit_refutation` ordering relative to Step 10/11 (operator sub-decision: should refutation log before or after closure?).
4. Update the outer `try/except GovernanceRefuseError` handler since the exception no longer fires on refuse; the RunReport must be assembled in the normal flow with `exit_code=20` (or new code) on refuse-and-closure-completed.
5. Optionally extend `operative_truth_separator.separate_operative_from_theoretical` to accept a `refuse_path: bool = False` keyword so the prompt can be specialized for refuse-cases (emit `operative=["refuse bundle"]` without an LLM call, or with a refuse-specialized prompt; operator sub-decision).
6. Update `test_orchestration_runner.py` assertions (envelope count 9 → 11 on refuse-cases; exit_code semantics; refutation event ordering).

Estimated LoC delta: 30–80 LoC in `orchestration_runner.py`, 0–40 LoC in `operative_truth_separator.py`, 50–150 LoC in tests. Total: <300 LoC. No schema changes. No new component. No new Article. No new procedure step.

### 1.4 Test cases where each Position differs behaviorally

Under the alpha-fixture set, all three operator-locked cases (`case_01_electroculture`, `case_02_policy_governance`, `case_03_operational_organizational`) produce `verdict=refuse` at Step 9 (per `elif_v0_1_alpha_replay_report.md` §case_01.3 / §case_02.3 / §case_03.3, each 0.83 structural similarity). Every existing test case differs behaviorally between A and B:

- **case_01** — A: 9 step envelopes, exit_code 20, no Step 10 / Step 11 content. B: 11 step envelopes, exit_code (TBD — either still 20 with closure markers, or new closure code), Step 10 operative=`["refuse bundle"]` + theoretical=`[uncertainty sources from Step 9]`, Step 11 content entries logged.
- **case_02** — identical shape of divergence; same uncertainty-source-list and operative/theoretical mapping pattern.
- **case_03** — identical shape of divergence.

Cases authored later (Phase 3 in `elif_audit_synthesis.md` §4.3) that produce `verdict=constrain` or `verdict=explicitly_abstain` would NOT differ between A and B at the runtime level: under both positions, Step 10 and Step 11 fire on non-refuse verdicts. The behavioral divergence is exclusively on the refuse-path.

---

## 2. Implications Table

The following side-by-side table is presented without ranking, weighting, or recommendation. Each row is a substrate-anchored implication, not an argument.

| Aspect | Position A (status quo) | Position B (post-refusal closure) |
|---|---|---|
| Runner exit code on refuse | 20 (`GovernanceRefuseError`) | 20 (same code) OR a new code (e.g., 21 for "refuse with closure") — operator-decision sub-question |
| Step 10 fired on refuse? | No (runner raises before reaching Step 10) | Yes; operative=`["refuse the bundle"]`, theoretical=`[uncertainty sources from Step 9]` (per `elif_v0_1_alpha_replay_report.md` recommendation surfaced §247) |
| Step 11 fired on refuse? | No (same halt path) | Yes; capacity_change entries describing pattern engaged in declining the bundle |
| MemoryLogger content_pass entries on refuse case? | None (only `open`, 9× `step_committed`, `step_7_modeB`, `refutation`, `close` — 14 events per alpha §case_01.6) | Includes `judgment_act` + `pattern_engaged` + `capacity_change` entries (closed-set change_types per memory_logger.py `_VALID_CHANGE_TYPES`) |
| Memory of refused case for future cross-case influence? | Persisted via `refutation` event_type + uncertainty sources in Step 9 step_committed payload; no `pattern_engaged` or `capacity_change` content | Persisted via the same refutation/open/close substrate PLUS Step 11 content-pass entries; richer cross-case signal |
| Theoretical claims from refused case recorded? | No structured `theoretical` array (Step 10 not invoked); uncertainty sources in Step 9 payload are present but not in operative/theoretical schema shape | Structured `theoretical` array per `step_10` schema; future world-model schema-seam (Phase 7) would have a target to populate |
| User-facing closure stage exists? | No structural closure; refuse halts mid-procedure from the user's surface viewpoint; `refutation` event is the closure-event-as-emitted | Structural closure exists; operative/theoretical separation is rendered; capacity-change record is rendered |
| Schema bytes changed? | No | No (the existing `step_10` and `step_11` schemas already accept the post-refusal closure payload shape per alpha §case_01.7) |
| Procedure version remains v1.0? | Yes | Yes (per the recommendation surfaced in `elif_v0_1_what_remains.md` §3 — schema validation passes under either path; the change is runner code only) |
| Cost per case (live mode) | ~$0.21 (per `elif_v0_1_alpha_cost_complexity_report.md` §1.2) — Step 9 governance call ends LLM use on refuse | ~$0.21 + Step 10 LLM call (~$0.03–0.05 estimated additional, by step-cost proportion) = ~$0.24–0.26 (Step 11 is no-LLM); under 22-call cap with headroom |
| Behavioral change on case_01 | None from status quo; exit 20 with 9 envelopes | 11 envelopes; closure record visible; `theoretical` array populates with electroculture uncertainty sources |
| Behavioral change on case_02 | None | 11 envelopes; closure record populates with reversibility / actor-incentive uncertainty sources |
| Behavioral change on case_03 | None | 11 envelopes; closure record populates with consent-profile / persistence uncertainty sources |
| Structural similarity vs operator-authored Condition C reference | 0.83 (alpha-measured) | Rises toward ~1.0 (the 17% gap from §case_01.4 / §case_02.4 / §case_03.4 closes; per `elif_v0_1_what_remains.md` §6) |
| V1 closure-surface availability | No closure surface in V1 refuse-path UX (per `elif_audit_b_user_experience.md` §B3.2(c)) | Closure surface available in V1 refuse-path UX |
| V2 cross-case dashboard substrate availability | Dashboard inputs incomplete: no `judgment_act` / `pattern_engaged` / `capacity_change` on refuse-cases (per `elif_audit_c_media_communication.md` §C6.2) | Dashboard inputs complete: cross-case content-pass operational |
| Sterile-equilibrium detector input completeness | `capacity_change_records` count is zero across all refuse-cases (per memory_logger.py read_case_state aggregation) — detector input is partial | `capacity_change_records` populated; detector input complete |
| Future-case reuse signal | `reuse_detected` event-type infrastructure exists in MemoryLogger but the cross-case substrate from refused cases is thin (only the `refutation` payload and Step 9 step_committed payload contribute) | Cross-case substrate is richer; pattern-recognition emission has structured content to compare against |
| Test suite impact | `test_orchestration_runner.py` continues to assert exit_code=20 with 9-envelope tuple length on refuse-cases; no test changes required | `test_orchestration_runner.py` requires updates: envelope-count assertion changes (9 → 11), Step 10 / Step 11 commit-events must be asserted, refutation event ordering may need re-specification |
| Schema fixture coverage | Step 10 / Step 11 fixtures (`step_10__case_*.json`, `step_11__case_*.json`) exist but are not exercised by the runner on refuse-path; replay harness loads them when the runner branch reaches them (never, in alpha) | Existing fixtures are exercised; the offline replay path naturally validates the closure shape against the same fixtures already in `src/elif_v0_1/offline_fixtures/` |
| Replay harness changes | None; replay terminates as currently coded | Minor; the replay harness must permit Step 10 / Step 11 fixture loading after a refuse verdict (verify in `replay/__init__.py` — the 689 LoC harness has a per-component fallback path that should already support this) |
| Article VII benchmark feasibility (per `elif_constitutional_layer.md` §156) | Persistence-infrastructure-level benchmark is met; content-level benchmark (faster arbitration on similar-shape, compositional reuse, pattern recognition without sovereignty) cannot be tested cross-refuse-case | Content-level benchmark gains a refuse-case surface; cross-case capacity observability becomes testable on the all-refuse alpha cohort |
| 17% structural-similarity gap closure (alpha) | Gap remains; the 17% is exactly the Step 10 + Step 11 + content-pass delta against the operator-authored reference | Gap closes toward ~1.0; reference is approximately matched on the same fixture set |

The table is exhaustive of the implications surfaced across the three audits + the alpha replay report + the runner code. No row reflects an inference beyond cited substrate.

---

## 3. Doctrine Implications

Per the seven Articles (v0.4 doctrine, from `elif_constitutional_layer.md` §31–43). For each Article: what does Position A preserve, what does Position B preserve, what does each strain. No ranking.

### Article I — Non-Absolutization of Intelligence

- **Position A preserves:** the runner does not let any output (including a refuse verdict's downstream commentary) claim a closure shape larger than the refusal warrants. The refuse-halt is the most architecturally austere expression of "refutation conditions accompany every output" — the procedure simply stops.
- **Position B preserves:** if Step 10 runs and populates `theoretical` with uncertainty sources, the resulting envelope explicitly carries the refutation conditions in the `theoretical` array — a more legible enumeration of partiality than absence.
- **Position A strains:** none directly (Article I is structurally protected by closed-set verdict vocabulary at Step 9, not by what runs after).
- **Position B strains:** if Step 10's `operative` array is populated under refuse with anything beyond "refuse the bundle" (e.g., partial operative commitments leaking through), the closed-set vocabulary discipline gains an enforcement point. The recommendation surfaced in `elif_v0_1_alpha_replay_report.md` §262 specifies `operative=["refuse bundle"]` only, which preserves Article I; deviation would strain it.

### Article II — Frame Humility

- **Position A preserves:** the refuse verdict at Step 9 stops downstream framing activity. The frame is refused; no further frame-shape gets committed.
- **Position B preserves:** Step 10's structured separation can record that the refused bundle was the frame; the closure makes frame-rejection more visible to subsequent cases.
- **Position A strains:** none.
- **Position B strains:** none directly; potentially imports a subtle Article II tension if Step 10 under refuse generates new framings (it should not, per the recommendation surfaced).

### Article III — No Self-Validation

- **Position A preserves:** silence after refuse prevents the runner from claiming internal-elegance closure ("look how cleanly we refused").
- **Position B preserves:** the closure record is structured, not narrative; the operative/theoretical separation traces to schema, not to internal coherence.
- **Position A strains:** none.
- **Position B strains:** if the closure surface (V1 / V2) renders the post-refusal Step 10 / Step 11 content as a "complete case" rather than as a refused case with structured closure metadata, the rendering layer (not the substrate) could re-import self-validation. The substrate itself is neutral on this.

### Article IV — Partiality of Models

- **Position A preserves:** by halting, the runner makes no attempt to separate operative from theoretical on a refused frame — which is honest if one reads Article IV as "the gap between operative and theoretical is itself partial; on refuse, even the gap is not arbitrable."
- **Position B preserves:** Article IV's "theoretical and operative are both partial views" is structurally rendered when Step 10 fires on refuse: `operative=["refuse bundle"]` is the partial view of what may be acted on; `theoretical=[uncertainty sources]` is the partial view of what remains. The Article's enforcement gains a surface.
- **Position A strains:** Article IV's enforcement on refuse-cases is implicit (via Step 9's uncertainty sources) rather than structurally separated.
- **Position B strains:** none directly.

### Article V — Refusal-Capability

This is the governing Article for G0. From `elif_constitutional_layer.md` §37:

> **Article V — Refusal-Capable.** "Unknown," "insufficient evidence," "do not scale," "framing malformed" are valid outputs. **DUAL: refusal where evidence is sufficient is its own false closure (refusal-theater).**

- **Position A preserves:** the cleanest defense of refusal-capability — the runner halts cleanly, exit code 20, no downstream surface continues. From `elif_audit_a_world_models.md` §A3.1: "The runner's halt-on-refuse discipline (`exit_code=20`) must remain inviolate. No 'soft refuse on simulator-anchored frames' path may be introduced." Position A is the literal reading of "refusal halts reasoning."
- **Position B preserves:** the DUAL clause. Article V's second sentence names refusal-theater as a failure mode. If Step 10 / Step 11 do not fire on refuse, the refused case is recorded structurally as "halted" — but the content of what was refused, and the capacity engaged in refusing, is not. A reading of Article V that emphasizes the DUAL clause says: a refusal that does not record what it refused, and how, risks becoming refusal-theater at the procedural-record level (the record is too thin to verify the refusal was substantive).
- **Position A strains:** the DUAL clause — if Step 10/11 not firing means the refusal's substance is under-recorded, the refused-case body of evidence cannot itself be audited for refusal-theater patterns.
- **Position B strains:** the first clause — running Step 10 / Step 11 after refuse can be read as "the refusal does not halt reasoning; it just changes its shape." A reading that emphasizes the first clause says: refusal SHOULD halt; closure passes after refuse are reasoning-continuation by another name.

The two readings of Article V are not reconcilable from outside the operator's adjudication. Each is internally coherent. The decision is which reading is doctrinally honest.

### Article VI — Coherent Convergence

- **Position A preserves:** Article VI's emphasis that "Branching Roadmap Engine and Operative Truth Separator must produce arbitrated, actionable pathways within finite decomposition cycles" — when Step 9 refuses, the cycle is closed; no further arbitration occurs. The "finite decomposition cycles" interpretation closes at Step 9.
- **Position B preserves:** the Operative Truth Separator is specifically named in Article VI as a convergence-producer. If it never fires on refuse, the convergence Article VI requires is structurally elided in refuse-cases. Position B is the reading that says: convergence on a refused case takes the shape of structured closure (operative=`["refuse bundle"]`), and Article VI requires that closure surface to exist.
- **Position A strains:** Article VI's naming of the Operative Truth Separator as a load-bearing convergence-producer; on refuse, the Separator is silent.
- **Position B strains:** none directly; if Step 10 runs honestly under refuse, Article VI's convergence requirement is more legibly met.

### Article VII — Capacity vs Truth + Memory Logger Doctrine

See §5 below for the deep dive.

- **Position A preserves:** the MemoryLogger's persistence-infrastructure-level Article VII coverage (open, step_committed, refutation, close events written per alpha case). The capacity-vs-truth distinction is preserved by the append-only JSONL discipline and the closed-set event_types/change_types.
- **Position B preserves:** Article VII's CONTENT-level operationalization (the `judgment_act` / `pattern_engaged` / `capacity_change` entries that the alpha cannot currently emit on refuse-cases). Per `elif_v0_1_what_remains.md` §5.1: "Article VII (Capacity vs Truth): TESTED at the persistence infrastructure level... NOT TESTED at the content level (Step 11 capacity_change entries don't emit on refuse-path)."
- **Position A strains:** Article VII's content-level enforcement on refuse-cases. The substrate exists; the content does not.
- **Position B strains:** the Article's anti-truth-accumulation guard. If Step 11 content-pass fires on refuse-cases AND the cross-case dashboard renders capacity counts without explicit "INVITATION TO TEST" framing, the very content that enables Article VII observability could re-import sovereignty (per `elif_constitutional_layer.md` Risk #23: "Capacity framed as truth approach → sovereignty re-import").

---

## 4. Article-by-Article Impact Matrix

Single-cell-per-pair statements. Closed-form; no ranking.

| Article | Position A interaction | Position B interaction |
|---|---|---|
| I — Non-Absolutization | Halt-on-refuse is the most austere expression; no downstream output claims closure. | `theoretical` array structurally enumerates partiality; closed-set `operative=["refuse bundle"]` preserves discipline. |
| II — Frame Humility | Refusal stops further frame-shape commitment. | Refused frame is structurally recorded as refused; cross-case visibility of frame-rejection improves. |
| III — No Self-Validation | Silence after refuse prevents internal-elegance closure. | Closure is schema-anchored, not narrative; risk only at rendering layer, not substrate. |
| IV — Partiality of Models | Operative/theoretical separation is moot on refused frame; honest reading of "the gap is itself partial." | Operative/theoretical separation is rendered; the Article gains a surface for refuse-cases. |
| V — Refusal-Capable | Literal first-clause reading: refusal halts reasoning. | DUAL-clause reading: refusal records what it refused; avoids refusal-theater at procedural-record level. |
| VI — Coherent Convergence | Convergence terminates at Step 9 verdict; finite decomposition closes. | Operative Truth Separator (Article-VI-named) gets to fire on refuse-cases; convergence is structurally complete. |
| VII — Capacity vs Truth | Persistence-infrastructure level is honored; content-pass is silent on refuse-cases. | Content-pass fires; capacity_change / pattern_engaged / judgment_act entries populate; risk depends on rendering discipline. |

### 4.1 Cross-Article tensions internal to each Position

The matrix above captures direct interactions. The cross-Article tensions internal to each Position are also load-bearing:

- **Position A internal tension:** Article V's first clause is honored maximally; Article VI's naming of the Operative Truth Separator as load-bearing is honored implicitly (the Separator exists, just doesn't fire on refuse); Article VII's content-pass is silent on refuse-cases. The tension is between austere Article V and surface-bearing Article VI + Article VII. Position A weights the austere reading; Article VI's Separator-naming and Article VII's content-pass are read as non-applicable to refuse-cases by structural elision.
- **Position B internal tension:** Article V's first clause is loosened (or re-interpreted via the DUAL clause); Article VI's Separator-naming and Article VII's content-pass are honored. The tension is between the literal first-clause reading of Article V and the surface-bearing readings of VI + VII. Position B weights surface-bearing; the first-clause reading is read as exhausted by the `refutation` event + Step 9 verdict, with Step 10/11 acting as closure rather than continued reasoning.

The doctrinal posture each Position takes against its internal tension is itself the operator's adjudication, not a derivable conclusion.

---

## 5. Article VII Impact (deep dive)

Article VII is the capacity-vs-truth axis plus the Memory Logger doctrine. From `elif_constitutional_layer.md` §43:

> **Article VII — Generative Reconstruction.** Arbitrated convergence must produce structures that EXTEND the system's accumulated capacity, not merely close the current question. ... **Capacity accumulation is observable; truth accumulation is forbidden.**

The asymmetric Position A / Position B implications:

### 5.1 capacity_change recorded for refused cases?

- **Position A:** No. The closed-set `_VALID_CHANGE_TYPES` (`{arbitration_shortcut_added, framework_candidate_emerged, composition_path_discovered, pattern_recognition_added, judgment_act_logged}`) are all only emitable through Step 11 content-pass. Step 11 not firing means none of the five change types is recorded against refuse-cases. The alpha read_case_state aggregation (per memory_logger.py line ~358) returns `capacity_change_records = 0` for all three alpha cases.
- **Position B:** Yes. The closed-set change types can be emitted under refuse-cases (most likely `judgment_act_logged` for the act of refusing, possibly `pattern_recognition_added` if the refused-frame shape has been seen before).

### 5.2 pattern_engaged tracked for refused cases?

- **Position A:** No. The `pattern_engaged` content is part of the Step 11 content-pass; the `pattern_recognized` event_type is in `_VALID_EVENT_TYPES` but is not currently emitted by the runner on refuse-cases. The infrastructure exists; the content does not.
- **Position B:** Yes. The pattern engaged in refusing (e.g., "bundle-of-irreversibility-axes refused" for case_01; "irreversibility + governance-demand pattern refused" for case_02) is logged as pattern engagement.

### 5.3 Theoretical-source array (Step 10) for refused-case simulator claims

This anchor is specifically named in `elif_audit_a_world_models.md` §A3.4:

> Step 10 must explicitly populate `theoretical` with all simulator-derived claims, regardless of how confident the simulator was. This requires an explicit prompt clause AND a schema-level enforcement... The operator-pending question on whether Step 10/11 runs on refuse-path becomes MORE LOAD-BEARING under world-model integration. If Step 10 does not run on refuse, simulator-anchored refusals never get their theoretical claims recorded — a Memory Logger gap.

- **Position A:** Once a world-model schema-seam ships (Phase 7+), simulator-anchored claims that contribute to a refuse-verdict are NOT recorded in any `theoretical` array. The simulator's contribution to the refusal is implicit in Step 9's `unresolved_uncertainty_sources` but not separated as theoretical.
- **Position B:** Simulator-anchored claims that contribute to a refuse-verdict ARE recorded in `theoretical`. The schema-seam at Phase 7 has a structured target to populate; Audit A's prerequisite 9 ("simulator-bias detection" — see `elif_audit_a_world_models.md` §A4.2) has a recording surface.

### 5.4 Sterile-equilibrium detector input completeness

The sterile-equilibrium detector is deferred to v0.2 (per `elif_v0_1_what_remains.md` §5.3) and queued as Phase 5 deliverable in the synthesis (per `elif_audit_synthesis.md` §4.5). The detector inputs include:

- `capacity_change_records` count per case (currently zero across alpha refuse-cases per memory_logger.py read_case_state)
- `pattern_recognized` event count per case (currently zero on refuse-path)
- `judgment_acts_recorded` count per case (currently zero on refuse-path)

The detector's read on the alpha cohort, under each position:

- **Position A:** all three refuse-cases register as zero on all three signals. The detector cannot distinguish a refused case (where refusal is the substantive output) from a sterile-equilibrium case (where the procedure produced no engagement). Input is structurally incomplete for the refuse-path.
- **Position B:** refuse-cases register signal on all three; the detector can distinguish substantive refusal from sterility.

### 5.5 Read against `read_case_state` aggregation

The MemoryLogger's `read_case_state` method (per memory_logger.py ~line 348) aggregates per-case signals including `capacity_change_records`, `pattern_recognized` count, `judgment_acts_recorded` count, and uncertainty-source counts. The aggregation is the substrate for V2 dashboard inputs (per Audit C §C6.2) and for the sterile-equilibrium detector inputs (per `elif_v0_1_what_remains.md` §5.3).

- **Position A:** `read_case_state` on a refuse-case returns the open/step_committed/refutation/close skeleton with `capacity_change_records=0`, `judgment_acts_recorded=0`, `pattern_recognized_count=0`. The aggregation is structurally truthful — it accurately reports that no content-pass entries exist — but the aggregation cannot be used to distinguish "refused substantively" from "produced no engagement at all."
- **Position B:** `read_case_state` returns non-zero counts on the content-pass signals. The aggregation can distinguish substantive refusal from sterility. The cross-case dashboard reads from this aggregation and renders frequencies, NOT predictions (per `elif_audit_c_media_communication.md` §OD-C-3).

### 5.6 v0.4 Risk activation/defusion

From `elif_constitutional_layer.md` §132–140:

- **Risk #23 — Capacity framed as truth approach → sovereignty re-import (CRITICAL).** Position A: not activated (no capacity content to misread as truth on refuse-cases). Position B: activated as a downstream rendering concern (the dashboard at V2 must surface capacity-counts with INVITATION-TO-TEST framing per `elif_audit_c_media_communication.md` §OD-C-3); the substrate itself is neutral.
- **Risk #24 — Memory Logger becomes prestige store (HIGH).** Position A: not activated. Position B: activated only if the operator-facing surface treats `pattern_engaged` entries as "blessed patterns"; mitigated by the closed-set discipline that requires every entry to be refutable.
- **Risk #26 — Generative pressure becomes "appear capable" optimization (HIGH).** Position A: defused (no generative pressure on refuse-path). Position B: present but bounded — Step 10 on refuse populates `operative=["refuse bundle"]` only (per the recommendation surfaced in `elif_v0_1_alpha_replay_report.md` §262); no "appear capable" surface results.
- **Risk #29 — Pattern recognition treated as predictive certainty (HIGH).** Position A: defused (no pattern recognition emitted). Position B: present; mitigated by the doctrinal rule that pattern recognition is INVITATION TO TEST, not validation; enforcement is at the rendering layer (V2 dashboard scope per §OD-C-3).
- **Risk #30 — Article VII defends long-running ELIF instance against compression (CRITICAL).** Position A: defused (no accumulated patterns to defend). Position B: present in principle; mitigated by the v0.4 locked rule that no pattern is sacrosanct.

The asymmetric reading: Position A defuses Risk #23 / #24 / #26 / #29 / #30 by emptying the content surface; Position B activates them as bounded surfaces requiring rendering discipline at V2. Position A's defusion is also Position A's silence on Article VII content-level enforcement; Position B's activation is also Position B's enabling of Article VII content-level operationalization. The same trade.

### 5.7 Four-pole failure-mode taxonomy (v0.4) on the refuse-path

Per `elif_constitutional_layer.md` the four poles are Absolutization, False Closure, Fragmentation, Sterile Equilibrium. Each pole's defense intersects G0:

- **Absolutization.** Position A: defended structurally by halt-at-Step-9 (the runner makes no further claims); the strictest defense in the system per Audit A §A3.5. Position B: defended by closed-set `operative=["refuse bundle"]` discipline at Step 10 (no operative beyond refusal is permitted) and by the `theoretical` array's explicit partiality enumeration. The Audit A note (§A3.5 Absolutization defense): "refusal capability stays inviolate at Step 9" reads under Position A as no further surface; under Position B as Step 10/11 being closure-not-reasoning.
- **False Closure.** Position A: false-closure-via-Step-10-or-Step-11 is impossible because they don't fire. Position B: false-closure-via-simulator (per Audit A §A3.5) is structurally defended because Step 10 must populate `theoretical` with all simulator-derived claims; the Audit A note ("Step 10 must run even on refuse so simulator-anchored claims are recorded as theoretical") reads under Position A as a gap; under Position B as defended. The asymmetry: Position A defends against false-closure-via-Step-10 by elision; Position B defends against false-closure-via-simulator by structured recording.
- **Fragmentation.** Position A: convergence terminates at Step 9; Audit B's Step 8 stage-gated roadmap is the final convergence surface. Position B: convergence terminates at Step 10's operative/theoretical separation; Audit B §B4.3's "What's Actionable Now" surface is the final convergence surface. Both positions structurally defend against fragmentation (Step 8's stage-gated roadmap requires `>=1 continuation_gate per stage`); the difference is where the final convergence surface lands.
- **Sterile Equilibrium.** Position A: detector input is structurally incomplete on refuse-cases (per §5.4); detection of sterile equilibrium in refuse-cases must rely on Step 9 uncertainty-source patterns, not on content-pass entries. Position B: detector input is complete; sterile-equilibrium detection has the full Article VII content-pass signal set to read.

The four-pole defenses are not all aligned with one Position. Absolutization defense is cleanest under Position A. False-closure-via-simulator defense is cleanest under Position B. Fragmentation defense is structurally equivalent. Sterile-equilibrium detection is more complete under Position B. The operator's adjudication must weigh which pole's defense is most load-bearing for their reading of the doctrine.

---

## 6. V1 / V2 / V3 Consequences

Per Audits B + C, the user-visible surface depends on G0.

### 6.1 V1 (case-viewer / decision-room V1)

**Closure-stage existence:**
- **Position A:** No explicit closure stage for refuse-cases. The user-facing journey terminates at Step 9 verdict display; the `refutation` event in the JSONL trail records the halt. Per `elif_audit_b_user_experience.md` §B3.2(c), the journey naturally ends at "Refuse the bundle" with uncertainty sources shown as next-steps; no operative/theoretical surface.
- **Position B:** Explicit closure stage exists. The user sees the operative list (`["refuse bundle"]`) and the theoretical list (uncertainty sources from Step 9, restructured into Article-IV-compliant separation) and the MemoryLogger content-record summary. Per `elif_audit_b_user_experience.md` §B3.7 V1 surface list: "Operative / Theoretical panel for Step 10... MemoryLogger content panel for Step 11... Refuse-closure surface."

**V1 refuse-explainer copy:**
- **Position A:** The exit_code-20 explanation is approximately "Refuse the bundle pending decomposition; uncertainty sources X/Y/Z must be resolved." (Per Audit B §B3.6 — refuse-as-valid-output framing.) No operative/theoretical separation in copy.
- **Position B:** The same refuse-explainer copy, extended with "Operative: refuse bundle. Theoretical: [uncertainty sources, separated]. This case has been recorded; pattern X was engaged; capacity change Y was logged." (Per Audit B §B3.2(d).)

### 6.2 V2 (cross-case dashboard / laboratory mode)

**Step 10/11 panel feasibility:**
- **Position A:** Step 10/11 panels are not feasible across all-refuse cohort. If V2 launches with only refuse-cases in the corpus, the panel is empty. Either Position A must be modified at Phase 4 (per `elif_audit_synthesis.md` §4.5 prereq G2) or V2 must wait until non-refuse live cases exist.
- **Position B:** Step 10/11 panels feasible from the v0.1-cohort onward. Three alpha cases plus future cases all populate.

**V2 cross-case dashboard inputs:**
- **Position A:** Dashboard inputs limited to refutation events, Step 9 verdict + uncertainty sources, and step_committed event_counts. No `capacity_change` aggregation, no `pattern_engaged` aggregation, no `judgment_act` aggregation across cases. Per `elif_audit_c_media_communication.md` §C6.2: "V2 cross-case dashboard requires Step 11 content-pass operational."
- **Position B:** Dashboard inputs complete: `capacity_change_records` aggregation, `pattern_recognized` event counts, `judgment_act_logged` counts, uncertainty-source recurrence frequencies. Per Audit C §OD-C-3: surface presents counts, not predictions.

### 6.3 V3 (laboratory mode pattern panel completeness)

**V3 reframed per synthesis §2.4** — V3 = multi-operator (per Audit C); V3 features described in Audit B are V2-mature.

- **Position A:** V3 pattern panel for multi-operator inhabitation has no per-case capacity-change records to aggregate across operators. If V3 ever opens (synthesis treats as SPECULATION), the cross-operator observability surface is empty for refuse-cases.
- **Position B:** V3 pattern panel has structured per-case content to aggregate across operators; cross-operator observability is structurally feasible.

V3 may never open under either position (per `elif_audit_synthesis.md` §4.9; per Audit C §C6.3). The G0 decision does not force V3; it shapes what V3 could surface if it ever does.

### 6.4 Per-surface enumeration of V1 elements under each Position

Per `elif_audit_b_user_experience.md` §B4.1 the V1 surface scope is: case viewer + decision map + scenario tree + governance panel + refuse-explainer + MemoryLogger timeline + operator dashboard. Under each Position:

| V1 element | Position A behavior on refuse-cases | Position B behavior on refuse-cases |
|---|---|---|
| Case viewer | Renders steps 1–9 envelopes; envelope-count badge = 9 | Renders steps 1–11 envelopes; envelope-count badge = 11 |
| Decision map | Renders Step 2 axes + Step 6 cross-scale relations | Identical (decision map is Step 2/6 surface; G0 doesn't touch this) |
| Scenario tree | Renders Step 7 mode-A trajectories + Step 8 stage-gated roadmap | Identical |
| Governance panel | Renders Step 9 verdict + confidence + uncertainty sources | Same Step 9 render; PLUS a Step 10 operative/theoretical panel rendered as adjacent surface |
| Refuse-explainer | "Refuse the bundle pending decomposition; uncertainty sources X/Y/Z must be resolved" — terminal stage | Same refuse-explainer text PLUS a "What's Actionable Now" panel rendering `operative=["refuse bundle"]` and `theoretical=[uncertainty sources]` |
| MemoryLogger timeline | Renders 14 events (open / 9× step_committed / step_7_modeB / refutation / close / bookkeeping) | Renders 17–20+ events including Step 10 + Step 11 step_committed and any content-pass events |
| Operator dashboard tile (per-case) | Shows exit_code=20, similarity 0.83, no capacity_change count, no pattern_engaged count | Shows exit_code=20 (or new closure code), similarity ~1.0, capacity_change count > 0, pattern_engaged count > 0 |

The decision map and scenario tree are unaffected by G0; they render Step 2/6 and Step 7/8 outputs respectively, which both Positions produce identically. The governance panel, refuse-explainer, MemoryLogger timeline, and operator dashboard tile differ — and these are the surfaces where the operator experiences G0's behavioral consequence.

---

## 7. MemoryLogger Consequences

Concrete, per case:

### 7.1 Event types written

**Position A (current alpha behavior):**
- `open` (1 per case)
- `step_committed × 9` (steps 1–9)
- `step_committed` (step_7_modeB forensic entry)
- `refutation` (1 — `trigger="governance_refuse"`)
- `close` (1 — exit_code=20)
- bookkeeping (1)
- **Total: 14 events per refuse-case** (per `elif_v0_1_alpha_replay_report.md` §case_01.6)

**Position B:**
- All Position A events, PLUS:
- `step_committed` for step_10
- `step_committed` for step_11 (the synthesized run_summary envelope)
- Optionally: `pattern_recognized` (1 per pattern engaged in refusing)
- Optionally: `capacity_change` (1 per capacity-change of kind `judgment_act_logged` or similar)
- Optionally: `reuse_detected` (1 per cross-case reuse — only relevant once cross-case state replay is operational)
- **Total: 17–20+ events per refuse-case** (lower bound 17 = +step_10 + step_11 + 1 capacity_change; upper bound 20+ = +multiple content-pass entries)

### 7.2 Content fields populated

**Position A:**
- Step 9 step_committed payload includes Step 9 output (verdict, confidence, uncertainty sources)
- `refutation` payload includes `trigger` + `halt_reason`
- `close` payload includes `exit_code` + `completed_at_iso`
- No `change_type` entries
- No `judgment_act` summaries
- No `pattern_engaged` content

**Position B:**
- All Position A fields, PLUS:
- Step 10 step_committed payload includes the operative/theoretical structure
- Step 11 step_committed payload includes the `run_summary` (already in alpha for non-refuse path)
- `change_type` entries from the closed-set (most likely `judgment_act_logged` for refuse-cases)
- `judgment_act` content summarizing the act of refusal
- `pattern_engaged` content where pattern recognition fired

### 7.3 JSONL trail length per case

- **Position A:** 14 lines (one event per line; append-only).
- **Position B:** 17–20+ lines (the exact count depends on Step 11 content-pass policy, which is operator-decision sub-question for Phase 5 if Position B is adopted).

### 7.4 Append-only invariant

- **Position A:** preserved (the trail is append-only as shipped).
- **Position B:** preserved (the additional events under Position B are also appended; no event is mutated).

### 7.5 Supersede-only correction discipline

The `correction` event_type is emitted only via the `emit_correction` path, never via `write_event` directly. This discipline is invariant under both positions; neither modifies it.

---

## 8. World-Model Consequences (Phase 7+ implications)

Per `elif_audit_a_world_models.md` §A3.4 and §A4.2 prereq 9, the world-model schema-seam (Phase 7 in the synthesis numbering) is contingent on simulator-bias detection being operational at Phase 5. The schema-seam itself is Phase 7 specification, Phase 8 wiring.

### 8.1 Refused-case simulator claims at the schema-seam boundary

When (if) a simulator is wired at Phase 8 and contributes input to a Step 4 evidence anchor or a Step 7 trajectory:

- **Position A:** A refuse-verdict at Step 9 halts. If the simulator's output contributed to the refusal (e.g., the simulator's projection was a load-bearing uncertainty source named in Step 9), that contribution is recorded ONLY as one of the `unresolved_uncertainty_sources` in Step 9's payload. It is NOT recorded as a `theoretical` entry in Step 10 (Step 10 does not fire). The simulator's contribution to the refusal is implicit and non-typed.
- **Position B:** The simulator's contribution to the refusal is recorded as a `theoretical` entry in Step 10. If Step 10's schema is extended at Phase 7 to include a `theoretical_sources` array (per Audit A §A3.4 recommendation), the simulator is cited explicitly per theoretical claim.

### 8.2 Memory Logger gap on simulator-bias detection

Per `elif_audit_a_world_models.md` §A3.4:

> If Step 10 does not run on refuse, simulator-anchored refusals never get their theoretical claims recorded — a Memory Logger gap.

- **Position A:** the gap is real and remains in force at Phase 8 (if Phase 8 opens). Simulator-bias detection at the sterile-equilibrium detector (Phase 5) cannot distinguish simulator-anchored refusals from non-simulator-anchored refusals, because the simulator contribution to a refusal is not structurally separated.
- **Position B:** the gap is closed. Simulator-bias detection has a structured surface to read.

### 8.3 Sterile-equilibrium detection of simulator-bias-induced convergence at Phase 5

Per `elif_audit_a_world_models.md` §A3.5 "Sterile equilibrium" pole defense:

> A simulator's high-confidence output closes a case before the procedure has surfaced enough uncertainty. ... Step 10 must run even on refuse so simulator-anchored claims are recorded as theoretical.

- **Position A:** simulator-anchored convergence in a refused case cannot be detected by the sterile-equilibrium detector, because the simulator-contribution-to-refusal signal is not in the detector's input set.
- **Position B:** the detector can read `theoretical_sources` (if the schema-seam Phase 7 spec extends Step 10 this way) and detect simulator-bias-induced convergence at Phase 5.

Phase 7 (specification) and Phase 8 (wiring) may never open. Position A keeps the door to Phase 7 specification open (the seam can be specified regardless of refuse-halt resolution). Position A constrains what Phase 7's seam spec can accomplish for refuse-cases. Position B does not constrain Phase 7's seam spec further.

---

## 9. Reversibility Analysis

### 9.1 Is G0 reversible?

**Yes, in both directions, at bounded cost.** G0 is a runner-code-only decision; schemas, components, fixtures, and tests are unchanged by either choice.

### 9.2 Cost of flipping A → B (operator initially chooses A, later chooses B)

- Modify the refuse-halt branch in `orchestration_runner.py` (estimated 30–80 LoC).
- Confirm Step 10's `separate_operative_from_theoretical` method handles refuse-case prior_outputs cleanly (the alpha fixtures `step_10__case_*.json` already validate; live behavior under refuse needs verification).
- Update `_emit_close` to fire after Step 11 rather than after Step 9 on refuse (small change).
- Update the exit-code semantics if a new code is desired (operator sub-decision).
- Re-run E.2 live replay on the 3 alpha cases to verify Position B behavior.
- Updates to V1 surface if V1 has shipped (V1 closure-stage UX gains a render path).
- Updates to V2 if V2 has shipped (V2 dashboard inputs become richer; metrics need re-baselining).
- MemoryLogger JSONL trails for prior refuse-cases remain valid but are "incomplete" relative to the new policy. Migration: either re-run those cases under Position B (recommended; cost ~$0.63 for 3-case alpha cohort) or accept the partial trail (defensible; append-only invariant preserved).

**Total cost order-of-magnitude:** small (low hundreds of LoC + one E.2 re-run); V1/V2 rendering updates are the dominant cost if those surfaces have shipped.

### 9.3 Cost of flipping B → A (operator initially chooses B, later chooses A)

- Restore the halt-at-Step-9 branch (same LoC delta).
- Existing MemoryLogger trails written under Position B remain valid (append-only); they contain `step_committed` for steps 10 and 11 and potentially `capacity_change` / `pattern_recognized` entries that future runs will not produce.
- V1 closure-stage UX removed (small change).
- V2 dashboard inputs lose `capacity_change` / `pattern_engaged` / `judgment_act` aggregation for new refuse-cases. Existing aggregated data for old cases remains in the JSONL trail but the trend-line breaks.
- Phase 7 schema-seam spec, if drafted, must be revisited to reconfirm that `theoretical_sources` enforcement on refuse-cases is moot (since Step 10 no longer fires on refuse).

**Total cost order-of-magnitude:** comparable to A→B, with a downstream-debt asymmetry: data accumulated under B is preserved but becomes stranded; new refuse-cases run under A do not produce equivalent data.

### 9.4 Per-phase reversibility cost matrix

The flip cost depends on which phase has been reached at flip-time. Reference: `elif_audit_synthesis.md` §4 phase enumeration.

| Phase reached at flip-time | A→B cost | B→A cost |
|---|---|---|
| Phase 0 (G0 just written) | trivial; runner LoC change only | trivial; runner LoC change only |
| Phase 1 (E.2 completed) | small; re-run E.2 to regenerate refuse-case content-pass (~$0.63 alpha cohort) | small; existing trails preserved (append-only); future runs revert |
| Phase 2 (V1 shipped) | moderate; V1 rendering layer gains closure-stage; refuse-explainer copy extends; MemoryLogger timeline render extends | moderate; V1 closure-stage rendering removed; data continuity preserved for prior cases |
| Phase 3 (cases 2+3 + out-of-cluster live) | as Phase 2 + re-run later refuse-cases under new policy; cost scales with cohort | as Phase 2; aggregated cross-case dashboard inputs become heterogeneous (pre-flip vs post-flip) |
| Phase 4 (constitutional compression evaluated) | as Phase 3 + any v0.5 reframe of refuse-halt semantics must be revisited | as Phase 3; possible v0.5 reframe must be revisited |
| Phase 5 (MemoryLogger v0.2; cross-case influence) | as Phase 4 + sterile-equilibrium detector rebaselined against new content surface | as Phase 4; detector loses content-pass input; rebaselined against persistence-only |
| Phase 6 (V2 dashboard) | as Phase 5 + V2 dashboard tiles for capacity_change / pattern_engaged become live | as Phase 5 + V2 dashboard tiles for refuse-cases lose content; visual discontinuity at flip-date |
| Phase 7 (world-model schema seam specified) | as Phase 6 + spec must include `theoretical_sources` array for simulator-anchored refusals | as Phase 6 + spec must NOT include `theoretical_sources` enforcement on refuse-cases (the seam silences for refused frames) |
| Phase 8 (world-model wiring; may never open) | as Phase 7 + boundary adapter populates `theoretical_sources` on refuse | as Phase 7 + boundary adapter contribution to refuse-verdicts remains implicit |
| Phase 9 (multi-operator; SPECULATION) | as Phase 8 + multi-operator dashboard inherits the cross-case content surface | as Phase 8 + multi-operator dashboard has no refuse-case content surface |

The cost grows roughly linearly with phase depth, dominated at each phase by the rendering / aggregation work specific to that phase. Neither flip is structurally blocked at any phase.

### 9.5 Reversibility verdict

G0 is reversible in both directions at bounded cost. The cost is dominated by:
- LoC change in runner (small in both directions)
- Re-running E.2 (small; ~$0.63 for alpha cohort)
- V1/V2 surface rendering changes if shipped (the dominant cost, depending on phase reached at flip-time)
- Data continuity considerations (asymmetric: A→B preserves continuity by extending the trail; B→A creates a stranded-data discontinuity)

Neither flip is structurally blocked. Neither flip imports doctrinal violation. The Position adopted should be the one the operator's reading of Article V supports; reversibility means G0 is not an irreversible commitment.

### 9.6 What reversibility does NOT mean

Reversibility is a property of the code-and-data substrate, not of the doctrinal commitment. If the operator chooses Position A and later flips to Position B, the doctrinal record (the written G0 adjudication) is amended, not erased; the audit trail of the adjudication itself is append-only at the doctrinal level. Conversely: reversibility at the substrate level does NOT relieve the operator of choosing on doctrinal grounds. The point of the adjudication is the reading of Article V; reversibility lowers the cost of being wrong, not the importance of choosing well.

---

## 10. Open Doctrinal Questions

These are questions the operator should answer in adjudicating G0. They are NOT recommendations.

1. Does Article V's first clause ("refusal is a valid output; refusal halts reasoning") take precedence over its DUAL clause ("refusal where evidence is sufficient is its own false closure"), or is the DUAL clause the operative reading for the refuse-path?

2. Is the `refutation` event_type already in MemoryLogger sufficient as a record of refusal — or does Article VII require structured content-pass entries (judgment_act / pattern_engaged / capacity_change) for refused cases to count as observable capacity?

3. Does Article VI's naming of the Operative Truth Separator as a load-bearing convergence-producer require Step 10 to fire on refuse-cases for convergence to be structurally complete, or is finite-decomposition-terminates-at-Step-9 a sufficient reading?

4. If V2 is built and the cross-case dashboard renders capacity counts: does the INVITATION-TO-TEST framing (per Audit C §OD-C-3) hold tightly enough to prevent Risk #23 (capacity-as-truth) re-import — or is the safer choice to keep the dashboard inputs thin (Position A) to remove the temptation entirely?

5. Is the simulator-bias detection requirement at Phase 5 (per Audit A §A4.2 prereq 9) sufficient justification to structurally separate simulator-anchored claims at Step 10 on refuse-cases — or should the Phase 5 detector instead read from Step 9's `unresolved_uncertainty_sources` (which Position A populates) and apply heuristic separation downstream?

6. If the operator's reading of Article V supports Position A AND the operator wants V2 substrate eventually, is there a doctrinally-coherent intermediate (e.g., a v0.5 reframe of refuse-halt semantics that permits Step 10/11 to fire only as "post-refusal forensic capture" without permitting them to populate the operator-facing closure surface)? Note: this question explicitly sits inside the no-v0.5 absolute constraint of the current sprint; if pursued, it is Phase 4 substrate, not G0 substrate.

7. Is reversibility itself a doctrinal factor in adjudicating G0 — i.e., does the fact that the choice can be flipped at bounded cost weight the decision toward the more conservative position (A) or the more substrate-completing position (B)?

---

## 11. Operator Decisions Queued

**The one queued decision: G0 itself.**

The operator should write 1–2 paragraphs citing their reading of Article V. The doctrinal anchor for the decision is Article V (refusal-capability) as expressed in `elif_constitutional_layer.md` §37:

> "Unknown," "insufficient evidence," "do not scale," "framing malformed" are valid outputs. DUAL: refusal where evidence is sufficient is its own false closure (refusal-theater).

The operator's adjudication should specify:

1. Which reading of Article V governs G0 (first-clause-emphasis = halt-and-stop reading, supporting Position A; DUAL-clause-emphasis = refusal-must-record-its-content reading, supporting Position B).
2. Whether the operative_truth_separator's naming in Article VI changes the reading.
3. Whether Article VII's content-level operationalization on refuse-cases is doctrinally required, doctrinally optional, or doctrinally forbidden under the chosen reading.
4. Whether the world-model Phase-7 schema-seam consequences (the Memory Logger gap per Audit A §A3.4) are a factor in the adjudication or whether G0 should be adjudicated on Article V alone.

Format: a brief written record, appendable to `elif_v0_1_what_remains.md` §3 (extending the recommendation-surfaced text with the operator's adjudication) or as a new `notes/elif_g0_decision.md` document.

Once G0 is written down:
- Phase 1 (E.2 live-replay execution) opens per `elif_audit_synthesis.md` §4.1.
- All other queued operator decisions (G1-A through G3-D per synthesis §3) remain queued behind their own evidence gates; G0 does not chain them open.

---

## 12. What This Specification Does NOT Include

1. **A recommendation.** This document does not advocate Position A or Position B. Neither position is ranked, scored, or "leaned toward." The operator decides.

2. **Advocacy for either Position.** No paragraph in this document is structured as "Position X is better because Y." Wherever the substrate could be read as leaning, the asymmetric implication has been explicitly named as a trade, not a verdict.

3. **A timeline pressure ("decide by date X").** G0 is not calendar-keyed. The momentum-capture warning (memory note `momentum_capture_warning`) is the doctrinal anchor: forward motion that cannot be paused is the failure mode. G0 closes when the operator writes it down. Until then, every downstream phase remains gated.

4. **Any architectural alternative to the binary choice.** Position A and Position B exhaust the doctrinally-defensible options under v0.4. Hybrid framings (e.g., "Step 10 fires but is not surfaced to operator" — Question 6 in §10) are sub-questions of Position B with downstream-render policy attached, not alternatives to the binary. The schemas, components, and runner contract do not support a third position without architectural change (which is forbidden under this sprint's absolute constraints).

5. **A proposal for v0.5 reframe of refuse-halt semantics.** Sprint constraint: no v0.5. The Phase 4 constitutional-compression evaluation (per synthesis §4.4) is the surface where a v0.5 reframe of refuse-halt semantics would belong; it is not this sprint's surface.

6. **A new component, Article, or procedure step.** Sprint constraint and tri-audit convergence (`elif_audit_synthesis.md` §1.2): no addition.

7. **A world-model implementation specification.** Phase 7 specification is downstream of Phase 6 + Phase 7 gates per synthesis §4.7; G0 only shapes what Phase 7's seam can target for refuse-cases. The specification itself is out of scope here.

8. **A roadmap expansion.** The synthesis roadmap (Phases 0–9) is the authoritative roadmap. G0 is Phase 0. This document does not propose phases beyond Phase 9 or alternative phase orderings.

9. **A pattern adoption beyond evidence.** The capacity-vs-truth distinction is doctrinally enforced; this document does not promote any pattern from PF → CE on its own authority.

10. **An architecture inflation.** The 7-component / 11-step / 7-Article / 4-pole architecture is invariant under both Position A and Position B. G0 is a runner-code decision, not an architectural one.

---

**End of G0 decision package.**
