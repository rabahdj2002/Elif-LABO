# ELIF V1 Decision Room — Specification

> **Captured:** 2026-05-30
> **Status:** Operator-level specification of the V1 decision-room surface. Non-expansionary. Evidence-gated.
> **Authority:** Specification, not implementation. The operator will decide stack separately. This document does not commit a stack, does not commit a render engine, does not commit a deployment target.
> **Doctrine constraint:** V1 is the MINIMUM operator-facing surface that honors the v0.1-alpha substrate without re-importing affordances the audits (A, B, C) and the synthesis explicitly forbid. Per-case only. No cross-case. No expansion beyond what already exists.
> **Inputs read:** `notes/elif_audit_synthesis.md`, `notes/elif_audit_a_world_models.md`, `notes/elif_audit_b_user_experience.md`, `notes/elif_audit_c_media_communication.md`, `notes/elif_v0_1_what_remains.md`, `notes/elif_v0_1_alpha_replay_report.md`, `notes/elif_v0_1_alpha_cost_complexity_report.md`, `src/elif_v0_1/components/*.py`, `src/elif_v0_1/orchestration_runner.py`, `src/elif_v0_1/components/memory_logger.py`, `src/elif_v0_1/schemas/__init__.py`.
> **Epistemic registers used throughout:** CURRENT EVIDENCE (CE) — demonstrable from shipped v0.1-alpha; PLAUSIBLE FUTURE (PF) — projection if alpha behavior holds under E.2 live-replay; SPECULATION (SP) — beyond reasonable projection, labeled and non-load-bearing.

---

## Preface — what this spec is and what it is not

(CE) V0.1 alpha ships at 7 components / 11 steps / 2,533 component LoC / 8,424 total LoC, producing 9 schema-valid step JSONs + a MemoryLogger JSONL trail + a structured RunReport (exit_code=20 = GovernanceRefuseError) on each of the 3 operator-locked alpha cases. The structured outputs and the JSONL trail ARE the substrate this V1 surface renders. There is no new substrate.

(CE) Audit B settles UX archetype = decision-room (per-case) + laboratory (cross-case). Audit C settles communication object = arbitration trace, not knowledge. The synthesis §1.5 settles "the structured output IS the deliverable; rendering layer must remain small" with `rendering LoC ≤ 0.3 × substrate LoC` as the operational test (per C §C7.6).

(CE) Audit B and Audit C diverge on the user-visible stage count: B §B3.4 settles 8 stages; C §C5.3 settles ~7 surfaces. The synthesis §2.1 treats this as a UI design question, not an architectural question, with both choices doctrinally defensible. This spec keeps the 7-vs-8 choice as a queued operator decision (§13) and writes the surface inventory below as 7 screens with a documented 8-screen variant.

(CE) This spec is the V1 specification, where V1 = the minimum operator-facing surface per-case. It is NOT V2 (cross-case / laboratory; synthesis §4.6 Phase 6) and NOT V3 (multi-operator; synthesis §4.9 Phase 9; SP).

This spec does not propose any new component, any new Article, any new procedure step, any new schema, any new closed-set member, any new failure pole, any new media artefact family. Every load-bearing claim anchors to a specific existing Article, Step, schema field, or audit section. Where claims cannot be anchored to current evidence, they are labeled PF or SP and never used as decision rationale.

---

## §1 V1 Scope (what is in / what is not)

### §1.1 In scope

- **Per-case decision-room surface.** One case per visit. The case is the unit of work (B §B1.7). The room is something the operator ENTERS for a decision and LEAVES; the operator does not live in it (B §B1.3).
- **Mode-agnostic rendering.** V1 surface works for offline-mode runs (deterministic, fixture-driven; current alpha mode per Step 8 §8.8) AND live-mode runs (Anthropic API calls, ~$0.21/case projected). The surface does not distinguish — both produce the same step-JSON shapes. The mode is metadata; the surface is invariant.
- **Single operator.** No multi-operator infrastructure. V1 is single-operator-on-single-case. Authentication, attribution, conflict resolution — all out of scope (C §C6.3 SP-labeled).
- **CLI rendering required; minimal HTML/static rendering optional.** Per C §C6.1, V1 is "CLI + minimum text UI rendering Step 1–9 outputs; read-only after submit." HTML/static is a second target for the same data; queued as operator decision (§13).
- **Refuse-aware rendering.** exit_code=20 is the CORRECT verdict (CE: alpha replay produces refuse on all 3 cases; the runner halt is Article V structurally enforced). V1 surface renders refuse as the load-bearing communication object, not as failure.
- **Schema-validated step outputs as the source.** The surface reads existing `step_NN__case_XX.json` files (or live equivalent), the MemoryLogger JSONL trail, and the RunReport. No new files written by V1.
- **Read-only.** No edit affordances. No re-run affordance. No "tweak the prompt" affordance (B §B-non-recommendations 8; B §B3.6).

### §1.2 Out of scope (and why)

- **No cross-case views.** Cross-case is the laboratory archetype (B §B1.4) = V2 cross-case dashboard (C §C6.2) = synthesis Phase 6. Gated on Phase 5 MemoryLogger maturation (synthesis §4.5). Per §1.1 V1 is per-case only.
- **No LLM-prose summarization layer.** No "explain this verdict in plain language" affordance (B §B-non-recommendations 4; C §C7.8). Importing prose-summarization re-imports the chatbot affordance Article I refuses at the surface layer.
- **No chatbot, no conversational turn, no message thread.** B §B1.1 settles chatbot framing as ACTIVELY COUNTERPRODUCTIVE.
- **No audio, no video, no narration.** B §B2.7-2.8 and C §C3.10-3.11 settle these as DECORATIVE/risky. Synthesis §1.4 treats this as a doctrinal lock equivalent to the 8th-component rejection.
- **No simulation views, no world-model UI.** Synthesis §1.1 + A §A1.6 keep world models OUTSIDE ELIF. Visualisation of simulator output is C §C3.8 SPECULATION deferred to A; A defers to Phase 8 (synthesis §4.8) which may never open.
- **No re-run-with-different-prompt affordance.** B §B3.6 forbids re-execution loops; B §B-non-recommendations 8 forbids prompt-tweaking surfaces.
- **No knowledge-graph, no "what ELIF has learned" surface.** B §B-non-recommendations 11; C §C7.4. Truth-accumulation framing is Article VII violation.
- **No multi-operator infrastructure.** SP per C §C6.3, §OD-C-4.
- **No public-facing surfaces.** B §B-non-recommendations 9. V1 is operator-facing.
- **No cross-product runtime coupling (to OSG / Limova / media biome).** Synthesis §1.7 permanent prohibition.
- **No editing of step outputs after they are written.** Append-only JSONL discipline + closed-set schema validation (CE: memory_logger.py `_VALID_EVENT_TYPES`, `_VALID_CHANGE_TYPES`); V1 surface honors this by being read-only.

### §1.3 Stack-agnostic posture

This spec does not commit a stack. The data shapes are existing files (JSON + JSONL). The rendering targets are CLI (required) and HTML-static (queued, §13). The operator decides:

- Whether HTML is a flat static file emitted by the same renderer that emits CLI text;
- Whether HTML is a tiny Python web server (Flask, Bottle) or a static-site generator;
- Whether the CLI uses Python's `argparse` + plain text or a TUI library;
- Whether the rendering layer is one binary or two (one CLI, one HTML).

The spec is invariant under any of these choices. The constraint is the LoC budget (§12) and the schema-to-surface mapping (§4) — both stack-independent.

---

## §2 Screen Inventory

This spec proposes **7 screens** as the V1 primary inventory, matching C §C5.3 user-visible-journey count and synthesis §2.1's "either 7 or 8 is doctrinally defensible." The 8-screen variant (per B §B3.4) is documented as an alternative at §2.9.

Per C §C5.3, the 7-screen inventory compresses three internal procedure adjacencies:
- Step 7-A (BRE outside-frame trajectories) + Step 7-B (frame_validator cross-check) → one screen (the cross-check is an anti-monoculture defence; the operator does not need two screens but does need to see whether the cross-check passed).
- Step 7 + Step 8 (stage-gated roadmap) co-located on the same screen (continuation_gates are properties of trajectories).
- Step 1 (verdict) + Step 3 (assumptions surfaced) co-located on the same screen (both are frame_validator outputs, Step 1 verdict and Step 3 enriched-assumption list).

Step 10 (operative/theoretical) is its own screen, conditional on the G0 resolution (§9): under Position A it renders the absence-of-Step-10 honestly; under Position B it renders the populated Step 10 output.

Step 11 (MemoryLogger content) is NOT a screen in V1 (per C §C5.3 — "memory events are persistence-layer artefacts; V1 surfacing would be over-ceremonialization"). MemoryLogger JSONL trail is rendered on Screen 7 (closure) as a compact event list.

### §2.1 Screen 1 — Case Header & Submit

- **Underlying step(s):** Step 0 (input frame ingestion; external; operator authors). Pre-procedure surface.
- **Schema source:** `INPUT_FRAME_SCHEMA` (per `schemas/__init__.py`). The frame includes `id`, `text`, `locked_at_iso`, `doctrinal_scope_tag`, `companion_case`.
- **Operator action affordance:** READ-ONLY display of the locked input frame + a single "Run" affordance (CLI: command invocation; HTML: button that triggers the same back-end runner). After submission, the screen is frozen; no edit, no re-frame.
- **Refuse-mode rendering:** N/A (this screen is pre-procedure). After the run completes with exit_code=20, this screen displays the locked frame alongside the exit_code and the link to Screen 6 (Governance Verdict).
- **Anti-chatbot stance:** the case is submitted as a structured `InputFrame`, NOT as a prose question. The Submit affordance receives JSON or its CLI argument equivalent, never a conversational message.

### §2.2 Screen 2 — Frame Verdict & Surfaced Assumptions

- **Underlying step(s):** Step 1 (frame_validator initial validation) + Step 3 (frame_validator assumption surfacing). Per `frame_validator.py`.
- **Schema source:** `STEP_1_OUTPUT_SCHEMA` + `STEP_3_OUTPUT_SCHEMA` (per schemas dict). Step 1: `{verdict ∈ {valid, invalid, needs_decomposition}, reasons?}`. Step 3: `{assumptions: [string, ...]}` with `minItems=2`.
- **Operator action affordance:** READ-ONLY. The verdict is the load-bearing claim; the assumptions are the surfaced substance the operator must engage with.
- **Refuse-mode rendering:** N/A at this step (refuse is Step 9). Step 1's `invalid` verdict would halt at Step 1 with exit_code=10 (per orchestration_runner); the screen renders the verdict + reasons. `needs_decomposition` is a frame-shape verdict, NOT a final refusal.
- **Naming discipline:** the screen name "Frame Verdict" honors B §B3.2(a) rename ("Map" → "Axis Decomposition" goes to Screen 3; this screen is about the FRAME, not the map).
- **Linguistic discipline:** arbitration verbs only (surface, decompose, refuse). No "we learned that" or "you should understand that" copy. (C §C7.8 audit.)

### §2.3 Screen 3 — Axis Decomposition & Multi-Scale Relations

- **Underlying step(s):** Step 2 (object_decomposer 2-axis decomposition) + Step 6 (object_decomposer multi-scale relations).
- **Schema source:** `STEP_2_OUTPUT_SCHEMA` (axes ≥2, families ≥2 per axis per semantic post-validation in `object_decomposer.py`) + `STEP_6_OUTPUT_SCHEMA` (scales ≥2 + cross-scale relations).
- **Operator action affordance:** READ-ONLY. The decomposition IS the engagement substrate — per B §B2.2, the axis rendering is "the most direct rendering of Article III + Article IV" and "without this rendering, the operator sees only JSON; with it, the operator sees what the procedure refused to collapse."
- **Refuse-mode rendering:** N/A at this step (Step 2 + Step 6 succeed before Step 9 governance). The screen renders the decomposition regardless of downstream verdict — refusal-at-Step-9 does NOT erase the work done at Steps 2 + 6.
- **Rendering treatment:** flat tabular for V1 (axes × families table); decision-map graphical rendering is a SUPPORTING affordance per B §B1.6 + C §C3.2; deferred to V2 if needed. V1 ships the flat representation honestly; visualisation does not earn its way in at V1 (C §C7.6 over-visualisation early-warning).
- **Internal procedure compression note:** the operator-visible surface is "Axis Decomposition & Multi-Scale Relations"; the internal procedure runs Step 2 and Step 6 separately (separated by Step 4 + Step 5 in execution order). The screen presents both as a single conceptual surface because both are object_decomposer outputs and both are decomposition substrate.

### §2.4 Screen 4 — Hypotheses & Failure Conditions

- **Underlying step(s):** Step 4 (hypothesis_validator distinguishing_predictions) + Step 5 (hypothesis_validator fails_if).
- **Schema source:** `STEP_4_OUTPUT_SCHEMA` (hypotheses each carry `distinguishing_prediction`; schema-required per `hypothesis_validator.py` to prevent hypothesis-as-concern drift) + `STEP_5_OUTPUT_SCHEMA` (each hypothesis carries `fails_if` refutation condition).
- **Operator action affordance:** READ-ONLY.
- **Refuse-mode rendering:** N/A at this step. The hypothesis set is rendered regardless of Step 9 verdict; refuse-at-Step-9 does not invalidate the hypotheses, it adjudicates the bundle.
- **Critical UI commitment per C §C3.5:** "schema-equality of distinguishing_prediction + fails_if must be UI-equality." Hiding `fails_if` behind a "details" click would be doctrine-violating; Article I is operationalised by making refutation conditions visible at equal weight to predictions.
- **Rendering treatment:** per-hypothesis card or row; `distinguishing_prediction` and `fails_if` rendered side-by-side, not stacked-with-collapse.

### §2.5 Screen 5 — Outside-Frame Trajectories & Stage-Gated Roadmap

- **Underlying step(s):** Step 7-modeA (branching_roadmap_engine outside-frame trajectories) + Step 7-modeB (frame_validator cross-check feedback) + Step 8 (branching_roadmap_engine stage-gated roadmap with `continuation_gates` per stage).
- **Schema source:** `STEP_7_OUTPUT_SCHEMA` (trajectories with `outside-original-frame` tag per scaffold §8.10) + `STEP_8_OUTPUT_SCHEMA` (stages with continuation_gates per stage, ≥1 each).
- **Operator action affordance:** READ-ONLY.
- **Refuse-mode rendering:** N/A at this step. Trajectories and roadmap are rendered regardless of Step 9 verdict.
- **Cross-check rendering:** the Step 7-B cross-check status is a single status indicator on this screen — "frame_validator cross-check: passed" (per C §C5.3, the operator needs to see the cross-check status without seeing two separate screens).
- **Naming discipline:** per B §B3.2(b) rename ("Trajectories" → "Outside-Frame Alternatives"); the screen name surfaces that these are alternatives the original frame did NOT propose. This expresses Article II (frame humility) at the user surface.
- **Rendering treatment:** trajectory list (T1, T2, T3, T4 per alpha-case shape); stage-gated roadmap as a per-stage list with continuation_gates as text per stage. No animated tree; no "explore" affordance; static rendering only (C §C3.6 risk: animated motion = engagement-theater).

### §2.6 Screen 6 — Governance Verdict

- **Underlying step(s):** Step 9 (governance_kernel verdict + confidence_qualifier + unresolved_uncertainty_sources).
- **Schema source:** `STEP_9_OUTPUT_SCHEMA` with closed-set `verdict ∈ {constrain, refuse, explicitly_abstain}` (CE: `_VERDICT_VOCAB` in `governance_kernel.py` line 65) + `confidence` (free-text qualifier tied to ≥1 named source) + `unresolved_uncertainty_sources` with `minItems=1`.
- **Operator action affordance:** READ-ONLY. Per B §B4.1 and C §C3.3, the verdict gets FULL PROMINENCE on its own screen.
- **Refuse-mode rendering:** this screen IS the refuse-mode primary surface. When verdict=refuse (CE: all 3 alpha cases), the screen renders:
  - The verdict word ("refuse") with no apology, no softening adjective, no "however" clause.
  - The `confidence` qualifier displayed as free-text NOT as a numeric percentage. NEVER computed as confidence percent (would be Article III violation per §7 of this spec, anchored to C §C7.4).
  - The full `unresolved_uncertainty_sources` list, each source rendered at equal weight, NOT hidden behind "details", per C §C7.2.
  - A refuse-explainer copy block (§8) anchored to Article V, stating that refuse is the architecture's correct response, not an error.
- **Naming discipline:** per B §B3.3(a) rename ("decision pathways" was actually Step 9 governance, not pathway-routing; "Governance Verdict" is the honest name).
- **What this screen does NOT render:**
  - No "advice" framing (per task brief §6).
  - No LLM-prose summarization of the verdict (per task brief §6; B §B-non-recommendations 4; C §C7.8).
  - No "retry with different frame" button (per §1.2 and B §B3.6).
  - No engagement metric (no "this verdict is X% confident"; no "this case has Y points of uncertainty"; these would be Article I violations per §10).

### §2.7 Screen 7 — Closure (Operative/Theoretical Split + MemoryLogger Trail)

- **Underlying step(s):** Step 10 (operative_truth_separator) + Step 11 (memory_logger persistence). G0-dependent (§9).
- **Schema source:** `STEP_10_OUTPUT_SCHEMA` (operative-list + theoretical-list + optional absence_log) + `MEMORY_LOGGER_EVENT_SCHEMA` (closed-set `event_types`; closed-set `change_types`; append-only JSONL).
- **Operator action affordance:** READ-ONLY.
- **Refuse-mode rendering:** depends on G0 resolution.
  - **Under Position A (status quo; runner halts at Step 9 on refuse):** Step 10 fixtures EXIST but were NOT executed (CE: alpha replay §case_01.4 missing-behaviors; `operative_truth_separator.py` 207 LoC implemented; runner halts at Step 9). Screen 7 renders:
    - The MemoryLogger JSONL trail (CE: 14 events per case in alpha — 1 open + 9 step_committed + 1 step_7_modeB + 1 refutation + 1 close + 1 bookkeeping).
    - An honest "Step 10 not executed under refuse-halt; this case closed at Step 9 with refutation event" indicator.
    - The `refutation` event from the JSONL trail rendered as the closure record.
  - **Under Position B (runner continues Step 10 + Step 11 on refuse):** Screen 7 renders the populated Step 10 output (operative-list = "refuse the bundle"; theoretical-list = uncertainty sources from Step 9; optional absence_log) + the MemoryLogger trail INCLUDING the Step 11 capacity_change entries (closed-set per `_VALID_CHANGE_TYPES` in memory_logger.py: `arbitration_shortcut_added`, `framework_candidate_emerged`, `composition_path_discovered`, `pattern_recognition_added`, `judgment_act_logged`).
- **Naming discipline:** per B §B3.3 corrective rename ("Governance review" inverted what was actually happening; Step 10 is the actionable/theoretical split; this screen surfaces the closure honestly).
- **What this screen does NOT render:**
  - No cross-case observability (V2 scope).
  - No "pattern recognized" framing as validation; if any pattern is engaged at closure (Position B + future cases), it is rendered as "shape recognized; INVITATION TO TEST" per B §B4.3 + C §C7.4.
  - No knowledge-base / accumulated-wisdom framing (B §B-non-recommendations 11).

### §2.8 Cross-screen artifacts (operator-mode debug, NOT primary surface)

(CE) The alpha produces a `RunReport` object with `exit_code` + per-step envelopes + timestamps. The MemoryLogger JSONL trail is the second persistent artefact. The 11-step internal procedure is broader than the 7 user-visible screens.

Operator-mode debug surface (NOT a screen; accessible via CLI flag or HTML query parameter):
- Per-component LLM-call counts.
- Per-component LoC / dependency graph (B §B2.3 SUPPORTING).
- Runner halt-code mapping (10 / 20 / 30).
- Schema versions, fixture-mode flag, cost-cap parameter.
- Full RunReport JSON dump.

These are HIDDEN from the primary 7-screen flow per B §B4.1 ("what stays INTERNAL"). They are inspectable on demand for debugging without being foregrounded.

### §2.9 Alternative 8-screen inventory (per B §B3.4)

If the operator selects the 8-stage variant at §13 OD-V1-1, Screen 5 splits into:
- Screen 5a — Outside-Frame Alternatives (Step 7-A + Step 7-B cross-check)
- Screen 5b — Roadmap with Gates (Step 8)

The other 6 screens are unchanged. The trade-off:
- 7-screen: tighter operator journey; trajectories and roadmap co-located; fewer transitions.
- 8-screen: each procedural step surfaced individually; better mapping to internal procedure; minor extra transition cost.

This spec recommends 7 for V1 (closer to operator-engagement-per-screen optimization per C §C7.1 information-overload prevention) but the choice is doctrinally neutral and queued for operator decision.

---

## §3 Data Flow Map

This section traces the path from operator input through procedure execution to per-screen rendering. There are no new files written by V1; the rendering layer reads existing artefacts.

### §3.1 The four artefact families V1 consumes

Per C §C7.7, ELIF currently produces three artefact families (structured-output JSONs + RunReport + MemoryLogger JSONL). V1 adds a fourth: the rendered text/HTML translation. C §C7.7 explicitly notes that "rendered HTML/text is a translation, not a fourth family" — meaning V1's rendering layer is NOT a new artefact family; it is a translation of the existing three.

The three substrate artefact families V1 reads:

1. **Per-step structured-output JSONs.** One file per executed step per case. Naming: `step_NN__case_XX.json` (offline fixture convention; live mode produces equivalent in-memory or on-disk shape). Each JSON validates against the corresponding `STEP_N_OUTPUT_SCHEMA` in `src/elif_v0_1/schemas/__init__.py`.
2. **MemoryLogger JSONL trail.** One JSONL file per case at `<base_persistence_dir>/<case_id>/article_vii_tracking.jsonl` (per `memory_logger.py` `_EVENTS_FILENAME`). Append-only. Closed-set `event_types`.
3. **RunReport.** A structured object (in alpha: serializable Python dict) carrying `exit_code` + per-step envelopes + timestamps + run metadata. Per CE, alpha case_01 produces `exit_code=20` matching the refuse-verdict.

### §3.2 Operator input frame → procedure execution

Pre-existing flow (unchanged by V1):

1. Operator authors an `InputFrame` JSON satisfying `INPUT_FRAME_SCHEMA` (`id`, `text`, `locked_at_iso`, `doctrinal_scope_tag`, `companion_case`).
2. Operator invokes the existing CLI (`src/elif_v0_1/cli.py`) or replay harness (`src/elif_v0_1/replay/`), supplying `--case-id` + `--mode {offline,live}` + budget cap.
3. `orchestration_runner.py` executes Steps 1-9 sequentially, gated by data dependencies. Each step's output is validated against `STEP_N_OUTPUT_SCHEMA` and persisted (offline: fixture lookup; live: API call + persistence).
4. At Step 9, runner reads the verdict. Under Position A: halts on `refuse` with exit_code=20; Steps 10-11 not invoked. Under Position B: continues Step 10 + Step 11 on refuse path, emitting closure-record content.
5. MemoryLogger writes events at each step's commit-time (`open`, `step_committed`, `refutation` if applicable, `close`) per `_VALID_EVENT_TYPES`.

V1 does NOT modify any of this. V1 begins at step 6 of this flow:

6. **V1 rendering layer reads** the existing step JSONs + JSONL trail + RunReport, transforms them to text or HTML per the screen inventory, and presents them to the operator.

### §3.3 Per-screen JSON path consumption

The V1 rendering layer is a deterministic transformation from JSON paths to screen content. For each screen, the exact JSON paths consumed:

| Screen | Source artefact | JSON paths consumed |
|---|---|---|
| 1. Case Header & Submit | InputFrame JSON | `$.id`, `$.text`, `$.locked_at_iso`, `$.doctrinal_scope_tag`, `$.companion_case` |
| 2. Frame Verdict & Assumptions | `step_01__case_XX.json` + `step_03__case_XX.json` | step_1: `$.verdict`, `$.reasons[]`; step_3: `$.assumptions[]` |
| 3. Axis Decomposition & Multi-Scale | `step_02__case_XX.json` + `step_06__case_XX.json` | step_2: `$.axes[]`, `$.axes[].name`, `$.axes[].families[]`; step_6: `$.scales[]`, `$.cross_scale_relations[]` |
| 4. Hypotheses & Failure Conditions | `step_04__case_XX.json` + `step_05__case_XX.json` | step_4: `$.hypotheses[]`, `$.hypotheses[].statement`, `$.hypotheses[].distinguishing_prediction`; step_5: `$.hypotheses[].fails_if` (merged by hypothesis_id) |
| 5. Outside-Frame Trajectories & Roadmap | `step_07__case_XX.json` + `step_08__case_XX.json` + `step_07_modeB__case_XX.json` (if separate file) | step_7: `$.trajectories[]`, `$.trajectories[].tag` (filter for `outside-original-frame`); step_8: `$.stages[]`, `$.stages[].continuation_gates[]`; step_7_modeB: `$.cross_check_status` |
| 6. Governance Verdict | `step_09__case_XX.json` | `$.verdict`, `$.verdict_detail?`, `$.confidence`, `$.unresolved_uncertainty_sources[]` |
| 7. Closure | `step_10__case_XX.json` (if executed) + `article_vii_tracking.jsonl` + RunReport | step_10 (if Position B): `$.operative[]`, `$.theoretical[]`, `$.absence_log?`; JSONL: filter `event_type ∈ {open, close, refutation, capacity_change}`; RunReport: `$.exit_code`, `$.case_id`, `$.run_id` |

(CE) The JSON paths above are anchored to schema definitions in `src/elif_v0_1/schemas/__init__.py` and to alpha-case fixture shapes (`step_NN__case_XX.json` files in `src/elif_v0_1/offline_fixtures/`). The renderer does not introduce new fields or new schemas.

### §3.4 No new schemas

V1 introduces zero new schemas. The rendering layer is a read-only translation. If a field exists in v0.4.0 schemas, V1 may render it. If a field does not exist, V1 may NOT invent it (no derived metrics, no synthesized fields).

### §3.5 Refuse-mode data flow

Under Position A (CE: alpha behavior), the data flow stops at Step 9. Screens 1-6 render their corresponding step JSONs; Screen 7 renders only the MemoryLogger trail (open + step_committed × 9 + step_7_modeB + refutation + close + bookkeeping) and the RunReport (exit_code=20). The Step 10 fixture file MAY exist on disk (CE: it does in `src/elif_v0_1/offline_fixtures/`) but the V1 renderer MUST NOT load it if the runner did not execute Step 10 — that would be reading fixture data as if it were live procedure output, an Article III violation. V1 reads only what the runner actually produced for that run.

Under Position B (PF), the data flow continues through Step 10 + Step 11 even on refuse; Screen 7 renders the full Step 10 output + the expanded MemoryLogger trail including capacity_change entries.

### §3.6 Live-mode vs offline-mode invariance

The V1 surface does not branch on mode. Both modes produce the same JSON shapes (live mode = LLM API output validated against the same `STEP_N_OUTPUT_SCHEMA`; offline mode = fixture file loaded by the same `complete_structured` path in `llm_adapter.py`). The mode is metadata visible on Screen 1 + the operator-debug surface; the per-screen rendering is identical.

---

## §4 Schema-to-Surface Mapping

Per the task brief §4, this table maps every schema field to its rendering. Columns: `schema_field` / `source_step` / `screen_name` / `rendering_treatment` / `refuse_mode_treatment`. If a field has no screen, an explicit justification is given.

Schemas referenced (per `src/elif_v0_1/schemas/__init__.py`):
- `INPUT_FRAME_SCHEMA`
- `PROCEDURE_STEP_OUTPUT_SCHEMA` (envelope)
- `STEP_1` through `STEP_11` per-step schemas
- `ARTICLE_VII_TRACKING_SCHEMA`
- `MEMORY_LOGGER_EVENT_SCHEMA`
- `MEMORY_LOGGER_CORRECTION_SCHEMA`

### §4.1 InputFrame fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `id` | Step 0 (frame) | Screen 1 | header label, monospace | unchanged |
| `text` | Step 0 | Screen 1 | full text block, read-only | unchanged |
| `locked_at_iso` | Step 0 | Screen 1 | timestamp display | unchanged |
| `doctrinal_scope_tag` | Step 0 | Screen 1 | tag label (e.g., "scientific-evidential ambiguity"; "Cluster A") | unchanged |
| `companion_case` | Step 0 | Screen 1 | reference line, read-only | unchanged |

### §4.2 Step 1 (frame_validator initial verdict) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `verdict` | Step 1 | Screen 2 | label rendered with closed-set vocab visible (`valid` / `invalid` / `needs_decomposition`); no synonyms | if `needs_decomposition`: rendered as load-bearing engagement, NOT a soft failure |
| `reasons` (if present) | Step 1 | Screen 2 | bulleted text | unchanged |

### §4.3 Step 2 (object_decomposer 2-axis) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `axes[]` | Step 2 | Screen 3 | tabular per axis | unchanged |
| `axes[].name` | Step 2 | Screen 3 | axis header | unchanged |
| `axes[].families[]` | Step 2 | Screen 3 | family list per axis (≥2 per axis enforced by semantic post-validation in `object_decomposer.py`) | unchanged |

### §4.4 Step 3 (frame_validator assumption surfacing) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `assumptions[]` | Step 3 | Screen 2 | bulleted list; full text per assumption; no truncation | unchanged |

### §4.5 Step 4 (hypothesis_validator emission) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `hypotheses[]` | Step 4 | Screen 4 | card per hypothesis | unchanged |
| `hypotheses[].statement` | Step 4 | Screen 4 | hypothesis text | unchanged |
| `hypotheses[].distinguishing_prediction` | Step 4 | Screen 4 | rendered with EQUAL VISUAL WEIGHT to `fails_if` per C §C3.5 | unchanged |

### §4.6 Step 5 (hypothesis_validator fails_if) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `hypotheses[].fails_if` | Step 5 | Screen 4 | rendered side-by-side with `distinguishing_prediction` on the same per-hypothesis card | unchanged |

### §4.7 Step 6 (object_decomposer multi-scale) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `scales[]` | Step 6 | Screen 3 | flat list of scales (≥2) | unchanged |
| `cross_scale_relations[]` | Step 6 | Screen 3 | flat list; text per relation | unchanged |

### §4.8 Step 7 (branching_roadmap_engine outside-frame trajectories + frame_validator cross-check) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `trajectories[]` | Step 7-A | Screen 5 | list (T1-T4 typical) | unchanged |
| `trajectories[].tag` | Step 7-A | Screen 5 | tag label; filter for `outside-original-frame` per scaffold §8.10 | unchanged |
| `trajectories[].description` | Step 7-A | Screen 5 | text | unchanged |
| `cross_check_status` | Step 7-B | Screen 5 | single status indicator ("frame_validator cross-check: passed/failed") | unchanged |

### §4.9 Step 8 (branching_roadmap_engine stage-gated roadmap) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `stages[]` | Step 8 | Screen 5 | per-stage block | unchanged |
| `stages[].name` | Step 8 | Screen 5 | stage header | unchanged |
| `stages[].continuation_gates[]` | Step 8 | Screen 5 | gates rendered as text per stage (≥1 per stage required by schema) | unchanged |

### §4.10 Step 9 (governance_kernel verdict + confidence + uncertainty) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `verdict` | Step 9 | Screen 6 | the LOAD-BEARING display; closed-set vocab visible (`constrain` / `refuse` / `explicitly_abstain`); no synonyms; full prominence | if `refuse`: refuse-explainer copy block (§8) appears below verdict |
| `verdict_detail` (optional) | Step 9 | Screen 6 | sub-text below verdict | unchanged |
| `confidence` | Step 9 | Screen 6 | free-text qualifier as-is; NEVER converted to numeric percent; NEVER visualised as a confidence bar | unchanged |
| `unresolved_uncertainty_sources[]` | Step 9 | Screen 6 | bulleted list, FULL TEXT per source, `minItems=1` enforced; cannot be collapsed behind "details" click per C §C7.2 | rendered at full prominence; the uncertainty sources are the actionable substance under refuse |

### §4.11 Step 10 (operative_truth_separator) fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `operative[]` | Step 10 | Screen 7 | bulleted list ("act on now") | Position A: NOT rendered (Step 10 not executed; honest absence indicator); Position B: rendered with "refuse the bundle" as the operative item |
| `theoretical[]` | Step 10 | Screen 7 | bulleted list ("real but not actionable") | Position A: NOT rendered; Position B: rendered with uncertainty sources from Step 9 |
| `absence_log` (optional) | Step 10 | Screen 7 | text block; if present, surfaced | Position A: N/A; Position B: rendered |

### §4.12 Step 11 + MemoryLogger event fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `event_type` (closed-set) | Step 11 / MemoryLogger | Screen 7 | per-event line in compact chronological list; closed-set vocab visible (`open`, `close`, `step_committed`, `frame_locked`, `verdict_emitted`, `uncertainty_recorded`, `reuse_detected`, `pattern_recognized`, `refutation`, `capacity_change`, `correction`) | Position A: rendered (14 events: open + step_committed × 9 + step_7_modeB + refutation + close + bookkeeping); Position B: rendered with additional capacity_change events |
| `committed_at_iso` | MemoryLogger | Screen 7 | timestamp per event | unchanged |
| `event_id` | MemoryLogger | (debug-mode only) | hidden in primary; visible in debug | unchanged |
| `case_id` | MemoryLogger | Screen 1 + Screen 7 (debug) | header only on Screen 1; per-event omitted from primary | unchanged |
| `payload` (per event_type) | MemoryLogger | Screen 7 | type-dependent: open/close = brief; step_committed = step_id; refutation = brief; capacity_change = `change_type` (closed-set) + description | unchanged |
| `capacity_change.change_type` (closed-set) | Step 11 / MemoryLogger | Screen 7 | closed-set vocab visible (`arbitration_shortcut_added`, `framework_candidate_emerged`, `composition_path_discovered`, `pattern_recognition_added`, `judgment_act_logged`) | Position A: NOT rendered (not emitted under refuse-halt); Position B: rendered as INVITATION TO TEST framing per C §C7.4, NOT as validation |
| `correction` event (via `emit_correction`) | MemoryLogger | Screen 7 (debug-mode supplement) | append-only correction events surfaced as supersede-events; original never mutated (Article III) | unchanged |

### §4.13 ARTICLE_VII_TRACKING fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| (per shape of `results/case_*/article_vii_tracking.json`) | MemoryLogger | OMITTED from V1 primary surface | substrate-level artefact; not load-bearing for per-case rendering at V1; V2 cross-case dashboard will surface aggregations | unchanged |

**Justification for omission:** Article VII tracking is a cross-case observability substrate. V1 is per-case only. Surfacing Article VII aggregations at V1 would import V2 scope (synthesis §4.6 Phase 6) and violate the §1.1 scope discipline. The fields exist in v0.4.0 schemas and are populated by MemoryLogger; V1 simply does not render them. V2 (separate spec) will.

### §4.14 RunReport fields

| schema_field | source_step | screen_name | rendering_treatment | refuse_mode_treatment |
|---|---|---|---|---|
| `exit_code` | runner | Screen 1 (post-run) + Screen 7 | numeric + label ("20: GovernanceRefuseError") | rendered with REFUSE label; explicitly NOT framed as error |
| `case_id` | runner | Screen 1 | header | unchanged |
| `run_id` | runner | (debug-mode only) | hidden in primary | unchanged |
| `mode` | runner | Screen 1 (badge: "offline" / "live") | small label | unchanged |
| per-step envelopes | runner | distributed across Screens 2-6 | already rendered per step | unchanged |
| timestamps | runner | (debug-mode only) | hidden in primary | unchanged |

### §4.15 Schema fields with no screen

| schema_field | source_step | justification for omission |
|---|---|---|
| `PROCEDURE_STEP_OUTPUT_SCHEMA` envelope wrapper fields (e.g., `step_id`, `committed_at_iso`, `schema_version`) | all steps | metadata; rendered in debug-mode only; not load-bearing for operator engagement with substrate |
| `MEMORY_LOGGER_CORRECTION_SCHEMA` extensions | MemoryLogger | correction discipline is structural integrity not operator-engagement substrate; debug-mode only |
| ARTICLE_VII fields (all) | MemoryLogger | V2 cross-case scope per §4.13 |
| Live-mode API tool-call structured-output details | LLM adapter | hidden per B §B4.2 ("the Anthropic API tool-call structured-output details") |
| Prompt template content | components | NEVER surfaced (B §B-non-recommendations 8: no prompt-engineering surface) |

---

## §5 Operator Journey (Question → Verdict → Closure)

This section names the time-ordered stages, marks which are auto-advanced vs operator-paused-on, and surfaces refuse-stage explicitly. Per the task brief §5, the operator should never be surprised by exit_code 20.

### §5.1 Stage sequence

| # | Stage name | Auto / pause | What happens | What the operator sees |
|---|---|---|---|---|
| 1 | **Author** | OPERATOR-PAUSED (pre-run) | Operator authors `InputFrame` JSON (external to V1; via case file or CLI args) | Nothing yet — this is pre-V1 |
| 2 | **Submit** | OPERATOR-ADVANCED | Operator invokes runner (CLI command or HTML button); V1 displays Screen 1 | Screen 1 with locked frame + "Run" affordance |
| 3 | **Procedure executes** | AUTO-ADVANCED | Runner executes Steps 1-9 sequentially; offline: sub-second; live: 20-50s end-to-end (CE per cost_complexity_report §1) | CLI: simple "running…" indicator with per-step progress optional; HTML: same; NO chatbot-style streaming |
| 4 | **Frame Verdict** | AUTO-ADVANCED to Screen 2 | Step 1 + Step 3 outputs available | Screen 2 |
| 5 | **Decomposition** | AUTO-ADVANCED to Screen 3 | Steps 2 + 6 outputs available | Screen 3 |
| 6 | **Hypotheses** | AUTO-ADVANCED to Screen 4 | Steps 4 + 5 outputs available | Screen 4 |
| 7 | **Trajectories & Roadmap** | AUTO-ADVANCED to Screen 5 | Steps 7-A + 7-B + 8 outputs available | Screen 5 |
| 8 | **GOVERNANCE VERDICT (refuse stage explicit)** | AUTO-ADVANCED to Screen 6, OPERATOR-PAUSED here | Step 9 verdict emitted; runner halts here under Position A; under Position B continues internally to Steps 10-11 | Screen 6 with verdict + confidence + uncertainty sources; if `refuse`, refuse-explainer copy block visible |
| 9 | **Closure** | AUTO-ADVANCED to Screen 7 (after step 8 verdict rendered) | Step 10 (Position B only) + MemoryLogger trail finalized | Screen 7 with operative/theoretical split (if Position B) or MemoryLogger refutation event (if Position A) |
| 10 | **Exit** | OPERATOR-ADVANCED | Operator leaves the room | Optional summary line: "Case <id> closed at exit_code <code>" |

### §5.2 Why all rendering stages are AUTO-ADVANCED

The case is the unit of work, not the screen (B §B1.7). The operator does not need to click through screens to advance the procedure — the procedure has already executed. The rendering layer presents all screens in a fixed flow that the operator can scroll/page through. CLI: print all screens in order; HTML: scroll page or paginate.

This honors the pausability test (§11): the operator may close the laptop after Screen 3 and re-enter at Screen 3, because the underlying JSON files are persistent and the rendering is stateless.

### §5.3 The refuse stage is named explicitly

Per task brief §5: "Surface refuse-stage explicitly (the operator should never be surprised by exit_code 20)."

At stage 8 (Screen 6), the operator is OPERATOR-PAUSED. The screen heading is "Governance Verdict" (not "Result" or "Decision"). If the verdict is `refuse`, the refuse-explainer copy block (§8) is rendered IMMEDIATELY BELOW the verdict, not behind a click. The operator cannot reach Screen 7 without having seen the explicit refuse acknowledgment.

CE: all 3 alpha cases produce `refuse`. Under any V1 deployment using existing alpha cases, the refuse stage is the dominant operator experience. The journey must treat refuse as the load-bearing path, not the exception.

### §5.4 No re-execution loop

After Stage 10 (Exit), there is no "Run again" affordance. The case is closed. The operator authors a new case (Stage 1) for new work. (B §B3.6 + B §B-non-recommendations 8.)

### §5.5 No editing of upstream stages

Once the runner has produced Step N output, the operator cannot modify it through V1. No "re-run Step 4 with this hypothesis" affordance. The structured output is the deliverable; tampering with intermediate outputs would invalidate downstream and violate the schema-validation chain.

---

## §6 Governance Visibility

Per task brief §6: Step 9 verdict gets full prominence on its own screen. Confidence qualifier, uncertainty sources, refusal reasoning all visible. NO "advice" framing. NO LLM-prose summarization. Anti-chatbot stance is structural.

### §6.1 The Governance Verdict screen is structurally distinct

Screen 6 is the only screen whose primary surface is a single closed-set token. Screens 2-5 render structured decompositions; Screen 6 renders THE VERDICT. The visual hierarchy reflects this: the verdict gets the largest type (CLI: bold + uppercase; HTML: largest heading). The confidence qualifier and uncertainty sources are direct children of the verdict, NOT a sub-section.

### §6.2 Closed-set vocabulary visible

Per CE (`_VERDICT_VOCAB` in `governance_kernel.py` line 65), the closed set is `{constrain, refuse, explicitly_abstain}`. The verdict is rendered as the literal token from this set. No synonyms ("denied", "approved", "rejected", "decided"). No softening adjectives. The closed-set is itself a substrate commitment per CLAUDE.md closed-set discipline.

### §6.3 No "advice" framing

The verdict is NOT rendered as "We recommend you refuse" or "Our advice is to refuse" or "It seems the right call would be to refuse." These framings re-import LLM-as-assistant affordance (B §B1.1 chatbot framing as ACTIVELY COUNTERPRODUCTIVE). The verdict is rendered as the structural output of the governance_kernel: a closed-set token.

### §6.4 No LLM-prose summarization

The verdict is NOT preceded or followed by an LLM-generated prose summary of the case ("This case concerns electroculture pilot deployment across drought-prone regions for 5 years…"). The operator already knows the case (they authored it; they read the InputFrame on Screen 1). Summarization re-imports the chatbot/tutorial affordance Article III refuses.

### §6.5 Confidence qualifier rendered as free text, never as a number

Per CE (`STEP_9_OUTPUT_SCHEMA`), `confidence` is a free-text qualifier tied to ≥1 named uncertainty source. V1 renders it as the literal free-text the LLM emitted, validated against the schema. NEVER converted to a percent. NEVER rendered as a progress bar. NEVER aggregated into a "confidence score." Doing so would compute a numeric metric the substrate does not produce — an Article III violation (no self-validation) per §7 of this spec.

### §6.6 Uncertainty sources visible at full weight

`unresolved_uncertainty_sources` has `minItems=1` per schema. V1 renders every source as a full-text bullet, NOT collapsed behind a "details" or "expand" click. Per C §C7.2 early-warning signal: the schema-required `minItems=1` must be UI-required `minItems=1 visible`. If a single source is hidden, the surface has failed.

### §6.7 Refusal reasoning visible

The `confidence` text and the `unresolved_uncertainty_sources` list are the refusal reasoning. Under refuse, they are not subordinated — they ARE the substance of the verdict. The operator's actionable next-step is to engage with the uncertainty sources (per B §B3.6 — "the uncertainty sources surfaced as actionable next-steps, not as error messages").

### §6.8 Anti-chatbot stance is structural

This stance is enforced by:
- No conversational turn (Screen 6 is read-only after auto-advancement).
- No prose wrapper around the verdict.
- No "Why?" or "Tell me more" button (would invite a chatbot-like response).
- The closed-set vocabulary visible (the operator sees the token, not a paraphrase).
- The uncertainty sources visible at full weight (substantive engagement, not "AI explained it to me").

---

## §7 Uncertainty Visibility

Per task brief §7: unresolved uncertainty sources rendered honestly. Not minimized, not maximized, not interpreted. NEVER computed as confidence percent (would be Article III violation).

### §7.1 The schema requires minItems=1; V1 enforces UI-minItems=1-visible

Per `STEP_9_OUTPUT_SCHEMA`, `unresolved_uncertainty_sources` has `minItems=1`. If a Step 9 output passes schema validation, it has ≥1 source. V1 renders all sources visibly. There is no "hide low-priority sources" affordance. There is no "show top 3 sources" affordance. All sources are rendered, all at the same visual weight.

### §7.2 Not minimized

V1 does not summarize the uncertainty sources into a single number, label, or icon. Each source is rendered as the literal text the governance_kernel emitted, validated by schema. Each source is a substantive claim about what was not resolved; collapsing it into a metric would erase the substance.

### §7.3 Not maximized

V1 does not amplify the uncertainty visually. No flashing warnings, no red borders, no "WARNING: HIGH UNCERTAINTY" labels. The uncertainty sources are rendered at the same visual weight as other text content on Screen 6.

### §7.4 Not interpreted

V1 does not add prose interpretation around the uncertainty sources. No "this means…" framing. No "the model is unsure because…" framing. The source text speaks for itself; the rendering layer does not gloss it.

### §7.5 Never computed as confidence percent

Per task brief §7 and C §C7.4: any numeric percent computed over uncertainty sources would be a meta-confidence claim the schema does not produce. Inventing such a number = the system claims confidence about its own uncertainty = Article III violation (no self-validation) at the rendering layer.

V1 renders the schema's `confidence` field as free text and the `unresolved_uncertainty_sources` list as full-text bullets. No derived metrics.

### §7.6 No "uncertainty score"

V1 does not render any composite metric over the uncertainty sources. Not a count of "5 unresolved sources" with implied weight. Not a "complexity score." Not a "judgment difficulty rating." None of these exist in the substrate; inventing them at the rendering layer is the canonical "rendering platform with arbitration backend" failure mode (C §C7.6).

### §7.7 No "resolve this uncertainty" affordance

Under V1, the operator cannot click a source and trigger a sub-procedure to "resolve" it. The uncertainty sources are the substance of the refusal verdict; "resolving" them would mean re-running the case with different inputs, which is the re-execution loop V1 forbids (B §B3.6).

The operator's next action upon engaging with the uncertainty sources is to author a NEW case (a different bundled question that decomposes the uncertainty into a structurally different frame). This is operator work; V1 does not automate it.

---

## §8 Refusal Visibility

Per task brief §8: exit_code 20 as the CORRECT verdict, not failure. Refusal copy that does not apologize, does not encourage retry, does not suggest "different framing might work." Anchored to Article V.

### §8.1 Refuse-explainer copy block (canonical V1 text)

On Screen 6, when verdict=refuse, the following copy block is rendered IMMEDIATELY BELOW the verdict, in the same visual section (not behind a click, not on a tooltip):

> **This verdict is the architecture's structural response under Article V (Refusal Capability).**
>
> The procedure decomposed the bundled question, surfaced assumptions, emitted hypotheses with distinguishing predictions and refutation conditions, generated outside-frame trajectories with a stage-gated roadmap, and arbitrated to a refuse verdict with the uncertainty sources surfaced above.
>
> exit_code=20 is the correct architectural response, not an error.

That is the entire copy block. It does not apologize. It does not say "we're sorry, please try again." It does not say "perhaps a different framing might work." It does not suggest the operator retry. It does not invite re-execution.

### §8.2 What the copy block does NOT contain

- No "we encountered an issue."
- No "ELIF was unable to."
- No "please consider rephrasing."
- No "try again with."
- No "based on what you provided, the system could not."
- No first-person agency framing ("I", "we", "the assistant").
- No appeal to fluency, helpfulness, or user satisfaction.

### §8.3 Article V anchor

The copy block cites Article V (Refusal Capability) by name. This is structural transparency: the operator knows the doctrinal source of the verdict and can verify it against the locked v0.4 constitutional layer. (CE: `elif_constitutional_layer.md` Article V; alpha runner halt at exit_code 20 per `orchestration_runner.py`.)

### §8.4 Refuse copy is the same across all refuse cases

V1 does NOT per-case customize the refuse-explainer copy. The same copy block renders for every refuse verdict. Per-case substance is in the `confidence` qualifier + `unresolved_uncertainty_sources` list, which the schema produces. The explainer is a constant; the substance is per-case.

### §8.5 No "next steps" prescription

The refuse-explainer does NOT prescribe what the operator should do next. It does not say "consider authoring a new case that…" or "the uncertainty around X suggests you investigate Y." The operator's next move is operator judgment; V1 does not adjudicate it. The uncertainty sources are the substance; the operator engages with them on their own time.

### §8.6 Refuse-explainer copy approval queued

The exact wording in §8.1 is THIS SPEC's proposal. Operator approval is queued at §13 OD-V1-3. Operator may revise wording; the structural commitments (no apology, no retry encouragement, no first-person, no fluency) are load-bearing and must hold under any wording.

---

## §9 Closure Stage (G0-dependent)

Per task brief §9: if Position A: closure = refutation event in MemoryLogger as audit record only. If Position B: closure = operative/theoretical separation + case_closed event. Write both. The spec accommodates either.

### §9.1 Closure under Position A (status quo)

(CE) Position A is the alpha-shipped runner behavior. exit_code=20 halts after Step 9 on refuse. Step 10 + Step 11 are NOT exercised. MemoryLogger writes:
- 1 `open` event at run start.
- 9 `step_committed` events (Steps 1-9, including the Step 7-modeB cross-check sub-event).
- 1 `refutation` event capturing the refuse-verdict (per `memory_logger.py` `_VALID_EVENT_TYPES`).
- 1 `close` event at run end.
- 1 bookkeeping event (per alpha replay report §case_01.6).

Total: 14 events per refuse-case.

**Screen 7 rendering under Position A:**
- Heading: "Case Closure"
- Status line: "Step 10 not executed under refuse-halt (Position A). Case closed via refutation event."
- MemoryLogger event list: all 14 events in chronological order. Closed-set `event_type` visible per event. `committed_at_iso` per event. Compact format.
- Refutation event highlighted as the closure record.
- No operative list. No theoretical list. No absence_log.

### §9.2 Closure under Position B (Step 10 + Step 11 run on refuse)

(PF) Under Position B, the runner continues Step 10 + Step 11 after refuse. (Schema validation already supports this; CE: `operative_truth_separator.py` 207 LoC implemented, fixtures validate.) Step 10 produces operative-list, theoretical-list, optional absence_log. Step 11 emits content events including `capacity_change` entries.

**Screen 7 rendering under Position B:**
- Heading: "Case Closure"
- Operative section: bulleted list rendering `step_10.operative[]`. For the alpha refuse-case shape: typically `["refuse the bundle"]` per the operator's framing.
- Theoretical section: bulleted list rendering `step_10.theoretical[]`. For the alpha refuse-case shape: typically the uncertainty sources from Step 9.
- Absence log (if present): rendered as text block.
- MemoryLogger event list: as in §9.1 PLUS the additional content events (`capacity_change` × N entries; `judgment_act` events if emitted; `pattern_recognized` events if emitted).
- Capacity-change entries render closed-set `change_type` (CE: `arbitration_shortcut_added`, `framework_candidate_emerged`, `composition_path_discovered`, `pattern_recognition_added`, `judgment_act_logged`).
- Pattern-recognition events render as INVITATION TO TEST framing per C §C7.4, NOT as validation.

### §9.3 Spec accommodates either resolution

The screen inventory (§2.7), the data flow (§3.5), and the schema-to-surface mapping (§4.11, §4.12) all branch on G0 resolution explicitly. V1 ships with both renderings available; the deployed renderer reads whether Step 10 fixtures were executed (Position B: present and executed) or were not executed (Position A: present on disk as fixtures but not loaded for this run).

### §9.4 V1 does NOT advocate Position A or B

Per synthesis §1.3, §2.3, §4.0, the G0 adjudication is the single most leverageful operator decision. The spec accommodates either resolution without advocating. The choice is upstream of V1 implementation (G0 must close before V1 ships per synthesis Phase 0 → Phase 1 → Phase 2 sequence) and is flagged at §13 as an upstream blocker.

### §9.5 No closure framing as "knowledge added"

Under Position B, even when capacity_change events fire and patterns are engaged, the closure rendering does NOT frame this as "ELIF now knows X" or "the system has learned Y" or "a pattern has been confirmed." Article VII forbids truth-accumulation framing (B §B-non-recommendations 11; C §C7.4). The closure rendering says:
- "Refutation event recorded" (Position A).
- "Operative list: refuse the bundle. Theoretical list: <uncertainty sources>. Pattern engagement events recorded: <list>." (Position B.)

Pattern engagement is rendered as event record, not as validation claim.

---

## §10 Linguistic Audit Substrate

Per task brief §10: Zero unhedged claim-language. Pedagogical-verb count < 10% of operator-facing copy verbs. Substrate: arbitration verbs (decompose, refute, arbitrate, refuse, surface), NOT pedagogical verbs (learn, understand, master).

### §10.1 The audit substrate

Per C §C7.4 early-warning signal: "≥0 occurrences of unhedged claim-language permitted in V1 copy; if even one slips in, the copy is failing." Per C §C7.8 second signal: "pedagogical verbs (learn / understand / master / remember) vs. arbitration verbs (decompose / refute / arbitrate / refuse / surface). If pedagogical verbs appear at >10% of total verb count in operator-facing copy, the framing has drifted."

This spec adopts both as V1 acceptance criteria.

### §10.2 Permitted arbitration verbs

Canonical V1 verb substrate (extensible only via operator approval + doctrine revision):
- **decompose** — Step 2 / Step 6 / object_decomposer action verb.
- **surface** — Step 3 / frame_validator action verb (surface assumptions).
- **emit** — component-action verb for structured outputs.
- **validate** — schema-validation verb; also Article-anchor (frame_validator).
- **arbitrate** — governance_kernel verdict-emission verb.
- **refuse** — Article V refusal-capability verb.
- **refute** — fails_if + refutation event verb.
- **constrain** — Step 9 closed-set verdict word.
- **abstain** — Step 9 closed-set verdict word.
- **commit** — step_committed event verb.
- **record** — MemoryLogger persistence verb.
- **engage** — operator-action verb ("engage with the decomposition").
- **trace** — arbitration-trace noun verb-form.

### §10.3 Forbidden pedagogical verbs

Hard prohibition (V1 copy MUST NOT contain these verbs in operator-facing surface text):
- learn / learns / learning
- understand / understands / understanding
- master / masters / mastery
- remember / remembers / memorize
- teach / teaches / teaching
- explain / explains / explainer (the WORD; the function of surfacing structure is fine but called "surface" not "explain")
- tutor / tutorial
- lesson / lessons
- study / studies (in pedagogical sense)
- "let's…" framing
- "you'll discover" framing
- "we'll explore together" framing

### §10.4 Forbidden unhedged claim language

Per C §C7.4: "any UI text that reads 'the answer is' or 'the right decision is' or 'based on prior patterns, this is' without explicit refutation framing is doctrine-violating."

Hard prohibition (V1 copy MUST NOT contain):
- "The answer is…"
- "The right decision is…"
- "Based on prior patterns, this is…"
- "The truth here is…"
- "What ELIF found is…" / "ELIF concludes…"
- "We've determined that…"
- "It's clear that…"
- "Obviously…"
- Any first-person plural ("we", "our", "us") attributing agency to ELIF.

### §10.5 Linguistic audit at V1 ship gate

Before V1 ships, an explicit linguistic audit of every piece of operator-facing copy is performed. The audit:
- Counts pedagogical verbs (target: 0; threshold: <10% of total verb count per C §C7.8).
- Counts unhedged claim phrases (target: 0; threshold: 0 per C §C7.4).
- Cross-checks every UI element against the substrate-anchor audit (per C §C7.5; §11 of this spec).

The audit deliverable is a per-screen linguistic compliance report. If any threshold is missed, V1 does not ship until copy is revised.

### §10.6 Closed-set vocabulary respected in copy

Where the procedure has closed-set vocabulary (`verdict ∈ {valid, invalid, needs_decomposition}` for Step 1; `verdict ∈ {constrain, refuse, explicitly_abstain}` for Step 9; `event_type ∈ _VALID_EVENT_TYPES`; `change_type ∈ _VALID_CHANGE_TYPES`), the V1 copy uses the literal closed-set token, not a paraphrase. The token is the substrate; paraphrasing would obscure the closed-set discipline.

---

## §11 Pausability Test

Per task brief §11: V1 must be a stateless read over append-only JSONL + step JSONs. No background process. Operator can pause for weeks and re-enter without state rebuild. Per audit B §B4.5.

### §11.1 V1 is a read over persistent JSON/JSONL

V1 reads:
- The `InputFrame` JSON (operator-authored, persistent).
- The `step_NN__case_XX.json` step output files (runner-emitted, persistent).
- The `article_vii_tracking.jsonl` MemoryLogger trail (runner-emitted, append-only).
- The RunReport (runner-emitted, persistent in alpha; may be serialized to JSON for V1 read).

All four are persistent files. V1 has no in-memory state that depends on a session, a connection, or a background process. The renderer can be invoked at any time against any persisted case and produce the same 7-screen output.

### §11.2 No background process

V1 does NOT run:
- A daemon to keep a UI fresh.
- A WebSocket connection for live updates.
- A polling loop for new MemoryLogger events.
- A scheduled task to "refresh" the laboratory (V2 scope anyway; not V1).
- A cache that expires.

The renderer is a pure function from `(case_id, persistence_dir, mode_flag)` to rendered output. Stateless. Idempotent.

### §11.3 Operator pauses for weeks; re-enters cleanly

Test scenario:
- Operator runs Case A on day 0. Renderer produces 7 screens. Operator reads through Screen 3, then closes the laptop.
- Operator returns on day 28. Re-invokes renderer for Case A. Same 7 screens produced. Operator continues at Screen 4.

This works because:
- The step JSONs are persistent files; they don't decay.
- The JSONL trail is persistent; append-only.
- The RunReport is persistent.
- The renderer is stateless; it reads files and produces output.

There is no "session" to expire, no "state" to rebuild.

### §11.4 Mid-case pausing during procedure execution

V1 does NOT support mid-case pausing during procedure execution (i.e., pausing while the runner is mid-way through Step 4). Procedure execution is sub-second in offline mode, ~20-50s live. The pausability test applies AFTER the procedure has produced its persistent outputs. (B §B4.5 PF projection for V2: "single case runs in ~20-50s live; the operator can pause between cases. Mid-case pausing requires a snapshot mechanism but is not load-bearing for V2.")

V1 inherits this: pausability is at the case-boundary level. Within a case execution, the operator waits for the runner to complete (it will complete quickly).

### §11.5 No "fresh state" required to re-enter

When the operator returns on day 28, no migration is needed. No "rebuild your view" step. No "the format has changed, please re-import." The persistent JSON/JSONL files are schema-pinned at v0.4.0; V1's renderer reads v0.4.0 schemas.

If schemas evolve in v0.5+, V1 reads v0.4.0 schemas; older case files render with v0.4.0 conventions. Forward-compat (v0.5 schemas) requires renderer update; backward-read (v0.4.0 cases) is preserved.

### §11.6 The pausability test is the V3 maturity test, applied preemptively at V1

Per B §B4.5: "the laboratory surface must be a stateless read over MemoryLogger JSONL, not a live-state system." This is named as the V3 architectural commitment; the spec adopts it for V1 to prevent any V1 design that would later require redesign at V2/V3 to meet pausability.

### §11.7 What violates pausability (V1 design restrictions)

Any of the following would violate pausability and is explicitly forbidden in V1:
- A V1 implementation that requires a running web server with in-memory cache.
- A V1 that fetches case data from an API the renderer manages.
- A V1 that maintains a "current case pointer" in operator session.
- A V1 that depends on a database connection (V1 reads files, not DB).
- A V1 that displays "stale" / "refresh" indicators on rendered output.
- A V1 that requires the procedure runner to be online when rendering.

A V1 deployment that uses an HTTP server may be transient (the server can start, render, exit, restart) but the server MAY NOT cache or maintain session state. Each render is independent of prior renders.

---

## §12 Rendering LoC Budget

Per task brief §12: ≤ 0.3 × substrate LoC (~2,533 component LoC × 0.3 ≈ 760 LoC ceiling for V1 rendering layer). Per C §C7.6.

### §12.1 The substrate LoC anchor

Per CE (alpha cost_complexity_report.md §1; `elif_v0_1_what_remains.md` §6):
- Components: 2,533 LoC (sum across 7 components).
- Runner: 506 LoC.
- LLM adapter + schemas + base + run_context: ~1,000 LoC.
- Total v0.1 alpha implementation: 5,129 LoC code + 3,295 LoC tests = 8,424 LoC.

Per C §C7.6: "rendering layer ≤ 0.3 × substrate LoC." The substrate anchor is the component LoC (the load-bearing substrate that produces the structured outputs V1 renders).

### §12.2 V1 LoC ceiling

`2,533 × 0.3 = 759.9` → V1 rendering layer is capped at **≤ 760 LoC** (rounded).

Per C §C6.1: "small. ~500–1,000 LoC for a text-renderer (CLI) and ~1,500–2,500 LoC for a minimal HTML view (web)." The 760-LoC ceiling is tighter than C §C6.1's upper bound for HTML; this spec adopts the tighter ceiling because §C7.6 is the load-bearing test.

Under the ceiling:
- CLI renderer only: target ~500 LoC. Comfortable margin.
- CLI + HTML static renderer (shared transformation logic): target ~700 LoC. Tight but achievable.
- CLI + HTML server-rendered: likely > 760 LoC. Forbidden without operator-approved budget revision.

### §12.3 Why CLI is required and HTML is optional in V1

CLI rendering fits the budget comfortably. HTML rendering risks blowing the budget. Per §1.1, CLI is required and HTML is optional, with operator decision at §13.

If the operator selects HTML, the spec requires HTML to share transformation logic with CLI (i.e., one renderer with two output formats), not a separate HTML stack. This shares the budget across two outputs.

### §12.4 What counts toward the budget

The budget covers:
- The renderer module (per-screen rendering functions).
- The CLI entrypoint (argument parsing, command dispatch).
- The data-flow layer (reads JSON/JSONL files; transforms to rendering data structures).
- The linguistic-substrate constants (verb whitelists, refuse-explainer copy, screen heading copy).
- HTML templates (if HTML is selected).

The budget does NOT cover:
- Test code (tests are not the rendering layer).
- Existing infrastructure (orchestration_runner, components, schemas, llm_adapter).
- Operator documentation / README.

### §12.5 Budget enforcement at V1 ship gate

Before V1 ships, an explicit LoC count is performed against the rendering module. If the count exceeds 760 LoC, V1 does not ship until the budget is met (by simplification, not by exception). The C §C7.6 early-warning signal: "if rendering LoC exceeds substrate LoC, the system has become a rendering platform with an arbitration backend." This is the doctrinal anchor.

### §12.6 Substrate growth shifts the budget

If v0.5+ grows component LoC beyond 2,533 (per constitutional compression at synthesis Phase 4, the trajectory is COMPRESSION not growth — so this is unlikely), the 0.3× ratio recalculates. If components shrink (per the constitutional compression direction), the V1 rendering budget shrinks proportionally.

### §12.7 Per-screen LoC sub-budget (advisory)

Indicative split (operator may revise):

| Screen | Indicative LoC ceiling |
|---|---|
| 1. Case Header & Submit | ~50 |
| 2. Frame Verdict & Assumptions | ~80 |
| 3. Axis Decomposition & Multi-Scale | ~100 |
| 4. Hypotheses & Failure Conditions | ~100 |
| 5. Outside-Frame Trajectories & Roadmap | ~120 |
| 6. Governance Verdict | ~100 |
| 7. Closure | ~120 |
| Shared (data-flow, CLI entry, copy constants) | ~90 |
| **Total** | **~760** |

This is advisory; the only hard ceiling is the total 760.

---

## §13 Operator Decisions Queued

This spec surfaces the following operator decisions. They are scoped, time-bound, and explicitly marked. None are resolved by this spec.

### §13.1 OD-V1-1 — 7 vs 8 user-visible stage choice

(B §B3.4 settles 8; C §C5.3 settles ~7; synthesis §2.1 defensible either way.)

- **Option 7 (this spec's default):** Screen 5 holds Outside-Frame Trajectories + Stage-Gated Roadmap together. Tighter journey.
- **Option 8:** Screen 5 splits into Screen 5a (Outside-Frame Alternatives) + Screen 5b (Roadmap with Gates).

Operator chooses. Either is doctrinally defensible.

### §13.2 OD-V1-2 — CLI-only vs CLI+HTML for V1

(C §C6.1 names both as in-scope at V1; this spec recommends CLI required, HTML optional based on LoC budget §12.)

- **Option CLI-only:** ~500 LoC ceiling. Comfortable. Operator inhabits a terminal.
- **Option CLI+HTML:** ~700-760 LoC ceiling. Tight. Operator can open a browser tab.

Operator chooses. If HTML, the spec requires shared transformation logic per §12.3.

### §13.3 OD-V1-3 — Refuse-explainer copy approval

(This spec proposes the copy block at §8.1; operator reviews and approves or revises.)

The structural commitments (no apology, no retry encouragement, no first-person, no fluency, Article V anchor) are load-bearing. The exact wording is queued for operator approval.

### §13.4 OD-V1-4 — G0 resolution (UPSTREAM BLOCKER)

(Synthesis §4.0 Phase 0 names G0 as the single blocking gate. This spec accommodates both Position A and Position B, but cannot ship until G0 is closed.)

- **Position A:** runner halts at Step 9 on refuse; Step 10/11 not exercised; Screen 7 renders refutation event only.
- **Position B:** runner continues Step 10/11 on refuse; Screen 7 renders operative/theoretical split + capacity_change events.

This is NOT a V1-internal decision; it is an upstream doctrinal adjudication that V1 inherits. V1 SPEC accommodates either; V1 SHIP requires G0 closed.

**Flag:** until G0 is closed, V1 cannot ship. Operator should NOT begin V1 implementation while G0 remains open (per synthesis §4.0 "do not begin V1 surface design before G0 closes").

### §13.5 OD-V1-5 — V1 ship gate confirmation

(Per C §C6.1 + synthesis §4.2 Phase 2 prerequisites.)

The proposed ship gate (synthesis §4.2):
- E.2 live-replay completes with ≥0.83 structural similarity across 3 cases.
- No architectural regressions in live mode.
- G0 closed.
- Operator decision on OD-V1-1 (7 vs 8).
- Operator decision on OD-V1-2 (CLI vs CLI+HTML).
- Operator decision on OD-V1-3 (refuse-explainer copy).
- Per-surface substrate-anchor audit signed off (per C §C7.5).
- Linguistic audit signed off (per §10.5 of this spec).
- LoC budget audit signed off (per §12.5 of this spec).

Operator confirms or revises the gate.

### §13.6 OD-V1-6 — Persistence directory location

Where do V1's read targets live on disk? Anchored to runner's `base_persistence_dir` (per `memory_logger.py`). Operator selects a stable path; V1 reads from there.

### §13.7 OD-V1-7 — Mode badge wording

Screen 1 shows a mode badge ("offline" / "live"). Operator confirms wording. (Trivial; flagged for completeness.)

---

## §14 What this specification does NOT include

This section is load-bearing for the non-expansionary stance. The following non-inclusions are doctrinal, not omissions:

1. **No implementation.** This spec describes data flow, screen inventory, schema mapping, copy substrate, LoC budget. It does not write any rendering code. The operator decides the stack separately (OD-V1-2).

2. **No stack choice.** Python / Node / Go / Rust — the spec is invariant. The spec does not commit `argparse` vs `click` for CLI, nor Jinja2 vs handlebars for HTML if HTML is selected. Per §1.3 stack-agnostic posture.

3. **No V2 cross-case feature.** No laboratory view. No pattern panel. No judgment-act log. No capacity-vs-truth observability panel. No sterile-equilibrium detector outputs. All are V2/Phase-6 scope per synthesis §4.6 and B §B4.3.

4. **No chatbot affordance.** No conversational turn, no message thread, no "ask ELIF about this case" surface. Per B §B1.1, C §C7.8.

5. **No prose-summarization affordance.** No "explain this verdict in plain language" button. No LLM-generated executive summary. Per B §B-non-recommendations 4; C §C3.1 (executive briefs DECORATIVE if default).

6. **No audio rendering.** No TTS of verdict, no audio briefing, no "listen to the case." Per B §B2.7 + C §C3.10. Only screen-reader-accessible structured text (accessibility infrastructure, NOT an audio briefing surface — per C §C3.10).

7. **No video rendering.** No video summary, no animated walkthrough. Per B §B2.8 + C §C3.11.

8. **No re-run-with-different-prompt affordance.** No "try a different framing" button. No "what if you change X" sandbox. Per B §B3.6 + B §B-non-recommendations 8.

9. **No multi-operator infrastructure.** No authentication beyond what the OS provides (operator owns the laptop). No per-participant attribution. No conflict resolution. No "invite a collaborator." All V3/Phase-9 scope per synthesis §4.9 (SP-labeled, may never open).

10. **No cross-case observability.** No aggregated uncertainty trends. No pattern frequency counts. No "case N references case N-1 structures" surface. All V2/Phase-6 scope per synthesis §4.6 + C §C6.2.

11. **No knowledge-graph framing.** No "what ELIF has learned" surface. No accumulated-wisdom store. Per B §B-non-recommendations 11; C §C7.4 truth-accumulation prohibition.

12. **No public-facing surface.** V1 is operator-facing only. No share affordance. No "publish this case" button. No external readers. Per B §B-non-recommendations 9.

13. **No cross-product integration.** No coupling to OSG runtime. No Limova hooks. No media biome reuse. Per synthesis §1.7 permanent prohibition.

14. **No new component, no new Article, no new procedure step, no new schema, no new closed-set member.** Per task brief absolute constraints. Per A + B + C + synthesis convergence at §1.2.

15. **No simulation view, no world-model UI.** Per synthesis §1.1 + A §A1.6 + C §C3.8. World models OUTSIDE ELIF; visualisation question deferred to Phase 6/7/8 (synthesis §4.7-4.8).

16. **No "decision-room" prose framing in operator-facing copy.** The decision-room is the ARCHITECTURE (B §B1.7); the operator's screen language uses arbitration-trace verbs (§10.2), not "welcome to the decision room" copy.

17. **No metrics dashboard inside V1.** V1 is per-case rendering. Operator-mode debug surface (§2.8) carries technical metadata; it is not a metrics dashboard. Cost meter, throughput trend, refuse-rate aggregate — all V2 cross-case scope.

18. **No "confidence percentage" or numeric uncertainty score.** Per §7.5 + C §C7.4. Numerical aggregation over uncertainty fields is an Article III violation at the rendering layer.

19. **No "advice" / "recommendation" / "suggested action" framing.** Per §6.3 + B §B4.1 ("the verdict is the load-bearing communication object; compressing it visually risks the governance opacity failure mode").

20. **No "save this run" / "bookmark this case" affordance.** The cases are persistent files; the operator has the filesystem. V1 does not duplicate that with bookmarking UX. (Avoid over-ceremonialization per CLAUDE.md operator doctrine.)

21. **No drift-probe live-mode test surface.** Article I drift-probe (per `elif_v0_1_what_remains.md` §5.2) is a procedure-level test, not a V1 surface. Tested separately in Phase 1 E.2 live-replay; not rendered in V1.

22. **No surface that hides a load-bearing schema field.** Every field in v0.4.0 schemas is either rendered (per §4 mapping) or explicitly omitted with justification (per §4.15). No field is hidden by accident.

23. **No engagement metric inside V1.** No time-on-screen tracking. No click-through funnels. No "operator engagement score." These are the engagement-loop affordances B §B-non-recommendations 8 and `momentum_capture_warning.md` forbid.

---

## §15 Cross-reference index

Anchors used in this spec, traceable to source:

| Substrate anchor | Source |
|---|---|
| 7 components / 11 steps | `elif_v0_1_what_remains.md` §1; `src/elif_v0_1/components/`, `src/elif_v0_1/orchestration_runner.py` |
| Closed-set `verdict ∈ {constrain, refuse, explicitly_abstain}` | `governance_kernel.py` `_VERDICT_VOCAB` line 65 |
| Closed-set `event_types` (11) | `memory_logger.py` `_VALID_EVENT_TYPES` line 47-59 |
| Closed-set `change_types` (5) | `memory_logger.py` `_VALID_CHANGE_TYPES` line 63-69 |
| `STEP_9_OUTPUT_SCHEMA` `unresolved_uncertainty_sources` `minItems=1` | `governance_kernel.py` schema reference; `src/elif_v0_1/schemas/__init__.py` |
| exit_code=20 = GovernanceRefuseError | `orchestration_runner.py`; `elif_v0_1_alpha_replay_report.md` §case_01-03 |
| 14 MemoryLogger events per refuse-case in alpha | `elif_v0_1_alpha_replay_report.md` §case_01.6 |
| 2,533 component LoC | `elif_v0_1_alpha_cost_complexity_report.md` §1 |
| 0.83 structural similarity | `elif_v0_1_alpha_replay_report.md` §case_01.3 |
| Article V (Refusal Capability) | `elif_constitutional_layer.md` (locked v0.4) |
| Article VII (Capacity vs Truth) | `elif_constitutional_layer.md` (locked v0.4) |
| Decision-room archetype | Audit B §B1.3, §B1.7 |
| Laboratory archetype (cross-case; V2) | Audit B §B1.4; Audit C §C6.2 |
| Communication object = arbitration trace | Audit C §C2.3 |
| Rendering ≤ 0.3 × substrate LoC | Audit C §C7.6 |
| 7-vs-8 stage tension | Audit B §B3.4 vs Audit C §C5.3; Synthesis §2.1 |
| G0 refuse-halt adjudication | Synthesis §4.0; Audit A §A3.4; Audit B §Operator-decision 2; Audit C §OD-C-1 |
| Pausability test | Audit B §B4.5; Synthesis §1.9 |
| No chatbot / simulation workspace / audio / video | Audit B §B1.1, §B1.5, §B2.7-2.8; Audit C §C3.10-3.11; Synthesis §1.4 |
| Pedagogical-verb count <10% threshold | Audit C §C7.8 |
| Unhedged claim-language threshold = 0 | Audit C §C7.4 |
| Per-surface substrate-anchor audit | Audit C §C7.5 |
| Position A vs Position B refuse-halt | `elif_v0_1_what_remains.md` §3; `elif_v0_1_alpha_replay_report.md` §case_01.7 |
| `operative_truth_separator.py` 207 LoC implemented but unexercised on refuse-path | `elif_v0_1_what_remains.md` §1.6 |
| Schema-required `distinguishing_prediction` + `fails_if` (UI equality required) | Audit C §C3.5; `hypothesis_validator.py` |
| Engagement-theater warning | Audit C §C1.15 (from micro-video doctrine) |
| Four-organ separation (analogous) | CLAUDE.md (OSG project); Audit A §A1.1; Synthesis §1.7 |
| Momentum-capture warning | `momentum_capture_warning.md` memory note |

---

## §16 Coda

V1 ships when:
- G0 closes (operator writes the decision down).
- E.2 live-replay completes at ≥0.83 structural similarity with no architectural regressions.
- OD-V1-1 through OD-V1-7 are resolved.
- The per-surface substrate-anchor audit is signed off.
- The linguistic audit is signed off.
- The LoC budget audit is signed off.

V1 is small, precise, refuse-aware, and read-only. It renders what the v0.1 alpha produced; it does not invent. It honors arbitration as the architecture's identity; it does not import chatbot, simulation, or pedagogical affordances. It is a 7-screen flow over existing persistent JSON + JSONL artefacts, capped at 760 LoC, with refuse-as-correct-verdict as the load-bearing visibility commitment.

The operator can pause for weeks and re-enter. The verdict is never hidden. The uncertainty is never minimized. The closure is never disguised as "ELIF learned something." The substrate decides; the rendering surfaces what was decided. That is V1.

Everything else this spec could have proposed — visualisations, summaries, agent affordances, multi-operator rooms, public artefacts, knowledge-base aggregations — is either DECORATIVE or ACTIVELY COUNTERPRODUCTIVE under current evidence. The discipline is to refuse them until evidence forces a different answer. E.2 live-replay is the next evidence gate. Until G0 closes and E.2 runs, V1 stays a sketch.

---

**End of V1 specification.**
