# ELIF Audit A — World Models Inside ELIF

> **Status:** Operator-level strategic audit v0.1 — 2026-05-30. Authoring-only deliverable.
> **Scope:** Positioning analysis for "world models" relative to ELIF v0.1-alpha (shipped) + v0.4 Constitutional Layer (locked).
> **Authority:** Doctrinal audit; spawned from operator request for stress-testing the working hypothesis "LLMs generate. World models simulate. Agents execute. ELIF validates, arbitrates, governs, structures discovery, preserves corrigibility."
> **Constraints:** Non-expansionary. Anti-drift. Architecture-aware. No new components, no new articles, no new phases.
> **Inputs read:** `notes/elif_v0_1_what_remains.md`, `notes/elif_v0_1_alpha_replay_report.md`, `notes/elif_v0_1_alpha_cost_complexity_report.md`, `notes/future_audit_world_model_integration.md`, `notes/long_range_roadmap_v0_1.md`, OSG memory (`elif_constitutional_layer.md`, `elif_long_range_roadmap.md`, `momentum_capture_warning.md`), `src/elif_v0_1/components/`.

---

## Table of contents

1. [Three epistemic registers (read this first)](#three-epistemic-registers-read-this-first)
2. [A1. Architectural position](#a1-architectural-position)
3. [A2. Minimal integration path](#a2-minimal-integration-path)
4. [A3. Governance risk](#a3-governance-risk)
5. [A4. Operational roadmap](#a4-operational-roadmap)
6. [Operator decisions queued](#operator-decisions-queued)
7. [What this audit does NOT recommend](#what-this-audit-does-not-recommend)

---

## Three epistemic registers (read this first)

Throughout this document, every claim is tagged as one of:

- **CURRENT EVIDENCE (CE):** Demonstrable from the v0.1-alpha implementation (7 components, 11 steps, 2,533 component LoC, 8,424 total LoC), the offline replay (33 fixtures, 3 cases, 0.83 structural similarity vs. operator-authored Condition C, 100% test pass), or the v0.4 Constitutional Layer doctrine documents.
- **PLAUSIBLE FUTURE (PF):** A reasonable projection IF the current evidence holds under live-replay pressure (E.2 authorized as of 2026-05-30, not yet executed). PF claims assume Articles I-VII remain structurally enforced, the runner halts as currently coded, and Memory Logger persistence stays append-only.
- **SPECULATION (SP):** Beyond reasonable projection. Listed for completeness. Explicitly labeled. Never load-bearing for any recommendation.

The operator's working hypothesis itself is **PF**, not **CE**. It is a clean direction-pressure formulation that this audit stress-tests; it is not yet demonstrated by any artifact in the lab.

---

## A1. Architectural position

This section evaluates five candidate placements for world models relative to ELIF. Each is taken seriously. The default position is reached at the end, with the specific evidence that would flip it.

### A1.1 Option I — Outside ELIF (ELIF validates world-model outputs but does not host them)

**Shape:** World models live in a separate organ (a "simulation organ" parallel to the future Limova analogue in OSG's four-organ split). ELIF receives world-model outputs as input frames or as evidence anchors and applies its 11-step procedure to them. ELIF never invokes a world model; it never owns simulation state; it never tunes a simulator. The world model is to ELIF what the LLM cognition layer is to OSG's pedagogical biome — loosely coupled, never in the runtime authority path.

**Pros:**
- (CE) Preserves four-organ separation discipline: the OSG codebase already encodes "loosely coupled, never in runtime path" as a load-bearing pattern (`CLAUDE.md` four-organ separation, `MEDIA_BIOME_DOCTRINE.md`). Reusing the pattern at ELIF↔world-model boundary is doctrinally cheap.
- (CE) Compatible with Article I (Non-Absolutization of Intelligence): a world model is a partial projection; treating it as external evidence — not internal sovereignty — is the structurally correct posture.
- (CE) Compatible with Article IV (Partiality of Models): the simulator's output is theoretical until reality-validated; the operative/theoretical separator (Step 10) already exists to handle exactly this shape.
- (PF) Preserves the operator's working hypothesis verbatim: "World models simulate. ELIF validates, arbitrates, governs." Separation is the syntactic form of the hypothesis.
- (CE) Keeps ELIF's component count at 7. No 8th component, no parallel layer. The Step 8 decision package §1 Q3.1 already rejected an 8th component; this option does not re-open that question.

**Risks:**
- (PF) Risk of becoming a "world-model wrapper service" — i.e., ELIF degenerates into a thin validation shell over upstream simulator output and loses its own arbitration substrate. This is the inverse-momentum-capture failure: ELIF's identity gets captured by what it validates, not by what it produces.
- (PF) Coupling at the schema boundary becomes load-bearing: if `world_model_response.schema.json` (proposed in `future_audit_world_model_integration.md` §10) ever drifts, ELIF's input frame shape drifts with it. The decoupling looks clean in prose but creates a fragile schema seam in practice.
- (CE) The current `InputFrame` shape in `src/elif_v0_1/base.py` does not yet have an evidence-anchor or model-citation field. Adopting Option I in the form proposed would require either (a) augmenting `InputFrame` (drift risk) or (b) constraining world-model output to fit the current frame shape (loses information).

**Doctrine compatibility:**
- Article I: COMPATIBLE (world model is external partial; not sovereign).
- Article II (Frame Humility): COMPATIBLE (frame validator can refuse a simulation-derived framing as malformed; Step 1 verdict `needs_decomposition` still applies).
- Article III (No Self-Validation): COMPATIBLE — world-model output is external evidence by construction.
- Article IV (Partiality of Models): NATIVE FIT — operative/theoretical separation is the architecturally correct treatment of simulation output.
- Article V (Refusal Capability): COMPATIBLE — Step 9 can refuse a simulation-anchored frame the same way it refuses any other.
- Article VI (Coherent Convergence): COMPATIBLE if branching roadmap stages can ingest simulator outputs as evidence.
- Article VII (Capacity vs Truth): COMPATIBLE — Memory Logger can record simulator citations as capacity (which simulator helped on which case) without claiming truth accumulation.
- Four-pole taxonomy: ALL FOUR POLES preserved at the ELIF surface; absolutization risk shifts to the simulator-organ boundary but stays addressable via Article I recursion.
- Four-organ separation (OSG analogue): CONSISTENT.

**Evidence basis:**
- (CE) `notes/future_audit_world_model_integration.md` already names the connector architecture as "external Model Registry → Connector Adapter" — its own author framed world models as external when the audit was deferred 2026-05-27. The deferred audit is doctrinally consistent with Option I.
- (CE) The Step 8 decision package explicitly rejected an 8th component, and `notes/elif_v0_1_what_remains.md` §3 documents that the rejection held under implementation pressure.

### A1.2 Option II — Inside ELIF as a subordinate layer (under one of the 7 components)

**Shape:** World-model integration becomes a sub-responsibility of an existing component. Two natural homes:
- **(II-A)** under `hypothesis_validator` — Step 4 emits hypotheses; world models test the `distinguishing_prediction` field against simulator output.
- **(II-B)** under `branching_roadmap_engine` — Step 7 mode A emits outside-original-frame trajectories; world models project each trajectory and feed back projection deltas.

**Pros:**
- (CE) No new component. Component count stays at 7. Step 8 rejection of an 8th component remains honored.
- (PF) Tight integration with the existing schema seam — simulator output enters the procedure at a known, schema-validated step rather than via an external connector handshake.

**Risks:**
- (CE) Violates `notes/elif_v0_1_what_remains.md` §1 finding that components survived "as their scaffold-pinned shapes" — adding a world-model sub-responsibility would require either signature extension (drift) or a new method (signature explosion).
- (PF) Imports simulator cost into component cost: `cost_complexity_report.md` §1 shows offline cost is 0 and live cost is ~$0.21/case. Adding world-model invocation under one component inflates per-component LLM-call budget. The 22-call cap (§8.4) becomes load-bearing in a new way.
- (PF) **Article IV regression risk:** if a world model is invoked *inside* `hypothesis_validator`, the operative/theoretical separation gets blurred — the hypothesis-with-simulator-test starts to feel like ground truth rather than a partial projection. Subordinating a world model under any component drifts the component toward sovereignty-shaped output.
- (PF) Violates the rejected-8th-component decision in spirit: an 8th *component* was rejected, but the work it would have done leaks into existing components, which is functionally the same architectural expansion under a different label.

**Doctrine compatibility:**
- Articles I + IV: VIOLATED IN SPIRIT (the subordination invites sovereignty drift inside the host component).
- Article VI: COMPATIBLE (still converges into actionable pathways).
- Article VII: AT RISK — Memory Logger schemas would need to distinguish "simulator-anchored capacity" from "procedural capacity," which is exactly the truth-accumulation seam Article VII warns about.
- Four-pole taxonomy: weakens defense against the **absolutization** pole at the host-component boundary.

**Evidence basis:**
- (CE) `notes/elif_v0_1_what_remains.md` §2 says "Strictly: none. All 7 components ship at full pinned-signature implementation." Subordination violates the pinning principle.

### A1.3 Option III — Inside ELIF as a parallel layer (peer to the 7 components)

**Shape:** World models become the 8th component or a parallel "world model" subsystem with its own step ownership. Distinguished from Option II by being a peer, not a subordinate.

**Pros:**
- (PF) Forces explicit schema design at the simulator seam — no hidden coupling.
- (PF) Makes simulator cost visible at the procedure level rather than buried inside a host component.

**Risks:**
- (CE) **DIRECTLY VIOLATES** the Step 8 decision package §1 Q3.1 rejection of an 8th component, which `notes/elif_v0_1_what_remains.md` §3 confirmed held under implementation pressure ("the rejected 8th component from Step 8 §1 Q3.1 stayed rejected").
- (CE) Inflates the procedure: would add steps beyond the current 11 (the 11-step compression — old Step 11 absorbed into Step 9 — would partially unwind).
- (PF) **Direct conflict with v0.4 iteration discipline:** "The trajectory should now bend toward COMPRESSION, not addition" (`elif_constitutional_layer.md`). Adding a parallel layer is the maximally additive move available.
- (PF) Re-opens the prestige risk: a parallel layer with its own step ownership accumulates structural importance that the locked rule "no component survives by prestige" must then defend against.

**Doctrine compatibility:**
- v0.4 iteration discipline: VIOLATED.
- "no component survives by prestige" (locked rule): WEAKENED.
- Article VII risk 30 ("Article VII defends long-running ELIF instance against compression"): ACTIVATED — adding a parallel layer hands the future-compression-defender new mass to defend.

**Evidence basis:**
- (CE) Step 8 decision package rejection of the 8th component stayed locked through alpha implementation.
- (CE) v0.4 explicitly says "Future v0.5 (if any) should be smaller than v0.4."

### A1.4 Option IV — Inside ELIF as an optional layer (activatable per-case)

**Shape:** World models are an optional capability that the operator (or governance kernel) can activate per-case when a frame's nature suggests simulation would help. Off by default; on by per-case opt-in.

**Pros:**
- (PF) Preserves component count at 7; the "world model layer" is more a configuration flag than a structural element.
- (PF) Adopts the "dormant-by-default" discipline already in use in OSG's media biome (`packages/openstudygo_media_biome/` Phase A — 34-observer closed-set registry, all dormant).
- (PF) Operator-triggered activation aligns with non-self-propagation (`elif_constitutional_layer.md` foundational operational constraint).

**Risks:**
- (CE) The dormant-by-default pattern in OSG works because each observer is small (registry entry + activation criteria). A dormant world-model integration is NOT small: it requires a connector, a schema, a registry, an arbitration process — see `future_audit_world_model_integration.md` §10 proposed artifacts. The "optional" framing hides architectural mass.
- (PF) The activation decision becomes a new governance surface. Who decides per-case activation? If the governance kernel decides, governance kernel responsibility expands (drift). If the operator decides, every case needs an upfront activation choice (overhead).
- (PF) Per-case activation creates two cohorts: cases-with-simulator and cases-without. Article VII longitudinal tracking would need to handle the heterogeneity, complicating Memory Logger schema.
- (PF) "Optional" frequently degenerates into "default-on for cases that look harder" — which is a sovereignty-import path (the simulator becomes a confidence prop on hard cases).

**Doctrine compatibility:**
- Non-self-propagation: COMPATIBLE if operator-gated.
- Article VII (capacity, not truth): AT RISK due to heterogeneity.
- Four-pole taxonomy: introduces a new sterile-equilibrium variant — "simulator-on" cases close prematurely on simulator output, "simulator-off" cases stay in honest under-determination.

**Evidence basis:**
- (PF) The dormant-by-default pattern is proven small-scale (media biome). It is not proven for components of world-model size.

### A1.5 Option V — Inside ELIF as a future layer (Phase 5+, contingent on evidence)

**Shape:** World-model integration is reserved for a future phase of the long-range roadmap, contingent on prior gates being satisfied. `long_range_roadmap_v0_1.md` Phase 6 already names this position: "World-Model Orchestration (speculative direction)."

**Pros:**
- (CE) **THE ROADMAP ALREADY ENCODES THIS.** Phase 6 is named, gated (G6.1-G6.3), and bounded ("Do not cross yet" list). The audit is asking a question the roadmap has already answered structurally.
- (CE) Compatible with the deferred-audit posture of `future_audit_world_model_integration.md` ("This is a question-preservation artifact only").
- (CE) Respects the v0.4 plateau (no expansion until benchmark cases 2-3 produce evidence).
- (PF) Allows benchmark evidence from Phase 1-2 to inform whether world models should ever enter ELIF at all, or remain external organs.

**Risks:**
- (PF) "Future layer" framing leaves the architectural position ambiguous. Phase 6's "World-Model Orchestration" is consistent with Option I (orchestration = ELIF orchestrates external simulators, does not host them) AND with Option IV (optional layer activated when orchestration needs it). The roadmap does not yet commit to one or the other. This audit's job is to commit.
- (PF) "Future" framing risks momentum capture: as Phase 5 approaches, pressure builds to start preparing Phase 6 architecture early — which is exactly the failure mode the deferred-audit document was written to prevent.

**Doctrine compatibility:**
- Momentum capture warning: COMPATIBLE if "future" is bounded by explicit gates and stays as direction-pressure only.
- Roadmap failure mode #39 (Roadmap-as-prestige): AT RISK — if Phase 6's existence in the roadmap starts making Phase 6 feel inevitable, the roadmap has captured the architecture.

### A1.6 Default position and the evidence that would flip it

**Default position: OPTION I — Outside ELIF.**

World models sit outside ELIF as a separate organ. ELIF validates world-model outputs as external evidence anchors, following the same operative/theoretical discipline it applies to any other input. ELIF does not host, invoke, tune, own state for, or arbitrate among world models from inside its 7-component surface.

This position is reached by elimination:
- Option II (subordinate) violates the pinned-signature finding (`elif_v0_1_what_remains.md` §1).
- Option III (parallel) violates the 8th-component rejection AND the v0.4 compression direction.
- Option IV (optional) hides architectural mass behind a configuration flag and creates governance surface drift.
- Option V (future) is the roadmap's structural position but is not yet specific enough to commit; this audit's contribution is to fill in that Phase 6 is most safely realized AS Option I.

**Option I is doctrinally the cheapest position to defend.** Every article either natively fits the external-organ shape or is recursively defended at the schema boundary the same way it is defended at the frame boundary today.

**Evidence that would flip the default:**

1. (PF→CE) If live-replay (E.2) reveals that the current Step 4 `distinguishing_prediction` schema field is structurally insufficient to anchor hypotheses without simulator-derived test conditions, Option II-A becomes more defensible (hypothesis validator sub-responsibility). The flip is gated on a specific live-replay failure mode, not on speculation.
2. (PF→CE) If cases 2 and 3 (benchmark execution Phase 1) produce frames where world-model output is the only available evidence anchor (no domain literature, no operator expertise, no historical data), Option I's "external evidence" framing collapses because there is no other external evidence to triangulate against. In that case Option IV (optional internal) becomes more honest than Option I.
3. (PF→CE) If Article VII longitudinal tracking shows that Memory Logger capacity-accumulation is silently dominated by simulator-citation patterns, the boundary between "external" and "internal" has effectively collapsed, and Option I is a fiction. In that case Option V (future re-evaluation) with explicit recursion is required.

None of these flip conditions is satisfied by current evidence. The default holds.

---

## A2. MINIMAL INTEGRATION PATH

This section assumes ELIF survives live-replay (E.2 authorized) and asks: what is the smallest possible world-model integration that creates real value without architecture inflation? Six candidate integration shapes are evaluated. Each is anchored to a specific article and a specific case_01/02/03 behavior from the alpha replay.

### A2.1 Candidate evaluation — six integration shapes

#### A2.1.1 Scenario projection

**What it is:** Given a Step 7 mode A trajectory (outside-original-frame), a world model projects the trajectory N years forward and emits projected outcomes.

**Anchor article:** Article VI (Coherent Convergence). The trajectory needs to converge into something actionable; projection is one form of convergence test.

**Anchor case behavior:** case_02 (climate-adaptation bundle) Step 7 produces trajectories like "trajectory T2: opt-in regional pilots with rollback gates." A scenario-projection world model could project T2's 5-year and 10-year reversibility profiles to anchor the Step 9 verdict.

**Belongs inside ELIF?** **NO.** Scenario projection is the canonical case for an external simulation organ. ELIF receives projected outcomes as evidence; the operative_truth_separator (Step 10) treats projected outcomes as theoretical until reality-validated. **External (Option I).**

#### A2.1.2 Trajectory simulation

**What it is:** Multi-step state evolution of a system under specified policies — distinct from scenario projection in that the simulator owns the system state, not just the outcome.

**Anchor article:** Article IV (Partiality of Models). Trajectory simulators are the textbook case where the operative/theoretical separation must be defended hardest.

**Anchor case behavior:** case_03 (mental-health AI bundle) Step 6 produces multi-scale relations (data-coupling depth × infrastructure persistence). A trajectory simulator could exercise these axes under specified governance regimes.

**Belongs inside ELIF?** **NO.** Trajectory simulators carry STATE. ELIF's components are stateless per `cost_complexity_report.md` §3 ("methods are stateless per §8.9"). The only stateful component is Memory Logger, and `cost_complexity_report.md` §3 already flags this: "the only component with persistent state. JSONL schema drift is the load-bearing maintenance concern." Adding a second stateful surface inside ELIF doubles the stateful-component count and proportionally doubles the schema-drift attack surface. **External (Option I), strongly.**

#### A2.1.3 Intervention comparison

**What it is:** Given multiple proposed interventions (policy A vs B vs C), simulate each and emit comparative deltas.

**Anchor article:** Article VI (Coherent Convergence) + Article III (No Self-Validation). The intervention comparison must be anchored to external evidence, not to simulator-internal elegance.

**Anchor case behavior:** case_01 (electroculture) Step 4 produces hypothesis sets like "H1: weak electrical stimulation increases nitrogen fixation in arid soils." Intervention comparison could project H1's deployment vs. control under varying soil-conductivity profiles.

**Belongs inside ELIF?** **NO** — but with a partial qualifier. The COMPARISON of intervention outputs is structurally close to what the branching_roadmap_engine already does at Step 8 (stage-gated roadmap with continuation gates). ELIF already arbitrates among alternatives. **The simulators producing the per-alternative outcomes are external; the comparison/arbitration over their outputs is what ELIF already does at Step 8.** No new mechanism required.

#### A2.1.4 Policy forecasting

**What it is:** Closely related to scenario projection but specifically forecasts policy-level outcomes (adoption rates, compliance, equilibrium effects).

**Anchor article:** Article V (Refusal Capability) + Article IV (Partiality). Policy forecasts are the genre most prone to over-confident sovereignty claims; refusal capability must remain intact.

**Anchor case behavior:** case_02 (climate-adaptation bundle) Step 9 verdict was `refuse`. A policy forecast that suggested 20-35% food-resilience gain (from the input frame) is exactly the kind of simulator output that Article V must be able to refuse even when the simulator output is internally consistent.

**Belongs inside ELIF?** **NO.** Policy forecasts must enter the procedure as inputs to Step 1 (frame validator) or as evidence anchors to Step 4 (hypothesis validator). They must NOT enter as anchors that bypass Step 9 refusal capability. The cleanest way to guarantee this is to keep them external. **External (Option I).**

#### A2.1.5 Ecosystem simulation

**What it is:** Multi-agent simulation of an ecosystem (economic, biological, sociotechnical) with emergent behaviors.

**Anchor article:** Article I (Non-Absolutization of Intelligence) + Article VII (Capacity vs Truth).

**Anchor case behavior:** None of case_01/02/03 currently call for ecosystem simulation; this is the most speculative candidate. (CE: alpha replay produces no ecosystem-simulation signal.) (SP: future cases involving global coordination problems could.)

**Belongs inside ELIF?** **NO** — and this is the case where the "external" answer is most important. Ecosystem simulators are the genre most prone to sovereignty drift because their outputs LOOK like reality and the cost of running them creates institutional momentum to treat their outputs as authoritative. Article I must be defended at the input boundary; the cheapest way is to keep ecosystem simulators outside ELIF entirely. **External (Option I), defensively.**

#### A2.1.6 Uncertainty modeling

**What it is:** Probabilistic/Bayesian frameworks that quantify uncertainty over outcomes.

**Anchor article:** Article VI (Coherent Convergence) — Step 9 already requires `unresolved_uncertainty_sources` with `minItems=1` per `notes/elif_v0_1_what_remains.md` §1.5.

**Anchor case behavior:** All three alpha cases produce Step 9 verdicts with named uncertainty sources. The governance kernel already names uncertainty; uncertainty modeling would QUANTIFY what is currently NAMED.

**Belongs inside ELIF?** **PARTIAL — this is the one candidate where a case can be made for thin internal capability, but the case is not strong enough to flip the default.**

The current `STEP_9_OUTPUT_SCHEMA` (per `governance_kernel.py` lines 50-65) requires `unresolved_uncertainty_sources` as a string array. There is no field for uncertainty MAGNITUDE. If live-replay reveals that operators want to know "how uncertain" not just "what uncertainty source," a thin uncertainty representation could enter the schema without a world model.

**Recommendation:** uncertainty modeling, if needed, should be a SCHEMA refinement to existing Step 9 output, NOT a world-model integration. This means it does not enter the world-model question at all; it is a separate schema-evolution question that would not require Option I-V evaluation.

### A2.2 Summary table — what belongs where

| Candidate                  | Belongs inside ELIF? | Belongs as separate organ ELIF validates against? | Anchor article | Anchor case behavior                                            |
|----------------------------|----------------------|----------------------------------------------------|----------------|------------------------------------------------------------------|
| Scenario projection        | No                   | Yes                                                | VI             | case_02 Step 7 trajectories                                      |
| Trajectory simulation      | No (strongly)        | Yes                                                | IV             | case_03 Step 6 multi-scale relations                             |
| Intervention comparison    | No (comparison is already Step 8) | Yes (the simulators); No (the comparison) | VI + III  | case_01 Step 4 hypothesis-set deployment alternatives            |
| Policy forecasting         | No                   | Yes                                                | V + IV         | case_02 Step 9 refuse-verdict-despite-forecast                   |
| Ecosystem simulation       | No (defensively)     | Yes                                                | I + VII        | (CE) None in current cases; SP for future cases                  |
| Uncertainty modeling       | Not as world model. Possibly as Step 9 schema refinement. | N/A | VI | All three cases Step 9 `unresolved_uncertainty_sources` |

**Result:** ZERO of the six candidates belong inside ELIF as currently scoped. Five belong as separate organs. One (uncertainty modeling) belongs as a Step 9 schema refinement and is not a world-model question.

### A2.3 What the minimal integration path actually is

The minimal integration path is **a schema seam, not an architecture**.

Concretely:

1. **A single schema** (`world_model_response.schema.json` — already proposed in `future_audit_world_model_integration.md` §10 #5) that defines the SHAPE in which any external simulator's output must arrive before it can enter ELIF as an evidence anchor. Fields: `model_id`, `assumptions`, `predicted_outcomes`, `uncertainty`, `confidence`, `known_limits`, `refutation_conditions`. This schema lives at the ELIF boundary, NOT inside any component.
2. **One boundary adapter** that validates incoming world-model output against the schema and rejects malformed input at the `InputFrame` boundary — the same way frame_validator rejects malformed framing today.
3. **No new component.** No 8th component, no parallel layer, no optional internal capability.

This is consistent with Option I (Outside ELIF) and is the minimal integration path that creates real value (operators can cite external simulators as evidence anchors) without architecture inflation (ELIF stays at 7 components / 11 steps / pinned signatures).

**Cost estimate (PF):** schema file (~150 LoC); boundary adapter (~200 LoC); test fixtures for malformed inputs (~300 LoC). Total ~650 LoC — well within the v0.1 expansion budget and below the 2.8x expansion-floor concern in `cost_complexity_report.md` §5.

**Phase placement (PF):** Phase 5+ at the earliest, per the existing roadmap. The schema seam can be SPECIFIED earlier (Phase 4) but the actual integration into a live procedure should not occur until compositional arbitration has been stress-tested.

---

## A3. GOVERNANCE RISK

This section maps world-model interaction to four governance surfaces of ELIF: corrigibility (Article V), governance (Step 9 / Governance Kernel), anti-drift (Article VII + sterile-equilibrium detector), operative truth (Step 10). Then it maps specifically to the four-pole failure-mode taxonomy. Then it names required governance mechanisms IF world models entered ELIF in any form.

### A3.1 Interaction with corrigibility (Article V)

(CE) Article V is currently structurally enforced by the runner: `verdict == "refuse"` halts the run with exit code 20 (per `elif_v0_1_alpha_replay_report.md` §case_01-03). All three alpha cases produce `refuse` and the runner halts. This is the cleanest defense of corrigibility in the system.

(PF) World models threaten corrigibility specifically because **simulator output is high-status evidence in human reasoning**. The cognitive pattern "the simulation says X, therefore X is settled" is widely documented in policy and engineering contexts. If a world model enters the procedure, the Step 9 governance kernel will face implicit pressure to refuse LESS often when the simulator output is internally coherent.

**Required governance mechanism IF world models enter ELIF (any option):**
- The Step 9 governance kernel prompt MUST cite a closed-set anti-pattern: "simulator output is not evidence of operative truth; it is evidence of a model's projection." This is a prompt-level structural defense that exists today for the verdict vocabulary (`_VERDICT_VOCAB` in `governance_kernel.py` line 65) and would need to be extended.
- The runner's halt-on-refuse discipline (`exit_code=20`) must remain inviolate. No "soft refuse on simulator-anchored frames" path may be introduced.

### A3.2 Interaction with governance kernel (Step 9)

(CE) The governance kernel currently emits `verdict + confidence + unresolved_uncertainty_sources` with `minItems=1` on the uncertainty sources. The closed-set verdict vocabulary is `{constrain, refuse, explicitly_abstain}`.

(PF) World-model integration would press the governance kernel along three drift vectors:

1. **Verdict vocabulary expansion pressure.** A simulator that produces high-confidence projections will create pressure to add a verdict like `accept_with_simulator_anchor` or `conditionally_approve`. This is exactly the closed-set drift `CLAUDE.md` warns against ("closed-set discipline DOCTRINAL").
2. **Uncertainty source dilution.** If simulator output gets cited as ONE uncertainty source, the `minItems=1` requirement is trivially satisfied without surfacing the real uncertainty. The schema requirement is structural, but the prompt-discipline against shallow uncertainty sourcing requires explicit defense.
3. **Confidence inflation.** Simulator output tends to come with numerical confidence values; these get imported as "the model says 0.87 confidence" and ELIF's qualitative confidence becomes anchored to upstream numbers it did not generate.

**Required governance mechanism IF world models enter ELIF:**
- The closed-set verdict vocabulary stays frozen. No simulator-aware verdict gets added. This must be enforced at registry consistency assertion time (the pattern used elsewhere in OSG per `CLAUDE.md`).
- The governance kernel prompt must require that AT LEAST ONE uncertainty source be NON-simulator-derived (a meta-uncertainty rule: "you cannot let the simulator be the only source of named uncertainty"). This is structural anti-monoculture applied to the uncertainty surface.

### A3.3 Interaction with anti-drift (Article VII + sterile-equilibrium detector)

(CE) Article VII is enforced via Memory Logger persistence (open + step_committed + refutation + close events written for every replay per `elif_v0_1_alpha_replay_report.md` §case_01.6). The sterile-equilibrium detector is named in build plan §3.6 but `elif_v0_1_what_remains.md` §5.3 says it is UNTESTED in alpha and is deferred to v0.2.

(PF) World models interact with anti-drift in three specific ways:

1. **Simulator-anchored capacity accumulation drift.** Memory Logger may start logging "we used simulator X on case N" capacity-change entries. Over time, simulator citations dominate capacity accumulation. Article VII's `capacity_accumulation` becomes a function of WHICH SIMULATOR was used, not of ELIF's intrinsic arbitration capacity. This is the cleanest path to **truth accumulation via the back door** (failure mode #23: "Capacity framed as truth approach → sovereignty re-import").
2. **Compositional reuse drift.** Article VII permits compositional reuse of prior structures. If a prior case's simulator citation gets reused on a new case, the reuse FEELS like Article VII operating correctly, but it is actually pattern-locking on the simulator (failure mode #29: "Pattern recognition treated as predictive certainty").
3. **Sterile-equilibrium detection becomes harder.** If simulator-anchored cases all converge to similar verdicts (because the simulator's domain biases push them there), Article VII's longitudinal tracking will see CONVERGENCE — but the convergence is sterile equilibrium induced by simulator bias, not capacity accumulation. The current sterile-equilibrium detector (deferred to v0.2 anyway) must be specifically trained to detect simulator-bias-induced convergence.

**Required governance mechanism IF world models enter ELIF:**
- Memory Logger capacity-change entries MUST tag simulator-anchored capacity separately from procedural capacity. The `_VALID_CHANGE_TYPES` closed-set in `memory_logger.py` line 63-69 currently has five entries; a simulator-anchored variant could not be silently added. Either (a) a new doctrine-approved entry is added (drift risk), or (b) simulator-anchored capacity is REFUSED entry to Memory Logger altogether.
- The sterile-equilibrium detector (v0.2 deferred capability) must include a "simulator-bias-induced convergence" detector before any world-model integration goes live. Without this, anti-drift fails silently.

### A3.4 Interaction with operative truth (Step 10)

(CE) The operative_truth_separator (Step 10) is implemented (207 LoC) but **never exercised in the alpha replay** because the runner halts at Step 9 on `verdict=refuse` and all three cases produce refuse. The operator decision on whether Step 10/11 should run on the refuse-path is pending (`elif_v0_1_what_remains.md` §3 — Position B recommended but not adopted).

(PF) World models interact with operative truth in the strongest, most architectural way of all four governance surfaces:

**Simulator output is BY CONSTRUCTION theoretical until reality-validated.** Article IV (Partiality of Models) is the native article. Step 10 is the native step. The operative_truth_separator is the architectural surface where simulator output is honestly accounted for.

This is also why subordinating world models inside other components (Option II) is doctrinally dangerous: it bypasses the operative/theoretical separation by treating simulator output as already-arbitrated input to upstream steps.

**Required governance mechanism IF world models enter ELIF:**
- Step 10 must explicitly populate `theoretical` with all simulator-derived claims, regardless of how confident the simulator was. This requires an explicit prompt clause AND a schema-level enforcement (a `theoretical_sources` array that must list every simulator cited).
- The operator-pending question on whether Step 10/11 runs on refuse-path becomes MORE LOAD-BEARING under world-model integration. If Step 10 does not run on refuse, simulator-anchored refusals never get their theoretical claims recorded — a Memory Logger gap.

### A3.5 Mapping to the four-pole failure-mode taxonomy

| Pole | World-model-specific failure mode | Defense required IF world models enter ELIF |
|---|---|---|
| **Absolutization** | Simulator output treated as sovereign — "the model says X, therefore X." | Article I prompt-level recursion at the schema boundary; closed-set verdict stays frozen; refusal capability stays inviolate at Step 9. |
| **False closure** | A simulator's high-confidence output closes a case before the procedure has surfaced enough uncertainty. | Step 9 requirement that AT LEAST ONE uncertainty source be non-simulator-derived; Step 10 must run even on refuse so simulator-anchored claims are recorded as theoretical. |
| **Fragmentation** | Multiple conflicting simulators produce divergent projections; ELIF gets stuck decomposing instead of converging. | Step 8 stage-gated roadmap already structurally bounds decomposition cycles; world-model integration must NOT add a new decomposition surface. |
| **Sterile equilibrium** | Simulator-bias-induced convergence: cases anchored to the same simulator family converge to the same verdict shape because of simulator bias, not because of arbitration. Memory Logger capacity accumulation looks healthy but is actually monocultural at the simulator-citation layer. | Sterile-equilibrium detector (v0.2 deferred) must include simulator-bias detection BEFORE world-model integration goes live. This is a hard prerequisite, not a nice-to-have. |

**All four poles have specific world-model failure modes. All four require specific governance mechanisms. None of the required governance mechanisms is currently in v0.1 alpha; they are all v0.2+ scope.**

This is the strongest argument for keeping world models OUTSIDE ELIF (Option I) until at least Phase 4: the governance surface for world-model interaction is non-trivial, and v0.1 alpha does not yet have the governance machinery to defend against the failure modes that world-model integration would introduce.

### A3.6 Can world models become a source of epistemic closure?

**Yes — three distinct epistemic-closure vectors:**

1. **(PF) Drift via capacity accumulation.** Memory Logger silently aggregates simulator citations; over many cases, the citation pattern dominates capacity-change events; future cases inherit simulator-anchored arbitration shortcuts that nobody explicitly authored. The system gets "smarter" but only inside the simulator's domain assumptions.
2. **(PF) Self-confirmation via simulator reuse.** Compositional reuse fires on simulator-anchored structures because they are the densest in Memory Logger. Each reuse increments the confidence in the simulator-anchored pattern. Recognition becomes validation (failure mode #29).
3. **(PF) Monoculture inside simulation.** If two or three simulators of the same family (e.g., all neural-network-based, or all agent-based-model-based) are integrated, the cross-simulator arbitration becomes a simulation-of-simulations meta-arbitration with no exit to reality. Article III (No Self-Validation) is structurally violated even though every individual simulator looks "external."

These are not speculative concerns. They are the failure modes the v0.4 taxonomy was designed to detect, applied to the specific case of world-model integration. **Article VII risks 23, 24, 26, 29, 30 all activate under world-model integration.** None of these risks is hypothetical; they are named in the locked memory document and they are the doctrinal reason world-model integration was deferred in the first place.

---

## A4. OPERATIONAL ROADMAP

This section places world-model integration on the existing v0.1-v0.4 roadmap. It identifies the earliest phase at which integration could logically enter, lists prerequisites, names absolute non-prerequisites (what must not happen early), and specifies evidence gates per entry point.

### A4.1 Where world models could logically enter the existing roadmap

The roadmap already names Phase 6 ("World-Model Orchestration") as the speculative phase for this. Per `long_range_roadmap_v0_1.md` §Phase 6:

> **Critical doctrinal point:** Simulations are tools. Simulation outputs are theoretical until reality-validated (Article IV applies).
> **Gate to Phase 7:**
> - G6.1 — Simulation outputs never claimed as operative truth without reality validation
> - G6.2 — Conflicting world models arbitrated without choosing one as sovereign
> - G6.3 — Simulation absolutization risk addressed

The audit's contribution is to make Phase 6's structural commitment more specific:

**Phase 6 = Option I (Outside ELIF) realization, not Option II/III/IV.**

The roadmap's framing of "orchestration" must explicitly mean "ELIF orchestrates external simulators that live outside its 7-component surface." It must NOT mean "ELIF gains a world-model layer at Phase 6."

**EARLIEST entry point: Phase 5+. Most defensible entry point: Phase 6 as currently scoped.**

Under no interpretation does world-model integration enter at Phase 0-4. Each pre-Phase-5 phase has a structural reason to NOT host world models:

- **Phase 0 (Constitutional Stabilization):** plateau is operational; any architectural addition violates the locked plateau.
- **Phase 1 (Benchmark Execution):** cases 2 and 3 must be authored and run before any architectural extension is considered. Adding world models pre-benchmark contaminates benchmark evidence with simulator influence.
- **Phase 2 (Constitutional Compression):** the test of iteration discipline is compression, not expansion. Adding world models in Phase 2 inverts the phase's purpose.
- **Phase 3 (Minimal Architecture Emergence):** components ship as compressed v0.5 specifies; the 8th-component rejection is reaffirmed. World models would re-open it.
- **Phase 4 (Memory-Bearing Architecture):** Memory Logger must mature from log → substrate. Mixing simulator-citation patterns into Memory Logger before it is mature creates the epistemic-closure failure mode A3.6.1 directly.
- **Phase 5 (Compositional Arbitration):** explicitly named as "do not begin world-model integration until compositional arbitration stress-tested with contradictory cases" (`long_range_roadmap_v0_1.md` §Phase 5 "Do not cross yet").

### A4.2 Prerequisites that must already exist before world-model integration

Per the roadmap and this audit's analysis, the following prerequisites must hold:

| # | Prerequisite | Source | Current state |
|---|---|---|---|
| 1 | Offline replay validated | `elif_v0_1_alpha_replay_report.md` cohort verdict `partially` at 0.83 | SHIPPED (alpha) |
| 2 | Live replay validated (E.2) | Operator authorization 2026-05-30 | AUTHORIZED, NOT YET RUN |
| 3 | Article VII longitudinal tracking shipping at content level (not just persistence level) | `elif_v0_1_what_remains.md` §5 says CONTENT-LEVEL tracking UNTESTED in alpha | NOT YET (gated on refuse-path decision) |
| 4 | Sterile-equilibrium detector active | `elif_v0_1_what_remains.md` §5.3 says UNTESTED, deferred to v0.2 | NOT YET (v0.2 scope) |
| 5 | Multi-case generalization confirmed (cases 2 and 3 produce comparable artifacts) | Phase 1 gate G1.1 | NOT YET (cases 2 and 3 not authored) |
| 6 | Constitutional compression evaluated (Phase 2) | Phase 2 gates | NOT YET |
| 7 | Memory Logger demonstrably influences subsequent case arbitration (Phase 4 G4.1) | Phase 4 gate | NOT YET |
| 8 | Compositional arbitration stress-tested with contradictory cases (Phase 5) | Phase 5 G5.1-G5.4 | NOT YET |
| 9 | Sterile-equilibrium detector includes simulator-bias detection (this audit A3.5) | This audit | NOT YET (new requirement surfaced) |
| 10 | Closed-set verdict vocabulary stays frozen under world-model pressure (this audit A3.2) | This audit | DEFAULT (currently frozen; pressure not yet applied) |

**Prerequisites 1, 9, and 10 are NEW REQUIREMENTS surfaced by this audit beyond the roadmap.** Prerequisites 2-8 are already in the roadmap as phase gates. The audit's contribution is to make explicit that PREREQUISITES 9 AND 10 ARE NON-NEGOTIABLE before any world-model integration of any form.

### A4.3 What absolutely must NOT happen too early

The "do not cross yet" pattern from the roadmap, applied specifically to world models:

1. **Do NOT specify `world_model_response.schema.json` before Phase 4.** The schema seam (A2.3) is genuinely small, but specifying it pre-Phase-4 invites scope creep into Phase 3-4 work. The audit `future_audit_world_model_integration.md` already correctly defers this; that deferral must hold.
2. **Do NOT add a simulator-aware verdict to the Step 9 closed-set vocabulary at any phase.** This is a permanent prohibition. The closed-set discipline is doctrinal; expansion requires formal doctrine revision; world-model-driven vocabulary expansion is the canonical "silent drift" failure mode.
3. **Do NOT activate any world-model integration before the sterile-equilibrium detector is active AND has demonstrated simulator-bias detection capability on contradictory cases.** Prerequisite 9 is non-negotiable.
4. **Do NOT permit Memory Logger to accept simulator-derived capacity-change entries before Phase 4 G4.5 ("Operator can audit, modify, or wipe Memory Logger without architectural injury").** Otherwise simulator citations become unauditable accumulated capacity.
5. **Do NOT permit world-model output to enter Step 1 (frame_validator) as a frame that bypasses `needs_decomposition` verdict.** All world-model outputs that enter the procedure must enter as evidence anchors at later steps, not as pre-validated frames.
6. **Do NOT begin "while we wait for Phase 5, let's also prepare Phase 6" preparation work.** This is the canonical momentum-capture failure (`momentum_capture_warning.md`). Phase 6 preparation BEFORE Phase 5 gates close is exactly the symptom the warning was authored to detect.
7. **Do NOT scope world-model integration on the basis of external pressure** (operator excitement, AI-industry trends, simulator vendor offerings). The roadmap rule is explicit: "Does NOT revise when: External pressure suggests jumping phases."

### A4.4 Evidence gates per entry point

Three entry-point scenarios are possible. Each has specific evidence gates.

#### A4.4.1 Entry at Phase 6 (default, current roadmap)

**Gates (all must close):**
- G6.0 (NEW, from this audit): The schema seam (A2.3) has been specified as a Phase 5-late deliverable WITHOUT being implemented. Specification ≠ implementation.
- G6.1: Simulation outputs never claimed as operative truth without reality validation.
- G6.2: Conflicting world models arbitrated without choosing one as sovereign.
- G6.3: Simulation absolutization risk addressed.
- G6.4 (NEW, from this audit): Sterile-equilibrium detector has demonstrated simulator-bias detection on at least 2 contradictory test cases.

#### A4.4.2 Entry at Phase 5+ (earliest defensible)

**Only the schema seam (A2.3) — not full integration. Gates:**
- G5.5 (NEW, from this audit): Schema seam SPECIFIED but not yet WIRED to any live simulator. Specification reviewed against Articles I, III, IV, VII.
- Phase 5 G5.1-G5.4 closed first.

#### A4.4.3 Entry never (compression path)

**This is a real possibility under the v0.4 trajectory.** If Phase 2 compression evidence reveals that ELIF's value is entirely contained in its 7-component arbitration discipline and world-model orchestration is better served by another organ entirely, world models may never enter ELIF in any form.

This is consistent with the operator's working hypothesis verbatim: "World models simulate." If world models simulate AS A SEPARATE ORGAN that ELIF validates against, then the right long-term position is to keep them separate forever and have ELIF be an arbiter-organ that happens to consume world-model output as one evidence type among many.

**(PF) This is the position this audit defaults to.** Phase 6 in the roadmap is named, gated, and bounded; but the most likely outcome is that Phase 6 manifests as "ELIF orchestrates external simulators" and world models never become an ELIF-internal layer in any form.

### A4.5 Summary roadmap position

| Phase | World-model action | Justification |
|---|---|---|
| 0 (current) | DO NOTHING | Plateau is operational; deferred-audit posture holds. |
| 1 (E.2 + cases 2/3) | DO NOTHING | Benchmark evidence must be uncontaminated by simulator influence. |
| 2 (compression) | DO NOTHING | Compression direction; expansion forbidden. |
| 3 (component implementation under v0.5) | DO NOTHING | 8th-component rejection reaffirmed; components stay at pinned signatures. |
| 4 (Memory Logger maturation) | DO NOTHING | Memory Logger must mature pre-contamination. |
| 5 (compositional arbitration) | SPECIFY schema seam (A2.3); do NOT wire | Schema specification is a Phase 5-late activity; wiring is a Phase 6 activity. |
| 6 (world-model orchestration) | WIRE schema seam to one or two external simulators as Option I orchestration | All G6.0-G6.4 gates must close. Simulator-bias detection must be operational. |
| 7+ | Continue as Option I orchestration; never absorb world models into ELIF's component surface | Permanent doctrinal position. |

---

## Operator decisions queued

This audit places the following decisions on the operator's plate. Each is named, scoped, and time-bound. None requires action before Phase 1 benchmark execution closes.

1. **Confirm Option I as default architectural position (A1.6).** This audit recommends Option I — Outside ELIF — as the load-bearing default. Operator confirmation locks the default and constrains future expansion proposals to operate against this default.
2. **Confirm the minimal integration path is "schema seam, not architecture" (A2.3).** This audit recommends that the entire world-model integration question collapses to a single boundary schema plus a boundary adapter, and that nothing inside the 7-component surface changes. Operator confirmation closes Options II, III, IV decisively.
3. **Confirm new prerequisites 9 and 10 (A4.2).** Prerequisite 9 (sterile-equilibrium detector includes simulator-bias detection) and prerequisite 10 (closed-set verdict vocabulary stays frozen under world-model pressure) are new requirements this audit surfaces beyond the existing roadmap. Operator confirmation makes them binding gates.
4. **Confirm permanent prohibitions (A4.3 items 2 and 6).** Two prohibitions are framed as PERMANENT, not phase-bounded: (a) no simulator-aware verdict added to Step 9 closed-set vocabulary ever, and (b) no Phase 6 preparation work begins before Phase 5 gates close. Operator confirmation makes both permanent doctrinally.
5. **Adjudicate refuse-path Step 10/11 question with world-model context in mind (A3.4).** The pending question from `elif_v0_1_what_remains.md` §3 (whether Step 10/11 run on refuse-path) becomes MORE load-bearing under any world-model integration. Operator may wish to revisit the Position A vs B decision with this audit's analysis as input.
6. **Decide whether Phase 6 ever happens at all (A4.4.3).** This audit surfaces the genuine possibility that Phase 6 is never crossed — that ELIF's mature position is to arbitrate external organs without ever hosting world models internally. The operator may wish to elevate this from "speculative future" to "explicit doctrinal possibility" so that the roadmap correctly represents both branches.

---

## What this audit does NOT recommend

**This is a non-expansionary audit.** The following non-recommendations are LOAD-BEARING and should be cited if any future session proposes the listed actions:

1. **This audit does NOT recommend creating any new ELIF component, including a "WorldModelConnector," "SimulationOrchestrator," "ModelRegistry," or any other 8th component.** The 8th-component rejection stays locked. (Re-asserts `elif_v0_1_what_remains.md` §3.)
2. **This audit does NOT recommend authoring `world_model_response.schema.json`, `connectors/README.md`, `registry/world_models.registry.json`, or any of the artifacts named in `future_audit_world_model_integration.md` §10 #10.** The deferred audit's deferral stays in place. The schema seam (A2.3) is a Phase 5+ specification activity, not a current activity.
3. **This audit does NOT recommend adding any article, doctrine extension, four-pole-taxonomy fifth pole, or constitutional revision in response to world-model concerns.** All world-model failure modes map to existing failure modes (#23, #24, #26, #29, #30 in the v0.4 risk matrix). The constitutional layer is structurally complete for world models; no new article is required.
4. **This audit does NOT recommend creating a "world models" or "simulation" entry in OSG's memory system, in `docs/`, or in any other tracked artifact location at this time.** This audit document itself is the artifact. Adding registry entries or substrate would be the canonical "treat speculation as architecture" failure (`future_audit_world_model_integration.md` §"Why this is deferred").
5. **This audit does NOT recommend that the Step 8 decision package §1 Q3.1 rejection of the 8th component be revisited.** The rejection is the structural form of the answer to the world-model question.
6. **This audit does NOT recommend modifying the runner's refuse-halt behavior in response to world-model considerations.** The refuse-halt is the cleanest defense of corrigibility in the system. Any world-model integration must be designed to live within the refuse-halt discipline, not to relax it.
7. **This audit does NOT recommend specifying a "Phase 6 prep" workstream, a "world-model readiness" workstream, or any pre-Phase-5 preparatory activity for world models.** Such workstreams are the canonical momentum-capture failure (`momentum_capture_warning.md`); naming them is the symptom.
8. **This audit does NOT recommend that ELIF compete with, replace, or absorb the functionality of external world models.** ELIF's value is arbitration. Simulators' value is projection. The four-organ separation pattern that works in OSG should be respected at the ELIF↔world-model boundary as well.
9. **This audit does NOT recommend that the operator's working hypothesis ("LLMs generate. World models simulate. Agents execute. ELIF validates, arbitrates, governs, structures discovery, preserves corrigibility.") be elevated to doctrine.** The hypothesis is a clean direction-pressure formulation and should remain corrigible until Phase 5+ evidence either confirms or refutes its operational coherence. Adopting it as doctrine before benchmark evidence is available is the same failure mode the v0.4 trajectory bent away from.
10. **This audit does NOT recommend any cross-organ coupling between ELIF and OSG, Limova, the media biome, the reviewer biome, the country-shell substitution system, or any other production system.** ELIF is lab-scale; OSG is production. The boundary between them is doctrinally load-bearing in both directions.

---

**End of Audit A.**

Cross-cutting signals to other audits (B-user-experience, C-media-communication) are listed in the structured return summary.
