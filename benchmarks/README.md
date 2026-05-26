# benchmarks/

This directory tracks the **schemas** for benchmark runs, not the run outputs themselves. Run outputs live in `results/`.

- `differentiator_tracking.md` — schema for capturing observed differentiators across cases
- `component_engagement_tracking.md` — schema for capturing which components engaged per case

After each case is run, the actual data goes into `results/case_NN/` and the schemas in this directory may be revised if a benchmark-blocking ambiguity is found.
