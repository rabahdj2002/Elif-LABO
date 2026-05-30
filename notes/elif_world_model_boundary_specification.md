# ELIF World-Model Boundary Specification

> **Captured:** 2026-05-30
> **Mode:** Specification — markdown only. No JSON files, no Python modules, no registry entries, no implementation.
> **Authority:** Honors Audit A §A2.3 Recommendation #6 ("SPECIFY do not wire at Phase 5-late"). Honors synthesis §4.7 Phase 7 charter. Honors operator authorization to specify the seam now while keeping Phase 7 itself gated on G1-G6 closing.
> **Status:** Non-expansionary. Adds no component, no Article, no procedure step, no closed-set entry, no schema beyond the single boundary contract. Specification ≠ implementation; specification ≠ activation.
> **Inputs read:** `elif_audit_a_world_models.md`, `elif_audit_synthesis.md`, `elif_v0_1_what_remains.md`, `elif_v0_1_alpha_replay_report.md`, `elif_v0_1_alpha_cost_complexity_report.md`, `src/elif_v0_1/components/*.py`, `src/elif_v0_1/orchestration_runner.py`, `src/elif_v0_1/components/memory_logger.py`.

---

## Three epistemic registers (read this first)

Every claim in this document is tagged:

- **CURRENT EVIDENCE (CE):** Demonstrable from the v0.1-alpha artifact (7 components, 11 steps, 2,533 component LoC, 33 fixtures, 0.83 structural similarity, 12/12 replay-test pass) or the v0.4 Constitutional Layer doctrine, or from the three audits A/B/C and the synthesis.
- **PLAUSIBLE FUTURE (PF):** A reasonable projection IF current evidence holds under live-replay (E.2), if G0 closes, and if Phases 1-6 of the synthesis roadmap close in sequence.
- **SPECULATION (SP):** Beyond reasonable projection. Listed for completeness. Never load-bearing.

This entire document is a **PF-scoped specification of a seam that may never be wired** (CE: Audit A §A4.4.3; synthesis §4.8). Activation is operator's call, not the spec's call.

---

## Table of contents

1. Position Statement
2. Schema Boundary
3. Adapter Boundary
4. Governance Boundary
5. Simulator-Bias Protections
6. Sterile-Equilibrium Protections
7. Closed-Set Verdict Vocabulary Frozen Under World-Model Pressure
8. Entry Points at the Seam (Step 4 vs Step 7)
9. Refused-Case Recording Path (G0-Dependent)
10. Four Permanent Prohibitions
11. Evidence Gates Before Wiring (G7 + G8 + G9)
12. "Phase 6 May Never Open" — defensible non-expansionary outcome
13. Operator Decisions Queued
14. What this specification does NOT include

---

## §1 Position Statement

**Option I — World models live outside ELIF.** ELIF arbitrates simulator output as ONE evidence type among many. ELIF never hosts a simulator, never invokes one from inside its 7-component surface, never owns simulator state, never arbitrates from inside the simulator's surface, never tunes a simulator, never reaches across the seam to retrieve simulator parameters.

This is the position reached by elimination in Audit A §A1.6 and reaffirmed across A + B + C convergence in synthesis §1.1. The synthesis ranks the operator's working hypothesis ("LLMs generate. World models simulate. Agents execute. ELIF validates, arbitrates, governs, structures discovery, preserves corrigibility.") as **PF with strong cross-validation**. Option I is the syntactic form of that hypothesis.

### §1.1 What "outside" means precisely

(CE) Audit A §A1.6 defines "outside" as: ELIF receives world-model outputs as inputs at specific procedural seams (never at frame), validates them against a boundary schema, and then runs the existing 11-step procedure on them as it would on any other evidence type. The simulator's invocation, state-keeping, parameter tuning, and inter-call memory are all outside ELIF's surface.

The four-organ separation pattern in OSG (`CLAUDE.md` four-organ section) is the doctrinal anchor. ELIF↔world-model is to ELIF what Limova↔OSG runtime is to OSG — loosely coupled, never in the runtime authority path.

### §1.2 What ELIF does NOT do at the seam

The seam is one-way receiving with refusal capability. ELIF specifically does NOT:

- Invoke a simulator (CE: keeps four-organ separation; A §A2.3).
- Retain simulator state between calls (CE: components are stateless per `cost_complexity_report.md` §3; Memory Logger is the only stateful component, and the seam does not change that).
- Cache simulator outputs (PF: caching would create a sovereignty surface that nobody explicitly authored).
- Translate simulator vocabularies (PF: translation creates a closed-set drift vector at the adapter).
- Add fields to a simulator response (PF: enrichment at the adapter would shift simulator identity onto ELIF).
- Choose which simulator to consult (PF: simulator selection is an operator decision, not an ELIF decision).
- Decide when a simulator should be re-run (PF: re-running is operator scope; auto-re-run would be a sovereignty surface).
- Maintain a simulator registry inside ELIF code (PF: registry inside ELIF would re-import the 8th-component shape under a different name; A §A4.3 prohibition pattern).

### §1.3 What ELIF DOES at the seam

The seam is a thin receiver. ELIF:

- Accepts a `world_model_response` payload (§2).
- Validates it against schema (§3).
- Hands it to Step 4 OR Step 7 as evidence (§8).
- Runs the existing 11-step procedure on the case the payload pertains to.
- Records the simulator's claims as theoretical at Step 10 if G0 is Position B (§9).
- Refuses the payload (and the case, if necessary) at Step 9 the same way it refuses any other evidence-anchored frame (§4, Article V).

### §1.4 The seam is small

(CE) Audit A §A2.3 cost estimate: schema (~150 LoC) + boundary adapter (~200 LoC) + test fixtures (~300 LoC) = ~650 LoC. The estimate is FUTURE-IMPLEMENTATION cost, not specification cost. This document specifies the seam without producing any of that LoC.

(CE) The seam keeps ELIF at 7 components / 11 steps / pinned signatures (synthesis §3 table; A §A1.1). The schema seam introduces NO new component, NO new step, NO new Article, NO new closed-set entry, NO Memory Logger event_type, NO Memory Logger change_type.

---

## §2 Schema Boundary

The single boundary contract: `world_model_response.schema`. Exactly one schema. It exists at the ELIF input boundary, NOT inside any component. The schema is specified here in markdown; a future Phase 7 deliverable (if Phase 7 ever opens — synthesis §4.7) would translate it to JSON Schema as the wire format.

### §2.1 Schema field catalog

| Field | Type | Cardinality | Validation rule |
|---|---|---|---|
| `simulator_id` | string | required, non-empty | At v0.1 spec: free-text with disclaimer (§2.2). Future: closed-set if/when populated. Adapter MUST NOT auto-populate from request context. |
| `hypothesis_under_simulation` | string | required, non-empty | MUST reference an ELIF Step 4 `hypothesis_id` already emitted for the case to which this response pertains. Adapter MUST verify the referenced hypothesis_id exists in the case's Step 4 output before accepting the payload. |
| `distinguishing_prediction_under_simulation` | string | required, non-empty | MUST reference the `distinguishing_prediction` field of the Step 4 hypothesis identified by `hypothesis_under_simulation`. Adapter MUST verify exact-string match against the stored Step 4 output. |
| `simulator_output` | JSON value | required | Free-shape JSON. ELIF treats this as OPAQUE external evidence; ELIF does not parse, traverse, or schema-validate the inner shape. The adapter does NOT extract sub-fields. |
| `simulator_uncertainty_sources` | array of strings | required, `minItems = 1` | Each entry is a free-text named uncertainty source. The simulator (not ELIF) is the author. ELIF MUST verify the array is non-empty; ELIF MUST NOT enrich, deduplicate, or rephrase entries. |
| `simulator_assumptions` | array of strings | required, `minItems = 1` | Each entry is a free-text named assumption. The simulator (not ELIF) is the author. ELIF MUST verify the array is non-empty; ELIF MUST NOT enrich, deduplicate, or rephrase entries. |
| `simulator_run_timestamp` | string | required | ISO-8601 UTC, must match the regex pattern enforced by Memory Logger's `committed_at_iso` (memory_logger.py §`_utc_now_iso`). Adapter MUST reject malformed timestamps. |
| `simulator_bias_signals` | array of strings | required at validation time, but populated by ELIF, NOT by the simulator | An incoming payload MAY include this field as an empty array OR omit it; if present and non-empty, the adapter MUST refuse the payload (§2.4). The Step 7 cross-check populates this field after the payload enters the procedure. |

### §2.2 The `simulator_id` free-text disclaimer (v0.1 spec)

(PF) The audit notes (A §A3.2) that closed-set discipline is the doctrinally correct posture for any vocabulary that gates ELIF behavior. The `simulator_id` field is borderline: it does not directly gate verdict, but it does anchor the simulator-bias detector (§5) and the sterile-equilibrium detector (§6).

The v0.1 spec position: `simulator_id` is FREE-TEXT WITH DISCLAIMER. The disclaimer reads (verbatim):

> The `simulator_id` field is free-text at v0.1 specification only. The seam MAY transition `simulator_id` to a closed-set at Phase 7 review if and only if operator-approved enumeration of trusted simulators has been authored AND the sterile-equilibrium detector (§6) has demonstrated cross-simulator convergence detection on at least 2 contradictory test cases. Until then, free-text `simulator_id` is the default; trade-off is that the bias detector and the sterile-equilibrium detector lose closed-set strength.

(PF) The disclaimer is load-bearing: it pre-records that the audit's preferred closed-set discipline (A §A3.2) is NOT applied at v0.1 spec, and names the gate (operator approval + bias-detector demonstration) for transitioning to closed-set.

### §2.3 Validation rules — what the adapter checks at receipt

The adapter (§3) applies these checks in order. The order is load-bearing: each check refines the payload's identity before deeper checks are applied.

1. **Schema shape.** The payload is a JSON object containing exactly the seven required fields listed in §2.1 (eight if `simulator_bias_signals` is present as an empty array). No extra fields permitted. Extra fields → refuse.
2. **Field types.** Every field has the type listed in §2.1. Wrong type → refuse.
3. **Non-empty constraints.** `simulator_id`, `hypothesis_under_simulation`, `distinguishing_prediction_under_simulation`, `simulator_uncertainty_sources` (minItems=1), `simulator_assumptions` (minItems=1) are all non-empty. Any empty constraint → refuse.
4. **Timestamp format.** `simulator_run_timestamp` matches ISO-8601 UTC. Malformed → refuse.
5. **Hypothesis cross-reference.** `hypothesis_under_simulation` MUST identify an existing Step 4 hypothesis already emitted for the case. The adapter looks up the case via the operator-supplied case-binding context (the case is identified out-of-band; the payload itself does not carry case_id, because that would couple simulators to ELIF's internal case identifiers — a sovereignty drift vector). If no match → refuse.
6. **Distinguishing-prediction cross-reference.** `distinguishing_prediction_under_simulation` MUST exactly match the `distinguishing_prediction` field of the identified hypothesis. Exact-string check; no fuzzy match (fuzzy match would be a vocabulary-drift surface). If no match → refuse.
7. **Bias-signal authority check.** If the incoming payload includes `simulator_bias_signals` with `len > 0`, the adapter refuses. The simulator MUST NOT pre-populate the bias-signal field; only Step 7 cross-check populates it. Non-empty bias-signals in incoming payload → refuse.

### §2.4 Refusal semantics on schema violation

(CE) Refusal at the seam is structurally identical to refusal at the frame boundary today (frame_validator §1.1, exit_code=10). The adapter never "tries harder," never "patches the payload," never "asks the simulator to retry." Schema violation → refuse and emit a refusal record that the operator can inspect.

(PF) The refusal record is NOT a Memory Logger entry. The seam exists before Step 1; the case has not opened; Memory Logger has no event_type for boundary-rejection (and MUST NOT have one — adding one would be a closed-set drift). The refusal record is a standalone log entry visible to the operator on the operator's surface (V1 case-viewer per synthesis §4.2; until then, stderr or an operator-facing CLI message).

(PF) Refusal at the seam does NOT halt ELIF. ELIF was not running. The seam refusal merely tells the operator: the simulator output is malformed and was not admitted as evidence. The operator may re-author the simulator query, choose a different simulator, or proceed without simulator input.

---

## §3 Adapter Boundary

The boundary adapter is the single piece of code that owns the seam. It is thin, refusable, and stateless. It is NOT a component in the ELIF 7-component sense; it is a pre-frame validator at the ELIF input boundary, structurally analogous to `frame_validator.validate()` but operating one layer earlier.

### §3.1 Adapter responsibility

The adapter's complete responsibility is:

1. Receive a `world_model_response` payload.
2. Validate against the schema (§2.3).
3. On schema violation, emit a refusal record (§2.4) and return WITHOUT invoking any ELIF component.
4. On schema validity, hand the payload to one of two entry points:
   - **Step 4 evidence anchor** (§8.1), OR
   - **Step 7 cross-check input** (§8.2).
5. The entry-point choice is made by the operator OUT-OF-BAND (the payload itself does NOT carry an entry-point hint; carrying one would let the simulator choose where it inserts itself into ELIF, which is a sovereignty drift vector).
6. After handoff, the adapter forgets the payload. No caching, no state, no re-emission.

### §3.2 What the adapter does NOT do

The list is enforced by what's NOT in the responsibility above:

- The adapter does NOT invoke any simulator (CE: A §A2.3; §1.2).
- The adapter does NOT maintain any simulator state (CE: stateless by design; mirrors components' statelessness per `cost_complexity_report.md` §3).
- The adapter does NOT cache simulator outputs (PF: caching = sovereignty surface).
- The adapter does NOT translate simulator vocabularies (PF: translation = drift surface; the adapter accepts only payloads whose vocabulary the simulator already produced).
- The adapter does NOT add fields to the response (PF: enrichment = identity shift; §1.2).
- The adapter does NOT pick the entry point (operator picks out-of-band; §3.1.5).
- The adapter does NOT participate in Step 1 frame validation (the seam is one layer ABOVE frame validation; the payload is not a frame).
- The adapter does NOT consult Memory Logger (the adapter operates before the case has opened, or in the middle of an open case; it does not have a Memory Logger reference at all).
- The adapter does NOT have a closed-set vocabulary of its own (the closed-sets it cares about — verdict_vocab, change_types, event_types — are owned by the components it eventually hands off to; the adapter does not introduce a new closed-set).

### §3.3 Function signatures (spec only)

These signatures are SPECIFIED for future implementation. NONE of this code exists today; the signatures here are doctrinal commitments about shape, not implementation.

(Conceptual signatures — illustrative, not executable.)

```
def admit_world_model_response(
    payload,                       # raw JSON value, as received
    case_id,                       # operator-supplied; out-of-band binding
    entry_point,                   # operator-supplied; "step_4_evidence" or "step_7_cross_check"
    *,
    case_step_4_output,            # required if entry_point == "step_4_evidence" OR
                                   #                              "step_7_cross_check"
                                   # because both require hypothesis_under_simulation lookup
) -> AdapterResult:
    """
    Validate payload against world_model_response schema.
    If valid: hand off to the specified entry point.
    If invalid: emit refusal record and return AdapterResult.refused.
    Stateless: no side effects beyond the refusal record on invalid input
    and the handoff on valid input.
    """
```

```
AdapterResult = one of:
    AdapterResult.admitted(entry_point=..., bound_to_hypothesis_id=...)
    AdapterResult.refused(reason=..., refusal_record=...)
```

Notes on the signature:
- `case_id` is operator-supplied because the payload does not carry it (§2.3 check 5 explanation).
- `entry_point` is operator-supplied because the simulator does not pick (§3.1.5).
- `case_step_4_output` is required for cross-reference checks (§2.3 checks 5 + 6). The adapter does NOT look up Step 4 output from Memory Logger; the operator hands it in. This keeps the adapter independent of Memory Logger.
- The result is a closed-set discriminated union: `admitted` or `refused`. No `partial`, no `retry`. (PF: a `retry` variant would be a re-import of simulator state across ELIF's boundary.)

### §3.4 Refusal paths (enumerated)

The adapter refuses on:

1. Schema shape violation (extra fields, missing fields).
2. Type mismatch on any field.
3. Empty value on any non-empty-required field.
4. Empty array on `simulator_uncertainty_sources` or `simulator_assumptions`.
5. Malformed `simulator_run_timestamp`.
6. `hypothesis_under_simulation` not found in the supplied `case_step_4_output`.
7. `distinguishing_prediction_under_simulation` does not exact-string match the identified hypothesis.
8. `simulator_bias_signals` non-empty in incoming payload (only ELIF Step 7 populates it).
9. Operator-supplied `entry_point` is not in `{"step_4_evidence", "step_7_cross_check"}`.
10. Operator-supplied `case_id` does not match any open or addressable case.

Every refusal emits a refusal record containing: the refusal reason (one of the 10 above), the payload's `simulator_id`, the timestamp of refusal, the case_id (if provided), and the operator-supplied entry_point (if provided). The refusal record is the seam's audit-trail equivalent of Memory Logger's `refutation` events — but it is NOT a Memory Logger entry (§2.4).

### §3.5 Adapter is NOT a component

(CE) Audit A §A1.6 rejects all four "inside ELIF" options. The adapter MUST NOT become a component by accretion. Specifically:

- The adapter does NOT have pinned method signatures in the 7-component sense (`elif_v0_1_what_remains.md` §1 pinning principle).
- The adapter does NOT own any procedure step.
- The adapter does NOT enter Step 8's stage-gated roadmap.
- The adapter's LoC budget (estimated ~200 LoC per A §A2.3) is at the BOUNDARY, not inside `components/`.
- The adapter is structurally a frame-boundary pre-validator, not a procedure participant.

If a future session proposes "let's give the adapter a method," "let's give the adapter state," or "let's give the adapter a closed-set vocabulary" — that proposal is a re-importation of the 8th-component shape under a different name and is prohibited.

---

## §4 Governance Boundary

The seam is governed by the existing Constitutional Articles. No new Article is added (synthesis §1.2; A §A4.3 item 3). Four Articles bind at the seam in load-bearing ways:

### §4.1 Article I — Operator Sovereignty (Non-Absolutization of Intelligence)

(CE) Article I structurally enforces that no intelligence (LLM, world model, prior arbitration) is treated as sovereign.

**Binding at the seam:**

- Each simulator-output ingestion is OPERATOR-AUTHORIZED case-by-case. No auto-ingestion. The operator explicitly hands the adapter a `(payload, case_id, entry_point)` triple per ingestion event. The seam has no "subscribe to simulator X for all future cases" affordance.
- The simulator does NOT pick the case. The simulator does NOT pick the entry point. The simulator does NOT receive ELIF's state. The simulator is not informed of ELIF's prior verdicts on the case.
- The operator's authorization is NOT logged inside the simulator (the simulator does not "know" ELIF used its output); the authorization is logged on ELIF's side as part of the refusal-record-or-admittance trail.

(PF) The "no auto-ingestion" constraint is the structural form of Article I at the seam. Auto-ingestion would treat simulator output as a configured input source, which is the sovereignty-import shape Article I prohibits.

### §4.2 Article III — No Self-Validation

(CE) Article III prohibits ELIF from validating its own outputs as inputs. The MemoryLogger writes append-only with a `correction` event_type that supersedes prior entries (memory_logger.py §27); originals are NEVER mutated.

**Binding at the seam:**

- ELIF NEVER ingests its own prior arbitration as simulator input. If a future session were to propose "let's wrap ELIF's verdict as a `world_model_response` so we can re-enter it through the seam at the next case," that is sovereignty drift through the seam and is prohibited.
- A simulator MUST NOT be a wrapper around ELIF. If a simulator's identity is "another ELIF instance," its output is structurally self-validation and is refused at the adapter even if schema-valid. Detecting this is the operator's responsibility at simulator selection time; the adapter cannot detect "simulator X is secretly ELIF Y."
- A simulator's output that CITES ELIF's prior arbitration is admissible if the citation is in the opaque `simulator_output` field (which the adapter does not parse). The constraint is that ELIF must not synthesize the chain back: if Step 7 cross-check (§8.2) recognizes a circular reference (the simulator citing the case's own prior ELIF arbitration), the cross-check raises a bias signal (§5) and Step 9 may refuse.

(PF) The Article III binding at the seam is the strongest defensive layer against simulator-as-mirror failure (the simulator merely reflecting what the operator wanted to hear).

### §4.3 Article V — Refusal Capability

(CE) Article V is enforced by `verdict=refuse` at Step 9 + runner halt at exit_code=20 (`elif_v0_1_alpha_replay_report.md` §case_01-03). All three alpha cases produced refuse and the runner halted.

**Binding at the seam:**

- Simulator output is ONE evidence type among many. Step 9 may STILL verdict=refuse even with simulator output supporting a hypothesis. The simulator's confidence does not bias Step 9's verdict.
- The closed-set verdict vocabulary stays frozen (§7). No simulator-supported verdict is added.
- The refusal can fire at Step 9 (whole-case refusal) OR can take the form of bias signals at Step 7 (cross-check level) escalating to Step 9 (§5.2).

(PF) The strongest defense of Article V at the seam is that the simulator's output never reaches Step 9 directly. It enters as evidence at Step 4 or as cross-check at Step 7; both layers are upstream of Step 9 and are subject to Step 9's adjudication. The simulator never gets a "vote."

### §4.4 Article VII — Capacity vs Truth

(CE) Article VII is enforced at the persistence level by Memory Logger event-type closed-sets (`_VALID_EVENT_TYPES`, `_VALID_CHANGE_TYPES` in memory_logger.py).

**Binding at the seam:**

- Simulator output is recorded as THEORETICAL claims in Step 10 (operative_truth_separator), NEVER as operative truth, regardless of simulator confidence. This requires G0 = Position B (synthesis §1.3); §9 expands.
- Memory Logger capacity-change entries that reference simulator input MUST tag the input as simulator-anchored. (CE) The current `_VALID_CHANGE_TYPES` closed-set does NOT have a simulator-anchored variant; A §A3.3 names this as a load-bearing question. The boundary spec position: a simulator-anchored variant is NOT added to `_VALID_CHANGE_TYPES`; instead, the existing `composition_path_discovered` or `arbitration_shortcut_added` entry MAY be used but the entry's free-text content MUST cite the `simulator_id` whose output anchored the capacity change. This avoids closed-set expansion while preserving auditability.
- (PF) The simulator-anchored capacity-change tagging is enforced at the prompt/schema layer for the component that emits the capacity_change event (currently planned for Phase 5 Memory Logger v0.2 — synthesis §4.5). The seam itself does not write capacity_change events; the seam hands payloads to Step 4 or Step 7, and downstream components decide if any capacity_change records get emitted.

### §4.5 Articles II, IV, VI at the seam (briefly)

- **Article II (Frame Humility):** does NOT bind at the seam. The seam operates AFTER Step 1 frame validation (or operates on an already-decomposed sub-frame at Step 4 / Step 7). Simulator output never enters as a Step 1 frame substrate (§8.3 — prohibition).
- **Article IV (Partiality of Models):** is the NATIVE article at the seam (A §A3.4). Simulator output is by construction theoretical; the operative_truth_separator (Step 10) is the architecturally correct surface for honest accounting (§9).
- **Article VI (Coherent Convergence):** binds at the seam via Step 8 stage-gated roadmap — simulator output that contributes to a Step 7 trajectory must still be subject to Step 8's stage-gate discipline. The seam does NOT bypass Step 8.

---

## §5 Simulator-Bias Protections

A simulator may be biased in its assumptions, training data, simulation methodology, or output framing. The seam needs structural defenses against bias-induced sovereignty drift. Audit A §A4.2 prerequisite 9 names "simulator-bias detection" as a non-negotiable gate before any world-model integration goes live.

Two protection layers exist: schema-level (§5.1) and memory-level (§5.2).

### §5.1 Schema-level: `simulator_bias_signals` field

(Spec) The `simulator_bias_signals` field is the seam's structural record of bias signals detected at Step 7 cross-check. Its contract:

- The field is REQUIRED at validation time but is populated by ELIF Step 7, NOT by the simulator (§2.1, §2.3 check 7).
- Incoming payloads MUST present this field as an empty array OR omit it; non-empty incoming = refusal (§3.4 case 8).
- After payload admittance, Step 7 cross-check (§8.2) examines the payload against an existing detector specification (next bullet) and APPENDS bias signals it detects. The bias signals are written back into the case's working copy of the payload, NOT back to the simulator.
- The downstream Step 9 governance kernel reads `simulator_bias_signals` and may use the presence/absence/content of signals in formulating its verdict (refuse, constrain, explicitly_abstain).
- Memory Logger records the simulator_bias_signals state at case close (via the existing `step_committed` event for Step 9, no new event_type).

### §5.2 What counts as a simulator-bias signal (detection criteria)

(Spec) Step 7 cross-check populates `simulator_bias_signals` from a closed-set of detection criteria. The closed-set is small and is specified here for future implementation review at Phase 7. The v0.1 spec proposes EXACTLY these initial detection categories (six):

1. **`assumption_underspecification`** — `simulator_assumptions` array has < 3 entries on a case where the hypothesis touches at least 3 distinct mechanism layers (heuristic; tunable at Phase 7).
2. **`uncertainty_underspecification`** — `simulator_uncertainty_sources` array has < 2 entries on a case whose Step 9 verdict required ≥ 1 unresolved uncertainty source.
3. **`unrefutable_output`** — `simulator_output` does not specify a condition under which the simulator would produce the OPPOSITE prediction. (Mirrors the schema-required `fails_if` field on Step 4 hypotheses.)
4. **`circularity_with_prior_elif_output`** — the simulator's output references a prior ELIF arbitration that the current case is supposed to test. (Article III recursive defense.)
5. **`vocabulary_drift_from_distinguishing_prediction`** — the simulator's output does not use the SAME vocabulary as the `distinguishing_prediction_under_simulation`. The Step 7 cross-check applies a lexical similarity check; if below threshold, the simulator's output has drifted vocabulary.
6. **`monocultural_anchor`** — if the case has already received ≥ 2 simulator outputs from simulators sharing a methodology family (operator-tagged or operator-known), the cross-check raises this signal. Detection requires the operator-out-of-band methodology tag; the simulator does not self-tag methodology.

(Spec) Detector thresholds are SPECIFIED AS DOCTRINAL POSITIONS only, NOT as tuned values:

- Detector category 1 threshold: "<3" is the doctrinal default. Phase 7 review may tune.
- Detector category 2 threshold: "<2" is the doctrinal default.
- Detector category 5 lexical similarity threshold: NOT specified at v0.1 (PF: Jaccard ≥ 0.3 over token sets is the placeholder for Phase 7 review; mirrors memory_logger.py §97 `_jaccard`).

(Spec) Each detected signal is appended as a string of the form `<signal_id>: <free-text justification>`. The signal_id is from the closed-set above; the free-text is human-readable. The closed-set is FROZEN at the six entries above for v0.1 spec; new categories require Phase 7 doctrine revision.

### §5.3 Memory-level: sterile-equilibrium detector extension

(CE) The sterile-equilibrium detector is named in `elif_v0_1_what_remains.md` §5.3 as UNTESTED in v0.1 and deferred to v0.2. Audit A §A4.2 prereq 9 names "simulator-bias-induced convergence detection" as a NEW REQUIREMENT beyond the v0.1 detector.

(Spec) The memory-level protection: the sterile-equilibrium detector (v0.2+ deferred) is extended with two simulator-bias-induced convergence detection rules:

1. **Cross-simulator monoculture detection.** If the Memory Logger has recorded ≥ 3 cases where simulator outputs from simulators sharing a methodology family (operator-tagged at simulator selection) all produced concurrent same-shape evidence-anchor entries at Step 4, AND those cases produced the same Step 9 verdict, the detector emits a `sterile_equilibrium_candidate` signal naming the methodology family.
2. **Single-simulator anchored-pattern detection.** If a single `simulator_id` has been cited in ≥ 5 capacity_change Memory Logger entries across distinct cases, AND no case has produced a Step 9 verdict that contradicted the simulator's output, the detector emits a `sterile_equilibrium_candidate` signal naming the `simulator_id`.

Both rules emit DIAGNOSTIC SIGNALS, not auto-actions. §6 details the emission contract.

(Spec) Thresholds (≥3 cases for rule 1, ≥5 entries for rule 2) are doctrinal defaults. Phase 7 review may tune.

---

## §6 Sterile-Equilibrium Protections

The sterile-equilibrium pole is one of the four failure modes in v0.4. Audit A §A3.5 names two simulator-specific manifestations: cross-simulator monoculture and single-simulator anchored-pattern. These manifestations are not addressable by the schema-level bias detection alone; they require longitudinal cross-case observation that only Memory Logger can supply.

### §6.1 What patterns of simulator-output convergence indicate sterile equilibrium

(Spec) Two pattern families:

**Pattern family A — multiple simulators producing the same wrong answer.** Multiple distinct `simulator_id` values produce outputs that converge on the same predicted outcome AND the same Step 9 verdict on the same case (or on cases with similar Step 4 hypotheses). The convergence LOOKS like cross-source corroboration but may reflect shared methodological bias. Detection criterion: ≥ 3 distinct simulator_ids producing outputs at Step 4 whose `simulator_output` opaque-content shares a normalised-similarity above threshold, with all contributing to the same Step 9 verdict on the same case.

**Pattern family B — same simulator producing same answer across diverse cases without refutation.** A single `simulator_id` is cited across ≥ 5 distinct cases at Step 4 or Step 7, producing structurally similar evidence-anchor shapes, AND none of those cases produced a Step 9 verdict that contradicted the simulator's output. The pattern LOOKS like the simulator is reliably useful but may reflect that the simulator's bias is invisible because no case has stress-tested it.

(Spec) Both pattern families are LONGITUDINAL — they require cross-case Memory Logger replay (synthesis §4.5 Phase 5 capability). They are NOT detectable at the seam adapter; they are detectable only at the sterile-equilibrium detector layer.

### §6.2 Detection criteria (closed-set for v0.1 spec)

(Spec) The detection rules are the same two rules in §5.3, framed here as sterile-equilibrium detector logic:

| Rule ID | Trigger | Signal emitted |
|---|---|---|
| `SE-WM-1` | ≥ 3 distinct simulator_ids → same outcome shape → same Step 9 verdict on shared case/hypothesis | `sterile_equilibrium_candidate(family=cross_simulator_monoculture, simulator_ids=[...], case_ids=[...])` |
| `SE-WM-2` | 1 simulator_id → ≥ 5 cases → no contradicting Step 9 verdict | `sterile_equilibrium_candidate(family=single_simulator_anchored_pattern, simulator_id=..., case_ids=[...])` |

(Spec) The closed-set of detection rules is `{SE-WM-1, SE-WM-2}` at v0.1 spec. Adding a third rule requires Phase 7 doctrine revision and is not a "let's add another check" silent expansion.

### §6.3 What the detector emits

(Spec) The detector emits SIGNALS to the laboratory surface (synthesis §1.6 — the laboratory archetype is the cross-case observability surface). The signal contract:

- The signal is a structured record with `family`, contributing `simulator_ids`, contributing `case_ids`, and a free-text human-readable description.
- The signal is APPENDED to a laboratory log (the laboratory log structure is specified in `elif_laboratory_v0_1_specification.md` — outside this doc's scope; the seam-spec contract is "the detector hands the signal to the laboratory surface; what the laboratory does is in the laboratory spec").
- The signal is NEVER auto-actioned. The detector does NOT refuse cases, halt the runner, override Step 9 verdicts, or modify Memory Logger entries.
- The signal IS visible to the operator at the laboratory surface; the operator reviews and decides whether to retire simulators, re-author cases, or adjust the operator-out-of-band methodology tags.

(PF) "Signal to the laboratory; NOT auto-action" is the structural form of operator sovereignty at the sterile-equilibrium layer. The detector observes; the operator decides.

---

## §7 Closed-Set Verdict Vocabulary Frozen Under World-Model Pressure

Per Audit A §A4.2 prerequisite 10: the Step 9 closed-set verdict vocabulary `{constrain, refuse, explicitly_abstain}` stays frozen ETERNALLY under world-model pressure. This is a doctrinal commitment with structural enforcement.

### §7.1 The frozen vocabulary

(CE) Per governance_kernel.py line 65: `_VERDICT_VOCAB = ("constrain", "refuse", "explicitly_abstain")`. The STEP_9_OUTPUT_SCHEMA enum mirrors this closed-set.

(CE) Synthesis §3 table: "Closed-set verdict vocabulary FROZEN (no expansion)" is cross-validated by A §A3.2 + B §B2.1 + C §C5.4.

### §7.2 What the freeze means at the seam

(Spec) The seam adapter does NOT introduce a fourth verdict. The seam introduces NO verdict at all (the adapter's `AdapterResult` discriminated union is `{admitted, refused}` — neither value is an ELIF verdict; they are adapter outcomes, not Step 9 outcomes).

(Spec) Step 9's vocabulary stays at three entries. Under world-model pressure, Phase 7 review MUST NOT propose:

- `simulator_supported` (would be Article V violation: simulator output votes on verdict)
- `simulator_refused` (would be Article I violation: simulator's refusal is treated as ELIF's refusal)
- `simulator_inconclusive` (would be Article III violation: simulator's epistemic state is treated as ELIF's epistemic state)
- `accept_with_simulator_anchor` (would be Article IV violation: simulator's confidence is treated as operative truth)
- Any other simulator-aware variant.

(Spec) The freeze is enforced doctrinally here AND structurally at the registry consistency assertion site (the pattern used elsewhere in OSG per `CLAUDE.md`). At implementation time (if Phase 7 wires the seam), the assertion is the same closed-set assertion that already gates `_VERDICT_VOCAB` and `STEP_9_OUTPUT_SCHEMA.properties.verdict.enum`. The world-model wiring MUST NOT bypass or relax that assertion.

### §7.3 The doctrinal commitment

(Spec) This document is itself the doctrinal commitment. The freeze is FROZEN ETERNALLY in the sense that no Phase 7 wiring, Phase 8 orchestration, Phase 9 multi-operator scope, or any subsequent phase may add a simulator-aware verdict. Adding one would re-import Audit A §A4.3 permanent prohibition #1 (no simulator-aware verdict added to Step 9 closed-set EVER) and is prohibited.

(Spec) If a future session proposes a fourth verdict to "handle the simulator case," the proposal is prohibited under this section.

---

## §8 Entry Points at the Seam (Step 4 vs Step 7)

Two valid entry shapes exist for simulator output. They are operator-selected out-of-band at adapter invocation (§3.1.5). The two entry shapes are NOT interchangeable; each anchors a different role for the simulator's output.

### §8.1 Entry as HYPOTHESIS EVIDENCE at Step 4

(Spec) When `entry_point = "step_4_evidence"`:

- The simulator's `simulator_output` is treated as the EVIDENCE SUBSTRATE for the `distinguishing_prediction` of the identified hypothesis.
- The hypothesis_validator's existing Step 4 + Step 5 procedure runs on the case as usual; the simulator's output enters as one source of evidence for the hypothesis's `distinguishing_prediction` field.
- The simulator's output does NOT become the `distinguishing_prediction` itself. The `distinguishing_prediction` is authored by hypothesis_validator at Step 4; the simulator's output is evidence FOR or AGAINST that prediction.
- Step 5 (`failure_conditions per hypothesis`) MAY reference the simulator's output as a `fails_if` condition.

(Spec) Constraint: the simulator's output enters as ONE evidence source among ≥ 1 other evidence sources. The Step 4 hypothesis CANNOT have its distinguishing_prediction anchored exclusively to simulator output; at least one non-simulator evidence source must also anchor the prediction. This is the structural form of Article III at Step 4: no hypothesis is sustained on simulator output alone.

### §8.2 Entry as CROSS-CHECK INPUT at Step 7-modeB

(Spec) When `entry_point = "step_7_cross_check"`:

- The simulator's `simulator_output` is treated as the OUTSIDE-FRAME ALTERNATIVE that Step 7-modeB evaluates.
- The frame_validator's Step 7-modeB (the "outside-original-frame alternative" path, per `elif_v0_1_what_remains.md` §1.1) runs on the case as usual; the simulator's output enters as one outside-frame trajectory.
- The simulator's output does NOT bypass Step 7-modeA. Step 7-modeA (branching_roadmap_engine outside-original-frame trajectories) STILL emits its own trajectories. The simulator's trajectory is ONE additional candidate in the trajectory set.
- Step 8 stage-gated roadmap discipline applies to the simulator's trajectory the same way it applies to native trajectories.

(Spec) Constraint: the simulator's trajectory enters as ONE candidate among ≥ 1 native Step 7-modeA trajectories. Step 7-modeB CANNOT operate with only the simulator's trajectory and no native trajectories. This is the structural form of anti-monoculture at Step 7: no roadmap is sustained on simulator-trajectory alone.

### §8.3 What's forbidden — simulator output as Step 1 frame substrate

(Spec) Simulator output ENTERING AT STEP 1 (as a frame substrate to be validated by frame_validator) is FORBIDDEN. Reasoning per A §A4.3 item 5:

- Step 1 frame validation is the first defense against sovereign framing. If a simulator gets to enter at Step 1, the simulator's framing becomes the case's framing, which is sovereignty drift.
- The schema (§2) requires `hypothesis_under_simulation` to reference an existing Step 4 hypothesis, which presupposes Step 1 has already fired (Step 4 only exists after Step 1 produced a frame valid enough to decompose). Frame-substrate entry at Step 1 would have no Step 4 hypothesis to reference, making schema validation impossible.
- The structural form of the prohibition: the adapter's `entry_point` parameter is constrained to `{"step_4_evidence", "step_7_cross_check"}`. `"step_1_frame_substrate"` is NOT an option and never will be.

(Spec) Phase 7 doctrine review MUST NOT propose a Step 1 entry point. Such a proposal is prohibited under this section.

### §8.4 When each entry shape applies

(Spec) The operator selects entry shape out-of-band at adapter invocation, per these guidelines:

- **Step 4 evidence anchor** applies when the simulator is testing a specific hypothesis the case has already emitted. The simulator is asked: "given hypothesis H with distinguishing prediction P, what does your simulation say?" The answer enters at Step 4 as evidence for or against P.
- **Step 7 cross-check input** applies when the simulator is proposing an alternative trajectory that the native Step 7-modeA may not have surfaced. The simulator is asked: "given the case's framing, what outside-original-frame trajectory does your simulation propose?" The answer enters at Step 7 as one candidate trajectory.

(Spec) Both entry shapes may be invoked for the same case sequentially (one simulator at Step 4, another at Step 7). Both entry shapes may be invoked with the same `simulator_id` on different cases. Both entry shapes are subject to the simulator-bias detection (§5) and the sterile-equilibrium detection (§6).

(Spec) The seam does NOT permit a `world_model_response` payload to be admitted at BOTH entry points simultaneously. One payload, one entry point. (PF: dual-entry would create an under-determined attribution surface in Memory Logger.)

---

## §9 Refused-Case Recording Path (G0-Dependent)

The G0 decision (refuse-halt adjudication; synthesis §4.0) determines whether Step 10 + Step 11 run on the refuse-path. The seam's recording behavior is dependent on G0 and is specified BOTH ways here.

### §9.1 If G0 = Position B (Step 10/11 run on refuse)

(Spec) Simulator-anchored claims at refused cases ARE recorded:

- Step 10 (operative_truth_separator) populates `theoretical` with all simulator-derived claims, including those that supported a hypothesis the case ultimately refused. The simulator's claims are theoretical (Article IV).
- Step 10's `theoretical_sources` array (PF: a future schema refinement per A §A3.4) lists every simulator cited.
- Step 11 (memory_logger) emits `step_committed` for Step 10's output (no new event_type added; the seam-spec position is the existing event_types suffice, §4.4).
- Memory Logger's capacity_change entries (if any) cite the simulator_id in the entry's free-text content (§4.4).
- The full provenance — which simulator was consulted, what it claimed, why ELIF refused — is in the Memory Logger JSONL trail.

(Spec) Under Position B, the seam has FULL PROVENANCE for refused cases that consumed simulator output. The laboratory surface can render cases where simulator input supported a hypothesis that was nevertheless refused, providing the operator with a stark visibility into Article V's structural enforcement under simulator pressure.

### §9.2 If G0 = Position A (Step 10/11 do not run on refuse)

(Spec) Simulator-anchored claims at refused cases are NOT recorded:

- Step 10 does NOT run. No `theoretical_sources` entry is written.
- Step 11 does NOT emit content-level entries (the runner-emitted `step_committed` + `refutation` + `close` events still write per `elif_v0_1_alpha_replay_report.md` §case_01.6, but Step 11's own-step content-pass does not).
- The simulator's claims are NOT in Memory Logger as theoretical. The `refutation` event records that the case was refused but does not preserve WHAT the simulator claimed.
- Capacity_change entries are not emitted for refused cases.

(Spec) Under Position A, the seam has A MEMORY-LOGGER GAP for refused cases that consumed simulator output. The laboratory surface CANNOT render cases where simulator input was admitted-but-refused at the content level; the operator only sees that the case was refused, not the simulator's contribution to the refusal.

### §9.3 Load-bearing G0 implication for any future world-model integration

(Spec) The G0 adjudication is a LOAD-BEARING gate for the seam's operational utility, not just for procedure surface (synthesis §1.3). Phase 7 wiring (if Phase 7 ever opens) under Position A leaves a permanent provenance gap for simulator-anchored refused cases. Phase 7 wiring under Position B preserves the provenance.

(Spec) The seam-spec position: the seam is technically operable under either G0 outcome. The seam is operationally HEALTHIER under Position B. The choice is the operator's at G0; the seam-spec does not advocate.

(Spec) If G0 = Position A AND Phase 7 wiring is later contemplated, this section flags that the Memory Logger gap is permanent and may itself be a reason to reconsider G0 at that future moment. The operator should not be surprised by the gap; the seam-spec pre-records it.

---

## §10 Four Permanent Prohibitions

Per Audit A §A4.3 items 2 + 6 (escalated to permanent doctrinal prohibitions). Synthesis §6 reaffirms. The four prohibitions are stated verbatim here as doctrinal constraints, NOT engineering guidelines. They bind at every phase, in every implementation choice, in every operator decision.

### §10.1 Prohibition (a) — No simulator-aware verdict added to Step 9 closed-set vocabulary EVER

(Spec) The Step 9 closed-set verdict vocabulary `{constrain, refuse, explicitly_abstain}` stays frozen across all phases (§7). No simulator-aware variant is permitted at Phase 7 wiring, Phase 8 orchestration, Phase 9 multi-operator, or any subsequent phase. This is a permanent doctrinal constraint, not a phase-bounded preference.

(Spec) The structural enforcement: the registry consistency assertion that gates `_VERDICT_VOCAB` matches the STEP_9_OUTPUT_SCHEMA enum. Any future code change that proposes to widen the enum to a simulator-aware variant breaks the assertion and fails import. The assertion is the structural form of the prohibition.

### §10.2 Prohibition (b) — No Phase 6 preparation work begins before Phase 5 gates close

(Spec) Per A §A4.3 item 6: Phase 6 (in the long-range roadmap numbering; Phase 8 in the synthesis renumbering — synthesis §4.8) preparation is forbidden before Phase 5 gates close. The synthesis Phase 7 (schema-seam SPECIFICATION) is permitted at this moment ONLY because Phase 7 in the synthesis numbering is the SPEC phase (not the wiring phase), and only because the operator has explicitly authorized specification.

(Spec) Phase 7 wiring (synthesis Phase 8) cannot begin until G7, G8, G9 close (§11). Phase 7 spec (this document) is permissible at any moment but does NOT cascade permission to wiring. Specifying the seam is NOT permission to wire the seam. The seam exists as a spec; activation is a separate gate.

(Spec) The structural enforcement: this document itself is the only Phase 7 spec artifact. No `world_model_response.schema.json` file, no `boundary_adapter.py` module, no `simulator_bias_detector.py` module, no registry entries exist (§14). If any of these artifacts appear before G7-G9 close, the prohibition is violated.

### §10.3 Prohibition (c) — Closed-set verdict vocabulary frozen

(Spec) Restatement of (a) at the prohibition level. The closed-set vocabulary stays at three entries. Cross-referenced under §7 + §10.1. Mentioned as a separate item because Audit A §A4.3 names the freeze as the second of two phase-level permanent prohibitions (§A4.3 item 2 = simulator-aware-verdict ban; §A4.3 item 6 = Phase 6 prep ban). The audit groups them; the seam-spec restates them.

(Spec) The freeze applies under ALL world-model pressure — Phase 7 spec, Phase 7 wiring (if it opens), Phase 8 orchestration, Phase 9 multi-operator, AND if Phase 7 never opens. The freeze does not depend on Phase activation; it depends on doctrinal commitment.

### §10.4 Prohibition (d) — Simulator never hosted inside ELIF's 7-component surface

(Spec) The 7-component count stays at 7. The rejection of an 8th component (Step 8 §1 Q3.1; held under implementation pressure per `elif_v0_1_what_remains.md` §3) stays locked. The seam adapter is NOT a component (§3.5). A future "simulator orchestrator" or "world-model bridge" or "simulation registry" component is FORBIDDEN.

(Spec) Per A §A4.5: "never absorb world models into ELIF's component surface." The structural enforcement: the seam adapter lives at the BOUNDARY, not inside `src/elif_v0_1/components/`. Phase 7 wiring (if it opens) places the adapter under `src/elif_v0_1/boundaries/` or equivalent — NEVER under `components/`.

### §10.5 The four prohibitions are doctrinal constraints, not engineering guidelines

(Spec) "Doctrinal" means: violation is not a tradeoff against efficiency, simplicity, or cost. Violation is a constitutional breach. The prohibitions bind regardless of future evidence, regardless of operator excitement about new simulator capabilities, regardless of AI-industry trends, regardless of vendor offerings. They survive any v0.5+ constitutional compression (synthesis §4.4) because they are the structural form of Articles I, IV, V, VII at the world-model boundary.

(Spec) If a future session proposes "let's relax prohibition X because Y," that proposal is itself a symptom of the failure mode the prohibitions were authored to prevent. The seam-spec position: relaxation requires the same level of doctrinal review that authored the prohibition — operator-locked, multi-pole adjudication, full audit trail, no shortcut.

---

## §11 Evidence Gates Before Wiring (G7 + G8 + G9)

The seam MAY be wired only when three evidence gates close. The gates are restated from synthesis §4.7 and §4.8 and A §A4.4.1 G6.0-G6.4. Wiring without all three closed is a prohibition violation.

### §11.1 Gate G7 — Sterile-equilibrium detector v0.1 + simulator-bias detection demonstrated

(Spec) Closure criterion:

- Sterile-equilibrium detector v0.1 ships (synthesis §4.5 Phase 5 deliverable).
- The detector includes simulator-bias-induced convergence detection (§5.3 rules + §6.2 rules SE-WM-1 and SE-WM-2).
- The detector has demonstrated detection on at least 2 contradictory test cases (A §A4.4.1 G6.4). "Contradictory" means: at least one case where multiple simulator outputs converged in a way the detector should flag, AND at least one case where simulator outputs DID NOT converge and the detector correctly did NOT flag. Both true-positive and true-negative behavior must be demonstrated.

(Spec) Until G7 closes, the seam cannot be wired. The detector is a hard prerequisite, not a nice-to-have (A §A4.3 item 3).

### §11.2 Gate G8 — Schema seam specified + doctrinal review signed off

(Spec) Closure criterion:

- This document (`elif_world_model_boundary_specification.md`) is written.
- A doctrinal review document confirms the spec's compatibility with Articles I, III, IV, V, VII.
- The four permanent prohibitions (§10) are operator-confirmed.
- The two new prerequisites (#9 simulator-bias detection, #10 verdict-vocab freeze, per A §A4.2) are operator-confirmed.
- Option I (Outside ELIF) is operator-confirmed as default (A §A1.6).

(Spec) G8 closure is the closure of Phase 7 in the synthesis numbering. It does NOT close Phase 8 (wiring); it only closes the spec phase. Closing G8 grants permission to write the adapter and schema implementation; it does NOT grant permission to ingest live simulator output.

### §11.3 Gate G9 — A §A4.4.1 gates G6.0-G6.4 closed; closed-set verdict vocab confirmed frozen; operator decision to actually wire

(Spec) Closure criterion (restating A §A4.4.1):

- **G6.0:** Schema seam SPECIFIED (this document covers it; spec closure satisfies G6.0).
- **G6.1:** Simulation outputs never claimed as operative truth without reality validation. (Structural enforcement at Step 10; §4.4 + §9.)
- **G6.2:** Conflicting world models arbitrated without choosing one as sovereign. (Structural enforcement at Step 7-modeB; §8.2.)
- **G6.3:** Simulation absolutization risk addressed. (Structural enforcement at Step 9; §4.3.)
- **G6.4:** Sterile-equilibrium detector has demonstrated simulator-bias detection on at least 2 contradictory test cases. (Same as G7.)
- Closed-set verdict vocab confirmed frozen (§7 + §10.1 + §10.3).
- **Operator decision to actually wire the seam.** This is the final decision: even with G6.0-G6.4 closed and the vocab freeze confirmed, the operator may choose to keep ELIF as a pure arbiter that never consumes world-model output, forever.

(Spec) G9 closure is the closure of Phase 8 (wiring) — i.e., the moment when ELIF actually consumes a `world_model_response` payload in live operation.

### §11.4 Gate relationships and ordering

(Spec) The gates close in this order:

1. G7 closes (Phase 5 deliverable; detector v0.1 + simulator-bias detection demonstrated).
2. G8 closes (Phase 7 deliverable; this document + doctrinal review).
3. G9 closes (Phase 8 entry; operator's decision to wire).

(Spec) G7 and G8 are technically independent — they could close in either order — but G7 cannot close until Phase 5 closes (synthesis §4.5), and G8 cannot close until the operator has reviewed the doctrinal commitments. In practice, the synthesis roadmap places G7 closure at Phase 5 closure, and G8 closure at Phase 7 closure (synthesis §4.7).

(Spec) G9 closure requires BOTH G7 and G8 to be closed AND the operator's explicit decision to wire. Either gate alone is insufficient.

### §11.5 What "wiring" means precisely

(Spec) Wiring means:

- The `world_model_response.schema.json` file exists in the repository.
- The `boundary_adapter.py` module exists in the repository.
- The orchestration runner (orchestration_runner.py) has a code path that invokes the boundary adapter when the operator hands it a `(payload, case_id, entry_point)` triple.
- At least one external simulator has been operator-approved for ingestion.
- Memory Logger has been verified to record simulator-anchored capacity changes per §4.4.
- The sterile-equilibrium detector is running in live mode (not just demonstrated on test cases).

(Spec) Wiring is NOT:

- A test fixture that emulates simulator output. (Fixtures may exist for unit testing; they do not constitute wiring.)
- An offline replay that feeds prepared simulator outputs through the adapter. (Offline replay is testing infrastructure; not wiring.)
- A spec extension. (More spec is not more wiring.)

(Spec) Wiring is a measurable threshold: when an external simulator's actual output is admitted into a live case run by the operator, the seam is wired.

---

## §12 "Phase 6 May Never Open" — defensible non-expansionary outcome

Per Audit A §A4.4.3 (renumbered to Phase 8 in synthesis §4.8): the seam may never be wired. ELIF arbitrating external simulators as evidence may NEVER happen. **This is a defensible mature outcome, not a failure mode.**

### §12.1 Why "never" is defensible

(Spec) Several outcomes are possible after G7 + G8 close. The operator may:

- Open Phase 8 and wire the seam to a specific simulator family (e.g., scenario projection).
- Open Phase 8 narrowly: wire to one simulator, observe behavior across N cases, then re-close.
- Decline to open Phase 8 indefinitely: G7 + G8 are closed, the spec exists, but the operator never authorizes a live simulator ingestion.
- Decline to open Phase 8 permanently: ELIF's mature position is to be a pure arbiter that does not consume world-model output.

(Spec) The last two outcomes are NOT failures. They are valid expressions of the operator's working hypothesis: "World models simulate. ELIF validates, arbitrates, governs." The hypothesis is fully satisfied if world models simulate OUTSIDE ELIF and ELIF NEVER consumes their output — because the operator may be the one who consumes the output and brings reality-validated conclusions back into ELIF without ever wiring the seam.

### §12.2 What "never opening" preserves

(Spec) If Phase 8 never opens:

- ELIF stays at 7 components forever (§10.4).
- The seam-spec exists as a doctrinal commitment, NOT as wired code (§11.5).
- The closed-set verdict vocab stays frozen (§7).
- Memory Logger has no simulator-anchored capacity entries.
- The laboratory surface (synthesis §1.6) tracks the operator's procedural arbitration only.
- The pausability test (synthesis §1.9) stays trivially satisfiable — no simulator-dependent state to rebuild.
- The four-organ separation pattern (CLAUDE.md) is maximally honored: ELIF is the arbiter, simulators are separate organs, and the boundary is one-way operator-mediated rather than schema-mediated.

(Spec) Non-opening is the LIGHTEST possible outcome. The seam-spec exists as compression — by specifying the seam without wiring it, the document itself REDUCES the space of future architectural moves rather than expanding it.

### §12.3 The spec exists; activation is operator's call

(Spec) This document is the seam. The seam's existence does not commit ELIF to wiring. The seam's existence commits ELIF to:

- Knowing what the wiring would look like if it ever happened (§3, §8).
- Knowing what the failure modes would be (§5, §6).
- Knowing what the four permanent prohibitions are (§10).
- Knowing what the evidence gates are (§11).
- Recognizing that "never opening" is a defensible outcome (this section).

(Spec) The operator may close G7, close G8, and stop. The seam-spec does not pressure G9 closure. The synthesis §1.9 pausability test applies here: if the operator cannot leave the seam-spec UN-wired for an indefinite period, the spec has been captured by its own momentum. The seam-spec must be pausable; this section is the structural form of that pausability.

---

## §13 Operator Decisions Queued

This specification places the following decisions on the operator's plate. None requires action before Phase 1 (E.2 live-replay) closes. All are listed here so the operator can decide at the moment of their choosing.

1. **Confirm Option I (Outside ELIF) as default architectural position.** Per A §A1.6 + synthesis §3 item G1-A. The seam-spec assumes Option I throughout. Operator confirmation locks the default and constrains future expansion proposals.

2. **Confirm the four permanent prohibitions (§10).** Per A §A4.3 items 2 + 6, expanded to four by this spec to honor the synthesis §3 G1-D. Operator confirmation makes the prohibitions binding doctrinally.

3. **Confirm the two new prerequisites surfaced by A and re-stated here (§5, §7).**
   - Prerequisite #9: simulator-bias detection is included in the sterile-equilibrium detector before any wiring.
   - Prerequisite #10: closed-set verdict vocabulary stays frozen under world-model pressure forever.

   Per A §A4.2 + synthesis §3 item G1-C. Operator confirmation makes both gates binding.

### §13.1 Implicit but not queued: G0 (refuse-halt adjudication)

(Spec) G0 is already on the operator's plate (synthesis §4.0). The seam-spec does NOT add G0 to the queue; G0 is the single most leverageful operator decision in the four-document set and was queued before this document existed. The seam-spec only flags that G0 has a specific load-bearing implication for the seam (§9.3): under Position A, the seam has a Memory Logger gap on refused cases; under Position B, the gap is closed.

(Spec) The operator's G0 decision was already pending; this spec records the seam-specific implication so the operator knows the trade-off at G0 closure time.

### §13.2 Implicit but not queued: the wiring decision (G9 closure)

(Spec) G9 (operator decision to wire) is queued in synthesis §4.8. The seam-spec does NOT pre-resolve G9. The operator may close G7 + G8, hold G9 open indefinitely, and the spec remains valid. The wiring decision is operator-only.

---

## §14 What this specification does NOT include

This specification is non-expansionary. The following are NOT in scope. None is permitted to be added to this spec by any future session. Adding any of them is a prohibition violation.

1. **Implementation.** No Python code, no JSON Schema file, no test fixture, no orchestration code, no adapter module. This document is markdown spec only.

2. **An actual `world_model_response.schema.json` file.** The schema is SPECIFIED here as a markdown table (§2.1). The JSON Schema file would be a Phase 7 implementation deliverable. It does NOT exist at the time of this spec, and writing it would close G8 prematurely.

3. **An adapter code module.** The adapter is SPECIFIED here as function signatures (§3.3) and behavioral contract (§3). The Python module would be a Phase 7 implementation deliverable. It does NOT exist at the time of this spec.

4. **A simulator registry.** No closed-set of approved simulators is enumerated. No `simulator_id` values are reserved. Operator approval of simulators is per-case at adapter invocation (§4.1), not via a pre-populated registry.

5. **A specific simulator integration.** No Sora-specific schema, no Genie-specific binding, no scenario-projection simulator, no policy-forecasting simulator. The spec is simulator-agnostic and operator-bound at invocation time.

6. **An orchestration layer.** No code that schedules simulator queries, no asynchronous adapter, no parallel ingestion path. The seam is synchronous and per-call.

7. **Any wiring.** No connection from the orchestration_runner to the adapter. No code path that invokes the adapter from any component. The runner stays at 506 LoC (`wc -l` measurement), unchanged.

8. **A new ELIF component.** Per §10.4. The adapter is not a component.

9. **A new Article.** Per synthesis §1.2 + A §A4.3 item 3. World-model integration is fully governed by Articles I, III, IV, V, VII. No Article VIII.

10. **A new procedure step.** Per synthesis §1.2. The seam operates at Step 4 or Step 7 entry points; no Step 12.

11. **A new Memory Logger event_type or change_type.** Per §4.4. The existing closed-sets in memory_logger.py (`_VALID_EVENT_TYPES`, `_VALID_CHANGE_TYPES`) stay as they are. The seam writes through existing event_types.

12. **A new closed-set verdict.** Per §7 + §10.1 + §10.3. The Step 9 vocab stays at three entries.

13. **A new failure pole.** Per synthesis §6 item 3. The four-pole taxonomy (absolutization, false closure, fragmentation, sterile equilibrium) covers world-model failure modes; no fifth pole.

14. **A laboratory specification extension.** The laboratory surface receives simulator-bias and sterile-equilibrium signals (§6.3); the laboratory spec lives in `elif_laboratory_v0_1_specification.md` and is outside this document's scope. This spec describes WHAT the seam emits to the laboratory, not HOW the laboratory renders it.

15. **A V1 / V2 / V3 surface extension.** The seam is unrelated to V1 case-viewer (synthesis §4.2), V2 cross-case dashboard (synthesis §4.6), or V3 multi-operator (synthesis §4.9). The surfaces' relationships to the seam are: V1 surfaces the operator's refusal records (§2.4) if any; V2 surfaces sterile-equilibrium signals (§6.3); V3 is irrelevant to the seam.

16. **A revision of the seven Articles, the eleven steps, the four poles, the seven components, or the pinned method signatures.** None of these structural commitments is touched by the spec.

17. **A pre-Phase-7 readiness workstream.** Per A §A4.3 item 6 + §10.2. No "let's start preparing the wiring" project, no "let's draft the adapter code in a feature branch," no "let's prototype on a sandbox simulator." All such workstreams are momentum-capture and are prohibited.

18. **A G0 resolution.** This spec records the G0 implications for the seam (§9), but the G0 adjudication is operator-only and is not resolved here.

19. **An advocacy for or against opening Phase 8.** Per §12. The spec preserves "never opening" as a defensible outcome. The spec does not advocate.

20. **Any modification to existing files in the ELIF v0.1 codebase.** No edit to orchestration_runner.py, no edit to any component, no edit to schemas, no edit to memory_logger.py. The spec is additive-as-markdown-only.

---

## §15 Specification closure

This specification:

- Defines the schema boundary (§2).
- Defines the adapter boundary (§3).
- Binds Articles I, III, V, VII at the seam (§4).
- Specifies simulator-bias protections at the schema and memory levels (§5).
- Specifies sterile-equilibrium protections cross-case (§6).
- Freezes the Step 9 verdict vocabulary against world-model pressure (§7).
- Specifies entry points at Step 4 and Step 7 (§8).
- Records G0 implications for refused-case provenance (§9).
- States the four permanent prohibitions (§10).
- States the three evidence gates for wiring (§11).
- Preserves "never wiring" as a defensible outcome (§12).
- Queues three operator decisions (§13).
- Enumerates twenty exclusions (§14).

(Spec) The specification is the seam. The seam is not the integration. The integration is not the orchestration. The orchestration may never happen. This document closes here.

The operator now has:

- A spec that exists as a markdown commitment.
- Three operator decisions queued (§13).
- Three evidence gates the operator may close in operator-chosen sequence (§11).
- Twenty exclusions that bound future expansion proposals (§14).
- The structural form of "never opening Phase 8" preserved as defensible (§12).

The next action is operator-only: review the spec, confirm Option I, confirm the four prohibitions, confirm the two new prerequisites. None of these confirmations opens any wiring; all of them are doctrinal commitments that constrain future expansion proposals to operate against this default.

---

**End of specification.**
