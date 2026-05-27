# Phase Gates — Operational Checklist

**Status:** Locked 2026-05-27. Derived from `notes/long_range_roadmap_v0_1.md`. Operator-checked at each phase transition.

**Discipline:** A gate is unsatisfied unless its evidence is recorded in the appropriate `results/` or `cases/` location. Verbal claims do not satisfy gates.

---

## Gate semantics

- **Unchecked `[ ]`** — not yet satisfied
- **Checked `[x]`** — satisfied with recorded evidence
- **Blocked `[!]`** — explicitly cannot be satisfied; phase advancement requires doctrine revision

**Rule:** advancement to Phase N+1 requires ALL Phase N gates marked `[x]`. No partial advancement.

---

## Phase 0 — Constitutional Stabilization (CURRENT)

Gates required to enter Phase 1:

- [ ] **G0.1** — Case 02 input frame authored
  - Location: `cases/case_02_policy_governance/input_frame.md`
  - Constraint: must satisfy the "good case shape" per README (reasonable optimizers disagree, but governance constraint still binds)
  - Operator-authored, not assistant-authored

- [ ] **G0.2** — Case 03 input frame authored *independently of case 02 execution*
  - Location: `cases/case_03_operational_organizational/input_frame.md`
  - Constraint: must embed ambiguity (re-org, vendor, strategic decision with conflicting signals)
  - **Must be authored BEFORE case 02 runs** (independence requirement)
  - Operator-authored

**Do-not-cross boundaries during Phase 0:**
- Do NOT begin Phase 1 until BOTH cases authored
- Do NOT iterate constitutional layer further
- Do NOT add components, articles, or new doctrine sections

---

## Phase 1 — Benchmark Execution

Gates required to enter Phase 2:

- [ ] **G1.1** — Both cases produce comparable artifacts per `procedure/benchmark_template.md`
  - Locations: `results/case_02/`, `results/case_03/`
  - Required: `condition_a_output.md`, `condition_b_output.md`, `condition_c_output.md`, `analysis.md`

- [ ] **G1.2** — Intra-case Articles I-VI evaluated per case
  - Recorded in: `results/case_NN/analysis.md`
  - Required fields: governance_impact, refusal_capability, frame_decision, operative_vs_theoretical

- [ ] **G1.3** — Longitudinal Article VII evaluated across cases 1→2→3
  - Recorded in: `results/case_NN/article_vii_tracking.json`
  - Schema: `benchmarks/article_vii_capacity_accumulation_tracking.md`

- [ ] **G1.4** — Sterile-equilibrium signature absent
  - Test: `time_delta_vs_prior_similar < 0` for similar-shape cases OR `reuse_count_total > 0` OR `capacity_change_records` populated
  - If present: Article VII demoted per pressure rule (NOT iterated)

- [ ] **G1.5** — Sovereignty-import signature absent
  - Test: no pattern with confidence ≥0.9 missing refutation conditions
  - If present: recursive Article I tightened in Phase 2

**Do-not-cross boundaries during Phase 1:**
- Do NOT propose constitutional revision based on case 2 alone — wait for case 3
- Do NOT rush case 3 to confirm case 2 — independence is the discipline
- Do NOT generalize Article VII findings before benchmark closure

---

## Phase 2 — Constitutional Compression

Gates required to enter Phase 3:

- [ ] **G2.1** — Constitutional layer evaluated for compression candidates
  - Each Article reviewed against Phase 1 evidence: load-bearing or decorative?
  - Recorded in: `doctrine/07_constitutional_compression_review.md` (to be authored at Phase 2 entry)

- [ ] **G2.2** — Operator approves compressed (or unchanged) form
  - Explicit operator sign-off required
  - Possible outcomes: v0.5 with fewer articles, OR v0.5 = v0.4 (unchanged), OR article relationships clarified

- [ ] **G2.3** — Memory Logger refined per benchmark findings
  - Recorded in: `architecture/memory_logger_v0_5.md` (to be authored)

- [ ] **G2.4** — Risk matrix updated with discovered failure modes
  - Recorded in: appended to `doctrine/06_constitutional_layer_v0_4.md` § Risk Matrix

**Do-not-cross boundaries during Phase 2:**
- Do NOT add new articles in Phase 2; only compress or merge
- Do NOT proceed to memory-bearing if compression revealed deeper structural problems

---

## Phase 3 — Minimal Architecture Emergence

Gates required to enter Phase 4:

- [ ] **G3.1** — Components implemented as specified by compressed v0.5
  - Location: TBD (`architecture/components/` or similar)
  - Operator-supervised, NOT autonomous

- [ ] **G3.2** — Integration test passes on case 1 replay without contaminating prior results

- [ ] **G3.3** — Components remain interruptible, reviewable, removable
  - Each component has explicit halt mechanism + audit log

- [ ] **G3.4** — Non-self-propagation preserved at component level
  - Components do NOT invoke each other autonomously without Governance Kernel arbitration

**Do-not-cross boundaries during Phase 3:**
- Do NOT add components beyond compressed set
- Do NOT optimize for component performance; optimize for review-ability

---

## Phase 4 — Memory-Bearing Architecture

Gates required to enter Phase 5:

- [ ] **G4.1** — Memory Logger demonstrably influences subsequent case arbitration (capacity accumulation operational)
- [ ] **G4.2** — Deprecation events occur naturally (not just additions)
- [ ] **G4.3** — No pattern claims confidence ≥0.9 without refutation conditions
- [ ] **G4.4** — Memory ossification signature absent (deprecation rate > threshold relative to addition rate)
- [ ] **G4.5** — Operator can audit, modify, or wipe Memory Logger without architectural injury

**Do-not-cross boundaries:**
- Do NOT permit Memory Logger to invoke its own deprecation
- Do NOT allow Memory Logger to author its own refutation conditions
- Do NOT permit pattern recognition to fire confidently before ≥3 cases

---

## Phase 5 — Compositional Arbitration

Gates required to enter Phase 6:

- [ ] **G5.1** — Article VII operational at scale (visible capacity accumulation, not decorative)
- [ ] **G5.2** — Frameworks remain refutable; deprecation is normal
- [ ] **G5.3** — No framework has accumulated prestige protection
- [ ] **G5.4** — Operator can compress constitutional layer further if benchmark warrants

**Do-not-cross boundaries:**
- Do NOT begin world-model integration until compositional arbitration stress-tested with contradictory cases
- Do NOT permit ELIF to invoke itself recursively without operator initiation
- Do NOT consider "wisdom" to have emerged

---

## Phase 6+ — Speculative

Gates for Phases 6-9 are listed in `notes/long_range_roadmap_v0_1.md` but are SPECULATIVE. They will be re-specified when Phase 5 closes, based on actual evidence. Do not commit to Phase 6+ gate specifics until Phase 5 evidence is in.

---

## Gate-status update protocol

When a gate is satisfied, the operator (or operator-supervised assistant):

1. Records the evidence at the location specified
2. Marks the gate `[x]` in this document
3. Notes the date of satisfaction
4. Does NOT advance to next phase until ALL gates of current phase are `[x]`

When a gate is determined to be blocked:

1. Records `[!]` with reason
2. Determines whether doctrine revision is required
3. Returns to operator for decision

---

## Meta-discipline

The phase gates themselves are corrigible. If a gate proves unsatisfiable in practice, or if a missing gate emerges, this document is revised — but only at phase transitions, not in the middle of a phase. Mid-phase gate revision is a drift vector.

**Like everything else: no gate survives by prestige.** If a gate stops serving the discipline, it compresses or is removed under benchmark evidence.
