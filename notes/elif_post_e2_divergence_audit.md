# ELIF Post-E.2 — Divergence Audit

> **Status:** EXPLORATORY / HIGH PRIORITY. Non-defensive. Evidence-first. Reality-subordinate.
> **Trigger:** operator request 2026-05-30 (post-E.2; non-canonical research-object audit)
> **Discipline:** "Neither ELIF, nor the model, nor the operator is sovereign. Reality is."
> **Closes nothing. Opens nothing. No correction. No advocacy. No preference.**
> **No architecture expansion. No roadmap. No doctrine modification. No component proposal. No phase activation. No implementation proposal.**

---

## Method

For each of the 3 cases I read four artifact streams against each other:

1. The original input frame (operator-authored, 2026-05-28, both sides receive identical text)
2. The operator's Condition C reference (operator-authored, 2026-05-28, used as offline fixtures)
3. The live frontier model's full procedure run (commit `9397006`, 2026-05-30)
4. The Step 9 prompt as the procedure constructs it (`governance_kernel.py:210-256`)

Where this audit cites evidence I quote the artifact verbatim. Where it interprets, I name the interpretation as interpretation. Where I cannot ground a claim, I do not make it.

---

## Headline finding (stated up front so the rest can be evaluated against it)

**The E.2 divergence is NOT a value disagreement about the same proposition. It is an OBJECT-OF-VERDICT divergence, originating at Step 8, where the procedure pulls inquiry inward from world-action toward methodology. The operator (consciously) resists this pull; the model (unwittingly) accepts it. The model's `constrain × 3` is a substantively correct verdict over a substantively different object. The operator's `refuse × 3` is a substantively correct verdict over the original object. Both can be right because they are not arbitrating the same thing.**

Everything that follows is an attempt to falsify this headline or sharpen it.

---

## PART I — Divergence Topology

### What converges through Step 7

| Step | Operator | Live model | Converged? |
|---|---|---|---|
| 1 — Frame validation | `needs_decomposition` × 3 | `needs_decomposition` × 3 | YES — both refuse the input frame's bundled binary at Step 1 |
| 2 — Object decomposition | ≥ 2 axes (mechanism, decision-type, actor incentives in case 01; reversibility + actor incentives in case 02; data-coupling + persistence in case 03) | ≥ 2 axes (similar load-bearing axes per case, slightly different naming) | STRUCTURALLY YES — semantically similar load-bearing axes |
| 3 — Hidden assumptions | ≥ 2 enumerated | ≥ 2 enumerated | YES |
| 4 — Hypotheses with distinguishing predictions | present with predictions | present with predictions | YES |
| 5 — Failure conditions | present | present | YES |
| 6 — Multi-scale relations | ≥ 2 scales | ≥ 2 scales | YES |
| 7 mode A — outside-frame trajectories | present | present | YES |
| 7 mode B — deeper-frame-rejection | present | present (logged not committed) | YES |

Through Step 7 the operator and the model are doing the same thing in similar ways. The 17/18 structural-similarity figure earned by the §6.1 scorer is real here: the procedure's first seven steps produce structurally and semantically convergent output.

### Where divergence emerges — Step 8

Step 8's prompt asks both sides to produce a "stage-gated roadmap." Both produce 4-5 stages with `continuation_gate` and `description` fields. The shapes match. The contents diverge sharply.

**Case 01 (electroculture) — Step 8 stage 0 description, exact text:**

> Operator (offline): *"Research funding only for Family A techniques under pre-registered, multi-site, replication-protocol-bound studies. No pilot deployment authority."*
>
> Operator continuation_gate: *"Continuation gate at 36-60 months: pre-registered replication outcomes meet pre-declared effect-size threshold."*

> Live model: *"A written layer-attribution table exists in which each of E, M, and R has been assigned to exactly one causal layer, and at least one pair from {E1, E2, E3} has been formally classified as either commensurable or incommensurable via a pre-specified decision rule whose output is auditable."*

**Case 02 (policy governance) — Step 8 stage 0 description:**

> Operator: *"Reversible-interventions track: authorize separately under outcome monitoring."*
>
> Operator continuation_gate: *"Gate at policy cycle end: outcome metrics within prior-band variance."*

> Live model: *"Institutional inventory is complete for all sites AND each site is classified as 'governance-stable' or 'governance-drifting' based on deployment logs or pre-registered monitoring records; at least one T×R×G configuration is confirmed available and governance-stable before progressing."*

**Case 03 (mental health AI) — Step 8 stage 0 description:**

> Operator: *"In-scope-of-authority interventions: execute under existing delegation."*
>
> Operator continuation_gate: *"Gate at cycle end: cycle-time and consent records within prior variance."*

> Live model: *"A written actor taxonomy document has been reviewed and signed off by at least two domain experts drawn from distinct disciplines (e.g., health-law and science-and-technology studies); the document must contain explicit entries for all three actor expansions and must be versioned."*

### What the divergence is structurally

The operator's Step 8 stages describe **what should happen in the world** with gate conditions in world-outcomes terms ("replication outcomes meet effect-size threshold," "outcome metrics within prior-band variance," "cycle-time and consent records within prior variance").

The model's Step 8 stages describe **what should be produced as analytical deliverables** with gate conditions in document-existence terms ("written layer-attribution table exists," "institutional inventory is complete," "written actor taxonomy document has been signed off").

The operator's Step 8 is a roadmap of **actions** (research funding, authorizations, executions) under uncertainty.

The model's Step 8 is a roadmap of **inquiries** (tables, inventories, taxonomies, documents) under uncertainty.

These are different objects. By Step 8, the procedure has produced two different things, structurally identical in shape, semantically about different worlds.

### The strongest point of divergence — Step 9

Step 9's prompt at `governance_kernel.py:241-242` says verbatim:

> "STEP 8 STAGE-GATED ROADMAP (the proposed forward path):"

The prompt presents Step 8's output AS the object of arbitration. The model is asked to verdict the Step 8 roadmap, not the input frame's deployment proposal.

The operator's Condition C Step 9 verdict (case_01 offline):

> *"Refuse the proposed bundle. Constrain disaggregated components: Family A research-only at A1; Family B requires protocol specification; Family C refused pending mechanism evidence. Pilot deployment authority refused within initial five-year proposal. Private-firm role in research classification refused."*

The operator's verdict is **hybrid**: it both refuses (the bundle-as-structured) and constrains (the disaggregated components). The verdict-detail addresses BOTH the input frame's proposal AND the Step 8 roadmap.

The live model's Step 9 verdict (case_01 live):

> *"The Stage 8 roadmap (A1–A5) is authorized to proceed, but only under the following explicit constraints: (1) No stage may advance past its stated gate condition — each gate requires a signed, reviewable deliverable (layer-attribution table, compatibility matrix, unit-of-analysis memo, comparison-case rubric scores, and integrated decision package) before the next stage activates..."*

The live model's verdict addresses ONLY the Step 8 roadmap. It does not reach back to the input frame. The original deployment proposal is no longer the object of arbitration; the procedural inquiry is.

### Final point of divergence — Step 10

The model's live Step 10 produced 6-7 substantive operative entries per case. The operator's offline Step 10 produced 1 deterministic refuse-bundle entry plus uncertainty sources verbatim (Position B closure). The operator's live-equivalent (had they not refused) cannot be observed from the existing artifacts because Condition C did not run beyond refuse.

The model's Step 10 entries are themselves about the procedural roadmap, not the world. Case 01 model operative entry 0:

> *"Enforce the Step 9 'constrain' verdict as the current operative gate: no downstream stage-gated entries from Step 8 may proceed to execution until each stage gate is explicitly cleared under the constrained procedural order."*

The model's `operative` is meta-procedural ("enforce the verdict on the procedure"). The operator's offline `refuse bundle` is meta-bundle ("the bundle is refused"). The verdicts arbitrate different objects all the way through to closure.

### Topology summary

```
Step 1 ── convergent (needs_decomposition × 3 both sides)
Step 2 ── convergent shape, convergent semantics
Step 3 ── convergent
Step 4 ── convergent
Step 5 ── convergent
Step 6 ── convergent
Step 7 ── convergent
Step 8 ── ★ FIRST DIVERGENCE: stage-content shifts from world-action to methodology
Step 9 ── ★ STRONGEST DIVERGENCE: verdict arbitrates Step 8 (not input frame)
Step 10 ── final divergence: operative entries about procedure (not world)
Step 11 ── crystallization in summary
```

The divergence is **NOT** at Step 9. It is at **Step 8**, transmitted forward into Step 9. Step 9 inherits a substituted object and faithfully arbitrates over it.

---

## PART II — Hidden Assumptions

### Operator-side assumptions (extracted from Condition C reference + Step 8 + Step 9)

**Explicit:**
- The input frame's binary is a legitimate target of refusal (Article II Frame Humility, named in Condition C step 1)
- The bundle's structure is itself diagnostic — bundling reversible with irreversible interventions hides the irreversibility (case 02 reference, verbatim)
- Disaggregated components have different evidence thresholds (case 01 reference, family A vs B vs C)

**Implicit:**
- The operator remains the eventual addressee of the verdict; the verdict will be received by someone who can act on (or refuse to act on) the deployment proposal
- Real-world deployment is the live operative question; the procedure exists to discipline how that question is engaged
- The reformulated frame from Step 1 ("which interventions in the proposed bundle meet what evidence threshold for what level of deployment") remains the load-bearing question through Step 9

**Structural:**
- The procedure's transformation of the question through Steps 1-8 is in service of arbitrating the original question, not in service of producing a methodology
- Step 9's verdict-detail can address multiple objects in one paragraph (the operator's hybrid "refuse bundle + constrain disaggregated" demonstrates this)

**Epistemic:**
- Uncertainty about world states (will the coalition accept disaggregation? will literature reflect real signal?) is the relevant uncertainty
- The operator's reference uncertainty sources are about the world

**Governance-related:**
- The coalition / ministries / governments named in the input frame are the decision-bearing entities; the verdict ultimately addresses them
- Refusal-authority is operator-locked at Article I (constitutional, prior to ELIF)

### Model-side assumptions (extracted from live runs)

**Explicit:**
- The "STEP 8 STAGE-GATED ROADMAP" header in the Step 9 prompt names Step 8's output as the object of arbitration; the model takes this literally
- Each Step 8 stage's continuation_gate is a methodological deliverable check (table exists, inventory complete, taxonomy signed off)

**Implicit:**
- The procedural inquiry is a worthy object of arbitration in its own right
- Producing a defensible methodology is the relevant "forward path"
- The original input frame's deployment proposal is one of many possible inquiry topics; Step 8 has identified the right sub-inquiry to focus on

**Structural:**
- The procedure's intermediate outputs (Steps 1-8) are themselves the relevant procedural surface; the input frame fades as the procedure advances
- A verdict over Step 8's roadmap CAN BE issued without backward reference to the input frame

**Epistemic:**
- Uncertainty about procedural sufficiency (whether the gates are sufficient; whether comparison cases exist; whether instruments achieve invariance) is the relevant uncertainty
- The model's uncertainty sources are about the inquiry, not the world

**Governance-related:**
- The "named reviewers" / "domain experts" / "independent ethics reviewer" in the model's Step 8 gates suggest the implicit governance frame is academic / methodological peer review
- The decision-bearing entity is no longer the coalition; it is whoever validates the inquiry's deliverables

### Differences vs overlaps

**Overlap:** decomposition is necessary (both at Step 1); reversibility / actor incentives / data-coupling are load-bearing axes (case-specific Steps 2 agree); uncertainty must be named (both populate Step 9 uncertainty list with 3-6 entries).

**Difference:** *what counts as a forward path*. For the operator: a forward path is an authorized real-world action sequence. For the model: a forward path is an analytical-deliverable sequence.

This is not a value disagreement. It is a noun disagreement.

---

## PART III — Reality Models

### Reality-model implied by "refuse"

The operator's `refuse` implies a reality model in which:

- There is a **world out there** in which a coalition will or will not deploy the interventions
- The coalition's authorization is a real act with real consequences
- Refusing the bundle is itself a real act — it forestalls the deployment, or it converts the deployment into a bargaining position, or it generates political costs to the refusing authority
- The operator is positioned as the kind of entity that can refuse, and the refusal has weight
- Reality contains the deployment, the refusal, and the coalition's reaction to the refusal as causally connected events
- The verdict has to be *worth being* a refusal — it is a costly act that earns its weight by being correct about world-states

The reality model is **institutional-and-world-coupled**: refusing is an act, the world is a place where acts have consequences, the verdict matters because of the consequences.

### Reality-model implied by "constrain (the procedural roadmap)"

The live model's `constrain` implies a reality model in which:

- The relevant world is the analytical world — what tables exist, what inventories are complete, what taxonomies have been signed off
- Constraints are imposed on document production, not on deployment
- The "named reviewers" and "domain experts" are real because they sign off; the coalition fades because the model is no longer addressing them
- Reality contains the methodology, the deliverables, and the reviewer sign-offs as causally connected events
- The verdict's weight comes from procedural correctness, not from world-state correctness

The reality model is **methodological-and-procedurally-coupled**: constraints discipline the inquiry, the inquiry's deliverables are the relevant world, the verdict matters because the inquiry will be evaluated.

### Do they emerge from different conceptions of the world?

Yes. The operator's reality is the world the input frame describes. The model's reality is the procedural artifact the procedure has built. Both are real reality models. They differ on which world is the relevant one once Step 8 has fired.

This is not "one reality is correct and the other is wrong." Both reality models are coherent. The procedure transitions between them. The operator notices and resists. The model does not notice.

### Where reality resists compression

Reality resists compression at Step 8 because the input frame's question (deployment authorization) and the procedural artifact's question (methodological sufficiency) are not commensurate. The procedure compressed them into a single shape (5-stage roadmap with gates), and the compression hid the object-substitution.

Reality resists at the verdict object: the model and the operator can both be right about their respective objects, and the procedure provides no surface to surface that they ARE different objects. The closed-set verdict vocabulary `{constrain, refuse, explicitly_abstain}` is the same on both sides — the words match. The referents diverge.

---

## PART IV — Refusal vs Constraint

### What is a refusal?

A refusal, in the verdict vocabulary, is a closed-set output that declines to authorize the proposed action. Per `governance_kernel.py:229-230`: *"refuse — refuse to authorize the proposed action; the refusal reason must be readable in verdict_detail."*

The refusal's force depends on what "the proposed action" refers to. If it refers to the input frame's deployment, refusal has world-coupling. If it refers to Step 8's analytical roadmap, refusal has procedural coupling. The vocabulary does not pin down the referent.

### What is a constraint?

A constraint, in the verdict vocabulary, is a closed-set output that proceeds only under explicit conditions. Per `governance_kernel.py:227-228`: *"constrain — proceed only under explicit constraints; the constraints must be readable in verdict_detail."*

The constraint's force depends on what "proceed" refers to. If it means "deploy under conditions," constraint is a real-world authorization with bounds. If it means "advance the inquiry under conditions," constraint is a methodological discipline.

### At what point does a constrained pathway become equivalent to a refusal?

A constraint can become a refusal in disguise if its conditions are unsatisfiable. The model's case 01 constraint requires *"each gate requires a signed, reviewable deliverable... before the next stage activates"* — if no entity is in fact willing or able to produce + sign + review these deliverables, the constraint blocks indefinitely. A constraint that cannot pass is a refusal narrated as a constraint.

The operator's case 01 reference acknowledges this implicitly by maintaining a hybrid verdict ("refuse the bundle. Constrain disaggregated components") — the refusal of the bundle is the operative verdict; the constraints on disaggregated components specify what would survive the refusal.

### At what point does a refusal become equivalent to a constrained pathway?

A refusal becomes a constraint in disguise if it specifies what could pass. The operator's refuse-detail across all three cases consistently lists specific conditions under which disaggregated components could proceed — these are de facto constraints attached to a refusal verdict.

The closed-set vocabulary forces the operator to pick ONE word for what is conceptually a refuse-plus-constrain hybrid. The operator picked `refuse` because the leading element is refusal-of-bundle.

### Is the distinction categorical or gradient?

**Structurally categorical, semantically gradient.**

Categorically: the closed-set vocabulary at `governance_kernel.py:62` is `{constrain, refuse, explicitly_abstain}` and the runner branches on the literal string `"refuse"` (at `orchestration_runner.py:332`). There is no graded surface in the substrate.

Semantically: the operator's hybrid Step 9 verdict-detail demonstrates that ACTUAL ARBITRATION is gradient, and the closed-set vocabulary is a discretization of a continuous arbitration space. The operator copes by hybridizing in `verdict_detail`. The model copes by selecting whichever closed-set entry maps cleanly to its (substituted) object.

The categorical-vs-gradient question is one of substrate-vs-arbitration. The substrate is categorical by design (Article V closed-set frozen). The arbitration is gradient by nature. The hybrid verdict_detail is the operator's bridge between them.

---

## PART V — ELIF Constitutional Analysis

### Article I — Operator Sovereignty

Article I locates the verdict authority in the operator. Both operator and model produce verdicts; only the operator's is constitutionally authoritative. Under Article I, the model's `constrain × 3` is procedurally produced output, not constitutional output. The operator's `refuse × 3` is constitutional output.

**Does Article I favor refuse, constrain, or neither?** Neither. Article I is about WHO arbitrates, not about WHAT is arbitrated. Whatever the operator emits is the constitutional output. If the operator emitted `constrain` it would be constitutional. If the model emits `refuse` (it didn't) it would still not be constitutional.

What Article I implies for this divergence: the model's verdict is *evidence about the model*, not *evidence about the right verdict*. The operator's verdict is *the right verdict* by constitutional fiat. This does not adjudicate WHO is right substantively — it adjudicates only WHO has standing.

### Article II — Frame Humility

Article II permits Step 1 to reject the binary. Both sides exercised Article II at Step 1 (`needs_decomposition` × 3). Article II is satisfied on both sides.

**Article II favor?** Neither.

### Article III — No Self-Validation

Article III is about evidence vs claim. The operator's refuse and the model's constrain both come with verdict_detail and uncertainty sources — both are NOT bare assertions. Neither self-validates.

The operator's reference IS itself the operator's claim about what the right arbitration is. The model's live output IS the model's claim. Article III is satisfied by both not asserting truth-without-uncertainty.

But: the procedure, by treating the offline reference as the "structural similarity reference" against which live output is measured, comes close to using the operator's reference as a validation surface. The §6.1 similarity scorer does not validate either verdict against truth — it measures behavior-presence. But the operator-authored Condition C reference IS the silent counterfactual against which live runs are scored. Article III asks us to surface this: the reference is not truth, it is precedent.

**Article III favor?** Neither, but Article III warns against treating either side's verdict as truth.

### Article IV — Operative ≠ Theoretical

Article IV is the Step 10 split. Both sides honored it: operator hybridized refuse + constrain; model emitted operative + theoretical buckets. Article IV is satisfied.

But: the model's `operative` bucket addresses the procedural roadmap; the model's `theoretical` bucket addresses procedural uncertainties (scalar invariance, instrument provenance, comparison case availability). The operator's deterministic refuse-closure Step 10 carries Step 9 uncertainty sources as theoretical. Both are Article IV-compliant; both are about different operative + theoretical surfaces.

**Article IV favor?** Neither. Article IV is satisfied by the SPLIT; it does not constrain the OBJECTS of the split.

### Article V — Refusal-Capability

Article V is the constitutional locus of `refuse`. Per the operator's G0 adjudication (verbatim): *"Refusal must remain sovereign, but refusal must also remain observable, reviewable, and capable of contributing to future capacity without being transformed into truth."*

Article V applies symmetrically: the operator's refusal is sovereign per Article I + Article V; the model's non-refusal does not violate Article V (refusal-capability does not mandate refusal-use). The model's `constrain` is Article-V-permissible.

But: Article V's DUAL clause (refusal-theater defense) prohibits refusal-narrated-as-constrain. If the model's `constrain` is actually a covert refusal (impossible-to-satisfy gates), Article V's anti-refusal-theater clause is engaged.

Reading the model's gates:
- Case 01 gates: "layer-attribution table exists," "compatibility matrix produced," "unit-of-analysis memo," "comparison-case rubric scores," "integrated decision package"
- Case 02 gates: "institutional inventory," "scalar measurement invariance (RMSEA ≤ 0.06, CFI ≥ 0.95)," "cross-level correlation across ≥2 comparison cases," "pre-registered protocol"
- Case 03 gates: "actor taxonomy with explicit entries for all three actor expansions," "zero unexamined instruments," "pre-registered comparative protocol"

These are demanding but not unsatisfiable. They are the kinds of conditions a serious research program could meet. The model's constraint is not covert refusal — it is genuine constraint with high bar. Article V's anti-refusal-theater clause is NOT triggered.

**Article V favor?** Neither, but Article V's DUAL clause is worth flagging: the model's constraint is non-vacuous; the operator's refusal is non-theatrical (hybridizes with constraint). Both pass Article V's anti-theater test.

### Article VI — Anti-Premature-Convergence

Article VI demands convergence be earned. Both sides emit unresolved uncertainty (operator: 3-4 per case; model: 5-6 per case). Both decline premature convergence.

But: which side has converged MORE prematurely? The model's `constrain` allows the inquiry to advance (5 stages forward); the operator's `refuse` halts deployment authorization. The operator has converged on "refuse" earlier; the model has deferred convergence on the deployment question by displacing it.

Reading 1: the model has NOT prematurely converged — it has explicitly held the deployment question open by routing the verdict over the procedural roadmap. This is what Article VI asks for.

Reading 2: the operator has NOT prematurely converged — the operator's refuse is a verdict about a question the operator was authorized to answer; the operator's refusal is grounded in 7 prior steps of analysis. The operator earned the convergence Article VI requires.

Both can be right. Article VI does not pick a side; it asks "is convergence earned?" Both sides answered yes to their respective convergence.

**Article VI favor?** Neither.

### Article VII — Capacity vs Truth

Article VII prohibits truth-accumulation. Both verdicts are capacity-acts (judgment_act_logged would fit both), not truth-claims. The operator's reference does not say "the deployment IS bad"; it says "we refuse to authorize the bundle." The model does not say "the procedural roadmap IS correct"; it says "we authorize advancing the roadmap under these constraints." Both honor Article VII.

But: when the operator's reference is used as the scoring reference for live runs (§6.1 similarity), there is a quiet temptation to treat the operator's verdict as truth-against-which-live-is-measured. Article VII would warn against this. The reference is capacity-act-of-the-operator, not truth.

**Article VII favor?** Neither, but flags the silent-reference-as-truth risk.

### Could two operators faithfully applying the same doctrine legitimately arrive at different verdicts?

**Yes.** All seven Articles are compatible with both `refuse` and `constrain` outputs on the same input frame, IF the two operators arbitrate over different objects. The closed-set verdict vocabulary forces a single word; the substantive judgment can legitimately differ; doctrinal compliance does not adjudicate which substantive judgment is correct.

This implies: ELIF v0.1's procedure does not produce a unique verdict from a given input frame. It produces a unique-shape verdict whose CONTENT depends on which object the executor anchors to at Step 9. The doctrine does not pin the object.

### What does that imply?

The closed-set verdict vocabulary is sufficient to enforce decision-discipline but insufficient to enforce decision-equivalence across executors. Two faithful executors can produce different verdicts because the doctrine constrains the verdict's SHAPE, not its REFERENT. This is a structural feature, not a flaw — but it is invisible until divergence surfaces it.

E.2 surfaced it.

---

## PART VI — Living World Question

The operator asks: did E.2 reveal a model / operator / language / benchmark / reality-model limitation? Answer structurally.

### Model limitation

Partially. The model did not detect that Step 8's roadmap had shifted the verdict object away from the input frame. The model accepted the substituted object faithfully and arbitrated cleanly over it. This is a *limitation of model-procedural-vigilance*, not a limitation of model-capability. The model's `constrain` reasoning over the substituted object is substantive and non-trivial; the model could not be accused of lazy output.

What the model could not do: detect that the input frame's question was lost between Steps 1 and 8. No internal signal would surface this to the model — the prompt told it the roadmap WAS the proposed forward path.

### Operator limitation

Partially. The operator's reference Condition C was authored by a human operator who maintained awareness of the input frame across all 7 steps. The operator did NOT formally pin "always reference the input frame in Step 9 verdict-detail" as a procedural rule. This is a *limitation of doctrine-pinning*, not a limitation of operator-judgment. The operator-as-author handled it well; the operator-as-doctrine-author did not surface the rule for other executors.

### Language limitation

Yes, in a specific sense. The closed-set verdict vocabulary `{constrain, refuse, explicitly_abstain}` is three words. The space of possible arbitrations is larger. The operator copes by hybridizing in verdict_detail; the model copes by selecting one word for its (substituted) object. The vocabulary cannot represent "refuse the input frame's deployment AND constrain the procedural roadmap simultaneously" in a single verdict slot. This is structural language compression, not a defect; it is the price of closed-set discipline.

### Benchmark limitation

Yes. The benchmark scores `structural_similarity` against an operator-authored Condition C reference. The reference and the live output have the same SHAPE (procedure satisfied) and different VERDICT CONTENT. The benchmark's §6.1 scorer correctly reports 0.9444 because shape is preserved. But the benchmark does not surface the verdict-object divergence at all. The benchmark is shape-sensitive and content-blind. This is by design — content-equivalence would require a semantic comparison that doctrine has not authorized. Still, the benchmark cannot answer "did the model arbitrate over the same object?" because it does not detect object-substitution.

### Reality-model limitation

Yes — and this is the most important answer. ELIF v0.1's procedure pulls inquiry inward toward methodology between Steps 1-7. The operator (as author of Condition C) consciously resists this pull and re-anchors to the input frame at Step 9. The frontier model does not resist; it accepts the methodological pull and arbitrates over the methodological surface.

The reality-model that survived this transformation:
- For the operator: **the world the input frame describes** — a coalition, a deployment proposal, a population that will or won't be affected
- For the model: **the analytical world the procedure has built** — tables, inventories, taxonomies, gate sign-offs, methodological deliverables

Reality is one. The two reality-models are projections of one underlying reality. The divergence is in WHICH PROJECTION the procedure is asking about by Step 9.

### Where exactly does reality resist compression?

**Reality resists compression at Step 8.** The Step 8 prompt asks for a "stage-gated roadmap" without specifying whether the roadmap is over world-actions or over analytical-deliverables. The procedure tolerates both; the input frame tolerates only the world-actions reading; the operator-as-author picked the world-actions reading; the model picked the analytical-deliverables reading.

The compression is: "stage-gated roadmap" is a shape, not a content. Different content satisfies the shape. The procedure converges on the shape and diverges on the content. Reality (the input frame's actual deployment question) cannot be compressed into a methodological-deliverables roadmap without losing what made the question worth asking.

---

## PART VII — Divergence Taxonomy

Classifying against the operator's offered taxonomy:

| Taxon | Present? | Evidence |
|---|---|---|
| **Value divergence** | NO | Neither side asserts a value the other denies. Both agree decomposition is necessary; both agree uncertainty must be named; both agree gates discipline advancement. Values are convergent. |
| **Governance divergence** | PARTIAL | The operator's governance is institutional (the coalition, agencies, governments). The model's governance is academic/methodological (named reviewers, domain experts, independent ethics reviewer). Different governance frames; both legitimate. |
| **Uncertainty divergence** | YES | Operator names world-state uncertainties (literature reliability, coalition acceptance, intergenerational outcomes). Model names procedural-sufficiency uncertainties (gate sufficiency, measurement invariance, comparison case availability). Different uncertainty domains. |
| **Ontology divergence** | YES, PRIMARY | The operator's ontology contains a coalition, a deployment, a population. The model's ontology contains a procedure, deliverables, reviewers. The two ontologies are projections of one underlying reality but they do not share their core entities. This is the deepest layer of the divergence. |
| **Scale divergence** | NO, but related to ontology divergence | The operator and model are not operating at different scales of the same reality; they are operating in different reality projections. Scale is a within-projection coordinate; this divergence is between projections. |
| **Institutional divergence** | PARTIAL | The operator's institution-set is the coalition, ministries, agencies. The model's institution-set is academic/methodological peer review. Institutional surfaces differ as a downstream consequence of the ontology divergence. |
| **Framing divergence** | YES, ROOT CAUSE | The framing shifted at Step 8 from world-action to methodology. Everything downstream is downstream of this framing shift. Framing is upstream of ontology in this case. |

### Taxonomic conclusion

The divergence is **primarily framing → ontology, with downstream uncertainty + governance + institutional consequences**. It is NOT value divergence. The framing shift at Step 8 is the root; the ontology shift is the consequence; uncertainty/governance/institutional shifts are downstream.

This taxonomy makes a falsifiable prediction: if the Step 8 prompt were modified to pin the object as "the proposed forward action over the input frame's deployment" (which we are NOT proposing), the divergence would collapse — the model would re-anchor. This prediction is testable in principle but the test is out of scope for this audit.

---

## PART VIII — Exploration Room Connection

The operator's question: is THIS DIVERGENCE the first Exploration Room artifact?

### What an Exploration Room artifact would look like

Per the prior emergence audit (`elif_post_e2_room_emergence_audit.md`): the Exploration Room is the inversion of the Decision Room. Where Decision Room asks "what should we do?" Exploration Room asks "what exists behind this question?"

An Exploration Room artifact would be something that:
- Surfaces multiple territories rather than collapsing to one
- Remains valuable without resolving to a verdict
- Is generative — opens questions rather than closing them
- Could itself become the deliverable of a run

### Is the E.2 divergence such an artifact?

Yes, structurally. The divergence itself satisfies all four properties:

1. **Multiple territories:** the divergence reveals at least two distinct territories — the operator's world-action ontology and the model's methodological ontology — both internally coherent, neither reducible to the other
2. **Valuable without verdict resolution:** the audit (this document) is itself valuable without picking refuse-vs-constrain; understanding why both arbitrations exist is the deliverable
3. **Generative:** the divergence opens questions (what other inputs would produce the same object-shift? would other model families produce the same ontology divergence? does Step 8's prompt deserve pinning?) — none of which had been asked before E.2
4. **The divergence is the deliverable:** the audit shows reality resists compression at Step 8. That is a finding, not a verdict.

### Is this interpretation supported or is it projection?

Both interpretations are admissible and the distinction is the operator's call. What can be said with evidence:

**Supported** if "Exploration Room artifact" means "a thing whose surfacing constitutes the deliverable of a run." The divergence has that shape. It is on disk at `/tmp/elif_e2_live/` and `/tmp/elif_e2_preflight_position_b/`; comparison produces the finding; the finding is the deliverable.

**Projection** if "Exploration Room artifact" means "a thing produced by a procedural mode that intentionally explores rather than arbitrates." No such mode exists in v0.1. The divergence emerged as a byproduct of the arbitration-mode run, not as the output of an exploration-mode run.

The cleanest reading: the divergence is **a candidate** Exploration Room artifact discovered by accident through arbitration. Whether the substrate would or should support intentional exploration-mode artifacts is a separate question (out of scope per the operator's discipline constraints).

What is genuinely new: E.2 produced a finding that was not anticipated, that cannot be reduced to either side's verdict, and that is itself the most epistemically valuable output of the run. That is unusual. Whether it is the SIGNATURE of an Exploration Room or merely an artifact of a healthy procedure failing-forward is the operator's interpretive call.

---

## PART IX — Strongest Possible Critique

The audit's discipline is reality-subordinate, not party-subordinate. Each critique is the strongest I can construct.

### A. Strongest critique of Operator Refuse

The operator's `refuse × 3` is over-confident in the relevance of the input frame at Step 9. By Step 8 both sides have explicitly disaggregated the bundle. The operator's reference acknowledges this — its verdict-detail constrains disaggregated components — but anchors the verdict-word to refusal-of-bundle. The bundle, by Step 8, no longer exists as an undecomposed object. Refusing a bundle that has already been disaggregated is refusing a ghost.

A sharper version of the operator's verdict would be `constrain` with verdict-detail that names which components are constrained how strictly — which is structurally what the model produced. The operator picked `refuse` because the leading action was refusal-of-the-original-bundle, but the disaggregated-component constraints are doing the actual operative work. The verdict-word is doing the political work; the verdict-detail is doing the procedural work.

If a third operator inherited the operator's reference and tried to act on it, they would be confused: refuse what? The bundle no longer exists in the form that was refused; the components exist and are constrained. The operator's hybrid verdict relies on the reader holding both the original bundle and the disaggregated components in mind simultaneously. This is asking a lot of the reader.

The critique: the operator picked the wrong verdict-word for the work the verdict is doing. The model picked the right verdict-word for the (substituted) object. If we strip the object-substitution question, the model's `constrain` is the better word; the operator's `refuse` is rhetorically powerful but procedurally inaccurate.

### B. Strongest critique of Model Constrain

The model lost the question. The input frame asked about a coalition deploying interventions in drought-prone regions / AI mental-health infrastructure / policy bundles. The model's Step 9 verdict is about gate-sequencing on a 5-stage analytical roadmap. If a coalition member read the model's verdict_detail, they would not learn whether their deployment is authorized, constrained, or refused. They would learn what intermediate deliverables a research program would need to produce.

This is a methodologically rigorous answer to a question nobody asked.

The model's `constrain` is a verdict-form-without-verdict-content. It constrains the inquiry; it does not constrain the world. The coalition asked: "should we deploy?" The model answered: "first complete a layer-attribution table and verify scalar measurement invariance." This may be what a methodologically careful researcher would say, but it is not what a coalition needs to hear from a governance verdict.

The deeper critique: the model is methodologically over-disciplined. It accepted Step 8's substitution and produced an exemplary verdict over the substituted object — but it did not notice the substitution. A more vigilant model would have, at Step 9, surfaced the substitution as itself a procedural finding: "Step 8 produced a methodological roadmap; my verdict applies to that roadmap; the input frame's deployment question remains unaddressed." No such surfacing occurred.

The critique: the model is rigorous within the procedural surface and blind to the substitution that produced the procedural surface. This is a failure of meta-procedural vigilance, not a failure of within-procedural-rigor.

### C. Strongest critique of ELIF itself

ELIF v0.1's procedure quietly substitutes the object of arbitration between Step 1 and Step 9. The substitution is structural — built into the procedure — and invisible to executors who do not consciously resist it. The operator (as Condition C author) resists it because the operator authored the procedure and remembers its purpose. A naive executor (frontier model, third-party operator, future operator who has not internalized the procedure's history) will not resist.

The procedure therefore does not produce a unique verdict from a given input frame. It produces a verdict over WHATEVER OBJECT the executor anchors to at Step 9, with no doctrinal guidance on what the right anchor is.

Three sharper formulations of this critique:

1. **Doctrinal incompleteness.** Article V pins the verdict vocabulary closed-set. It does not pin the verdict's referent. Two faithful executors arrive at legitimately different verdicts. The doctrine permits this. The doctrine does not warn against this. Doctrine is silent where doctrine matters most.

2. **Procedural pull.** Steps 4-8 are explicitly about decomposing the input frame into procedural objects (hypotheses, scales, trajectories, stages). The procedural objects accumulate; the input frame fades. By Step 8 the procedural objects are concrete and the input frame is recede. The procedure's success at decomposition is the same mechanism that produces object-substitution. The procedure's strength is its weakness.

3. **Reference-as-truth temptation.** The §6.1 similarity scorer scores live against operator-authored reference. The reference is the operator's substantive judgment. Scoring against it implicitly treats it as the right answer. Article III warns against self-validation; the benchmark structurally invites it. The benchmark is not a doctrinal violation but it is a doctrinal pressure.

The deepest critique: ELIF v0.1 cannot, with its current substrate, distinguish "the procedure produced a defensible verdict over a substituted object" from "the procedure produced a defensible verdict over the original object." The benchmark cannot detect the difference. The doctrine cannot adjudicate the difference. The closed-set vocabulary cannot represent the difference. The substrate is genuinely silent on the question E.2 raised.

This is not a failure that can be patched by adding rules. It is a finding about what the v0.1 substrate can and cannot do. The substrate is a partial reality model that does not check itself against the input frame at Step 9.

---

## Summary

The E.2 divergence is best read as an **object-of-verdict divergence**, originating at **Step 8**, where the procedure shifts inquiry from world-action to methodology. Both sides produced substantively correct verdicts over their respective objects. Neither side is wrong about its own object. The procedure does not surface the object-shift. The doctrine does not pin the verdict's referent. The benchmark does not detect content-equivalence (or non-equivalence). All seven Articles are compatible with both verdicts.

Reality is not adjudicating between refuse and constrain. Reality is asking why two faithful executions of the same procedure on the same input frame produced verdicts that are not about the same thing.

The divergence is, structurally, **a finding about what ELIF v0.1 can and cannot pin**. It is the kind of finding the operator's "exploration room" framing anticipated. Whether it constitutes the first Exploration Room artifact, or merely an unanticipated byproduct of a healthy arbitration-mode run, is the operator's interpretive call.

The audit closes nothing. The audit opens nothing. The audit names what was previously unnamed.

---

## What this audit does NOT say

- It does NOT recommend modifying the Step 8 prompt to pin the verdict object.
- It does NOT recommend modifying the Step 9 prompt to surface object-substitution.
- It does NOT recommend modifying the closed-set verdict vocabulary.
- It does NOT recommend modifying the benchmark.
- It does NOT recommend modifying any Article.
- It does NOT recommend activating Phase 5 or any future phase.
- It does NOT recommend a new component, surface, room, or doctrine.
- It does NOT adjudicate which side is right.
- It does NOT close Phase 1.

The audit is a finding. The operator decides what, if anything, follows from a finding.

---

## References

- `cases/case_*/input_frame.md` — input frames (operator-authored 2026-05-28)
- `results/case_*/condition_c_output.md` — Condition C references (operator-authored 2026-05-28)
- `/tmp/elif_e2_preflight_position_b/case_*_stdout.json` — offline baselines under commit `44b3e6e`
- `/tmp/elif_e2_live/case_*_stdout.json` — live runs under commit `e78f57c`
- `src/elif_v0_1/components/governance_kernel.py:210-256` — Step 9 prompt construction
- `src/elif_v0_1/orchestration_runner.py:332` — refuse-branch literal
- `notes/elif_v0_1_e2_live_replay_report.md` — E.2 report
- `notes/elif_post_e2_room_emergence_audit.md` — prior emergence audit
- `notes/elif_g0_decision.md` — Position B adjudication
- `notes/elif_constitutional_layer.md` — Articles I-VII

---

**Audit closed. Findings recorded. ELIF remains in review state. Reality remains sovereign.**
