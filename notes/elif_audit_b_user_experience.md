# ELIF Audit B — User Experience Positioning

> **Status:** Audit v0.1 — 2026-05-30. Operator-level strategic audit. Authoring-only deliverable. No architecture changes proposed.
> **Scope:** UX archetype, media-form, user-journey, and product-roadmap analysis for ELIF v0.1-alpha after implementation pressure and before live-replay (E.2) execution.
> **Authority:** sub-audit of Step 8 / v0.4 constitutional layer / v0.1 alpha replay verdict (`partially` at 0.83 structural similarity, exit_code 20 = GovernanceRefuseError as CORRECT verdict).
> **Doctrine constraint:** non-expansionary, anti-drift, evidence-aware. No new components, no new Articles, no new procedure steps. UX positioning ONLY.
> **Epistemic discipline:** each claim is labeled CURRENT EVIDENCE / PLAUSIBLE FUTURE / SPECULATION. Where labels are omitted, the surrounding paragraph header carries them.

---

## Table of contents

1. [Reading the alpha behavior before judging UX](#reading-the-alpha-behavior-before-judging-ux)
2. [B1. UX archetypes](#b1-ux-archetypes)
3. [B2. Media forms](#b2-media-forms)
4. [B3. User journey](#b3-user-journey)
5. [B4. Product roadmap](#b4-product-roadmap)
6. [Operator decisions queued](#operator-decisions-queued)
7. [What this audit does NOT recommend](#what-this-audit-does-not-recommend)

---

## Reading the alpha behavior before judging UX

This audit is not free to invent a UX. It must work backwards from what the v0.1 alpha actually demonstrates, because any UX archetype not aligned with the alpha's load-bearing behavior is either decorative or actively misleading.

The relevant ground truth from `elif_v0_1_what_remains.md`, `elif_v0_1_alpha_replay_report.md`, and `elif_v0_1_alpha_cost_complexity_report.md`:

- **The alpha is offline-fixture-driven across three operator-locked cases.** Steps 1-9 reproduce reference behavior at 0.83 structural similarity. Steps 10 and 11 do not fire because the runner halts on `verdict=refuse` at Step 9. The exit code is 20 (`GovernanceRefuseError`) and this is the CORRECT verdict, not a failure.
- **The procedure is 11 steps, 7 components, 5 schema tiers, 1 runner, 1 replay harness, 1 MemoryLogger.** Implementation is 5,129 LoC code + 3,295 LoC tests. Tests-to-code ratio 0.64. No component required architectural redesign during implementation.
- **The MemoryLogger writes 14 events per case in alpha replay** (1 open + 9 step_committed + 1 step_7_modeB + 1 refutation + 1 close + 1 bookkeeping = 14, not "702 entries" — the 702 number cited in the brief is not what the replay report records; I use the alpha report's numbers as the verified figure).
- **Cost in offline mode: $0.00 per cohort. Live-mode estimate: ~$0.21 per case, ~$0.63 per 3-case cohort, ~95 cohorts per $20 baseline.** Per-step latency offline is sub-millisecond; live mode is bounded by Anthropic API at 2-5s per structured-output call.
- **The constitutional layer v0.4 is locked: 7 Articles + four-pole failure-mode taxonomy** (absolutization / false closure / fragmentation / sterile equilibrium). Article VII (capacity vs truth) is the governing distinction: capacity accumulation is observable and permitted; truth accumulation is forbidden.
- **The thinking-reed anchor: fragile AND upright.** Each adjective maps to operational rules, not metaphor.
- **The momentum-capture warning is constitutional: pausability is the maturity test.** A UX that cannot be paused / cannot be inhabited briefly without state loss has captured itself.

Operator's working hypothesis under stress-test in this audit:
> "LLMs generate. World models simulate. Agents execute. ELIF validates, arbitrates, governs, structures discovery, preserves corrigibility."

The five verbs ELIF owns — **validate, arbitrate, govern, structure discovery, preserve corrigibility** — are the constraints every UX choice must respect. A UX that frames ELIF as a generator, simulator, or agent is misaligned at the architecture level, not just at the surface.

This anchors B1-B4.

---

## B1. UX archetypes

This section evaluates each candidate archetype against the alpha behavior. The criterion is whether the archetype's affordances express what ELIF actually does (decompose, validate, arbitrate, route, govern, build discovery pathways) or whether they hide or distort it.

### B1.1 Chatbot

**Verdict: ACTIVELY COUNTERPRODUCTIVE.**

CURRENT EVIDENCE. The alpha emits a frame-validation verdict, then a 2-axis decomposition, then schema-validated hypotheses with distinguishing predictions, then a stage-gated roadmap, then a refuse-verdict with named uncertainty sources. None of these outputs is a conversational turn. None of them benefits from being typed at by a user one message at a time. The closed-set vocabulary (`{valid, invalid, needs_decomposition}`) is structural, not conversational; a chatbot wrapper hides it under prose.

Worse, a chatbot framing imports the LLM affordance ELIF was designed to constrain: conversational fluency. The 0.83-similarity outputs in offline replay are structural, not stylistic — but a chatbot surface reframes them as "answers from an assistant," which re-imports sovereignty at the surface layer that the Articles refuse at the architecture layer (Article I, Article III). A user typing "what should I do about electroculture?" into ELIF-as-chatbot and receiving "Refuse the bundle pending decomposition into 2 axes…" experiences this as a failure of helpfulness rather than the correct governance verdict.

The chatbot archetype is the single largest UX risk for ELIF. It is the affordance the surrounding LLM market trains users to expect, and it is the affordance most directly incompatible with what the alpha proved the procedure does.

### B1.2 Dashboard

**Verdict: SUPPORTING role only; not the primary archetype.**

CURRENT EVIDENCE. A dashboard fits parts of the alpha output: the per-step status table in `case_01.2`, the per-component acceptance summary, the behavioral similarity score (0.83), the LLM-call cost per case ($0.21 live, $0.00 offline), the MemoryLogger event counts. These are tabular, refreshable, observation-shaped — exactly what dashboards do well.

But the dashboard archetype cannot host the LOAD-BEARING outputs: the frame-validation reasoning trace, the axis decomposition with families, the hypothesis set with distinguishing predictions, the stage-gated roadmap with continuation gates, the uncertainty-source enumeration. These are structured artifacts, not metrics; flattening them into KPI tiles strips exactly the structural detail that makes them defensible against Article I/III/IV.

A dashboard for run-state and cost-state is genuinely useful as a SECONDARY surface (monitoring throughput, cost burn, refuse-rate, MemoryLogger growth, Article VII capacity trends across cases). It is not the surface where the operator inhabits a case.

### B1.3 Decision room

**Verdict: LOAD-BEARING. Single closest fit to what the alpha actually does.**

CURRENT EVIDENCE. The case_01 input frame (a 5-year multi-actor electroculture pilot program with structured if-yes / if-no closure) IS a decision request. The alpha's Step 1 output ("the frame is needs_decomposition — refuse the bundle, decompose into mechanism-plausibility and reversibility axes") IS a decision-room verdict. Steps 2-9 walk through axis decomposition, assumption surfacing, hypothesis sets with distinguishing predictions, scale-bridging, outside-frame trajectory enumeration, stage-gated roadmap construction, and governance kernel arbitration — the structure of a multi-axis decision package.

The decision-room archetype expresses what Article V actually does (refusal as valid output), what Article VI does (decomposition must converge into arbitrated pathways), and what Article VII does (this decision's structure feeds future similar-shape decisions). It does NOT misrepresent the procedure as conversation or as generic analytics.

The decision-room framing also explicitly invites the operator-attention discipline the momentum-capture warning requires: a decision room is something you ENTER for a decision, then LEAVE. You do not live in it. The pausability constraint maps naturally onto room-entry / room-exit, not onto a chat thread or a dashboard that runs forever.

The risk: "decision room" implies a single decision per visit. ELIF's procedure produces a decision package — verdict + uncertainty + roadmap + memory — not a single yes/no. A naive decision-room UX could collapse this into "refuse / approve" buttons, losing the structural output. The mitigation is that the room's surface area is the package, not a button.

### B1.4 Laboratory

**Verdict: LOAD-BEARING for cross-case work. Secondary archetype, complementary to decision room.**

CURRENT EVIDENCE for per-case scope: weak. The alpha runs one case at a time and exits. There is no in-alpha behavior that resembles "experimentation": no parameter sweep, no A/B variant, no observation between attempts. Inside a single case, ELIF is not a laboratory; it is a structured arbitration.

PLAUSIBLE FUTURE for cross-case scope: load-bearing under Article VII. The capacity-vs-truth distinction (capacity accumulates across cases, truth does not) and the requirement that the MemoryLogger record judgment-acts, patterns engaged, and capacity-changes describe a longitudinal artifact that IS laboratory-shaped — a place where shapes from prior cases are re-encountered, tested, and (sometimes) deprecated. This becomes the natural surface for the Phase 5 compositional-arbitration question.

The decision-room and laboratory archetypes hybridize cleanly: each case is a decision room visit; the laboratory is the corridor of rooms, the cross-case memory substrate, the Article VII surface. The operator enters a room to arbitrate; returns to the laboratory to observe what shapes have accumulated.

SPECULATION (labeled): a multi-operator laboratory is genuinely premature. The constitutional layer is locked at single-operator non-self-propagation. Collective laboratory framings (capsules, multi-actor decision rooms) are deferred to Phase 5+ in `future_audit_ux_lived_environment.md` and remain deferred. This audit does not propose them.

### B1.5 Simulation workspace

**Verdict: ACTIVELY COUNTERPRODUCTIVE if framed as ELIF's surface.**

CURRENT EVIDENCE. ELIF does not simulate. The operator's hypothesis explicitly assigns simulation to world models, not to ELIF. The alpha's hypothesis_validator emits hypotheses with distinguishing predictions and fails-if conditions — these are simulation INPUTS for an external world model, not simulation outputs ELIF produces. The branching_roadmap_engine emits stage-gated continuation gates — these are EXPERIMENT GATES for external execution, not simulated outcomes.

A simulation workspace UX implies ELIF generates simulated futures the user explores. That misrepresents the four-organ separation the hypothesis asserts. ELIF's contribution is the STRUCTURE under which simulations would be evaluated, not the simulation itself.

PLAUSIBLE FUTURE (under Phase 6+ speculative): a simulation workspace could be the EXTERNAL surface where world-model outputs are received and then routed back into ELIF's hypothesis validator or governance kernel. In that framing, the workspace is the world-model's surface, not ELIF's. ELIF would be invoked from within it but not housed by it.

### B1.6 Map-based interface

**Verdict: SUPPORTING role for specific outputs; not the primary archetype.**

CURRENT EVIDENCE. Three alpha outputs are genuinely map-shaped:
- The Step 2 decomposition (2 axes × N families per axis): a 2D plane.
- The Step 7 outside-original-frame trajectories: a small set of branching paths.
- The Step 8 stage-gated roadmap: a directed graph with continuation gates as nodes.

A map view for these three artifacts adds real legibility — axis structure becomes spatial, trajectory branching becomes traceable, roadmap gates become inspectable. This is a SUPPORTING affordance inside the decision-room archetype, not a stand-alone product surface.

The risk is that a map UX implies a navigable, explorable territory. The alpha emits FIXED maps (one per Step), not navigable ones. A user who tries to "explore" the Step 2 decomposition outside the procedure is doing something the architecture does not support. The map view should render the procedure's outputs, not invite exploration of them.

### B1.7 Hybrid model — recommended

**Verdict: DECISION ROOM (primary) + LABORATORY (cross-case secondary) + map view + dashboard as embedded affordances.**

CURRENT EVIDENCE supports the primary (decision room): the alpha's per-case behavior is decision-package-shaped.
PLAUSIBLE FUTURE supports the secondary (laboratory): Article VII requires cross-case memory and capacity observation, which a laboratory archetype expresses without overreaching.
The map view and dashboard are AFFORDANCES inside these two archetypes, not separate archetypes.

The hybrid keeps ELIF's identity legible. It does not import LLM-product affordances (chatbot), it does not import simulation affordances (workspace), it does not import unbounded exploration affordances (free-form map). It expresses the five verbs (validate, arbitrate, govern, structure discovery, preserve corrigibility) directly through room-entry / package-output / memory-corridor.

Concrete operator-facing framing of the hybrid:
- The **case** is the unit of work.
- A case opens a **decision room**.
- The room hosts the 11-step procedure (mostly hidden) and surfaces the per-step structured output as inspectable panels (axis map, hypothesis table, roadmap graph, governance verdict, uncertainty list).
- Closing the room writes the case to the **laboratory**.
- The laboratory is the cross-case surface: a list of prior rooms, the patterns engaged, the capacity-change log, the deprecation events, the Article VII observables.
- The operator inhabits the laboratory between cases (paused state). The operator inhabits a room during a case (active state). The transition is explicit, observable, and pausable.

---

## B2. Media forms

Each media type is classified by what it expresses about the alpha's behavior and which Article / Step / four-pole failure mode it strengthens or undermines. The verdicts are intentionally firm.

| Media form | Classification | Tied to |
|---|---|---|
| Structured text | LOAD-BEARING | All 7 components emit structured JSON; the entire procedure is text-structured. |
| Decision maps | LOAD-BEARING | Step 2 axes + families; Step 9 verdict with uncertainty sources. |
| Dependency graphs | SUPPORTING | Cross-component data flow (Step 4→5; Step 7→8); useful for operator debugging, not for case output. |
| Scenario trees | LOAD-BEARING | Step 7 outside-original-frame trajectories; Step 8 stage-gated roadmap. |
| Timelines | SUPPORTING | Step 8 roadmap stages have ordering; MemoryLogger is append-only chronological. Useful but not load-bearing. |
| Simulations | ACTIVELY COUNTERPRODUCTIVE | Hypothesis owns the operator hypothesis: world models simulate; ELIF does not. Embedding simulations inside ELIF imports the affordance the four-organ separation forbids. |
| Audio briefings | DECORATIVE (and risky) | No alpha behavior is improved by audio. Audio of refusal verdicts is at best redundant, at worst fluency-inflating (Article I/III risk). |
| Video summaries | DECORATIVE (and risky) | Same as audio, with added engagement-loop risk (Phase 8 failure mode #36 institutional capture). |
| Laboratory mode | LOAD-BEARING (cross-case) | Article VII observable surface; MemoryLogger longitudinal view; capacity-vs-truth distinction made visible. |

### B2.1 Structured text — LOAD-BEARING

CURRENT EVIDENCE. The alpha emits structured JSON at every step. The schemas (5 tiers: input frame, step output envelope, Article VII, memory logger event, correction) enforce shape. The closed-set vocabularies (verdict ∈ {valid, invalid, needs_decomposition}, governance verdict ∈ closed set, event_types closed) are structural constraints, not stylistic choices. The structured text IS the deliverable; everything else in the UX is a rendering of it.

This means ELIF's primary "medium" is the structured object, not the rendered surface. A UX that hides the structure under prose is hiding the architecture's main contribution. The structured text must remain inspectable (operator can drill in), exportable (operator can take the artifact away), and signed (the MemoryLogger entry references the artifact by hash, per Article VII).

### B2.2 Decision maps — LOAD-BEARING

CURRENT EVIDENCE. The Step 2 decomposition output is a 2-axis × N-families-per-axis structure. Case_01 produces axes A/B/C + D/E (mechanism plausibility / reversibility profile). Case_02 produces reversibility + actor-incentive axes. Case_03 produces data-coupling-depth + infrastructure-persistence axes. These ARE maps: each axis is a dimension, each family is a region, each case-input becomes a located point.

A decision-map rendering of Step 2 is not decorative; it makes the axis discipline (>=2 distinct scales, >=2 families per axis, per semantic post-validation) operator-visible. It is the most direct rendering of Article III (decomposed reasoning) and Article IV (refuse collapsed objects). Without this rendering, the operator sees only JSON; with it, the operator sees what the procedure refused to collapse.

The Step 9 governance verdict + uncertainty-source list is also map-shaped (verdict at center, uncertainty sources radiating). Lower priority but consistent affordance.

### B2.3 Dependency graphs — SUPPORTING

CURRENT EVIDENCE. The component dependency graph from `elif_v0_1_alpha_cost_complexity_report.md` §3 is real: frame_validator → object_decomposer → hypothesis_validator → branching_roadmap_engine → governance_kernel → operative_truth_separator → memory_logger, with the orchestration_runner as the integration surface. This is useful for operator debugging, for understanding why Step 10 doesn't fire when Step 9 refuses, and for monitoring per-component LLM-call cost.

It is NOT load-bearing for case output. Operators consume the per-case decision package; they do not consume the dependency graph as part of the case. Reserve this rendering for operator-mode / debug-mode views, not for case-room main surface.

### B2.4 Scenario trees — LOAD-BEARING

CURRENT EVIDENCE. Step 7 mode A emits outside-original-frame trajectories (T1-T4 in case_01). Step 8 emits a stage-gated roadmap with continuation gates per stage. Both are scenario trees: branching, gated, partially ordered, refutable.

The tree rendering is load-bearing because it expresses the Article V / VI / VII tie: refusal at one branch is valid output; convergence into actionable pathways within finite cycles is required; pathways become reviewable material for future cases. None of this is visible in a flat list. A tree view is the only rendering that makes the "stage-gated" structure operator-inspectable as gating, not as sequence.

### B2.5 Timelines — SUPPORTING

CURRENT EVIDENCE. The Step 8 roadmap stages have order. The MemoryLogger is append-only chronological. A timeline view of the MemoryLogger is genuinely useful for the laboratory archetype (when did each case open / close, when did deprecation events fire, when did pattern-engagement count tick up).

It is not load-bearing per case because a single case's procedure executes in seconds-to-minutes; a per-case timeline adds nothing the dashboard or trace view doesn't. The cross-case timeline (laboratory surface) is more interesting — it expresses Article VII capacity-accumulation visibly.

Classification stands: SUPPORTING. Useful in the laboratory, redundant in the decision room.

### B2.6 Simulations — ACTIVELY COUNTERPRODUCTIVE

CURRENT EVIDENCE. The operator hypothesis is explicit: world models simulate; ELIF does not. The hypothesis_validator emits distinguishing_prediction and fails_if; the branching_roadmap_engine emits stage gates. These are simulation-design INPUTS for an external world model, not simulation outputs ELIF generates.

Embedding a simulation surface inside ELIF (interactive sliders, animated outcomes, "what if you change X" affordances) commits two errors: (1) it implies ELIF generates simulated futures, importing the affordance Article I refuses (sovereignty over context); (2) it imports the engagement loops the danger-audit in `future_audit_ux_lived_environment.md` flags as the failure mode most directly opposed to corrigibility.

PLAUSIBLE FUTURE (Phase 6+, speculative): an EXTERNAL simulation workspace receives ELIF's hypothesis/roadmap outputs and runs them in a world model. The handoff is unidirectional: ELIF emits, world model receives, world model returns reality contact, ELIF re-validates. The simulation is not ELIF's surface; it is the world model's surface. This is structural separation, not UX coupling.

### B2.7 Audio briefings — DECORATIVE (and risky)

CURRENT EVIDENCE. Nothing in the alpha output benefits from audio. A refuse-verdict with named uncertainty sources read aloud is at best redundant (the operator already reads it) and at worst fluency-inflating (the audio voice imports tone, confidence, authority that the structured output explicitly disowns). Article III (no self-validation) is violated when audio adds "trust me" warmth to a structured output that explicitly carries refutation conditions.

There is no Step / Article / failure mode that audio media strengthens. There is at least one (Article III) it weakens.

Classification: DECORATIVE if benign, ACTIVELY COUNTERPRODUCTIVE if the audio voice carries any authority signal. Default position: do not build.

### B2.8 Video summaries — DECORATIVE (and risky)

CURRENT EVIDENCE. Same logic as audio, with added engagement-loop risk. Video summaries of case verdicts invite share-ability, watch-time optimization, and external surface area that the momentum-capture warning explicitly flags as architecture risk. Failure mode #36 (institutional capture, Phase 8) and #37 (prestige accumulation, Phase 8) name the downstream consequences.

Classification: DECORATIVE. Do not build. The decision-room artifact is the deliverable; a video about the deliverable converts it into content marketing for itself.

### B2.9 Laboratory mode — LOAD-BEARING (cross-case)

CURRENT EVIDENCE for the substrate: the MemoryLogger writes open / step_committed / refutation / close events at append-only JSONL per case. The closed-set event_types and change_types are structural. Cross-case content (judgment_act / pattern_engaged / capacity_change) is the unrealized Step 11 capacity — pending refuse-halt adjudication.

PLAUSIBLE FUTURE under E.2 live replay: once Step 10 and Step 11 are exercised (whether under refuse-halt Position B or under non-refuse live cases), the laboratory mode becomes the operator-facing surface for Article VII observability. It shows: which patterns have been engaged across cases, which have been deprecated, time-to-arbitration trends, compositional-reuse references, deprecation events. This is the surface that makes "ELIF has accumulated capacity" empirically visible — and equally importantly, makes "ELIF has been accumulating TRUTH" empirically detectable as the failure mode it is.

The laboratory mode is LOAD-BEARING because Article VII is operationally meaningful only if its observables are inspectable. A non-rendered MemoryLogger satisfies the persistence requirement but not the longitudinal-observation requirement that distinguishes capacity-watching from prestige-accumulating.

---

## B3. User journey

The operator's straw-man journey:
> Question → Frame validation → Map → Tensions → Trajectories → Experiments → Decision pathways → Governance review

This is approximately the 11-step procedure with consolidations. The audit task is to compare it against the procedure honestly, name missing or redundant steps, ask whether procedure and journey should be the same, and propose the user-visible journey separately from the internal procedure.

### B3.1 Mapping the straw-man to the 11-step procedure

| Straw-man stage | Internal procedure mapping | Component owner |
|---|---|---|
| Question | input frame (case authoring) | (external; operator authors) |
| Frame validation | Step 1 + Step 3 + Step 7-modeB | frame_validator |
| Map | Step 2 + Step 6 (decomposition + multi-scale relations) | object_decomposer |
| Tensions | Step 4 + Step 5 (hypotheses + failure conditions) | hypothesis_validator |
| Trajectories | Step 7-modeA (outside-original-frame trajectories) | branching_roadmap_engine |
| Experiments | Step 8 (stage-gated roadmap with continuation gates) | branching_roadmap_engine |
| Decision pathways | Step 9 (governance kernel verdict + confidence + uncertainty) | governance_kernel |
| Governance review | Step 10 (operative-truth separation) + Step 11 (memory logger content) | operative_truth_separator + memory_logger |

The straw-man covers all 11 internal steps under 8 user-facing stages. Coverage is good. The naming has minor mismatches that matter.

### B3.2 Missing or under-named in the straw-man

**(a) Object Decomposition is hidden under "Map."**

CURRENT EVIDENCE. Step 2 is the most Article-IV-load-bearing step in the procedure (refuse collapsed heterogeneous objects). The straw-man's "Map" obscures this: a user might read "map" as topography rendering. The honest user-facing name is **Decomposition** or **Axis Decomposition**. "Map" can remain as the SUPPORTING rendering affordance (the decision map) but should not be the stage name.

**(b) Outside-Frame trajectories are conflated with "Trajectories."**

CURRENT EVIDENCE. Step 7 mode A specifically emits outside-original-frame trajectories — alternatives the original frame did not propose. The straw-man's "Trajectories" is ambiguous; a user might read it as "the trajectories the question implied." The honest user-facing name is **Outside-Frame Alternatives** or **BRE Trajectories** (where BRE = Branching Roadmap Engine, internal name not user-facing). Naming this precisely matters because it expresses Article II (frame humility) at the user surface: the trajectories shown are NOT what the question proposed; they are what the procedure surfaced as outside-frame possibilities.

**(c) Operative-Truth Separation is missing entirely from the straw-man.**

CURRENT EVIDENCE. Step 10's operative-truth separation is a distinct user-facing stage. It answers a question the user actually has at the end: "what can I act on now (operative) versus what is real but not actionable (theoretical)?" Folding Step 10 into "Governance review" hides the Article IV partiality-of-models commitment. The user-facing journey needs an explicit stage: **Operative / Theoretical Separation** or, more user-friendly, **What's Actionable Now**.

This is the same Step 10 / Step 11 refuse-halt issue surfaced in §3 of `elif_v0_1_what_remains.md`. The straw-man journey accidentally re-imports the runner's halt by omitting Step 10 from the user-facing surface. Whether the runner Position A or Position B resolves, the user-facing journey should still name the Step 10 contribution.

**(d) MemoryLogger / Capacity Recording is missing entirely from the straw-man.**

CURRENT EVIDENCE. Step 11 + MemoryLogger writes the longitudinal record that Article VII requires for observability. The user-facing journey should include a closure stage that says, explicitly, "this case has been recorded; pattern X was engaged; capacity change Y was logged." Without this, the user sees decision-pathways and governance-review but never sees the laboratory accumulating. Article VII becomes invisible to the user, which means the capacity-vs-truth distinction becomes invisible too.

The user-facing name: **Closure & Capacity Record** or **Case Closure**.

### B3.3 Redundant in the straw-man

**(a) "Decision pathways" and "Governance review" both refer to Step 9 + Step 10.**

CURRENT EVIDENCE. The governance_kernel emits the verdict + confidence + uncertainty (Step 9). The operative-truth separator emits the operative/theoretical split (Step 10). Calling the Step 9 output "decision pathways" and the Step 10 output "governance review" inverts the names: Step 9 IS governance, Step 10 is the actionable-pathway split.

Recommended user-facing rename: **Step 9 = Governance Verdict; Step 10 = Actionable / Theoretical Split.** This corrects the inversion and makes the journey legible.

### B3.4 Re-ordering

The internal procedure is sequentially gated by data dependencies. The user-facing journey can collapse some of these into single user-visible stages without changing internal order. Recommended user-facing sequence (8 stages over 11 internal steps):

1. **Question** (input frame authoring) — Step 0 (external)
2. **Frame Validation** — Steps 1, 3, 7-mode-B
3. **Axis Decomposition** — Steps 2, 6
4. **Hypothesis & Failure Conditions** — Steps 4, 5
5. **Outside-Frame Alternatives** — Step 7-mode-A
6. **Roadmap with Gates** — Step 8
7. **Governance Verdict** — Step 9
8. **Actionable / Theoretical Split + Case Closure** — Steps 10, 11

The internal procedure remains 11 steps; the user surface is 8 stages. This is the journey ELIF should present.

### B3.5 Procedure (internal) vs user journey (external) — should they be the same?

**No. They should not be the same. The procedure is 11 steps; the user journey is 8 stages.** Keeping them aligned 1:1 forces the user to learn the internal step structure, which exposes the implementation rather than the architecture's intent.

CURRENT EVIDENCE. The procedure has internal artifacts the user does not need to see directly: mode A vs mode B for Step 7, the runner's halt-code mapping (10 / 20 / 30), the closed-set assertion at orchestration_runner construction, the per-step semantic post-validation. These are correctness machinery, not user content. Exposing them inflates surface area and invites the user to fiddle with what they should not.

PLAUSIBLE FUTURE: the 8-stage user journey is a STABLE external contract. The internal 11-step procedure can compress (per `elif_constitutional_layer.md` iteration discipline: future revisions should bend toward compression). If v0.5 compresses to 9 internal steps, the user journey can remain 8 stages — the external contract holds. This decoupling is the discipline.

### B3.6 What the user journey must NOT do

The user journey must not invite re-execution loops ("try a different frame and see what happens"). The alpha is deterministic per fixture in offline mode and is bounded by cost-cap (22 LLM calls per case) in live mode. A UX that invites repeated re-runs imports the engagement-loop failure mode flagged in `future_audit_ux_lived_environment.md`. The journey is one-way through the stages with explicit close, not a sandbox.

The user journey must not collapse the refuse-verdict into a generic "failed" or "blocked" state. Refuse is the CORRECT verdict for all three alpha cases; exit_code 20 is success in the architectural sense. The UX must express refuse-as-valid-output (Article V) without coding refuse as failure. The user-facing language: **"Refuse the bundle pending decomposition / re-framing"** with the uncertainty sources surfaced as actionable next-steps, not as error messages.

---

## B4. Product roadmap

V1 / V2 / V3 surfaces tied to evidence gates, not calendar time. The doctrine constraint is non-expansionary: each version's minimum viable surface is the smallest surface that expresses the alpha's existing behavior; nothing is added speculatively.

### B4.1 V1 — Offline alpha surface (CURRENT EVIDENCE supports this version)

**Evidence prerequisite:** the v0.1 alpha replay verdict (`partially` at 0.83 structural similarity across 3 cases, schema-validated). This is the current state.

**Minimum viable surface:**
- A **case viewer** rendering the 3 alpha cases' structured outputs (Steps 1-9) as inspectable panels.
- A **decision-map rendering** for Step 2 (axes × families).
- A **scenario-tree rendering** for Step 7 + Step 8 (outside-frame trajectories, stage-gated roadmap).
- A **governance verdict panel** for Step 9 (verdict + confidence + uncertainty sources).
- A **refuse explainer**: when the verdict is refuse, the surface explicitly frames it as "this is the architecture's correct response," not as an error.
- A **MemoryLogger event timeline** showing the 14 events per case (open / per-step / refutation / close).
- A **per-case dashboard tile** in operator-mode showing: similarity score, LLM-call count, cost (offline = $0.00).

**What stays INTERNAL (hidden from user):**
- The 11-step procedure structure (presented as 8 stages externally).
- The runner halt-code mapping (10 / 20 / 30).
- The mode-A vs mode-B split inside Step 7.
- The closed-set vocabulary assertion at runner construction.
- The per-component LoC / dependency graph (operator-debug mode only).
- The schema versions, the fixture-mode flag, the cost-cap parameter.

**What stays USER-VISIBLE:**
- The 8 user-facing stages with their named outputs.
- The refuse verdict as a load-bearing result, not a failure.
- The uncertainty sources as actionable next-steps.
- The case closure including a "this is logged for cross-case observation" affirmation.

**What stays HIDDEN entirely (not even operator-debug):**
- Any narrative wrapper around the structured output (no LLM-prose summarization layer).
- Any "explain this verdict in plain language" affordance that re-imports the chatbot archetype.
- Any audio / video rendering of the case output.

**V1 cohort scope:** 3 alpha cases only. The decision-room archetype operates on each. The laboratory archetype is a placeholder (no cross-case observable yet, because Steps 10/11 don't fire in alpha refuse-path).

### B4.2 V2 — Live-replay-validated surface

**Evidence prerequisite:** E.2 live replay (just authorized by operator) executes successfully. This means:
- At least one of the 3 alpha cases produces an end-to-end live run with schema-validated outputs at Steps 1-9 matching offline replay structural behavior.
- The refuse-halt adjudication is resolved (Position A status-quo or Position B Step-10+11-on-refuse). The resolution is doctrinal, not architectural redesign.
- Live-mode cost holds within the projected $0.21/case envelope (or within reasonable drift).
- At least one case demonstrates Steps 10 and 11 firing under either non-refuse verdict (live case differs from offline fixture) or under Position B refuse-closure.

**Minimum viable surface, in addition to V1:**
- **Live case-run trigger**: operator can author a new input frame, submit, and observe the procedure run. Cost is displayed before and after.
- **Operative / Theoretical panel** for Step 10: rendering of operative list (act-on-now items) and theoretical list (real but not actionable items). With absence_log surfaced.
- **MemoryLogger content panel** for Step 11: judgment_acts, patterns engaged, capacity-changes. Surfaced as a closure record, not as analytics.
- **Refuse-closure surface**: when refuse is the verdict, the UX surfaces what was refused, the uncertainty sources, the operative list ("refuse the bundle"), and the theoretical list (uncertainty sources from Step 9). This is the UX expression of Position B (whichever doctrinal resolution is adopted, the surface should accommodate it).
- **Cost meter**: per-case LLM call count, cost burn against the per-case cap (22 calls), and per-cohort cost burn against a configurable budget.

**What becomes USER-VISIBLE in V2 that was hidden in V1:**
- The closure record (Step 11 content).
- The operative / theoretical split (Step 10 content).
- Live-mode cost.

**What stays HIDDEN even in V2:**
- The per-step structured output of intermediate retries (if any).
- The Anthropic API tool-call structured-output details.
- Any prompt-engineering surface (Article III; ELIF must not surface "tweak the prompt to fix the verdict").

**V2 cohort scope:** the 3 alpha cases live-replayed + any additional operator-authored cases. The laboratory archetype activates: cross-case observation is now possible because Step 11 capacity-change records exist.

### B4.3 V3 — Multi-case-generalization-confirmed surface

**Evidence prerequisite:** multi-case generalization confirmed. This means:
- At least 5-10 cases run live, including at least one non-Cluster-A/B/C case (a case shape NOT covered by case_01 electroculture / case_02 policy / case_03 operational).
- Article VII observables show measured capacity accumulation: time-to-arbitration trend (case N+1 ≤ case N for similar-shape problems), compositional-reuse frequency (case N references case N-1 structures), pattern-emergence rate, pattern-refutation rate.
- The MemoryLogger has accumulated enough cross-case content that the four-pole failure-mode taxonomy is exercised by at least one case at each pole (absolutization probed, false closure probed, fragmentation probed, sterile equilibrium probed).
- The procedure has not required architectural redesign for any of these cases.

**Minimum viable surface, in addition to V2:**
- **Laboratory mode primary surface**: the cross-case corridor view. Lists prior cases by shape-tag, surfaces compositional-reuse references, shows capacity-change trends, surfaces deprecation events.
- **Pattern panel**: each pattern engaged across cases, with engagement count, last-engaged timestamp, deprecation status. Pattern recognition is rendered as "shape recognized; INVITATION TO TEST" not as "answer."
- **Capacity-vs-truth observability panel**: explicit rendering of the distinction. The UI separates "ELIF can now do X faster / with more composition" (capacity, permitted) from any framing that would imply "ELIF knows X" (truth, forbidden). This is a structural UI commitment to Article VII.
- **Judgment-act log**: the operator-readable record of where rule-underdetermination triggered judgment, what was considered, what was chosen, and what consequences followed. This is the meta-reviewable surface of the thinking-reed (the "thinking" component of fragile-and-upright-and-thinking).
- **Sterile-equilibrium and fragmentation detector outputs**: surface the MemoryLogger's signature detectors as observability tiles in the laboratory. Not as alerts (no engagement-loop), but as inspectable signals.

**What becomes USER-VISIBLE in V3 that was hidden in V2:**
- Cross-case pattern engagement.
- Capacity-accumulation trends.
- Deprecation events (a pattern was deprecated because cases N+2, N+3 refuted it).
- Judgment-act records.

**What stays HIDDEN even in V3:**
- Any framing that converts pattern recognition into prediction or validation.
- Any aggregation framing that turns the laboratory into a "knowledge base" (truth-accumulation framing, forbidden).
- Any prestige surface (no leaderboard of patterns; no "most-engaged shape" trophy; the system must not have a hall of fame).

**V3 cohort scope:** 5-10+ cases, including out-of-cluster shapes. The decision-room archetype matures (the operator can enter a new case knowing what to expect from the room). The laboratory archetype is the primary inhabit-surface, with the decision room as the room you visit to do work.

### B4.4 What V1 / V2 / V3 do NOT include

The roadmap is non-expansionary. The following are NOT in V1/V2/V3 under this audit:
- Multi-operator collective ELIF surfaces (deferred per `future_audit_ux_lived_environment.md` revisit conditions).
- Capsule architecture as a UX primitive (same deferral).
- Industrial-vs-civilizational UX modes (same deferral).
- Audio / video media surfaces (DECORATIVE per B2).
- Simulation workspace inside ELIF (ACTIVELY COUNTERPRODUCTIVE per B2).
- Chatbot framing (ACTIVELY COUNTERPRODUCTIVE per B1).
- Free-form exploration affordances (re-run loops, prompt-tweaking surfaces).
- A "knowledge graph" of accumulated patterns (truth-accumulation framing).
- Public-facing surfaces (V1-V3 are operator-facing; public exposure deferred to a separate audit not in scope).
- Any cross-product integration that couples ELIF to the OSG pedagogical biome, the Media biome, or the Continuity layer at runtime. The four-organ separation and the constitutional non-self-propagation rule both forbid this at this phase.

### B4.5 Pausability test at each version

CURRENT EVIDENCE (V1): trivially pausable. The alpha is offline, fixture-driven, deterministic. The operator can close the laptop and return without state loss.

PLAUSIBLE FUTURE (V2): pausable if live-run state is per-case-bounded. A single case runs in ~20-50s live; the operator can pause between cases. Mid-case pausing requires a snapshot mechanism but is not load-bearing for V2.

PLAUSIBLE FUTURE (V3): pausable iff the laboratory surface remains stateless-read. The cross-case observability tiles must be derivable from the MemoryLogger JSONL on demand, not maintained as live state. If the laboratory surface starts requiring background processes to keep its tiles fresh, the architecture has captured itself (momentum-capture failure mode). The discipline is: the laboratory is a VIEW over append-only JSONL, not a live system.

This pausability check is the V3 maturity test, not just a UX preference. If the laboratory surface cannot be left for weeks and re-entered without state-rebuild, V3 has over-coupled to its own execution.

---

## Operator decisions queued

These decisions are surfaced for the operator. The audit does not adopt or recommend; it makes the choices explicit.

1. **Adopt the decision-room + laboratory hybrid as the V1 archetype framing?** Per B1.7, this is the UX framing most aligned with the alpha's behavior and the operator's five-verb hypothesis (validate, arbitrate, govern, structure discovery, preserve corrigibility). Alternative is to defer all UX commitment until V2 live-replay evidence.

2. **Resolve the Step 10 / Step 11 refuse-halt question** (carried forward from `elif_v0_1_what_remains.md` §3 and `elif_v0_1_alpha_replay_report.md` operator-decision-points). Position A (status quo halt) or Position B (run Step 10/11 even on refuse for closure recording). The user journey B3 assumes Position B is consistent with the user-facing journey including a closure stage; under Position A, the user-facing closure stage records the refusal event only via the `refutation` event type (which the MemoryLogger already writes). Either resolution works for V1; V2 design depends on the resolution.

3. **Rename user-facing stages per B3.2:** "Map" → "Axis Decomposition"; "Trajectories" → "Outside-Frame Alternatives"; "Decision pathways" → "Governance Verdict"; "Governance review" → "Actionable / Theoretical Split + Case Closure". Or keep operator's straw-man names. Audit recommends the renames because they preserve Article-level legibility; operator may decline.

4. **Confirm the V1 surface scope** (B4.1): case viewer + decision map + scenario tree + governance panel + refuse-explainer + MemoryLogger timeline + operator dashboard. The scope is deliberately small. Operator may want to expand or contract; the audit's position is no expansion before E.2 live replay produces evidence.

5. **Confirm media-form classifications** (B2): structured text + decision maps + scenario trees + laboratory mode as load-bearing; audio + video as decorative-and-risky. Operator may overrule any classification; the audit's firm position is that audio/video should not be built in V1-V3.

6. **Confirm non-expansion zones** (B4.4): no chatbot framing, no simulation workspace inside ELIF, no multi-operator surfaces, no capsule architecture, no public exposure, no cross-product runtime coupling. Operator may overrule any of these; the audit's firm position is each is incompatible with the constitutional layer at this phase.

7. **Adopt the pausability test as a V3 architectural commitment** (B4.5): laboratory surface must be a stateless read over MemoryLogger JSONL, not a live-state system. Or accept that V3 may import live-state coupling. The audit's firm position is the pausability test is the V3 maturity test, not optional.

---

## What this audit does NOT recommend

This section is load-bearing. The non-expansion stance is the operator's discipline applied to a UX investigation specifically, and it must be explicit.

1. **No new ELIF components.** The 7 components survived implementation pressure intact. Adding an 8th was already rejected at Step 8 §1 Q3.1 and stays rejected. No UX requirement in this audit creates pressure for a new component. The decision-map rendering is a renderer, not a component. The laboratory surface is a renderer over MemoryLogger, not a component.

2. **No new Articles.** The constitutional layer is locked at v0.4 with seven Articles and a four-pole failure-mode taxonomy. The iteration discipline is compression, not addition. No UX archetype in this audit requires a new Article; each was tied back to existing Articles.

3. **No new procedure steps.** The 11-step procedure is the procedure. The 8-stage user journey is a presentation layer over it. The presentation does not modify the procedure; the procedure does not need new steps to support the presentation.

4. **No chatbot, no LLM-prose summarization layer, no "explain this in plain language" affordance.** All three re-import the affordance Article I refuses (sovereignty over context) at the surface layer. The structured output IS the deliverable. Wrapping it in prose hides the architecture's contribution.

5. **No audio briefings, no video summaries.** Both are DECORATIVE at best and engagement-loop risks at worst. Failure mode #36 (institutional capture) and #37 (prestige accumulation) name the downstream consequences. Do not build.

6. **No simulation workspace inside ELIF.** Simulation is the world-model's affordance per the operator's hypothesis. Importing it inside ELIF imports the four-organ-violation it is forbidden to make.

7. **No multi-operator UX, no capsules, no industrial-vs-civilizational scaling surfaces.** These are deferred per the existing `future_audit_ux_lived_environment.md` revisit conditions (Phase 4-5+ at earliest, post-multi-case-evidence). This audit does not revoke that deferral.

8. **No re-execution loops, no "tweak the prompt" affordances, no free-form exploration sandbox.** The procedure is bounded; the cost-cap is structural; the engagement-loop affordance is the failure mode `momentum_capture_warning.md` warns against. The UX must invite case authoring, package consumption, and case closure — not repeated re-runs of the same case.

9. **No public-facing surfaces at V1-V3.** ELIF is operator-facing. Any public surface re-imports failure modes (engagement, prestige, institutional capture) that the constitutional layer was designed to resist. Public surface decisions are a separate audit not in scope.

10. **No cross-product runtime coupling.** ELIF does not integrate with the OSG pedagogical biome, the Media biome, or the Continuity layer at runtime. The four-organ separation and the non-self-propagation rule both forbid this. Cross-product DOCTRINAL learnings flow freely; runtime coupling does not.

11. **No knowledge-graph of accumulated patterns, no "what ELIF has learned" surface.** This is truth-accumulation framing. Article VII forbids it. The laboratory surface renders capacity (what ELIF can now do faster / with composition) and never truth (what ELIF knows). The UI commitment to this distinction is structural, not stylistic.

12. **No background processes maintaining laboratory state.** The laboratory is a VIEW over append-only JSONL, derivable on demand. Background processes maintaining live laboratory state are the pausability-failure mode; if the laboratory cannot be left for weeks and re-entered without rebuild, the architecture has over-coupled to its own execution.

---

## Coda

The alpha proves a small thing precisely: 7 components and 11 steps reproduce 0.83 of operator-authored reference structural behavior across three cases under offline replay, with refuse as the architecturally-correct verdict in all three. The UX positioning that respects this evidence is small and precise: a decision-room archetype where each case is entered, arbitrated, and closed, sitting inside a laboratory corridor where capacity (not truth) accumulates across cases. The structured output is the deliverable. The refuse verdict is success. The MemoryLogger is a substrate, not a feature. The procedure is hidden under an 8-stage journey, but the journey expresses the architecture rather than disguising it.

Everything else this audit could have proposed — capsules, simulation workspaces, audio summaries, multi-operator rooms, knowledge graphs, public dashboards — is either DECORATIVE or ACTIVELY COUNTERPRODUCTIVE under current evidence. The discipline is to refuse them until evidence forces a different answer. E.2 live replay is the next evidence gate. Until it runs, V2 stays a sketch.
