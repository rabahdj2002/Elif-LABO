# ELIF Audit C — Media, Communication & Experience Architecture

**Captured:** 2026-05-30
**Audit ID:** C_media_communication
**Status:** Operator-level strategic positioning audit. Non-expansionary.
**Sibling audits:** A (World Models), B (User Experience)
**Authority:** Positioning analysis only. This document does NOT propose new ELIF components, articles, phases, atom types, observers, or communication artefacts.

---

## Purpose and discipline

The operator authorized E.2 (live-replay pressure on v0.1 alpha) on 2026-05-30. The alpha shipped at 7 components / 11 steps / 2,533 LoC of components / 8,424 LoC total / 83% structural similarity against the operator-authored reference / 100% test pass / partial acceptance pending refuse-halt adjudication. The Constitutional Layer is locked at v0.4 (7 Articles + four-pole failure taxonomy + capacity-vs-truth + thinking-reed + emergent-wisdom recognition). The roadmap is locked at Phases 0–9 with confidence gradient HIGH (0–2) / MEDIUM (3–5) / SPECULATIVE (6–9).

Inside that fence, three questions remain unanswered at audit time:

1. What does ELIF actually communicate to a human, when a run completes?
2. What of OpenStudyGo's media substrate transfers, and what does not?
3. What productisation path is honest from this v0.1 alpha?

This document answers those questions with three epistemic registers held rigorously apart:

- **CURRENT EVIDENCE** — what v0.1 alpha + 33 fixtures + 3 reference cases + v0.4 doctrine demonstrably produce.
- **PLAUSIBLE FUTURE** — what holds if live-replay (E.2) reproduces the alpha's structural similarity at ≥0.83 with no architectural regressions.
- **SPECULATION** — claims that depend on substrates not yet shipped, on adoption decisions not yet made, or on judgments that have no current evidence in either project. Always labelled.

The transferability matrix in §C1 is the load-bearing piece of this audit. It is the section to read if nothing else is read.

---

## C1. Can ELIF reuse OpenStudyGo media structures?

The question is structural, not branded. For each major OSG media structure: classify as DIRECTLY TRANSFERABLE, TRANSFERABLE WITH MODIFICATION, or NON-TRANSFERABLE; cite which ELIF Article or behaviour the structure would serve; declare the transformation cost honestly.

The framing constraint: ELIF is a procedural arbitration system. Its outputs are decomposition / hypothesis / governance verdict / operative-truth separation / memory event. OSG media biome substrates are designed around pedagogical artefacts (atoms, companions, scenarios, narrators) optimised for cross-formation amortisation under cluster-of-5+ verification. The two systems share a doctrinal grammar (closed-set discipline, observer-first, four-organ separation, preserve-over-chase) but the artefacts they produce differ in kind.

### C1.1 Limova framework

**Classification:** NON-TRANSFERABLE.

**Reasoning:** Limova is a marketing/distribution substrate (SEO blogs, social posting, customer support drafts, prospecting). Its assistants (John / Lou / Tom / Elio / Julia / Manue / Charly / Rony) are bound to acquisition + amplification workflows that have no analogue in ELIF's procedural shape. ELIF does not have a learner audience to amplify into; it has a single operator (or, plausibly, a small operator team) running cases one at a time.

**Which ELIF behaviour would it serve?** None presently identifiable. Article V (refusal-capable) and Article I (non-absolutization) actively reject the kind of broadcast-shape, frequency-driven posting that Limova exists to coordinate.

**Honest reading:** Limova belongs to pedagogy. Any future ELIF surface that does need external reach (a public artefact registry, an operator-blog) would NOT route through Limova — the four-organ separation that keeps Limova out of OSG's runtime applies, recursively, to ELIF.

### C1.2 Gemini media generation layer

**Classification:** NON-TRANSFERABLE in current shape; the underlying *capability* (structured LLM cognition feeding pedagogical artefacts) is already present inside ELIF in different form (the 7 components' LLM adapter calls).

**Reasoning:** Gemini in the OSG architecture is the script/cognition layer between the formation seed and audio/video artefact pipelines. It produces scripts, capsules, sequencing. ELIF has no scripts and no capsules. ELIF has structured outputs (decomposition / hypothesis tree / roadmap / verdict) that an LLM adapter already produces inside the existing seven components, gated by closed-set vocabulary + schema validation + semantic post-validation.

**Which ELIF behaviour would it serve?** None directly. Lifting Gemini into ELIF would mean importing a generation organ that is structurally redundant with ELIF's own LLM adapter (`llm_adapter.py`, 279 LoC) under Articles I (non-absolutization) and III (no self-validation).

**Honest reading:** the temptation will be to say "Gemini could draft natural-language briefings of ELIF outputs." That capability does not require Gemini-the-organ; it requires a single additional structured-output template inside the existing adapter. Importing Gemini would be architectural inflation.

### C1.3 Atom generation pipeline

**Classification:** TRANSFERABLE WITH MODIFICATION — but the modification is heavy enough to make the transfer marginal.

**Reasoning:** The OSG atom-generation pipeline produces validated, hash-pinned, closed-set-typed pedagogical artefacts at scale (target ~32K atom instances at 5K formations). The mechanism — generate → IC/AV validate → canonical-promote → register by hash → re-use across formations sharing structural fingerprints — is structurally analogous to how ELIF could produce **reusable arbitration artefacts**: a Step-2 decomposition shape, a Step-7 trajectory, a Step-9 verdict pattern. Capacity-vs-truth (Article VII) requires this kind of compositional reuse — "faster arbitration on similar-shape problems."

**Required modifications:** atom_type, atom_domain, canonical-status semantics, partial-credit cap, scenario eligibility — none of these names survive. ELIF would need: arbitration_artefact_type, problem_shape_fingerprint, pattern_invitation_status (note: NOT "canonical" — the word implies sovereignty Article I forbids), refutation_condition.

**Which ELIF behaviour does it serve?** Article VII (Generative Reconstruction) directly. The Memory Logger is the substrate site for Article VII; an atom-style hash-pinned-and-typed registry of past arbitration shapes is exactly the compositional reuse substrate Article VII names.

**Honest cost:** roughly equivalent to building it from scratch under different names. The transfer is conceptual, not file-portable. **CURRENT EVIDENCE:** none — Article VII is currently tested only at the persistence-infrastructure level (open / step_committed / refutation / close events written), not at the content level (judgment_act / pattern_engaged / capacity_change entries NOT emitted in alpha refuse-path runs). **PLAUSIBLE FUTURE:** if E.2 + a Position-B refuse-halt resolution emits Step 11 content entries, a pattern registry becomes feasible. Until then, this transfer is unauthorised by evidence.

### C1.4 Companion architecture

**Classification:** NON-TRANSFERABLE.

**Reasoning:** A companion is a per-formation pedagogical artefact bundle: ordered atoms, audio capsules, scenarios, manifest. It is per-learner-facing. ELIF has no learner and no per-case bundled artefact comparable to a companion. The closest ELIF analogue (a per-case RunReport: open + 9 step_committed + refutation + close events + JSONL trail + structured run_report) is fundamentally different in kind — it is an audit trail of arbitration, not a deliverable pedagogical artefact.

**Which ELIF behaviour would it serve?** None. Mapping companion architecture onto ELIF would import a learner-facing framing the system does not have and the Constitutional Layer does not invite.

**Honest reading:** the structural similarity ("a per-X bundle of typed sub-artefacts") is real but shallow. The semantics diverge entirely once you ask: what does the bundle *do* for the receiver?

### C1.5 Concept explainers

**Classification:** NON-TRANSFERABLE.

**Reasoning:** A concept explainer in OSG is an atom_type whose job is to teach a concept to a learner who does not yet know it. ELIF's outputs are arbitration verdicts, not pedagogical instruction. The operator running an ELIF case already understands the problem domain; they are seeking decomposition / hypothesis arbitration / verdict on a bundled question — not a tutorial.

**Which ELIF behaviour would it serve?** None directly. Frame validation (Step 1 + 3) surfaces assumptions; that's surfacing, not explaining.

**Speculation, labelled:** at a far-future V3+ surface (decision room, multiple operators) some ELIF outputs may need light explanation of their *meaning* — e.g., what a `verdict=refuse` with confidence_qualifier means in plain English for a stakeholder. That is a translation surface, not a concept-explainer transfer. Build small, not transfer.

### C1.6 Scenario library (8 closed-set shapes)

**Classification:** NON-TRANSFERABLE in content; the *closed-set-of-shapes discipline* is doctrinally relevant.

**Reasoning:** The 8 scenario shapes (clinical_judgment_triage / multistep_decision_under_uncertainty / troubleshooting_diagnostic / safety_inspection_checklist / case_analysis_root_cause / ethical_dilemma_resolution / technical_implementation_planning / regulatory_compliance_audit) are pedagogical scenarios — what does a learner DO inside them. ELIF's procedure does not contain scenarios; it contains arbitration steps. The eight shapes do not map onto Steps 1–11.

**What IS transferable:** the *discipline* of identifying a closed-set of structurally-distinct shapes that recur across cases and freezing the set at a finite cardinality. ELIF already does this: 11 steps, 4 failure modes, closed-set verdict vocabulary, closed-set event_types and change_types. The scenario library is an additional instance of the same doctrinal grammar already present in ELIF. The mechanism does not need to be imported because the discipline is already operating.

**Which ELIF behaviour would the discipline serve?** Article VII's pattern-emergence and pattern-deprecation regime requires exactly this kind of finite-cardinality closed set, and ELIF already uses it.

**Honest reading:** no transfer. The discipline is already shared.

### C1.7 Cognitive density doctrine

**Classification:** TRANSFERABLE WITH MODIFICATION — the doctrine itself transfers; its concrete metrics do not.

**Reasoning:** OSG's cognitive density doctrine says: text-native primary, audio surgical, video narrow, never modality collapse. The doctrine resists engagement-theater (completion ≠ retention). ELIF's analogue would be: arbitration-output-density should match the operator's actual reasoning load; "cognitive ease through visualisation" is its own false-closure mode (Article V dual: refusal-where-evidence-is-sufficient = refusal-theater; symmetrically, *clarity-without-decomposition* = clarity-theater).

**Which ELIF behaviour does it serve?** Article V dual + the broader risk identified in §C7 below as "over-visualisation." The doctrine provides a structural defence against pretty dashboards eating judgment substance.

**Required modifications:** drop the text/audio/video closed-set; ELIF's modality is structured-text-output (JSON envelopes for each step) plus a possible operator-readable summary view. The density doctrine becomes: "every visible output earns its place by surfacing a step's load-bearing content, not by rendering it pleasingly."

**Honest cost:** writing one short ELIF-doctrine paragraph; importing nothing.

### C1.8 Friction-preserving learning structures

**Classification:** TRANSFERABLE WITH MODIFICATION — extremely relevant doctrinally; not portable as code.

**Reasoning:** OSG's friction-preserving doctrine resists the "smooth UX" temptation that turns learning into consumption. ELIF has a sibling temptation: turn the 11-step procedure into a one-click "Get Verdict" button that hides the steps the operator was supposed to engage with. That would collapse the procedure into a magic-8-ball, weaponizing Article V refusal-capability into refusal-theater (the verdict is refuse but the operator never engaged with the decomposition that produced it).

**Which ELIF behaviour does it serve?** Articles II + III + IV directly. Frame humility, no self-validation, partiality of models — all require the operator to engage with the surfaced assumptions and decompositions, not to receive a verdict in isolation.

**Required modification:** rename. The OSG concept is "friction preserves learning"; the ELIF concept is "friction preserves judgment". Same shape, different semantics.

**Honest cost:** one paragraph of doctrine; structural commitment in any UX design.

### C1.9 Narrator library (8 closed-set profiles, voice-routing, tone classes)

**Classification:** NON-TRANSFERABLE.

**Reasoning:** Narrators are a TTS-layer artefact — a fingerprinted voice consumed across formations in a language at 1.0 inheritance ratio. ELIF has no audio output. No analogue exists for a "voice identity" of arbitration outputs. The operator might IMAGINE that ELIF outputs could be narrated; that imagination would import a delivery modality the system does not need and that risks engagement-theater (a soothing voice reading a refuse-verdict is exactly the failure mode the cognitive density doctrine in §C1.7 names).

**Which ELIF behaviour would it serve?** None.

**Speculation, labelled:** at V3+ a screen-reader-accessible audio output of a structured verdict might be useful for accessibility. That is an accessibility transformation, not a narrator-library transfer.

### C1.10 Atom library (14 domain categories closed-set)

**Classification:** NON-TRANSFERABLE in content; the *14-domain partition* is a pedagogical taxonomy with no ELIF analogue.

**Reasoning:** The 14 domain categories (healthcare_clinical, trades_construction, exam_prep_methodology, etc.) partition the pedagogical universe. ELIF cases are problem-frames; they cluster by *problem shape* (scientific-evidential ambiguity / policy-governance-bundle / operational-organizational-bundle — the three case clusters already in the alpha) not by domain.

**What IS transferable:** the *closed-set-domain-partition discipline*. ELIF already uses problem-shape clustering in the alpha cases. As cases accumulate, ELIF will need a finite, closed-set partition of problem shapes to enable Article VII compositional reuse. The mechanism (a hash-indexed registry with import-time closed-set sanity gates) is portable; the contents are not.

**Speculation, labelled:** the existing 3 case clusters (A/B/C) might become the seed of an ELIF problem-shape closed-set. This is pure speculation until E.2 + further cases provide evidence that the clustering survives pressure.

### C1.11 Shell propagation engine (cross-language)

**Classification:** NON-TRANSFERABLE.

**Reasoning:** Shell propagation is country-aware lexicon substitution: "Medicare" → "NHS" → "HMRC" → "Medicare AU". ELIF outputs do not have country-specific lexicon to substitute. A frame validation that asks whether `electroculture pilot deployment` is well-bundled does not change its arbitration shape between US and UK contexts. The arbitration question is invariant under shell.

**Which ELIF behaviour would it serve?** None. Importing shell-substitution would create a non-load-bearing layer.

**Speculation, labelled:** at far-future V4+ if ELIF operates on regulatory bundles whose constituents differ by jurisdiction (US-only / EU-only regulators), some lexical localisation might be useful. This is true speculation — multiple substrate decisions away.

### C1.12 34-observer media biome registry

**Classification:** NON-TRANSFERABLE in content; the *observer-first discipline + state-machine + closed-set registry pattern* is doctrinally shared.

**Reasoning:** The 34 observers (4 acquisition + 8 MV + 8 LIM + 5 GEM + 5 AUD + 4 XO) observe media-side phenomena (publication cadence, voice drift, cognitive fragmentation in micro-videos, etc.) that have no ELIF analogue. ELIF has no publication surface, no voice drift to detect, no micro-video chains. Importing the registry is meaningless.

**What IS transferable:** the *observer-first + state-machine + closed-set registry* pattern. ELIF already uses this in a different form: the MemoryLogger has closed-set event_types and change_types, the schemas have closed-set verdict and confidence vocabularies. The build-plan §3.6 specifies a sterile-equilibrium signature detector inside MemoryLogger. The discipline is present; only the specific observer names from media biome are non-portable.

**Honest reading:** if ELIF eventually grows additional observation surfaces (e.g., a drift-probe observer for hypothesis-as-concern emission, a fragmentation detector for over-decomposition), the *machinery* — DORMANT → REVIEW_PENDING → PILOT → SIGNAL_EMIT → HALT_CAPABLE → QUARANTINED → RETIRED, hibernation requirements, halt-action exclusivity — is structurally importable. The specific 34 names are not.

**Which ELIF behaviour does the discipline serve?** Article VII anti-sterile-equilibrium directly (the state machine is the structural anti-drift defence).

### C1.13 State machine (DORMANT → REVIEW_PENDING → PILOT → SIGNAL_EMIT → HALT_CAPABLE → QUARANTINED → RETIRED)

**Classification:** TRANSFERABLE WITH MODIFICATION — high-fit pattern for any future ELIF observer infrastructure; not portable as-is because the state semantics are media-specific (PILOT = `read_only`, SIGNAL_EMIT = `signal_emit_only` to audit log; HALT_CAPABLE = can trigger biome-wide halt actions).

**Required modifications:** ELIF observers (if/when they exist) observe a different substrate (procedural drift, fragmentation signatures, sterile-equilibrium markers in the MemoryLogger). PILOT / SIGNAL_EMIT semantics need to be reframed around procedural arbitration rather than media publication.

**Which ELIF behaviour does it serve?** Article VII enforcement at the substrate level. The state machine is the structural defence against ceremonial activation ("we activated observers but they don't actually fire").

**Honest cost:** the file is ~400 LoC; a port would be ~250 LoC under ELIF semantics. **PLAUSIBLE FUTURE only** — there is no evidence yet that ELIF needs additional observer infrastructure beyond what schemas + semantic post-validation already enforce.

### C1.14 Halt actions (8 with biome-wide exclusivity)

**Classification:** TRANSFERABLE WITH MODIFICATION — the *single-carrier exclusivity invariant* is doctrinally relevant; the 8 specific halt action IDs are media-specific.

**Reasoning:** The 8 halt actions (HA-PUB-REFUSE / HA-PUB-CHANNEL-PAUSE / HA-PUB-BIOME-PAUSE / HA-CAPSULE-REJECT / HA-CAPSULE-PIPELINE-PAUSE / HA-COST-LEDGER-HALT / HA-OUTBOUND-BLOCK / HA-AUDIT-ALERT-ONLY) bind to media publication and TTS substrate. ELIF has no publication, no capsule pipeline, no outbound channel. The names do not transfer.

**What IS transferable:** the *single-carrier-exclusivity discipline* — at most one observer may carry a biome-wide-exclusive action. This is the structural defence against multiple observers triggering correlated halts under the same root cause. ELIF's analogue would be: at most one component may carry the run-level halt authority; currently this is `governance_kernel` (Step 9 verdict). The discipline is implicitly present; making it explicit in code would be an honest port.

**Which ELIF behaviour does it serve?** Articles V + VI (refusal-capability + coherent convergence). Halt authority concentrated in one place avoids fragmentation of refusal.

**Honest cost:** ~100 LoC of explicit invariant code; **CURRENT EVIDENCE** already shows the runner halts at Step 9 cleanly across all 3 alpha cases.

### C1.15 Micro-video chaining doctrine

**Classification:** NON-TRANSFERABLE in content; the *engagement-theater warning* is doctrinally critical for ELIF V1+.

**Reasoning:** The micro-video doctrine is about NOT shipping chained 8-second clips as primary pedagogy. ELIF has no clips. But the deeper finding — *the failure mode where completion-rate looks good while 30-day retention diverges* — has a direct ELIF analogue. Replace "completion-rate" with "operator-runs-completed-without-engagement-with-decomposition". Replace "30-day-retention" with "subsequent-case-quality-of-decomposition". The failure mode is identical: a system that produces well-formed outputs that the operator doesn't engage with becomes a magic-8-ball.

**Which ELIF behaviour does it serve?** Article V dual (refusal-where-engagement-was-skipped = refusal-theater); Article III (no self-validation: the system's well-formed output is not proof of substantive engagement).

**Honest reading:** the micro-video doctrine is the structural antecedent of an ELIF UX doctrine (audit-by-engagement, not by output-completion). The transfer is doctrinal, paragraph-length, not code-length.

### C1.16 Transferability matrix (consolidated)

See **Transferability matrix summary** at end-of-document. The honest aggregate verdict: of 15 structures audited, 3 are TRANSFERABLE WITH MODIFICATION (atom generation pipeline, cognitive density doctrine, friction-preserving learning structures) and 1 borderline (state machine + halt actions as discipline). The rest are NON-TRANSFERABLE because they belong to pedagogy (companion / concept explainer / narrator / atom library / shell propagation / Limova / Gemini / scenario / 34 observers / micro-video) and ELIF is not a pedagogical system.

The honest summary: **the OSG media substrate transfers as DOCTRINE more than as CODE.** Anyone proposing to "reuse the media biome for ELIF" should first identify which file they want, ask which ELIF Article it serves, and apply the burden of proof in §C1.3 and §C1.10 honestly.

---

## C2. What is ELIF actually communicating?

OpenStudyGo communicates pedagogical knowledge / skill / competency / mastery, addressed to a learner. ELIF communicates something structurally different. This section names what.

### C2.1 The communication objects ELIF produces

For each ELIF output type, the audit names what the OUTPUT IS as a communication object, what an operator RECEIVES, and what action the operator can take with it.

**Decomposition (Step 3 frame + Step 2 object decomposition):**
- *Communication object:* a finite, closed-set-typed enumeration of axes + families + assumptions surfaced from a bundled question.
- *Operator receives* (from case_01): two axes with ≥2 families each (mechanism plausibility families A/B/C + reversibility families D/E), plus ≥2 surfaced assumptions.
- *Action enabled:* operator can see the structure of the question they thought they asked; can identify which axis they had not considered.
- *Article tie:* II (Frame Humility) + III (Decomposed Reasoning).

**Frame surfacing / deeper-frame rejection (Step 2 + 5):**
- *Communication object:* a verdict ∈ {valid, invalid, needs_decomposition} on the user's framing, plus a list of surfaced assumptions, plus (in Step 5) per-hypothesis fails_if conditions.
- *Operator receives* (alpha, all 3 cases): `verdict = needs_decomposition` plus assumption list.
- *Action enabled:* operator can refuse the original framing as a single binary question; can decompose into the axes the frame implicitly bundled.
- *Article tie:* II + V (refusal-capable framing rejection).

**Hypothesis tree with distinguishing predictions (Step 4):**
- *Communication object:* a set of hypotheses, each carrying a distinguishing_prediction (what evidence would discriminate this hypothesis from the others) and fails_if (what evidence would refute it).
- *Operator receives* (alpha, all 3 cases): a hypothesis set matching reference shape, schema-validated.
- *Action enabled:* operator can identify what evidence to collect to advance arbitration; can recognise hypothesis-as-concern drift (a hypothesis without a distinguishing_prediction is structurally forbidden by schema).
- *Article tie:* I (Epistemic Discipline) + III.

**Failure-conditions per hypothesis (Step 5):**
- *Communication object:* an explicit `fails_if` block per hypothesis, listing the evidence patterns that would refute it.
- *Operator receives* (alpha, all 3 cases): fails_if conditions matching reference shape.
- *Action enabled:* operator can hold every hypothesis to its refutation condition rather than discarding refutation when convenient.
- *Article tie:* I directly; III enforced.

**Branching roadmap (Step 6 multi-scale + Step 7-modeA + Step 8 stage-gated):**
- *Communication object:* a stage-gated roadmap with continuation_gates per stage + outside-original-frame trajectories.
- *Operator receives* (alpha, all 3 cases): roadmap matching reference T1–T4 trajectories + stage-gated structure.
- *Action enabled:* operator can identify the alternatives to the bundle they were originally proposed (T1–T4 are alternatives to "deploy the bundle as proposed"); can identify per-stage gates that justify continuation or refusal.
- *Article tie:* V + VI + VII.

**Governance verdict with confidence_qualifier + uncertainty_sources (Step 9):**
- *Communication object:* `{verdict, verdict_detail?, confidence, unresolved_uncertainty_sources}` where verdict ∈ {constrain, refuse, explicitly_abstain}, confidence is a free-text qualifier tied to ≥1 named uncertainty source, and unresolved_uncertainty_sources has minItems=1.
- *Operator receives* (alpha, all 3 cases): `verdict=refuse` + confidence text + ≥1 uncertainty source.
- *Action enabled:* operator can act on a verdict that comes with explicit conditions of its own refutability; cannot mistake a refusal for an absolute claim (Article I structurally enforced via mandatory uncertainty source).
- *Article tie:* V + VI + VII.

**Operative/theoretical separation (Step 10):**
- *Communication object:* operative-list + theoretical-list + optional absence_log.
- *Operator receives* (alpha, all 3 cases): **NOT EXECUTED.** Runner halts at Step 9 on refuse-verdict. Fixture exists and validates; runtime behaviour pending operator adjudication on refuse-halt position (Position A status quo / Position B reference-matching).
- *Action enabled (if executed):* operator can distinguish "what we will treat as operative knowledge under current evidence" from "what remains theoretical, partial, open."
- *Article tie:* IV (Partiality of Models).
- *Compromise:* the component is implemented at 207 LoC; the runtime path is not exercised. The communication object exists in schema but does not currently reach the operator in alpha refuse-cases.

**Memory event with Article VII tracking (Step 11, absorbed into Step 9 in v1.0 + persisted via MemoryLogger):**
- *Communication object:* persisted JSONL events — `open`, per-step `step_committed`, `refutation`, `close`, plus (when executed) `judgment_act`, `pattern_engaged`, `capacity_change`.
- *Operator receives* (alpha, all 3 cases): 14 events written per case (open + 9 step_committed + 1 step_7_modeB + 1 refutation + 1 close + 1 bookkeeping). Content-level Step 11 entries (judgment_act / pattern_engaged / capacity_change) **NOT WRITTEN** under refuse-halt.
- *Action enabled (in alpha):* operator can audit a run after the fact via JSONL trail; can verify the procedure ran end-to-end.
- *Action enabled (if Step 11 content entries fire):* operator can begin to observe Article VII capacity accumulation cross-case — faster arbitration on similar-shape problems, compositional reuse of prior decomposition shapes.
- *Article tie:* VII directly.

### C2.2 What the user actually receives at the end of a v0.1 alpha run

Pointing to case_01_electroculture's actual alpha output shape (from §case_01.7 of the replay report):

- **A structured RunReport object** with `exit_code=20` (governance refuse), per-step envelopes, timestamps.
- **9 schema-valid step output JSONs** (Step 1 through Step 9; Step 10 fixture available but not executed; Step 11 own-content not emitted).
- **A doctrinal verdict (`refuse`)** matching the operator-authored Condition C reference.
- **A reasoned uncertainty-source list** named on the Step 9 output.
- **A MemoryLogger JSONL trail** (14 events for case_01) persisting the run.

**This is what a user receives.** Not a narrative briefing. Not a rendered chart. Not an audio explanation. A structured machine-readable trace plus a refuse-verdict plus a list of unresolved uncertainty sources.

### C2.3 The communication object ELIF is

Putting it as one sentence: ELIF communicates **a structurally-decomposed arbitration verdict with explicit refutation conditions on every claim it makes**. The communication object is not knowledge; it is an arbitration shape — a structured statement about how a question was decomposed, which hypotheses survived schema validation, which roadmap shapes were considered outside the original frame, and what the governance kernel concluded with its own confidence and uncertainty surfaced.

**This is not what OpenStudyGo communicates.** OSG hands a learner content that, if mastered, becomes their knowledge. ELIF hands an operator an *arbitration trace* that, if engaged with, becomes their judgment substrate for this case and (via MemoryLogger Article VII) for similar future cases.

The pressure-test of the operator's working hypothesis ("LLMs generate. World models simulate. Agents execute. ELIF validates, arbitrates, governs, structures discovery, preserves corrigibility.") at this level:

- "Validates" is supported by alpha evidence (frame validator + governance kernel produce schema-valid verdicts matching reference).
- "Arbitrates" is supported by alpha evidence (hypothesis validator + branching roadmap engine produce arbitrated outputs).
- "Governs" is supported by alpha evidence (refuse-halt discipline operationalises Articles V + VI + VII at the runner level).
- "Structures discovery" is partially supported (Step 7 outside-original-frame trajectories matching reference; Step 8 stage-gated roadmap matching).
- "Preserves corrigibility" is partially supported (MemoryLogger persistence path works; Step 11 content-pass not yet exercised under refuse-halt).

The hypothesis is firmer at the validates/arbitrates end and softer at the structures-discovery/preserves-corrigibility end. **PLAUSIBLE FUTURE:** under E.2 live-replay pressure these distinctions become measurable. **SPECULATION:** that ELIF's corrigibility role becomes the deepest part of its value once cross-case state replay (v0.2 scope) tests compositional reuse.

---

## C3. ELIF media taxonomy

A "media" taxonomy for ELIF must be ruthlessly anti-decorative. Each candidate is anchored to a specific Article or substrate behaviour. Anything anchored to "looks good" is rejected at this layer of the audit.

The classification scheme:
- **INDISPENSABLE** — without this surface, the corresponding Article cannot be communicated to the operator at all.
- **USEFUL** — this surface materially improves operator engagement with substrate; the substrate exists without it but is harder to engage.
- **OPTIONAL** — this surface is defensible at later phases but not load-bearing.
- **DECORATIVE** — this surface adds visual mass without engaging substrate; structurally rejected on cognitive density doctrine grounds (§C1.7).

### C3.1 Executive briefs

- **Classification:** OPTIONAL at V2+; DECORATIVE if presented as the primary output.
- **Article anchor:** none directly. A brief that summarises a refuse-verdict + uncertainty sources risks collapsing the procedural engagement Articles II + III + IV require.
- **Substrate behaviour at risk:** Frame humility (II) and decomposition discipline (III) require the operator to engage with the decomposition, not skip past it to a summary.
- **Honest reading:** a brief is acceptable as an *operator-requested* exit view (with explicit "this elides the decomposition"); structurally rejected as a default surface.

### C3.2 Decision maps

- **Classification:** USEFUL at V2+.
- **Article anchor:** VI (Coherent Convergence). A decision map is the visible form of the Step 8 stage-gated roadmap with continuation_gates per stage.
- **Substrate behaviour served:** rendering the trajectories T1–T4 + their stage gates so the operator can see the arbitrated alternatives + the conditions for moving between stages.
- **Risk:** map-as-aesthetic could decorate without serving Article VI. Map must render the schema-validated structure, not a stylised approximation.

### C3.3 Governance alerts

- **Classification:** INDISPENSABLE.
- **Article anchor:** V (Refusal-Capable) directly.
- **Substrate behaviour served:** surfacing `verdict=refuse` to the operator with sufficient prominence that it cannot be missed. Currently surfaced via `exit_code=20` + the Step 9 schema output; that is sufficient for a CLI-level operator. At any V1+ surface beyond CLI, a governance-alert surface is structurally required.
- **Honest reading:** the refuse-verdict is the load-bearing output of the system. A surface that hides it (or presents it as one option among many) is doctrine-violating.

### C3.4 Decomposition cards

- **Classification:** USEFUL at V1.
- **Article anchor:** III (Decomposed Reasoning) + II (Frame Humility).
- **Substrate behaviour served:** rendering the Step 2 axes + families and Step 3 surfaced assumptions in a form the operator can engage with directly. Currently this is a JSON output; an operator-facing card view (one card per axis, one card per assumption) is structurally honest.
- **Honest reading:** the card form is a translation of an existing schema-validated output, not a new artefact. No new substrate is needed.

### C3.5 Hypothesis cards

- **Classification:** USEFUL at V1.
- **Article anchor:** I (Epistemic Discipline) + III.
- **Substrate behaviour served:** rendering each Step 4 hypothesis with its distinguishing_prediction + fails_if visible. The schema already requires both; the card surfaces them with equal weight.
- **Honest reading:** schema-equality of distinguishing_prediction + fails_if must be UI-equality. Hiding fails_if behind a "details" click would be doctrine-violating — Article I is operationalised by making refutation conditions visible.

### C3.6 Trajectory maps

- **Classification:** USEFUL at V2+; depends on decision-map adoption (overlaps with §C3.2).
- **Article anchor:** V + VI + VII.
- **Substrate behaviour served:** rendering the Step 7 outside-original-frame trajectories so the operator can see what was *not* the proposed bundle.
- **Risk:** a trajectory map that animates between options risks engagement-theater (pretty motion, no decomposition engagement). Static, schema-derived layout only.

### C3.7 Scenario trees

- **Classification:** DECORATIVE for ELIF.
- **Article anchor:** none.
- **Substrate behaviour:** scenarios are an OSG pedagogical artefact (closed-set of 8 shapes per §C1.6). ELIF has no scenarios in this sense. Importing scenario-tree visualisation would import OSG's pedagogical framing — exactly the educational-contamination risk in §C7.8.
- **Honest reading:** explicitly rejected. Not "optional later" — structurally not a fit.

### C3.8 Simulation views

- **Classification:** SPECULATION (deferred to Audit A).
- **Article anchor:** none currently.
- **Cross-audit note:** simulation belongs to Audit A (World Models). If ELIF eventually integrates with simulation substrate, the visualisation question is downstream of the integration question. Audit C does not pre-empt Audit A.

### C3.9 Uncertainty dashboards

- **Classification:** USEFUL at V2+.
- **Article anchor:** I + V + VI. The Step 9 mandatory unresolved_uncertainty_sources field is the substrate; a dashboard renders it across cases.
- **Substrate behaviour served:** at single-case scale, a list is sufficient. At cross-case scale (v0.2+), aggregating uncertainty sources across cases — which kinds of uncertainty recur, which are resolved by accumulated evidence — feeds Article VII pattern recognition. The dashboard is the rendering of this cross-case aggregation.
- **Risk:** dashboard-as-metric-game (turning uncertainty into a number to "track down") would re-import sovereignty. The dashboard must preserve uncertainty as substantive, not gamify it.

### C3.10 Audio briefings

- **Classification:** DECORATIVE.
- **Article anchor:** none.
- **Substrate behaviour at risk:** audio narration of arbitration verdicts is the exact failure mode the cognitive density doctrine (§C1.7) and engagement-theater warning (§C1.15) name. A soothing voice reading "verdict=refuse, confidence qualifier: low" is a clarity-theater artefact.
- **Honest reading:** explicitly rejected at all phases. The only audio use case that would survive is screen-reader-accessible output of the structured text — that is accessibility infrastructure, not an audio briefing surface.

### C3.11 Video explainers

- **Classification:** DECORATIVE.
- **Article anchor:** none.
- **Substrate behaviour at risk:** identical to §C3.10. Video explainers of ELIF outputs would be the worst expression of engagement-theater — visually pleasing renderings of refusal-verdicts the operator never engaged with.
- **Honest reading:** explicitly rejected at all phases. Not a fit for ELIF's communication object.

### C3.12 Aggregate finding

Of 11 candidates:
- 1 INDISPENSABLE (governance alerts)
- 4 USEFUL at V1/V2 (decision maps, decomposition cards, hypothesis cards, trajectory maps, uncertainty dashboards — counting trajectory maps + decision maps together as overlapping surfaces, 4 distinct surfaces)
- 1 OPTIONAL (executive briefs — restricted use)
- 1 SPECULATION-deferred-to-A (simulation views)
- 4 DECORATIVE/rejected (scenario trees, audio briefings, video explainers)

The communication surface for ELIF is small. It is anchored on rendering schema-validated structured outputs honestly, not on producing media-rich artefacts.

---

## C4. Limova / Gemini compatibility

This section addresses the operator's specific question: could Limova-style atoms exist inside ELIF; could Gemini-style media generation eventually support ELIF; is ELIF a fundamentally different media architecture than OSG.

### C4.1 Could Limova-style atoms exist inside ELIF?

Per the candidate atom types:

**Decomposition atom:** a structured artefact representing one Step 2 axis-family decomposition shape, hash-pinned, reusable across cases sharing the same problem-shape fingerprint.
- *Could exist?* YES under Article VII (Generative Reconstruction) once cross-case state replay (v0.2 scope) is implemented and Step 11 content entries emit.
- *Honest cost:* substantial. Requires Step 11 content-pass execution (currently blocked by refuse-halt question), requires problem-shape fingerprinting (currently informal — the 3 case clusters A/B/C), requires hash-pinning discipline (analogous to OSG atom-canonical promotion but with different semantics — "pattern_invitation_status", not "canonical", to respect Article I).
- *CURRENT EVIDENCE:* none. The substrate to file this kind of atom does not exist.
- *PLAUSIBLE FUTURE:* if E.2 + refuse-halt resolution + v0.2 cross-case replay produce stable pattern emergence per Article VII benchmark requirements ("compositional reuse frequency: case N references case N-1 structures"), decomposition atoms become a credible substrate.

**Governance atom:** a structured artefact representing one Step 9 verdict shape (refuse-with-uncertainty-sources X/Y/Z) reusable as a recognisable arbitration pattern.
- *Could exist?* YES under Article VII, with the same caveats as decomposition atoms.
- *Honest risk:* governance atoms approach pattern-as-prestige (risk 24 in v0.4 risk matrix). Memory Logger as prestige store is structurally forbidden; deprecation routine is required for any atom registry.

**Tradeoff atom:** a structured artefact representing one Step 7 outside-original-frame trajectory pattern.
- *Could exist?* YES under Article VII with caveats above.
- *Honest reading:* the trajectory T1–T4 in the alpha cases are structurally similar across the 3 cases (each case produces ~4 outside-frame trajectories). This is suggestive but not yet evidence of pattern stability.

**Trajectory atom:** synonymous with tradeoff atom above; one Step 7 trajectory becomes a recognisable shape.
- See above.

**Uncertainty atom:** a structured artefact representing one unresolved_uncertainty_source pattern (e.g., "mechanism uncertainty in agritech bundles") reusable across cases.
- *Could exist?* YES; uncertainty-source recurrence is already partially observable in the 3 alpha cases (each surfaces ≥1 uncertainty source; cross-case overlap is not yet measured).
- *Honest risk:* uncertainty atoms could become a substrate for sovereignty re-import ("we know what kinds of uncertainty matter"). Risk 23 in v0.4 risk matrix (capacity framed as truth approach) applies hardest here. Article I + III enforcement must apply recursively to the atom registry itself.

**Simulation atom:** a structured artefact representing a simulation hypothesis or simulation-derived prediction.
- *Could exist?* SPECULATION. Deferred to Audit A. The substrate (simulation integration) is not present and the operator's working hypothesis posits world models as a separate organ ("World models simulate.") — making "simulation atom inside ELIF" a category error pending Audit A's positioning.

### C4.2 Could Gemini-style media generation eventually support ELIF?

The question is whether an external LLM cognition organ tuned for media artefact generation could feed ELIF. Honest answer:

**Not as Gemini-the-OSG-organ.** Gemini in OSG produces scripts + capsules + sequencing for pedagogical delivery. ELIF has no pedagogical delivery. Importing Gemini-as-organ is architectural inflation per §C1.2.

**As a cognition substrate for an ELIF translation layer (operator brief surfacing) — YES, but at V2+.** A structured-output template that translates a Step 9 verdict + uncertainty sources into a one-paragraph operator-facing summary IS a cognition task. It does NOT require Gemini-the-organ; it requires one additional template inside the existing `llm_adapter.py`. The discipline of structured-output + closed-set vocabulary already exists; the briefing template is a thin extension.

**Doctrine cost:** none if implemented as an additional adapter template; substantial (organ-import) if implemented as a separate cognition organ. The honest choice is the thin extension.

### C4.3 Is ELIF a fundamentally different media architecture than OSG?

**YES.**

The two systems share doctrinal grammar (closed-set discipline, observer-first, four-organ separation, preserve-over-chase, runtime authority separation, anti-monoculture) and a doctrine of how to govern AI cognition (validate-before-promote, schema-required structured outputs, no auto-promotion, hibernation periods, memory-blessing rituals).

But the **artefacts they produce differ in kind**:

- OSG produces pedagogical artefacts that compose into learner-facing companion bundles addressed to a many-to-many learner audience under content-density and acquisition-observability disciplines.
- ELIF produces arbitration traces addressed to a one-to-one operator audience under epistemic-discipline and capacity-accumulation disciplines.

The substrate they amortise is different:
- OSG amortises *content* (an atom reused across formations sharing a domain) and *voice* (a narrator fingerprint reused across formations sharing a language).
- ELIF amortises *arbitration shape* (a decomposition pattern reused across cases sharing a problem-shape, if/when Article VII content entries operationalise) and *judgment* (an operative/theoretical separation pattern reused across cases sharing an evidentiary structure).

The receiver-action they invite is different:
- OSG's artefacts invite learning (study, exercise, mastery, transfer).
- ELIF's artefacts invite judgment (engagement with decomposition, weighing of hypotheses against their fails_if, accepting or refusing a verdict whose refutation conditions are explicit).

**Shared substrate** (the doctrinal grammar): closed-set discipline, observer-first posture, anti-monoculture, runtime authority separation, four-organ separation. These are not OSG-specific; they are project-wide governance discipline that ELIF inherited at v0.4. The shared substrate is governance, not media.

**Divergence:** the artefacts, the receivers, the actions invited. Different kinds.

**Operational implication:** mechanisms-as-doctrine transfer (the discipline of closed-set vocabulary, the observer-state-machine pattern, the partial-credit cap framing under Article VII). Mechanisms-as-code largely do not transfer (atom library, narrator library, scenario library, companion architecture, shell propagation, micro-video doctrine). The §C1 transferability matrix expresses this.

---

## C5. ELIF user journey

The operator's straw-man:

> Question → Frame validation → Decomposition → Tensions → Hypotheses → Trajectories → Governance → Recommendation → Memory

The actual 11-step procedure (per shipped scaffold):

| Step | Owner | Substance |
|---|---|---|
| 1 | frame_validator | Initial frame validation (verdict ∈ {valid, invalid, needs_decomposition}) |
| 2 | object_decomposer | Object decomposition (≥2 axes, ≥2 families per axis) |
| 3 | frame_validator | Frame surfacing — assumptions surfaced from frame |
| 4 | hypothesis_validator | Hypothesis emission with distinguishing_prediction per hypothesis |
| 5 | hypothesis_validator | Failure conditions (fails_if) per hypothesis + deeper-frame rejection probe |
| 6 | object_decomposer | Multi-scale relation — scales identified + cross-scale relations |
| 7-A | branching_roadmap_engine | Outside-original-frame trajectories emitted |
| 7-B | frame_validator | Outside-frame BRE feeds back into frame validator for cross-check |
| 8 | branching_roadmap_engine | Stage-gated roadmap with continuation_gates per stage |
| 9 | governance_kernel | Verdict + confidence_qualifier + unresolved_uncertainty_sources (absorbed Step 11) |
| 10 | operative_truth_separator | Operative-list + theoretical-list + optional absence_log |
| 11 | memory_logger | Memory event entries (judgment_act / pattern_engaged / capacity_change) |

### C5.1 Where the straw-man and the procedure align

Strong alignment for the front half:
- "Question" → input frame (per InputFrame schema)
- "Frame validation" → Step 1
- "Decomposition" → Step 2 (object_decomposer 2 axes); the straw-man labelled "Decomposition" but the procedure decomposes the OBJECT (the bundle being asked about), not the question itself.
- "Tensions" → loosely Step 3 (assumptions surfaced) + Step 5 (fails_if); the straw-man does not have a clean 1:1 mapping here.
- "Hypotheses" → Step 4 + Step 5 hypothesis-validator outputs.
- "Trajectories" → Step 7-modeA outside-original-frame trajectories.
- "Governance" → Step 9 verdict + confidence + uncertainty.

### C5.2 Where the straw-man and the procedure diverge

The straw-man omits or compresses:
- **Step 2 vs Step 6 distinction.** The straw-man has a single "Decomposition" node. The procedure has Step 2 (object decomposition into axes/families) AND Step 6 (multi-scale decomposition — different cognitive operation). These are not the same.
- **Step 7-modeA vs Step 7-modeB distinction.** The straw-man "Trajectories" elides the split. Step 7 fires twice: mode A in branching_roadmap_engine emits outside-frame trajectories; mode B in frame_validator cross-checks. This is structural anti-monoculture (multi-method per concern).
- **Step 8 stage-gated roadmap as separate from Step 7 trajectories.** Step 7 emits trajectories; Step 8 stages them into a continuation-gated roadmap. The straw-man's "Trajectories" elides the staging step.
- **Step 10 operative/theoretical separation.** The straw-man has "Recommendation" between Governance and Memory. In the procedure, Step 10 is operative/theoretical separation — NOT a recommendation. The procedure does not produce recommendations; it produces a separation of what may be acted on (operative) from what remains theoretical/partial.
- **Step 11 capacity_change tracking.** The straw-man's "Memory" elides Article VII content. The procedure's Step 11 records judgment_act + pattern_engaged + capacity_change — the substrate for Article VII compositional reuse cross-case.

### C5.3 The honest user-visible journey vs the internal procedure

The internal procedure has 11 steps. A user-visible journey at V1 does NOT need to surface 11 distinct screens or 11 distinct interactions. It needs to surface the substrate behaviour the operator must engage with.

**Honest user-visible journey at V1 (CLI / minimal UI):**

1. **Submit case** (input frame).
2. **Receive frame verdict** (Step 1 verdict + Step 3 assumptions visible).
3. **Engage with decomposition** (Step 2 axes/families + Step 6 multi-scale visible; this is where the operator must actually look at the structure).
4. **Engage with hypotheses + their refutation conditions** (Step 4 + Step 5 visible — equal weight to distinguishing_prediction and fails_if).
5. **Engage with outside-frame trajectories** (Step 7-modeA visible; Step 7-modeB cross-check status visible as governance signal).
6. **See the stage-gated roadmap** (Step 8 visible).
7. **Receive the verdict + uncertainty sources** (Step 9 visible with full prominence).
8. **See the operative/theoretical separation** (Step 10 visible — pending refuse-halt adjudication).
9. **See the memory event entries** (Step 11 visible — pending operationalisation; in alpha the JSONL trail is the artefact).

**Should the user-visible journey mirror the internal procedure 1:1?**

**Mostly yes; with two structural compressions:**

- Step 7-modeA and Step 7-modeB should be presented as ONE "outside-frame trajectory analysis with governance cross-check" view, not two separate steps. The cross-check is a structural anti-monoculture defence; the operator does not need to see two screens but does need to see whether the cross-check passed.
- Step 8 (stage-gated roadmap) should be co-located with Step 7 in the trajectory view, as continuation_gates are properties of trajectories.

**Step 9 must be presented as its own screen with full prominence.** The verdict is the load-bearing communication object; compressing it visually risks the governance opacity failure mode (§C7.2).

**Step 10 must be presented separately from Step 9** — pending refuse-halt adjudication. If the operator adjudicates Position B (Step 10 runs even on refuse), the separation between Step 9 verdict and Step 10 operative/theoretical decision must be visible. Collapsing them would compress the very distinction Article IV requires.

**Step 11 must not be a screen at all in V1.** Memory events are persistence-layer artefacts; the operator audits them via JSONL trail or (at V2+) via cross-case dashboard. Surfacing Step 11 as a UI screen at V1 would be over-ceremonialization (the doctrine in CLAUDE.md "feedback_avoid_over_ceremonialization") since the content-pass is not currently operational.

### C5.4 Conclusion on user journey

The straw-man is approximately right at the high level (Question → Frame → Decomposition → Hypotheses → Trajectories → Governance → Memory) but elides the internal distinctions that operationalise Articles II + III + IV + V + VI + VII at the procedure level. A user-visible journey honest to the procedure must NOT compress Step 9 / Step 10 / Step 11 into a single "Recommendation" + "Memory" tail.

**The user-visible journey and the internal procedure should be CLOSE BUT NOT IDENTICAL.** The procedure has 11 steps; the V1 user-visible journey has approximately 7 surfaces (1: submit; 2: frame verdict + assumptions; 3: decomposition; 4: hypotheses; 5: trajectories with governance cross-check + stage-gated roadmap; 6: verdict + uncertainty; 7: operative/theoretical, pending refuse-halt adjudication). Memory is audit infrastructure, not a journey screen.

---

## C6. Productisation roadmap

The audit is **non-expansionary**. This roadmap names what each phase would look like *if* productisation proceeds, with explicit evidence-prerequisites, not time-prerequisites.

### C6.1 V1 — Minimum communication layer

**User experience:** CLI + minimum text UI rendering Step 1–9 outputs. Read-only after submit; no editing of step outputs. Operator submits a case JSON, sees a structured per-step output trail, reads Step 9 verdict, exits.

**Media types (per §C3 classification):**
- Governance alerts (INDISPENSABLE).
- Decomposition cards (USEFUL).
- Hypothesis cards (USEFUL).

**Complexity level:** very low. The substrate (per-step JSON outputs from the existing alpha runner) is unchanged. The V1 layer is a translation layer — JSON → text/HTML rendering. No new components; no new schemas; no new closed-set members.

**Engineering implications:** small. ~500–1,000 LoC for a text-renderer (CLI) and ~1,500–2,500 LoC for a minimal HTML view (web). No new dependencies on LLM cognition (the renderer is deterministic).

**Prerequisite EVIDENCE (not time):**
- E.2 live-replay completes at structural similarity ≥0.83 across the 3 reference cases.
- No architectural regressions surface in live mode (i.e., closed-set vocabulary drift detected by IC-style validators stays at zero).
- Refuse-halt question adjudicated by operator (Position A or Position B chosen; Step 10/11 path decided).

V1 ships when those three conditions hold. It does not ship "in N weeks"; it ships when the evidence is in.

### C6.2 V2 — Structured exploration layer

**User experience:** V1 + cross-case dashboard. Operator can submit a case, see its trace, AND see how its outputs relate to prior cases — which axes recur, which hypothesis shapes recur, which uncertainty sources recur. This is the surface that operationalises Article VII at the UX level.

**Media types:**
- All V1 surfaces +
- Decision maps (USEFUL).
- Trajectory maps (USEFUL).
- Uncertainty dashboards (USEFUL).
- Executive briefs as opt-in only (OPTIONAL).

**Complexity level:** moderate. The cross-case dashboard requires the MemoryLogger Step 11 content-pass to be operational (judgment_act / pattern_engaged / capacity_change emitting). It requires problem-shape fingerprinting (informal at v0.1 — the 3 cluster labels A/B/C in the cases).

**Engineering implications:** moderate. Cross-case state replay (v0.2 scope per long-range roadmap) is prerequisite. Pattern-emergence / pattern-refutation tracking per Article VII benchmark requirements.

**Prerequisite EVIDENCE:**
- V1 in operator use with ≥10 cases run.
- Step 11 content-pass operational (judgment_act / pattern_engaged / capacity_change entries emitted on >0% of cases).
- MemoryLogger compositional-reuse detection works cross-case (per §8.2 of `elif_v0_1_what_remains.md` — currently the alpha does NOT run cross-case state replay; this is v0.2 acceptance scope).
- Article VII benchmark requirements partially satisfied: time-to-arbitration trend across cases shows N+1 ≤ N for similar-shape problems; compositional reuse frequency >0.

### C6.3 V3 — Advanced decision room

**User experience:** V2 + multi-operator engagement with a case. The decision room is where multiple operators (or operator + advisors) engage with the SAME case's decomposition and hypotheses concurrently, with explicit roles (one frames; another adjudicates; another logs operative/theoretical separation). The room preserves Article V refusal-capability — any participant can refuse — and Article III decomposed-reasoning — operations track per-participant.

**Media types:**
- All V2 surfaces +
- Multi-participant decomposition card (USEFUL; new surface).
- Multi-participant hypothesis card (USEFUL; new surface).
- Per-participant uncertainty-source contribution (USEFUL).

**Complexity level:** substantial. Multi-operator infrastructure imports a new failure-mode surface (one operator dominates decomposition; one operator's framing absorbs others; the "consensus" weaponises Article VI coherent-convergence into convergence-theater). Defences must be explicit.

**Engineering implications:** substantial. Authentication, per-participant attribution, conflict-resolution for divergent surface assumptions, audit trail across participants.

**Prerequisite EVIDENCE:**
- V2 in stable use with ≥30 cases run by single operator.
- Article VII capacity accumulation observable cross-case (faster arbitration on similar-shape problems demonstrably faster).
- Failure-mode #32 (Pattern dogmatization) NOT firing — the operator has demonstrated they can refute previously-blessed patterns when new evidence requires it.
- New operator demand surfaced (this is a substrate prerequisite — multi-operator infrastructure should not be built for a solo operator).

**SPECULATION, labelled:** V3 may never ship. If the operator remains solo through the lifetime of the project, V3 is a category error — building multi-operator infrastructure for a single-operator system. The non-self-propagation constitutional anchor (memory note `momentum_capture_warning`) applies: ELIF must not "want" more operators in order to justify V3.

### C6.4 V4+ — Possible simulation / world-model integration

**Cross-audit dependency:** simulation integration belongs to Audit A (World Models). Audit C does NOT pre-empt the integration question. If world-model integration is pursued (operator decision), the communication surface for simulation outputs is the V4+ scope.

**Honest reading:** all V4+ details deferred to Audit A. The cross-cutting signal from C to A: any simulation outputs must respect the same epistemic-discipline + frame-humility + refusal-capable Articles that govern current ELIF outputs. A simulation surface that produces high-confidence predictions without uncertainty sources would be doctrine-violating regardless of how compelling the simulation is.

**Prerequisite EVIDENCE:**
- V3 operational (or V2 sufficient if operator remains solo).
- Audit A positions simulation as substrate ELIF should consume (not as substrate ELIF should become).
- Operator decision on simulation integration — adoption requires explicit doctrinal review at the level of v0.4 Article scope.

### C6.5 Phase-to-evidence map (consolidated)

| Phase | Required evidence | Currently held? |
|---|---|---|
| V1 | E.2 live-replay ≥0.83; no regressions; refuse-halt adjudicated | E.2 authorised, not yet run; refuse-halt pending |
| V2 | V1 in use ≥10 cases; Step 11 content-pass operational; cross-case state replay (v0.2 scope); Article VII capacity-accumulation evidence | None held |
| V3 | V2 stable ≥30 cases; failure-mode #32 NOT firing; new operator demand | None held; multi-operator demand SPECULATION |
| V4+ | V3 stable OR V2 stable with solo operator; Audit A simulation positioning; explicit doctrinal review | None held |

The honest reading: V1 is one operator-decision + one E.2 run away. V2 is v0.2 acceptance scope + operator engagement. V3 is far. V4+ is genuinely speculative.

---

## C7. Communication risks

For each named risk: the failure mode it triggers (four-pole taxonomy + roadmap failure modes 31–39 where applicable), what must be ACTIVELY prevented, what early-warning SIGNAL would indicate it is occurring (measurable, not aesthetic).

### C7.1 Information overload

**Failure mode triggered:** Fragmentation (perpetual decomposition). Surfaces in the four-pole taxonomy as the failure mode Article VI addresses.

**Active prevention:** the V1 user-visible journey is bounded at approximately 7 surfaces (per §C5.3). Adding additional surfaces requires explicit doctrine revision. Cross-case dashboard at V2+ is opt-in, not default.

**Early-warning signal (measurable):** operator-elapsed-time-on-decomposition-screens divided by operator-elapsed-time-on-verdict-screens. If verdict-screen time approaches zero (operator skipping past decomposition to verdict), the surfaces are inviting verdict-shopping. Specifically: if mean time-on-decomposition < 30% of mean time-per-case across ≥10 cases, the V1 UI is failing.

### C7.2 Governance opacity

**Failure mode triggered:** False closure (premature termination, masked by procedure). Articles V + VI direct concern.

**Active prevention:** Step 9 verdict + uncertainty sources must be surfaced with full prominence. The unresolved_uncertainty_sources list cannot be collapsed behind a "details" click; the schema-required minItems=1 must be UI-required minItems=1 visible.

**Early-warning signal (measurable):** count of operator-actions-taken after a refuse-verdict that DO NOT engage with the listed uncertainty sources. If operators consistently act despite refuse-verdicts without referencing the surfaced uncertainty (i.e., the verdict is rendered but ignored), the verdict has become opaque-by-being-decorative. Specifically: if ≥20% of operator post-verdict actions across ≥10 cases ignore the unresolved_uncertainty_sources list, the governance surface is failing.

### C7.3 Procedural inflation

**Failure mode triggered:** Roadmap-as-prestige (#39 in the v0.4 risk register, applied to the procedure rather than the roadmap).

**Active prevention:** the 11-step procedure is locked at v0.1; expansion requires evidence at v0.2+ that a structurally distinct procedural step is required (per the iteration-discipline rule, the trajectory should bend toward compression, not addition). Surfaces should NOT duplicate procedural steps — one screen per procedural concern.

**Early-warning signal (measurable):** if any V1+ UX iteration proposes adding a step to the procedure (vs. exposing an existing step more visibly), audit against the v0.4 iteration-discipline rule. Specifically: any proposal for a Step 12 must be refused unless cases 2–3 surface a structurally distinct failure mode not covered by the four-pole taxonomy (per v0.4 lock).

### C7.4 False confidence

**Failure mode triggered:** Absolutization. Articles I + III + IV direct concern. Risk 23 in the v0.4 risk matrix (capacity framed as truth approach).

**Active prevention:** every Step 9 verdict carries confidence_qualifier + unresolved_uncertainty_sources — schema-enforced. Every Article VII pattern_engaged event must be presented as INVITATION TO TEST, not VALIDATION (per v0.4 "How to apply" anchor: "When pattern recognition output is framed as 'this is true,' refuse and cite 'recognition = invitation to test, not validation'").

**Early-warning signal (measurable):** linguistic audit of operator-facing copy. Any UI text that reads "the answer is" or "the right decision is" or "based on prior patterns, this is" without explicit refutation framing is doctrine-violating. Specifically: ≥0 occurrences of unhedged claim-language permitted in V1 copy; if even one slips in, the copy is failing.

### C7.5 "ELIF theater"

**Failure mode triggered:** Sterile equilibrium. Article VII direct concern. Risk 26 in the v0.4 risk matrix (generative pressure becomes "appear capable" optimization).

**Active prevention:** every visible surface must trace to substrate behaviour. Surfaces that exist only for aesthetic mass — pretty rendering of empty content, animated transitions with no semantic content, "AI is thinking..." spinners — are structurally rejected on cognitive density doctrine grounds.

**Early-warning signal (measurable):** per-surface substrate-anchor audit. Every V1 UI element must be traceable to a specific Article or schema field. The signal is binary: if a UI element cannot be named as `serves Article X via schema field Y`, it is theater. Audit cadence: at every UI iteration; threshold for action: any single un-anchored element.

### C7.6 Over-visualisation

**Failure mode triggered:** Same as ELIF theater (sterile equilibrium) with a specific sub-mode: visualisation as substitute for engagement.

**Active prevention:** the §C3 media taxonomy is closed-set. Adding a visualisation type requires the same closed-set discipline as adding an Article — explicit operator approval + doctrine revision. The 11 candidate media types in §C3 are the audit's closed set; nothing else passes the gate without explicit revision.

**Early-warning signal (measurable):** ratio of LoC in rendering layer to LoC in substrate layer. Currently the alpha is 8,424 LoC of substrate + 0 LoC of rendering. At V1, the rendering layer should be a small fraction of substrate LoC (target: rendering ≤ 0.3 × substrate). If rendering LoC exceeds substrate LoC, the system has become a rendering platform with an arbitration backend.

### C7.7 Excessive media production

**Failure mode triggered:** Captured roadmap (#39). Risk 26 (generative pressure becomes "appear capable" optimization).

**Active prevention:** ELIF does not produce media in the OSG sense (atoms, capsules, scenarios, companions). At every productisation phase, the surfaces are operator-facing translations of existing schema-validated outputs — not new artefacts to amortise at scale.

**Early-warning signal (measurable):** number of distinct media artefact types ELIF produces. At v0.1 alpha: structured-output JSONs (per step) + RunReport + MemoryLogger JSONL. Three artefact families. At V1: same three families + rendered HTML/text surface. If ELIF starts producing a fourth distinct artefact family (e.g., "narrative briefings" as their own type rather than rendered translations), the trajectory has drifted.

### C7.8 Educational contamination from OSG

**Failure mode triggered:** Frame humility violated (II) + partiality of models violated (IV). The contamination is doctrinal not procedural: OSG's pedagogical framing assumes a learner who does not know and must be taught; ELIF's framing assumes an operator who knows the domain and is seeking arbitration on a bundled question. Importing pedagogical framing into ELIF outputs would re-frame the operator as a learner, which collapses the engagement Articles II + III + IV require.

**Active prevention:** explicit copy-review discipline against pedagogical framing. No "let's learn together" copy. No "here's what you need to know" copy. No "5 things you should consider" copy. The voice is arbitration-trace, not tutorial.

**Early-warning signal (measurable):** copy-style audit. The audit is linguistic: pedagogical verbs (learn / understand / master / remember) vs. arbitration verbs (decompose / refute / arbitrate / refuse / surface). If pedagogical verbs appear at >10% of total verb count in operator-facing copy, the framing has drifted.

A second signal: the OSG atom library closed-set (14 domain categories) is pedagogical. If ELIF starts categorising its outputs by pedagogical domain rather than by problem-shape, the contamination has reached the substrate layer.

---

## Transferability matrix summary

| OSG structure | Classification | Article / behaviour served | Honest transfer cost |
|---|---|---|---|
| Limova framework | NON-TRANSFERABLE | none | belongs to pedagogy |
| Gemini media generation | NON-TRANSFERABLE (organ); capability redundant with `llm_adapter.py` | none directly | architectural inflation if imported |
| Atom generation pipeline | TRANSFERABLE WITH MODIFICATION | Article VII (compositional reuse) | heavy; ~ equivalent to building from scratch under new semantics |
| Companion architecture | NON-TRANSFERABLE | none | no learner-facing bundle analogue |
| Concept explainers | NON-TRANSFERABLE | none directly | operator is not a learner |
| Scenario library (8 shapes) | NON-TRANSFERABLE in content; discipline already shared | closed-set discipline (Article VII) | no transfer; ELIF already uses pattern |
| Cognitive density doctrine | TRANSFERABLE WITH MODIFICATION (doctrine, not code) | Article V dual; cognitive-density-as-anti-theater | one paragraph |
| Friction-preserving learning structures | TRANSFERABLE WITH MODIFICATION (doctrine, not code) | Articles II + III + IV | one paragraph + UX commitment |
| Narrator library | NON-TRANSFERABLE | none | no audio output |
| Atom library (14 domains) | NON-TRANSFERABLE in content; discipline already shared | closed-set partition (Article VII) | no transfer; ELIF already uses pattern |
| Shell propagation engine | NON-TRANSFERABLE | none | no jurisdiction-bound lexicon to substitute |
| 34-observer media biome registry | NON-TRANSFERABLE in content; discipline (observer-first + state machine) shared | Article VII anti-sterile-equilibrium | discipline transfer only |
| State machine | TRANSFERABLE WITH MODIFICATION (if/when ELIF observers exist) | Article VII substrate | ~250 LoC under ELIF semantics |
| Halt actions (8 + exclusivity) | TRANSFERABLE WITH MODIFICATION (single-carrier exclusivity discipline) | Articles V + VI | ~100 LoC; CURRENT EVIDENCE shows runner halts cleanly already |
| Micro-video chaining doctrine | TRANSFERABLE WITH MODIFICATION (doctrine, not code; engagement-theater warning) | Articles V dual + III | one paragraph |

**Aggregate verdict:**
- 3 of 15 structures TRANSFERABLE WITH MODIFICATION as code (atom generation pipeline conceptually, state machine, halt actions) — and all three carry caveats requiring substrate that does not currently exist.
- 4 of 15 TRANSFERABLE WITH MODIFICATION as doctrine only (cognitive density, friction-preserving, observer-first discipline, micro-video doctrine).
- 8 of 15 NON-TRANSFERABLE (Limova, Gemini, companion, concept explainer, scenario library, narrator library, atom library, shell propagation).

The honest summary: **the OSG media biome transfers as governance grammar, not as media substrate.** The grammar (closed-set, observer-first, state machine, hibernation, partial-credit, refusal-capability) is already operating in ELIF v0.4 via different code. The media substrate (atoms, capsules, narrators, companions, shells) does not transfer because the receiving organ is structurally different (arbitration vs. pedagogy).

---

## Operator decisions queued

The audit surfaces, for operator deliberation under v0.4 doctrine, the following decisions. None are recommendations; each is a decision-shape with its trade-offs surfaced honestly.

### OD-C-1. Refuse-halt position (architectural-but-localized)

Per `elif_v0_1_what_remains.md` §3 and `elif_v0_1_alpha_replay_report.md` operator-decision-points-surfaced: should Step 10 + Step 11 run on `verdict=refuse`?

- **Position A (status quo):** Article V refusal-capability halts downstream reasoning. Step 10 + Step 11 not exercised on refuse-path; alpha 17% structural gap remains; Article VII content-pass not operationalised in current alpha runs.
- **Position B (reference-matching):** Step 10 + Step 11 run as post-refusal closure; structural similarity rises to ~1.0 against reference; Article VII content-pass becomes operational; V2 cross-case dashboard becomes substrate-ready.

This audit's reading: Position B is the necessary path for V2 productisation per §C6.2 (V2 requires Step 11 content-pass operational). But this audit does NOT advocate adoption; the operator must adjudicate on doctrinal grounds (which reading of Article V is honest). This audit cannot make that call.

### OD-C-2. V1 ship gate

If V1 is to be built, the gate is the three-condition evidence requirement in §C6.1:
- E.2 live-replay ≥0.83
- No architectural regressions in live mode
- OD-C-1 adjudicated

Operator decision: do those three constitute a sufficient ship-gate, or are additional conditions required? This audit proposes the three as the minimum honest gate; the operator may add (never subtract).

### OD-C-3. V2 cross-case dashboard scope

If V2 is to be built, the scope question is: which cross-case patterns are surfaced? The risk is sovereignty re-import via the dashboard (risk 23 in v0.4 risk matrix). This audit's reading: the dashboard surfaces frequencies (which axes recur, which uncertainty-sources recur, which hypothesis-shape patterns recur) WITHOUT computing "prediction strength" or "pattern confidence" — the surface presents counts, not predictions. Operator decision: does this constraint hold, or does the dashboard need more / less / different metrics?

### OD-C-4. V3 as substrate question (not as roadmap question)

Operator decision: is multi-operator demand a real substrate (other operators exist who want to use ELIF on shared cases) or a roadmap projection (a category to fill on a roadmap document)? If the latter, V3 is structurally rejected on the non-self-propagation constitutional anchor. This audit does not project V3 demand; the operator alone can know.

### OD-C-5. Surface-LoC budget

Operator decision: what fraction of total project LoC should rendering layer represent? This audit's reading: rendering ≤ 0.3 × substrate is a defensible bound under the cognitive density doctrine. Operator may set tighter or looser. The decision becomes the audit anchor for §C7.6 over-visualisation early-warning signal.

---

## What this audit does NOT recommend

This section is load-bearing for the non-expansionary stance.

1. **This audit does NOT recommend building V1.** V1 is a candidate phase whose gate (§C6.1) is the three-condition evidence requirement. The audit names the gate. The decision to walk through it is the operator's.

2. **This audit does NOT recommend importing any OSG media biome substrate as code.** Per §C1 transferability matrix, 8 of 15 structures are NON-TRANSFERABLE and the rest transfer as doctrine more than as code. Anyone proposing to "lift the atom library into ELIF" or "give ELIF a companion architecture" should be referred to §C1.3 and §C1.4 first.

3. **This audit does NOT recommend adding any V2/V3/V4 surfaces beyond those §C3 classifies as INDISPENSABLE or USEFUL.** Audio briefings, video explainers, scenario trees are explicitly DECORATIVE and structurally rejected.

4. **This audit does NOT recommend adding a 12th procedural step.** Per v0.4 iteration-discipline rule, the trajectory bends toward compression. Procedural inflation (§C7.3) is a named failure mode.

5. **This audit does NOT recommend importing Gemini-the-organ.** Per §C1.2 and §C4.2, the cognition capability is already in `llm_adapter.py`. Importing Gemini-the-organ is architectural inflation.

6. **This audit does NOT recommend a separate ELIF Article on communication or media.** The Constitutional Layer is locked at v0.4 with explicit iteration-discipline. A communication-focused Article VIII is exactly the kind of additive iteration the lock forbids without evidence of a structurally-distinct fifth failure mode.

7. **This audit does NOT recommend resolving the refuse-halt question on this audit's authority.** OD-C-1 is the operator's adjudication, not the audit's.

8. **This audit does NOT recommend a productisation timeline.** Phases are gated on evidence (§C6.5), not on calendar. Naming a calendar date would be a doctrinal violation (momentum-capture warning).

9. **This audit does NOT recommend any cross-organ coupling between ELIF and OSG runtime.** Four-organ separation in OSG and the analogous discipline in ELIF v0.4 both forbid this.

10. **This audit does NOT recommend treating the §C3 media taxonomy as exhaustive.** The taxonomy is closed-set under audit scope. Expansion requires the same explicit operator approval + doctrine-revision discipline as any other closed-set in the project.

---

## Cross-cutting signals to other audits

- **To Audit A (World Models):** simulation views (§C3.8) and V4+ communication surfaces for simulation outputs (§C6.4) are deferred to A. A's positioning on simulation-as-substrate-ELIF-consumes vs. simulation-as-substrate-ELIF-becomes will determine whether the V4+ communication question is well-formed at all. C asks A to anchor simulation outputs to the same epistemic-discipline + frame-humility + refusal-capable Articles that govern current ELIF outputs.

- **To Audit B (User Experience):** the §C5 user-journey audit (V1 ~7 surfaces; not 1:1 with 11 steps) and the §C7 risk register (information overload / governance opacity / "ELIF theater" / over-visualisation) are direct inputs to B's UX positioning. B should treat §C5.3 as a substrate-anchor and §C7 as the failure-mode register for any UX design proposal.

- **To Audit B:** the §C2 finding that ELIF communicates an *arbitration trace, not knowledge*, is load-bearing for any UX proposal. If B's UX positioning frames ELIF outputs as "decisions delivered" or "advice given," it imports the OSG-style framing that C explicitly rejects (§C7.8 educational contamination).

- **To Audit A:** the §C1 transferability matrix (specifically C1.3 atom generation, C1.13 state machine, C1.14 halt actions) names which OSG governance grammar transfers to ELIF and which does not. A's positioning of world models as substrate ELIF interfaces with should reference the same transferability framing — what transfers as grammar vs. what transfers as code.
