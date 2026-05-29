# SCAFFOLD NOTE — READ BEFORE TOUCHING THIS DIRECTORY

This directory encodes the v0.1 architecture from
`notes/step_8_decision_package_v0_1.md` in Python module structure.

## Hard constraints

1. **Every component method raises `NotImplementedError`. Do not call.**
2. `ProcedureRunner.run` raises `NonSelfPropagationError`. Do not bypass it.
3. The CLI is a notice. It does not invoke the runner.
4. The closed-set tuples in `base.py` are doctrinal. Adding entries is a
   doctrine-revision act, not a refactor.

## Authorization status

- **Granted (2026-05-29):** construction PLANNING for ELIF v0.1.
- **Not granted:** implementation of Memory Logger, orchestration runner,
  component prompts, or anything beyond stubs.

Implementation requires a separate, explicit operator build authorization.

## What you can safely do in this scaffold

- Read the structure to understand the v0.1 architecture
- Run the test suite (it verifies the scaffold, not behavior)
- Reference the schemas (they are the canonical contract)
- Reference component class names + signatures in design docs

## What you cannot safely do

- Implement any `NotImplementedError` method body
- Add an 8th component (Step 8 §1 explicit rejection)
- Expand `PROCEDURE_STEP_IDS` past 11
- Wire `cli.main` to `ProcedureRunner.run`
- Have the scaffold do real I/O of any kind

Violating these is not a refactor — it is a doctrinal breach that bypasses
the operator's planning-vs-build gate.
