# ELIF v0.1 — Complete Technical Build Plan

**Status:** PLANNING ONLY, 2026-05-29. Operator-authorized construction PLANNING only; this document does NOT constitute build authorization.

**Authority anchors (do not deviate):**
- `notes/step_8_decision_package_v0_1.md` — the v0.1 binding decision package
- `results/step_8_architecture_decision.md` — the LOCKED architecture decision
- `procedure/elif_mode_procedure_v1.0.md` — the locked execution procedure (v1.0 still authoritative; v1.1 candidate is in §2.2 of step_8_architecture_decision)
- `doctrine/06_constitutional_layer_v0_4.md` — the LOCKED constitutional layer (7 Articles, four-pole taxonomy)
- `architecture/00..07_*.md` — provisional component contracts

**Scope of this document:**
This plan addresses the seven operator-required deliverables in seven numbered sections plus an open-questions section (Section 8). It proposes a buildable directory layout, module boundaries, schemas, component contracts, Memory Logger design, orchestration runner, MVP scope boundary, engineering estimate, and an acceptance test pack. It does not implement those things. The plan converts to build authorization separately.

**What this plan refuses to do (smallest disposition wins, compression > expansion):**
- No 8th component (Step 8 §1 Q3.1 + Q6.1 rejected; closed-set discipline applies)
- No constitutional v0.5 speculation (v0.4 LOCKED)
- No Memory Corridor, Continuity Layer runtime, ORC, CIM, World Model, Decision Room, Civilizational layer, Adaptive population-scale feedback — all DEFERRED per operator brief 2026-05-29
- No web UI, no external API, no inter-component messaging system, no service-mesh framing
- No autonomous progression: every milestone surfaces an operator-authorization gate

---

## Section 1 — Technical Architecture

### 1.1 Repository structure (proposed layout)

The proposal extends the existing scaffold at `src/elif_v0_1/`. Existing files (`__init__.py`, `base.py`, `components/__init__.py`, `components/frame_validator.py`) remain authoritative; this plan does NOT modify them. The plan describes the eventual full layout once build is authorized.

```
/home/dev/elif-lab/
├── src/
│   └── elif_v0_1/
│       ├── __init__.py                          # public API surface, closed-set guard (EXISTS)
│       ├── base.py                              # closed-set IDs, errors, frozen data shapes (EXISTS)
│       ├── cli.py                               # CLI entry point: `elif run --case <id> --condition <a|b|c>`
│       ├── orchestration_runner.py              # 11-step procedure runner + state machine
│       ├── memory_logger.py                     # architecture-dependent Article VII persistence
│       ├── llm_adapter.py                       # frontier-LLM call abstraction (single adapter, no multi-family yet)
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── input_frame.schema.json
│       │   ├── procedure_step_output.schema.json
│       │   ├── article_vii_tracking.schema.json # references existing results/case_*/article_vii_tracking.json shape
│       │   ├── memory_logger_event.schema.json
│       │   └── run_log.schema.json
│       ├── components/
│       │   ├── __init__.py                       # imports the 7 owners (EXISTS, partial)
│       │   ├── frame_validator.py                # Step 1 + Step 3 sub + Step 7-modeB sub (EXISTS as scaffold)
│       │   ├── object_decomposer.py              # Step 2 + Step 6 sub
│       │   ├── hypothesis_validator.py           # Steps 4 + 5
│       │   ├── branching_roadmap_engine.py       # Step 7-modeA + Step 8
│       │   ├── governance_kernel.py              # Step 9 (absorbs Step 11 confidence/uncertainty)
│       │   ├── operative_truth_separator.py     # Step 10
│       │   └── memory_logger.py                  # Step 11 (post-Step-8-renumber from Step 12)
│       ├── prompts/
│       │   ├── __init__.py
│       │   ├── frame_validator.system.md
│       │   ├── object_decomposer.system.md
│       │   ├── hypothesis_validator.system.md
│       │   ├── branching_roadmap_engine.system.md
│       │   ├── governance_kernel.system.md
│       │   └── operative_truth_separator.system.md
│       │   # NB: memory_logger has NO system prompt — architecture-dependent, not prompt-portable
│       └── tests/
│           ├── __init__.py
│           ├── test_closed_set_guards.py
│           ├── test_base_dataclasses.py
│           ├── test_frame_validator.py
│           ├── test_object_decomposer.py
│           ├── test_hypothesis_validator.py
│           ├── test_branching_roadmap_engine.py
│           ├── test_governance_kernel.py
│           ├── test_operative_truth_separator.py
│           ├── test_memory_logger.py
│           ├── test_orchestration_runner.py
│           ├── test_schemas_validate.py
│           ├── test_case_01_replay.py            # benchmark replay
│           ├── test_case_02_replay.py
│           └── test_case_03_replay.py
└── results/
    ├── case_01/                                  # existing on-disk outputs (immutable reference)
    ├── case_02/
    ├── case_03/
    └── v0_1_runs/                                # NEW: per-run output dir created by orchestration runner
        ├── <run_id>/
        │   ├── input_frame.locked.json
        │   ├── per_step/
        │   │   ├── step_01.output.json
        │   │   ├── ...
        │   │   └── step_11.output.json
        │   ├── article_vii_tracking.json         # matches results/case_*/ shape
        │   ├── execution_log.jsonl               # per-step run log
        │   └── run_meta.json
        └── _index.json                            # cross-case index (Memory Logger maintained)
```

### 1.2 Module boundaries

| Module | Responsibility | Architecture-dependent? |
|---|---|---|
| `base.py` | Closed-set IDs, errors, frozen `InputFrame` / `ProcedureStepOutput` dataclasses | No (data shapes only) |
| `cli.py` | Thin entry point; argument parsing; invokes orchestration_runner | No |
| `orchestration_runner.py` | 11-step state machine; sequential execution; governance insertion; time-box enforcement | Yes (state) |
| `memory_logger.py` | Article VII persistence; cross-case index; reuse detection | Yes (persistence + cross-case) |
| `llm_adapter.py` | Single frontier-LLM call boundary; structured-output enforcement; retry budget | Yes (network) |
| `components/<name>.py` | One owner per component; methods for each step it owns | Mostly prompt-portable (6 of 7); `memory_logger.py` is architecture |
| `prompts/<name>.system.md` | System prompt for the component's LLM call | Prompt-portable artifact |
| `schemas/*.json` | JSON Schemas; runtime validation of every step output | No (declarative) |

**Rule:** one module per component + one orchestration runner + one Memory Logger + one CLI + one LLM adapter. **No cross-component imports between component files** — components communicate only via committed step outputs, never by reaching into each other's classes. This enforces step-output-as-contract discipline.

### 1.3 Data flow

```
operator: elif run --case case_NN --condition c
        │
        ▼
  cli.py
        │ loads cases/case_NN/input_frame.md
        │ constructs InputFrame (locked, frozen)
        ▼
  orchestration_runner.execute(input_frame)
        │
        ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ Step 1 → FrameValidator.validate(input_frame)               │
  │   verdict ∈ {valid, invalid, needs_decomposition}           │
  │   if invalid → RAISES FrameInvalidError, run halts          │
  │ Step 2 → ObjectDecomposer.decompose(step1.output)           │
  │ Step 3 → FrameValidator.surface_assumptions(input, step1)   │
  │ Step 4 → HypothesisValidator.hypothesize(step2.output)      │
  │ Step 5 → HypothesisValidator.failure_conditions(step4)      │
  │ Step 6 → ObjectDecomposer.multi_scale(step2)                │
  │   (optional per Q6.3: operator-judged ceremony risk)        │
  │ Step 7 → split:                                              │
  │   modeA → BranchingRoadmapEngine.outside_frame(step4)       │
  │   modeB → FrameValidator.surface_deeper_frame_rejection(…)  │
  │ Step 8 → BranchingRoadmapEngine.staged_roadmap(step7.modeA) │
  │ Step 9 → GovernanceKernel.adjudicate(step8, all prior)      │
  │   verdict ∈ {constrain, refuse, abstain}                    │
  │   output shape includes confidence + uncertainty (absorbed) │
  │   if refuse + sterile-equilibrium signature → halts         │
  │ Step 10 → OperativeTruthSeparator.separate(step9, all)      │
  │ Step 11 → MemoryLogger.entry(case_id, all step outputs)     │
  └──────────────────────────────────────────────────────────────┘
        │
        ▼
  Per-step writes:
    - results/v0_1_runs/<run_id>/per_step/step_NN.output.json
    - results/v0_1_runs/<run_id>/execution_log.jsonl (append)
  Step 11 writes:
    - results/v0_1_runs/<run_id>/article_vii_tracking.json
    - results/v0_1_runs/_index.json (Memory Logger cross-case append)
        │
        ▼
  cli.py prints run_id + path; exit code reflects governance verdict
```

**Key contract:** once a step writes its output, the output is immutable. Subsequent steps may read it; no step may mutate it. The runner is sequential and single-pass; no rollback, no revision.

### 1.4 Interfaces (per-component contract)

Every component method has the same shape: takes one or more typed inputs, returns a typed `ProcedureStepOutput` whose `content` field matches the component's structured output schema. Closed-set output codes are enumerated below.

| Component | Method | Input | Output `.content` | Closed-set codes |
|---|---|---|---|---|
| FrameValidator | `validate` | `InputFrame` | `{verdict, reformulated_frame?}` | `verdict ∈ {valid, invalid, needs_decomposition}` |
| FrameValidator | `surface_assumptions` | `InputFrame, step1_output` | `{assumptions: list[str]}` | n/a (open content; ≥2 entries; declarative form) |
| FrameValidator | `surface_deeper_frame_rejection` | `InputFrame, step1_output` | `{rejections: list[{trajectory, one_line_reason}]}` | `trajectory ∈ {deeper_frame_rejection}` (Article II tie) |
| ObjectDecomposer | `decompose` | `step1_output` | `{families: list[{family, rationale}]}` | n/a (≥2 families) |
| ObjectDecomposer | `multi_scale` | `step2_output` | `{scales: list[str], cross_scale_relations: list[str], scale_axis_engaged: bool}` | `scale_axis_engaged ∈ {true, false}` (Q6.3 optional) |
| HypothesisValidator | `hypothesize` | `step2_output` | `{hypotheses: list[{id, statement, distinguishing_prediction}]}` | n/a (each ≥1 distinguishing prediction) |
| HypothesisValidator | `failure_conditions` | `step4_output` | `{failure_conditions: list[{hypothesis_id, failure_condition}]}` | n/a (each ≥1 observable failure condition) |
| BranchingRoadmapEngine | `outside_frame` | `step4_output, step1_output` | `{trajectories: list[{tag, one_line_reason}]}` | `tag ∈ {outside_original_frame}` (≥1 entry) |
| BranchingRoadmapEngine | `staged_roadmap` | `step7_modeA_output` | `{stages: list[{stage_id, continuation_gate}]}` | n/a (each stage ≥1 testable continuation gate) |
| GovernanceKernel | `adjudicate` | `step8_output, all_prior_outputs` | `{verdict, confidence, unresolved_uncertainty_sources: list[str], constraints?, refusal_reason?}` | `verdict ∈ {constrain, refuse, abstain}` |
| OperativeTruthSeparator | `separate` | `step9_output, all_prior_outputs` | `{operative_strand?, theoretical_strand?, absence_reason?}` | exactly one of {both present, absence_reason present} |
| MemoryLogger | `entry` | `case_id, all step outputs, prior cross-case index` | `{events: list[MemoryLoggerEvent], article_vii_tracking: ArticleVIITrackingRecord}` | `event.event_type ∈ {open, close, pattern_recognized, refutation, capacity_change}` |

**Type contract:** every method returns a `ProcedureStepOutput` whose `content` field is validated against the corresponding JSON Schema at runtime by the orchestration runner before the output is committed. Schema-violation raises `ELIFError` and halts the run (no silent acceptance).

### 1.5 Schemas

Five JSON Schemas land under `src/elif_v0_1/schemas/`. Sketch (full schemas authored in build phase):

#### 1.5.1 `input_frame.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "InputFrame",
  "type": "object",
  "required": ["id", "text", "locked_at_iso", "doctrinal_scope_tag", "companion_case"],
  "properties": {
    "id": {"type": "string", "pattern": "^case_[0-9]{2,}_[a-z_]+$|^v0_1_run_[A-Za-z0-9_]+$"},
    "text": {"type": "string", "minLength": 1},
    "locked_at_iso": {"type": "string", "format": "date-time"},
    "doctrinal_scope_tag": {"type": "string", "enum": ["benchmark_replay", "phase_2_v1_1_entry", "operational_run"]},
    "companion_case": {"type": "string"}
  },
  "additionalProperties": false
}
```

#### 1.5.2 `procedure_step_output.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ProcedureStepOutput",
  "type": "object",
  "required": ["step_id", "content", "committed_at_iso", "time_box_status"],
  "properties": {
    "step_id": {"type": "string", "enum": ["step_1","step_2","step_3","step_4","step_5","step_6","step_7","step_8","step_9","step_10","step_11"]},
    "content": {"type": "object"},
    "committed_at_iso": {"type": "string", "format": "date-time"},
    "time_box_status": {"type": "string", "enum": ["within_box", "box_exceeded_output_truncated"]}
  },
  "additionalProperties": false
}
```

#### 1.5.3 `article_vii_tracking.schema.json`

Mirrors the exact shape of `results/case_01/article_vii_tracking.json` (already on disk, schema_version "v0.4.0"). Required top-level keys: `schema_version`, `case_id`, `captured_ts`, `execution_phase`, `procedure_version_used`, `execution_order_note`, `time_to_arbitration`, `compositional_reuse`, `pattern_emergence`, `memory_logger_capacity_change_records`, `failure_records`, `judgment_acts`, `article_i_check`, `article_ii_check`. See Section 3 for full subschema breakdown.

#### 1.5.4 `memory_logger_event.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MemoryLoggerEvent",
  "type": "object",
  "required": ["event_id", "event_type", "case_id", "procedure_step", "input_frame_id", "captured_ts", "payload"],
  "properties": {
    "event_id": {"type": "string"},
    "event_type": {"type": "string", "enum": ["open", "close", "pattern_recognized", "refutation", "capacity_change"]},
    "case_id": {"type": "string"},
    "procedure_step": {"type": "string", "enum": ["step_1","step_2","step_3","step_4","step_5","step_6","step_7","step_8","step_9","step_10","step_11"]},
    "input_frame_id": {"type": "string"},
    "captured_ts": {"type": "string", "format": "date-time"},
    "supersedes_event_id": {"type": "string", "description": "Set when an operator-led correction creates a new event; original event is NEVER mutated"},
    "payload": {"type": "object"}
  },
  "additionalProperties": false
}
```

#### 1.5.5 `run_log.schema.json` (per-line schema for execution_log.jsonl)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RunLogLine",
  "type": "object",
  "required": ["run_id", "ts", "step_id", "phase", "status"],
  "properties": {
    "run_id": {"type": "string"},
    "ts": {"type": "string", "format": "date-time"},
    "step_id": {"type": "string"},
    "phase": {"type": "string", "enum": ["step_start", "llm_call", "llm_response", "schema_validate", "commit", "step_complete", "time_box_overrun", "governance_halt", "frame_invalid_halt", "sterile_equilibrium_halt"]},
    "status": {"type": "string", "enum": ["ok", "warn", "error"]},
    "detail": {"type": ["string", "object", "null"]}
  },
  "additionalProperties": false
}
```

### 1.6 Component contracts (protocol-class signatures)

Each component is one class. Signatures sketch (Python typing; methods raise `NotImplementedError` in scaffold):

```python
# src/elif_v0_1/components/frame_validator.py
class FrameValidator:
    component_id = "frame_validator"
    article_ties = ("II",)
    def validate(self, input_frame: InputFrame) -> ProcedureStepOutput: ...
    def surface_assumptions(self, input_frame: InputFrame, step1: ProcedureStepOutput) -> ProcedureStepOutput: ...
    def surface_deeper_frame_rejection(self, input_frame: InputFrame, step1: ProcedureStepOutput) -> ProcedureStepOutput: ...

# src/elif_v0_1/components/object_decomposer.py
class ObjectDecomposer:
    component_id = "object_decomposer"
    article_ties = ("IV",)
    def decompose(self, step1: ProcedureStepOutput) -> ProcedureStepOutput: ...
    def multi_scale(self, step2: ProcedureStepOutput) -> ProcedureStepOutput: ...

# src/elif_v0_1/components/hypothesis_validator.py
class HypothesisValidator:
    component_id = "hypothesis_validator"
    article_ties = ("I", "III")
    def hypothesize(self, step2: ProcedureStepOutput) -> ProcedureStepOutput: ...
    def failure_conditions(self, step4: ProcedureStepOutput) -> ProcedureStepOutput: ...

# src/elif_v0_1/components/branching_roadmap_engine.py
class BranchingRoadmapEngine:
    component_id = "branching_roadmap_engine"
    article_ties = ("V", "VI", "VII")
    def outside_frame(self, step4: ProcedureStepOutput, step1: ProcedureStepOutput) -> ProcedureStepOutput: ...
    def staged_roadmap(self, step7_modeA: ProcedureStepOutput) -> ProcedureStepOutput: ...

# src/elif_v0_1/components/governance_kernel.py
class GovernanceKernel:
    component_id = "governance_kernel"
    article_ties = ("V", "VI", "VII")
    def adjudicate(self, step8: ProcedureStepOutput, prior: dict[str, ProcedureStepOutput]) -> ProcedureStepOutput: ...

# src/elif_v0_1/components/operative_truth_separator.py
class OperativeTruthSeparator:
    component_id = "operative_truth_separator"
    article_ties = ("IV",)
    def separate(self, step9: ProcedureStepOutput, prior: dict[str, ProcedureStepOutput]) -> ProcedureStepOutput: ...

# src/elif_v0_1/components/memory_logger.py
class MemoryLogger:
    component_id = "memory_logger"
    article_ties = ("VII",)
    def entry(self, case_id: str, all_steps: dict[str, ProcedureStepOutput], cross_case_index: dict) -> ProcedureStepOutput: ...
    # Read-side APIs (architecture-dependent):
    def list_cases(self) -> list[str]: ...
    def get_case_state(self, case_id: str) -> dict: ...
    def find_reuse_candidates(self, case_id: str, current_outputs: dict) -> list[dict]: ...
    def append_event(self, event: dict) -> str: ...     # returns event_id
    def emit_correction(self, original_event_id: str, correction_payload: dict) -> str: ...
```

**Closed-set guard:** the orchestration runner asserts at construction time that exactly these 7 component classes are importable from `src/elif_v0_1/components/__init__.py`. An 8th class fails the guard.

---

## Section 2 — Component-by-Component Design

### 2.1 Frame Validator

- **Purpose:** Refuses to let reasoning proceed until the frame survives Article II scrutiny. Owns Step 1 (verdict), Step 3 (assumption surfacing sub-behavior), Step 7-modeB (deeper-frame-rejection sub-behavior).
- **Inputs (typed):** `InputFrame`; for sub-behaviors, also `step1` output.
- **Outputs (typed):**
  - Step 1: `{verdict: enum, reformulated_frame?: str}` — verdict from closed set `{valid, invalid, needs_decomposition}`. If verdict ≠ `valid`, `reformulated_frame` is required.
  - Step 3: `{assumptions: list[str]}` — declarative-form, ≥2 entries, not questions.
  - Step 7-modeB: `{rejections: list[{trajectory, one_line_reason}]}` — `trajectory` fixed at `deeper_frame_rejection`.
- **Validation rules (structural; from procedure v1.0 Steps 1, 3, 7 mode B):**
  - Step 1: verdict must be one of three; `invalid`/`needs_decomposition` requires reformulated_frame.
  - Step 3: ≥2 entries; each entry must be a declarative statement (no `?` allowed as final character per structural heuristic; LLM-prompt enforces).
  - Step 7-modeB: ≥0 entries (modeB may be empty); when present, each entry includes one-line reason.
- **Dependencies (reads from):** Step 3 and Step 7-modeB read Step 1's output. Step 1 reads only `InputFrame`. The Frame Validator never reads other components' outputs.
- **Failure modes:**
  - `validate()` returning `invalid` → orchestration_runner RAISES `FrameInvalidError` and halts the run. The Memory Logger captures a `refutation` event before exit.
  - `surface_assumptions()` returning fewer than 2 entries → schema validation fails → `ELIFError`.
  - `surface_deeper_frame_rejection()` returning entries without one-line reasons → schema validation fails.
- **Architecture-dependent behavior:** None. Pure prompt-portable.
- **Prompting-portable behavior:** All three methods. System prompt at `prompts/frame_validator.system.md` enforces closed-set verdicts + declarative form + Article II framing.

### 2.2 Object Decomposer

- **Purpose:** Article IV — every model is a partial projection; decomposition is composable forward across cases. Owns Step 2 (family decomposition) + Step 6 (multi-scale sub-behavior).
- **Inputs (typed):** Step 1 output for Step 2; Step 2 output for Step 6.
- **Outputs (typed):**
  - Step 2: `{families: list[{family, rationale}]}` — ≥2 families, each with named rationale.
  - Step 6: `{scales: list[str], cross_scale_relations: list[str], scale_axis_engaged: bool}` — when `scale_axis_engaged=false`, both list fields may be empty AND the output must include an `absence_reason` field naming why scale-axis was disabled (Q6.3 ceremony-risk operator judgment).
- **Validation rules (structural):**
  - Step 2: ≥2 families; each has rationale.
  - Step 6: if `scale_axis_engaged=true`, ≥2 distinct scales + ≥1 cross-scale relation; if `false`, `absence_reason` required.
- **Dependencies:** Step 2 reads Step 1; Step 6 reads Step 2. No cross-component reads beyond what the runner provides.
- **Failure modes:**
  - Step 2: <2 families → schema fail → halt.
  - Step 6 with `scale_axis_engaged=true` but missing relations → schema fail.
- **Architecture-dependent behavior:** None.
- **Prompting-portable behavior:** Both methods. Q6.3 ceremony-risk handling lives in the prompt (instructs the LLM to disable scale-axis only if content is naturally single-scale and to name the absence_reason explicitly).

### 2.3 Hypothesis Validator

- **Purpose:** Articles I + III — no self-validation; every claim traces to external evidence. Owns Steps 4 (hypotheses + distinguishing predictions) + 5 (failure conditions).
- **Inputs (typed):** Step 2 output for Step 4; Step 4 output for Step 5.
- **Outputs (typed):**
  - Step 4: `{hypotheses: list[{id, statement, distinguishing_prediction}]}` — each hypothesis has a distinguishing prediction (an observation that discriminates it from alternatives).
  - Step 5: `{failure_conditions: list[{hypothesis_id, failure_condition}]}` — one failure condition per hypothesis from Step 4; failure conditions must be observable (not vacuous).
- **Validation rules:** every Step 4 hypothesis has a distinguishing prediction; every Step 4 hypothesis_id appears once in Step 5 with an observable failure condition.
- **Dependencies:** Step 4 reads Step 2; Step 5 reads Step 4.
- **Failure modes:** missing prediction → schema fail; failure_conditions count ≠ hypothesis count → schema fail; vacuous failure condition (LLM-prompt enforces; runner cannot detect statically).
- **Architecture-dependent behavior:** None.
- **Prompting-portable behavior:** Both methods. The strongest signal-per-cost component per Step 6 evidence (Articles I + III tie).

### 2.4 Branching Roadmap Engine

- **Purpose:** Articles V + VI + VII — refuse-capable, coherent convergence, generative reconstruction. Owns Step 7-modeA (outside-frame trajectories that feed Step 8) and Step 8 (stage-gated roadmap).
- **Inputs (typed):** Step 4 output and Step 1 output for Step 7-modeA; Step 7-modeA output for Step 8.
- **Outputs (typed):**
  - Step 7-modeA: `{trajectories: list[{tag, one_line_reason}]}` — tag fixed at `outside_original_frame`, ≥1 entry.
  - Step 8: `{stages: list[{stage_id, continuation_gate}]}` — every stage carries at least one testable continuation gate (the explicit condition under which the next stage may begin).
- **Validation rules:** Step 7-modeA: ≥1 trajectory tagged `outside_original_frame` with one-line reason. Step 8: every stage has ≥1 continuation_gate; each gate states a testable observation condition.
- **Dependencies:** Step 7-modeA reads Step 4 + Step 1; Step 8 reads Step 7-modeA.
- **Failure modes:** outputs without tagged trajectories; roadmaps without gates; gates without testable conditions.
- **Architecture-dependent behavior:** None (Article VII compositional reuse happens at Memory Logger entry, not in BRE itself).
- **Prompting-portable behavior:** Both methods.

### 2.5 Governance Kernel

- **Purpose:** Articles V + VI + VII enforcement at the verdict layer. Step 9 owner; absorbs the former Step 11 confidence + uncertainty annotation as output-shape extension (Step 8 §2 binding decision).
- **Inputs (typed):** Step 8 output + dict of all prior step outputs.
- **Outputs (typed):** `{verdict, confidence, unresolved_uncertainty_sources: list[str], constraints?: list[str], refusal_reason?: str}` — `verdict ∈ {constrain, refuse, abstain}`. `confidence` is a value in [0.0, 1.0] tied to ≥1 named entry in `unresolved_uncertainty_sources` (procedure v1.0 Step 11 tying-discipline preserved).
- **Validation rules:**
  - `verdict` from closed set.
  - `confidence` must be tied to ≥1 entry of `unresolved_uncertainty_sources` (no confidence asserted without an unresolved uncertainty source named).
  - `verdict=constrain` requires `constraints` non-empty.
  - `verdict=refuse` requires `refusal_reason` non-empty.
  - `verdict=abstain` requires `unresolved_uncertainty_sources` non-empty.
- **Dependencies:** Reads Step 8 output + all prior committed outputs.
- **Failure modes:**
  - Schema-violating output → `ELIFError`, halt.
  - `verdict=refuse` + sterile-equilibrium signature detected by Memory Logger pre-check → orchestration_runner halts with `GovernanceRefuseError` AND logs a `refutation` event.
- **Architecture-dependent behavior:** Reads Memory Logger sterile-equilibrium detector (architecture-dependent assist); the kernel itself is prompt-portable but the halt-on-sterile-equilibrium pathway requires the Logger.
- **Prompting-portable behavior:** Adjudicate method.

### 2.6 Operative Truth Separator

- **Purpose:** Article IV — operative ≠ theoretical; both are partial. Step 10 owner.
- **Inputs (typed):** Step 9 output + dict of all prior outputs.
- **Outputs (typed):** `{operative_strand?: str, theoretical_strand?: str, absence_reason?: str}` — exactly one of: both strands present, OR `absence_reason` present (per procedure v1.0 Step 10 "absence of one strand must be logged with reason").
- **Validation rules:** XOR semantics: (operative AND theoretical) XOR (absence_reason). No other combination is valid.
- **Dependencies:** Reads Step 9 + all prior.
- **Failure modes:** both strands missing AND no absence_reason → schema fail; merged-strand outputs (only one prose field "truth") → schema fail.
- **Architecture-dependent behavior:** None.
- **Prompting-portable behavior:** Yes.

### 2.7 Memory Logger

- **Purpose:** PRIMARY site of Article VII enforcement. Owns Step 11 (post-Step-8-renumber from Step 12). Architecture-dependent — the only component that requires persistence + cross-case state + audit-trail discipline.
- **Inputs (typed):** `case_id`, `all_steps: dict[step_id, ProcedureStepOutput]`, `cross_case_index: dict`.
- **Outputs (typed):** `{events: list[MemoryLoggerEvent], article_vii_tracking: ArticleVIITrackingRecord}`.
- **Validation rules (structural; from procedure v1.0 Step 12):**
  - ≥1 entry in the events list, drawn from `{capacity_change, pattern_recognized, refutation}` event types (other event types are runner-internal).
  - Each declarative-form entry has ≥1 line-ref into the case's Condition C output (for benchmark replay) or into the per_step outputs (for non-replay runs).
  - `article_vii_tracking` validates against `article_vii_tracking.schema.json` (Section 3).
- **Dependencies:** Reads all prior step outputs + the on-disk cross-case index (`results/v0_1_runs/_index.json`).
- **Failure modes:**
  - Empty events list → schema fail.
  - Entries missing line-refs → schema fail.
  - `recognition_confidence > 0.9` without `refutation_conditions` → Article I violation, halts run with `GovernanceRefuseError`.
  - Reuse-flag where Frame Validator should have refused → Article II violation, logs and surfaces in run_meta.
- **Architecture-dependent behavior:**
  - JSONL append-only persistence per case (`results/v0_1_runs/<run_id>/article_vii_tracking.json` write + execution_log.jsonl append).
  - Cross-case index maintenance.
  - Reuse detection (`find_reuse_candidates`).
  - Operator-correction emission (creates new events; never mutates original).
  - Sterile-equilibrium signature check.
- **Prompting-portable behavior:** None. The Memory Logger does NOT have a system prompt at `prompts/memory_logger.system.md` because its function is bookkeeping, not reasoning. Step 8 §6 explicitly: 10 of 11 steps prompt-portable; Step 11 is the architecture-dependent exception.

---

## Section 3 — Memory Logger Design

The Memory Logger is the strongest architecture-dependent surface in v0.1. Step 8 §6 places it as the sole owner of cross-case state, Article VII capacity tracking, and audit-trail discipline.

### 3.1 Schema — Article VII tracking record

Mirrors `results/case_01/article_vii_tracking.json` exactly. Required top-level keys (per existing on-disk reality):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ArticleVIITrackingRecord",
  "type": "object",
  "required": [
    "schema_version",
    "case_id",
    "captured_ts",
    "execution_phase",
    "procedure_version_used",
    "execution_order_note",
    "time_to_arbitration",
    "compositional_reuse",
    "pattern_emergence",
    "memory_logger_capacity_change_records",
    "failure_records",
    "judgment_acts",
    "article_i_check",
    "article_ii_check"
  ],
  "properties": {
    "schema_version": {"const": "v0.4.0"},
    "case_id": {"type": "string"},
    "captured_ts": {"type": "string"},
    "execution_phase": {"type": "string", "enum": ["E1", "E1.5", "E2", "E3"]},
    "procedure_version_used": {"type": "string", "enum": ["v1.0", "v1.1"]},
    "execution_order_note": {"type": "string"},
    "time_to_arbitration": {
      "type": "object",
      "required": ["time_to_first_arbitration_minutes", "time_to_final_convergence_minutes", "measurement_note", "prior_similar_shape_cases", "prior_similar_shape_cases_note", "time_delta_vs_prior_similar", "time_delta_note"],
      "properties": {
        "time_to_first_arbitration_minutes": {"type": ["number", "null"]},
        "time_to_final_convergence_minutes": {"type": ["number", "null"]},
        "measurement_note": {"type": "string"},
        "prior_similar_shape_cases": {"type": "array", "items": {"type": "string"}},
        "prior_similar_shape_cases_note": {"type": "string"},
        "time_delta_vs_prior_similar": {"type": ["number", "null"]},
        "time_delta_note": {"type": "string"}
      }
    },
    "compositional_reuse": {
      "type": "object",
      "required": ["prior_structures_referenced", "reuse_count_total", "fresh_structures_authored", "fresh_structures_note", "reuse_ratio"],
      "properties": {
        "prior_structures_referenced": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["case_id", "structure_type", "reuse_kind"],
            "properties": {
              "case_id": {"type": "string"},
              "structure_type": {"type": "string"},
              "reuse_kind": {"type": "string", "enum": ["direct", "composed", "deprecated"]}
            }
          }
        },
        "reuse_count_total": {"type": "integer", "minimum": 0},
        "fresh_structures_authored": {"type": "integer", "minimum": 0},
        "fresh_structures_note": {"type": "string"},
        "reuse_ratio": {"type": "number", "minimum": 0.0, "maximum": 1.0}
      }
    },
    "pattern_emergence": {
      "type": "object",
      "required": ["patterns_recognized", "patterns_deprecated", "candidate_frameworks"],
      "properties": {
        "patterns_recognized": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["pattern_id", "first_seen_in_case", "recognition_confidence", "refutation_conditions"],
            "properties": {
              "pattern_id": {"type": "string"},
              "first_seen_in_case": {"type": "string"},
              "recognition_confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
              "refutation_conditions": {"type": "string", "minLength": 1}
            }
          }
        },
        "patterns_deprecated": {"type": "array"},
        "candidate_frameworks": {"type": "array"}
      }
    },
    "memory_logger_capacity_change_records": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["change_type", "case_id", "description", "refutable_with"],
        "properties": {
          "change_type": {"type": "string", "enum": ["arbitration_shortcut_added", "framework_candidate_emerged", "composition_path_discovered", "pattern_recognition_added", "judgment_act_logged"]},
          "case_id": {"type": "string"},
          "description": {"type": "string"},
          "refutable_with": {"type": "string"}
        }
      }
    },
    "failure_records": {"type": "array"},
    "judgment_acts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["case_id", "decision_point", "alternatives_considered", "selected_operation", "reason", "consequence"],
        "properties": {
          "case_id": {"type": "string"},
          "decision_point": {"type": "string"},
          "alternatives_considered": {"type": "array", "items": {"type": "string"}},
          "selected_operation": {"type": "string"},
          "reason": {"type": "string"},
          "consequence": {"type": "string"}
        }
      }
    },
    "article_i_check": {
      "type": "object",
      "required": ["any_pattern_confidence_above_0_9_missing_refutation", "note"],
      "properties": {
        "any_pattern_confidence_above_0_9_missing_refutation": {"type": "boolean"},
        "note": {"type": "string"}
      }
    },
    "article_ii_check": {
      "type": "object",
      "required": ["any_reuse_where_frame_validator_should_have_refused", "note"],
      "properties": {
        "any_reuse_where_frame_validator_should_have_refused": {"type": "boolean"},
        "note": {"type": "string"}
      }
    }
  },
  "additionalProperties": false
}
```

### 3.2 Storage model

**JSONL append-only per-case + an index.**

```
results/v0_1_runs/
├── _index.json                          # cross-case index; rewritten atomically on each new run
├── <run_id>/
│   ├── input_frame.locked.json
│   ├── run_meta.json
│   ├── per_step/
│   │   └── step_NN.output.json          # one per step, immutable after commit
│   ├── article_vii_tracking.json        # full Article VII record (Section 3.1)
│   ├── events.jsonl                     # append-only event log (Section 3.3)
│   └── execution_log.jsonl              # per-step run log (Section 1.5.5)
```

**Append-only discipline:**
- `events.jsonl` is opened with `O_APPEND`; the runner never seeks within it.
- Per-step output JSON files are write-once: once written, the runner asserts file existence and refuses to overwrite.
- The cross-case `_index.json` is rewritten as a whole on each run-completion (because it is a derived view, not the source of truth).
- Corrections create NEW events (Section 3.4); original events are never overwritten or deleted.

### 3.3 Event structure

Each line of `events.jsonl` is one `MemoryLoggerEvent` (Section 1.5.4 schema). Event types are closed-set:

| event_type | When emitted | Payload shape |
|---|---|---|
| `open` | Runner starts a case run | `{run_id, case_id, procedure_version_used, execution_phase}` |
| `close` | Runner completes Step 11 successfully | `{run_id, case_id, final_verdict_from_step_9, exit_code}` |
| `pattern_recognized` | Memory Logger detects a cross-case structure reuse | `{pattern_id, first_seen_in_case, recognition_confidence, refutation_conditions}` |
| `refutation` | Frame Validator returns invalid; Governance Kernel returns refuse; Article I/II violation | `{trigger, refutation_source, halt_reason}` |
| `capacity_change` | Article VII tracker observes a capacity-change record | `{change_type, description, refutable_with}` |

### 3.4 Correction model

Operator-led corrections create NEW events; original events are NEVER mutated. The correction event carries `supersedes_event_id` pointing to the original. Read APIs return the latest in supersession-chain order by default; a `--show-superseded` flag exposes the full history.

**Why:** preserves audit trail (Article III: every claim traces externally; the trace must survive operator correction). Aligns with constitutional v0.4 risk #25 ("trajectory stability becomes path dependence" → revision is traceable, not punished).

### 3.5 Traceability model

Every event has these cross-refs:

- `procedure_step` — which step of the runner emitted it
- `input_frame_id` — the locked input frame this run originated from
- `case_id` — the case context
- `captured_ts` — ISO timestamp
- `supersedes_event_id` (optional) — chain to original on corrections

The cross-case `_index.json` maintains an inverted index by `pattern_id` and `case_id` so reuse detection is O(prior_cases) per new run, not O(total events).

### 3.6 Retrieval model — read APIs

```python
class MemoryLogger:
    def list_cases(self) -> list[str]:
        """Return all case_ids that have at least one closed event."""

    def get_case_state(self, case_id: str) -> dict:
        """Return the latest Article VII tracking record + open events for the case."""

    def find_reuse_candidates(self, case_id: str, current_outputs: dict) -> list[dict]:
        """Scan prior cases' patterns_recognized + structure_type fields against current
        outputs; return candidate matches with similarity score. Used by Step 11 entry()
        to populate compositional_reuse.prior_structures_referenced."""

    def get_event(self, event_id: str) -> dict:
        """Return a single event by id, following supersession chain to latest."""

    def get_event_history(self, event_id: str) -> list[dict]:
        """Return event + all superseding events in order."""

    def detect_sterile_equilibrium(self, case_id: str) -> bool:
        """Return True if the Article VII signature for the case + cross-case index
        indicates sterile equilibrium per benchmarks/article_vii_capacity_accumulation_tracking.md
        §'Critical failure patterns'. Used by Governance Kernel pre-verdict."""

    def append_event(self, event: dict) -> str:
        """Validate against schema, assign event_id, append to events.jsonl, return id."""

    def emit_correction(self, original_event_id: str, correction_payload: dict) -> str:
        """Create a new event with supersedes_event_id set; original is never touched."""
```

**Reuse detection algorithm (concrete):**
1. Load cross-case index.
2. For each `pattern_id` in the index, compute a structural-shape comparison against the current run's step outputs (initially: substring match on structure_type; later: configurable matcher).
3. Threshold (configurable, default 0.6) determines whether a match becomes a `prior_structures_referenced` entry with `reuse_kind=composed`.
4. `reuse_kind=direct` is reserved for explicit operator declaration (not auto-detected) — direct reuse is rare and high-stakes (Article II check applies).
5. `reuse_kind=deprecated` is set when the candidate pattern carries an active deprecation event.

**Sterile-equilibrium detector (concrete):**
- Across the current case + ≥2 prior cases, if all of:
  - `reuse_count_total = 0`
  - `fresh_structures_authored = 0` OR all fresh structures replicate prior pattern shapes verbatim
  - No `patterns_deprecated` entries across the window
  - All `recognition_confidence` values stationary (no movement vs prior)
- Then `detect_sterile_equilibrium = True`. The Governance Kernel may then halt with `verdict=refuse, refusal_reason="sterile_equilibrium_signature"`.

---

## Section 4 — Orchestration Runner

### 4.1 Execution order — the 11-step compressed sequence

Per Step 8 §2.2 binding decision. Order is fixed; no skipping; no reordering. Step 6 may emit `scale_axis_engaged=false` with absence_reason (Q6.3 ceremony-risk operator judgment per case).

| # | Owner | Method | Reads |
|---|---|---|---|
| 1 | FrameValidator | `validate(input_frame)` | InputFrame |
| 2 | ObjectDecomposer | `decompose(step1)` | Step 1 |
| 3 | FrameValidator | `surface_assumptions(input_frame, step1)` | InputFrame, Step 1 |
| 4 | HypothesisValidator | `hypothesize(step2)` | Step 2 |
| 5 | HypothesisValidator | `failure_conditions(step4)` | Step 4 |
| 6 | ObjectDecomposer | `multi_scale(step2)` | Step 2 |
| 7a | BranchingRoadmapEngine | `outside_frame(step4, step1)` | Step 4, Step 1 |
| 7b | FrameValidator | `surface_deeper_frame_rejection(input_frame, step1)` | InputFrame, Step 1 |
| 8 | BranchingRoadmapEngine | `staged_roadmap(step7a)` | Step 7a only (modeB does NOT enter Step 8 per Step 8 §2.2) |
| 9 | GovernanceKernel | `adjudicate(step8, prior_outputs)` | Step 8 + all prior |
| 10 | OperativeTruthSeparator | `separate(step9, prior_outputs)` | Step 9 + all prior |
| 11 | MemoryLogger | `entry(case_id, all_steps, cross_case_index)` | all steps + cross-case index |

Step 7 is the only split step. Its two modes commit as TWO separate `ProcedureStepOutput` records under `per_step/step_07a.output.json` and `per_step/step_07b.output.json`.

### 4.2 Procedure execution — sequential, no revision once committed

The runner is a strict state machine. State transitions:

```
NOT_STARTED → STEP_1_RUNNING → STEP_1_COMMITTED → STEP_2_RUNNING → ... → STEP_11_COMMITTED → RUN_CLOSED
```

Out-of-band transitions:
- Any `STEP_N_RUNNING → HALTED_FRAME_INVALID` (raised by Step 1)
- Any `STEP_N_RUNNING → HALTED_GOVERNANCE_REFUSE` (raised by Step 9, including sterile-equilibrium pre-check)
- Any `STEP_N_RUNNING → HALTED_SCHEMA_VIOLATION` (raised by any step whose output fails schema validation)
- Any `STEP_N_RUNNING → STEP_N_TIME_BOX_EXCEEDED → STEP_N_COMMITTED` (output truncated, time_box_status=`box_exceeded_output_truncated`, run continues)

Once a step commits, the runner immediately writes:
- `per_step/step_NN.output.json` (immutable)
- A `commit` line to `execution_log.jsonl`

No state in memory survives a step commit other than the read-only dict of prior outputs. The runner is restart-resistant: a partially-completed run can be resumed by reading the per_step directory and computing the next step.

### 4.3 Governance insertion points

Two governance insertions, both architecture-dependent:

**Insertion A — Article II / Frame Validator refusal (Step 1):**
- If Step 1 returns `verdict=invalid`, the runner raises `FrameInvalidError` and halts before Step 2.
- Memory Logger emits a `refutation` event with `trigger=frame_invalid` and the run closes with non-zero exit code.

**Insertion B — Article VII / Memory Logger sterile-equilibrium check (Step 9 pre-verdict):**
- Before Step 9 runs the Governance Kernel adjudicate, the runner calls `MemoryLogger.detect_sterile_equilibrium(case_id)`.
- If True, the runner passes a hint to the Governance Kernel prompt (in the system message): "sterile equilibrium signature detected — verdict=refuse with refusal_reason='sterile_equilibrium_signature' is recommended unless the case content materially differs from prior."
- The Governance Kernel may override the hint if the LLM's adjudication produces a different verdict; if `verdict=refuse + refusal_reason='sterile_equilibrium_signature'`, the runner halts post-Step-9 with `GovernanceRefuseError`.

### 4.4 Refusal flow

The three halt modes are distinct and each produces a different exit code:

| Halt mode | Exit code | Captured events |
|---|---|---|
| `HALTED_FRAME_INVALID` | 10 | `open`, `refutation(trigger=frame_invalid)`, `close(exit_code=10)` |
| `HALTED_GOVERNANCE_REFUSE` | 20 | `open`, all step events through Step 9, `refutation(trigger=governance_refuse)`, `close(exit_code=20)` |
| `HALTED_SCHEMA_VIOLATION` | 30 | `open`, all step events through the failing step, `refutation(trigger=schema_violation, step=<NN>)`, `close(exit_code=30)` |
| `RUN_CLOSED` (success) | 0 | full event sequence including Step 11 capacity_change |

Halt modes are explicit by exit code so the CLI can be scripted and the operator can grep them.

### 4.5 Logging flow

Two log streams per run:

**execution_log.jsonl** (run-level; per-line schema in 1.5.5):
- One line for each of: step_start, llm_call, llm_response, schema_validate, commit, step_complete.
- One line for each halt event (time_box_overrun, governance_halt, frame_invalid_halt, sterile_equilibrium_halt).
- The execution log is for runner forensics; it is NOT the source of truth for Article VII tracking (that is `article_vii_tracking.json`).

**events.jsonl** (Memory Logger; per-line schema in 1.5.4):
- Closed-set event types only.
- Append-only.
- Source of truth for cross-case reuse detection.

Both logs are written synchronously per line (`fsync` after each append) so a crashed run is recoverable from disk state.

---

## Section 5 — MVP Scope Boundary

### 5.1 Included in v0.1 (mirror of Step 8 decision package §9)

- **7 canonical components** as Python classes under `src/elif_v0_1/components/`.
- **6 system prompts** (the 6 prompt-portable components — Memory Logger has no prompt).
- **1 architecture-dependent Memory Logger** with persistence + cross-case index + reuse detection + correction model + sterile-equilibrium detector.
- **1 thin orchestration runner** (11-step state machine, governance insertions A + B, refusal flow with three halt exit codes).
- **1 LLM adapter** (single frontier-LLM family; structured-output enforcement).
- **1 CLI entry point** (`elif run --case <id> --condition <a|b|c> [--procedure v1.0|v1.1]`).
- **5 JSON Schemas** (`input_frame`, `procedure_step_output`, `article_vii_tracking`, `memory_logger_event`, `run_log`).
- **Closed-set guards** at import time (already in `base.py`/`__init__.py`).
- **Test suite** covering: per-component canonical tests; orchestration integration; Memory Logger persistence; case_01/02/03 replay; closed-set test; doctrine compatibility test.
- **Procedure v1.0 execution** (the LOCKED procedure remains authoritative; v1.1 is selectable via CLI flag but the default is v1.0 until Phase 2 entry-act validates compression).

### 5.2 Excluded from v0.1

Mirror of decision package §8.3 + operator's 2026-05-29 explicit exclusions:

- No web UI of any kind
- No external API surface (no HTTP server; no REST; no gRPC; no MCP server)
- No multi-conversation continuity / Memory Corridor
- No Continuity Layer runtime (separate doctrine; OSG memory `continuity_layer_doctrine.md`)
- No cross-LLM-family adapters (single-model E1.5 baseline; multi-family is Phase 3-4)
- No real-time observation / streaming output
- No collaboration / multi-operator coordination
- No World-Model integration of any kind
- No ELIF Capsules / UX layer
- No constitutional v0.5 compression authoring
- No external benchmark integration
- **ORC (organic dynamic substrate)** — DEFERRED
- **CIM (Civilizational Intelligence Matrix)** — DEFERRED
- **Decision Room** — DEFERRED
- **Civilizational layer** — DEFERRED
- **Adaptive population-scale feedback** — DEFERRED
- No 8th component (Step 8 §1 binding rejection)
- No procedure v1.1 execution as default path (v1.1 is a Phase 2 entry-act; v1.0 remains default)
- No embedding store, no vector DB, no graph DB (Memory Logger is JSONL only)
- No fine-tuning, no custom ML, no model training of any kind

Each exclusion is reviewable; none is dead. The non-self-propagation constraint keeps deferrals dormant until evidence pulls them active.

---

## Section 6 — Engineering Estimate

### 6.1 Development phases

Mapping decision package §8.1 to operational phases (refined per this plan):

**Phase 0 — Scaffolding (1.0 days)**
- Extend existing scaffold: complete `components/__init__.py` imports; create empty class files for the 6 not-yet-scaffolded components.
- Add `schemas/` directory with the 5 JSON Schemas as draft documents.
- Add empty `prompts/<name>.system.md` files (6 of them).
- Add `tests/` skeleton with one test_closed_set_guards.py.
- Verify `import elif_v0_1` succeeds and closed-set guard fires.
- **Exit gate:** `python -m unittest src.elif_v0_1.tests.test_closed_set_guards` passes.

**Phase 1 — Architecture-dependent layer (3.0 days)**
- Implement `memory_logger.py` end-to-end: persistence, schemas, event log, cross-case index, reuse detection, correction model, sterile-equilibrium detector.
- Implement `llm_adapter.py`: one frontier-LLM call boundary, structured-output enforcement, retry budget.
- Author test_memory_logger.py: persistence write→read; correction event creates new event without mutating original; reuse detection finds prior structures; sterile-equilibrium detector returns False on case_01 (has compositional reuse) and True on a synthetic stationary fixture.
- **Exit gate:** all Memory Logger tests pass on synthetic fixtures.

**Phase 2 — Components (4.0 days)**
- Implement each of the 7 component classes, calling `llm_adapter` with the appropriate system prompt and validating responses against the per-step schema.
- Author each of the 6 system prompts at `prompts/<name>.system.md` (Memory Logger has no prompt).
- Author per-component canonical tests (positive/negative/edge inputs).
- **Exit gate:** all 7 component test files pass; `import elif_v0_1.components` produces all 7 classes.

**Phase 3 — Procedure runner (2.0 days)**
- Implement `orchestration_runner.py` state machine.
- Implement the two governance insertions (Article II + Article VII).
- Implement the three refusal flows.
- Implement `cli.py` entry point.
- Author orchestration integration test (synthetic input frame → full 11-step run → all artifacts on disk).
- **Exit gate:** test_orchestration_runner.py passes; a synthetic case runs end-to-end producing all expected artifacts.

**Phase 4 — Acceptance tests (1.5 days)**
- Author the per-component canonical tests' negative/edge cases.
- Author the closed-set test (`test_no_eighth_component`).
- Author the doctrine compatibility test (procedure v1.0 fields preserved; no silent v0.5 expansion).
- Author the schema validation test (every fixture validates against its schema).
- **Exit gate:** the full test suite passes locally; coverage report shows ≥80% on the runner + Memory Logger.

**Phase 5 — Case-replay verification (2.5 days)**
- Run case_01_electroculture input frame through v0.1 procedure v1.0; capture output to `results/v0_1_runs/case_01_replay/`.
- Run case_02_policy_governance; capture similarly.
- Run case_03_operational_organizational; capture similarly.
- For each, compare the per-step output JSON files structurally to the existing `results/case_NN/condition_c_output.md` (structural equivalence: same Step 1 verdict family; same number of Step 2 family entries with same axis name; same Step 4 hypothesis count ±1; same Step 9 verdict).
- For each, compare the produced `article_vii_tracking.json` against the existing one (the `compositional_reuse` and `pattern_emergence` arrays should match within tolerance — see Section 7.4).
- **Exit gate:** all three replay tests pass; structural equivalence accepted per Section 7.4 tolerances.

### 6.2 Estimated effort (refined per phase)

| Phase | Days |
|---|---|
| Phase 0 — Scaffolding | 1.0 |
| Phase 1 — Architecture-dependent layer | 3.0 |
| Phase 2 — Components | 4.0 |
| Phase 3 — Procedure runner | 2.0 |
| Phase 4 — Acceptance tests | 1.5 |
| Phase 5 — Case-replay verification | 2.5 |
| **Total** | **14.0** |

Within the decision package §8.1 baseline of 12-14 days. Risk-adjusted upper bound is 16 days if Phase 5 case-replay surfaces structural-equivalence failures that require iterating on prompts.

### 6.3 Risks

Inherited from decision package §8.2 plus risks newly visible from this plan:

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Procedure v1.1 (11-step compressed) fails to preserve signal | medium | medium | Phase 5 runs default v1.0; v1.1 is a separate Phase 2 entry act |
| R-02 | Memory Logger reuse-detection false positives | medium | low | Schema requires explicit refutation_conditions; cross-case validation gate before promotion |
| R-03 | Single-model E1.5 results don't generalize | high | medium | Documented disclosure in run_meta.json; multi-family deferred to Phase 3-4 |
| R-04 | Operator authors single-scale case breaking Step 6 ceremony | low | low | Step 6 emits `scale_axis_engaged=false` with absence_reason |
| R-05 | v0.5 pressure collapses design under Phase 2 | low | high | v0.4 LOCKED; non-self-propagation constraint |
| R-06 | Architecture surface bleeds into prompt-portable steps | medium | medium | Per-step closed-set output schema; runtime schema validation halts on violation |
| R-07 | Cross-machine continuity gap | low | medium | Single-machine v0.1; out of v0.1 scope |
| R-08 | Component growth pressure from Phase 2-3 cases | medium | high | Closed-set guard at import time; "no 8th component" symmetric to "no component survives by prestige" |
| **R-09 (new)** | **LLM adapter retries inflate cost without operator awareness** | medium | medium | Retry budget hard-cap per run; CLI flag `--max-llm-calls`; runtime aborts on exceeding |
| **R-10 (new)** | **Step 7 split (modeA vs modeB) confuses orchestration; modeB outputs accidentally feed Step 8** | medium | medium | Runner explicitly reads ONLY step_07a for Step 8; test_orchestration_runner.py covers this case |
| **R-11 (new)** | **Case-replay structural-equivalence is too strict and rejects acceptable LLM variation** | medium | medium | Section 7.4 defines tolerances; equivalence is structural (count, axis name, verdict family), not text-equivalent |
| **R-12 (new)** | **Memory Logger correction model is misused — operators delete events instead of superseding** | low | high | Read APIs return supersession-chain latest; deletion API does NOT exist (write-only persistence) |
| **R-13 (new)** | **Sterile-equilibrium detector creates feedback loop: refuses runs because prior runs were refused** | low | medium | Detector ignores refused runs in its window; only successful Step 11 entries count toward stationarity check |

### 6.4 Validation strategy

The validation strategy is **case replay**. v0.1 is considered operational when:

1. case_01_electroculture, case_02_policy_governance, case_03_operational_organizational each replay through the v0.1 runner under procedure v1.0.
2. Each produces a Step 9 verdict in the same family as the existing `results/case_NN/condition_c_output.md` (`refuse` or `constrain` — both cases produced refuse-bundle outputs).
3. Each produces an `article_vii_tracking.json` whose `compositional_reuse.prior_structures_referenced` contains at least the patterns that the existing on-disk file lists.
4. Each produces a Step 11 capacity-change record with `change_type ∈ {pattern_recognition_added, judgment_act_logged}`.
5. No run exits with `HALTED_SCHEMA_VIOLATION` (any schema fail indicates a v0.1 implementation defect, not a benchmark failure).

Structural equivalence — not text equivalence — is the bar (Section 7.4 tolerances).

### 6.5 First usable milestone

**Lower-bound first-usable milestone:** end of Phase 3 (Day 10).

At end of Phase 3:
- A fresh case input frame can be loaded by the CLI.
- The 11-step orchestration runner executes the full sequence.
- Frame Validator → Object Decomposer → Hypothesis Validator → Branching Roadmap Engine → Governance Kernel → Operative Truth Separator → Memory Logger all produce committed outputs.
- A Memory Logger entry is produced on disk with at least one capacity-change record.
- The run produces exit code 0 (success) or 10/20/30 (refusal flows).

This is the first day the operator can sit down and run `elif run --case case_NN --condition c` and see a result. Phases 4 + 5 harden this surface and validate against the three benchmark cases, but Phase 3 is the floor of usability.

**Day-by-day breakdown to first usable milestone:**

| Day | Activity |
|---|---|
| 1 | Phase 0 scaffolding |
| 2-4 | Phase 1 Memory Logger + LLM adapter |
| 5-8 | Phase 2 components (~0.5 day per component) |
| 9-10 | Phase 3 orchestration runner + CLI |
| 11-12 | Phase 4 acceptance tests |
| 13-14 | Phase 5 case-replay verification |

---

## Section 7 — Acceptance Test Pack

These tests v0.1 MUST pass before being considered operational.

### 7.1 Per-component canonical tests

**One test file per component.** Each test file covers:
- **Positive case:** typical input → schema-valid output → expected closed-set code.
- **Negative case:** malformed input → raises `ELIFError` or returns invalid verdict.
- **Edge case:** boundary condition (empty input, minimum valid input, maximum useful input).

| Component | Positive test | Negative test | Edge test |
|---|---|---|---|
| FrameValidator | well-formed input frame → verdict ∈ closed set | empty `text` → schema fail | needs_decomposition without reformulated_frame → schema fail |
| ObjectDecomposer | typical Step 1 output → ≥2 families | Step 1 valid (no decomposition needed) → graceful continuation | 1 family returned → schema fail |
| HypothesisValidator | ≥2 families → ≥1 hypothesis with distinguishing prediction | hypothesis without distinguishing prediction → schema fail | hypothesis_count differs in Step 5 → schema fail |
| BranchingRoadmapEngine | step4 outputs → ≥1 trajectory tagged | trajectory without one-line reason → schema fail | empty trajectories list → schema fail |
| GovernanceKernel | sufficient context → verdict ∈ closed set | confidence asserted without unresolved uncertainty source → schema fail | sterile-equilibrium hint + LLM still returns constrain → runner permits but logs |
| OperativeTruthSeparator | both strands distinguishable → split output | merged single-strand output → schema fail | both strands missing without absence_reason → schema fail |
| MemoryLogger | full run → ≥1 capacity-change record | empty events list → schema fail | recognition_confidence > 0.9 without refutation_conditions → Article I violation |

### 7.2 Procedure-runner integration test

**test_orchestration_runner.py — synthetic case end-to-end:**

```
Given:
  - InputFrame: synthetic_test_case_001 with frame text exercising all 11 steps
  - LLM adapter mocked to return canned structured outputs per step
When:
  - orchestration_runner.execute(input_frame)
Then:
  - 11 step output files written to results/v0_1_runs/<run_id>/per_step/
  - article_vii_tracking.json written with schema_version="v0.4.0"
  - events.jsonl contains: open + refutation? + capacity_change + close
  - execution_log.jsonl contains: 11 commit lines, no error lines
  - Run exits with exit code 0
```

Additional assertions:
- Step 7 split: step_07a and step_07b both exist; step_08 input is step_07a only (test_step7_split_isolation).
- Refusal flow: synthetic InputFrame designed to elicit Step 1 invalid → run halts with exit 10, no step_2..step_11 files exist.
- Refusal flow: synthetic context designed to elicit Step 9 refuse → exit 20.
- Refusal flow: malformed step output (forcibly injected) → exit 30.
- Sterile-equilibrium detector: empty cross-case index → detector returns False (no prior cases to compare).

### 7.3 Memory Logger persistence test

**test_memory_logger.py:**

- **Write → read:** create an event, read it back by id; equal contents.
- **Append-only enforcement:** open events.jsonl with O_APPEND and append two events; second event's offset > first's; first event's bytes unchanged.
- **Correction model:** emit correction for event_A → new event_B has supersedes_event_id=A; event_A on disk unchanged; `get_event(A)` returns B (latest in chain); `get_event_history(A)` returns [A, B].
- **Cross-case reuse detection:** seed two prior cases with patterns_recognized; new run's structure_type matches one pattern; `find_reuse_candidates` returns the match with reuse_kind=composed.
- **Sterile-equilibrium detector:** seed three stationary cases (no reuse, no fresh, stationary confidence) → detector returns True. Replace one with a fresh structure → returns False.
- **Schema enforcement:** attempt to append an event with event_type not in closed set → raises ELIFError.
- **Idempotency:** running the same case twice with the same input_frame produces two distinct run_ids; the cross-case index reflects both (no merge).

### 7.4 Case replay tests (the 3 benchmark cases)

For each of case_01, case_02, case_03:

**test_case_NN_replay.py:**

```
Given:
  - cases/case_NN/input_frame.md loaded into InputFrame
  - procedure_version_used = "v1.0"
  - LLM adapter calls a real frontier model (or recorded fixtures if --offline)
When:
  - orchestration_runner.execute(input_frame)
Then (structural equivalence to results/case_NN/):
  - Step 1 verdict family matches (existing case_01 returned `needs decomposition`;
    replay must return `needs_decomposition`)
  - Step 2 families count matches existing condition_c family count ±0
  - Step 4 hypothesis count matches existing ±1 (LLM variation tolerance)
  - Step 8 stages count matches existing ±1
  - Step 9 verdict family matches (refuse-family for all three cases per the existing
    Step 6 cross-case analysis)
  - article_vii_tracking.json:
    - compositional_reuse.prior_structures_referenced contains AT LEAST the same
      pattern_ids as the existing file (additions allowed; subtractions not)
    - pattern_emergence.patterns_recognized contains the patterns from the existing
      file (text may differ; pattern_ids must match)
    - judgment_acts non-empty
    - article_i_check.any_pattern_confidence_above_0_9_missing_refutation = false
    - article_ii_check.any_reuse_where_frame_validator_should_have_refused = false
```

**Tolerances (Section 6.4 + 7.4):**

| Field | Tolerance |
|---|---|
| Verdict family (Step 1, Step 9) | Exact match on family (not text) |
| Family count (Step 2) | ±0 |
| Hypothesis count (Step 4) | ±1 |
| Failure condition count (Step 5) | must equal hypothesis count |
| Trajectories count (Step 7a) | ±1 |
| Roadmap stages count (Step 8) | ±1 |
| pattern_ids (Article VII tracking) | superset (additions allowed) |
| reuse_count_total | ≥ existing value × 0.5 |
| judgment_acts | ≥1 |
| article_i_check | exact match (must be false) |
| article_ii_check | exact match (must be false) |

These tolerances accept non-deterministic LLM variation in language but require structural equivalence in shape.

### 7.5 Closed-set test: no 8th component

**test_closed_set_guards.py:**

```
def test_seven_components_exactly():
    from elif_v0_1.base import COMPONENT_IDS
    assert len(COMPONENT_IDS) == 7
    assert "frame_validator" in COMPONENT_IDS
    assert "object_decomposer" in COMPONENT_IDS
    assert "hypothesis_validator" in COMPONENT_IDS
    assert "branching_roadmap_engine" in COMPONENT_IDS
    assert "governance_kernel" in COMPONENT_IDS
    assert "operative_truth_separator" in COMPONENT_IDS
    assert "memory_logger" in COMPONENT_IDS

def test_eleven_steps_exactly():
    from elif_v0_1.base import PROCEDURE_STEP_IDS
    assert len(PROCEDURE_STEP_IDS) == 11

def test_seven_articles_locked():
    from elif_v0_1.base import ARTICLE_IDS
    assert ARTICLE_IDS == ("I", "II", "III", "IV", "V", "VI", "VII")

def test_four_failure_mode_poles():
    from elif_v0_1.base import FAILURE_MODE_POLES
    assert len(FAILURE_MODE_POLES) == 4

def test_components_module_exports_exactly_seven_classes():
    import elif_v0_1.components as comp
    classes = [getattr(comp, name) for name in dir(comp) if name[0].isupper()]
    assert len(classes) == 7

def test_import_fails_if_closed_set_drifts():
    # Smoke: the assert_consistent() guard at import time must fire.
    from elif_v0_1 import assert_consistent
    assert_consistent()  # must not raise
```

### 7.6 Doctrine compatibility test

**test_doctrine_compatibility.py:**

- **Procedure v1.0 fields preserved:** every Step's output schema includes all required fields per `procedure/elif_mode_procedure_v1.0.md` Table §"Procedure steps (LOCKED)".
- **No silent v0.5 expansion:** the constitutional layer at `doctrine/06_constitutional_layer_v0_4.md` is read at test time; assert exactly 7 Articles present; assert "v0.4" string in the document; assert no "v0.5" header exists.
- **Article VII schema_version pinned:** every produced `article_vii_tracking.json` carries `schema_version="v0.4.0"`. A run that produces a different version fails the test.
- **Memory Logger event_type closed set unchanged:** assert event_type enum is exactly `{open, close, pattern_recognized, refutation, capacity_change}`. Any addition fails the test.
- **No reference to deferred concepts in production code:** grep the `src/elif_v0_1/` tree for forbidden tokens (`memory_corridor`, `continuity_layer`, `world_model`, `orc`, `cim`, `decision_room`, `civilizational`); any hit fails the test.

---

## Section 8 — Open questions / operator decisions

The following questions surfaced during this planning exercise. Each requires operator decision before the corresponding build work proceeds. None of them blocks Phase 0 scaffolding; some block later phases.

### 8.1 LLM adapter choice

- **Question:** which frontier LLM family is the v0.1 baseline? (Anthropic Claude, OpenAI GPT-4-class, Google Gemini, etc.) The decision package §8.2 R-03 marks single-model dependence as a high-likelihood risk for generalization.
- **Blocks:** Phase 1 LLM adapter implementation.
- **Default if no decision:** match the model used in the existing case_01/02/03 runs (whatever produced `condition_c_output.md`). This makes Phase 5 case-replay maximally interpretable.

### 8.2 Procedure v1.0 vs v1.1 default for Phase 5 replay

- **Question:** Phase 5 replay defaults to procedure v1.0 (which the existing case results were produced under). Should v1.1 also run during Phase 5 as a "compression preservation" smoke test, or is v1.1 strictly a Phase 2 entry act?
- **Blocks:** Phase 5 test plan finalization.
- **Default if no decision:** Phase 5 runs v1.0 only. v1.1 is a separate Phase 2 entry-act.

### 8.3 Sterile-equilibrium detector activation in Phase 5

- **Question:** the sterile-equilibrium detector is in scope for v0.1, but Phase 5 case-replay produces only 3 cases under v0.1 — the detector cannot fire meaningfully on only 3 cases. Should the detector be activated in v0.1 (and tested with synthetic fixtures only) or deferred to v0.2?
- **Blocks:** Phase 1 Memory Logger scope.
- **Default if no decision:** implemented in v0.1, tested with synthetic fixtures only, runtime-active but unlikely to fire on 3-case window.

### 8.4 LLM cost cap

- **Question:** decision package §8.2 R-09 (new) — should the v0.1 runner have a hard-cap `--max-cost-usd` flag analogous to OSG's en_pilot, or only a `--max-llm-calls` flag?
- **Blocks:** Phase 3 CLI implementation.
- **Default if no decision:** `--max-llm-calls=22` (≈ 2 calls per step × 11 steps) as a budget proxy; cost cap deferred to a later iteration.

### 8.5 Memory Logger correction-emission permissions

- **Question:** operator-led corrections create new events that supersede originals. Should there be a CLI subcommand for emitting corrections (`elif correct --event-id <id> --payload <json>`), or is correction emission only done via direct Python API for v0.1?
- **Blocks:** Phase 4 CLI surface finalization.
- **Default if no decision:** Python API only in v0.1; CLI surface for corrections deferred.

### 8.6 Phase 5 LLM cost

- **Question:** Phase 5 case-replay requires running 3 frontier-LLM cases × 11 steps × ~2 calls/step = ~66 LLM calls. At a conservative $0.30/call this is ~$20 for one replay pass; debug iterations could 3-5x this. Is this an acceptable Phase 5 budget?
- **Blocks:** Phase 5 budget approval.
- **Default if no decision:** record Phase 5 LLM cost transparently in `run_meta.json`; operator may pause Phase 5 mid-flight if cost exceeds expectations.

### 8.7 Schema versioning strategy

- **Question:** if Phase 5 surfaces a need to extend the article_vii_tracking schema (e.g., new check field), does v0.1 ship with schema_version "v0.4.0" frozen, or does v0.1 own the schema as "v0.1.0" and reference v0.4 doctrinal anchor separately?
- **Blocks:** Phase 1 schema authoring.
- **Default if no decision:** v0.1 freezes the schema_version at "v0.4.0" (matching existing on-disk files); any extension creates a Phase 2 entry-act for schema_version bump.

### 8.8 Case-replay fixture mode

- **Question:** for CI environments without LLM API access, should Phase 5 support a `--offline` mode that replays recorded LLM responses from a fixtures directory, allowing deterministic CI runs?
- **Blocks:** Phase 5 CI integration.
- **Default if no decision:** v0.1 ships with `--offline` support; fixtures captured during the first live Phase 5 run; subsequent CI runs use fixtures.

### 8.9 Frame Validator sub-behavior commit granularity

- **Question:** Step 1 (validate) and Step 3 (surface_assumptions) and Step 7-modeB (deeper_frame_rejection) are all Frame Validator sub-behaviors. Do they share state in memory, or does each LLM call start fresh with only the prior committed step outputs visible?
- **Blocks:** Phase 2 Frame Validator implementation.
- **Default if no decision:** each LLM call starts fresh per the runner's "no cross-component imports" discipline; the runner passes prior committed outputs only.

### 8.10 Step 7 split observability

- **Question:** Step 7 splits into modeA (BRE) and modeB (Frame Validator deeper-frame-rejection). Both emit committed outputs (step_07a.output.json, step_07b.output.json). Should the runner produce a separate `step_07.summary.json` that combines the two for human readability, or is the split enough?
- **Blocks:** Phase 3 runner output format finalization.
- **Default if no decision:** no combined summary; the two committed outputs suffice; operator may post-process.

---

## Closing statement

This document is a planning artifact. It describes the smallest buildable v0.1 — 7 components, 11 steps, 1 architecture-dependent Memory Logger, 1 thin orchestration runner, 14 engineering days — that preserves the signal surviving three-case compression evidence.

The plan refuses to expand:
- No 8th component
- No constitutional v0.5
- No Memory Corridor, Continuity Layer runtime, ORC, CIM, World Model, Decision Room, Civilizational layer, Adaptive population-scale feedback
- No web UI, external API, multi-LLM-family, cross-machine continuity, fine-tuning, embedding store, graph DB

The plan refuses to commit to build:
- Build authorization is separate from this planning approval
- No autonomous progression past Phase 0 without explicit operator gate transitions

Section 8's open questions are the explicit decision surface between planning approval and build authorization.

**Smallest disposition wins. Compression > expansion. This is what survived evidence.**
