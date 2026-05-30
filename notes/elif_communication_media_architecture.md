# ELIF Communication & Media Architecture — Operator-Facing Consolidated Reference

> **Captured:** 2026-05-30
> **Priority ID:** P6_Comm (ELIF 100-hour Sprint)
> **Consolidates:** Audit B (UX positioning) + Audit C (Media/communication) into one operator-facing document.
> **Status:** Non-expansionary. Evidence-gated. No new component, no new Article, no new procedure step, no roadmap expansion, no v0.5.
> **Authority:** Distillation only. Cannot resolve operator decisions; cannot reweight audit findings; cannot introduce framings not present in B or C.
> **Doctrine constraint:** capacity-vs-truth at Article VII; preserve-over-chase; closed-set discipline; momentum-capture warning; four-organ separation; non-self-propagation; rendering-layer LoC ≤ 0.3 × substrate LoC.
> **Epistemic registers used:** CURRENT EVIDENCE / PLAUSIBLE FUTURE / SPECULATION. Where the surrounding paragraph header carries them they are not repeated per claim.

---

## 1. Operator-Facing Summary (load-bearing one-pager)

**ELIF's communication object is an arbitration trace with explicit refutation conditions on every claim it makes, addressed to a single operator, inviting judgment engagement — not knowledge, not advice, not entertainment, not consumption.** Across Audit B (UX positioning) and Audit C (media/communication), three independent lines of pressure converge on the same conclusion: the structured per-step output IS the deliverable; the user-visible surface is a small rendering of that structured output anchored to specific Articles and schema fields; the operator's role is to engage decomposition, weigh hypotheses against their `fails_if` conditions, and accept or refuse a governance verdict whose own refutation conditions (`unresolved_uncertainty_sources` ≥ 1) are explicit. Every productisation step downstream — V1 case viewer, V2 cross-case dashboard, V3 multi-operator room (if it ever opens), V4+ simulation interface (if it ever opens) — is gated on this single substrate-anchored discipline: every UI element traces to one Article and one schema field, or it is theater (Audit C §C7.5). This is the operator-quotable claim of the document.

---

## 2. Decision-Room Communication Model (per-case surface)

**Communicative posture.** The decision-room surface is the operator-facing expression of one case. The communication object is **the arbitration trace produced by Steps 1–9 (and Steps 10–11 if Position B is adopted at Gate G0)**, not knowledge about the bundle being arbitrated. Audit B §B1.3 names the archetype as LOAD-BEARING — the single closest fit to what the alpha actually does. Audit C §C5.3 names the same surface under a substrate-anchored vocabulary ("user-visible journey"). The two vocabularies coexist: B's "decision room" is operator-facing; C's "user-visible journey" is doctrinally precise. The synthesis (Audit Synthesis §2.5) accepts both.

**Receiver.** A single operator. Multi-operator engagement is Phase 9 in the synthesis roadmap and SPECULATION per Audit C §C6.3; it is not a V1 / V2 communication target.

**Action invited.** Judgment engagement, not consumption. The room is a place the operator ENTERS to do work and LEAVES when the case closes (Audit B §B1.3). The pausability test (Audit B §B4.5) is binding at every version: the room must be exitable mid-flight without state-rebuild on re-entry.

**The 7–8 user-visible surfaces inside the decision room.** Audit B §B3.4 enumerates 8 user-visible stages over 11 internal steps; Audit C §C5.3 compresses to approximately 7 surfaces (Step 7-A + 7-B + Step 8 collapsed into one trajectory + governance-cross-check + stage-gated-roadmap view). Both compressions are doctrinally defensible (Audit Synthesis §2.1). The list below names each surface by what it communicates, anchored to the Article(s) it serves.

| # | Surface (B-naming) | Internal Step(s) | Communication purpose | Article anchor |
|---|---|---|---|---|
| 1 | **Question** (input frame authoring) | Step 0 (external) | The operator commits a bundled question to the room as a schema-valid InputFrame. | II (Frame Humility); the act of committing is the first frame-humility surface. |
| 2 | **Frame Validation** | Steps 1, 3, 7-mode-B | A schema-validated verdict ∈ {valid, invalid, needs_decomposition} on the operator's framing + surfaced assumptions + outside-frame BRE governance cross-check status. | II + V (refusal-capable framing rejection). |
| 3 | **Axis Decomposition** | Steps 2, 6 | A closed-set-typed enumeration of ≥2 axes with ≥2 families per axis + multi-scale relations between axes. Renders the structure of the question the operator thought they asked. | III (Decomposed Reasoning) + IV (Partiality of Models). |
| 4 | **Hypothesis & Failure Conditions** | Steps 4, 5 | The hypothesis set, each carrying `distinguishing_prediction` AND `fails_if` rendered with equal weight. Hiding `fails_if` behind a click is doctrine-violating (Audit C §C3.5). | I (Epistemic Discipline) + III. |
| 5 | **Outside-Frame Alternatives (with governance cross-check) + Stage-Gated Roadmap** | Steps 7-A, 7-B, 8 | Outside-original-frame trajectories T1–T4 (or whatever the case emits) + the runner's anti-monoculture cross-check status + the continuation-gated staging that turns each trajectory into a refusable pathway. | V + VI + VII. |
| 6 | **Governance Verdict** | Step 9 | `{verdict, verdict_detail?, confidence_qualifier, unresolved_uncertainty_sources}` with `verdict ∈ {constrain, refuse, explicitly_abstain}` and `minItems=1` on uncertainty sources, surfaced with full prominence. The load-bearing output of the system. Audit C §C3.3 names this INDISPENSABLE. | V + VI + VII; Article I structurally enforced via mandatory uncertainty source. |
| 7 | **Actionable / Theoretical Split** | Step 10 | The operative-list / theoretical-list / optional absence_log. PENDING refuse-halt adjudication (Gate G0). In V1 under Position A the surface records the refusal event via the `refutation` event type only. | IV (Partiality of Models). |
| 8 | **Case Closure** | Step 11 | The closure record: "this case has been written; pattern X was engaged; capacity-change Y was logged." Surfaced as a closure affirmation, NOT as analytics. In V1 the JSONL trail IS the artefact; per Audit C §C5.3 this is NOT a V1 screen, it is audit infrastructure. | VII (Generative Reconstruction) directly. |

**The compression option (Audit C §C5.3 — 7 surfaces).** Audit C collapses surfaces 5 above into one trajectory-with-governance-cross-check + stage-gated-roadmap view, and treats Step 11 as persistence-layer infrastructure not as a screen. Either compression is doctrinally defensible; the operator selects at V1 design time (G2 family decision per Synthesis §3).

**What this surface MUST NOT do** (Audit B §B3.6 + §B-non-rec 4 + 8 + Audit C §C7.5):
- Must not collapse the refuse-verdict into a generic "failed" / "blocked" / "error" state. Refuse is the architecturally-correct verdict in all 3 alpha cases; `exit_code=20` is success in the architectural sense.
- Must not invite re-execution loops ("try a different frame and see what happens"), "tweak the prompt to fix the verdict" affordances, or free-form exploration sandboxes.
- Must not wrap any panel in LLM-prose summarization ("explain this verdict in plain language") — this re-imports the chatbot archetype Audit B §B1.1 names as ACTIVELY COUNTERPRODUCTIVE.
- Must not render any element that does not trace to `serves Article X via schema field Y` (Audit C §C7.5 binary test).

---

## 3. Laboratory Communication Model (cross-case surface)

**Communicative posture.** The laboratory surface is the operator-facing expression of the cross-case corridor of prior rooms. The communication object is **capacity-vs-truth observability + pattern-engagement counts + deprecation events**, derived as a stateless read over the append-only MemoryLogger JSONL. Article VII (capacity-vs-truth) is the load-bearing anchor: capacity accumulates and is observable; truth does not accumulate and must remain structurally unrepresentable in the surface. Audit B §B2.9 names the laboratory mode LOAD-BEARING for cross-case work; Audit C §C6.2 names the equivalent surface as the V2 cross-case dashboard. The Synthesis §1.6 confirms these are three names for the same substrate: the laboratory archetype (B) = the cross-case dashboard (C) = the Article VII content surface (A's anti-drift concern).

**Receiver.** The same single operator. Multi-operator laboratory framings are Phase 9 SPECULATION; not in scope for V1–V2 under the non-self-propagation constitutional anchor.

**Action invited.** Judgment engagement on patterns. The operator inhabits the laboratory between cases (paused state) and inhabits a decision room during a case (active state). Pattern recognition is rendered as "shape recognized; INVITATION TO TEST" — never as "answer" or "validation" (Audit B §B4.3; Audit C §C7.4 early-warning).

**Article VII anchoring (load-bearing).** Article VII's operational meaningfulness depends on its observables being inspectable. A non-rendered MemoryLogger satisfies the persistence requirement but not the longitudinal-observation requirement that distinguishes capacity-watching from prestige-accumulating. The laboratory surface IS the operationalization of Article VII at the UX level — and equally importantly, the surface that makes "ELIF has accumulated capacity" empirically visible AND makes "ELIF has been accumulating TRUTH" empirically detectable as the failure mode it is.

**Laboratory tiles (V2 — only after Phase 5 closes; PLAUSIBLE FUTURE).** Each tile traces to a specific schema field or MemoryLogger event_type / change_type; nothing is added for aesthetic mass.

| Tile | What it renders | Schema/event anchor | Counts not predictions? |
|---|---|---|---|
| Prior-rooms corridor | List of closed cases by shape-tag, with `open` / `close` timestamps. | MemoryLogger `open` + `close` events. | Counts. |
| Pattern panel | Each pattern engaged across cases with engagement count, last-engaged timestamp, and deprecation status. | MemoryLogger `pattern_engaged` change_type. | Counts only; framed as INVITATION TO TEST. |
| Capacity-change log | Per-case capacity-accumulation entries with sign-of-change and qualitative anchor. | MemoryLogger `capacity_change` change_type; Article VII benchmark. | Capacity-observable counts; never truth-shaped. |
| Judgment-act log | Operator-readable record of where rule-underdetermination triggered judgment, what was considered, what was chosen, what consequences followed. The meta-reviewable surface of the thinking-reed. | MemoryLogger `judgment_act` change_type. | Records, not metrics. |
| Uncertainty-source frequency | Aggregated count of unresolved_uncertainty_sources that recur across cases — which kinds of uncertainty recur, which are resolved by accumulated evidence. | Step 9 output `unresolved_uncertainty_sources` arrays summed over cases. | Counts; never confidence scores. |
| Deprecation events | A pattern was deprecated because cases N+2, N+3 refuted it. Rendered as evidence of the system's refutation discipline working. | MemoryLogger `pattern_engaged` entries with deprecation flag. | Events, not rates. |
| Sterile-equilibrium / fragmentation signals | The detector outputs surfaced as inspectable signals, NOT as alerts (no engagement-loop). | MemoryLogger signature-detector outputs (deferred from v0.1 per `elif_v0_1_what_remains.md` §5.3). | Inspectable; not actionable-by-default. |

**What the laboratory surface MUST NOT do** (Audit B §B4.3 non-rec + Audit B §B4.4 + Audit C §C7.4 / §C7.6 / §OD-C-3):
- Must not compute "prediction strength" or "pattern confidence." Counts only. Any tile that aggregates and ranks slips into sovereignty (Article I).
- Must not gamify uncertainty (no dashboard-as-metric-game that turns uncertainty into a number to "track down").
- Must not maintain a leaderboard, hall-of-fame, or "most-engaged-shape" trophy. The system must not have a hall of fame.
- Must not require background processes to keep tiles fresh — every tile must be derivable on demand from the MemoryLogger JSONL. If the surface starts requiring background processes, the architecture has captured itself (momentum-capture failure mode); the pausability test (Audit B §B4.5) FAILS.
- Must not produce any framing that converts pattern recognition into prediction or validation; must not aggregate into a "knowledge base" / "what ELIF has learned" surface (Audit B §B4.4: truth-accumulation framing is forbidden).

---

## 4. Transferability Matrix Summary (from Audit C §C1)

A single consolidated table covering all 15 OSG media structures audited in C §C1. Classes: DIRECT / WITH MODIFICATION / NON-TRANSFERABLE / DOCTRINE-ONLY. Note: Audit C does not use "DIRECT" — no OSG media structure transfers directly as code; the closest is the discipline patterns embedded in halt-actions and state-machine which still require porting under different semantics.

| # | OSG structure | Class | Justification (one sentence) | If transferable: ELIF Article / behaviour served |
|---|---|---|---|---|
| 1 | Limova framework (marketing/distribution organ + 8 assistants) | NON-TRANSFERABLE | Marketing/distribution substrate for many-to-many learner acquisition; ELIF has no learner audience, no broadcast cadence, no acquisition workflow. | — |
| 2 | Gemini media generation layer (script + cognition organ) | NON-TRANSFERABLE (as organ); capability redundant | Gemini-as-organ is structurally redundant with ELIF's existing `llm_adapter.py` (279 LoC) — importing it is architectural inflation. | — (capability already present) |
| 3 | Atom generation pipeline (generate → IC/AV → canonical-promote → register-by-hash → reuse) | WITH MODIFICATION | The pipeline shape (hash-pinned, closed-set-typed, reusable artefacts) maps onto Article VII compositional reuse — but the modification is heavy enough that transfer is roughly equivalent to building from scratch under new semantics (no "canonical" naming permitted under Article I; needs `pattern_invitation_status` instead). | Article VII (Generative Reconstruction) directly. |
| 4 | Companion architecture (per-formation pedagogical artefact bundle) | NON-TRANSFERABLE | Per-learner bundle of typed sub-artefacts; ELIF has no learner-facing bundle. The closest analogue (per-case RunReport + JSONL) is an audit trail of arbitration, not a deliverable bundle — different in kind. | — |
| 5 | Concept explainers (atom_type that teaches a concept to a learner) | NON-TRANSFERABLE | Tutorial framing assumes a learner who doesn't know the domain; ELIF's operator knows the domain and is seeking arbitration. Frame validation surfaces assumptions; that is surfacing, not explaining. | — |
| 6 | Scenario library (8 closed-set shapes — clinical_judgment_triage / ethical_dilemma_resolution / etc.) | NON-TRANSFERABLE in content; DOCTRINE-ONLY for the closed-set-of-shapes discipline | The 8 shapes are pedagogical scenarios — what does a learner DO inside them. ELIF's procedure does not contain scenarios. The closed-set-of-shapes DISCIPLINE is already operating in ELIF v0.4 via different code (closed-set verdict vocabulary, closed-set event_types). No transfer needed. | Article VII pattern-emergence / pattern-deprecation regime (already operating). |
| 7 | Cognitive density doctrine (text-native primary; audio surgical; video narrow; never modality collapse) | WITH MODIFICATION (doctrine-only — one paragraph) | The doctrine itself transfers as the structural defence against pretty-dashboards-eating-judgment-substance ("clarity-without-decomposition = clarity-theater"); concrete OSG metrics (text/audio/video closed-set) do not transfer because ELIF's modality is structured-text-output. | Article V dual + over-visualisation risk (§9). |
| 8 | Friction-preserving learning structures (OSG resists smooth-UX learning-as-consumption) | WITH MODIFICATION (doctrine-only — one paragraph) | The structural commitment maps onto ELIF: a one-click "Get Verdict" button would collapse the procedure into a magic-8-ball; "friction preserves learning" becomes "friction preserves judgment." | Articles II + III + IV directly. |
| 9 | Narrator library (8 NARRATOR_PROFILE_IDS closed-set; voice-routing; tone classes) | NON-TRANSFERABLE | TTS-layer artefact tying voice fingerprints to formations at 1.0 inheritance ratio; ELIF has no audio output, no "voice identity" of arbitration outputs. A soothing voice reading a refuse-verdict is the exact engagement-theater the cognitive-density doctrine forbids. | — |
| 10 | Atom library (14 ATOM_DOMAIN_CATEGORIES closed-set — healthcare_clinical / trades_construction / etc.) | NON-TRANSFERABLE in content; DOCTRINE-ONLY for closed-set-domain-partition discipline | The 14 domain categories partition the pedagogical universe; ELIF cases cluster by problem-shape (the 3 alpha clusters A/B/C), not by pedagogical domain. The closed-set-partition discipline is already shared. | Article VII compositional-reuse substrate (discipline only). |
| 11 | Shell propagation engine (country-aware lexicon substitution US/UK/CA/AU/FR/BE/CH/QC) | NON-TRANSFERABLE | ELIF outputs have no country-specific lexicon to substitute; arbitration shape is invariant under shell. Importing shell-substitution would create a non-load-bearing layer. | — |
| 12 | 34-observer media biome registry (4 acquisition + 8 MV + 8 LIM + 5 GEM + 5 AUD + 4 XO; all DORMANT) | NON-TRANSFERABLE in content; DOCTRINE-ONLY for observer-first + closed-set registry pattern | The 34 observers observe media-side phenomena (publication cadence, voice drift, cognitive fragmentation in micro-videos); ELIF has no publication, no voice drift, no micro-video chains. The observer-first + closed-set discipline is already operating in ELIF via MemoryLogger closed-set event_types and change_types. | Article VII anti-sterile-equilibrium (discipline already operating). |
| 13 | State machine (DORMANT → REVIEW_PENDING → PILOT → SIGNAL_EMIT → HALT_CAPABLE → QUARANTINED → RETIRED) | WITH MODIFICATION (if/when ELIF observers exist) | High-fit pattern for any future ELIF observer infrastructure; not portable as-is because PILOT / SIGNAL_EMIT semantics are media-publication-specific. Port estimate: ~250 LoC under ELIF semantics. PLAUSIBLE FUTURE only — no evidence yet that ELIF needs additional observer infrastructure beyond what schemas + semantic post-validation already enforce. | Article VII enforcement at the substrate level. |
| 14 | Halt actions (8 IDs with single-carrier biome-wide-exclusivity invariant) | WITH MODIFICATION (single-carrier-exclusivity discipline) | The 8 specific halt action IDs are media-publication-bound (HA-PUB-REFUSE / HA-CAPSULE-REJECT etc.); the single-carrier-exclusivity discipline transfers as the structural defence against multiple components fragmenting refusal-authority. ELIF's analogue: at most one component carries run-level halt authority (currently `governance_kernel` at Step 9). | Articles V + VI (refusal-capability + coherent convergence). |
| 15 | Micro-video chaining doctrine (resist chained-clips engagement-theater; completion ≠ retention) | WITH MODIFICATION (doctrine-only — one paragraph; engagement-theater WARNING) | Replace "completion-rate" with "operator-runs-completed-without-engagement-with-decomposition"; replace "30-day-retention" with "subsequent-case-quality-of-decomposition." Identical failure mode: a system that produces well-formed outputs that the operator doesn't engage with becomes a magic-8-ball. | Article V dual (refusal-where-engagement-was-skipped = refusal-theater) + Article III. |

**Aggregate verdict (matches Audit C §C1.16 / Synthesis §1.10):**
- 0 of 15 structures DIRECTLY TRANSFERABLE as code.
- 3 of 15 TRANSFERABLE WITH MODIFICATION as code substrate (atom generation pipeline conceptually, state machine, halt actions) — all three carry caveats requiring substrate that does not currently exist (Step 11 content-pass not operational; no ELIF observer infrastructure shipped; explicit single-carrier invariant code not yet written).
- 4 of 15 DOCTRINE-ONLY (cognitive density, friction-preserving, observer-first discipline, micro-video doctrine).
- 8 of 15 NON-TRANSFERABLE (Limova, Gemini-as-organ, companion, concept explainer, narrator library, atom library content, shell propagation, scenario library content — and the 34-observer registry content itself).

**The honest summary the operator should carry forward:** the OSG media substrate transfers as **governance grammar, not as media substrate**. The grammar (closed-set discipline, observer-first, anti-monoculture, runtime authority separation, four-organ separation) is already operating in ELIF v0.4 via different code. The media code itself does not transfer because the receiving organ is structurally different — arbitration vs. pedagogy.

---

## 5. Media Architecture Summary — Why ELIF Is Fundamentally Different from OSG

**Both projects share doctrinal grammar** (closed-set discipline, observer-first posture, anti-monoculture, runtime authority separation, four-organ separation, preserve-over-chase, validate-before-promote, schema-required structured outputs, no auto-promotion, hibernation periods, memory-blessing rituals). This shared grammar is the substrate that ELIF inherited from OSG at v0.4.

**The artefacts they produce differ in kind.** This is the load-bearing finding of Audit C §C4.3 and is restated here verbatim as the operator-quotable claim of this section.

| Dimension | OSG | ELIF |
|---|---|---|
| Communication object | Knowledge / skills / competency / mastery as pedagogical artefacts. | An arbitration trace with explicit refutation conditions on every claim. |
| Receiver | Many-to-many learner audience. | One-to-one operator audience (V3 multi-operator is SPECULATION and may never open). |
| Action invited | Learning (study, exercise, mastery, transfer). | Judgment engagement (engagement with decomposition; weighing of hypotheses against `fails_if`; accepting / refusing a verdict whose refutation conditions are explicit). |
| Discipline under which it operates | Content-density + acquisition-observability. | Epistemic-discipline + capacity-accumulation. |
| What is amortised across uses | *Content* (an atom reused across formations sharing a domain) and *voice* (a narrator fingerprint reused across formations sharing a language). | *Arbitration shape* (a decomposition pattern reused across cases sharing a problem-shape, if/when Article VII content entries operationalise) and *judgment* (an operative/theoretical separation pattern reused across cases sharing an evidentiary structure). |
| What expansive infrastructure can be built | Atom library, narrator library, scenario library, companion architecture, shell propagation engine, 34-observer pipeline — all defensible at scale because each amortises across thousands of pedagogical surfaces. | Nothing expansive. The structured output IS the deliverable. The rendering layer subordinates to the substrate; rendering LoC ≤ 0.3 × substrate LoC (Audit C §C7.6; Synthesis §1.5). |

**The substrate that transfers is governance grammar.** Specifically:
- Closed-set discipline (verdict vocab, event_types, change_types — all already operating in ELIF v0.4).
- Observer-first discipline (the pattern of building the observer before the layer it observes — already operating in MemoryLogger).
- State-machine discipline (operationalised in OSG as DORMANT → REVIEW_PENDING → ... → RETIRED; transferable as discipline for any future ELIF observer infrastructure that might emerge).
- Hibernation discipline (the cooling period between observer activations — transferable if/when ELIF has observers to activate).
- Partial-credit semantics (the Article VII-aligned framing where pattern recognition is invitation-to-test, not validation).
- Single-carrier halt exclusivity (currently implicit in `governance_kernel` Step 9; transferable as explicit invariant code).

**The substrate that does NOT transfer is the media code itself.** No atom library lift, no narrator library lift, no scenario library lift, no companion architecture lift, no Limova lift, no Gemini-organ lift, no 34-observer registry lift. The §4 transferability matrix lays the substrate down individually; this is the consolidated summary.

**The temptation to refuse repeatedly.** The single most common likely-failure mode the operator will face during V1–V2 development is "why don't we just lift the atom library shape into ELIF? we already have the code." The answer is at §C1.3: roughly equivalent to building from scratch under different names, AND blocked by Step 11 content-pass not being operational, AND blocked by the absence of a problem-shape fingerprint registry, AND blocked by the absence of refutation-condition semantics on the artefact registry itself. The honest move is to defer this work to Phase 5 (MemoryLogger maturation) of the synthesis roadmap and refuse the lift now.

---

## 6. What Transfers from OSG (Itemised)

Each item carries a one-sentence justification matched to its Audit C §C1 entry.

- **Closed-set discipline** — transfers as governance grammar. Already operating in ELIF v0.4 via `_VALID_EVENT_TYPES` + `_VALID_CHANGE_TYPES` + verdict vocabularies; structural-enforcement (import-time `assert_registry_consistent()`-equivalent) is the same shape as OSG's media-biome closed-set sanity gates.
- **Observer-first discipline** — transfers as governance grammar. The pattern "observer exists BEFORE the layer it observes" already operates in MemoryLogger (the persistence shape is built before the content-pass it observes is live); transferable to any future ELIF observer that emerges.
- **State machine pattern (DORMANT → REVIEW_PENDING → PILOT → SIGNAL_EMIT → HALT_CAPABLE → QUARANTINED → RETIRED)** — transfers as governance grammar at process boundaries. Not portable as-is (PILOT / SIGNAL_EMIT semantics are media-publication-specific); portable as ~250 LoC under ELIF semantics IF and only if ELIF develops observer infrastructure beyond schemas + semantic post-validation. PLAUSIBLE FUTURE only.
- **Halt actions with single-carrier exclusivity** — transfers as governance grammar. The 8 specific halt action IDs do not transfer; the single-carrier-exclusivity invariant (at most one component may carry run-level halt authority) is already implicitly present in `governance_kernel` Step 9; making it explicit is ~100 LoC of invariant code.
- **Hibernation discipline** — transfers as governance grammar. The cooling-period-between-observer-activations pattern is transferable IF ELIF develops observer infrastructure to activate.
- **Partial-credit semantics** — transfers as governance grammar. The discipline of NOT awarding full validation for partial pattern recognition maps onto Article VII's "pattern recognition is invitation-to-test, not validation" — same shape, different domain.
- **Anti-monoculture defense** — transfers as doctrine. Already operating in ELIF v0.4 via Step 7's mode-A + mode-B (multi-method per concern at the procedure layer); the doctrine is the structural-commitment-to-method-diversity-per-concern.
- **Cognitive density doctrine** — transfers as ONE-PARAGRAPH doctrinal anchor. Replace text/audio/video closed-set with structured-text-output as primary modality; the structural commitment "every visible output earns its place by surfacing a step's load-bearing content, not by rendering it pleasingly" carries directly.
- **Friction-preserving doctrine** — transfers as ONE-PARAGRAPH doctrinal anchor. Replace "friction preserves learning" with "friction preserves judgment"; structural commitment in any UX design — no one-click "Get Verdict" button; the operator must engage decomposition, hypothesis-with-fails_if, and outside-frame alternatives.
- **Micro-video engagement-theater WARNING** — transfers as ONE-PARAGRAPH warning anchor (what NOT to do). The failure mode "system that produces well-formed outputs that the operator doesn't engage with becomes a magic-8-ball" applies recursively to ELIF; engagement-by-completion-rate-without-decomposition-engagement is the canonical failure shape to refuse.

---

## 7. What NEVER Transfers from OSG (Itemised, with Failure-Mode Naming)

For each: the failure mode (named per Audit C §C7.8 "educational contamination from OSG" sub-categorised) that would fire if the structure were transferred.

- **Limova framework** — pedagogy-specific marketing/distribution organ; does not map onto ELIF's one-to-one operator audience. **Failure mode if transferred:** broadcast-shape posting cadence with no learner audience and no acquisition workflow re-imports the engagement-theater + prestige-accumulation failure modes (Audit B §B2.8 references failure modes #36 institutional capture + #37 prestige accumulation). The system would acquire posting cadence as a maintenance obligation with no substrate behaviour served.
- **Gemini-as-organ media generation** — pedagogy-content surface for scripts + capsules + sequencing. **Failure mode if transferred:** architectural inflation — Gemini-the-organ is structurally redundant with the existing `llm_adapter.py`, so importing it doubles the cognition surface without doubling the substrate behaviour. Sterile-equilibrium failure mode (Audit C §C7.5 "ELIF theater") — surface exists with no anchored Article.
- **Companion architecture** — pedagogy-progression-specific per-formation bundle. **Failure mode if transferred:** importing the learner-facing framing that ELIF does not have collapses the operator-as-judgment-engager into operator-as-learner-consumer; Article II (Frame Humility) violated because the framing assumes the receiver doesn't know the domain; Article IV (Partiality of Models) violated because the bundle implies completeness rather than partiality.
- **Concept explainers** — pedagogy-specific framing where the system teaches a concept to a learner who doesn't know it. **Failure mode if transferred:** identical to companion architecture — collapses operator-as-judgment-engager into operator-as-learner; Article II + IV violated; surfaces would be "let me explain why this verdict is refuse" rather than "here is the verdict + its uncertainty sources + its refutation conditions." Direct educational contamination per Audit C §C7.8.
- **Narrator library content (`NARRATOR_PROFILE_IDS` — 8 closed-set voice tones)** — voice tones for learners, not for arbitration. **Failure mode if transferred:** audio narration of arbitration verdicts is the exact failure mode the cognitive-density doctrine names. A soothing voice reading "verdict=refuse, confidence qualifier: low" violates Article III (no self-validation: the audio voice imports tone, confidence, authority that the structured output explicitly disowns). Audit C §C3.10 explicit rejection at all phases.
- **Atom library content (`ATOM_DOMAIN_CATEGORIES` — 14 pedagogical-domain categories: healthcare_clinical, trades_construction, exam_prep_methodology, etc.)** — knowledge atoms for pedagogical delivery, not arbitration atoms. **Failure mode if transferred:** categorising ELIF outputs by pedagogical domain rather than by problem-shape causes the educational-contamination failure to reach the substrate layer (Audit C §C7.8 second early-warning signal). The categorisation drift becomes structural — ELIF starts behaving like a pedagogical system because its substrate believes it is one.
- **Shell propagation engine** — country-specific lexicon substitution (Medicare → NHS → HMRC → Medicare AU) for pedagogy, not for arbitration. **Failure mode if transferred:** importing a country-aware lexicon-substitution layer for ELIF outputs creates a non-load-bearing rendering layer that adds rendering LoC without serving any Article. The rendering-LoC budget ≤ 0.3 × substrate test (Audit C §C7.6) breaches immediately; the surface becomes a rendering platform with an arbitration backend.
- **Scenario library content (`SCENARIO_SHAPE_IDS` — 8 closed-set shapes: clinical_judgment_triage, ethical_dilemma_resolution, troubleshooting_diagnostic, etc.)** — pedagogical-practice scenarios, not arbitration shapes. **Failure mode if transferred:** importing scenario-tree visualisation imports OSG's pedagogical framing. Audit C §C3.7 explicit rejection — "DECORATIVE for ELIF, not optional later, structurally not a fit." Educational contamination at the visualisation layer.
- **34-observer media biome registry itself** — specific to media generation pipeline (acquisition + micro-video + Limova + Gemini + Audio + cross-organ observers). **Failure mode if transferred:** the 34 specific observers observe phenomena ELIF does not have (publication cadence, voice drift, cognitive fragmentation in micro-videos, capsule-pipeline-state-drift). Importing the registry creates 34 dormant observers with nothing to observe — sterile-equilibrium failure at the observer layer; ceremonial activation pressure rises ("we activated observers but they don't actually fire") which the OSG state-machine was structurally designed to prevent in its own domain but is meaningless in ELIF's.

**The over-arching failure mode named once.** Audit C §C7.8 names it: **educational contamination from OSG**. Pedagogical framing assumes a learner who does not know and must be taught; ELIF's framing assumes an operator who knows the domain and is seeking arbitration on a bundled question. Importing pedagogical framing into ELIF outputs re-frames the operator as a learner, which collapses the engagement Articles II + III + IV require. Every NON-TRANSFERABLE entry above is a specific surface where this contamination would land if the transfer were attempted.

---

## 8. ELIF Media Taxonomy Resolved (from Audit C §C3)

A single consolidated table covering all 11 candidate media types from C §C3. Classes: INDISPENSABLE / USEFUL / OPTIONAL / DECORATIVE.

| # | Media Type | Class | Article / behaviour anchor |
|---|---|---|---|
| 1 | Governance alerts (surfacing `verdict=refuse` with full prominence) | INDISPENSABLE | Article V (Refusal-Capable) directly. The refuse-verdict is the load-bearing output. A surface that hides it or presents it as one option among many is doctrine-violating. Currently surfaced via `exit_code=20` + Step 9 schema output (sufficient for CLI); any V1+ surface beyond CLI structurally requires this. |
| 2 | Decomposition cards (Step 2 axes/families + Step 3 surfaced assumptions, one card per axis / per assumption) | USEFUL at V1 | Article III (Decomposed Reasoning) + II (Frame Humility). Translation of an existing schema-validated output; no new substrate. |
| 3 | Hypothesis cards (Step 4 hypotheses with `distinguishing_prediction` + `fails_if` rendered with equal weight) | USEFUL at V1 | Article I (Epistemic Discipline) + III. Schema-equality of `distinguishing_prediction` and `fails_if` MUST be UI-equality; hiding `fails_if` behind a "details" click is doctrine-violating. |
| 4 | Decision maps (Step 8 stage-gated roadmap with continuation_gates per stage, rendered spatially) | USEFUL at V2+ | Article VI (Coherent Convergence). Renders the schema-validated structure, not a stylised approximation. Risk: map-as-aesthetic could decorate without serving VI; the rendering must trace to the schema fields. |
| 5 | Trajectory maps (Step 7-A outside-original-frame trajectories) | USEFUL at V2+ (overlaps with decision maps) | V + VI + VII. Static, schema-derived layout only; animated trajectory transitions are engagement-theater. |
| 6 | Uncertainty dashboards (cross-case aggregation of unresolved_uncertainty_sources — which kinds recur, which resolved by accumulated evidence) | USEFUL at V2+ | I + V + VI. At single-case scale a list is sufficient (V1); at cross-case scale (V2) aggregation feeds Article VII pattern recognition. Risk: dashboard-as-metric-game would re-import sovereignty; counts only, never confidence scores. |
| 7 | Executive briefs (one-paragraph summary of refuse-verdict + uncertainty sources) | OPTIONAL at V2+ (restricted use); DECORATIVE if presented as primary output | None directly anchored. A brief is acceptable as an *operator-requested* exit view with explicit "this elides the decomposition" framing; structurally rejected as a default surface because it would collapse the procedural engagement Articles II + III + IV require. |
| 8 | Scenario trees (visualisation of branching-pedagogical-practice shapes) | DECORATIVE — explicitly rejected | None. ELIF has no scenarios in the pedagogical sense. Importing scenario-tree visualisation imports OSG's pedagogical framing — the educational-contamination risk (§C7.8). Cognitive-density doctrine violation. Not "optional later" — structurally not a fit. |
| 9 | Audio briefings (TTS narration of arbitration verdicts) | DECORATIVE-AND-RISKY — explicitly rejected at all phases | None. Article III (no self-validation) violated: audio voice imports tone, confidence, authority the structured output explicitly disowns. The only audio use-case that survives is screen-reader-accessible output of the structured text — accessibility infrastructure, not an audio briefing surface. |
| 10 | Video explainers (rendered video summaries of case verdicts) | DECORATIVE-AND-RISKY — explicitly rejected at all phases | None. Same logic as audio, with added engagement-loop risk (failure modes #36 institutional capture + #37 prestige accumulation). The decision-room artefact is the deliverable; a video about the deliverable converts it into content marketing for itself. |
| 11 | Simulation views (visualisation of world-model output if/when ELIF eventually consumes it) | DEFERRED to Audit A | None currently. Audit C does NOT pre-empt the integration question. If world-model integration is pursued, the visualisation question becomes well-formed at Phase 7-design-time (per Synthesis §2.6). C asks A to anchor any simulation outputs to the same epistemic-discipline + frame-humility + refusal-capable Articles that govern current ELIF outputs. |

**Aggregate (consolidated finding):**
- 1 INDISPENSABLE (governance alerts).
- 5 USEFUL at V1/V2 (decomposition cards, hypothesis cards, decision maps, trajectory maps, uncertainty dashboards — counting trajectory maps + decision maps together as overlapping surfaces, 4 distinct surfaces).
- 1 OPTIONAL (executive briefs, restricted-use).
- 1 DEFERRED to Audit A (simulation views).
- 3 DECORATIVE / explicitly rejected (scenario trees, audio briefings, video explainers).

**The communication surface for ELIF is small.** It is anchored on rendering schema-validated structured outputs honestly, not on producing media-rich artefacts. The closed-set of 11 candidates is the audit's closed-set; expansion requires the same closed-set discipline as adding an Article (explicit operator approval + doctrine revision).

---

## 9. Communication Risk Register (from Audit C §C7)

A single consolidated table covering all 8 risks from §C7, each anchored to the four-pole failure-mode taxonomy + risk-roadmap failure modes 31–39 where applicable.

| # | Risk | Failure mode it triggers (four-pole + #31–39) | Active prevention | Early-warning signal (measurable) |
|---|---|---|---|---|
| 1 | Information overload | Fragmentation (perpetual decomposition); four-pole. Article VI direct concern. | V1 user-visible journey bounded at approximately 7 surfaces (Audit C §C5.3) or 8 stages (Audit B §B3.4); cross-case dashboard at V2+ opt-in, not default. Additional surfaces require explicit doctrine revision. | Operator-elapsed-time on decomposition screens divided by operator-elapsed-time on verdict screens. If verdict-screen time approaches zero (operator skipping past decomposition to verdict), surfaces are inviting verdict-shopping. Specifically: mean-time-on-decomposition < 30% of mean-time-per-case across ≥ 10 cases = V1 UI failing. |
| 2 | Governance opacity | False closure (premature termination, masked by procedure); four-pole. Articles V + VI direct concern. | Step 9 verdict + uncertainty sources surfaced with full prominence; `unresolved_uncertainty_sources` schema `minItems=1` is UI-required `minItems=1` visible; no collapse behind "details" click. | Count of operator-actions taken after a refuse-verdict that DO NOT engage with the listed uncertainty sources. Specifically: ≥ 20% of operator post-verdict actions across ≥ 10 cases ignore the `unresolved_uncertainty_sources` list = governance surface failing. |
| 3 | Procedural inflation | Roadmap-as-prestige (#39 in v0.4 risk register applied to procedure). | 11-step procedure locked at v0.1; expansion requires evidence that a structurally distinct procedural step is required; per v0.4 iteration-discipline the trajectory bends toward compression, not addition. Surfaces should NOT duplicate procedural steps — one screen per procedural concern. | Any V1+ UX iteration proposing to add a step to the procedure (vs. exposing an existing step more visibly) must be refused unless cases 2–3 surface a structurally distinct failure mode not covered by the four-pole taxonomy. Specifically: any proposal for a Step 12 refused under v0.4 lock. |
| 4 | False confidence | Absolutization; four-pole. Articles I + III + IV direct concern. Risk 23 (capacity framed as truth approach). | Every Step 9 verdict carries `confidence_qualifier` + `unresolved_uncertainty_sources` (schema-enforced); every Article VII `pattern_engaged` event presented as INVITATION TO TEST, not VALIDATION. | Linguistic audit of operator-facing copy. Any UI text reading "the answer is" / "the right decision is" / "based on prior patterns, this is" without explicit refutation framing = doctrine-violating. Specifically: ≥ 0 occurrences of unhedged claim-language permitted in V1 copy; if even one slips in, copy is failing. |
| 5 | "ELIF theater" | Sterile equilibrium; four-pole. Article VII direct concern. Risk 26 (generative pressure becomes "appear capable" optimization). | Every visible surface traces to substrate behaviour. Surfaces that exist only for aesthetic mass (pretty rendering of empty content, animated transitions with no semantic content, "AI is thinking..." spinners) structurally rejected on cognitive-density doctrine grounds. | Per-surface substrate-anchor audit. Every V1 UI element must be traceable to a specific Article + schema field. Binary signal: if a UI element cannot be named as `serves Article X via schema field Y`, it is theater. Audit cadence: at every UI iteration; threshold for action: any single un-anchored element. |
| 6 | Over-visualisation | Sterile equilibrium with sub-mode: visualisation as substitute for engagement. | §C3 media taxonomy is closed-set (11 candidates). Adding a visualisation type requires the same closed-set discipline as adding an Article — explicit operator approval + doctrine revision. | Ratio of LoC in rendering layer to LoC in substrate layer. Currently alpha is 8,424 LoC substrate + 0 LoC rendering. At V1 target: rendering ≤ 0.3 × substrate. If rendering LoC exceeds substrate LoC, the system has become a rendering platform with an arbitration backend. |
| 7 | Excessive media production | Captured roadmap (#39); risk 26 ("appear capable" optimization). | ELIF does not produce media in the OSG sense (atoms, capsules, scenarios, companions); at every productisation phase the surfaces are operator-facing translations of existing schema-validated outputs, not new artefacts to amortise at scale. | Number of distinct media-artefact types ELIF produces. At v0.1 alpha: structured-output JSONs (per step) + RunReport + MemoryLogger JSONL = 3 artefact families. At V1: same 3 families + rendered HTML/text surface (translation, not a fourth family). If ELIF starts producing a fourth distinct artefact family (e.g., "narrative briefings" as their own type rather than rendered translations), the trajectory has drifted. |
| 8 | Educational contamination from OSG | Frame humility violated (II) + partiality of models violated (IV). Doctrinal contamination, not procedural. | Explicit copy-review discipline against pedagogical framing. No "let's learn together" copy. No "here's what you need to know" copy. No "5 things you should consider" copy. The voice is arbitration-trace, not tutorial. | Copy-style audit. Pedagogical verbs (learn / understand / master / remember) vs. arbitration verbs (decompose / refute / arbitrate / refuse / surface). If pedagogical verbs > 10% of total verb count in operator-facing copy, framing has drifted. Second signal: if ELIF starts categorising outputs by pedagogical domain (per OSG's 14-domain partition) rather than by problem-shape (per the 3 alpha clusters), contamination has reached the substrate layer. |

---

## 10. Linguistic Audit Substrate

The vocabulary audit is the operator-facing concrete test for risks 4 (false confidence), 5 (ELIF theater), and 8 (educational contamination). The audit is binary at the per-element level (each piece of copy passes or fails) and proportional at the per-document level (the 10% pedagogical-verb cap).

**Approved arbitration verbs.** These verbs are the operator-facing vocabulary ELIF's copy should use. They preserve the arbitration-trace framing.

- decompose
- refute
- arbitrate
- refuse
- surface
- validate (in the schema-validation sense, not the answer-validation sense)
- frame
- weigh (hypotheses against `fails_if`)
- govern
- structure (discovery)
- preserve (corrigibility)
- engage
- acknowledge (uncertainty source)
- close (case closure, not closure-as-resolution)

**Forbidden pedagogical verbs.** These verbs import the OSG pedagogical framing and re-frame the operator as a learner. Their presence in operator-facing copy is the early-warning signal for educational contamination (risk 8).

- learn
- understand (in the "now you understand" sense — distinct from "the system understands the frame")
- master
- remember
- study
- absorb
- internalize
- memorize
- grasp
- explain (the system does not explain its verdict; it surfaces the verdict + uncertainty sources + refutation conditions)
- teach
- educate
- guide (in the tutorial sense)

**Forbidden absolutising verbs.** These verbs import sovereignty over context (Article I violation). Their presence is the early-warning signal for false confidence (risk 4).

- prove
- confirm (in the truth-accumulation sense — distinct from "schema confirms shape")
- establish (as in "establishes truth")
- demonstrate (in the "demonstrates the answer" sense)
- conclude (without explicit `confidence_qualifier`)
- recommend (the procedure does not produce recommendations; Step 10 produces an operative/theoretical separation)
- the answer is
- the right decision is
- based on prior patterns, this is

**Quantified ceiling.** Audit C §C7.8: **pedagogical-verb count < 10% of all operator-facing copy verbs**. This is the audit threshold. Above 10%, framing has drifted; below 10%, the copy is within audit tolerance. Above 0% for unhedged absolutising verbs is automatically a failure (Audit C §C7.4: "≥ 0 occurrences of unhedged claim-language permitted in V1 copy; if even one slips in, the copy is failing"). The two ceilings are not symmetric.

**How to run the audit.** Per Audit B §B-Operator-decision-3, the cadence is at every UI iteration (V1, V2 onward). The audit is a simple regex / spaCy verb-extraction over operator-facing copy strings (excluding code comments, schema field names, and internal documentation); pedagogical verbs above 10% surface the copy for review; absolutising verbs at any count surface the copy for immediate revision.

**Why this matters at substrate level.** A second signal layered on top of vocabulary: if ELIF starts categorising its outputs by pedagogical domain (the OSG `ATOM_DOMAIN_CATEGORIES` 14-domain partition: healthcare_clinical / trades_construction / exam_prep_methodology / etc.) rather than by problem-shape (the 3 alpha clusters A/B/C), the contamination has reached the substrate layer (Audit C §C7.8 second early-warning signal). Substrate-level contamination is harder to reverse than vocabulary-level contamination and should be detected by direct inspection of any new closed-set the system introduces.

---

## 11. Per-Phase Communication Surfaces (V1 / V2 / V3 / V4+)

A condensed summary of what each productisation phase communicates, what stays internal, what stays HIDDEN entirely, and the prerequisite EVIDENCE. The full V1 spec lives in P3 (V1 decision-room specification); the full laboratory spec lives in P4 (laboratory v0.1 specification); this section is summary.

### V1 — Minimum communication layer

**What is communicated** (Audit B §B4.1 + Audit C §C6.1):
- 8 user-visible stages (Audit B compression) OR 7 user-visible surfaces (Audit C compression) — operator-selectable at V1 design time.
- Governance alerts (INDISPENSABLE).
- Decomposition cards (USEFUL — Step 2 axes/families + Step 3 surfaced assumptions).
- Hypothesis cards (USEFUL — Step 4 + Step 5 with `distinguishing_prediction` and `fails_if` at equal weight).
- Refuse-explainer (when verdict is refuse, surface explicitly frames it as "the architecture's correct response," not as an error).
- MemoryLogger event timeline (14 events per case visible).
- Per-case dashboard tile in operator-mode (similarity score, LLM-call count, cost; offline = $0.00).

**What stays INTERNAL** (Audit B §B4.1 "What stays INTERNAL"):
- 11-step procedure structure (presented as 8 stages / 7 surfaces externally).
- Runner halt-code mapping (10 / 20 / 30).
- Mode-A vs mode-B split inside Step 7.
- Closed-set vocabulary assertion at runner construction.
- Per-component LoC / dependency graph (operator-debug mode only).
- Schema versions, fixture-mode flag, cost-cap parameter.

**What stays HIDDEN entirely** (Audit B §B4.1 + Audit C §C7.5):
- Any narrative wrapper around the structured output (no LLM-prose summarization layer).
- Any "explain this verdict in plain language" affordance.
- Any audio / video rendering.
- Any UI element not traceable to `serves Article X via schema field Y` (Audit C §C7.5 binary test).

**Prerequisite EVIDENCE** (Synthesis §4.1 + Audit C §C6.1):
- E.2 live-replay completes at structural similarity ≥ 0.83 across the 3 reference cases.
- No architectural regressions in live mode (closed-set vocabulary drift stays at zero).
- Refuse-halt question adjudicated by operator (Gate G0 closed — Position A or Position B).
- Rendering-layer LoC budget set (≤ 0.3 × substrate per Audit C §C7.6).

### V2 — Structured exploration layer (cross-case dashboard / laboratory mode)

**What is communicated** (Audit B §B4.2 + Audit C §C6.2 + §3 above):
- All V1 surfaces.
- Decision maps (USEFUL — Step 8 stage-gated roadmap rendered spatially).
- Trajectory maps (USEFUL — Step 7-A trajectories).
- Uncertainty dashboards (USEFUL — cross-case aggregation of `unresolved_uncertainty_sources`).
- Executive briefs as opt-in only (OPTIONAL, restricted use, with explicit "this elides the decomposition" framing).
- Operative / Theoretical panel (Step 10 outputs).
- MemoryLogger content panel (Step 11 entries: judgment_act, pattern_engaged, capacity_change — surfaced as closure record, not analytics).
- Refuse-closure surface (when refuse is the verdict, UX surfaces what was refused + uncertainty sources + operative list ("refuse the bundle") + theoretical list (uncertainty sources from Step 9)).
- Cost meter (per-case LLM-call count, cost burn against per-case cap of 22 calls, per-cohort cost burn against configurable budget).
- All seven laboratory tiles from §3 above (prior-rooms corridor, pattern panel, capacity-change log, judgment-act log, uncertainty-source frequency, deprecation events, sterile-equilibrium / fragmentation signals).

**What stays INTERNAL** (additions to V1):
- Per-step structured output of intermediate retries (if any).
- Anthropic API tool-call structured-output details.

**What stays HIDDEN entirely** (additions to V1):
- Any prompt-engineering surface (Article III; ELIF must not surface "tweak the prompt to fix the verdict").
- "Prediction strength" / "pattern confidence" computation (Audit C §OD-C-3 + §9 risk 4).
- Any leaderboard, hall-of-fame, "most-engaged-shape" surface (Audit B §B4.3 non-rec; the system must not have a hall of fame).
- Any framing that converts pattern recognition into prediction or validation.
- Background processes maintaining laboratory state (Audit B §B4.5; the surface must be a stateless read over append-only JSONL).

**Prerequisite EVIDENCE** (Synthesis §4.6 + Audit C §C6.2):
- V1 in operator use with ≥ 10 cases run.
- Phase 5 closed: MemoryLogger v0.2 operational; cross-case influence measurable (case N+1's per-step output influenced by case N's MemoryLogger content in a measurable way — time-to-arbitration trend, compositional-reuse frequency).
- Step 11 content-pass operational (judgment_act / pattern_engaged / capacity_change emitted on > 0% of cases).
- The V2 dashboard scope is operator-confirmed as counts-not-predictions (Gate G3-B from Synthesis §3).

### V3 — Multi-operator decision room (SPECULATION; may never open)

**What is communicated** (Audit B §B4.3 + Audit C §C6.3):
- All V2 surfaces.
- Multi-participant decomposition card.
- Multi-participant hypothesis card.
- Per-participant uncertainty-source contribution.
- Per-participant attribution + conflict-resolution for divergent surface assumptions.

**What stays INTERNAL** (additions to V2): authentication; per-participant attribution machinery; audit trail across participants.

**What stays HIDDEN entirely** (additions to V2):
- Any framing that imports "consensus" as a sovereignty surface (Article VI violation — "the consensus weaponises Article VI coherent-convergence into convergence-theater" per Audit C §C6.3).
- Public-facing surfaces (V1–V3 are operator-facing).

**Prerequisite EVIDENCE** (Synthesis §4.9 + Audit C §C6.3):
- V2 stable use ≥ 30 cases.
- Article VII capacity accumulation observable cross-case (faster arbitration on similar-shape problems demonstrably faster).
- Failure mode #32 (Pattern dogmatization) NOT firing — the operator has demonstrated they can refute previously-blessed patterns when new evidence requires it.
- **NEW operator demand surfaced** — the substrate prerequisite. Multi-operator infrastructure should not be built for a solo operator (Audit C §C6.3 + Audit C §OD-C-4 + non-self-propagation constitutional anchor).

**SPECULATION caveat.** If the operator remains solo through the lifetime of the project, V3 is a category error — building multi-operator infrastructure for a single-operator system. ELIF must not "want" more operators in order to justify V3. The synthesis preserves "Phase 9 may never open" as a defensible doctrinal outcome.

### V4+ — Possible simulation / world-model integration

**Cross-audit dependency.** Simulation integration belongs to Audit A (World Models). Audit C does NOT pre-empt the integration question. The Synthesis re-numbers: world-model orchestration is Phase 8 in the synthesis roadmap (Phase 6 in the long-range roadmap). The visualisation question (Audit C §C3.8 simulation views) becomes well-formed at Phase 7-design-time + Phase 8 implementation.

**What is communicated (if V4+ opens):**
- All V2 / V3 surfaces (whichever lineage was reached).
- A simulation surface for world-model outputs entering as evidence anchor at Step 4 (hypothesis distinguishing predictions) or Step 7 (outside-frame trajectories) — never as a Step 1 frame.
- An updated Article VII benchmark including simulator-anchored vs procedural capacity distinction.

**What stays HIDDEN entirely:**
- Any UI element that displays world-model output as high-confidence prediction without uncertainty sources (Audit C §C6.4 cross-cutting signal to A).
- Any simulator-aware verdict at Step 9 closed-set (Synthesis §4.7 permanent prohibition under Audit A §A4.3 item 2).
- Any surface that absorbs the simulator into ELIF's component surface (Synthesis §4.8 permanent prohibition).

**Prerequisite EVIDENCE** (Synthesis §4.7 + §4.8 + Audit C §C6.4):
- V3 operational (or V2 sufficient if operator remains solo).
- Phase 7 closed (world-model schema seam SPECIFIED — not implemented).
- All Gate G6.0–G6.4 from Audit A closed.
- Sterile-equilibrium detector confirmed operational with simulator-bias detection.
- Closed-set verdict vocabulary confirmed frozen.
- Operator decision: actually wire the seam OR keep ELIF as pure arbiter without ever consuming world-model output.

**SPECULATION caveat.** V4+ may never open. Audit A §A4.4.3 names "Entry never (compression path)" as a real possibility under the v0.4 trajectory. The synthesis preserves this.

---

## 12. Operator decisions queued

These decisions are surfaced for the operator. The package does not adopt or recommend; it makes the choices explicit.

1. **Transferability matrix sign-off (or contestation of specific cells).** The §4 matrix consolidates 15 OSG media structures with explicit per-cell justification. The operator may sign off as-is, contest specific cells (e.g., promote the state-machine pattern from PLAUSIBLE-FUTURE WITH MODIFICATION to a currently-actionable port), or defer until Phase 5 (MemoryLogger maturation) opens.

2. **Linguistic-audit ceiling adoption (10% pedagogical-verb cap).** Audit C §C7.8 names the quantified ceiling: **pedagogical-verb count < 10% of all operator-facing copy verbs**, with **0% tolerance for unhedged absolutising verbs**. Adopting this as the V1 copy-audit threshold turns the early-warning signal into an explicit gate. Alternative is to defer the threshold until V1 copy exists and an empirical baseline can be measured.

3. **ELIF media taxonomy sign-off** (the §8 / Audit C §C3 classifications as locked decisions). The 11-candidate closed-set is the audit's closed-set; signing off locks it under the same closed-set discipline as the closed-set verdict vocabulary. Expansion requires explicit operator approval + doctrine revision. Alternative is to keep the taxonomy as an audit-level observation rather than a locked closed-set.

4. **Approval to use this consolidated doc as the operator-facing communication architecture reference.** This package is a distillation of Audit B + Audit C + Synthesis §1.5 + §2.5 + §3 + §4.2 + §4.6. The operator may sign off as the reference doc the team / future-operator reaches for when a communication / media question arises, or treat the distillation as advisory while continuing to reach for the original audits.

These four decisions can close at any time independently. None blocks Gate G0 (refuse-halt adjudication) which remains the single highest-leverage operator decision per the Synthesis §1.3 and §2.3.

---

## 13. What this package does NOT include

This section is load-bearing for the non-expansionary stance.

1. **No visual design / mockups.** The package names communication surfaces by Article + schema-field anchor; rendering choices (typography, layout, colour, interaction pattern) are V1-design-time decisions not consolidated here. Mockups before E.2 live-replay closes would import the momentum-capture failure (Synthesis §6 non-rec 6).

2. **No brand.** ELIF has no brand surface in V1–V3 (operator-facing only; public surface deferred under Audit B §B-non-rec 9). Brand is a far-future-V4+ question outside this package's scope.

3. **No stack choice.** CLI vs HTML vs TUI vs Electron is a V1-implementation-time decision. Audit C §C6.1 names the LoC range (500–2,500 LoC depending on CLI-only vs HTML-also) but does not select. The package does not select either.

4. **No implementation.** Specification ≠ implementation (Synthesis §2.6 + §4.7). This package is the consolidated-operator-facing-reference layer; the V1 implementation lives in P3 (V1 decision-room specification) and the laboratory implementation lives in P4 (laboratory v0.1 specification). Code lives nowhere in this document.

5. **No pedagogical OSG framing imported under different vocabulary.** Any renaming exercise that takes a pedagogical OSG primitive (atom, companion, scenario, narrator, shell, capsule, micro-video) and ports it into ELIF under a non-pedagogical name is the canonical educational-contamination failure (Audit C §C7.8). The package refuses this category of move pre-emptively. If a future operator-facing copy edit reads "let's just rename `companion` to `case_bundle`," the answer is at §C1.4: the structural similarity is real but shallow; the semantics diverge entirely once you ask what the bundle DOES for the receiver, and ELIF's receiver is not a learner.

6. **No new ELIF Article on communication or media.** The Constitutional Layer is locked at v0.4. Adding an Article VIII for communication is exactly the additive iteration the lock forbids without evidence of a structurally-distinct fifth failure mode (Audit C §C-non-rec 6; Synthesis §1.2).

7. **No new procedure step.** The 11-step procedure is invariant at the synthesis level. Surfaces are presentation layers over the procedure; the procedure does not need new steps to support presentation (Audit B §B-non-rec 3).

8. **No chatbot framing.** Audit B §B1.1 names this as ACTIVELY COUNTERPRODUCTIVE — the single largest UX risk for ELIF. Permanently out of scope under all three audits (Synthesis §1.1 + §1.5).

9. **No audio / video media surfaces.** Audit B §B2.7 + §B2.8 + Audit C §C3.10 + §C3.11 + Synthesis §1.4 converge: PERMANENTLY out of scope under current evidence. Even at V4+ if simulation integration is pursued, the simulation surface does not import audio/video.

10. **No simulation workspace inside ELIF.** Simulation is the world-model's affordance per the operator's hypothesis. Importing it inside ELIF imports the four-organ-violation it is forbidden to make (Audit B §B1.5 + §B2.6 + Audit C §C3.8 + Synthesis §1.1 + §1.5).

11. **No multi-operator surfaces at V1–V2.** V3 is SPECULATION (Audit C §C6.3) gated on NEW operator demand as a substrate prerequisite, not as a roadmap projection (Audit C §OD-C-4).

12. **No public-facing surfaces.** V1–V3 are operator-facing. Public exposure imports failure modes (engagement, prestige, institutional capture) the constitutional layer was designed to resist (Audit B §B-non-rec 9).

13. **No cross-product runtime coupling with OSG.** ELIF does not integrate with the OSG pedagogical biome, Media biome, Continuity layer, or any other production system at runtime. The four-organ separation and non-self-propagation rule both forbid this (Synthesis §1.7 + Audit B §B-non-rec 10 + Audit C §C-non-rec 9).

14. **No knowledge-graph / "what ELIF has learned" surface.** Truth-accumulation framing is forbidden under Article VII. The laboratory surface renders capacity (what ELIF can now do faster / with composition) and never truth (what ELIF knows). UI commitment to this distinction is structural, not stylistic (Audit B §B-non-rec 11).

15. **No background processes maintaining laboratory state.** The laboratory is a VIEW over append-only JSONL, derivable on demand. Background processes are the pausability-failure mode (Audit B §B-non-rec 12 + §B4.5).

16. **No re-execution loops, no "tweak the prompt" affordances, no free-form exploration sandbox.** The procedure is bounded; the cost-cap is structural; the engagement-loop affordance is the failure mode the momentum-capture warning resists (Audit B §B-non-rec 8 + §B3.6).

17. **No rendering layer growth above 0.3 × substrate LoC.** Audit C §C7.6: if rendering LoC exceeds substrate LoC, the system has become a rendering platform with an arbitration backend. The 0.3 ratio is the audit's defensible bound (Synthesis §1.5 + §3 G3-D).

---

**End of package.**

This document is the operator-facing distillation of Audit B + Audit C on the communication and media architecture of ELIF. It does not resolve Gate G0 (refuse-halt). It does not propose V1 / V2 / V3 / V4 implementation — those live in P3, P4, P2, P5 respectively. It locks the transferability matrix, the media taxonomy, the risk register, and the linguistic ceiling as operator-facing references the team can reach for when a communication or media question arises.
