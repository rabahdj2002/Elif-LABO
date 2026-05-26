# Case 01 — Electroculture

**Status:** Run (Round 7). Documented post-hoc in `results/case_01_electroculture/` (to be created).

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
