# Cross-Case Structural Heatmap

**Status:** Overnight preparation deliverable 2026-05-28. **NOT a decision document.** Evidence organization only.

**Scope:** tabular heatmap across Cases 01, 02, 03 showing engagement intensity, recurrence, portability likelihood, architecture-dependence likelihood, governance activation, decomposition variation, uncertainty patterns. No interpretation beyond evidence organization.

**Legend (intensity scale):**
- ⬛ — fully engaged / strongly present / 3/3 evidence
- ◧ — partially engaged / mixed evidence / 2/3
- ▢ — minimally engaged / weak signal / 1/3
- ⬜ — not engaged / 0/3
- N/A — not applicable for that case

**Inputs:** `results/step_6_cross_case_analysis.md`, `results/case_NN/article_vii_tracking.json` (referenced via step 6 synthesis), `results/step_7_reclassification.md`.

---

## 1. Component engagement intensity (per-case, per-component)

| Component | Step(s) | C01 | C02 | C03 | Aggregate | Architecture-dependent? |
|---|---|---|---|---|---|---|
| Frame Validator | 1 | ⬛ | ⬛ | ⬛ | 3/3 | partial (D1 form arch-dep; D12 substance portable) |
| Object Decomposer | 2 | ⬛ | ⬛ | ⬛ | 3/3 | partial (named-axis form vs narrative content) |
| Hypothesis Validator | 4-5 | ⬛ | ⬛ | ⬛ | 3/3 | **YES** (D3 + D4 no A/B analogue) |
| Branching Roadmap Engine | 8 | ⬛ | ⬛ | ⬛ | 3/3 | **YES** (D7 no A/B analogue) |
| Governance Kernel | 9 | ⬛ | ⬛ | ⬛ | 3/3 | partial (D8 form vs D13 substance) |
| Operative Truth Separator | 10 | ⬛ | ⬛ | ⬛ | 3/3 | **YES** (D9 no A/B analogue) |
| Feedback / Memory Logger | 12 | ⬛ | ⬛ | ⬛ | 3/3 | **YES** (D11 no A/B analogue) |
| **B-tag: Hidden assumption** | 3 | ⬛ (9) | ⬛ (8) | ⬛ (10) | 3/3 | partial |
| **B-tag: Multi-scale** | 6 | ⬛ (7+3) | ⬛ (5+3) | ⬛ (5+3) | 3/3 | **YES** (cross-scale relations no A/B analogue) |
| **B-tag: Outside-frame** | 7 | ⬛ (5) | ⬛ (3) | ⬛ (4) | 3/3 | partial / mixed |
| **C-tag: Recommendation packet** | 11 | ⬛ | ⬛ | ⬛ | 3/3 | NO (tying-form is convention) |

**Heatmap observation:** uniform ⬛ across all components in all three cases. **No dormancy detected.** No A→D demotion candidate surfaces from engagement-intensity alone.

---

## 2. Per-step recurrence frequency

| Step | Engagement | A_in_B (Condition B overlap) | A_in_A (Condition A overlap) | Differentiator IDs |
|---|---|---|---|---|
| 1 | 3/3 | partial | partial | D1, D12 |
| 2 | 3/3 | partial | partial | (no D-tagged; D18 content-derived axis) |
| 3 | 3/3 | partial | partial | D2 |
| 4 | 3/3 | no | no | D3 |
| 5 | 3/3 | no | no | D4 |
| 6 | 3/3 | no | no | D5 |
| 7 | 3/3 | partial | partial | D6, D17 (2/3) |
| 8 | 3/3 | no | no | D7 |
| 9 | 3/3 | yes (substantive) | yes (substantive) | D8, D13 |
| 10 | 3/3 | no | no | D9 |
| 11 | 3/3 | partial | partial | D10 |
| 12 | 3/3 | no | no | D11 |

**Heatmap observation:** Steps 4-5, 6, 8, 10, 12 are the cleanest "no A/B overlap" columns. Step 9 is the cleanest "yes A/B overlap" column. Steps 1, 2, 3, 7, 11 are mixed.

---

## 3. Prompting-portability likelihood (architecture-dependence inverse)

| Differentiator | Portability assessment | Source |
|---|---|---|
| D1 — Frame-validation one-of-three | partial — form arch-dep; substance reachable via B prompt | Step 6 §2.1 |
| D2 — Enumerated declarative assumptions | partial — content overlaps B "uncertainties"; statement-form arch-dep | Step 6 §2.1 |
| D3 — Hypotheses with predictions | low — no A/B analogue | Step 6 §2.1 |
| D4 — Failure conditions | low — no A/B analogue | Step 6 §2.1 |
| D5 — Multi-scale + cross-scale relation | low — no A/B analogue | Step 6 §2.1 |
| D6 — `outside-original-frame` tagging | partial — D12 narrative portable; explicit tag arch-dep | Step 6 §2.1 |
| D7 — Stage-gated roadmap | low — no A/B analogue | Step 6 §2.1 |
| D8 — Governance one-of-three | partial — D13 substance portable; form arch-dep | Step 6 §2.1 |
| D9 — Operative-vs-theoretical | low — no A/B analogue | Step 6 §2.1 |
| D10 — Tying-discipline | partial — mention portable; tying arch-dep | Step 6 §2.1 |
| D11 — Memory Logger entries | low — purely procedural; no analogue | Step 6 §2.1 |
| D12 — Frame-rejection narrative in baseline | high — present in A and B (operator's cross-case observation) | Step 6 §2.2 |
| D13 — refuse-bundle-with-disaggregated-constraint | high — substantively portable across all conditions | Step 6 §2.2 |
| D14 — Parallel-funding mandate | high — portable | Step 6 §2.2 |
| D15 — Proposer meta-uncertainty | high — both engage | Step 6 §2.2 |
| D16 — Reversibility-axis (2/3) | high — content-derived | Step 6 §2.3 |
| D17 — Deeper-frame-rejection (2/3) | partial — domain-emergent | Step 6 §2.3 |
| D18 — Content-derived decomposition axis | N/A — meta-observation | Step 6 §2.4 |

**Heatmap observation:** clean architecture-dependence concentrates in D3, D4, D5, D7, D9, D11 (six differentiators). Clean portability concentrates in D12-D16 (substantive content). Form-architecture-dependent + substance-portable is the largest mixed band (D1, D2, D6, D8, D10).

---

## 4. Architecture-dependence likelihood (signal heatmap)

Cross-tabulating §1 component engagement × §3 portability:

| Component | Step | Engagement | Architecture-dep signal | Notes |
|---|---|---|---|---|
| Hypothesis Validator | 4-5 | 3/3 | **HIGH** | D3 + D4 |
| Branching Roadmap Engine | 8 | 3/3 | **HIGH** | D7 |
| Operative Truth Separator | 10 | 3/3 | **HIGH** | D9 |
| Memory Logger | 12 | 3/3 | **HIGH** | D11 |
| Object Decomposer | 2 + 6 (sub) | 3/3 | **HIGH** (via sub-behavior) | D5 (sub-beh) |
| Frame Validator | 1 + 3 (sub) + 7-modeB (sub) | 3/3 | MEDIUM | D1 form, D2 form, D17 partial |
| Governance Kernel | 9 + 11 (annotation) | 3/3 | MEDIUM | D8 form, D10 form |
| (Step 7 Mode A) | 7 | 3/3 | LOW | BRE-compositional redundancy |
| (Step 11 standalone) | 11 | 3/3 | LOW (substance) | C-tag confirmed |

**Heatmap observation:** the smallest-real-ELIF signal concentration is in 4 components (Hypothesis Validator, BRE, Operative Truth Separator, Memory Logger) plus Object Decomposer (with multi-scale sub-behavior). Frame Validator and Governance Kernel hold form-traceability value.

---

## 5. Governance activation frequency

Per Article V/VI/VII engagement.

| Case | Governance verdict (Step 9) | Refuse? | Constrain? | Abstain? | Halt conditions triggered? |
|---|---|---|---|---|---|
| C01 (electroculture) | refuse-the-bundle + constrain-disaggregated | Yes (bundle) | Yes (components) | No | None — Article VII operational |
| C02 (autonomous AI agriculture) | refuse-the-bundle + constrain-disaggregated | Yes (bundle) | Yes (components) | No | None |
| C03 (AI mental-health) | refuse-the-bundle + constrain-disaggregated | Yes (bundle) | Yes (components) | No | None |

**Heatmap observation:** governance kernel engaged 3/3 with identical verdict shape. This is one of the cleanest 3/3 substantive convergences. Also one of the strongest signals of input-frame design dependency (all three frames had bundle-binary closure shape — see prep audit T1).

### Article-specific engagement

| Article | C01 | C02 | C03 | Notes |
|---|---|---|---|---|
| Article I — Non-absolutization | ⬛ | ⬛ | ⬛ | Refutation conditions present in all hypotheses |
| Article II — Frame humility | ⬛ | ◧ | ⬛ | D17 deeper-frame-rejection in C01+C03 only |
| Article III — No self-validation | ⬛ | ⬛ | ⬛ | External evidence anchors in all cases |
| Article IV — Partiality of models | ⬛ | ⬛ | ⬛ | Operative-vs-theoretical separation explicit (Step 10) |
| Article V — Refusal-capable | ⬛ | ⬛ | ⬛ | refuse-the-bundle 3/3 |
| Article VI — Coherent convergence | ⬛ | ⬛ | ⬛ | Stage-gated roadmap 3/3 |
| Article VII — Generative reconstruction | ⬛ | ⬛ | ⬛ | Memory Logger entries 3/3 |

**Heatmap observation:** Article II is the only article with mixed engagement (2/3 via D17 deeper-frame-rejection). All others are clean 3/3.

---

## 6. Decomposition-axis variation

Per D18 + per-case Step 2 outputs.

| Case | Load-bearing decomposition axis | Cross-scale axis (Step 6) | Variation type |
|---|---|---|---|
| C01 (electroculture) | mechanism plausibility | pseudoscience-normalization-velocity vs mechanism-testing-velocity | mechanism / temporal |
| C02 (autonomous AI agriculture) | reversibility profile (ecological/molecular) | irreversible-molecular-change vs 5-year-governance-cycle | reversibility / temporal |
| C03 (AI mental-health) | data-coupling depth + infrastructure persistence | individual-scale consent does not aggregate to civilizational-scale | governance / consent |

**Heatmap observation:** **3/3 cases use distinct load-bearing axes.** D18 is the strongest evidence against rigid procedure-imposition. The procedure produces decomposition shape (named-axis discipline); content determines which axis is load-bearing.

---

## 7. Uncertainty-handling patterns

Per per-case Step 3 + Step 11 outputs.

| Case | Step 3 assumptions | Step 11 unresolved-uncertainty sources | Overlap (qualitative) |
|---|---|---|---|
| C01 | 9 declarative statements | ≥3 sources (mechanism evidence, scaling validity, framer-incentive) | partial |
| C02 | 8 declarative statements | ≥3 sources (ecological reversibility, governance scope, control timescale) | partial |
| C03 | 10 declarative statements | ≥3 sources (consent aggregation, infrastructure permanence, data coupling) | partial |

**Heatmap observation:** uncertainty surfaces at two structural sites (Step 3 enumeration + Step 11 tying). Partial overlap unmeasured quantitatively — see Z3 in cost/signal compression analysis.

### Patterns recognized (Article VII tracking)

| Case | Patterns recorded | Reuse from prior cases | Confidence range |
|---|---|---|---|
| C01 (re-executed) | 5 | 5 | ≤0.75 |
| C02 (first run) | 4 | 0 | ≤0.75 |
| C03 (third) | 5 | 4 | ≤0.75 |

**Heatmap observation:** all patterns recorded with confidence ≤0.75 (no Sovereignty-import signature). Reuse counts grow case-over-case as expected.

---

## 8. Halt-condition signatures (Article VII tracking)

| Signature | Detected? | Per-case evidence | Action |
|---|---|---|---|
| Sterile-equilibrium (`time_delta ≥ 0` + `reuse=0` + `capacity_change=empty` + `patterns=empty`) | NO | time_delta uninstrumented; reuse non-zero in C01+C03; capacity changes recorded all three | none |
| Sovereignty-import (confidence >0.9 missing refutation) | NO | all confidence ≤0.75 with explicit refutation | none |
| Article II violation via stale-framing-reuse | NO | all reuse `composed`, applied to freshly-decomposed framing | none |

**Heatmap observation:** clean ⬜ across all halt signatures. No demotion pressure.

---

## 9. Cost intensity heatmap (estimated % of Condition C)

| Step | C01 share | C02 share | C03 share | Mean |
|---|---|---|---|---|
| 1 | ~3% | ~3% | ~3% | ~3% |
| 2 | ~10% | ~10% | ~10% | ~10% |
| 3 | ~8% | ~8% | ~8% | ~8% |
| 4-5 | ~20% | ~20% | ~20% | ~20% |
| 6 | ~8% | ~8% | ~8% | ~8% |
| 7 | ~8% | ~7% | ~9% | ~8% |
| 8 | ~15% | ~15% | ~15% | ~15% |
| 9 | ~7% | ~7% | ~7% | ~7% |
| 10 | ~7% | ~7% | ~7% | ~7% |
| 11 | ~5% | ~5% | ~5% | ~5% |
| 12 | ~9% | ~9% | ~9% | ~9% |

(Per-case shares are estimates from Step 6 §4.1 — content-block ratio at 750/600/650 baseline words and 3500/2400/3000 Condition C words; precise per-step word counts not measured.)

**Heatmap observation:** cost shares are roughly uniform across cases (procedure mechanically applies). The total Condition C expansion ratio is the per-case variable (4.76x / 4.29x / 4.38x).

---

## 10. Convergence vs divergence map

| Behavior class | C01 | C02 | C03 | Convergence |
|---|---|---|---|---|
| Procedural-form artifacts | full | full | full | **CONVERGE 3/3** |
| Substantive recommendation shape | refuse-bundle | refuse-bundle | refuse-bundle | **CONVERGE 3/3** |
| Load-bearing decomposition axis | mechanism | reversibility | governance/consent | **DIVERGE 3/3** |
| Deeper-frame-rejection (D17) | present | absent | present | **PARTIAL 2/3** |
| Reversibility-as-axis (D16) | absent | present | present | **PARTIAL 2/3** |
| Article II engagement intensity | strong | medium | strong | **MIXED** |
| Article VII reuse signal | strong (5) | none (0; first) | strong (4) | as expected |

**Heatmap observation:** the architecture converges on procedural form + substantive recommendation while diverging on content-derived decomposition axes. This is the central empirical finding the working hypothesis rests on.

---

## 11. What this heatmap does NOT do

- Does NOT interpret beyond evidence organization
- Does NOT recommend any compression / graduation / demotion
- Does NOT modify any artifact
- Does NOT make architecture decisions
- Does NOT close any unresolved tension from prep audit §6

## 12. What this heatmap does

- Organizes engagement intensity per component per case (§1)
- Organizes per-step recurrence + overlap (§2)
- Maps portability likelihood per differentiator (§3)
- Maps architecture-dependence likelihood per component (§4)
- Tracks governance activation + article-specific engagement (§5)
- Maps decomposition-axis variation (§6)
- Maps uncertainty-handling patterns + Article VII tracking (§7-8)
- Maps cost intensity per step per case (§9)
- Maps convergence/divergence shape (§10)

---

## 13. Cross-references

- `results/step_6_cross_case_analysis.md` (primary evidence base)
- `results/case_01/article_vii_tracking.json`, `results/case_02/article_vii_tracking.json`, `results/case_03/article_vii_tracking.json`
- `benchmarks/differentiator_tracking.md`
- `benchmarks/component_engagement_tracking.md`
- `benchmarks/article_vii_capacity_accumulation_tracking.md`
- Parallel overnight deliverables (specifically: `cost_signal_compression_analysis.md` §1 ranks the columns in §3 here; `frontier_llm_capability_audit.md` deepens §3 portability assessment)
