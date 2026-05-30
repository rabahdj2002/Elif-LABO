# ELIF v0.1 alpha cost + complexity report

**Captured:** 2026-05-30
**Mode:** offline fixture replay (decision §8.8)
**Smoke command:** `python3 -m src.elif_v0_1.replay --offline`

This report aggregates four cost axes for the v0.1 alpha:

1. **Runtime cost** — LLM calls per run (live + offline)
2. **Complexity cost** — LoC per component
3. **Maintenance cost** — per-component dependency notes
4. **Procedural overhead** — per-step latency in offline mode

It closes with a revisit of the 2.8x expansion floor estimate in the build
plan against the measured shape of the alpha.

---

## §1 Runtime cost

### Offline mode (alpha replay)

| component | LLM calls per case | cost USD |
|---|---|---|
| frame_validator (Step 1 + Step 3 + Step 7-modeB) | 3 | 0.00 |
| object_decomposer (Step 2 + Step 6) | 2 | 0.00 |
| hypothesis_validator (Step 4 + Step 5) | 2 | 0.00 |
| branching_roadmap_engine (Step 7-modeA + Step 8) | 2 | 0.00 |
| governance_kernel (Step 9) | 1 | 0.00 |
| operative_truth_separator (Step 10) | 0 (runner halts before) | 0.00 |
| memory_logger (Step 11) | 0 (no LLM; runner halts before) | 0.00 |
| **per case total** | **10 calls (offline; each loads one fixture)** | **0.00** |
| **cohort total (3 cases)** | **30 calls (offline)** | **0.00** |

The per-call cap is operator-locked at 22 per `--max-llm-calls` (decision
§8.4). The current alpha consumes 10 of 22 per case; the headroom (12
unused per case) absorbs Step 10 + Step 11 + retry budget under live mode.

### Live mode estimate (claude-sonnet-4-6 per §8.1)

Estimating 10-12 calls per case at average input ~2k tokens / output ~1k
tokens (per-step structured-output budgets):

- Input: 10 calls * 2000 tok = 20,000 tok @ $3.00/MTok = $0.06
- Output: 10 calls * 1000 tok = 10,000 tok @ $15.00/MTok = $0.15
- **Per case: ~$0.21**
- **Three-case cohort: ~$0.63**

Per the task brief, a $20 live-mode baseline subsumes ~95x case-cohort
runs, far exceeding the cap. The baseline is comfortable; offline mode is
free.

---

## §2 Complexity cost — LoC per component

Measured via `find /home/dev/elif-lab/src/elif_v0_1 -name *.py | xargs wc -l`.

### Components

| component | LoC | LoC/owned-step |
|---|---|---|
| frame_validator | 270 | 90 (3 steps: 1, 3, 7-modeB) |
| object_decomposer | 323 | 161 (2 steps: 2, 6) |
| hypothesis_validator | 383 | 191 (2 steps: 4, 5) |
| branching_roadmap_engine | 415 | 207 (2 steps: 7-modeA, 8) |
| governance_kernel | 366 | 366 (1 step: 9) |
| operative_truth_separator | 207 | 207 (1 step: 10) |
| memory_logger | 569 | 569 (1 step: 11 + persistence) |
| **components total** | **2,533** | **230 avg** |

### Foundation

| module | LoC |
|---|---|
| base.py | 123 |
| run_context.py | 172 |
| llm_adapter.py | 279 |
| schemas/__init__.py | 508 |
| orchestration_runner.py | 493 |
| replay/__init__.py | 689 |
| replay/__main__.py | 70 |
| cli.py | 175 |
| __init__.py | 87 |
| **foundation total** | **2,596** |

### Tests

| module | LoC |
|---|---|
| test_branching_roadmap_engine | 374 |
| test_governance_kernel | 371 |
| test_hypothesis_validator | 365 |
| test_memory_logger | 405 |
| test_object_decomposer | 281 |
| test_orchestration_runner | 356 |
| test_frame_validator | 250 |
| test_llm_adapter | 206 |
| test_run_context | 164 |
| test_schemas | 149 |
| test_closed_sets | 129 |
| test_replay | 129 |
| test_scaffold_imports | 116 |
| **tests total** | **3,295** |

### Grand totals

| section | LoC |
|---|---|
| components | 2,533 |
| foundation (incl. runner + replay) | 2,596 |
| tests | 3,295 |
| **all v0.1** | **8,424** |

(Above counts include `__init__.py`s; trailing whitespace and blank lines
are not stripped per `wc -l` convention.)

---

## §3 Maintenance cost — per-component dependency notes

### frame_validator
- Depends on: base (InputFrame, ELIFError), llm_adapter, run_context, schemas.
- No cross-component import. Step 7 split is mode B only.
- Stability: pinned signatures; ctor takes run_context; methods are stateless per §8.9.

### object_decomposer
- Depends on: base, llm_adapter, run_context, schemas (STEP_2, STEP_6).
- No cross-component import. Reads Step 2 decomposition as Step 6 input.
- Stability: methods take run_context as keyword; semantic post-validation
  beyond JSON schema enforces axis/family counts.

### hypothesis_validator
- Depends on: base, llm_adapter, run_context, schemas (STEP_2, STEP_4, STEP_5).
- No cross-component import. Reads Step 2 decomposition + Step 4 hypotheses.
- Stability: methods take run_context as keyword; semantic post-validation
  enforces distinguishing_prediction + fails_if.

### branching_roadmap_engine
- Depends on: base, llm_adapter, run_context, schemas (STEP_4, STEP_5, STEP_7, STEP_8).
- No cross-component import. Reads Step 4 + Step 5 inputs.
- Stability: ctor takes run_context; emits only `outside-original-frame` tag
  (mode B reserved for frame_validator per §8.10).

### governance_kernel
- Depends on: base, llm_adapter, run_context, schemas (STEP_8, STEP_9).
- No cross-component import. Reads Step 8 roadmap + dict of prior steps.
- Stability: closed-set verdict vocabulary cited in prompt; absorbs old
  Step 11 (confidence + uncertainty) per Step 8 compression.

### operative_truth_separator
- Depends on: base, llm_adapter, run_context, schemas (STEP_10).
- No cross-component import.
- Stability: 207 LoC; method takes run_context; never executed in alpha
  replay because runner halts at Step 9 refuse.

### memory_logger
- Depends on: base (InputFrame, ELIFError), schemas (SCHEMA_VERSION).
- No LLM calls (decision §8.10: architecture-dependent, takes no
  run_context).
- Stability: append-only JSONL; events keyed by case_id; closed-set
  event_types and change_types.
- **Architectural risk:** the only component with persistent state. JSONL
  schema drift is the load-bearing maintenance concern.

### orchestration_runner
- Depends on: ALL 7 components + base + run_context + llm_adapter.
- This is the integration surface. Maintenance is dominated by:
  - Step-owner table consistency assertions (fails at construction if
    closed-set drifts).
  - Halt code mapping (10 / 20 / 30 — per build plan §4.4).
  - Refusal flow correctness (the alpha-surfaced Step 10/11 gap is here).

### replay
- Depends on: base, llm_adapter, run_context, schemas, orchestration_runner.
- Reads cases/ inputs + results/ references. Writes nothing.
- Stability: includes per-component fallback path for runner unavailability.

---

## §4 Procedural overhead — per-step latency

Measured in offline-fixture mode (no network):

| step | dominant cost | wall-clock (offline) |
|---|---|---|
| step_1 | fixture load + JSON parse + schema validate | <1 ms |
| step_2 | fixture load + JSON parse + schema + semantic validate | <2 ms |
| step_3 | fixture load + schema | <1 ms |
| step_4 | fixture load + schema | <1 ms |
| step_5 | fixture load + schema | <1 ms |
| step_6 | fixture load + schema + semantic validate | <2 ms |
| step_7 (mode A + mode B) | 2 fixture loads + 2 schemas | <2 ms |
| step_8 | fixture load + schema | <1 ms |
| step_9 | fixture load + schema | <1 ms |
| step_10 | N/A (halted) | 0 ms |
| step_11 | N/A (halted) | 0 ms |
| **per-case total** | **fixture-bound** | **~10-15 ms** |
| **cohort (3 cases)** | **~30-45 ms wall** | observed ~120 ms incl. import |

In live mode, per-step latency is bounded by the Anthropic API (typically
2-5s per structured-output tool call). Per-case wall: 20-50s. Cohort
wall: 60-150s.

---

## §5 2.8x expansion floor revisit

**Build plan §5 estimated** (from `notes/elif_v0_1_build_plan.md`): the
v0.1 implementation would expand to ~2.8x the scaffold's LoC, where the
scaffold was estimated at ~1,200-1,500 LoC.

**Original estimate (from build plan):**
- Scaffold: ~1,400 LoC
- v0.1 implementation expansion floor: 2.8x = ~3,920 LoC for code
- Plus tests at ~1.5x code = ~5,880 LoC test
- **Total estimate: ~9,800 LoC**

**Measured (this alpha):**
- Components: 2,533 LoC
- Foundation (runner, replay, schemas, base): 2,596 LoC
- Implementation code total: 5,129 LoC
- Tests: 3,295 LoC
- **Total measured: 8,424 LoC**

**Ratio observation:**
- Implementation code (5,129) vs original scaffold estimate (1,400): **3.66x**
- This exceeds the 2.8x floor.
- Tests-to-code ratio: 3,295 / 5,129 = **0.64**
- This is BELOW the 1.5x estimate; tests are leaner than projected.

**Where the expansion went beyond 2.8x:**
1. Per-component prompt builders + closed-set vocabulary citations
   (~100-150 LoC per component beyond scaffold).
2. Semantic post-validation per component (~30-50 LoC each beyond JSON
   schema, defending against fixture/live drift).
3. Replay harness (689 LoC) — not in original scaffold estimate.
4. Memory logger persistence + closed-set event types (569 LoC vs scaffold
   ~50 LoC; ~10x for the architecture-dependent component).

**Where the expansion stayed BELOW estimate:**
1. Tests are 0.64x code, not 1.5x — fewer/leaner test files than budgeted.
2. The scaffold-to-implementation transition kept method signatures pinned
   (no signature explosion).

**Conclusion:** the 2.8x floor underestimated component-level prompt +
validation cost by ~30%, but tests came in 60% lighter than budgeted, so
the all-in total (8,424) is within ~15% of the original estimate (9,800).
The estimate stands as a rough order-of-magnitude marker; the actual
distribution shifted from "lots of tests" to "lots of validation in code."

---

## §6 Cost summary

- **Cohort run cost (offline):** 30 LLM-call slots consumed, $0.00 spent.
- **Cohort run cost (live estimate):** ~$0.63 at sonnet-4-6 list pricing.
- **Live budget at $20 baseline:** ~95 cohort runs (~285 individual cases).
- **Implementation LoC:** 8,424 (5,129 code + 3,295 tests).
- **Per-step latency offline:** <2 ms per step; ~10-15 ms per case.
- **Maintenance concern surface area:** memory_logger persistence (only
  stateful component); refusal-halt path for Step 10/11 (operator
  adjudication pending).
