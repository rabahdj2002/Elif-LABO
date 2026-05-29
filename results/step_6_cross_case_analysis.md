# Step 6 — Cross-Case Differentiator Analysis

**Status:** LOCKED 2026-05-28. Step 6 of the locked 8-step Phase 1 sequence.

**Scope (locked):** cross-case differentiator recording, prompt-portability analysis, architecture-dependence analysis, dormant vs engaged component analysis, recurring vs non-recurring pattern analysis, cost/signal observations.

**Scope explicitly excluded:** component additions, architecture expansion, v0.5 trajectory revision, philosophical consolidation, adoption of any candidate pattern. Reclassification (which procedure steps graduate, collapse, or demote) is Step 7. Architecture decision is Step 8.

**Working hypothesis being tested (per operator framing carrying into Step 6):**
> "ELIF may not primarily be a system producing fundamentally different conclusions. ELIF may instead be an architecture that makes certain epistemic and governance behaviors systematic, reproducible, traceable, and constraint-enforced."

The open question carried through this analysis:
> "How much of [Condition C's ~4x] structure produces additional signal versus additional procedural ceremony?"

---

## 1. Method

Three cases ran under matching evidence structure (procedure v1.0, E1.5 — procedure-augmented LLM, single-model). Each case produced Conditions A (bare LLM), B (structured-reasoning prompt), C (procedure v1.0 mechanical execution). All outputs saved verbatim to `results/case_NN/`.

Per `benchmarks/differentiator_tracking.md`, each differentiator is captured with:
- `description` (factual, not interpretive)
- `condition_c_line_refs` (Step number anchors into Condition C output)
- `also_in_condition_b` (yes / no / partial)
- `also_in_condition_a` (yes / no / partial — added field to capture the operator-named cross-case observation about baseline frame-rejection)
- `architecture_dependent` (yes / no / partial / uncertain)
- `survives_across_cases` (0/3, 1/3, 2/3, 3/3)
- `mapped_component` (A / B / C / D / unmapped)

**Honest contamination note:** all three Conditions A, B, C of all three cases were produced by the same LLM in the same session. "Bare" Condition A here means "no structured-reasoning scaffold and no procedure scaffolding" — not "no prior context." A truly bare LLM in a clean session would be a stronger test of baseline frame-humility. The operator chose Option 2 (E1.5) knowing this; the contamination is recorded but not corrected here.

---

## 2. Differentiator capture (per-case + cross-case)

### 2.1 — Structural differentiators (procedural-form artifacts)

These differentiators are produced by the procedure's structure (Steps 1-12) as discrete formal artifacts.

| ID | Differentiator | C-01 | C-02 | C-03 | Survives | A_in_B | A_in_A | Arch-dep |
|---|---|---|---|---|---|---|---|---|
| D1 | Explicit frame-validation verdict (`needs decomposition`) as first output, returned in one of three named forms | ✓ | ✓ | ✓ | **3/3** | partial (B diagnoses binary narratively) | partial (A names binary narratively) | partial — narrative form portable; structural one-of-three-verdict form architecture-dependent |
| D2 | Enumerated declarative assumptions (≥2 entries, statement-form) | ✓ (9) | ✓ (8) | ✓ (10) | **3/3** | partial (B's "deepest uncertainties" has overlap content) | partial (A engages narratively) | partial — content portable; enumeration-with-statement-form architecture-dependent |
| D3 | Hypotheses with explicit distinguishing predictions | ✓ (6) | ✓ (5) | ✓ (5) | **3/3** | no | no | YES |
| D4 | Failure conditions per hypothesis (Step 5 explicit) | ✓ (6) | ✓ (5) | ✓ (5) | **3/3** | no | no | YES |
| D5 | Multi-scale mapping (≥2 named scales) with ≥1 named cross-scale relation | ✓ (7 scales, 3 relations) | ✓ (5 scales, 3 relations) | ✓ (5 scales, 3 relations) | **3/3** | no | no | YES |
| D6 | Trajectories tagged `outside-original-frame` with one-line reason | ✓ (5) | ✓ (3) | ✓ (4) | **3/3** | partial (B/A name binary problem narratively) | partial | partial — frame-questioning is partially portable; explicit `outside-frame` tagging is architecture-dependent |
| D7 | Stage-gated branching roadmap (every stage carries explicit testable continuation gate) | ✓ | ✓ | ✓ | **3/3** | no (B produces recommendation without staged structure) | no | YES |
| D8 | Governance kernel produces one of {constrain, refuse, abstain} explicitly (no annotation-only output) | ✓ | ✓ | ✓ | **3/3** | substantively yes (B reaches refuse/constrain) | substantively yes | partial — substance portable; explicit-one-of-three-form architecture-dependent |
| D9 | Operative-vs-theoretical separation as discrete structural section | ✓ | ✓ | ✓ | **3/3** | no (B mixes them in tradeoff tables) | no (A merges them in narrative) | YES |
| D10 | Recommendation packet with confidence tied to specific unresolved-uncertainty sources | ✓ | ✓ | ✓ | **3/3** | partial (B states confidence + uncertainty separately) | partial | partial — confidence-uncertainty mention portable; explicit tying architecture-dependent |
| D11 | Memory Logger entries with category tags and line-refs into Condition C output | ✓ (7) | ✓ (5) | ✓ (6) | **3/3** | no | no | YES (purely procedural; no baseline analogue) |

### 2.2 — Substantive differentiators (content-level patterns)

These are substantive conclusions or analytical moves, distinguishable from procedural form.

| ID | Differentiator | C-01 | C-02 | C-03 | Survives | A_in_B | A_in_A | Arch-dep |
|---|---|---|---|---|---|---|---|---|
| D12 | Frame-rejection-of-the-binary appearing narratively in baseline | ✓ | ✓ | ✓ | **3/3** | YES | YES | NO — this is the operator-named cross-case observation: frame-humility is latent in baseline LLM |
| D13 | Substantive recommendation: refuse-the-bundle-while-constraining-disaggregated-components | ✓ | ✓ | ✓ | **3/3** | YES | YES | NO — substantively portable; the procedure makes it structural/traceable, not novel |
| D14 | Parallel-comparable-funding-in-established-alternatives mandate | ✓ | ✓ | ✓ | **3/3** | YES | YES | NO — portable |
| D15 | Same meta-uncertainty about whether proposing actor will accept disaggregated authorization | ✓ | ✓ | ✓ | **3/3** | partial (B mentions, A engages narratively) | partial | partial |

### 2.3 — Partial-recurrence differentiators (the operator's "more informative because not universal" set)

| ID | Differentiator | C-01 | C-02 | C-03 | Survives | Observation |
|---|---|---|---|---|---|---|
| D16 | Reversibility-as-load-bearing-decomposition-axis | ✗ (mechanism plausibility was load-bearing) | ✓ (ecological/molecular irreversibility) | ✓ (institutional/political-economic irreversibility) | **2/3** | Same axis-label; different mechanisms. Suggests the procedure produces content-appropriate decomposition axes rather than imposing one. The 2/3 occurrence is more informative than a 3/3 occurrence would have been, because it shows the procedure is not rigidly imposing reversibility on every case. |
| D17 | Deeper-frame-rejection trajectory (scope-of-authority OR scope-of-consent questioning) | ✓ (T5: ethical asymmetry of drought-prone-region farmer test population) | ✗ | ✓ (T4: healthcare-ministry scope-of-authority for civilizational-scale effects) | **2/3** | Domain-emergent. Appears in cases where the question's scale of effect exceeds the proposer's natural scope of authority/consent. Does NOT appear in Case 02 (deployment proposal scope ≈ proposer authority). |

### 2.4 — Content-derived decomposition axis (3/3 evidence)

This is a meta-observation across all three cases:

| ID | Description | C-01 axis | C-02 axis | C-03 axis | Survives | Observation |
|---|---|---|---|---|---|---|
| D18 | Load-bearing decomposition axis is content-derived, not procedure-imposed | mechanism plausibility | reversibility profile | data-coupling depth + infrastructure persistence (two axes) | **3/3** | The procedure (Step 2: "≥2 distinct families with named rationale") is content-agnostic at the rule level. The case content determines which axis is load-bearing. **This is partial evidence against the hypothesis that the procedure imposes a rigid decomposition shape.** |

---

## 3. Component engagement (per-case)

Per `benchmarks/component_engagement_tracking.md`, each of the 7 canonical components + B-tagged candidates + C-tagged artifact is recorded per case.

### 3.1 Canonical components (A-tagged per pre-case audit)

| Component | Procedure step(s) | C-01 engaged | C-02 engaged | C-03 engaged | Frequency | Prompting portable | Current pressure |
|---|---|---|---|---|---|---|---|
| Frame Validator | Step 1 | ✓ | ✓ | ✓ | 3/3 | partial (D1, D12) | engaged (3/3) |
| Object Decomposer | Step 2 | ✓ | ✓ | ✓ | 3/3 | partial (Conditions A and B produce decomposition narratively without named-axis structure) | engaged (3/3) |
| Hypothesis Validator | Steps 4 + 5 | ✓ | ✓ | ✓ | 3/3 | no (D3, D4 architecture-dependent) | engaged (3/3) |
| Branching Roadmap Engine | Step 8 | ✓ | ✓ | ✓ | 3/3 | no (D7 architecture-dependent) | engaged (3/3) |
| Governance Kernel | Step 9 | ✓ | ✓ | ✓ | 3/3 | partial (D8 substance portable; form architecture-dependent) | engaged (3/3) |
| Operative Truth Separator | Step 10 | ✓ | ✓ | ✓ | 3/3 | no (D9 architecture-dependent) | engaged (3/3) |
| Feedback / Memory Logger | Step 12 | ✓ | ✓ | ✓ | 3/3 | no (D11 architecture-dependent) | engaged (3/3) |

**Cross-case summary:** 7/7 canonical components engaged in 3/3 cases. **No dormant components.** No A→D demotion candidates surface from the cross-case evidence.

### 3.2 B-tagged candidates (per pre-case mapping audit)

| Candidate | Procedure step | C-01 engaged | C-02 engaged | C-03 engaged | Frequency | Prompting portable | Provisional collapse target | Current pressure |
|---|---|---|---|---|---|---|---|---|
| Hidden assumption extraction | Step 3 | ✓ (9) | ✓ (8) | ✓ (10) | 3/3 | partial (content overlap with Condition B "uncertainties"; statement-form is architecture-dependent) | Frame Validator | engaged (3/3); collapse-target evidence weak — Step 3 enumerated assumptions in all three cases that Step 1 verdicts did not themselves contain. Step 1 produced one-of-three verdicts; Step 3 produced 8-10 statements per case. The two outputs are not redundant. **No commitment to collapse vs graduate yet — that is Step 7.** |
| Multi-scale mapping | Step 6 | ✓ | ✓ | ✓ | 3/3 | no | Object Decomposer | engaged (3/3); collapse-target evidence weak — Step 6's cross-scale relations included material Step 2 did not produce in any case (e.g., Case 02 "irreversible-molecular-change vs 5-year-governance-cycle"; Case 03 "individual consent does not aggregate to civilizational consent"; Case 01 "pseudoscience-normalization-velocity exceeds mechanism-testing-velocity"). **No commitment yet.** |
| Exploration beyond framing | Step 7 | ✓ (5) | ✓ (3) | ✓ (4) | 3/3 | partial (Conditions A and B narratively engage frame-rejection; explicit `outside-original-frame` tagging architecture-dependent) | Branching Roadmap Engine | engaged (3/3); collapse-target evidence mixed — Step 8 produced stage-gated roadmaps in all three cases; Step 7 produced trajectories some of which were upstream of Step 8 (T1-T2 entered Step 8 stages) and some of which were not (T3-T5 questioned premises that Step 8 did not act on). **No commitment yet.** |

### 3.3 C-tagged (procedural artifact)

| Item | Procedure step | C-01 engaged | C-02 engaged | C-03 engaged | Frequency | Current pressure |
|---|---|---|---|---|---|---|
| Recommendation packet | Step 11 | ✓ | ✓ | ✓ | 3/3 | engaged (3/3); remains C-tagged. Step 11 is the output-shape that packages other steps' work into a reviewable artifact. **No commitment to upgrade or remove.** |

### 3.4 Architecture-files validation status

Pre-case scaffolds at `architecture/01-07_*.md` listed Case 01 engagement as "(to fill from results)" — those entries can now be populated by referencing the per-case results files. **That population is administrative; it is NOT component reclassification (Step 7).**

---

## 4. Cost / signal observations

### 4.1 Length data

| Case | Cond A (words) | Cond B (words) | Cond C (words) | C / mean(A,B) |
|---|---|---|---|---|
| Case 01 | ~750 | ~720 | ~3500 | ~4.76x |
| Case 02 | ~600 | ~520 | ~2400 | ~4.29x |
| Case 03 | ~650 | ~720 | ~3000 | ~4.38x |
| **Mean** | ~667 | ~653 | ~2967 | **~4.48x** |

### 4.2 Per-step signal-vs-ceremony observation

This is the explicit signal-vs-ceremony analysis the operator named. **Observations only; no adoption of "ceremony" labels for procedural-revision purposes.**

| Step | Cost share (est. % of Condition C) | Architecture-dependent signal | Substantive content overlap with B/A | Signal-vs-ceremony observation |
|---|---|---|---|---|
| 1 — Frame validation | ~3% | partial (D1) | partial (D12) | Signal: structural form is novel; content (frame-rejection) is portable. **Recurrence of D12 in baseline weakens the architecture-dependence claim for this step's content.** Form-as-anchor for downstream steps may still be signal — needs cross-case test of whether downstream steps would proceed coherently without Step 1's explicit verdict. |
| 2 — Object decomposition | ~10% | partial | partial | Signal: named-axis decomposition is more rigorous than narrative; content is content-derived (D18). **The procedure produces decomposition shape; baseline produces decomposition content. Whether the shape adds signal beyond the content is the cross-case question — Cases 2 and 3 each produced different load-bearing axes, which suggests the shape constrains less than it might.** |
| 3 — Hidden assumptions | ~8% | partial | partial | Signal: enumeration with statement-form. Content overlap with Condition B's "deepest uncertainties" is substantial but not complete. **Could collapse into Step 1 if assumptions are reformulated as part of frame-reformulation, OR could remain distinct.** Step 7 evaluation. |
| 4-5 — Hypotheses + failure conditions | ~20% | YES | no | **Highest architecture-dependence finding.** No baseline analogue. Cases 2 and 3 both produced 5 hypotheses each with failure conditions; case 01 produced 6. The pre-registered-falsifiability discipline is structurally absent from Conditions A and B. **This is the cleanest "signal not ceremony" candidate so far; cross-case evidence is 3/3.** |
| 6 — Multi-scale | ~8% | YES | no | Architecture-dependent. Cross-scale relations produced in all three cases. Case 01 introduced a cross-scale relation (pseudoscience-normalization-velocity) Cases 02-03 did not. Case 03 introduced "consent does not aggregate across scales." **Signal candidate; cross-case test of whether material differs from Step 2 is what Step 7 evaluates.** |
| 7 — Outside-frame trajectories | ~8% | partial | partial | Frame-rejection-narrative portable (D12). Explicit `outside-frame` tagging architecture-dependent. Some Step 7 trajectories enter Step 8 stages (forward composition); some question premises Step 8 does not act on (independent value). **Signal mixed; some trajectories ceremony-suspect.** |
| 8 — Stage-gated roadmap | ~15% | YES | no | **High signal.** No baseline analogue produced staged continuation gates. The discipline of "every stage carries a testable continuation gate" is architecture-dependent. 3/3 cases produced staged roadmaps. |
| 9 — Governance kernel | ~7% | partial | YES (D13) | **Substantive recommendation is fully portable.** Form (one-of-three explicit) is architecture-dependent. **Signal-vs-ceremony question is most acute here: if Conditions A and B independently reach the same governance recommendation, the procedure's contribution is form-traceability, not content-novelty.** |
| 10 — Operative vs theoretical | ~7% | YES | no | **Signal candidate.** Conditions A and B mixed operative and theoretical content; Condition C separated them as discrete sections. Whether downstream consumers benefit from the separation is not testable from within the three-case evidence. |
| 11 — Recommendation packet | ~5% | partial | partial | **Ceremony-suspect.** Confidence + unresolved-uncertainty mentions are partially portable. The explicit-tying form is architecture-dependent but may be procedural artifact (C-tag). Step 7 evaluation. |
| 12 — Memory Logger entries | ~9% | YES | no | **Architecture-dependent and longitudinally-purposed.** Step 12 entries are the substrate for Article VII tracking — they have no in-case purpose beyond enabling cross-case capacity analysis. **Whether they are signal or ceremony depends on whether cross-case capacity analysis produces actionable findings; Step 7 begins that evaluation.** |

### 4.3 Signal-vs-ceremony provisional reading (recording only)

| Category | Procedure steps | Cross-case evidence |
|---|---|---|
| **Highest architecture-dependence + lowest baseline overlap** (signal candidates) | Steps 4-5, 8, 10, 12 | 3/3 cases produced unique-to-Condition-C structural content with no analogue in Conditions A/B. |
| **Architecture-dependent form + partial baseline overlap** (mixed) | Steps 1, 2, 6, 7, 9, 11 | 3/3 cases produced these but Conditions A/B produced overlapping content narratively. The procedure's contribution is form-traceability + recoverability, not content-novelty. |
| **Ceremony-suspect** | (Step 11 by C-tag; no others clearly identified) | C-tag is procedural-artifact by design; whether other steps drift into ceremony is a Step 7 question. |

**No commitment** to which steps "are signal" vs "are ceremony." Recording only.

---

## 5. Cross-case patterns: recurring vs non-recurring

### 5.1 3/3 recurring patterns (candidate compositional structures)

| Pattern | Status |
|---|---|
| refuse-bundle-while-constraining-disaggregated-components | 3/3 occurrence. **No adoption.** Deprecation-pressure has not been applied: all three input frames had bundle-binary closure shape. A case with non-bundle-binary closure has not been tested. |
| parallel-comparable-funding-in-established-alternatives | 3/3 occurrence. **No adoption.** Same deprecation-pressure caveat. |
| same-meta-uncertainty-about-proposer-good-faith | 3/3 occurrence. **No adoption.** Same caveat. |
| Step 1 returning `needs decomposition` against bundle-binary inputs | 3/3 occurrence; partially function of input-frame design. Same caveat. |
| Content-derived load-bearing decomposition axis (D18) | 3/3 evidence; **this is partial evidence against rigid-procedure-imposition.** No adoption — this is meta-observation. |

### 5.2 2/3 partial recurrence (the operator's "more informative because not universal" set)

| Pattern | Status |
|---|---|
| Reversibility-as-load-bearing-decomposition-axis (D16) | 2/3. Absent in Case 01 (mechanism plausibility was load-bearing). **Domain-emergent rather than procedure-imposed; this is the most informative cross-case finding for the working hypothesis.** |
| Deeper-frame-rejection trajectory (D17) | 2/3. Absent in Case 02. Domain-emergent; appears when effect-scale exceeds proposer-authority-scale. |

### 5.3 0/3 anti-patterns NOT observed

Per `article_vii_tracking.md` schema, the following critical failure patterns should be checked:

| Failure pattern | Detected? | Note |
|---|---|---|
| **Sterile equilibrium signature** (`time_delta_vs_prior_similar ≥ 0` consistently + `reuse_count_total = 0` + `capacity_change_records` empty + `patterns_recognized` empty) | **NOT detected** | Time delta is uninstrumented (gap noted). Reuse counts: 0 in Case 02 (first case), 4 in Case 03, 5 in Case 01 (re-executed third). Capacity-change records: present in all three cases. Patterns recognized: present in all three. |
| **Sovereignty-import signature** (patterns with confidence > 0.9 missing refutation conditions) | **NOT detected** | All patterns recorded with confidence ≤ 0.75 and explicit refutation conditions. |
| **Article II violation via stale-framing-reuse** (any `reuse_kind=direct` where Frame Validator should have refused) | **NOT detected** | All reuse was `reuse_kind=composed`, applied to freshly-decomposed framing per Case 01 and Case 03 article_ii_check. |

**Halt conditions per schema NOT triggered.** Article VII remains operational; no demotion pressure surfaces from cross-case evidence.

---

## 6. Working-hypothesis-relevant findings

Per the operator's framing carrying into Step 6, the working hypothesis under test is:

> "ELIF may be an architecture that makes certain epistemic and governance behaviors systematic, reproducible, traceable, and constraint-enforced — not a system producing fundamentally different conclusions."

The cross-case evidence has the following relation to this hypothesis:

| Finding | Direction of evidence |
|---|---|
| Substantive recommendations converge across A/B/C in 3/3 cases | **Supports** the hypothesis (procedure does not shift conclusions). |
| Frame-rejection-as-narrative appears in 3/3 baseline (A) cases | **Supports** the hypothesis (baseline LLMs have latent frame-humility on transparently-bundled inputs). |
| Steps 4-5, 8, 10, 12 produce structural artifacts with no baseline analogue in 3/3 cases | **Supports** the hypothesis (architecture-dependence is real but it is in *traceability and form*, not in *substantive direction*). |
| Reversibility-axis non-universality (2/3) | **Supports** the hypothesis (procedure is not imposing rigid universal shape; content-emergent decomposition). |
| 3/3 cases agree on refuse-bundle-while-constraining-disaggregated | **Compatible** with hypothesis — same conclusion across conditions, made structural by procedure. |
| ~4x cost expansion in Condition C | **Open question** per operator: how much is signal vs ceremony? Steps 4-5, 8, 10, 12 are signal-leaning. Steps 1, 9, 11 are form-vs-content-portable mixed. |

**No conclusion adopted.** The hypothesis remains under test. Three cases are insufficient for hypothesis adoption per the locked rule (≥3 case demonstrations + deprecation-pressure survival; deprecation-pressure has not been applied because all three input frames shared bundle-binary closure shape).

---

## 7. What this document does NOT do

- Does not classify any procedure step as graduating, collapsing, or demoting. **That is Step 7.**
- Does not commit to any architecture revision. **That is Step 8.**
- Does not modify procedure v1.0. **That is forbidden during Phase 1.**
- Does not adopt any candidate compositional structure as canonical. **Per locked rule.**
- Does not declare ELIF "works" or "doesn't work." **Both readings remain available from this evidence.**
- Does not iterate the constitutional layer. **Locked at v0.4.**

What this document does:
- Records observed differentiators across three matching-evidence-structure cases.
- Computes survival counts (0/3 to 3/3) per differentiator.
- Records prompt-portability and architecture-dependence per differentiator.
- Records component engagement state per case.
- Records cost/length observations with the signal-vs-ceremony question explicit.
- Cross-references Article VII tracking JSON files for capacity-accumulation metrics.

---

## 8. Step 7 readiness statement

Step 7 of the locked 8-step Phase 1 sequence is reclassification of B-tagged procedure steps (Steps 3, 6, 7) and Step 11 (C-tagged), per `procedure/abcd_classification_system.md` retention bars. Evidence required for Step 7 is now on disk:

- Per-case differentiator + component engagement (this document).
- Per-case Article VII tracking (results/case_NN/article_vii_tracking.json).
- Per-case Conditions A, B, C outputs verbatim.
- Cross-case pattern occurrence counts.
- Signal-vs-ceremony observations.

Step 7 begins when operator authorizes. **No reclassification work performed until then.**

---

## 9. Cross-references

- `procedure/elif_mode_procedure_v1.0.md` — the procedure executed.
- `procedure/benchmark_template.md` — capture template.
- `procedure/step_to_component_mapping_audit_v1_0.md` — pre-case provisional mapping (the baseline against which Step 7 reclassifies).
- `procedure/abcd_classification_system.md` — A/B/C/D retention bars.
- `procedure/phase_gates.md` — phase-gate semantics; G1.1-G1.5 to be evaluated at Step 7/8.
- `benchmarks/differentiator_tracking.md` — schema applied here.
- `benchmarks/component_engagement_tracking.md` — schema applied here.
- `benchmarks/article_vii_capacity_accumulation_tracking.md` — schema applied in per-case JSON.
- `results/case_01/{condition_a,b,c}_output.md`, `preliminary_observations.md`, `article_vii_tracking.json`.
- `results/case_02/{same}`.
- `results/case_03/{same}`.
- `doctrine/06_constitutional_layer_v0_4.md` — constitutional anchor; pressure rule.
