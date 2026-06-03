# ELIF Execution & State Contract

## 1. Mutation & Authority Matrix
| Role | Allowed to Mutate | Permission Level |
| :--- | :--- | :--- |
| **Engine (Layer 1)** | `Planet`, `Inquiry Object` (metadata), `Inquiry History` | **Full Read/Write** on reasoning substrate. |
| **Inquiry (Layer 2)** | `History Log`, `Confidence Vector` | **Append-Only** persistent state. |
| **Rooms (Layer 3)** | `RoomState` (internal interaction data) | **Strictly Read-Only** relative to Inquiry/Engine. |
| **User** | `Refinement Directives` | **Indirect Mutation** via trigger functions only. |
| **Governance Room** | `Engine Execution` | **Execution Authority** (Interrupt/Block). Cannot modify reasoning content. |

---

## 2. Sync Pulse Output & Run Identity Contract
A "Sync Pulse" is a deterministic state transition. Every pulse must append a **Run Identity** to the persistent history to ensure traceability:

```json
{
  "run_id": "UUID",
  "parent_run_id": "UUID | null",
  "mutation_source": "USER | GOVERNANCE | ENGINE",
  "delta_type": "QUESTION | CONSTRAINT | CONTEXT | NONE",
  "pulse_timestamp": "ISO-8601",
  "step_outputs": {
    "1..11": "Structured Step Data"
  },
  "confidence_vector": [0.0...1.0],
  "active_constraints": ["constraint_id", ...]
}
```

---

## 3. State Transition Rules & Dependency Scoping
To prevent chaotic loops and inconsistent hybrids, ELIF follows strict dependency-aware transition logic:

| Input Change | Triggered Action | Dependency Rule |
| :--- | :--- | :--- |
| **Question State Change** | **Full Pipeline Rerun (Steps 1–11)** | Invalidates ALL internal nodes. |
| **Constraint Refinement** | **Partial Rerun (Steps 4–9)** | Invalidates all downstream dependent nodes (10, 11). |
| **Context/Signal Add** | **Partial Rerun (Steps 3–6)** | Invalidates all downstream dependent nodes (7, 8, 9, 10, 11). |
| **UI Room Navigation** | **No Rerun** | Read-only projection from existing RoomState cache. |

**Invalidation Rule**: If Step $N$ is recomputed, all steps where $M > N$ must be marked as `STALE` and cleared from the projection until re-validated by the current pulse.

---

## 4. Governance Authority & Decision Separation
The Governance Room operates as the system's "Constitutional Court" with strict separation between analysis and execution:

### §4.1 Separation of Reasoning vs. Action
*   **Interpretation Phase**: The Governance Room first generates a "Governance Rationale" (Prose/Logic) which is visible to the operator but has NO execution effect.
*   **Execution Phase**: Only upon a "Final Signature" (Automated or Manual) does the Governance result commit one of the following levels. This prevents "Double-Commit" drift.

### §4.2 Authority Levels
*   **Level 0 (Advisory)**: Surfacing of minor inconsistencies (Warning only).
*   **Level 1 (Constraint Injection)**: Enforces immutable boundaries. 
    *   **Stacking Policy**: Level 1 constraints **stack** by default. 
    *   **Conflict Resolution**: If a new Level 1 constraint contradicts an existing one, the Engine triggers an immediate **Level 2 Block** (System cannot resolve self-contradiction).
*   **Level 2 (Execution Block)**: Full halt (exit_code=20). 

---

## 5. Termination & State Equality Definitions
The system stops iterating based on the **State Equality Metric** to prevent infinite loop drift:

### §5.1 State Equality Metric
Two state snapshots are considered **Identical** if and only if:
1.  **Confidence Vector**: All float values match within a precision tolerance of $\epsilon = 0.001$.
2.  **Structural Integrity**: The hash of `step_outputs` (excluding timestamps/IDs) is identical.
3.  **Unresolved Zones**: The set of `zone_ids` is mathematically equivalent.

### §5.2 Terminal Conditions
*   **Hypothesis Closure**: Binary match between Step 5 (Design) and Step 11 (Audit).
*   **Acceptable Uncertainty**: `residual_darkness` falls below user-set `Confidence Threshold`.
*   **System Stasis**: Convergence reached via State Equality Metric.
*   **Convergence Lock**: Once stable, the "Sync Engine" button is visually disabled.

## 6. Audit & State Observability
Every "Sync Pulse" must be accompanied by an entries in the `MemoryLogger` (Step 11) using the following Event Schema:
*   `COGNITIVE_TRANSITION`: Tracking the movement from Step N to Step N+1.
*   `MUTATION_AUTHORITY`: Logging who (Engine, User, Governance) triggered the state change.
*   `DRIFT_SCORE`: A comparative metric between the `Input Frame` and the `Current Question State`. If the score exceeds 40%, the Governance Room triggers a **Level 2 Execution Block**.

