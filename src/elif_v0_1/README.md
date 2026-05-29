# ELIF v0.1 — Scaffold

This directory is a **scaffold**, not an implementation. It encodes the v0.1
architecture from `notes/step_8_decision_package_v0_1.md` in Python module
structure so the plan is concrete and reviewable without being the build itself.

## What this scaffold is

- 7 component classes (one per indispensable component per Step 8 §2)
- 1 orchestration runner (sequential, no revision)
- 1 schemas module (the load-bearing JSON contract)
- 1 CLI entry point (prints a notice; performs no work)
- Import-time consistency checks for the four closed-set tuples

Every component method raises `NotImplementedError`. The orchestration
runner raises `NonSelfPropagationError` to make the non-self-propagation
constraint structural, not merely written.

## What this scaffold is NOT

- Not a runnable procedure
- Not authorized to call an LLM or write state to disk
- Not a substitute for operator build authorization

The operator authorized **construction planning** for ELIF v0.1. This
scaffold is the deliverable of that planning. Converting any
`NotImplementedError` to a real body requires a separate, explicit build
authorization (per CLAUDE.md "Non-self-propagation" and Step 8 §12).

## Closed-set discipline

Four closed-set tuples live in `base.py`:

| Tuple | Cardinality | Doctrinal anchor |
|---|---|---|
| `COMPONENT_IDS` | 7 | Step 8 §1 (Q3.1 + Q6.1 rejected 8th component) |
| `PROCEDURE_STEP_IDS` | 11 | Step 8 §2 compression (Step 11 absorbed into Step 9; renumber) |
| `ARTICLE_IDS` | 7 | Constitutional Layer v0.4 LOCKED (Articles I-VII) |
| `FAILURE_MODE_POLES` | 4 | v0.4 four-pole failure-mode taxonomy |

Adding entries requires formal doctrine revision + operator approval, not
silent expansion. `assert_consistent()` fires at import — drift fails imports.

## How to verify the scaffold

```bash
cd /home/dev/elif-lab
python3 -m unittest discover -s src/elif_v0_1/tests -p "test_*.py" -v
```

All tests should pass without any LLM call, network access, or filesystem
mutation outside the test runner's own bookkeeping.

## Build-authorization gate

The scaffold is the artifact of the **planning** authorization granted on
2026-05-29. It remains a scaffold until the operator grants a separate
**build** authorization. Until then:

- Do not implement component bodies
- Do not implement Memory Logger persistence
- Do not wire CLI to ProcedureRunner.run()
- Do not introduce a new component or step (closed-sets are doctrinal)

See `SCAFFOLD_NOTE.md` for the loud, top-of-tree reminder.
