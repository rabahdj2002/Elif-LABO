# Article VII — Capacity Accumulation Tracking

**Schema (not run output).** Per-case data goes into `results/case_NN/article_vii_tracking.json`.

This schema operationalizes Article VII (Generative Reconstruction) of the v0.4 constitutional layer. Article VII requires ELIF to demonstrate **increasing capacity over time** — without claiming truth accumulation. Capacity is measured **longitudinally cross-case**, not within a single case.

**Anchor:** `doctrine/06_constitutional_layer_v0_4.md` §Article VII.

---

## The capacity vs truth distinction (binding)

- **Capacity accumulation:** ELIF gets MORE CAPABLE over time. **Observable. Permitted.**
- **Truth accumulation:** ELIF claims to know MORE truth over time. **Unobservable. Forbidden.**

Every metric in this schema measures capacity. None claim truth-approach.

---

## Per-case longitudinal metrics

Each case run records the following, with explicit reference to prior cases for cross-case comparison.

### 1. Time-to-arbitration

| Field | Type | Description |
|---|---|---|
| `time_to_first_arbitration_minutes` | int | Elapsed time from case start to first arbitrated pathway output |
| `time_to_final_convergence_minutes` | int | Elapsed time from case start to last arbitrated convergence |
| `prior_similar_shape_cases` | list[case_id] | Cases whose shape this case resembles |
| `time_delta_vs_prior_similar` | float | Time delta vs avg of `prior_similar_shape_cases`; negative = faster (Article VII signal) |

**Article VII signal:** `time_delta_vs_prior_similar < 0` for similar-shape cases (faster on second encounter). If consistently ≥ 0 across cases, Article VII may be decorative.

### 2. Compositional reuse

| Field | Type | Description |
|---|---|---|
| `prior_structures_referenced` | list[dict] | Each: `{case_id, structure_type, reuse_kind}` where `reuse_kind ∈ {direct, composed, deprecated}` |
| `reuse_count_total` | int | Total cross-case structure references in this case |
| `fresh_structures_authored` | int | New compositional structures created in this case |
| `reuse_ratio` | float | `reuse_count_total / (reuse_count_total + fresh_structures_authored)` |

**Article VII signal:** `reuse_count_total > 0` for case 2+ (composition across cases is happening). If always zero, ELIF treats each case fresh = sterile equilibrium.

**Article II override check:** any `reuse_kind=direct` reuse where Frame Validator should have rejected → flag as Article II violation (stale framing reuse).

### 3. Pattern emergence

| Field | Type | Description |
|---|---|---|
| `patterns_recognized` | list[dict] | Each: `{pattern_id, first_seen_in_case, recognition_confidence, refutation_conditions}` |
| `patterns_deprecated` | list[dict] | Each: `{pattern_id, originally_authored_in_case, deprecation_reason, deprecation_evidence}` |
| `candidate_frameworks` | list[dict] | Each: `{framework_id, supporting_case_count, deprecation_pressure_survived, adoption_status}` |

**Article VII signal:** `patterns_recognized` grows monotonically (but each pattern is refutable). `candidate_frameworks` may exist but `adoption_status` must require ≥3 supporting cases + deprecation survival + operator approval.

**Sovereignty-import detection:** any pattern recognized with `recognition_confidence > 0.9` AND missing `refutation_conditions` → flag as Article I violation (pattern claimed as truth, not invitation-to-test).

### 4. Memory Logger capacity-change records

| Field | Type | Description |
|---|---|---|
| `capacity_change_records` | list[dict] | Each: `{change_type, case_id, description, refutable_with}` where `change_type ∈ {arbitration_shortcut_added, framework_candidate_emerged, composition_path_discovered, pattern_recognition_added, judgment_act_logged}` |
| `failure_records` | list[dict] | Inherited from v0.3 Memory Logger; preserved |

**Article VII signal:** `capacity_change_records` must contain entries by case 2. If empty across all cases, Memory Logger is operating in v0.3 mode (failures only) and Article VII has no substrate.

### 5. Judgment-act log (emergent-wisdom extension)

| Field | Type | Description |
|---|---|---|
| `judgment_acts` | list[dict] | Each: `{case_id, decision_point, alternatives_considered, selected_operation, reason, consequence}` |

Judgment-acts are *not* mandated by article. They are recorded as the substrate for emergent wisdom (operational extension under v0.4, not Article VIII).

**Sovereignty-import detection:** any judgment-act where `reason` claims "this is correct" rather than "this is appropriate to this case under these conditions" → flag for review.

---

## Per-case checklist for Article VII

When running a benchmark case, the following questions must be answered explicitly in `results/case_NN/article_vii_tracking.json`:

- [ ] Has time-to-arbitration been measured vs prior similar-shape cases? (If no prior similar-shape cases, mark `prior_similar_shape_cases: []` and note baseline.)
- [ ] Are any prior cases' structures referenced? List them with `reuse_kind`.
- [ ] Are new patterns recognized? Each must carry refutation conditions.
- [ ] Are any prior patterns deprecated in this case? List with deprecation evidence.
- [ ] Memory Logger contains `capacity_change_records` entries from this case run?
- [ ] Judgment-acts logged for operation-selection moments under rule-underdetermination?
- [ ] No pattern recognized with `confidence > 0.9` AND missing refutation_conditions? (Article I check)
- [ ] No reuse where Frame Validator should have refused? (Article II check)

---

## Critical failure patterns to detect

### Sterile equilibrium signature

If across cases 2 and 3:
- All intra-case Articles I-VI satisfied
- AND `time_delta_vs_prior_similar ≥ 0` consistently
- AND `reuse_count_total = 0` consistently
- AND `capacity_change_records` empty
- AND `patterns_recognized` empty

→ Article VII is decorative; ELIF is in sterile equilibrium. The article was structurally insufficient OR Memory Logger / Branching Roadmap Engine implementations did not honor it.

**Halt condition:** if detected, demote Article VII to doctrine-only per pressure rule; do not iterate constitutional layer; investigate component-level implementation.

### Sovereignty-import signature

If across cases:
- Patterns recognized with `confidence > 0.9` AND missing `refutation_conditions`, OR
- Judgment-acts framed as "this is correct" rather than "this is appropriate to case under conditions"

→ Capacity accumulation has drifted into truth accumulation. Article I has not held under Article VII's pressure.

**Halt condition:** if detected, halt Article VII operation; review Memory Logger output; consider Article VII compression in v0.5.

---

## What this schema does NOT track

- "Correctness" of ELIF outputs (not the objective function; Article III applies)
- "Quality" of insights as subjective judgments (sovereignty-shaped)
- Inter-run improvement of LLM model itself (out of scope; ELIF tracks its own architecture, not the underlying model)
- "Ascent toward truth" (forbidden framing)

These are deliberately excluded. Article VII is operational and longitudinal, not philosophical.

---

## Status

- Schema version: v0.4.0 (matches constitutional layer v0.4)
- Locked: 2026-05-27
- Subject to revision if cases 2-3 surface benchmark-blocking ambiguity
