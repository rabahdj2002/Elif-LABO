# ELIF-Mode Procedure v1.0

**Status:** LOCKED 2026-05-28. Supersedes v0.1.
**Lock authority:** operator approval of TBD-fills and Step 12 (post-case Memory Logger entry).
**Purpose:** ELIF-mode is a *specifiable procedure*, not a mindset. The procedure must be executable by an operator following written steps, without "thinking like ELIF."

---

## Locking decisions (what changed from v0.1)

1. All six TBD validation rules and rejection criteria filled with **structural rules** (form / falsifiability), not prescriptive rules (content).
2. New **Step 12 — post-case Memory Logger entry** added so Article VII (capacity accumulation) becomes measurable within Phase 1 rather than only at longitudinal aggregate.
3. Execution discipline extended with **time-box rule** per step to prevent infinite refinement of any single step.
4. Steps 3, 6, 7 remain B-tagged (candidate components) pending case 2/3 evidence — provisional classification documented in `step_to_component_mapping_audit_v1_0.md`.

---

## Procedure steps (LOCKED)

| # | Step | Required output | Validation rule (structural) | Rejection criteria | A/B/C/D tag | Canonical mapping |
|---|---|---|---|---|---|---|
| 1 | Frame validation | One of three forms: `valid` / `invalid` / `needs decomposition` + reformulated frame if not `valid` | Output must take exactly one of the three forms. If `invalid` or `needs decomposition`, output must include a reformulated frame. | Outputs lacking the three-form taxonomy; `invalid` without reformulation. | A | Frame Validator |
| 2 | Object decomposition | ≥2 distinct object families with named decomposition rationale | Decomposition must produce ≥2 distinct families AND name the rationale for the partition. | <2 families; partition without rationale. | A | Object Decomposer |
| 3 | Hidden assumption extraction | Enumerated assumptions list (≥2 entries) | Assumptions enumerated (numbered/bulleted), each a declarative statement (not a question), ≥2 entries. | Prose-only "things to consider"; question-form entries; <2 entries. | B | Provisional: Frame Validator sub-behavior |
| 4 | Predictive hypothesis construction | Hypotheses with distinguishing predictions | Each hypothesis must contain ≥1 distinguishable prediction (an observation that would discriminate it from alternatives). | "Concerns" without predictions; predictions that match all alternatives. | A | Hypothesis Validator |
| 5 | Failure condition enforcement | Falsifiability statement per hypothesis | Each hypothesis must include ≥1 explicit failure condition (an observation that would refute it). | Hypotheses without failure conditions; failure conditions that are vacuous (cannot be observed). | A | Hypothesis Validator (folded) |
| 6 | Multi-scale mapping | Mapping across ≥2 explicitly named scales with ≥1 cross-scale relation | ≥2 distinct scales named explicitly (e.g., molecular / cellular / organism / ecosystem / population / temporal-horizon) AND ≥1 stated relation across them. | Single-scale outputs; scales named but unrelated; cross-scale relation present but scales unnamed. | B | Provisional: Object Decomposer sub-behavior (scale-axis) |
| 7 | Exploration beyond framing | ≥1 trajectory tagged `outside-original-frame` with one-line reason | ≥1 trajectory must be explicitly tagged `outside-original-frame` with a one-line reason for the tag. | Outputs that only refine the original frame; outputs that wander without naming the wander. | B | Provisional: Branching Roadmap Engine sub-behavior |
| 8 | Branching roadmap generation | Stages with continuation gates | Every roadmap stage must contain ≥1 continuation gate (an explicit condition for proceeding to the next stage). | Roadmaps without gates; gates without testable conditions. | A | Branching Roadmap Engine |
| 9 | Governance kernel application | Constrain / refuse / explicitly abstain | Governance outputs must do one of: constrain, refuse, or explicitly abstain. | Governance outputs that only annotate; outputs that are silent on governance. | A | Governance Kernel |
| 10 | Operative vs theoretical truth separation | Explicit separation, OR explicit "not present, because…" | Operative and theoretical strands must be distinguishable. Absence of one strand must be logged with reason. | Outputs where the two strands are merged (not distinguishable); absences without logged reason. | A | Operative Truth Separator |
| 11 | Recommendation + confidence + unresolved uncertainty | Structured output packet | All three fields present (recommendation, confidence, unresolved-uncertainty source). Confidence must be tied to a corresponding unresolved-uncertainty source. | Outputs missing any of the three fields; confidence asserted without a corresponding unresolved-uncertainty source. | C | Procedural artifact |
| **12** | **Post-case Memory Logger entry** | **≥1 entry across {capacity-change observed / pattern engaged / pattern deprecated / judgment-act witnessed}** | **Each entry must be a declarative statement with ≥1 line-ref into the case's Condition C output.** | **Empty Step 12; entries without line-refs; entries that only restate Condition C output without naming what category they fall under.** | **A** | **Feedback / Memory Logger** |

---

## Execution discipline (LOCKED)

- **No improvisation.** If a step's output feels wrong, that is benchmark data, not a signal to adapt the step.
- **No hidden adaptation.** Changes to the procedure during a benchmark invalidate the benchmark.
- **No ontology injection beyond the written procedure.**
- **Time-box per step.** E1 max-duration per step: 15 minutes. If a step exceeds its time-box, the output as-of-the-bound is what gets recorded; the next step begins. Time-box overruns are themselves benchmark data (logged in Step 12 if recurrent).

---

## Execution phases

- **E1:** Founder-executed mechanical procedure (current).
- **E2:** Third-party procedural execution (mandatory gate before contract pack). Tightened time-box: 10 min/step.
- **E3:** Prototype-assisted execution (post-architecture decision).

Only after E2 succeeds does the architecture phase begin.

---

## What this procedure does NOT do

- Does not specify *how* to perform each step (intentionally — the operator's execution is itself the benchmark variable across E1/E2/E3).
- Does not force specific content shapes (validation rules check form, not answer).
- Does not pre-decide whether B-tagged steps (3, 6, 7) graduate to A or collapse — that is decided post-case-2-and-3 in the reclassification step.

---

## Cross-references

- `procedure/abcd_classification_system.md` — A/B/C/D tag semantics.
- `procedure/benchmark_template.md` — output-capture template per case (v1.0).
- `procedure/step_to_component_mapping_audit_v1_0.md` — pre-case mapping audit (Step 3 of the locked 8-step Phase 1 sequence).
- `procedure/phase_gates.md` — operational phase gates.
- `doctrine/06_constitutional_layer_v0_4.md` — constitutional anchor; component definitions.
- `benchmarks/article_vii_capacity_accumulation_tracking.md` — Step 12 destination.
