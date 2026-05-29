# Step-to-Component Mapping Audit v1.0

**Status:** LOCKED 2026-05-28. Pre-case audit for Phase 1 benchmark.
**Purpose:** Tag each procedure step (v1.0) against the 7 canonical components defined in `doctrine/06_constitutional_layer_v0_4.md`. Surface mismatches **before** case 02 runs so post-case reclassification cannot be retrofitted to whatever ELIF actually produced.

**Operator refinement honored:** each non-mapped behavior is classified as one of:

- **implicit sub-behavior** of an existing component
- **candidate new component**
- **procedural artifact** (not architecture-worthy)

Final classification is gated on case 2/3 evidence. This document records the **provisional** mapping and the evidence required to confirm or upgrade each.

---

## Audit summary

| Procedure step | Canonical component | Status | Confirmation criterion |
|---|---|---|---|
| 1. Frame validation | Frame Validator | clean-mapped (A) | — |
| 2. Object decomposition | Object Decomposer | clean-mapped (A) | — |
| 3. Hidden assumption extraction | (none) | **provisional sub-behavior of Frame Validator** (B) | See §3.1 |
| 4. Predictive hypothesis construction | Hypothesis Validator | clean-mapped (A) | — |
| 5. Failure condition enforcement | Hypothesis Validator (folded) | clean-mapped (A) | — |
| 6. Multi-scale mapping | (none) | **provisional sub-behavior of Object Decomposer** (B) | See §3.2 |
| 7. Exploration beyond framing | (none) | **provisional sub-behavior of Branching Roadmap Engine** (B) | See §3.3 |
| 8. Branching roadmap generation | Branching Roadmap Engine | clean-mapped (A) | — |
| 9. Governance kernel application | Governance Kernel | clean-mapped (A) | — |
| 10. Operative vs theoretical separation | Operative Truth Separator | clean-mapped (A) | — |
| 11. Recommendation + confidence + unresolved uncertainty | (output shape) | **procedural artifact** (C) | See §4 |
| 12. Post-case Memory Logger entry | Feedback / Memory Logger | clean-mapped (A) | — |

**Mapping inventory:**
- 7 of 12 steps clean-A mapped to 6 canonical components (Hypothesis Validator covers steps 4 + 5).
- 3 of 12 steps provisionally B-mapped to existing components, pending case evidence.
- 1 of 12 steps procedural artifact (C).
- 1 of 12 steps clean-A mapped to Memory Logger (Step 12, added in v1.0 lock).
- 7 of 7 canonical components have at least one procedure step mapped to them.

---

## §3 — Provisional classifications for B-tagged steps

### §3.1 Step 3 — Hidden assumption extraction

**Provisional classification:** implicit sub-behavior of Frame Validator.

**Reasoning:** Frame validation is structurally incomplete without surfacing the assumptions the frame embeds. Article II (Frame Humility) implies the Frame Validator must interrogate not only the frame's surface shape but the assumptions that make the frame possible. Step 3 is therefore the assumption-surfacing operation that Frame Validator performs after Step 1's three-form taxonomy is selected.

**Why it is currently a separate step rather than folded into Step 1:** the operator may not naturally interrogate assumptions when validating a frame's three-form classification. Separating the step keeps the procedure executable without ELIF-background — the operator does not need to know that assumption-extraction is "part of Frame Validator," only that Step 3 must produce ≥2 enumerated declarative assumptions.

**Confirmation criteria (post-cases 2-3):**

- If Step 3 produces material the Frame Validator (Step 1) does not — i.e., assumptions that change the validity verdict retroactively — Step 3 graduates to candidate component status.
- If Step 1 outputs in cases 2-3 already contain assumption-surfacing material in their reformulated frames, Step 3 collapses into Step 1 (no separate component).
- If Step 3 produces material identical in shape across all three cases and uncorrelated with validity outcomes, Step 3 demotes to procedural artifact.

### §3.2 Step 6 — Multi-scale mapping

**Provisional classification:** implicit sub-behavior of Object Decomposer (scale-axis decomposition).

**Reasoning:** Scale is one decomposition axis among many. Step 2 (Object Decomposer) requires ≥2 distinct object families with named decomposition rationale. If the rationale is "scale-axis," Step 6 is operationally what Step 2 already produces. Step 6 exists as a separate step in v1.0 to ensure scale-axis decomposition is *attempted* even when the operator's intuitive Step 2 decomposition is along a different axis (e.g., functional, temporal, structural).

**Confirmation criteria (post-cases 2-3):**

- If Step 6 in cases 2-3 produces scales that Step 2 already produced under different framing, Step 6 collapses into Step 2.
- If Step 6 produces scales Step 2 missed AND those scales materially affect downstream steps (hypotheses, roadmap, governance), Step 6 graduates to candidate component.
- If Step 6 produces scales Step 2 missed but those scales never affect downstream steps, Step 6 demotes to procedural artifact.

### §3.3 Step 7 — Exploration beyond framing

**Provisional classification:** implicit sub-behavior of Branching Roadmap Engine.

**Reasoning:** Article II (Frame Humility) + Article VI (Coherent Convergence) together imply that the Branching Roadmap Engine must produce trajectories that exit the original frame, not just refine it. Step 7 is the explicit out-of-frame branching that the Branching Roadmap Engine performs before Step 8 converges into a stage-gated roadmap.

**Confirmation criteria (post-cases 2-3):**

- If Step 7 in cases 2-3 produces trajectories that Step 8 (Branching Roadmap Engine) does not produce on its own when Step 7 is omitted as a thought experiment, Step 7 graduates to candidate component.
- If Step 8 in cases 2-3 already produces out-of-frame trajectories without Step 7's prompt, Step 7 collapses into Step 8.
- If Step 7 produces trajectories that never survive Step 9's governance kernel, Step 7 demotes to procedural artifact (entertaining-but-irrelevant exploration).

---

## §4 — Step 11 retention as procedural artifact

**Classification:** C-tagged procedural artifact.

**Reasoning:** Recommendation + confidence + unresolved-uncertainty is the **output packaging shape**, not a component behavior. It is the format the other components' outputs converge into for benchmark capture. It is procedural because every benchmark requires an output packet; it is not architectural because no canonical component is performing the packaging.

**Pressure to graduate:** Step 11 would graduate to A only if evidence across cases 2-3 shows that **the packaging act itself produces material the upstream steps did not** — e.g., the act of stating confidence forces a re-examination of hypotheses, or the act of stating unresolved uncertainty surfaces a new failure condition. This is plausible but not predicted. Default: retain as C.

---

## §5 — Memory Logger gap closure (Step 12)

**Closure act:** Step 12 was added to procedure v1.0 specifically to map the previously unmapped Memory Logger component to a procedure step.

**Why this matters:** Doctrine v0.4 names Memory Logger as "PRIMARY site of Article VII enforcement" — the substrate for capacity accumulation and pattern deprecation. Without Step 12, Article VII could not be measured at case level in Phase 1; capacity-accumulation would only be visible at longitudinal aggregate (case 4+).

**Engagement criterion for Step 12:** ≥1 entry across {capacity-change observed / pattern engaged / pattern deprecated / judgment-act witnessed}, each with line-refs into Condition C output.

**Risk awareness (per risk #24):** Memory Logger entries must remain refutable. Step 12 entries are not certifications; they are line-ref-anchored observations that later evidence can deprecate.

---

## §6 — What this audit does NOT decide

This audit is **provisional**. It locks the pre-case mapping so that post-case reclassification has a baseline to compare against. It does NOT:

- Decide whether B-tagged steps graduate, collapse, or demote (case 2/3 evidence decides).
- Reclassify any canonical component (component reclassification is the operator-act of Step 7 in the locked 8-step Phase 1 sequence).
- Authorize new components (Article II + locked rules: no component addition without benchmark evidence forcing it).

---

## Cross-references

- `procedure/elif_mode_procedure_v1.0.md` — the procedure being mapped.
- `procedure/abcd_classification_system.md` — tag semantics.
- `procedure/benchmark_template.md` — capture template for case outputs (v1.0).
- `doctrine/06_constitutional_layer_v0_4.md` — canonical-component definitions.
- `benchmarks/component_engagement_tracking.md` — post-case engagement-frequency schema.
