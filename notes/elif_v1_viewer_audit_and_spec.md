# ELIF V1 Viewer — Audit & Specification

> **Status:** SPECIFICATION EXERCISE. Visibility-only.
> **Trigger:** operator request 2026-05-30 — "Do not build more ELIF. Reveal the ELIF that already exists."
> **Constraints (enforced throughout):** No new component. No new Article. No new phase. No new architecture. No procedure modification. No schema modification. No world-model integration. No simulator hosting. No Phase 7 / Phase 8 work. Read-only over existing artifacts.
> **Closes nothing. Opens nothing. Specifies, does not implement.**

This is not an implementation proposal. It is a specification audit answering: *what is the minimum rendering required to expose existing ELIF artifacts as observable surfaces, without adding any reasoning capability the substrate does not already produce?*

---

## §0 — Discipline test

Every rendering choice in this document must pass two tests:

1. **The Reveal Test.** Could a sufficiently determined reader extract this information from the existing artifacts on disk? If yes, the rendering reveals. If no, the rendering builds — which is out of scope for this spec.
2. **The Truth Test.** Does the rendering claim anything the artifact does not already claim? If yes, it crosses into Article III territory (no self-validation) and Article VII territory (capacity vs truth). If no, it stays observational.

I apply both tests to every proposed surface.

---

## §1 — Substrate audit (what already exists)

Before specifying viewers, I enumerate the artifacts the viewer would render. All currently live on disk under `src/elif_v0_1/` or in run output directories.

### 1.1 Per-run artifacts (one set per ProcedureRunner.run() invocation)

| Artifact | Where it lives | Shape |
|---|---|---|
| `RunReport.run_context` | Returned by `ProcedureRunner.run()` | Frozen dataclass with case_id, condition, run_id, started_at_iso, procedure_version, offline_mode, max_llm_calls |
| `RunReport.step_outputs` | Same — tuple of 11 `StepOutputEnvelope` instances | Per-envelope: step_id, content (dict), committed_at_iso, llm_calls_used, time_box_status, structured_output_dict |
| `RunReport.exit_code` | Same | 0 / 10 / 20 / 30 |
| `RunReport.memory_logger_entries_written` | Same | int |
| `RunReport.completed_at_iso` | Same | ISO timestamp |
| MemoryLogger JSONL | `<persistence_dir>/<case_id>/article_vii_tracking.jsonl` | Append-only events: open / step_committed / refutation / close / (post-Position-B: also step_10 and step_11 commits + close-at-end) |

### 1.2 Per-cohort artifacts (built by replay harness)

| Artifact | Where it lives | Shape |
|---|---|---|
| `ReplayResult` | Returned by `replay_case()` | Per-case structural-similarity score + missing/unexpected behaviors + runner_path |
| `AcceptanceReport` | Returned by `replay_all_cases()` | Per-cohort aggregate of per-case results |
| Reference markdown | `results/<case_short>/condition_c_output.md` | Operator-authored Condition C reference |
| Offline fixtures | `src/elif_v0_1/offline_fixtures/step_*__case_*.json` | Per-step canonical operator-authored outputs |

### 1.3 Cross-run artifacts (no aggregation tool currently runs them)

| Artifact | Where it would live | Shape |
|---|---|---|
| Offline-vs-live comparison | Currently lives only as side-by-side reading | Per-step diff between offline and live |
| Multi-run cohort comparison | Does not exist as a structured artifact | Would be derived |
| Divergence history across dates | Does not exist | Would be derived |

### 1.4 Substrate verdict

**Every viewer specified below operates over (1.1) and (1.2). (1.3) requires aggregation but does not require new procedure or new reasoning.** Aggregation is pure computation — the substrate's `RunReport` instances are the inputs; the output is a table or panel of comparisons.

This means the substrate is **already sufficient** for everything the viewer needs to expose. Nothing in the viewer specs below modifies any existing component.

---

## §2 — Decision Room Specification (minimal)

### 2.1 Substrate read

Single `RunReport` instance. From that:

- `run_context.case_id`, `run_context.condition`, `run_context.run_id` — header
- `step_outputs[8].structured_output_dict` (= Step 9) — verdict, verdict_detail, confidence, unresolved_uncertainty_sources
- `step_outputs[9].structured_output_dict` (= Step 10) — operative, theoretical, absence_log
- `step_outputs[10].structured_output_dict` (= Step 11) — run_summary including final_verdict, post_refusal_closure
- `exit_code`, `completed_at_iso` — footer

### 2.2 Rendering shape

A single-page view organized into seven sections:

```
+----------------------------------------------------------+
| RUN HEADER                                                |
|   case_id  |  condition  |  run_id  |  procedure_version  |
+----------------------------------------------------------+
| STEP 9 — Verdict                                          |
|   verdict:                       <one of {constrain,      |
|                                  refuse, explicitly_      |
|                                  abstain}>                |
|   confidence:                    <prose>                  |
|   verdict_detail:                <paragraph>              |
|                                                           |
|   Unresolved uncertainty sources:                         |
|     - <bullet 1>                                          |
|     - <bullet 2>                                          |
|     - ...                                                 |
+----------------------------------------------------------+
| STEP 10 — Operative vs Theoretical                        |
|   Operative (what the verdict authorizes):                |
|     1. <bullet>                                           |
|     2. <bullet>                                           |
|     ...                                                   |
|   Theoretical (unresolved questions):                     |
|     1. <bullet>                                           |
|     2. <bullet>                                           |
|     ...                                                   |
|   Absence log: <prose, if present>                        |
+----------------------------------------------------------+
| STEP 11 — Run Summary                                     |
|   final_verdict | step_count | llm_calls_used             |
|   post_refusal_closure: <True | False>                    |
+----------------------------------------------------------+
| RUN FOOTER                                                |
|   exit_code  |  completed_at_iso                          |
+----------------------------------------------------------+
```

### 2.3 What the Decision Room does NOT do

- Does not render Steps 1–8 (they are intentionally absent; this is the *decision* room, not the *procedure* room)
- Does not compare to any reference
- Does not score the verdict
- Does not recommend an operator action
- Does not display approve/reject buttons or any actionable controls (rendering is read-only)
- Does not aggregate across runs
- Does not interpret the verdict — only renders it

### 2.4 Doctrinal compatibility

- **Article I (sovereignty):** rendering preserves the operator as the eventual addressee; no recommendation surface
- **Article III (no self-validation):** no validation surface; the verdict is presented, not validated
- **Article VII (capacity vs truth):** the run_summary's `post_refusal_closure` flag is a capacity marker, not a truth claim; rendering preserves this distinction
- **Position B (G0):** the post_refusal_closure field is the load-bearing surface that makes the Decision Room work on refuse-cases as well as non-refuse-cases

### 2.5 Reveal Test + Truth Test

- **Reveal:** every field in the rendering is a verbatim or trivially formatted extraction from existing `step_outputs` content. ✅
- **Truth:** the rendering claims only what the artifacts claim. ✅

### 2.6 Minimum implementation surface

A pure-function in Python: `def render_decision_room(run_report: RunReport) -> str` returning Markdown or HTML. No state. No reasoning. No I/O beyond input/output.

**Estimated complexity: ~60-80 LoC for Markdown rendering, ~100-150 LoC for static HTML.**

---

## §3 — Laboratory Viewer Specification (minimal)

### 3.1 Substrate read

Multiple `RunReport` instances + their associated MemoryLogger JSONLs + (optional) `AcceptanceReport` from a replay run.

### 3.2 Rendering shape

Four panels, each pure-observation:

#### Panel A — MemoryLogger event timeline (per case)

```
Case: case_01_electroculture
Run: run_16cb971f313b4208bea59373c6454527  (2026-05-30T13:00:00Z)

Time         | Event          | Detail
-------------|----------------|-------------------------------------------
13:00:00Z    | open           | run_id, condition=c, offline_mode=False
13:00:14Z    | step_committed | step_1     llm_calls=1
13:00:23Z    | step_committed | step_2     llm_calls=2
...
13:02:30Z    | step_committed | step_9     llm_calls=10  verdict=constrain
13:02:30Z    | step_committed | step_10    llm_calls=11
13:02:30Z    | step_committed | step_11    llm_calls=11  post_refusal_closure=False
13:02:30Z    | close          | exit_code=0
```

Renders the raw events with timestamps. No interpretation.

#### Panel B — Replay result table (per cohort)

```
Case                              | exit_code | similarity | matched | verdict
----------------------------------|-----------|------------|---------|----------
case_01_electroculture            | 0         | 0.9444     | 17/18   | constrain
case_02_policy_governance         | 0         | 0.9444     | 17/18   | constrain
case_03_operational_organizational| 0         | 0.9444     | 17/18   | constrain
```

Pure rendering of `AcceptanceReport.per_case_results`. No new metrics.

#### Panel C — Offline-vs-live diff (per case)

```
Case: case_01_electroculture                                            
                                                                          
Field             | Offline reference     | Live run             | Same? 
------------------|-----------------------|----------------------|------
exit_code         | 20                    | 0                    | NO    
envelopes count   | 11                    | 11                   | yes   
step_9 verdict    | refuse                | constrain            | NO    
step_9 uncertainty count | 4              | 5                    | NO    
step_10 operative count  | 1              | 6                    | NO    
step_10 theoretical count | 4             | 5                    | NO    
step_11 post_refusal_closure | True       | False                | NO    
memory_events     | 15                    | 14                   | NO
```

Pure cell-by-cell comparison of structural fields. No claim about *why* they differ.

#### Panel D — Article VII observations

A read-only table of MemoryLogger events with `capacity_change` event_type, if any have been emitted. As of commit `9397006`, none have been emitted (no consumer writes them yet under Position B), so this panel renders an honest empty state:

```
Article VII capacity_change records:
  (none — Position B implementation made the surface emitable on
   refuse-cases, but no MemoryLogger consumer currently writes
   capacity_change events. Panel will populate when consumers exist.)
```

### 3.3 What the Laboratory Viewer does NOT do

- Does not detect patterns across cases ("all three cases refuse" is not "pattern: bundled deployments are refusable")
- Does not score case-pair similarity (find_reuse_candidates exists; the Viewer does not call it; the operator can invoke it separately if desired)
- Does not interpret the offline-vs-live diff (does not claim either side is "right")
- Does not compute trends over time
- Does not aggregate Article VII capacity records into "capacity trajectories" (would be truth-accumulation)
- Does not flag, alert, or notify on any observation

### 3.4 Doctrinal compatibility

- **Article III (no self-validation):** the Viewer renders observations as raw events + raw diffs. It does not validate either side against the other.
- **Article VII (capacity vs truth):** the Article VII panel renders capacity events as events, not as accumulated truth. The empty state (when no events exist) is honest, not hidden.
- **Anti-pattern-mining discipline:** Panel B shows per-case rows, not aggregate statistics that look like generalizations. Panel C shows per-field diffs, not "similarity verdicts."

### 3.5 Reveal vs Truth tests

- **Reveal:** every field in every panel is extracted from existing artifacts. ✅
- **Truth:** the Viewer states only what the artifacts state. The diff panel's "NO" annotation is a literal comparison, not a judgment. ✅

### 3.6 Critical risk identified

The Laboratory Viewer's risk is **the user's interpretation of the diff panel.** Looking at "step_9 verdict: refuse | constrain | NO" the reader will naturally ask "which is right?" The Viewer must not answer. Mitigations:

- Panel C is labeled "Offline-vs-Live Structural Diff" not "Disagreement Diagnostic"
- Each "NO" cell is a literal comparison; no aggregate "diverged: yes/no" verdict appears
- The Viewer's header text should explicitly state: "Both sides are valid procedural outputs. The Viewer renders the comparison; it does not adjudicate it. For substantive interpretation, see the divergence audit at `notes/elif_post_e2_divergence_audit.md` and the object drift audit at `notes/elif_post_e2_object_drift_audit.md`."

This is the load-bearing discipline. Without it, the Laboratory Viewer becomes a recommendation surface.

### 3.7 Minimum implementation surface

Four pure-functions, each operating over the substrate:

```
def render_memory_timeline(case_id, jsonl_path) -> str
def render_replay_table(acceptance_report) -> str
def render_offline_vs_live_diff(offline_report, live_report) -> str
def render_article_vii_observations(jsonl_paths) -> str
```

**Estimated complexity: ~250-350 LoC total.** All four panels are read-only; none requires LLM calls.

---

## §4 — Exploration Lens Specification (minimal)

### 4.1 Substrate read

Single `RunReport` instance. From that:

- `step_outputs[1].structured_output_dict` (= Step 2) — axes + families
- `step_outputs[5].structured_output_dict` (= Step 6) — scales + cross-scale relations
- `step_outputs[6].structured_output_dict` (= Step 7) — outside-frame trajectories
- `step_outputs[8].structured_output_dict.unresolved_uncertainty_sources` (= Step 9 uncertainty)
- `step_outputs[9].structured_output_dict.theoretical` (= Step 10 theoretical bucket)

### 4.2 Strict answer to the operator's question

**Yes — these five sources can be rendered as an exploration map without changing the procedure, without adding an exploration mode, and without adding a new component.** The reasoning:

1. All five are already in `RunReport.step_outputs` after every successful run
2. None requires LLM calls (they're already produced; the Lens reads them)
3. The Lens is a re-organization of artifacts under a different reading lens, not a new procedural step
4. Position B made even the refuse-branch artifacts populate Step 10's theoretical bucket — so the Lens now works for refuse-cases too (post-G0)

The Lens is therefore implementable today over the v0.1 substrate. **No procedural change required.**

### 4.3 Rendering shape

A single-page view organized as a map with five territories:

```
+============================================================+
|                      EXPLORATION MAP                       |
|                  Case: case_01_electroculture              |
+============================================================+

  [Territory: Decomposition Axes]                            
  ┌───────────────────────────────────────┐                  
  │  Axis 1: mechanism plausibility       │                  
  │    Family A: ... | Family B: ... | C  │                  
  │  Axis 2: decision type bundled        │                  
  │    Family D: ... | Family E: ...      │                  
  │  Axis 3: actor incentive structure    │                  
  │    Family G: ... | Family H: ...      │                  
  └───────────────────────────────────────┘                  
                                                              
  [Territory: Scales]                                        
  ┌───────────────────────────────────────┐                  
  │  Scale 1: organism                    │                  
  │  Scale 2: field                       │                  
  │  Scale 3: institutional               │                  
  │  Cross-scale relations: (rendered)    │                  
  └───────────────────────────────────────┘                  
                                                              
  [Territory: Outside-frame trajectories]                    
  ┌───────────────────────────────────────┐                  
  │  Trajectory 1: ...                    │                  
  │  Trajectory 2: ...                    │                  
  │  ...                                  │                  
  └───────────────────────────────────────┘                  
                                                              
  [Territory: Unresolved uncertainty (Step 9)]               
  ┌───────────────────────────────────────┐                  
  │  - <verbatim uncertainty 1>           │                  
  │  - <verbatim uncertainty 2>           │                  
  │  - ...                                │                  
  └───────────────────────────────────────┘                  
                                                              
  [Territory: Open theoretical questions (Step 10)]          
  ┌───────────────────────────────────────┐                  
  │  - <verbatim theoretical 1>           │                  
  │  - <verbatim theoretical 2>           │                  
  │  - ...                                │                  
  └───────────────────────────────────────┘                  
```

Each territory is a verbatim or near-verbatim extraction. No relationships are drawn between territories. The map is FLAT — five panels of territories, each shown for its own sake. The reader connects them.

### 4.4 What the Exploration Lens does NOT do

- Does not draw edges between axes / scales / trajectories / uncertainties / theoreticals (would imply relationship-claims the substrate does not make)
- Does not rank, score, or prioritize any territory
- Does not suggest which territory to "explore further"
- Does not synthesize the territories into a single map / model
- Does not add new content the Step output did not produce
- Does not omit the verdict — the Decision Room handles the verdict; the Lens deliberately ignores it to keep the lens orthogonal
- Does NOT create a procedural mode where exploration is the deliverable — it renders existing artifacts under a new lens; the run that produced the artifacts was still an arbitration run

### 4.5 Doctrinal compatibility

- **Article II (frame humility):** the territories include Step 7's outside-frame trajectories — frame humility is rendered, not eroded
- **Article VI (anti-premature-convergence):** the Lens deliberately does NOT converge on a recommendation; it stays in the open territory space
- **Article VII (capacity vs truth):** the Lens does not accumulate territories as truths; it shows them as artifacts

### 4.6 The most important doctrinal observation

**The Exploration Lens is the doctrinal vindication of the prior emergence audit's finding that "Exploration Room may emerge as a re-reading of existing artifacts."** It is non-additive — adds no substrate. It is non-procedural — does not modify any prompt or schema. It is non-canonical — could be removed without affecting any other surface. **It is purely a perspectival choice over existing data.**

### 4.7 The operator's risks revisited

Recall the operator's risks from the emergence audit: exploration theater / infinite decomposition / curiosity without convergence.

- **Exploration theater:** the Lens renders verbatim artifacts. Theatricality is impossible because nothing is invented.
- **Infinite decomposition:** Step 2's 2-4 axis cap, Step 6's ≥2 scale floor, Step 7's structured trajectory schema — all already bound the territory count. The Lens does not relax these bounds.
- **Curiosity without convergence:** convergence is provided by Step 9 verdict (Decision Room). The Lens does not convergence; it deliberately stays in the pre-convergence territory.

All three risks are defended by the substrate before the Lens reads it. The Lens does not need additional defenses.

### 4.8 Reveal vs Truth tests

- **Reveal:** every territory is extracted from existing step_outputs. ✅
- **Truth:** the Lens shows what the artifacts show. No edges, no synthesis, no claim. ✅

### 4.9 Minimum implementation surface

A pure-function: `def render_exploration_lens(run_report: RunReport) -> str`. No state. No reasoning. No I/O beyond input/output.

**Estimated complexity: ~120-180 LoC for Markdown rendering with the five-territory layout.**

---

## §5 — Object Drift Panel Specification

### 5.1 Substrate read

Single `RunReport` instance. From that:

- `step_outputs[0].structured_output_dict` (= Step 1) — frame_validator output (verdict + reformulated_frame if present)
- `step_outputs[1].structured_output_dict` (= Step 2) — object decomposition
- `step_outputs[3].structured_output_dict` (= Step 4) — hypotheses
- `step_outputs[5].structured_output_dict` (= Step 6) — multi-scale
- `step_outputs[6].structured_output_dict` (= Step 7) — outside-frame trajectories
- `step_outputs[7].structured_output_dict` (= Step 8) — stage-gated roadmap
- `step_outputs[8].structured_output_dict` (= Step 9) — verdict
- (Optional) `cases/<case_id>/input_frame.md` — the original input frame text for back-reference

### 5.2 Critical design constraint

The Object Drift Panel must not CLAIM to detect drift. It must RENDER the chain in a way that lets the human reader observe whether drift happened. **If the Panel asserts "drift detected" it has crossed into Article III self-validation.** The Panel's job is to show; the reader's job is to see.

### 5.3 Rendering shape

A vertical chain with seven nodes (Steps 1, 2, 4, 6, 7, 8, 9) plus an anchor at the top for the input frame:

```
+==================================================================+
|                    OBJECT CHAIN VIEWER                            |
|                Case: case_01_electroculture                       |
+==================================================================+

  [ANCHOR — Input Frame]
  ┌─────────────────────────────────────────────────────────────┐
  │  Verbatim input frame text:                                 │
  │  "A coalition of agricultural researchers, environmental    │
  │   agencies, and private agritech companies is considering   │
  │   launching a large-scale research and pilot deployment     │
  │   program around electroculture techniques..."              │
  │                                                              │
  │  Reading lens (constant; not run-specific):                 │
  │  "The object as posed: the bundled deployment proposal      │
  │   authorized by the coalition."                             │
  └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
  [STEP 1 — Frame Validation]
  ┌─────────────────────────────────────────────────────────────┐
  │  verdict: needs_decomposition                               │
  │  reformulated_frame:                                        │
  │    "Per technique in the proposed list, what evidence       │
  │     quality and mechanism plausibility exists..."           │
  │                                                              │
  │  Reading lens: "The object as Step 1 reformulates it."       │
  └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
  [STEP 2 — Object Decomposition]
  ┌─────────────────────────────────────────────────────────────┐
  │  Axes: <list>                                               │
  │  Families per axis: <list>                                  │
  │                                                              │
  │  Reading lens: "The object as a partition across axes."     │
  └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
  [STEP 4 — Hypotheses with distinguishing predictions]
  ┌─────────────────────────────────────────────────────────────┐
  │  Hypotheses: H1, H2, H3, ...                                │
  │                                                              │
  │  Reading lens: "The object as claims about outcomes."        │
  └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
  [STEP 6 — Multi-scale relations]
  ┌─────────────────────────────────────────────────────────────┐
  │  Scales: <list>                                             │
  │  Cross-scale relations: <list>                              │
  │                                                              │
  │  Reading lens: "The object as a system across scales."      │
  └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
  [STEP 7 — Outside-frame trajectories]
  ┌─────────────────────────────────────────────────────────────┐
  │  Trajectories: <list>                                       │
  │                                                              │
  │  Reading lens: "The object as one element of a space of     │
  │                  alternatives."                              │
  └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
  [STEP 8 — Stage-gated roadmap]
  ┌─────────────────────────────────────────────────────────────┐
  │  Stages: <list with stage_id, description, gate>            │
  │                                                              │
  │  Reading lens: "The object as a procedural artifact —       │
  │                  a roadmap. (NOTE: this step is the          │
  │                  bifurcation point per object drift audit;   │
  │                  the roadmap may describe world-actions OR   │
  │                  analytical deliverables. Reader observes    │
  │                  which.)"                                    │
  └─────────────────────────────────────────────────────────────┘
                            │
                            ▼
  [STEP 9 — Verdict]
  ┌─────────────────────────────────────────────────────────────┐
  │  verdict: <verdict>                                          │
  │  verdict_detail: <paragraph>                                │
  │                                                              │
  │  Reading lens: "The verdict's referent — what the verdict   │
  │                  is ABOUT — is whatever Step 8 produced.     │
  │                  Reader observes whether this is still the   │
  │                  input frame's deployment question or       │
  │                  Step 8's procedural artifact."              │
  └─────────────────────────────────────────────────────────────┘
```

The reading-lens annotations are **constant strings** — they describe what each step's output IS, structurally. They do not vary per case. The reader applies them to the rendered content and forms their own judgment about whether the chain stays anchored to the input frame.

### 5.4 What the Object Drift Panel does NOT do

- Does NOT claim "drift detected" or "drift not detected"
- Does NOT compute a "drift score"
- Does NOT flag specific steps as "where drift happened"
- Does NOT compare the Step 8 stages to the input frame and report dissimilarity
- Does NOT mark the bifurcation point with anything beyond the constant note at Step 8
- Does NOT propose remediation

### 5.5 The single load-bearing semantic choice

The reading-lens annotations are the only departure from pure rendering. They are constant strings authored from the object drift audit's findings. They are **not** computed per-run. They are essentially **labels of what each step's output is, structurally.**

This is the borderline between revealing and building. My judgment: constant labels that describe what the substrate already produces are *revealing*. They do not add reasoning; they do not introduce new metrics; they orient the reader to what they are looking at. The labels would still be true even if the reader disagreed with the object drift audit's conclusions — they describe the step's *kind of output*, not its quality.

Alternative if even this is too much: render the chain without the reading-lens annotations. Pure step-output content + step-id headers. The reader applies their own labels. This is the **strict minimum**.

### 5.6 Doctrinal compatibility

- **Article II (frame humility):** the anchor surface (input frame at top + Step 1 reformulated_frame) preserves the original frame as a referent — this is the only viewer surface that does so. It is also the panel that surfaces the absence of back-reference for the reader to observe.
- **Article III (no self-validation):** the Panel renders; does not validate.
- **Article VII (capacity vs truth):** no truth claim is accumulated; the chain is observed, not adjudicated.

### 5.7 The Panel's most important property

**The Object Drift Panel is the only viewer surface that makes the object-drift phenomenon observable inside the substrate.** The other viewers render artifacts as they were intended. This viewer renders artifacts under a lens that the object drift audit revealed.

Without this Panel, the divergence between refuse and constrain remains a finding in a notes file. With this Panel, the divergence becomes observable per-case at run time, by a human reader, without claim, score, or judgment from the system.

### 5.8 Reveal vs Truth tests

- **Reveal:** every rendered field is extracted from existing artifacts. The reading-lens annotations describe what each step's output IS, structurally. ✅
- **Truth:** the Panel does not claim drift occurred. It renders the chain. The reader sees. ✅ (with the caveat noted in §5.5 about reading-lens annotations being a borderline case)

### 5.9 Minimum implementation surface

A pure-function: `def render_object_chain(run_report: RunReport, input_frame_path: Optional[Path]) -> str`. The input_frame_path argument is optional; if provided, the anchor section includes the verbatim frame text. If not, the anchor section is omitted.

**Estimated complexity: ~200-280 LoC for Markdown rendering.** Higher than other panels because the chain is longer and each node carries more structure.

---

## §6 — World-Model Seam Observation

### 6.1 What was NOT asked

The operator explicitly prohibited: world-model integration, simulator hosting, Phase 7 opening, Phase 8 opening. This section observes **seams** — structural locations where a world model could attach without modifying the substrate. Observation only.

### 6.2 The four rooms as a rendering layer

The four viewers — Decision Room, Laboratory Viewer, Exploration Lens, Object Drift Panel — share a structural property: they are **read-only renderings over `RunReport` instances and their associated artifacts.** None of them touches:

- Procedure execution (orchestration_runner.py)
- Component logic (the seven components)
- Schemas
- Closed-set vocabularies
- Articles I-VII
- Phase gates

This means the four viewers form a **rendering layer that is structurally independent of the substrate.** Removing all four would not affect any procedural surface.

### 6.3 Where world models could attach (seams)

A world model — defined here as *a queryable representation of the input frame's actual entities* (the coalition, the deployment, the regions, the population, the timeline) — could attach at five seams without modifying ELIF's substrate:

#### Seam 1 — Decision Room verdict-detail entity resolution

The verdict_detail prose in Step 9 references entities like "the coalition," "Family A," "pilot deployment authority." A world model could resolve these references to entries in a separate world-model store. **Implementation: a side panel adjacent to the Decision Room that displays "this verdict's entity references resolved against world model X."** The Decision Room itself is unchanged. The world model is consulted by the side panel only. No substrate modification.

#### Seam 2 — Laboratory Viewer cross-case grounding

The Lab's offline-vs-live diff panel shows "step_9 verdict: refuse | constrain | NO." A world model could augment this by resolving each verdict's referent ("the bundle as posed in input frame X" vs "Stage 8 roadmap A1-A5") to entries in the world model. **Implementation: an annotation layer on the diff cells.** The Lab itself is unchanged.

#### Seam 3 — Exploration Lens territory grounding

The Lens renders five territories (axes, scales, trajectories, uncertainty, theoretical). A world model could overlay these with "this territory corresponds to a real region of the input frame's world." **Implementation: hover-text or footnotes on each territory.** The Lens itself is unchanged.

#### Seam 4 — Object Drift Panel anchor expansion

The Panel's anchor section renders the input frame text. A world model could expand the anchor with structured entity extraction ("the coalition" = {member: agritech_companies, member: environmental_agencies, ...}). **Implementation: an expanded anchor section.** The Panel itself is unchanged.

#### Seam 5 — Reference markdown enrichment

The reference markdown files at `results/<case_short>/condition_c_output.md` are operator-authored prose. A world model could be referenced by the prose ("Family C members include [Christofleau-style antennas, Lakhovsky oscillators]" — where the bracketed list is resolved against the world model). **Implementation: pre-render the reference with world-model annotations.** The reference content itself is preserved.

### 6.4 What the seams have in common

**All five seams attach AT THE RENDERING LAYER, not at the substrate.** None of them requires modifying any procedural component. Each viewer would gain an optional world-model overlay; the viewer's core rendering remains unchanged.

This means: **if a world model is ever introduced (which is out of scope for this audit), the four viewers are forward-compatible with it as overlays.** The viewers do not need to be redesigned. The substrate does not need to be modified. The world model attaches at the rendering layer and either adds value to the viewers or does not — the viewers function identically with or without it.

### 6.5 The single structural property this exposes

**ELIF's core identity is the procedural substrate (the seven components + Articles + closed-set vocabularies + 11-step procedure).** The four viewers do not touch this. A world model, if introduced as a rendering-layer overlay, would also not touch this. **The substrate's core identity is preserved across the introduction of viewers and the future introduction of world models — provided both stay at the rendering layer.**

The seam analysis does not propose introducing world models. It observes that the seams exist and are clean.

### 6.6 What this seam observation does NOT do

- Does not propose a world model
- Does not propose Phase 7 / Phase 8 opening
- Does not propose any orchestration of world models with the substrate
- Does not propose simulator hosting
- Does not propose any LLM-mediated grounding of entities
- Does not propose any cache, store, or persistence layer for world-model state
- Does not propose any API by which the viewers would consult a world model (that's an implementation question and out of scope)

It only observes that **the rendering layer is structurally compatible with future world-model overlays without requiring substrate modification.**

---

## §7 — Complexity / Risk Analysis

### 7.1 Per-viewer complexity (rough LoC estimates)

| Viewer | Estimated LoC | Pure function? | LLM calls? |
|---|---|---|---|
| Decision Room | 60-150 | Yes | No |
| Laboratory Viewer (4 panels) | 250-350 | Yes (per panel) | No |
| Exploration Lens | 120-180 | Yes | No |
| Object Drift Panel | 200-280 | Yes | No |
| **Total** | **~650-960 LoC** | Yes | No |

All viewers are pure functions over existing artifacts. None requires LLM calls, network access, or persistent state. The full viewer suite is sub-1000 LoC and zero-billing per invocation.

### 7.2 Per-viewer risk

| Viewer | Risk class | Specific risk |
|---|---|---|
| Decision Room | **Low** | Reader treats the verdict as authoritative without reading verdict_detail. Mitigated by always-visible verdict_detail + uncertainty sources. |
| Laboratory Viewer | **Medium** | Reader interprets the offline-vs-live diff panel as a "who is right" surface. Mitigated by §3.6 header text and structural design (per-field literal diffs, no aggregate verdict). |
| Exploration Lens | **Low** | Reader treats territories as exhaustive. Mitigated by the Lens explicitly rendering each territory as "what Step N produced" not "all there is." |
| Object Drift Panel | **Medium-High** | Reader treats the constant reading-lens annotations as truth claims about drift. Mitigated by the strict-minimum option (§5.5 alternative: omit annotations entirely). The Panel is the highest-risk viewer because its purpose is to make drift observable; the discipline that prevents it from claiming drift is the most easily eroded. |

### 7.3 Cross-viewer risk

**The four viewers in combination create a comprehensive ELIF visibility layer.** This is the visibility the operator requested. The risk is that the visibility layer becomes the perceived ELIF — readers interact with the viewers and treat them as the canonical interface, conflating "what ELIF is" with "what is rendered."

Mitigations:
- Each viewer must explicitly identify itself as a rendering, not a substrate
- Each viewer must link to the substrate artifacts it renders (e.g., the JSON file paths, the source files)
- Each viewer must include a disclaimer pointing at the relevant audit (object drift, divergence, emergence) so the reader can ground their interpretation

### 7.4 Doctrinal risk

**The four viewers do not modify Articles I-VII.** They render under the Articles' constraints. The doctrinal risk is not in the viewers themselves but in the operator's interpretation of what the viewers reveal. Specifically:

- The Object Drift Panel makes the constitutional blind spot (Article VII's silence on referent) observable. Once observable, the operator faces a question the doctrine cannot answer: *should the substrate detect drift?* Answering yes opens implementation work (out of scope for this spec). Answering no preserves the substrate's current architecture but accepts that the blind spot will remain visible per-run.
- The Laboratory Viewer's offline-vs-live diff panel makes the §6.1 similarity scorer's content-blindness observable. Once observable, the operator faces a question about whether the benchmark's structural-similarity-as-success contract is sufficient. The viewer does not push toward an answer; the question becomes visible.

**The viewers' job is to make the substrate observable. The questions the substrate cannot answer become observable too. This is a feature, not a bug — but it changes the operator's decision surface.**

### 7.5 What the visibility layer does NOT do

- Does not introduce any new arbitration capability
- Does not change what the substrate can decide
- Does not modify the procedural arc
- Does not propose architecture
- Does not open phases
- Does not provide closure on E.2 or anything that follows from E.2

It only makes existing substrate observable. **Whether observation is enough is the operator's call. The visibility layer does not ask the question — it makes the question available to be asked.**

### 7.6 Implementation surface (read-only spec; not a build proposal)

If the operator chooses to materialize the visibility layer:

- Single file or package: `src/elif_v0_1/viewers/` with four pure-function modules
- No new dependencies (Markdown rendering is Python-native; HTML rendering can use standard library)
- No new tests required beyond `def test_viewer_renders_runreport()` per viewer (the viewers are pure functions; testing is trivial)
- No new schemas
- No new closed-set vocabularies
- No procedural modification
- No memory layer
- No state

This is the smallest possible visibility layer over the current substrate. **Even smaller versions are possible — e.g., implementing only the Decision Room, or only the Object Drift Panel — and each is independently useful.**

---

## §8 — Summary

ELIF v0.1's substrate already contains:
- Decision artifacts (Step 9 + 10 + 11 outputs)
- Laboratory artifacts (MemoryLogger JSONL + replay results)
- Exploration artifacts (Step 2 + 6 + 7 + 9 uncertainty + 10 theoretical)
- Object Drift artifacts (Step 1 → 2 → 4 → 6 → 7 → 8 → 9 chain)

**These artifacts are currently invisible because no rendering surface exposes them at the operator's interaction layer.** The four viewers specified above expose them. They are:

- **Decision Room:** ~60-150 LoC pure-function. Renders Step 9 + 10 + 11 from a single RunReport. Doctrinally compatible. Low risk.
- **Laboratory Viewer:** ~250-350 LoC across four panels (memory timeline, replay table, offline-vs-live diff, Article VII observations). Doctrinally compatible. Medium risk (the diff panel must stay literal, not adjudicatory).
- **Exploration Lens:** ~120-180 LoC pure-function. Renders five territories as a flat map. **The doctrinal vindication of the prior emergence audit's finding.** Low risk.
- **Object Drift Panel:** ~200-280 LoC pure-function. Renders the seven-step chain with optional constant reading-lens annotations. **The first surface that makes the object-drift phenomenon observable per-run.** Medium-high risk (annotations are borderline reveal-vs-build; strict minimum without annotations is also viable).

Total visibility layer: ~650-960 LoC. Zero LLM calls. Zero billing per invocation. No new schemas, no new vocabularies, no procedural modification, no doctrinal change.

**The four viewers form a rendering layer structurally independent of the substrate.** A future world model, if introduced, could attach as a rendering-layer overlay at any of five identified seams without modifying the substrate. **This is observation only; no world model is proposed.**

**The visibility layer makes the substrate observable. It does not change what the substrate is.** Whether the operator chooses to materialize it is outside this spec.

---

## §9 — What this specification does NOT do

- Does not propose implementation
- Does not propose a roadmap entry
- Does not propose phase activation
- Does not propose a new component
- Does not propose a new Article
- Does not modify any schema
- Does not modify any closed-set vocabulary
- Does not modify the procedure
- Does not propose world-model integration
- Does not propose simulator hosting
- Does not propose Phase 7 / Phase 8
- Does not adjudicate the E.2 verdict-class divergence
- Does not close Phase 1
- Does not open any subsequent phase
- Does not recommend whether to build the visibility layer

**The specification is a strict reveal-vs-build audit + minimum-surface description for each viewer + seam observation + complexity/risk analysis. Nothing more.**

The governing principle: *Do not build more ELIF. Reveal the ELIF that already exists.* The spec describes what revelation would look like at minimum cost, in strict doctrinal compatibility, with risks identified.

What follows from a specification is the operator's call.

---

## References

- Prior emergence audit: [elif_post_e2_room_emergence_audit.md](elif_post_e2_room_emergence_audit.md)
- Prior divergence audit: [elif_post_e2_divergence_audit.md](elif_post_e2_divergence_audit.md)
- Object drift audit: [elif_post_e2_object_drift_audit.md](elif_post_e2_object_drift_audit.md)
- E.2 live replay report: [elif_v0_1_e2_live_replay_report.md](elif_v0_1_e2_live_replay_report.md)
- Position B implementation: commit `44b3e6e`
- Substrate source: `src/elif_v0_1/`
- Reference outputs: `results/case_*/condition_c_output.md`

---

**Specification closed. No build proposed. ELIF remains in review state. Reality remains sovereign.**
