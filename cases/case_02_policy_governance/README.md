# Case 02 — Policy / Governance Conflict

**Status:** Not yet authored. Must be authored independently before case 3 begins.

**Domain:** Policy / governance

**Purpose this case must serve:** Stress-test the Governance Kernel where optimization and constitutional constraint **conflict**.

## Case design constraint (non-negotiable)

The interesting test is a case where a strong optimizer would choose an answer the governance layer **refuses**. If optimization and governance coincidentally agree, the kernel hasn't been stress-tested — it has only annotated.

**Bad case shape:** the morally obvious one. Everyone agrees the constrained answer is correct.
**Good case shape:** reasonable optimizers disagree, but the governance constraint still binds.

If no such case can be constructed, that is itself a finding about the kernel's reach.

## Required artifacts (per `procedure/benchmark_template.md`)

- `input_frame.md` — the question, verbatim
- `condition_a_output.md` — bare LLM
- `condition_b_output.md` — structured prompt
- `condition_c_output.md` — ELIF-mode via the locked procedure
- `analysis.md` — observed differentiators, component engagement, governance impact

## Trigger condition

Per Rule 1 (Reality Confrontation Priority), case 2 must be executed within a fixed window after authorship, regardless of refinement opinions.
