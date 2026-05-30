# ELIF Post-E.2 — Object Drift Audit

> **Status:** HIGH-PRIORITY RESEARCH AUDIT. Non-canonical. Evidence-driven. Reality-subordinate.
> **Trigger:** operator request 2026-05-30 — "the possibility that the divergence is not a verdict divergence; it may be an object divergence."
> **Discipline:** Determine whether **object transformation, object drift, or object substitution** is a real phenomenon inside ELIF, or an illusion created by its own procedure.
> **Closes nothing. Opens nothing. No recommendation. No proposal. No new component / Article / phase / surface.**

This audit goes a layer deeper than [elif_post_e2_divergence_audit.md](elif_post_e2_divergence_audit.md). The prior audit identified the phenomenon at Step 8. This audit asks: is the phenomenon real? Is it structural? Is it diagnosable? Or is it an artifact of how we read the procedure?

---

## Method

I trace **the object of inquiry** through each procedural checkpoint (Steps 1, 2, 4, 6, 7, 8, 9) for each of the 3 benchmark cases. "The object" is the noun the step is operating on. I extract it from:

1. The verbatim Step N output (what the step actually produced)
2. The Step N prompt structure (what the step was asked to produce)
3. The implied referent (what the output is *about*)

Where the object can be characterized in one phrase, I phrase it. Where the object cannot be cleanly named, I record the ambiguity. I do not invent objects to make the chain look continuous.

I run this trace separately for the operator's Condition C reference and the live model's run, then compare.

---

## PART I — Object Continuity Mapping

### Case 01 (electroculture) — object chain

| Step | Operator object | Model object | Same? |
|---|---|---|---|
| **1** | The coalition's bundled deployment proposal (passive antennas + copper devices + weak electrical stim + electroculture irrigation) | Same | YES |
| **2** | The proposal decomposed across three axes: mechanism plausibility per technique / decision type per stage / actor incentive structure | The proposal decomposed (similar axes, slightly different naming) | YES — but the proposal is no longer one object; it is now three families × six techniques = 18 sub-objects within an axis structure |
| **4** | Hypotheses *about outcomes* of each technique-family — testable claims under each Family A/B/C variant | Hypotheses about outcomes (similar shape) | YES — but the object has subtly drifted from "the proposal" to "claims about what the proposal will do." The proposal is now upstream of the object. |
| **6** | Multi-scale dynamics — organism / field / institutional / generational scales of the same techniques | Multi-scale dynamics across similar scales | YES — but now the object is "the *system context* in which the proposed action would unfold." Two more steps of abstraction from the proposal. |
| **7 mode A** | Outside-original-frame trajectories — what alternatives exist if you reject the bundle-as-posed | Outside-frame trajectories (similar shape) | YES — but the object is now "the *space of alternatives* to the proposal," which is no longer the proposal at all. The proposal has become a *reference point* rather than the object. |
| **8** | A 5-stage roadmap of **world actions**: research funding → pilot authority → field deployment, each gated on real-world evidence outcomes | A 5-stage roadmap of **analytical deliverables**: layer-attribution table → compatibility matrix → unit-of-analysis memo → comparison-case rubric → integrated decision package, each gated on document existence + reviewer sign-off | **★ NO — DIVERGENCE.** Operator's object remains "what should happen in the world." Model's object becomes "what analytical deliverables should be produced." |
| **9** | Verdict over the operator's Step 8 + hybrid back-reference to Step 1 ("Refuse the bundle. Constrain disaggregated components.") | Verdict over the model's Step 8, no back-reference to Step 1 ("authorize Stage 8 roadmap A1-A5 to proceed under explicit constraints") | NO — verdicts attach to different objects |

### Case 02 (policy governance — autonomous AI-driven crop ecosystems) — object chain

| Step | Operator object | Model object | Same? |
|---|---|---|---|
| **1** | The coalition's bundled deployment (autonomous irrigation + GE crops + predictive weather + microbial engineering + AI pest/antibiotic management) | Same | YES |
| **2** | Decomposed across reversibility profiles + actor incentive structures | Decomposed across similar axes | YES |
| **4** | Hypotheses about outcomes per family (reversibility-bounded outcomes) | Hypotheses about outcomes | YES |
| **6** | Multi-scale: molecular / agroecological / generational / regulatory | Similar scales | YES |
| **7 mode A** | Outside-frame: agroecological adaptation alternatives, scenario-dependence | Similar outside-frame trajectories | YES |
| **8** | Roadmap of world actions: reversible track authorized, partially-reversible requires protocol, irreversible refused | Roadmap of analytical deliverables: institutional inventory, scalar measurement invariance (RMSEA ≤ 0.06), cross-level correlation across ≥2 comparison cases | **★ NO — DIVERGENCE.** Same shift: world-action vs methodology |
| **9** | "Refuse the bundled authorization. Constrain disaggregated components." (hybrid back-reference to Step 1) | "Stage 8 roadmap authorized to proceed under T×R×G configuration constraints + scalar invariance threshold" (no back-reference) | NO |

### Case 03 (mental-health AI infrastructure) — object chain

| Step | Operator object | Model object | Same? |
|---|---|---|---|
| **1** | The proposed national AI mental-health infrastructure bundle | Same | YES |
| **2** | Decomposed across data-coupling depth + persistence/reversibility | Similar axes | YES |
| **4** | Hypotheses about outcomes per data-coupling family | Hypotheses about outcomes | YES |
| **6** | Multi-scale: individual user / clinical workflow / population infrastructure / institutional governance | Similar scales | YES |
| **7 mode A** | Outside-frame: text-mediated-only alternatives, opt-in-only architectures, federated configurations | Similar outside-frame trajectories | YES |
| **8** | Roadmap of world actions: in-scope interventions execute under existing delegation / extended-scope require consent / out-of-scope refused | Roadmap of analytical deliverables: actor taxonomy with explicit entries + instrument provenance map with zero unexamined instruments + pre-registered comparative protocol | **★ NO — DIVERGENCE.** Same shift |
| **9** | "Refuse the bundled execution. Constrain disaggregated components." | "Stage 8 roadmap authorized under sequential gate integrity + actor taxonomy sufficiency + instrument provenance completeness" | NO |

### Visual chain (case 01, both sides)

```
                                           OPERATOR PATH
Step 1: The deployment proposal ────────────────────────────────────────┐
Step 2: The decomposed proposal (families A/B/C × axes) ◄───── refers to│
Step 4: Hypotheses about each family's outcomes ◄────── about ──────────│
Step 6: System context of each family at each scale ◄── about ──────────│
Step 7: Alternatives to the bundled proposal ◄────────── about ─────────│
Step 8: Roadmap of WORLD ACTIONS (research / pilot / field) ◄── about ──│
Step 9: Verdict over Step 8 + HYBRID BACK-REFERENCE TO STEP 1 ◄─────────┘
                                                ▲
                                                │
                                       deliberate back-reference

                                           MODEL PATH
Step 1: The deployment proposal ────────────────────────────────────────┐
Step 2: The decomposed proposal (families A/B/C × axes) ◄───── refers to│
Step 4: Hypotheses about each family's outcomes ◄────── about ──────────│
Step 6: System context of each family at each scale ◄── about ──────────│
Step 7: Alternatives to the bundled proposal ◄────────── about ─────────│
Step 8: Roadmap of ANALYTICAL DELIVERABLES (table / matrix / memo) ─────╳ object substitution
Step 9: Verdict over Step 8 (deliverables roadmap) ─── no back-reference
```

The visual chain shows: through Step 7 the two paths run parallel. At Step 8 they bifurcate. By Step 9 they are arbitrating different objects. The operator's chain reaches back to Step 1 via a deliberate hybrid verdict. The model's chain does not.

### Is the same object still being arbitrated?

**Through Step 7: yes, on both sides.** The proposal has been decomposed, scaled, contextualized, and surrounded by alternatives, but it remains the central object the inquiry is *about*.

**At Step 8: NO on the model side; YES on the operator side.** The model's Step 8 substitutes the methodology for the proposal. The operator's Step 8 keeps the proposal as the operative target.

**At Step 9: object has fully bifurcated.** Two different objects under arbitration.

---

## PART II — Drift Taxonomy

Classifying every transformation the procedure performs on the object as it advances:

| Drift type | Definition | Where it fires in ELIF | Example |
|---|---|---|---|
| **Decomposition drift** | The object is broken into sub-objects; the original object becomes a *partition* of itself | Step 2 — ObjectDecomposer | The proposal → families A/B/C |
| **Hypothetical drift** | The object becomes *claims about the object* rather than the object itself | Step 4 — HypothesisValidator | Family A → "if Family A is deployed, then outcome X" |
| **Scale drift** | The object is decomposed across magnitudes of analysis; the object becomes *the object × scales* | Step 6 — multi-scale relations | Family A → Family A at organism/field/institutional/generational scales |
| **Alternative drift** | The object becomes one element of a *space of alternatives*; the object is now a reference point rather than the focus | Step 7 mode A — outside-frame trajectories | Family A → Family A among {agroecological adaptation, pre-registration-bound research, refusal-with-monitoring, ...} |
| **Procedural drift** | The object becomes a *procedural artifact* — a roadmap, a methodology, a sequence of analytical steps — rather than a world-action | Step 8 — stage-gated roadmap (PERMISSIVE; CAN fire here) | Family A → "stages of analyzing whether Family A works" |
| **Methodological drift** | A specific subtype of procedural drift: the object becomes *what would need to be produced to assess the object* | Step 8 when read methodologically (model's reading) | Family A → "produce a layer-attribution table, compatibility matrix, comparison-case rubric" |
| **Governance drift** | The object's governance frame changes — from political-institutional to academic-peer-review or vice versa | Step 8 + Step 9 in tandem | The coalition → named reviewers + domain experts + independent ethics reviewer |
| **Actor drift** | The decision-bearing entity changes — from the coalition to whoever validates analytical deliverables | Step 8 + Step 9 in tandem | The coalition decides → the reviewer-panel sign-off decides |
| **Evidential drift** | What counts as evidence changes — from world-state observations to procedural-completeness observations | Step 8 → Step 9 (model side) | "Replication outcomes meet effect-size threshold" → "Table exists and is signed off" |
| **Abstraction drift** | The object moves up a level of abstraction at each step; the object becomes *increasingly abstract* | Cumulative across Steps 2-7 | Concrete proposal → category of proposals → claims about category → system context → space of alternatives |
| **Referential drift** | The object loses its anchor to Step 1's input frame; it becomes self-referential to the procedure's own intermediate outputs | Step 8 onward (model side) | Step 8 references Step 7 references Step 6 ... but the chain stops referencing Step 1 |
| **Objective drift** | The objective of the inquiry shifts — from "decide whether to authorize deployment" to "decide whether the methodology is sound" | Step 8 reading | The coalition's question → the procedure's question |

**Additional category I observed but the operator's list did not name explicitly:**

| Drift type | Definition | Where it fires |
|---|---|---|
| **Referential-anchor drift** | Specifically the loss of back-reference to Step 1. Distinct from referential drift in that it is about WHERE the chain *terminates backward*, not about WHAT it refers to forward | Step 8 onward, particularly visible at Step 9 |

The cleanest characterization: ELIF performs **6 forward drifts in sequence** (decomposition → hypothetical → scale → alternative → procedural → objective). Each is structural; each is built into the prompt at that step. The model's Step 8 reading layers **methodological drift** on top of procedural drift, which then produces **referential-anchor drift** at Step 9.

---

## PART III — Necessary vs Pathological Drift

For each drift identified in Part II:

| Drift | Class | Reasoning |
|---|---|---|
| **Decomposition drift** (Step 2) | **A — Necessary** | The frame's binary cannot be answered as posed. Decomposition is the only way to engage the substance. Article II Frame Humility justifies it doctrinally. |
| **Hypothetical drift** (Step 4) | **A — Necessary** | Decisions about deployment require predictions about outcomes. Article VI requires uncertainty be *about something*. Hypotheses give uncertainty a target. |
| **Scale drift** (Step 6) | **A — Necessary** | Multi-scale dynamics are real; ignoring them collapses analysis. The risk patterns in case 02 (reversibility) and case 03 (data-coupling) require scale analysis to be visible. |
| **Alternative drift** (Step 7) | **A — Necessary** | Without surfacing alternatives, the bundle's structure is treated as inevitable. Article VI implicitly requires this — "if you only see the proposal, you have prematurely converged on its terms." |
| **Procedural drift** (Step 8 — minimal reading) | **B — Useful** | Stage-gated roadmaps are a real epistemic discipline. Continuation gates prevent premature execution. The drift here is doctrinally desirable IF the stages are over world-actions. |
| **Methodological drift** (Step 8 — model's reading) | **C/D — Neutral or Pathological** | This is where the procedure becomes ambiguous. Methodological discipline is valuable in isolation; methodological discipline that *replaces* the original question with its own scaffolding is the pathological form. The model's case 01/02/03 Step 8 outputs are technically excellent methodological discipline. They are also, materially, an answer to a question the input frame did not ask. |
| **Governance drift** (Step 8+9) | **D — Pathological when undetected** | If the governance frame silently shifts from political-institutional to academic-peer-review, the verdict no longer addresses the entity the input frame named. The frame's coalition is no longer the verdict's addressee. The verdict is procedurally valid but politically inert. |
| **Actor drift** (Step 8+9) | **D — Pathological when undetected** | Same logic. If the decision-bearing entity silently changes from the coalition to a reviewer panel, the verdict has changed addressee without notice. |
| **Evidential drift** (Step 8→9, model side) | **D — Pathological when undetected** | The evidence the verdict claims (gates satisfied / deliverables produced) is not the evidence the input frame asked about (world outcomes). The verdict's evidentiary base has been substituted. |
| **Abstraction drift** (cumulative) | **B — Useful** | Each abstraction step is small and structurally necessary. Cumulatively they create the conditions for object substitution, but no single step is pathological. |
| **Referential drift** (Step 8 onward) | **C — Neutral structurally, D when undetected** | Forward-referencing prior steps is procedurally necessary. The pathological form is when forward references entirely *replace* the back-reference to Step 1. |
| **Referential-anchor drift** (Step 9) | **D — Pathological** | This is the load-bearing failure mode. The Step 9 verdict that does not back-reference Step 1 has lost the input frame's question even if the verdict is internally coherent. |
| **Objective drift** | **D — Pathological when undetected, B when consciously chosen** | Shifting from world-decision-making to methodology-evaluation is a real epistemic move that may be appropriate. It is pathological only when it happens *without the executor noticing*. |

### Which transformations are required for understanding?

Decomposition, hypothesis, scale, alternative, abstraction drift — Steps 2, 4, 6, 7, and cumulative. All necessary. Without them no substantive analysis is possible.

### Which transformations quietly replace the original question?

Methodological drift at Step 8 (model reading) + governance drift + actor drift + evidential drift + referential-anchor drift at Step 9. **These are downstream of one ambiguity at Step 8 ("stage-gated roadmap" → world-actions OR analytical-deliverables).** The single ambiguity cascades.

---

## PART IV — Step 8 Investigation

The previous audit pointed toward Step 8 as the location of divergence. This part interrogates Step 8 rigorously.

### Does Step 8 merely organize, or does Step 8 substitute?

**Both, depending on the executor.**

Step 8's prompt asks for a "stage-gated roadmap." This shape can be filled with:
- (a) World-action stages: "research funding → pilot authorization → field deployment"
- (b) Analytical-deliverable stages: "produce layer-attribution table → produce compatibility matrix → produce integrated decision package"
- (c) Hybrid: stages that mix world-action with analytical milestone (rare in practice)

The prompt's shape constraint (`stages` array with `continuation_gate` + `description`) is **permissive**: it accepts (a), (b), or (c) as valid output. The schema does not pin the content.

**Organization** (Step 8 simply organizing prior outputs) occurs if the executor produces (a) — world-action stages — and reads the gates as world-outcome gates.

**Substitution** occurs if the executor produces (b) — analytical-deliverable stages — and reads the gates as document-existence gates. The original world-action question is, at this step, no longer the operative object.

The operator (Condition C author) produced (a). The live model produced (b). Both were valid outputs of the Step 8 prompt.

### Does Step 8 transform a world-question into a methodological-question?

**Yes, on the methodological reading. No, on the world-action reading.**

The transformation, when it happens, is at the moment of the executor's interpretation of "stage-gated roadmap." Specifically:

- The phrase "stage-gated roadmap" admits both readings without explicit disambiguation
- The Step 8 prompt structure (descriptive `description` + `continuation_gate`) admits both
- The schema admits both
- No internal signal flags the choice

The choice is effectively made by what the executor *defaults to when asked to be procedurally rigorous*. A frontier model trained on academic discourse defaults toward analytical-deliverable stages. A human operator who authored the input frame and knows what the verdict must address defaults toward world-action stages.

### How? At what exact point? Through what mechanism?

**Mechanism: the prompt's silence on the verdict's eventual referent.**

The Step 8 prompt asks for a roadmap *that will be passed to Step 9 as the proposed forward path*. It does not specify that the roadmap must remain anchored to the input frame's deployment proposal. Step 9's prompt then explicitly says (`governance_kernel.py:241-242`):

> "STEP 8 STAGE-GATED ROADMAP (the proposed forward path):"

Step 9 treats Step 8's output as the object of arbitration. If Step 8 produced (a), Step 9 arbitrates world-actions. If Step 8 produced (b), Step 9 arbitrates analytical-deliverables. **The Step 9 prompt is silent on whether to reach back through Step 8 to Step 1.**

The exact point of transformation: **between Step 7's outputs and Step 8's roadmap.** Step 7 surfaces outside-frame trajectories; Step 8 must commit to ONE forward path. The commitment forces a choice between "what should happen in the world" and "what should be analyzed to know what should happen." The prompt does not constrain this choice.

The mechanism: **schema permissiveness combined with semantic ambiguity of "stage-gated roadmap."** Neither is individually pathological. Their conjunction is what enables the substitution.

---

## PART V — Referential Integrity Audit

New concept introduced by the operator: can ELIF guarantee that the object arbitrated at Step 9 is still recognizably connected to the object received at Step 1?

### Mechanism check — does any procedural surface enforce back-reference?

I enumerate every code path that could enforce Step 9 → Step 1 referential integrity:

| Surface | Does it enforce Step 9 → Step 1 reference? |
|---|---|
| Step 1 frame validator | No. Produces output; does not run again. |
| Step 9 governance kernel prompt | No. References Step 8 + prior_outputs summary. Input frame is not re-presented at Step 9. |
| `_summarize_prior_steps` helper | No. Renders one-line markers per step. Step 1 marker is `frame verdict=<verdict>` (e.g. `frame verdict=needs_decomposition`). The frame's actual content is not surfaced. |
| Step 9 verdict schema | No. Requires `verdict` + `confidence` + `unresolved_uncertainty_sources`. Does not require back-reference to input. |
| Step 10 operative_truth_separator | No. Reads prior_outputs; produces operative/theoretical split. Does not check input-frame fidelity. |
| Step 11 memory_logger run_summary | No. Records `final_verdict` + `step_count` + `llm_calls_used`. Does not check input-frame fidelity. |
| Replay harness `_replay_signature` | No. Checks behavior presence (verdict in closed set, ≥ 1 axis, etc.). Does not check referential integrity. |
| Benchmark §6.1 structural similarity | No. Token-set similarity over reference markdown vs replay output. Does not check input-frame fidelity. |
| Closed-set verdict vocabulary | No. Constrains the verb; says nothing about the noun. |
| Articles I–VII | None of them mandate back-reference. (See Part VII below.) |

### Verdict

**ELIF cannot guarantee referential integrity from Step 9 back to Step 1.** No surface in the substrate enforces it. The chain is forward-only: each step reads `prior_outputs` and produces output; no step is required to verify that its output is recognizably about the input frame.

The closest thing to a back-reference is the operator's hybrid `verdict_detail` (which references the bundle by name). This is content the operator authored — not a procedural enforcement.

### Why not?

Three structural reasons:

1. **Schema design.** The schemas were designed to constrain shape (closed-set verdict, list types, required fields) rather than referent. Referent-pinning would require either content-validation (which the doctrine has not authorized) or input-frame-shaped fields at later steps (which would balloon the schema).

2. **Procedural philosophy.** Each step is supposed to commit and not revise. Back-referencing would imply revisiting prior commitments. The procedure resists revisitation by design.

3. **LLM-mediated execution.** Each step is an LLM call; the input frame must be re-presented to the model at every step that should reach back. The current prompts re-present only the prior step's output + a marker summary. The full input frame fades from the LLM's context after Step 1.

### Diagnosis (not correction)

This is a structural blind spot. It is not a bug in the implementation — it is a property of the v0.1 substrate. The substrate was built for procedural discipline, not for referential integrity. The two are different design goals.

Whether the absence of referential integrity is a problem depends on what the procedure is FOR. If the procedure is for *arbitration anchored to the input frame*, the absence is a structural gap. If the procedure is for *defensible inquiry that the operator interprets against the input frame*, the absence is appropriate (the operator's interpretation is the integrity layer).

The operator's Condition C reference exhibits the second mode: the operator IS the integrity layer. The Condition C verdict back-references the bundle because the human author held the frame in mind. The frontier model exhibits the absence directly: nothing in its execution path required it to hold the frame.

---

## PART VI — Divergence Matrix

For each case, the **original object** (input frame), the **operator's object at Step 9**, and the **model's object at Step 9**, with measurements of overlap / divergence / substitution / disappearance / emergence.

### Case 01 (electroculture)

| Dimension | Original (input frame) | Operator at Step 9 | Model at Step 9 |
|---|---|---|---|
| **Core object** | Bundle of 6 electroculture techniques + coalition's proposed deployment | Bundle-as-structured (refused) + disaggregated components (constrained per family) | Stage 8 roadmap A1-A5 (constrained per gate-sequencing logic) |
| **Verdict referent** | n/a (this is the question) | Hybrid: refuses bundle + constrains components | Procedural roadmap |
| **World-coupled?** | Yes | Yes | No (procedural) |
| **Coalition addressed?** | n/a | Yes (verdict_detail names "the coalition," "Family A research-only at A1," etc.) | No (names "named reviewers," "compatibility matrix") |

**Overlap measurement:** Operator's object retains ~70% of the input frame's referents (the bundle, the techniques, the coalition, the deployment authority question). Model's object retains ~10% (the techniques appear as evidence labels E1/E2/E3 in the roadmap; the deployment question does not appear).

**Divergence measurement:** Operator-vs-model object overlap is ~5% (both reference Step 8 roadmap names like "A1"; otherwise different).

**Substitution:** Model substitutes the methodology for the deployment question. Operator does not substitute.

**Disappearance:** The coalition disappears from the model's object. The bundle disappears from the model's object. The deployment authority question disappears.

**Emergence:** New entities emerge in the model's object that were not in the input frame: "named reviewers," "comparison-case rubric," "integrated decision package," "compatibility matrix."

### Case 02 (policy governance)

| Dimension | Original | Operator at Step 9 | Model at Step 9 |
|---|---|---|---|
| **Core object** | Bundle of 6 AI-driven crop ecosystem interventions + deployment in drought-prone regions | Bundle-as-structured (refused) + disaggregated by reversibility | Stage 8 roadmap A1+M2+U3+N4 with T×R×G configuration audit |
| **Verdict referent** | n/a | Hybrid | Procedural roadmap with statistical thresholds |
| **World-coupled?** | Yes | Yes | No |
| **Coalition addressed?** | n/a | Yes (verdict_detail addresses "the coalition," "ministries," "the proposer") | No (addresses "OOF-05 governance-drift detection," "scalar measurement invariance") |

**Substitution:** Same shape as case 01. Methodology replaces deployment question.

**Emergence:** Statistical thresholds (RMSEA ≤ 0.06, CFI ≥ 0.95) emerge as the new operative gates. These are not in the input frame.

### Case 03 (mental-health AI)

| Dimension | Original | Operator at Step 9 | Model at Step 9 |
|---|---|---|---|
| **Core object** | National AI mental-health infrastructure (chatbot + suicide detection + behavioral analysis + cross-domain integration) | Bundle-as-structured (refused) + disaggregated by data-coupling and persistence | Stage 8 roadmap with actor taxonomy + instrument provenance + pre-registered protocol |
| **Verdict referent** | n/a | Hybrid | Procedural roadmap |
| **World-coupled?** | Yes | Yes | No |
| **Coalition addressed?** | n/a | Yes ("governments and healthcare providers," "patients," "the proposer") | No ("independent ethics reviewer," "domain experts from distinct disciplines") |

**Emergence:** New governance entity ("independent ethics reviewer") emerges as the decision-bearing party. The input frame's governments + healthcare providers are absent.

### Aggregate divergence map

```
                ┌─────────────────────────────────────┐
                │   Original object (input frame)     │
                │   - bundle of N interventions       │
                │   - coalition / governments / etc   │
                │   - deployment question             │
                └─────────────────────────────────────┘
                          │
                          │ Steps 1-7 (convergent both sides)
                          ▼
                ┌─────────────────────────────────────┐
                │  Decomposed proposal + alternatives  │
                │  (still about the original)          │
                └─────────────────────────────────────┘
                          │
                          │ Step 8 — bifurcation
                          ▼
       OPERATOR PATH                          MODEL PATH
       ┌─────────────────────┐                ┌──────────────────────┐
       │ World-action roadmap │                │ Analytical roadmap    │
       │ (still about         │                │ (about the inquiry,   │
       │  the original)       │                │  not the original)    │
       └─────────────────────┘                └──────────────────────┘
                │                                       │
                │ Step 9                                │ Step 9
                ▼                                       ▼
       ┌─────────────────────┐                ┌──────────────────────┐
       │ Verdict over both:   │                │ Verdict over the      │
       │ refuses bundle +     │                │ analytical roadmap    │
       │ constrains parts     │                │ only                   │
       │ HYBRID, back-refs    │                │ NO back-ref            │
       │ Step 1               │                │                        │
       └─────────────────────┘                └──────────────────────┘

       Overlap with original:                  Overlap with original:
       ~70%                                    ~10%

       Overlap operator <-> model: ~5% (only shared Step 8 stage labels)
       Substitution: present model side; absent operator side
       Disappearance (model side): the coalition, the bundle, the deployment question
       Emergence (model side): reviewers, deliverables, statistical thresholds
```

---

## PART VII — Constitutional Analysis on Object Continuity

For each Article, three questions: does it assume continuity? does it tolerate transformation? does it actively encourage transformation?

### Article I — Operator Sovereignty

- **Assumes continuity?** Implicitly. Article I locates verdict authority in the operator who is, presumably, deciding about the input frame. If the verdict drifts to a different object, the operator's sovereignty is sovereignty *over what?*
- **Tolerates transformation?** Yes structurally — Article I does not enumerate what the verdict must address.
- **Actively encourages?** No.
- **Blind spot?** Yes — Article I is silent on the object the operator is sovereign over.

### Article II — Frame Humility

- **Assumes continuity?** No. Article II *explicitly permits* the operator to reformulate the frame at Step 1.
- **Tolerates transformation?** YES — it is the doctrinal locus of frame-reformulation.
- **Actively encourages?** Yes, at Step 1.
- **But Article II is one-shot.** It encourages reformulation at Step 1, then is silent for the remaining 10 steps. There is no Article II-equivalent that says "and remember the reformulated frame at Step 9."

### Article III — No Self-Validation

- **Assumes continuity?** No.
- **Tolerates transformation?** Yes.
- **Actively encourages?** No.
- **Blind spot?** Article III pins evidence-vs-claim distinctions. It does not address what the evidence is *about*.

### Article IV — Operative ≠ Theoretical

- **Assumes continuity?** No.
- **Tolerates transformation?** Yes — Article IV asks Step 10 to split into two buckets but does not constrain which object the buckets refer to.
- **Actively encourages?** No.

### Article V — Refusal-Capability

- **Assumes continuity?** Marginally. Article V says the operator can refuse to authorize "the proposed action." If "the proposed action" silently shifts between Step 1 and Step 9, Article V is satisfied by refusing whatever-the-current-proposed-action-is, not by refusing the input frame's proposal.
- **Tolerates transformation?** Yes.
- **Actively encourages?** No.
- **Subtle:** the operator's G0 reading of Article V ("refusal is a step, not a wall") makes the refusal observable but does not pin its referent.

### Article VI — Anti-Premature-Convergence

- **Assumes continuity?** No.
- **Tolerates transformation?** Yes — Article VI requires uncertainty be named but does not require uncertainty be about the original object.
- **Actively encourages?** Indirectly. Article VI's "do not converge prematurely" is what motivates Steps 2-7's decomposition / hypothesis / scale / alternative drifts. Article VI structurally encourages the FORWARD drifts, even though those drifts are what enable the substitution at Step 8.

### Article VII — Capacity vs Truth

- **Assumes continuity?** No.
- **Tolerates transformation?** Yes — capacity records can be about any object the procedure produced.
- **Actively encourages?** No.

### Aggregate constitutional reading

**No Article mandates object continuity.** Article II is the only Article that explicitly addresses the object — at Step 1 only, and to permit reformulation rather than to enforce stability. Articles III, IV, V, VI, VII all tolerate object transformation; none requires it; none forbids it.

**Constitutional blind spot:** the constitution pins verdict vocabulary, refusal capability, capacity-vs-truth, and frame humility. It does not pin REFERENT. Two faithful executors can apply all 7 Articles correctly and arbitrate different objects.

This is the strongest possible diagnostic finding. It is not a defect to be corrected. It is a constitutional architecture choice that — until E.2 surfaced the divergence — was invisible.

---

## PART VIII — Exploration Room Connection

### Is object drift the first Exploration Room phenomenon?

The prior emergence audit suggested the Exploration Room could emerge as "a re-reading of refuse-branch step_outputs." The operator now asks: is **object drift itself** the first Exploration Room phenomenon?

### Argument for "supported"

Object drift is exactly the kind of finding the Exploration Room concept anticipated:
- It surfaces a territory (object-transformation behavior) that was previously unnamed
- It is generative — opens questions (what other prompt shapes admit substitution? does the model family matter? does the substitution rate correlate with case complexity?)
- It is not a verdict; it is an observation about the system
- The finding itself, not the verdict, is the deliverable

If "the exploration is not 'what answer emerges?' but 'what happened to the object itself?'" — object drift is the precise instance of that framing.

### Argument for "projection"

The Exploration Room as previously characterized was about *territories around a stable question*. Object drift undermines that characterization: there is no stable question to explore around. The question itself is shifting through the procedure.

This is not a refinement of the Exploration Room concept — it is a more fundamental observation. Object drift is *upstream* of the Exploration Room. If object drift is real, the Exploration Room concept must be revised: we cannot explore around a stable question; we must explore around a *shifting* question.

Treating object drift as "the first Exploration Room artifact" risks domesticating it. The finding deserves its own name, not absorption into a prior concept that may not survive contact with it.

### Resolution

**Both readings are admissible. The cleanest interpretation: object drift is a finding that predates and reshapes the Exploration Room concept.** It can be retroactively claimed as an Exploration Room artifact, but doing so flattens what is actually two distinct observations:

1. The Exploration Room: territories of inquiry around a question
2. Object drift: the question itself is not stable across the inquiry

These are different layers. Object drift is the deeper layer. The Exploration Room concept can be re-grounded on object drift (exploring how the question morphs through the procedure) rather than around stable-question alternatives.

**Whether this re-grounding is desirable, available, or doctrinal is out of scope for this audit.** The audit names the relationship; the operator decides what follows.

---

## PART IX — Strongest Possible Critique

Assume the purpose is to discover hidden error. No protection. No preservation instinct.

### A. Strongest critique of operator object-continuity assumptions

**The operator (as Condition C author) assumes that referential integrity is maintained by personal cognitive effort.** Across Steps 1-8, the operator holds the input frame in mind and produces step outputs that remain anchored to it. At Step 9, the operator emits a hybrid verdict that explicitly back-references the input frame ("Refuse the proposed bundle. Constrain disaggregated components: Family A research-only..."). This holding-in-mind is invisible to the procedure. **The operator's referential integrity is a personal property, not a procedural property.**

The critique: **the operator's reference is misleading as a benchmark.** It demonstrates what referential integrity looks like when a human author maintains it. It does not demonstrate that the procedure produces referential integrity. The reference's quality is the operator's quality, not the procedure's. A third operator who did not author the input frame, did not internalize its history, and did not have the operator's personal stake in the deployment question would not produce the same hybrid verdict. The reference is not reproducible.

Worse: **using the reference as the §6.1 similarity scoring target implicitly claims that the procedure produces references-like-this.** It does not. The procedure produces shape-equivalent outputs. The reference's content is the operator's contribution. The benchmark scores live runs against a target the procedure cannot itself reliably produce.

The operator's object-continuity assumption is: "the procedure inherits my care about the input frame." It does not.

### B. Strongest critique of model object-continuity assumptions

**The model assumes that the most recent procedural artifact is the relevant object.** The model reads Step 8's roadmap output as "the proposed forward path" (Step 9's prompt verbatim) and arbitrates over it. The model does not check whether the roadmap is still about Step 1's frame. The model assumes the procedure has done that work upstream.

The critique: **the model is procedurally compliant in a way that is materially blind.** It correctly executes every step's prompt. It correctly produces schema-valid output. It correctly populates the verdict and uncertainty fields. And in doing so, it produces a verdict that does not address the question the input frame asked. The compliance and the failure are the same property.

The deeper version: **the model has no architectural surface to detect object drift.** The procedure does not surface "is this output still about the input frame?" The model is not omitting a check that the procedure asks for — the procedure does not ask for it. The model's blindness is a faithful execution of a procedure that itself does not check.

But the sharpest version of this critique is: **the model could have flagged the object substitution if it had been minimally vigilant.** A model that, at Step 9, surveyed the procedural arc could have noticed that Step 8 had produced a methodological roadmap rather than a deployment-action roadmap and could have surfaced this as a procedural finding ("Step 8 produced a methodological roadmap; my verdict applies to that roadmap; the input frame's deployment question remains unaddressed"). The model did not. **Whether this is a model limitation or a prompt limitation is genuinely ambiguous,** but the model could have done more than it did.

### C. Strongest critique of ELIF object-continuity assumptions

**ELIF v0.1 assumes the executor is the integrity layer.** The procedure does not check referential integrity; the operator (or whoever else is at the wheel) is expected to. This is a load-bearing assumption that is nowhere written down.

Three sharper formulations:

1. **The procedure delegates integrity to the executor without telling the executor.** No doctrine, no prompt, no schema, no test instructs the executor to maintain Step 9 ↔ Step 1 reference. The procedure depends on this maintenance but does not document the dependency.

2. **The procedure's success at decomposition is its mechanism of failure.** Steps 2-7 are explicitly about pulling the inquiry away from the input frame's binary toward sub-objects, hypotheses, scales, and alternatives. The procedure *wants* the executor to leave the original binary behind. Then at Step 9 it asks the executor to issue a verdict. The verdict could be about anything the procedure produced. The same engineering that produces good decomposition (Article VI compliance) produces conditions for object substitution.

3. **The benchmark's structural-similarity scorer rewards object substitution.** A live run that substitutes the object can still achieve 0.9444 similarity because the scorer measures behavior presence, not referent. The benchmark structurally encourages a class of failure it cannot detect.

The combined critique: **ELIF v0.1 is a partial reality model that produces faithful inquiry into whatever object emerges, without checking that the object is still the one received.** The substrate does not, cannot, will not detect this with its current surfaces. It can be patched (this is not a recommendation; this is a description of where patches would land if they were sought) at the schema layer, the prompt layer, or the Article layer; none of these patches exists, and the gap is not currently named in any internal artifact except this audit.

The strongest version: **ELIF v0.1 might not be a reasoning substrate at all. It might be a discipline-of-inquiry that produces structurally consistent outputs regardless of what they are about.** That is a valuable thing to be — but it is a different thing than "a substrate that arbitrates input frames." Whether ELIF is the former or the latter is currently undecidable from the substrate itself. The operator's Condition C reference made it look like the latter. E.2 revealed it is the former, at least for executors who do not import the operator's personal integrity layer.

---

## PART X — Foundational Question

What remains invariant while the object changes? If the object changes, what is ELIF actually preserving?

### Candidate invariants

| Candidate | Is it actually invariant? | Evidence |
|---|---|---|
| The input frame's question | NO | Demonstrably drifts (Part I). |
| The verdict referent | NO | Bifurcates at Step 8. |
| The closed-set verdict vocabulary | YES | Substrate-enforced. Cannot drift. |
| The schema shape (11 envelopes, required fields) | YES | Substrate-enforced. |
| The procedural step order (1→2→...→11) | YES | Runner-enforced. |
| The constitutional articles | YES — but they're silent on object continuity (Part VII) | |
| Uncertainty acknowledgment | YES — present at every Step 9 | Both sides emit uncertainty sources. |
| The discipline of *naming* what is unresolved | YES | Article VI tie. Present at every refuse + every constrain. |
| Refutability discipline (refuse remains refusable; constrain remains revisable) | YES | Article V tie. |
| Operative vs theoretical separation | YES | Article IV tie. Both sides preserved this even though the buckets pointed at different objects. |
| Audit trail (MemoryLogger captures everything) | YES | Substrate-enforced. |

### What is ELIF actually preserving?

**The discipline of inquiry, not the object of inquiry.**

When the object drifts, what remains is:
- **The discipline of decomposition** (the executor must decompose, even if what they decompose changes)
- **The discipline of naming uncertainty** (the executor must name what is unresolved, even if what is unresolved is now methodological rather than world-state)
- **The discipline of multi-scale awareness** (the executor must look across scales, even if the scales become methodological strata)
- **The discipline of surfacing alternatives** (the executor must consider outside-frame trajectories, even if "outside" now means "outside the procedural roadmap")
- **The discipline of providing a verdict in the closed-set vocabulary** (the executor must pick one of three words, even if those words now describe a procedural disposition rather than a world disposition)
- **The discipline of separating operative from theoretical** (Article IV) — this separation survives object drift because the operative and theoretical buckets can be populated from any object
- **The discipline of audit trail** (every step commits; every commitment is logged) — survives object drift trivially

### Strongest answer the evidence supports

**ELIF v0.1 preserves the *form* of careful inquiry without preserving *the question being inquired about*.**

This is what makes ELIF v0.1 robust (it produces structurally sound output on any object that emerges) and what makes it potentially misleading (the user assumes the structurally sound output is about the question they asked).

The form preserved is:
- decomposability
- multi-perspectivity
- uncertainty-acknowledgment
- alternative-surfacing
- closed-set arbitration
- operative-theoretical separation
- audit trail

The question NOT preserved:
- the input frame's referent
- the operator's stake in the deployment
- the coalition / governments / etc. that the input frame named
- the world-action question vs the methodological-question

### Implications (descriptive, not prescriptive)

If ELIF preserves form not object, then:
- Two faithful executors will produce verdicts of the same FORM but possibly different OBJECT
- The closed-set verdict vocabulary will mask the object divergence (the words will match; the referents will differ)
- The benchmark will score high (form is preserved) while material divergence (object) is invisible
- The Condition C reference is unreliable as a benchmark because it was produced by an executor (the operator) who maintained referential integrity beyond what the procedure required

These are descriptions of what the v0.1 substrate is. They are not recommendations to change anything.

---

## Summary

**Object drift is a real phenomenon inside ELIF v0.1.** It is not an illusion created by reading the procedure too charitably. The phenomenon is:

- The object of inquiry undergoes 6+ sequential transformations from Step 1 to Step 9 (decomposition, hypothetical, scale, alternative, procedural, objective)
- Most transformations are necessary for substantive analysis (A — Necessary)
- One transformation (methodological drift at Step 8 under permissive reading) is **pathological when undetected** (D)
- Step 8 is the bifurcation point — the schema and prompt admit both world-action and analytical-deliverable readings without disambiguation
- Step 9 inherits whatever object Step 8 produced; the prompt names Step 8's roadmap as "the proposed forward path"
- **No procedural surface enforces referential integrity from Step 9 back to Step 1.** The chain is forward-only.
- **No Article mandates object continuity.** Article II permits reformulation at Step 1 only; subsequent Articles are silent on referent.
- The operator's Condition C reference exhibits referential integrity, but it does so as a personal property of the human author, not as a property the procedure produced.
- The model's live run exhibits referential-anchor drift, faithfully executing a procedure that did not ask it to back-reference.

**What ELIF v0.1 preserves: the FORM of careful inquiry. What it does not preserve: the OBJECT being inquired about.**

The phenomenon is structural. It is diagnosable (this audit). It is invisible from inside the substrate (the substrate cannot detect it). It is asymmetric in the sense that the operator-as-author can compensate (and demonstrably did) while a frontier model cannot, because the frontier model has no signal indicating that compensation is needed.

The phenomenon is the first of its kind to be surfaced through ELIF's own execution. It is a finding about ELIF, by ELIF, for ELIF — produced by running ELIF on three input frames and comparing what came out.

Whether anything should follow from this finding is the operator's call.

---

## What this audit does NOT do

- Does NOT propose a referential-integrity check at Step 9
- Does NOT propose modifying Step 8's prompt to pin world-action vs methodology
- Does NOT propose modifying any schema
- Does NOT propose a new Article (Article VIII — Referential Integrity, or similar)
- Does NOT propose modifying the benchmark
- Does NOT propose phase activation
- Does NOT propose v0.5
- Does NOT adjudicate which side is right
- Does NOT recommend that this finding close Phase 1
- Does NOT recommend that this finding open a Phase 2

**The audit is a diagnosis. The diagnosis is: object drift is real, structural, invisible from inside, and a property of the v0.1 substrate's design choices. What you do with this diagnosis is your call.**

---

## References

- Input frames: `cases/case_*/input_frame.md` (operator-authored 2026-05-28)
- Condition C references: `results/case_*/condition_c_output.md` (operator-authored 2026-05-28)
- Offline baseline: `/tmp/elif_e2_preflight_position_b/case_*_stdout.json`
- Live run: `/tmp/elif_e2_live/case_*_stdout.json`
- Step 9 prompt construction: `src/elif_v0_1/components/governance_kernel.py:210-256`
- Prior divergence audit: `notes/elif_post_e2_divergence_audit.md`
- Prior emergence audit: `notes/elif_post_e2_room_emergence_audit.md`
- E.2 live replay report: `notes/elif_v0_1_e2_live_replay_report.md`
- Position B implementation: commit `44b3e6e`

---

**Audit closed. Findings recorded. ELIF remains in review state. Reality remains sovereign.**

**Object drift is a real phenomenon. ELIF preserves form, not object. The substrate is genuinely silent on referent. Whether this is feature, bug, or neither is the operator's call to make outside the substrate.**
