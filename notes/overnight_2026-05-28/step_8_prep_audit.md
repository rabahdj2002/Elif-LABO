# Step 8 Preparation Audit (cold engineering, no decisions)

**Status:** Overnight preparation deliverable 2026-05-28. **NOT a decision document.** Parallel substrate to `results/step_8_architecture_decision.md` for operator review.

**Scope:** evidence surfacing only. Names options. Does not select. Does not commit. Does not adopt.

**Inputs:** `results/step_6_cross_case_analysis.md`, `results/step_7_reclassification.md`, `procedure/abcd_classification_system.md`, `procedure/elif_mode_procedure_v1.0.md`, `doctrine/06_constitutional_layer_v0_4.md`.

---

## 1. Surviving A-tagged behaviors (3/3 engaged, no demotion candidates)

Per Step 6 §3.1 + §4.2.

| Procedure step | Component | Engagement | Architecture-dependent? | Cost share |
|---|---|---|---|---|
| 1 — Frame validation | Frame Validator | 3/3 | partial (form architecture-dependent; substance D12-portable) | ~3% |
| 2 — Object decomposition | Object Decomposer | 3/3 | partial (named-axis form vs narrative content) | ~10% |
| 4-5 — Hypotheses + failure conditions | Hypothesis Validator | 3/3 | **YES** (no A/B analogue) | ~20% |
| 8 — Stage-gated roadmap | Branching Roadmap Engine | 3/3 | **YES** (no A/B analogue) | ~15% |
| 9 — Governance kernel verdict | Governance Kernel | 3/3 | partial (substance D13-portable; one-of-three form architecture-dependent) | ~7% |
| 10 — Operative vs theoretical | Operative Truth Separator | 3/3 | **YES** (no A/B analogue) | ~7% |
| 12 — Memory Logger | Feedback / Memory Logger | 3/3 | **YES** (purely procedural; no baseline analogue) | ~9% |

**Aggregate (raw):** 7 A-tagged components × 3/3 engagement. Four are clean architecture-dependent (Steps 4-5, 8, 10, 12 — ~51% of Condition C cost). Three are partial-portability (Steps 1, 2, 9 — ~20% of Condition C cost).

**No A→D demotion candidate** surfaces from three-case evidence.

---

## 2. Unresolved B/C-tagged behaviors

Per Step 7 §2-5.

| Step | Tag | Engagement | Verdict | Unresolved question |
|---|---|---|---|---|
| 3 — Hidden assumptions | B | 3/3 | Graduation-candidate | Form architecture-dependent; substance partially portable. Overlap with Step 11 unresolved-uncertainty unmeasured. |
| 6 — Multi-scale | B | 3/3 | Graduation-candidate | Architecture-dependent in 3/3, but cases all had naturally multi-scale content. Untested on single-scale content. |
| 7 — Outside-frame trajectories | B | 3/3 | UNRESOLVED (mixed evidence) | BRE-compositional portion redundant; deeper-frame-rejection portion 2/3 with strong Article II tie. |
| 11 — Recommendation packet | C | 3/3 | Remains C (procedural artifact) | Substance fully portable to Step 9; tying-discipline is convention not behavior. |

**Aggregate (raw):** Four B/C-tagged steps × 3/3 engagement; cost ~29% of Condition C. None are dormant. None are clean graduation. None are clean removal.

---

## 3. Prompting-portable vs architecture-dependent separation

Per Step 6 §2 differentiator table.

### 3.1 Clean architecture-dependent (no baseline analogue)

| Differentiator | Survives | Architecture-dependent | Mapping |
|---|---|---|---|
| D3 — Hypotheses with distinguishing predictions | 3/3 | YES | Hypothesis Validator (Steps 4-5) |
| D4 — Failure conditions per hypothesis | 3/3 | YES | Hypothesis Validator (Steps 4-5) |
| D5 — Multi-scale mapping with cross-scale relation | 3/3 | YES | (B-tag) Object Decomposer sub-behavior candidate |
| D7 — Stage-gated branching roadmap with continuation gates | 3/3 | YES | Branching Roadmap Engine (Step 8) |
| D9 — Operative-vs-theoretical as discrete sections | 3/3 | YES | Operative Truth Separator (Step 10) |
| D11 — Memory Logger entries with category tags + line-refs | 3/3 | YES | Feedback / Memory Logger (Step 12) |

### 3.2 Clean prompting-portable (substantive content baseline-reachable)

| Differentiator | Survives | Architecture-dependent | Notes |
|---|---|---|---|
| D12 — Frame-rejection-of-binary appears narratively in Condition A | 3/3 | NO | Latent frame-humility in baseline. This is the operator-named cross-case observation. |
| D13 — refuse-bundle-while-constraining-disaggregated | 3/3 | NO | Substantive recommendation portable. Form-traceability is the procedure's contribution. |
| D14 — Parallel-comparable-funding-in-alternatives mandate | 3/3 | NO | Portable. |

### 3.3 Form-architecture-dependent + substance-portable (mixed)

| Differentiator | Survives | Form arch-dep | Substance portable | Notes |
|---|---|---|---|---|
| D1 — Explicit frame-validation one-of-three verdict | 3/3 | YES | YES (Condition B diagnoses narratively) | Form anchors downstream steps. |
| D2 — Enumerated declarative assumptions | 3/3 | YES | partial (B's "deepest uncertainties" overlaps) | Statement-form discipline architecturally specific. |
| D6 — `outside-original-frame` tagging | 3/3 | partial | partial | D12 + explicit tag. |
| D8 — Governance one-of-three (constrain/refuse/abstain) | 3/3 | YES | YES (D13) | One-of-three form vs narrative form. |
| D10 — Recommendation packet with confidence tied to uncertainty | 3/3 | YES (tying) | YES (mention) | Tying-discipline is the architectural surface. |
| D15 — Same meta-uncertainty about proposer good faith | 3/3 | partial | partial | Both express; procedure tags structurally. |

### 3.4 Partial recurrence (2/3 — more informative than 3/3)

| Differentiator | Pattern | Architecture-dependent? | Notes |
|---|---|---|---|
| D16 — Reversibility-as-load-bearing decomposition axis | 2/3 (Case 01 used mechanism plausibility) | NO (content-derived) | Suggests procedure does not impose universal axis. |
| D17 — Deeper-frame-rejection trajectory (scope-of-authority OR scope-of-consent questioning) | 2/3 (absent in Case 02) | partial (domain-emergent) | Appears when effect-scale exceeds proposer-authority-scale. |

**Cross-cutting reading:** the procedure's architecture-dependent capacity concentrates in *form*, *traceability*, and *recoverability* — not in *substantive content novelty*. Substantive conclusions converge across A/B/C in 3/3 cases.

---

## 4. Cost / signal concentration analysis

Per Step 6 §4.

| Category | Steps | Cost share | Architecture-dependence | Signal-vs-ceremony |
|---|---|---|---|---|
| Clean architecture-dependent + no baseline overlap | 4-5, 8, 10, 12 | ~51% | YES | Signal-leaning per cross-case evidence |
| Architecture-dependent form + partial baseline overlap | 1, 2, 9 | ~20% | partial | Mixed |
| B-tagged graduation-candidates | 3, 6 | ~16% | partial / YES | Signal-leaning per Step 7 verdict |
| B-tagged unresolved | 7 | ~8% | partial | Mixed (50% BRE-redundant; 50% Article-II tied) |
| C-tagged procedural artifact | 11 | ~5% | NO | Substance portable |

**Even with all B+C steps collapsed/removed,** Condition C expansion remains ~2.8x baseline (per Step 6 + Step 7 §6.1). Architecture-dependent A-tagged steps drive the majority of expansion.

**Implication for compression bounds:**
- Floor of ~2.8x is determined by A-tagged structural behaviors.
- Compression below ~2.8x requires deprecating A-tagged architecture-dependent components.
- Deprecation requires deprecation-pressure evidence (multiple cases failing to engage a component) — none surfaces from three-case evidence.

---

## 5. Recurring vs non-recurring structural behaviors

Per Step 6 §5.

### 5.1 Recurring (3/3)

- **Procedural-form structural behaviors:** D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11 — all procedural-form behaviors that the procedure mechanically produces appear in 3/3 (because the procedure mechanically runs).
- **Substantive content patterns:** D12 (baseline frame-rejection), D13 (refuse-bundle-with-disaggregated-constraint), D14 (parallel-funding mandate), D15 (proposer-meta-uncertainty) — substantive conclusions that converge across all three cases.

### 5.2 Partial recurring (2/3)

- D16 reversibility-axis (content-emergent)
- D17 deeper-frame-rejection (domain-emergent)

### 5.3 0/3 — anti-patterns NOT detected

- Sterile-equilibrium signature (Article VII halt condition)
- Sovereignty-import signature (confidence >0.9 missing refutation)
- Article II violation via stale-framing-reuse

**No halt conditions triggered.** Article VII operational; no demotion pressure.

---

## 6. Unresolved tensions surfaced (recording only)

### T1 — Bundle-binary-input-frame deprecation pressure not applied

All three input frames shared a bundle-binary closure shape. Step 1 returning `needs decomposition` in 3/3 is partially a function of input-frame design. The candidate patterns (refuse-bundle / parallel-funding / meta-uncertainty) are 3/3 but unfalsified by deprecation pressure.

**Unresolved:** would a non-bundle-binary input frame produce the same patterns or different ones? Three-case evidence cannot answer.

### T2 — Single-scale content not tested

Step 6 (multi-scale) achieved 3/3 engagement, but all three cases had naturally multi-scale content. The procedure's discipline mandates ≥2 scales + ≥1 cross-scale relation as a mechanical floor.

**Unresolved:** does Step 6 engage as ceremony when content is naturally single-scale? Three-case evidence cannot answer.

### T3 — E1.5 single-LLM-session contamination

All three Conditions A, B, C were produced by the same LLM in the same session. "Bare" Condition A here means "no scaffold + no procedure" not "no prior context."

**Unresolved:** would a truly bare LLM in a clean session produce the same D12 baseline frame-rejection? The architecture-dependence claims for partial-portability differentiators (D1, D2, D6, D8, D10) rest on Condition B comparison which is also single-session.

### T4 — Step 3 / Step 11 substantive overlap unmeasured

Step 7 §2 noted some Step 3 assumptions overlapped Step 11 unresolved-uncertainty sources within the same Condition C run. Overlap was not quantified.

**Unresolved:** would explicit overlap measurement support a merge (Q3.3 in Step 7 forwarded questions)?

### T5 — Deeper-frame-rejection in only 2/3 cases

D17 / Step 7 Mode B appears 2/3 (Case 02 absent). Step 7 §4 verdict was UNRESOLVED. The portion that does engage ties strongly to Article II Frame Humility.

**Unresolved:** is 2/3 below an adoption threshold? Adoption requires ≥3 case demonstrations per v0.4 emergent-wisdom rules. Behavior preservation does not require adoption.

### T6 — Architecture-dependence vs Frontier-LLM portability

The architecture-dependence claim rests on Condition B's behavior. Condition B is itself a structured-reasoning prompt (a less-disciplined scaffold). Frontier LLMs with more elaborate Condition-B-style prompting may close the gap on D1, D2, D6, D8, D10 (form-architecture-dependent differentiators).

**Unresolved:** how much of D1-D11 is recoverable through a more elaborate Condition B? (This is the Frontier-LLM Capability Audit territory — see separate document.)

### T7 — Cost concentration is structurally fixed

The ~2.8x floor (A-tagged architecture-dependent steps) means compression has a hard bound short of component deprecation.

**Unresolved:** is ~2.8x expansion acceptable per the project's value model? No external value model is defined.

---

## 7. Minimum viable architecture candidates (multi-option; no selection)

Option set across decision dimensions. The dimensions are independent; each can be picked separately.

### 7.1 Dimension A — B-tagged graduation policy (Steps 3, 6)

- **A.1** No formal action. Steps 3, 6 remain B-tagged procedure steps. Cost retained.
- **A.2** Document as sub-behaviors of existing components (Frame Validator + Object Decomposer). No new components. (Step 8 selection)
- **A.3** Formalize as 8th + 9th canonical components. Architecture grows by 2. (Rejected by Step 8.)
- **A.4** Merge Step 3 into Step 1 verdict-with-assumptions; merge Step 6 into Step 2 multi-axis decomposition. Cost compresses; downstream references must be retargeted.
- **A.5** Defer decision until 4th case provides single-scale evidence for Step 6 and overlap-measurement for Step 3.

### 7.2 Dimension B — Step 7 unresolved policy

- **B.1** Collapse entirely into Branching Roadmap Engine. Accept deeper-frame-rejection loss.
- **B.2** Split into BRE-feed (collapses) + Article II sub-behavior (Frame Validator). (Step 8 selection.)
- **B.3** Maintain pending 4th case.
- **B.4** Retain in current form.

### 7.3 Dimension C — Step 11 policy

- **C.1** Retain as procedure step.
- **C.2** Collapse into Step 9 output shape. (Step 8 selection.)
- **C.3** Move to post-procedure presentation layer.

### 7.4 Dimension D — Procedure compression scope

- **D.1** No compression. v1.0 remains executed procedure.
- **D.2** Compress 12 → 11 steps (Step 11 dissolves). (Step 8 selection.)
- **D.3** Compress 12 → 10 (Steps 11 + Step 3 dissolve into others).
- **D.4** Compress 12 → 9 (Steps 11 + 3 + 6 dissolve).
- **D.5** Aggressive compression: 12 → 8 with sub-behavior consolidation.

### 7.5 Dimension E — Pattern adoption

- **E.1** No adoption. Patterns remain candidates pending deprecation-pressure case. (Step 8 selection.)
- **E.2** Adopt patterns reaching 3/3 as canonical content shapes.
- **E.3** Defer adoption pending 4th and 5th cases (≥3 + deprecation pressure).

### 7.6 Dimension F — Constitutional iteration

- **F.1** v0.4 stays locked. (Step 8 selection.)
- **F.2** v0.5 compression attempted (must be smaller).
- **F.3** v0.4 → v0.5 article elimination (which article fails three-case pressure? none surface as failing).

**Cross-dimensional consistency note:** A.2 + B.2 + C.2 + D.2 + E.1 + F.1 is the Step 8 selection. Other consistent combinations: A.4 + B.1 + C.2 + D.4 + E.1 + F.1 (aggressive); A.1 + B.4 + C.1 + D.1 + E.1 + F.1 (no-change).

---

## 8. Smallest-buildable-core candidates (engineering-only enumeration)

These are candidate cores ranked by reductive aggression. **Recording only.**

### Core S0 — "preserve current procedure execution surface"
- All 7 components retained
- All 12 procedure steps retained
- Cost: ~4.48x baseline (per Step 6 §4.1)
- Risk: ceremonial inflation in B/C surface
- Risk: convergence on illusion of working

### Core S1 — "smallest preserving signal" (matches Step 8 disposition)
- All 7 components retained
- Procedure 12 → 11 (Step 11 → Step 9 output shape)
- B-tagged behaviors graduated to documented sub-behaviors
- Cost: estimated ~3.5x–4.0x baseline (not yet measured)
- Risk: graduation-by-documentation may not survive execution stress
- Risk: sub-behaviors may drift back into procedure-step granularity

### Core S2 — "aggressive sub-behavior consolidation"
- All 7 components retained
- Procedure 12 → 9 (Steps 3, 6, 11 all dissolve into owning components)
- Cost: estimated ~3.0x–3.5x baseline
- Risk: substantive loss of enumeration discipline (Step 3) or scale-relation discipline (Step 6)
- Risk: under-compression evidence not collected

### Core S3 — "Article-VII-only core"
- Reduce to: Frame Validator + Hypothesis Validator + Branching Roadmap Engine + Governance Kernel + Memory Logger (5 components)
- Drop: Object Decomposer (substance D18-portable), Operative Truth Separator (form architecture-dependent but content can be tagged inline)
- Cost: estimated ~2.5x–3.0x baseline
- Risk: loss of D9 separation discipline
- Risk: loss of multi-axis decomposition rigor
- Risk: insufficient evidence for this aggressive cut (no A→D demotion pressure surfaced)

### Core S4 — "constitutional-layer-only"
- Reduce to: Articles I-VII as doctrine + Memory Logger as observability substrate
- Drop: all 7 components as enforceable code surface; ELIF becomes a doctrine + logging layer only
- Cost: ~1.0x baseline (no procedural expansion)
- Risk: D3-D5, D7, D9, D11 architectural-dependence lost
- Risk: 3/3 evidence shows these are signal-leaning — this cut sacrifices the cleanest signal
- Risk: hypothesis "ELIF makes behaviors systematic/traceable/constraint-enforced" loses the enforcement substrate

**Step 8 selected S1.** S0, S2, S3, S4 are alternatives not selected. **No recommendation here — recording only.**

---

## 9. Risks if over-compressed (the under-architecture failure mode)

| # | Risk | Evidence trace |
|---|---|---|
| R-O1 | Loss of D3, D4 (hypothesis falsifiability discipline) under S3/S4 | Step 6 §4.2 — Steps 4-5 have no A/B analogue in 3/3 |
| R-O2 | Loss of D7 (stage-gated continuation discipline) under S3/S4 | Step 6 §4.2 — Step 8 has no A/B analogue in 3/3 |
| R-O3 | Loss of D9 (operative-vs-theoretical separation) under S3/S4 | Step 6 §4.2 — Step 10 has no A/B analogue in 3/3 |
| R-O4 | Loss of D11 (Memory Logger as Article VII substrate) under S4 | Step 6 §4.2 — Step 12 is the article VII enforcement primary site |
| R-O5 | Loss of enumeration-form rigor on assumptions if S2 merges Step 3 into Step 1 | Step 7 §2 — enumerated declarative form is form-architecture-dependent in 3/3 |
| R-O6 | Loss of cross-scale-relation rigor if S2 merges Step 6 into Step 2 | Step 7 §3 — cross-scale relations produced material Step 2 did not in 3/3 |
| R-O7 | Article VII tracking substrate weakens if Memory Logger loses Step 12 prominence | Constitutional layer v0.4 §"Component implications" |
| R-O8 | Working hypothesis ("systematic/traceable/constraint-enforced") loses enforcement surface under aggressive cuts | This hypothesis depends on the architecture-dependent A-tagged steps remaining executable |

**Over-compression failure mode:** ELIF becomes doctrine-with-logging; the constraint-enforcement substrate that produced the cross-case differentiation evaporates. The Phase 6 / Phase 9 long-range roadmap becomes vacuous (nothing concrete to scale).

---

## 10. Risks if under-compressed (the over-architecture failure mode)

| # | Risk | Evidence trace |
|---|---|---|
| R-U1 | Cost remains ~4.48x baseline indefinitely; ceremony surface persists | Step 6 §4.1 |
| R-U2 | Step 11 packaging-ceremony reified as canonical reasoning behavior | Step 7 §5 verdict was procedural artifact |
| R-U3 | Step 7 BRE-compositional redundancy persists; ~4% of cost duplicates Step 8 | Step 7 §4 — ~50% of Step 7 trajectories are BRE-redundant |
| R-U4 | B-tagged graduation-candidates persist as separate procedure steps that re-engage as if 8th/9th components | Risk of architecture-by-procedure-drift |
| R-U5 | Pattern adoption pressure builds without deprecation-pressure case ever applied | Risks "by drift" canonicalization of refuse-bundle / parallel-funding / etc. |
| R-U6 | Constitutional layer iteration discipline weakens (no v0.5 compression attempted; momentum-stability mistaken for evidence-stability) | v0.4 compression-trajectory rule |
| R-U7 | Procedure rigidity prevents the architecture from genuinely compressing under new evidence | Locked rule 02 — refinement cannot indefinitely delay confrontation |
| R-U8 | The "smallest real ELIF" question is asked but never answered; remains as recurring conversational topic | Self-confirmation loop risk |

**Under-compression failure mode:** ELIF becomes a procedurally-complete artifact whose cost expansion is not commensurate with signal added; the architecture survives by inertia rather than evidence; Article VII halts on its own enforcement (capacity stops growing because rigid form prevents revision).

---

## 11. Forward-looking gates (Phase 2 entry conditions, NOT decisions)

Per Step 8 §7. **Recording only.**

| Gate | Status as of 2026-05-28 | Evidence |
|---|---|---|
| G1.1 — Benchmark template locked | satisfied | benchmark_template.md v1.0 |
| G1.2 — Procedure locked | satisfied | elif_mode_procedure_v1.0.md v1.0 |
| G1.3 — ≥3 cases run | satisfied | results/case_01,02,03 |
| G1.4 — Cross-case + reclassification + arch-decision on disk | satisfied | results/step_6, step_7, step_8 |
| G1.5 — Constitutional stability under cases | satisfied (no v0.5 trigger) | doctrine/06_constitutional_layer_v0_4.md |

Phase 2 entry is structurally ready. Phase 2 begins on operator authorization.

---

## 12. What this audit does NOT do

- Does NOT make architecture decisions (Step 8 holds)
- Does NOT modify procedure v1.0
- Does NOT iterate constitutional layer v0.4
- Does NOT adopt or reject candidate patterns
- Does NOT recommend any specific compression core (S0-S4 are options)
- Does NOT trigger Phase 2 entry
- Does NOT close T1-T7 unresolved tensions

## 13. What this audit does

- Enumerates surviving A-tagged behaviors (§1)
- Enumerates unresolved B/C-tagged behaviors (§2)
- Separates prompting-portable from architecture-dependent differentiators (§3)
- Surfaces cost concentration with compression-floor finding (§4)
- Identifies recurring vs partial-recurring vs absent patterns (§5)
- Records 7 unresolved tensions (T1-T7) (§6)
- Enumerates 6 decision dimensions with independent option sets (§7)
- Enumerates 5 smallest-buildable-core candidates (S0-S4) (§8)
- Names 8 over-compression risks + 8 under-compression risks (§9-10)
- Records Phase 2 gate state (§11)

---

## 14. Cross-references

- `results/step_6_cross_case_analysis.md`
- `results/step_7_reclassification.md`
- `results/step_8_architecture_decision.md` — Step 8 selected core S1; this audit lists alternatives
- `procedure/abcd_classification_system.md`
- `procedure/elif_mode_procedure_v1.0.md`
- `doctrine/06_constitutional_layer_v0_4.md`
- `notes/long_range_roadmap_v0_1.md`
- Parallel overnight deliverables: `cost_signal_compression_analysis.md`, `cross_case_structural_heatmap.md`, `frontier_llm_capability_audit.md`, `minimal_buildability_mapping.md`, `anti_drift_audit.md`, `phase_9_exploratory_projection.md`
