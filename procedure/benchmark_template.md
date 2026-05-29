# Benchmark Template v1.0

**Status:** LOCKED 2026-05-28.
**Lock authority:** operator approval of three additions (differentiator entry shape, `procedure_version_used`, `execution_phase`).

Every benchmark case must produce a directly comparable artifact. Otherwise §7 component reclassification becomes interpretive.

## Required fields per case

| Field | Type | Description |
|---|---|---|
| `case_id` | string | e.g., `case_01_electroculture`, `case_02_*`, `case_03_*` |
| `domain` | string | scientific / policy / operational / etc. (informational only — does not affect procedure) |
| `procedure_version_used` | string | e.g., `v1.0`. Anchors which procedure version was executed. If the procedure evolves between case runs, this field is how comparability is preserved. |
| `execution_phase` | enum | one of `E1` / `E2` / `E3`. Records who executed the procedure (operator / third-party / prototype-assisted). |
| `input_frame` | string | the original question, verbatim. Must NOT contain ELIF vocabulary — case arrives in its native domain language. |
| `condition_a_output` | string | bare LLM answer (no scaffolding) |
| `condition_b_output` | string | structured-prompt answer |
| `condition_c_output` | string | ELIF-mode output produced via the locked procedure |
| `observed_differentiators` | list[differentiator] | per-entry shape below |
| `components_engaged` | list[string] | which of the 7 canonical components engaged (by name) |
| `components_dormant` | list[string] | which canonical components remained dormant (by name) |
| `behaviors_not_in_component_list` | list[string] | emergent unclassified behaviors |
| `prompting_portable_vs_architecture_dependent` | list[{behavior, classification, rationale}] | per behavior |
| `governance_impact` | enum | `constrain` / `refuse` / `abstain` / `annotate_only` |
| `operative_vs_theoretical` | enum | `present` / `absent` / `absent_with_logged_reason` |
| `step_12_entries` | list[memory_logger_entry] | per Step 12 of procedure v1.0 — see entry shape below |
| `time_box_overruns` | list[{step_number, observed_duration_min}] | per execution-discipline rule in procedure v1.0 |
| `notes` | string | anything benchmark-blocking |

## Entry shapes

### `differentiator` entry

| Field | Type | Description |
|---|---|---|
| `name` | string | short label (e.g., "frame-rejection", "non-local-trajectory") |
| `line_refs` | list[int] | line numbers into Condition C output where the differentiator is visible |
| `present` | bool | whether the differentiator engaged in this case |
| `rationale` | string | one-line explanation of why this counts as a differentiator |

### `memory_logger_entry` (Step 12 of procedure v1.0)

| Field | Type | Description |
|---|---|---|
| `category` | enum | one of `capacity_change` / `pattern_engaged` / `pattern_deprecated` / `judgment_act` |
| `statement` | string | declarative statement (not a question) |
| `line_refs` | list[int] | line numbers into Condition C output anchoring the entry |

## Absence logging rule

If a field is absent, record **why**. Absence is data about ELIF's domain reach. An absence without a logged reason is itself a rejection per procedure v1.0 Step 10.

## Frequency dimension

Each candidate behavior must record engagement across cases as one of:

- `0/3` — never engaged
- `1/3` — edge-case behavior
- `2/3` — recurring behavior
- `3/3` — candidate canonical component

Without frequency tracking, occasional emergence and structural persistence become conflated.

## Cross-references

- `procedure/elif_mode_procedure_v1.0.md` — the procedure whose outputs this template captures.
- `procedure/abcd_classification_system.md` — A/B/C/D tag semantics applied in `components_engaged` / `behaviors_not_in_component_list` analysis.
- `procedure/step_to_component_mapping_audit_v1_0.md` — pre-case mapping audit referenced when classifying `behaviors_not_in_component_list`.
- `benchmarks/differentiator_tracking.md` — cross-case differentiator schema.
- `benchmarks/component_engagement_tracking.md` — cross-case engagement schema.
- `benchmarks/article_vii_capacity_accumulation_tracking.md` — destination for `step_12_entries`.
