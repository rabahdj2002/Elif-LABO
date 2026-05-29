# Minimal Buildability Mapping

**Status:** Overnight preparation deliverable 2026-05-28. **NOT a decision document.** Engineering-only categorization.

**Scope:** map ELIF v0.1 components and procedure steps into five categories — indispensable / compressible / mergeable / removable / deferred — preparing for "smallest buildable system preserving surviving signal" engineering. **Preparatory only. No final retention decisions.**

**Inputs:** `results/step_6_cross_case_analysis.md`, `results/step_7_reclassification.md`, `results/step_8_architecture_decision.md`, `frontier_llm_capability_audit.md` §4 (5 strong architecture-dependent capacities).

---

## 1. Category definitions

- **Indispensable** — surface for which architecture-dependence is strong (no A/B analogue, no plausible frontier-LLM-trajectory closure) AND removal sacrifices signal that 3/3 evidence supports
- **Compressible** — surface that produces engagement but whose output is form-traceability over baseline-portable substance; compression preserves the form value while reducing cost surface
- **Mergeable** — surface whose function can be absorbed into another component's output shape without semantic loss
- **Removable** — surface whose substantive output is baseline-reachable AND form-value is not architecturally load-bearing
- **Deferred** — surface where evidence is insufficient for any of the above; revisit on future case

---

## 2. Per-component mapping

### 2.1 Frame Validator (Step 1 + Step 3 sub + Step 7-modeB sub)

| Sub-surface | Category | Rationale |
|---|---|---|
| Step 1 one-of-three verdict (form) | Compressible | Form-anchor for downstream steps. Cost ~3% — low; compression would not be net positive. |
| Step 1 substantive frame-rejection | Removable (substance baseline-reachable) | D12 latent in baseline (3/3). But removal of substance from architecture loses no architectural surface — substance flows through regardless. |
| Step 3 enumerated declarative assumptions (form) | Indispensable (form discipline) | Form architecture-dependent; substance partially portable. Removal would lose the statement-form discipline that constrains operator. |
| Step 3 assumption content | Removable (substance partially portable) | Content overlaps Condition B uncertainties. Substance does not depend on Step 3. |
| Step 7 Mode B deeper-frame-rejection (sub-behavior) | Deferred | 2/3 evidence; domain-emergent. Below adoption threshold but evidence-suggestive. |

**Component verdict:** retain. Form value (Step 1 verdict + Step 3 statement-form discipline) is the load-bearing contribution.

### 2.2 Object Decomposer (Step 2 + Step 6 sub)

| Sub-surface | Category | Rationale |
|---|---|---|
| Step 2 named-axis decomposition (form) | Indispensable | Named-axis discipline with rationale is form architecture-dependent; substance D18-content-derived. Cost ~10%. |
| Step 2 substance | Removable (substance baseline-reachable) | Decomposition is default LLM tendency. |
| Step 6 multi-scale awareness | Removable (substance baseline-reachable) | Multi-scale narrative present in baseline. |
| Step 6 cross-scale relation naming (sub-behavior) | Indispensable | Strong architecture-dependence in 3/3 (no A/B analogue). Cost ~8%. |

**Component verdict:** retain. Form value (named-axis + cross-scale-relation naming) is the load-bearing contribution.

### 2.3 Hypothesis Validator (Steps 4-5)

| Sub-surface | Category | Rationale |
|---|---|---|
| Step 4 hypothesis generation | Compressible? (substance partially portable) | Frontier LLMs generate hypotheses narratively. |
| Step 4 distinguishing-prediction discipline | **Indispensable** | Pre-registration is architecture-dependent (Frontier-LLM Audit §2.6 N1). |
| Step 5 failure conditions per hypothesis | **Indispensable** | Pre-registered falsifiability is the cleanest architecture-dependent capacity. |

**Component verdict:** retain. **Strongest architecture-dependent capacity in the entire evidence base.** Cost ~20% — concentrated, signal-leaning.

### 2.4 Branching Roadmap Engine (Step 7-modeA + Step 8)

| Sub-surface | Category | Rationale |
|---|---|---|
| Step 7 Mode A BRE-compositional trajectories | Mergeable into Step 8 | Per Step 8 Q7.1 selection. Trajectories that compose into Step 8 stages are upstream redundant. |
| Step 8 staged roadmap | Compressible? | Staging structure portable to skilled prompting. |
| Step 8 continuation-gate per stage | **Indispensable** | No A/B analogue in 3/3 (Frontier-LLM Audit §2.7 N2). |

**Component verdict:** retain. Step 8's continuation-gating is the load-bearing contribution. Cost ~15%.

### 2.5 Governance Kernel (Step 9 + Step 11 annotation absorbed)

| Sub-surface | Category | Rationale |
|---|---|---|
| Step 9 governance recommendation substance | Removable (substance baseline-reachable) | D13 substantively portable in 3/3. |
| Step 9 one-of-three explicit form | Compressible | Form architecture-dependent; substance fully portable. Question is whether form-value is worth the ~7% cost. |
| Step 11 confidence + uncertainty annotation (absorbed into Step 9) | Compressible (already absorbed) | Tying-discipline is form-value over portable substance. Cost ~5% absorbed. |

**Component verdict:** retain. **Most acute signal-vs-ceremony question** per Step 6 §4.2. Form-traceability defended; substance-novelty does not apply.

### 2.6 Operative Truth Separator (Step 10)

| Sub-surface | Category | Rationale |
|---|---|---|
| Step 10 discrete-section operative/theoretical separation | **Indispensable** | No A/B analogue in 3/3 (Frontier-LLM Audit §2.8 N3). Cost ~7%. |

**Component verdict:** retain. Clean architecture-dependent capacity.

### 2.7 Feedback / Memory Logger (Step 12)

| Sub-surface | Category | Rationale |
|---|---|---|
| Step 12 entries with category tags + line-refs | **Indispensable (definitional)** | No baseline analogue. Memory Logger has no in-case purpose; cross-case Article VII tracking depends on it. Cost ~9%. |

**Component verdict:** retain. Definitionally required for Article VII.

---

## 3. Per-step categorization summary

| Step | Category | Primary value | Estimated post-compression cost % |
|---|---|---|---|
| 1 | Compressible (form-anchor) | One-of-three verdict | ~3% |
| 2 | Indispensable (named-axis) | Decomposition discipline | ~10% |
| 3 | Indispensable (form) + Removable (substance) | Statement-form discipline | ~8% |
| 4-5 | **Indispensable (strongest signal)** | Pre-registered falsifiability | ~20% |
| 6 | Indispensable (cross-scale relations) | Multi-axis decomposition | ~8% |
| 7 Mode A | **Mergeable into Step 8** | (redundant) | (collapses) |
| 7 Mode B | Deferred | Article II sub-behavior | ~4% |
| 8 | **Indispensable (continuation gates)** | Stage-gated roadmap | ~15% |
| 9 | Compressible (form-traceability) | One-of-three verdict + tying-discipline | ~7% + ~5% absorbed |
| 10 | **Indispensable** | Operative/theoretical discrete sections | ~7% |
| 11 | **Mergeable into Step 9** (Step 8 selection) | (absorbed) | (collapses) |
| 12 | **Indispensable (definitional)** | Article VII substrate | ~9% |

---

## 4. Mergeable consolidation map

These mergers respect Step 8 selections + this audit's findings. **Recording only.**

### M1 — Step 11 → Step 9 (selected by Step 8)
Step 11's tying-discipline absorbs into Step 9 output shape. Step 9 cost grows by ~5% absorbed surface; Step 11 dissolves. Net ~0% change at the absorbed boundary.

### M2 — Step 7 Mode A → Step 8 (selected by Step 8)
Step 7's BRE-compositional trajectories absorb into Step 8 stage authoring upstream. ~4% removed from Step 7 surface.

### M3 — Step 7 Mode B → Frame Validator Article II sub-behavior (selected by Step 8)
Step 7's deeper-frame-rejection moves to Frame Validator. ~4% redistributed.

### M4 — Step 3 → Step 1 sub-behavior (selected by Step 8 as documented sub-behavior, not procedural merger)
Step 3 documented under Frame Validator as two-stage operation. Cost surface unchanged; granularity shifts.

### M5 — Step 6 → Step 2 sub-behavior (selected by Step 8 as documented sub-behavior, not procedural merger)
Step 6 documented under Object Decomposer as multi-axis operation. Cost surface unchanged; granularity shifts.

**Aggregate effect:** ~9% of Condition C cost relocates from procedure-step granularity to component-internal granularity. Net cost reduction estimated ~5% (Step 11 partial absorption + Step 7 Mode A removal).

---

## 5. Removable candidates (per category definitions)

A surface is removable if substance is baseline-reachable AND form-value is not architecturally load-bearing.

| Candidate | Substance baseline-reachable? | Form-value load-bearing? | Removable? |
|---|---|---|---|
| Step 1 substantive frame-rejection (substance only, not form) | YES (D12) | N/A — substance | YES (substance flows through) |
| Step 3 assumption content (substance only) | YES (partial overlap) | N/A — substance | YES (substance flows through) |
| Step 6 multi-scale awareness (narrative only, not cross-scale relations) | YES | N/A — substance | YES |
| Step 9 substantive recommendation (D13) | YES | N/A — substance | YES |
| Step 11 substantive content (per Step 7 §5) | YES | NO (form is convention) | YES (selected by Step 8) |
| Step 7 Mode A BRE-compositional content | YES (Step 8 produces same) | NO (form duplicates) | YES (selected by Step 8) |

**Aggregate:** removable substance surfaces all involve substance that is already baseline-reachable. Removing them does not affect what ELIF produces — only what ELIF takes credit for producing.

**Implication:** the "smallest buildable" reduction has a structural floor at the *architecture-dependent form contributions* — not at the substance. Form-traceability is what survives compression.

---

## 6. Deferred candidates

A surface is deferred if three-case evidence is insufficient for indispensable / removable / compressible / mergeable classification.

| Candidate | Deferral reason | Earliest revisit |
|---|---|---|
| Step 6 mechanical-floor on single-scale content | All 3 cases had multi-scale content | First single-scale case |
| Step 3 / Step 11 overlap quantification | Not measured | Phase 2 procedure v1.1 execution evidence |
| Step 7 Mode B deeper-frame-rejection adoption | 2/3 below adoption threshold (≥3 required) | 4th case engaging Mode B |
| Pattern adoption (D13/D14/D15/D16/D17) | Deprecation-pressure not applied | Non-bundle-binary input frame |
| Frontier-LLM trajectory exposure (D1/D2/D6/D8/D10) | Frontier LLMs evolving | Longitudinal re-execution |
| Constitutional v0.5 compression | No forcing evidence | Phase 2 entry |

---

## 7. Smallest-buildable engineering core (preparatory)

Given §2-6, the engineering core that preserves all indispensable surface:

| Component | Role | Indispensable surface | Cost share |
|---|---|---|---|
| Frame Validator | Step 1 + Step 3 sub + Step 7 Mode B sub | One-of-three verdict (form); statement-form discipline; Mode B sub | ~11% |
| Object Decomposer | Step 2 + Step 6 sub | Named-axis discipline + cross-scale relations | ~18% |
| Hypothesis Validator | Steps 4-5 | Pre-registered hypothesis + failure conditions | ~20% |
| Branching Roadmap Engine | Step 8 (Step 7 Mode A absorbed) | Stage-gated continuation | ~15% |
| Governance Kernel | Step 9 (Step 11 absorbed) | One-of-three verdict + tying-discipline | ~12% |
| Operative Truth Separator | Step 10 | Discrete-section separation | ~7% |
| Feedback / Memory Logger | Step 12 | Tagged entries + line-refs | ~9% |

**Aggregate retained cost:** ~92% of Condition C cost remains under this preparatory mapping. The compression net effect is ~8% reduction (Step 7 Mode A + partial Step 11 absorption + Step 1 substance overflow).

**This is consistent with Step 7 §6.1 finding:** the architecture-dependent floor (~2.8x of baseline) cannot be compressed further without sacrificing indispensable surface.

---

## 8. Engineering buildability checklist (preparatory)

If/when the operator authorizes Phase 2 v1.1 execution:

| Item | Status | Notes |
|---|---|---|
| Procedure v1.1 spec | not authored (Step 8 contract pack is the candidate) | Operator-gated |
| Memory Logger entry schema | exists at `benchmarks/article_vii_capacity_accumulation_tracking.md` | Stable |
| Article VII tracking JSON schema | exists per-case at `results/case_NN/article_vii_tracking.json` | Stable |
| Differentiator tracking schema | exists at `benchmarks/differentiator_tracking.md` | Stable |
| Step 9 absorbed Step 11 output-shape spec | not yet authored | Would author at v1.1 |
| Step 7 Mode B sub-behavior spec (Frame Validator Article II) | not yet authored | Would author at v1.1 |
| Step 3 statement-form rejection rules (sub-behavior of Step 1) | partially authored in step_to_component_mapping_audit_v1_0.md | Would refine at v1.1 |
| Step 6 multi-axis spec (sub-behavior of Step 2) | partially authored | Would refine at v1.1 |
| Time-box discipline | locked at 15 min/step v1.0 | May need rev for v1.1 |
| Memory Logger first-firing review process | not authored | Phase 2 entry consideration |

---

## 9. What this mapping does NOT do

- Does NOT remove any procedure step
- Does NOT modify procedure v1.0
- Does NOT author procedure v1.1
- Does NOT make final retention decisions
- Does NOT trigger Phase 2 entry
- Does NOT measure deferred candidates (requires future evidence)

## 10. What this mapping does

- Categorizes each component's surface as indispensable / compressible / mergeable / removable / deferred (§2)
- Per-step categorization summary (§3)
- Mergeable consolidation map M1-M5 (§4)
- Removable substance candidates (§5)
- Deferred candidate enumeration (§6)
- Smallest-buildable engineering core with cost shares (§7)
- Engineering buildability checklist (§8)

---

## 11. Cross-references

- `results/step_8_architecture_decision.md` (this audit grounds in Step 8 selections)
- `results/step_7_reclassification.md` §6 (cost concentration evidence)
- `results/step_6_cross_case_analysis.md` §4 (cost share evidence)
- `frontier_llm_capability_audit.md` §4 (5 indispensable capacities N1-N5 — match indispensable column here)
- `step_8_prep_audit.md` §7-8 (decision dimensions A-F and smallest-buildable-core candidates S0-S4)
- `procedure/abcd_classification_system.md`
