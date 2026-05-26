# Minimum Viable ELIF Architecture (current)

**Status:** Provisional. Subject to reclassification after benchmark cases 2 and 3. May compress to fewer than 7 components. May expand by ≤2 candidates from current B-tagged procedure steps. See `procedure/abcd_classification_system.md`.

## Components

| # | Component | Purpose | Experimentally validated? |
|---|---|---|---|
| 1 | [Frame Validator](01_frame_validator.md) | Inspects input questions for collapsed heterogeneous objects, false binaries, context-blind framings. Refuses to proceed until decomposed. | Yes — strong on case 01 |
| 2 | [Object Decomposer](02_object_decomposer.md) | Separates collapsed labels into distinct mechanism / category families before reasoning proceeds. | Yes — strong on case 01 |
| 3 | [Hypothesis Validator](03_hypothesis_validator.md) | Enforces that hypotheses include distinguishing predictions and failure conditions. Rejects "concerns" masquerading as hypotheses. | Yes |
| 4 | [Branching Roadmap Engine](04_branching_roadmap_engine.md) | Produces staged experimental pathways with continuation thresholds, branch conditions, and evidence-based routing. | Yes — strong on case 01 |
| 5 | [Governance Kernel](05_governance_kernel.md) | Immutable refusal conditions that override the answering layer. Constitutional pattern. | Structurally real, under-tested without conflict case |
| 6 | [Operative Truth Separator](06_operative_truth_separator.md) | First-class distinction between scientific / theoretical plausibility and operational viability. | Yes, but flagged "portable to prompting" — final classification pending case 2/3 |
| 7 | [Feedback / Memory Logger](07_feedback_memory_logger.md) | Records predictions, outcomes, deviations, corrections. Reality as final validator. | Not yet tested |

## Compression notice

Per Rule 2 (Failure-Permitted Architecture), this list is allowed to shrink. If after cases 2 and 3, only 3 components survive evidence pressure (e.g., Frame Validator, Governance Kernel, Branching Roadmap Engine), that is a valid result, not a failure.

## Not in this list (intentionally deferred)

- CIM (Civilizational Intelligence Matrix)
- ORC (organic dynamic substrate)
- Decision Room UX
- Multi-agent collaborative reasoning environment
- Population-scale adaptive feedback loops
- Cross-domain transfer validation
- Long-term structural memory

These are real concepts but not in the current architecture. They re-enter the discussion only after the minimum architecture proves reliable.
