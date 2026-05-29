# Frontier-LLM Capability Audit

**Status:** Overnight preparation deliverable 2026-05-28. **NOT a decision document.** Honest evidence-first assessment of which observed ELIF behaviors already appear latent in frontier LLMs without procedural enforcement.

**Scope:** clarify what ELIF needs architecture for vs what frontier LLMs already weakly possess. No conclusions. Recording only. The contamination caveat from Step 6 §1 applies: Conditions A and B were not produced by a clean-session bare LLM.

**Inputs:** `results/step_6_cross_case_analysis.md` (especially §2.2 substantive differentiators and the D12 baseline-frame-rejection observation), per-case Conditions A and B outputs, public observations about frontier LLM behavior on similar input-frame shapes.

---

## 1. Audit method

For each behavior class observed in ELIF Condition C, classify:

- **Class L (Latent):** behavior appears in Condition A (bare LLM, no scaffold) — evidence for frontier-LLM possession
- **Class P (Promptable):** behavior appears in Condition B (structured-reasoning prompt) but not Condition A — evidence for promptable possession
- **Class A-dep (Architecture-dependent):** behavior appears only in Condition C — evidence for procedure enforcement requirement

**Caveat (carried from Step 6):** all three conditions ran in the same LLM session. "Bare" Condition A may have been informed by the operator's framing earlier in conversation. A truly clean-session test has not been performed.

---

## 2. Behavior-class assessment per observed differentiator

### 2.1 Frame humility (Article II territory)

**ELIF surface:** Frame Validator (Step 1), one-of-three verdict; explicit `frame malformed` output permitted.

**Frontier-LLM observation:**
- **D12** (frame-rejection-narrative in baseline) appeared in Condition A in 3/3 cases.
- **Class:** L (latent).
- **Honest reading:** baseline LLMs *narratively* express frame-humility when input frames are transparently bundle-binary. The architecture's contribution is *form*: one-of-three explicit verdict + downstream anchor.
- **What frontier LLMs weakly possess:** narrative recognition of malformed framing.
- **What architecture adds:** structural one-of-three commitment that downstream steps can reference.

**Strength of evidence:** medium. The operator's cross-case observation is explicit on this. Single-session contamination may inflate Condition A's frame-humility (the operator framed the cases in conversation before Condition A ran).

### 2.2 Decomposition tendency (Object Decomposer territory)

**ELIF surface:** Step 2 named-axis decomposition with rationale.

**Frontier-LLM observation:**
- Conditions A and B produced decomposition *narratively* in 3/3 cases (per Step 6 §3.1: "narrative decomposition without named-axis structure").
- **Class:** L for substance; A-dep for named-axis form.
- **Honest reading:** decomposition is a default LLM tendency on multi-component prompts. The architecture's contribution is *named-axis discipline* with rationale.
- **What frontier LLMs weakly possess:** decomposition behavior, narrative-form.
- **What architecture adds:** axis-naming, rationale capture, content-derived axis selection that's reviewable (D18).

**Strength of evidence:** strong. Three independent baseline conditions decomposed without prompting.

### 2.3 Uncertainty expression

**ELIF surface:** Step 3 enumerated assumptions; Step 11 unresolved-uncertainty sources tied to confidence claims.

**Frontier-LLM observation:**
- Condition B's "deepest uncertainties" sections had partial content overlap with Step 3 assumptions in 3/3 cases (per Step 6 §2.1 D2 entry).
- Condition A engaged uncertainty *narratively* in 3/3 cases.
- **Class:** L for narrative; P for enumerated-uncertainty form; A-dep for enumerated-declarative-statement form (not questions, not prose).
- **Honest reading:** uncertainty expression is reachable via structured prompting. Architecture-specific contribution is the declarative-statement form (Step 3) and the tying-discipline (Step 11).
- **What frontier LLMs weakly possess:** uncertainty awareness, partial enumeration when prompted.
- **What architecture adds:** statement-form rejection of question-form entries; tying each confidence claim to a named uncertainty source.

**Strength of evidence:** strong. Step 6 §2.1 D2 explicitly notes the partial overlap.

### 2.4 Governance language (constrain / refuse / abstain)

**ELIF surface:** Step 9 Governance Kernel one-of-three verdict.

**Frontier-LLM observation:**
- Condition B reached refuse/constrain substantively in 3/3 cases (per Step 6 §2.1 D8 entry: "substantively yes").
- Condition A reached the same substantive governance recommendation in 3/3 cases (D13 substantively portable).
- **Class:** L for substance; A-dep for one-of-three explicit form.
- **Honest reading:** **this is the strongest "substance fully portable" case in the entire evidence base.** Frontier LLMs reach the governance recommendation without procedural enforcement.
- **What frontier LLMs weakly possess:** governance recommendation, substantive constrain/refuse content.
- **What architecture adds:** one-of-three explicit form (no narrative-only output); halt-condition language; structural verdict that's machine-actionable.

**Strength of evidence:** strong. The substance-portability finding is consistent across all three cases.

### 2.5 Multi-scale reasoning

**ELIF surface:** Step 6 multi-scale mapping with cross-scale relations.

**Frontier-LLM observation:**
- Conditions A and B did **NOT** produce comparable cross-scale relations in any of the three cases (per Step 6 §2.1 D5 entry, Step 7 §3).
- Multi-scale awareness narratively appeared in some Condition A outputs (mentions of "individual / institutional / civilizational"), but cross-scale relation explicit naming was absent.
- **Class:** L for multi-scale awareness; A-dep for cross-scale relations.
- **Honest reading:** the architecture-dependence here is real but bounded. Multi-scale awareness is latent; cross-scale relation *naming* requires procedural enforcement.
- **What frontier LLMs weakly possess:** multi-scale awareness as narrative.
- **What architecture adds:** explicit naming of cross-scale relations as decomposition output.

**Strength of evidence:** strong for cross-scale relations being architecture-dependent in 3/3 cases.

### 2.6 Hypothesis falsifiability

**ELIF surface:** Steps 4-5 hypotheses with explicit distinguishing predictions + failure conditions.

**Frontier-LLM observation:**
- Conditions A and B produced **no comparable** pre-registered hypothesis-with-failure-condition structure in 3/3 cases (per Step 6 §2.1 D3, D4).
- **Class:** A-dep.
- **Honest reading:** **this is the cleanest architecture-dependent capacity in the evidence base.** Frontier LLMs do not produce pre-registered falsifiability without procedural enforcement.
- **What frontier LLMs weakly possess:** narrative hypothesis-generation; some informal failure-mode mention.
- **What architecture adds:** the *pre-registration* discipline — hypotheses with failure conditions stated BEFORE any test, structurally distinct from post-hoc rationalization.

**Strength of evidence:** very strong. 3/3 absence in baseline.

### 2.7 Stage-gated routing

**ELIF surface:** Step 8 stage-gated roadmap with continuation gate per stage.

**Frontier-LLM observation:**
- Conditions A and B produced recommendations without staged continuation-gate structure in 3/3 cases (per Step 6 §2.1 D7).
- **Class:** A-dep.
- **Honest reading:** strong architecture-dependence. Continuation-gating per stage requires the BRE structural commitment.
- **What frontier LLMs weakly possess:** narrative "if X then Y" expressions.
- **What architecture adds:** explicit testable continuation gate per stage that survives review.

**Strength of evidence:** strong.

### 2.8 Operative vs theoretical separation

**ELIF surface:** Step 10 discrete-section separation.

**Frontier-LLM observation:**
- Conditions A and B mixed operative and theoretical content in 3/3 cases (per Step 6 §2.1 D9, §4.2 row 10).
- **Class:** A-dep.
- **Honest reading:** clear architecture-dependence. The separation is procedurally enforced.
- **What frontier LLMs weakly possess:** awareness of the distinction when explicitly prompted; not structural separation.
- **What architecture adds:** discrete-section commitment that downstream consumers can reference.

**Strength of evidence:** strong.

### 2.9 Longitudinal capacity tracking (Memory Logger)

**ELIF surface:** Step 12 entries with category tags and line-refs.

**Frontier-LLM observation:**
- Conditions A and B do not produce longitudinal-tracking artifacts (per Step 6 §2.1 D11).
- **Class:** A-dep purely.
- **Honest reading:** Memory Logger has no in-case purpose; it exists to enable cross-case Article VII tracking. This is procedural by construction.
- **What frontier LLMs weakly possess:** nothing comparable (no longitudinal substrate).
- **What architecture adds:** the substrate itself.

**Strength of evidence:** definitional.

### 2.10 Substantive recommendation patterns (D13 / D14 / D15 / D16 / D17)

**ELIF surface:** content-level patterns observed across Conditions A, B, C.

**Frontier-LLM observation:**
- **D13** (refuse-bundle-with-disaggregated-constraint): 3/3 in A, B, C. **Class L.**
- **D14** (parallel-funding mandate): 3/3 in A, B, C. **Class L.**
- **D15** (proposer meta-uncertainty): partial in A and B; explicit in C. **Class L for substance; P for explicit form.**
- **D16** (reversibility-axis): 2/3 with content-derived selection. **Class L.**
- **D17** (deeper-frame-rejection): 2/3 domain-emergent. **Class L.**

**Honest reading:** all substantive content patterns are baseline-reachable. The architecture's contribution is form-traceability + recoverability, not novel substance.

**Strength of evidence:** strong. This is the central frontier-LLM-portability finding.

---

## 3. Summary table — what frontier LLMs already weakly possess

| Behavior | Latency (L) | Promptable (P) | Architecture-dependent (A-dep) | Honest assessment |
|---|---|---|---|---|
| Frame humility (narrative) | ✓ | ✓ | (form) | Substance latent; form requires architecture |
| Decomposition (narrative) | ✓ | ✓ | (named-axis) | Substance latent; named-axis form requires architecture |
| Uncertainty expression (narrative) | ✓ | ✓ | (declarative-form) | Substance latent; statement-form requires architecture |
| Governance recommendation (substance) | ✓ | ✓ | (one-of-three) | Strongest substance-portability finding |
| Multi-scale awareness (narrative) | ✓ | partial | (cross-scale relations) | Awareness latent; cross-scale relations require architecture |
| Hypothesis falsifiability (pre-registered) | ✗ | ✗ | **✓ (strong)** | **Cleanest architecture-dependent capacity** |
| Stage-gated continuation | ✗ | ✗ | **✓ (strong)** | Clean architecture-dependent capacity |
| Operative/theoretical separation | ✗ | ✗ | **✓ (strong)** | Clean architecture-dependent capacity |
| Longitudinal capacity tracking | ✗ | ✗ | **✓ (definitional)** | Memory Logger is the substrate |
| Substantive patterns (refuse-bundle / parallel-funding / reversibility) | ✓ | ✓ | (form-traceability) | Substance fully baseline-reachable |

---

## 4. What ELIF truly needs architecture for (preliminary cold reading)

Concentrating on the A-dep column with strong evidence:

### N1 — Pre-registered hypothesis falsifiability (Steps 4-5)
The architecture's clearest contribution. Frontier LLMs do not produce pre-registered hypotheses with failure conditions absent explicit procedural enforcement. **~20% of Condition C cost.**

### N2 — Stage-gated continuation (Step 8)
Continuation-gating per stage is structural. Conditions A and B do not produce comparable output. **~15% of Condition C cost.**

### N3 — Operative/theoretical separation (Step 10)
Discrete-section commitment vs narrative-mix. **~7% of Condition C cost.**

### N4 — Cross-scale relation naming (Step 6 sub-behavior of Step 2)
Multi-scale awareness is latent; explicit cross-scale relation production is architecture-dependent. **~8% of Condition C cost.**

### N5 — Longitudinal capacity substrate (Step 12)
Memory Logger has no in-case alternative. **~9% of Condition C cost.**

**Aggregate:** ~59% of Condition C cost concentrates in the strong-architecture-dependent capacity. The remainder (~41%) is either form-traceability over portable substance (Steps 1, 2, 3, 9, 11) or unresolved (Step 7).

---

## 5. What ELIF does NOT need architecture for (preliminary cold reading)

Concentrating on L+P columns:

### NP1 — Substantive frame humility
Baseline LLMs narratively express frame humility on transparently bundled inputs.

### NP2 — Substantive governance recommendation
Refuse-bundle-with-disaggregated-constraint is reachable in baseline.

### NP3 — Substantive uncertainty expression
Frontier LLMs express uncertainty without procedural enforcement.

### NP4 — Substantive decomposition
Decomposition is a default LLM tendency on multi-component prompts.

### NP5 — Substantive patterns (parallel-funding, meta-uncertainty)
Reachable across A, B, C.

**Aggregate:** the substantive content patterns are largely baseline-reachable. The architecture's contribution to these is form-traceability + reviewability + machine-actionability, NOT novel substance.

---

## 6. The frontier-LLM-trajectory variable

The architecture-dependence claims rest on the current frontier LLM capability. A future LLM iteration with more elaborate baseline reasoning or with Condition-B-style structured-reasoning baked in may close gaps on form-architecture-dependent differentiators (D1, D2, D6, D8, D10).

Differentiators most exposed to frontier-LLM-trajectory closure:
- D1 (frame-validation form) — frontier LLMs increasingly produce structural verdicts
- D2 (enumerated declarative assumptions) — chain-of-thought + structured-output trends close form gap
- D6 (`outside-original-frame` tagging) — explicit tagging is a prompting pattern
- D8 (governance one-of-three) — instruction-following increasingly produces structured outputs
- D10 (tying-discipline) — output-shape compliance is a frontier-LLM-trajectory variable

Differentiators **least exposed** to frontier-LLM-trajectory closure:
- D3, D4 (pre-registered hypothesis falsifiability) — requires meta-discipline not closed by current trajectory
- D7 (stage-gated continuation) — structural commitment to continuation-gating is not a default LLM tendency
- D9 (operative/theoretical separation) — requires sustained section discipline
- D11 (longitudinal substrate) — definitionally architectural

**Implication for the working hypothesis:** ELIF's architecture-dependence is strongest in capacities that the frontier-LLM trajectory does not naturally close. The form-architecture-dependence on D1, D2, D6, D8, D10 may compress under frontier-LLM evolution. The substance-portability finding is already at the limit.

---

## 7. Honest tensions

### TH1 — Single-session contamination
All three Conditions A, B, C ran in the same LLM session. "Bare" Condition A means "no scaffold" not "no prior context." The operator framed the cases in conversation before Condition A ran. The latency claims (Class L) may be inflated by this contamination.

**What would resolve:** a clean-session bare-LLM run on the same case input frame.

### TH2 — Condition B is a single prompting style, not the prompting capability envelope
Condition B in this benchmark uses one "structured reasoning" prompt. Frontier LLMs respond to a wide envelope of prompting styles. A more elaborate Condition B may close gaps on D1, D2, D6, D8, D10.

**What would resolve:** multiple Condition B variants with progressively more elaborate prompting; measure where the gap closes.

### TH3 — Bundle-binary input-frame shape
All three cases shared bundle-binary closure shape. Frontier-LLM behavior on bundle-binary inputs may be a special case (the bundling is transparent enough to trigger latent frame-humility). Less-transparent input frames may not engage Class L behaviors.

**What would resolve:** a 4th case with non-bundle-binary input frame; measure whether Class L behaviors still hold.

### TH4 — Frontier-LLM trajectory uncertainty
The architecture-dependence claims are a function of *current* frontier LLM capability. They may erode over time as LLMs improve. This is not a benchmark failure; it is the natural shape of the architecture-dependence claim.

**What would resolve:** longitudinal benchmark re-execution as frontier LLMs evolve.

---

## 8. What this audit does NOT do

- Does NOT conclude that ELIF is unnecessary
- Does NOT conclude that ELIF is necessary
- Does NOT modify procedure v1.0
- Does NOT iterate constitutional layer
- Does NOT recommend specific compression based on portability findings
- Does NOT collapse N1-N5 into a "smallest core" — that is Minimal Buildability Mapping territory
- Does NOT measure with adversarial frontier-LLM prompting (would require additional case runs)

## 9. What this audit does

- Classifies 10 behavior categories by L / P / A-dep (§2-3)
- Identifies 5 strong architecture-dependent capacities (§4)
- Identifies 5 substantive patterns largely baseline-reachable (§5)
- Names which differentiators are most + least exposed to frontier-LLM trajectory closure (§6)
- Surfaces 4 honest tensions in the audit method itself (§7)

---

## 10. Cross-references

- `results/step_6_cross_case_analysis.md` (especially §1 contamination caveat, §2.2 substantive differentiators, §3.1 component engagement, §4.2 per-step signal observation)
- `results/case_NN/condition_a_output.md`, `results/case_NN/condition_b_output.md` for per-condition substance
- `doctrine/06_constitutional_layer_v0_4.md` (Article II frame humility framing)
- Parallel overnight deliverables (`step_8_prep_audit.md` §6 lists tensions T1-T7 that overlap with TH1-TH4 here; `minimal_buildability_mapping.md` uses §4 N1-N5 as input)
