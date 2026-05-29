# Case 01 — Electroculture

**Status:** Original Round 7 run (pre-procedure-v1.0, human-executed Condition C). Re-executed 2026-05-28 under procedure v1.0 / E1.5 for matching evidence structure with Cases 02 and 03 — see `results/case_01/`. This README is preserved as historical reference to the original Round 7 documentation.

**Domain:** Scientific / ambiguous-evidence

**Purpose this case served:** First demonstration that ELIF-mode produces behavior distinct from bare LLM and structured-prompt baselines on a domain with collapsed heterogeneous objects and ambiguous evidence.

**Differentiators observed (preliminary):**
- Frame refusal — original question refused and required decomposition
- Object decomposition into 4 mechanism families before reasoning
- Hypotheses H1–H5 with distinguishing predictions and failure conditions
- Branching experimental roadmap with stages 0–6 and decision gates
- Explicit operative vs theoretical truth separation
- 5 governance rules expressed as refusal conditions (under-tested without conflict case)

**Caveat:** Condition C was produced by a human thinking in ELIF mode, on a prepared example. The architecture-vs-cognition question is not yet resolved by this case alone.

**Next:** re-document under the locked benchmark template once `procedure/benchmark_template.md` is finalized.
