# Future Audit — World-Model Integration

**Status:** DEFERRED. Placeholder only. No architectural commitments.

**Date raised:** 2026-05-27
**Earliest revisit:** Post Phase 1 (cases 2 and 3 authored + executed)
**Recommended revisit:** Post Phase 2 (constitutional compression complete; evidence available about whether Article VII operationalized cleanly)
**Latest revisit:** Phase 6 (when world-model orchestration is actually scheduled)

---

## Why this is deferred

Producing schemas, registries, connector architectures, or arbitration processes now would:
- Author Phase 6 architecture while Phase 0 gates remain unsatisfied
- Treat speculation as architecture (Article I drift)
- Violate the locked stabilization posture
- Demonstrate momentum capture on day one of the plateau

The settling test must run on these questions. If they persist through silence and through benchmark pressure, they return later stronger and cleaner.

---

## Questions to preserve (raised 2026-05-27, verbatim)

The operator asked for:

1. **Classification of "world models"** for ELIF v0.x — should this include: external LLMs, scientific models, simulation engines, economic models, climate models, biological models, industrial/logistics models, geopolitical models, datasets + inference tools, agent systems, knowledge graphs, digital twins?

2. **First realistic integration layer** — API connectors, file/dataset ingestion, research paper ingestion, simulation outputs, LLM-as-specialist calls, structured model adapters, manual model outputs pasted into the system?

3. **Buy / build / rent / connect** — for each category, classify as external API, open-source model, SaaS tool, local model, custom-later, do-not-build-now.

4. **Correct "World Model Connector" architecture** — proposed shape: ELIF Core → Model Registry → Connector Adapter → Query Formatter → External Model / Simulation → Response Normalizer → Evidence / Assumption Extractor → Cross-Model Arbitration → Governance Kernel → Memory Logger.

5. **Schema for world-model response** — proposed fields: model_id, domain, input_case_id, assumptions, predicted_outcomes, uncertainty, confidence, evidence_basis, known_limits, operational_constraints, refutation_conditions, dependencies, recommended_next_test, raw_output, normalized_output.

6. **How ELIF compares conflicting model outputs** — rank? decompose assumptions? identify contradiction classes? produce arbitration graph? generate experimental pathway? trigger governance refusal? request more evidence?

7. **Realistic priority order** — proposed phases: LLM specialist connectors + paper ingestion (Ph 1) → scientific datasets + economic calculators + public APIs (Ph 2) → domain-specific simulators (Ph 3) → digital twins / sensors / institutional systems (Ph 4).

8. **What should NOT be integrated yet** — live sensors, autonomous agents, institutional systems, financial execution, medical decision systems, high-risk infrastructure, self-triggering pipelines.

9. **Doctrine preservation during integration** — how Articles I (Non-Absolutization), III (No Self-Validation), IV (Partiality of Models), VII (Capacity without truth) are enforced inside connector architecture.

10. **GitHub artifacts** — proposed: `docs/world_model_integration_plan.md`, `schemas/world_model_response.schema.json`, `connectors/README.md`, `registry/world_models.registry.json`, `benchmarks/world_model_arbitration_template.md`.

---

## Revisit conditions (binding)

This audit may be opened when ALL of the following hold:

- [ ] Cases 2 and 3 input frames authored
- [ ] Cases 2 and 3 executed through three conditions
- [ ] Article VII longitudinal tracking captured across cases 1, 2, 3
- [ ] Phase 2 constitutional compression evaluated
- [ ] Roadmap Phase 3-5 gate criteria reviewed under benchmark evidence
- [ ] Operator explicit decision to open this audit

If ANY of the above is unmet, this file stays a placeholder. The questions wait.

---

## What this document is NOT

- A schema specification
- A connector architecture
- A registry proposal
- An arbitration process
- A phasing commitment beyond the roadmap
- Permission to begin Phase 6 work

It is a question-preservation artifact only.
