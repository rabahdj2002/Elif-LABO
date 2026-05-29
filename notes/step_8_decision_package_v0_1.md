# Step 8 — Decision Package v0.1: What ELIF actually is

**Status:** v0.1 decision package, 2026-05-29. Anchored to `results/step_8_architecture_decision.md` (LOCKED 2026-05-28).
**Scope:** decide what ELIF v0.1 actually IS — buildable specification, not further validation.
**Operator question this package answers:** *"The goal is no longer validation. The goal is deciding what ELIF actually is."*

---

## 1. Smallest buildable ELIF v0.1 (one paragraph)

**ELIF v0.1 is a structured 11-step reasoning procedure operated against the Constitutional Layer v0.4, executed by a frontier LLM under a thin orchestration layer that handles per-case state, Article VII capacity tracking, and Memory Logger persistence. The 7 canonical components are owners-of-steps, not separate microservices. Compression evidence from three cases (electroculture / autonomous agriculture / mental-health infrastructure) shows the architecture concentrates signal at ~51% of expansion in 5 step-positions; the rest is supporting structure. Architecturally, v0.1 is one Python package + one Markdown procedure document + per-case JSONL state files. No service, no UI, no inter-component messaging.**

That is the floor. Anything below it gives up an evidence-supported signal; anything above it adds without architecture-forcing evidence.

---

## 2. Indispensable components (the 7)

These survived three-case pressure with 3/3 engagement and no demotion candidate per `results/step_6_cross_case_analysis.md`. **Removing any one collapses ELIF's signal.**

| # | Component | Why indispensable | Built as |
|---|---|---|---|
| 1 | Frame Validator | Article II tie; Step 1 valid/invalid/needs-decomp verdict; sub-behaviors Step 3 (assumption surfacing) + Step 7 deeper-frame-rejection | system-prompt module + structured output schema |
| 2 | Object Decomposer | Article IV tie; Step 2 family decomposition + Step 6 multi-scale sub-behavior | system-prompt module + structured output schema |
| 3 | Hypothesis Validator | Articles I, III tie; Steps 4-5 (hypotheses + failure conditions); strongest signal-per-cost | system-prompt module + structured output schema |
| 4 | Branching Roadmap Engine | Articles V, VI, VII; Steps 7 (BRE-feed) + 8 (stage-gated roadmap) | system-prompt module + structured output schema |
| 5 | Governance Kernel | Articles V, VI, VII; Step 9 verdict + confidence + unresolved-uncertainty (Step 11 absorbed) | system-prompt module + structured output schema |
| 6 | Operative Truth Separator | Article IV tie; Step 10 operative vs theoretical | system-prompt module + structured output schema |
| 7 | Feedback / Memory Logger | Article VII (primary); Step 11 capture (renumbered from Step 12) | **architecture-dependent** — persistent JSONL writer + cross-case reuse-count tracker |

**Count: 7 indispensable. None merge, none remove.** Step 8 §1 explicitly rejected adding an 8th component.

---

## 3. Mergeable components

**Zero further merges in v0.1.** Step 8 already executed the single eligible merge (Step 11 → Step 9 output-shape extension; 12 steps → 11 steps).

Two investigation items defer further merges to Phase 2 evidence (not v0.1):

| Q-ID | Potential merge | Why deferred |
|---|---|---|
| Q3.3 | Step 3 (assumption surfacing) ↔ Step 9 (uncertainty annotation) | Overlap not yet observable until v1.1 procedure executes in Phase 2 |
| Q6.3 | Step 6 (multi-scale) self-disable on naturally single-scale content | Requires a single-scale case (not yet authored) |

**Decision:** v0.1 ships with 11 distinct steps. Further merge candidates wait for Phase 2.

---

## 4. Removable components

**Zero components removable in v0.1.** No A→D demotion candidate surfaced in three cases per Step 6 §3.1. Step 8 §1 confirms zero removals.

The "remove if compression evidence forces it" gate is open in principle (Phase 2 constitutional compression evaluation) but **no removal is evidence-supported today**.

---

## 5. Deferred components (intentionally NOT in v0.1)

These were considered and consciously deferred per `notes/current_state.md` deferred-audit register + `notes/long_range_roadmap_v0_1.md`:

| Deferred | Earliest revisit phase | Why |
|---|---|---|
| World-model integration (schemas, registry, connectors, arbitration) | Post Phase 1 (Phase 6 territory) | Phase 6 territory; would author architecture before evidence forces it |
| UX / lived environment / ELIF Capsules / collective dynamics | Post Phase 4-5 | Emotionally compelling framing requires case evidence first; non-self-propagation constraint |
| Continuity Layer (pedagogical sublayer, silence-default, 10 Articles, 12 observers) | C-α rollout window | OSG memory `continuity_layer_doctrine.md` — separate doctrine, NOT a v0.1 component |
| Memory Corridor (multi-conversation continuity) | Beyond Continuity Layer | Defer-of-deferral; not v0.1 |
| Article VII visualization / external API / shared state | Post Phase 4 | Architecture-dependent surface that needs evidence accumulation first |
| Procedure v1.1 execution (compressed 11-step) | Phase 2 entry act | Compression preserves signal claim is unverified until v1.1 runs |
| Cross-LLM-family validation (currently single-model E1.5) | Phase 3-4 | Procedure portability is unproven |
| 8th component (Assumption Surfacer / Cross-Scale Relator) | Permanently rejected unless 3/3 + architecturally absent | Step 8 §1 Q3.1 + Q6.1 |

**Pattern:** v0.1 deliberately ships LESS than the long-range roadmap envisions. Each deferral is reviewable; none are dead — the non-self-propagation constraint keeps them dormant until evidence pulls them active.

---

## 6. Architecture-dependent behaviors (require code, not portable to prompt-only)

These require persistent state, cross-case composition, or audit-trail discipline that a stateless prompt cannot deliver:

| Behavior | Why architecture-dependent | v0.1 implementation surface |
|---|---|---|
| Memory Logger persistence | Cross-case state survives session end; reuse counts accumulate | JSONL append-only files per case + index |
| Article VII capacity tracking | `prior_structures_referenced`, `reuse_count_total`, `patterns_recognized`, `time_delta_vs_prior_similar` — all multi-case | Per-case `article_vii_tracking.json` + cross-case aggregator |
| Procedure orchestration | Step ordering, sequential output commit (no revision), time-box enforcement | Thin Python runner with step-by-step state machine |
| Audit trail | Every step output captured + linked to procedure version + execution phase | Per-case directory under `results/case_NN/` with conditioned outputs + meta |
| ABCD classification operation | A/B/C/D tags per behavior tracked across cases for reclassification | Aggregator over case results |
| Reuse detection (compositional pattern reuse) | Cross-case reuse_kind=composed annotation requires prior-case awareness | Memory Logger sub-routine |
| Procedure-version pinning | `procedure_version_used` field per case (v1.0 vs v1.1) | Schema-enforced JSON field + benchmark template binding |

**Total architecture-dependent surface area:** ~7 distinct behaviors. **All map to the Memory Logger component + the procedure-runner orchestrator.** No other component is architecture-dependent in v0.1.

---

## 7. Prompting-portable behaviors (encodeable as system prompt + structured output)

These can be delivered by a frontier LLM under a structured system prompt without bespoke code, given the architecture-dependent surface above is in place:

| Behavior | Procedure step(s) | Portability rationale |
|---|---|---|
| Frame validation verdict | Step 1 | Single-shot judgment with closed-set output (valid / invalid / needs decomposition + reformulated frame) |
| Hidden assumption enumeration | Step 3 (sub-behavior of Step 1) | Declarative form output; deterministic structure |
| Family-axis decomposition | Step 2 | Structured tree output |
| Multi-scale relations | Step 6 (sub-behavior of Step 2) | Structured pairs + cross-scale relations list |
| Hypotheses with distinguishing predictions | Step 4 | Closed-set output shape |
| Failure conditions per hypothesis | Step 5 | One-per-hypothesis structured output |
| Outside-frame trajectories | Step 7 BRE-feed | Trajectory list |
| Deeper-frame-rejection trajectories | Step 7 Article II side | Structured frame-rejection record |
| Stage-gated roadmap | Step 8 | Structured stage list |
| Governance verdict + confidence + uncertainty | Step 9 | Structured output (verdict, confidence_value, unresolved_uncertainty_sources[]) |
| Operative vs theoretical separation | Step 10 | Two-bucket output |

**Total prompt-portable surface area:** 10 of 11 procedure steps (everything except Step 11 Memory Logger entry, which is architecture).

**Implication:** v0.1 can be built as a **thin orchestration layer** (~500-1000 lines Python) calling a frontier LLM with carefully-engineered system prompts per component. No custom ML, no fine-tuning, no embedding store, no graph database.

---

## 8. Expected engineering scope + risk

### 8.1 Scope estimate

| Layer | Component count | Engineering days |
|---|---|---|
| Memory Logger (persistence + Article VII tracker + reuse detector) | 1 module | 2-3 days |
| Procedure runner (step orchestration + state machine + time-box) | 1 module | 2 days |
| Per-component system prompts (7 prompts, each Step 6 §6.2 evidence-grounded) | 7 modules | 3-4 days |
| Per-case state file schema + writer + reader | 1 module | 1 day |
| ABCD aggregator (cross-case differentiator tracking) | 1 module | 1 day |
| CLI runner (`elif run --case <id> --condition <a|b|c>`) | 1 entry-point | 0.5 day |
| Tests (synthetic case inputs; closed-set output validation; cross-case reuse detection) | 1 test suite | 2 days |
| Documentation alignment (sync to procedure v1.0; procedure v1.1 follow-on) | — | 1 day |

**Total: ~12-14 engineering days for shippable v0.1.** This is the smallest disposition that preserves three-case signal.

### 8.2 Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Procedure v1.1 (11-step compressed) fails to preserve signal in execution | medium | medium | Run a single case under v1.1 as Phase 2 entry act; abort compression if signal degrades; revert to v1.0 |
| Memory Logger reuse-detection false-positives (pattern over-attribution) | medium | low | Article VII schema requires explicit refutation_conditions per pattern; cross-case validation gate before any pattern promotes |
| Single-model E1.5 results don't generalize across LLM families | high | medium | Documented disclosure in every case's condition outputs; cross-LLM-family validation deferred to Phase 3-4 (already in roadmap) |
| Operator authors a single-scale case that breaks Step 6 ceremony | low | low | Q6.3 deferred; Step 6 can self-disable per operator judgment per case |
| Constitutional pressure (Phase 2 v0.5 candidate) collapses the design | low | high | v0.4 LOCKED status + non-self-propagation constraint; compression is permitted, expansion is not |
| Architecture-dependent surface bleeds into prompt-portable steps under runtime pressure | medium | medium | Per-step closed-set output schema enforced; any step's output that requires cross-case knowledge raises an error rather than silently consuming state |
| Cross-machine continuity gap (laptop ↔ VM) | low | medium | This is OSG's concern (handoff doc); ELIF v0.1 is single-machine until separately addressed |
| Component growth pressure from compelling Phase 2-3 cases | medium | high | Q3.1 + Q6.1 "no 8th component" precedent + locked-rule "no component survives by prestige" applied to additions symmetrically |

### 8.3 Scope explicitly OUT of v0.1

- No web UI
- No external API
- No multi-conversation continuity (Memory Corridor is deferred)
- No Continuity Layer (separate doctrine; not part of ELIF v0.1)
- No cross-LLM-family adapters (single-model E1.5 baseline only)
- No real-time observation (cases run discretely; no streaming)
- No collaboration / multi-operator coordination
- No World-Model integration of any kind
- No ELIF Capsules / UX layer
- No procedure v1.1 execution (Phase 2 entry act)
- No constitutional v0.5 compression (Phase 2 evaluation gate)
- No external benchmark integration (the 3-case benchmark template is ELIF-internal)

These exclusions are explicit — they prevent inflation of "v0.1" beyond what evidence supports.

---

## 9. The decision in one sentence

**ELIF v0.1 is: 7 system-prompt components (10 prompt-portable behaviors) + 1 architecture-dependent Memory Logger + 1 procedure-orchestration runner + 11-step compressed procedure + Constitutional Layer v0.4, totaling ~12-14 engineering days for a buildable shippable single-machine reasoning procedure with audit trail.**

Anything smaller gives up evidence-supported signal. Anything larger requires Phase 2+ evidence not yet on hand.

---

## 10. What happens after v0.1 ships

Per `notes/long_range_roadmap_v0_1.md` (corrigible, deprecatable):

- **Phase 2 entry act:** run a case under procedure v1.1 (the 11-step compressed). If signal preserves, v1.1 supersedes v1.0. If signal degrades, v1.1 is rejected and v1.0 remains.
- **Phase 2 substance:** constitutional compression evaluation. v0.4 → v0.5 candidate. Compression trajectory only; no expansion.
- **Phase 3-4:** cross-LLM-family validation; first ELIF Capsules consideration (DEFERRED).
- **Phase 5+:** World-Model integration consideration (DEFERRED).
- **Phase 6+:** AGORIA / ORC coordination consideration (DEFERRED).

None of Phase 2+ is in v0.1 scope. v0.1 is what ELIF actually IS today, based on what survived three-case compression.

---

## 11. Cross-references

- `results/step_8_architecture_decision.md` — full architectural decision basis
- `results/step_6_cross_case_analysis.md` — evidence base
- `results/step_7_reclassification.md` — 13 forwarded points + ABCD verdicts
- `procedure/elif_mode_procedure_v1.0.md` — locked execution procedure (v0.1 baseline)
- `doctrine/06_constitutional_layer_v0_4.md` — constitutional anchor
- `doctrine/02_locked_rules.md` — no component survives by prestige
- `notes/long_range_roadmap_v0_1.md` — Phase 2+ projections (deferred work)
- `notes/current_state.md` — operational snapshot (synced 2026-05-29 to audited reality)

---

## 12. Approval-required next step

This decision package proposes v0.1 = the smallest-real-ELIF specification above. **Operator approval converts this from proposal to v0.1 build authorization.**

If approved:
1. Create `src/elif_v0_1/` Python package skeleton (one directory)
2. Author the 7 component system prompts (one file each)
3. Implement Memory Logger + procedure runner (architecture-dependent layer)
4. Wire CLI entry point
5. Run procedure v1.1 entry-act case (Phase 2 entry)

If rejected: this proposal joins the deferred-audit register and Phase 0 stabilization extends until a different v0.1 disposition is decided.

**No build proceeds without explicit operator authorization.** Non-self-propagation constraint applies.
