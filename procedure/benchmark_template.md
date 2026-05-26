# Benchmark Template

Every benchmark case must produce a directly comparable artifact. Otherwise the §7 component reclassification becomes interpretive.

## Required fields per case

| Field | Description |
|---|---|
| `case_id` | e.g., `case_01_electroculture` |
| `domain` | scientific / policy / operational / etc. |
| `input_frame` | the original question, verbatim |
| `condition_a_output` | bare LLM answer |
| `condition_b_output` | structured-prompt answer |
| `condition_c_output` | ELIF-mode output (produced via the locked procedure) |
| `observed_differentiators` | list, each with line refs into Condition C |
| `components_engaged` | which of the 7 canonical components engaged |
| `components_dormant` | which canonical components remained dormant |
| `behaviors_not_in_component_list` | emergent unclassified behaviors |
| `prompting_portable_vs_architecture_dependent` | per behavior |
| `governance_impact` | did governance constrain, refuse, abstain, or only annotate |
| `operative_vs_theoretical` | present / absent / absent because… |
| `notes` | anything benchmark-blocking |

## Absence logging rule

If a field is absent, record **why**. Absence is data about ELIF's domain reach.

## Frequency dimension

Each candidate behavior must record engagement across cases as one of:
- `0/3` — never engaged
- `1/3` — edge-case behavior
- `2/3` — recurring behavior
- `3/3` — candidate canonical component

Without frequency tracking, occasional emergence and structural persistence become conflated.
