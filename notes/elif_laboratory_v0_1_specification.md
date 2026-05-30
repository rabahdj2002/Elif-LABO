# ELIF Laboratory v0.1 — Specification

> **Captured:** 2026-05-30
> **Status:** Specification only. No implementation. Non-expansionary.
> **Authority:** Specification of how a laboratory surface — defined as the **cross-case observability surface** distinct from the per-case V1 Decision Room — would consume the eventual outputs of MemoryLogger v0.2. This document does NOT specify v0.2 itself; that is `elif_audit_synthesis.md` §4.5 Phase 5 scope.
> **Doctrine constraint:** no v0.5, no new component, no new Article, no world-model implementation, no roadmap expansion, no speculative phase activation, no pattern adoption beyond evidence, no architecture inflation. The laboratory is a **stateless read** over append-only JSONL plus per-step JSON artifacts. It is not a new component; it is a rendering of substrate already named.
> **Substrate gates:** G5 (MemoryLogger v0.2 ships with cross-case state replay) per `elif_audit_synthesis.md` §5 gate table. The laboratory does not open before G5 closes. G0 (refuse-halt adjudication, §4.0 of the synthesis) gates the content the laboratory has anything to render.
> **Epistemic discipline:** every claim is anchored to one of three registers — **CURRENT EVIDENCE** (what the v0.1 alpha + locked doctrine demonstrably support); **PLAUSIBLE FUTURE** (what holds if the substrate-gated prerequisites close as specified); **SPECULATION** (what depends on substrate or operator decisions not yet held). Unlabelled paragraphs inherit the surrounding heading's register.

---

## §0. What this specification is and is not

This document specifies the **Laboratory v0.1** surface. "v0.1" here means: the smallest cross-case observability surface that can be built once the MemoryLogger transitions from log (append-only JSONL) to substrate (cross-case state replay + content event types), per `elif_audit_synthesis.md` §4.5 Phase 5. It is the surface that renders Article VII's capacity-vs-truth distinction honestly and renders the sterile-equilibrium detector's outputs as inspectable signals.

The Laboratory is not the Decision Room. The Decision Room (V1, per `elif_audit_b_user_experience.md` §B1.3 + `elif_audit_synthesis.md` §4.2) is per-case: a single case is entered, arbitrated, and closed. The Laboratory is cross-case: it is the corridor across rooms. The two archetypes hybridise per Audit B §B1.7 — the operator enters a room to arbitrate; returns to the laboratory between cases.

The specification draws a hard boundary at the substrate gate. Until MemoryLogger v0.2 emits `judgment_act` / `pattern_engaged` / `capacity_change` event types cross-case AND cross-case state replay is operational (per `elif_v0_1_what_remains.md` §8.3 v0.2 acceptance scope), the laboratory has nothing to render. This document specifies HOW it consumes those v0.2 outputs; it does NOT specify how v0.2 produces them.

What this document refuses to specify:
- Any implementation of cross-case state replay (that is v0.2 scope per the synthesis §4.5).
- Any new component, Article, procedure step, schema field, or closed-set entry.
- Any chatbot affordance, audio briefing, video summary, simulation workspace, knowledge-graph, multi-operator surface, or pedagogical framing inside the laboratory. These are PERMANENTLY out of scope per the cross-audit convergence at `elif_audit_synthesis.md` §1.4 + §1.5 + §1.7.
- A prediction layer, a "pattern confidence" score, or a "validated pattern" framing. The closed-set is **counts**, per `elif_audit_c_media_communication.md` §OD-C-3.
- A roadmap for Laboratory v0.2 / v0.3. The non-expansionary stance forbids it.

---

## §1. Scope — Cross-case only; per-case lives in V1

### §1.1 What the Laboratory shows that V1 cannot

CURRENT EVIDENCE. V1 is a case-viewer (`elif_audit_b_user_experience.md` §B4.1). Its surfaces are: case viewer rendering Steps 1-9 as inspectable panels; decision-map rendering of Step 2; scenario-tree rendering of Step 7 + Step 8; governance verdict panel for Step 9; refuse explainer; MemoryLogger event timeline for ONE case (the 14 events of the open + step_committed × 9 + step_7_modeB + refutation + close + bookkeeping chain documented in `elif_v0_1_alpha_replay_report.md` §case_01.6); per-case dashboard tile. Every one of these surfaces is scoped to a single case.

V1 by construction cannot show:
- The shape of capacity accumulation across cases (Article VII).
- The shape of pattern engagement across cases (Article VII compositional reuse).
- The shape of pattern deprecation across cases (Article VII refutation regime).
- The signal whether the system as a whole has entered sterile equilibrium (four-pole failure mode #4, defended by Article VII).
- The signal whether the procedure has fragmented across cases (four-pole failure mode #3).

These observables live, by definition, across cases. They are the substrate of Article VII. They cannot be rendered by a per-case surface.

### §1.2 Why cross-case observability is doctrinally required

CURRENT EVIDENCE. Article VII (capacity vs truth) requires that **capacity accumulation** be observable in a form distinct from truth accumulation. Per `elif_audit_b_user_experience.md` §B2.9 + §B4.3 and `elif_audit_c_media_communication.md` §C6.2:

> Article VII is operationally meaningful only if its observables are inspectable. A non-rendered MemoryLogger satisfies the persistence requirement but not the longitudinal-observation requirement that distinguishes capacity-watching from prestige-accumulating.

The substrate of Article VII (MemoryLogger as append-only JSONL with closed-set `_VALID_EVENT_TYPES` and `_VALID_CHANGE_TYPES` per `src/elif_v0_1/components/memory_logger.py` lines 47-69) already exists. What is missing at v0.1 alpha is the rendering surface. Without that surface, Article VII is structurally enforced (schemas pass, events are written) but operationally invisible. The Laboratory v0.1 is the rendering of an already-existing substrate, not the construction of a new one.

PLAUSIBLE FUTURE. Once MemoryLogger v0.2 emits `judgment_act` / `pattern_engaged` / `capacity_change` cross-case (v0.2 acceptance scope per `elif_v0_1_what_remains.md` §8.3), the rendering surface becomes feasible. Until then, the Laboratory has nothing to render but the structural events (`open`, `close`, `step_committed`, `refutation`) the alpha already writes. That subset is small but defensible — see §2 below.

### §1.3 Cross-case scope as a doctrinal boundary

The Laboratory's scope is bounded structurally:

- **In scope**: events emitted by MemoryLogger across all cases under `base_persistence_dir` (per `memory_logger.py` `_iter_case_dirs()` line 179); aggregations of those events; the sterile-equilibrium detector's verdict from `detect_sterile_equilibrium(case_id=None)` (line 455); the reuse-candidate scan from `find_reuse_candidates()` (line 294) on demand; the capacity-metrics aggregate from `compute_capacity_metrics()` (line 342).
- **Out of scope**: any per-case rendering already covered by V1; any rendering of `step_committed` payloads as decomposition-substance (V1 owns this); any prediction or confidence score not present in the substrate; any external surface (no public-facing variant of the Laboratory exists in v0.1).

Boundary enforcement is by source, not by convention. The Laboratory reads `_iter_case_dirs()` and the cross-case aggregates exposed by MemoryLogger; it does not reach into the schema-validated per-step output JSONs that V1 renders. The two surfaces have non-overlapping read paths.

---

## §2. MemoryLogger observability panel

### §2.1 Substrate consumed

CURRENT EVIDENCE. The MemoryLogger (per `memory_logger.py`) writes an append-only JSONL per case at `<base_persistence_dir>/<case_id>/article_vii_tracking.jsonl`. Each event carries `event_id`, `event_type` ∈ closed-set `_VALID_EVENT_TYPES`, `case_id`, `committed_at_iso`, `schema_version`, and an optional `payload`. Correction events carry `supersedes_event_id`; the original line is NEVER mutated (Article III audit-trail discipline; line 16 + line 405 of `memory_logger.py`).

PLAUSIBLE FUTURE (G5-gated). After v0.2, the closed-set will include `capacity_change` (already in `_VALID_EVENT_TYPES` line 57 + the closed-set `_VALID_CHANGE_TYPES` line 63), `pattern_recognized` (line 56), and `reuse_detected` (line 55). The v0.2 acceptance scope is what makes the panel content-rich; v0.1 alpha emits only the structural events (open / step_committed / refutation / close).

### §2.2 What the panel renders

The MemoryLogger observability panel is a stateless derivation over the JSONL files of all known cases. Its renderings are:

**Event timeline (cross-case)**. A chronological view of every event written across all cases, derived by iterating `_iter_case_dirs()` and reading each `article_vii_tracking.jsonl`, then merging by `committed_at_iso`. Filterable by `event_type` (closed-set; the filter dropdown lists exactly the 11 members of `_VALID_EVENT_TYPES`, no synonyms) and by `case_id` (free-text; the closed-set there is the set of directories under `base_persistence_dir` at read time).

**Aggregate counts (cross-case)**. The output of `compute_capacity_metrics()` (line 342 of `memory_logger.py`) rendered as a counts table: `total_events`, `capacity_change_records`, `reuse_count_total`, `patterns_recognized`, `cases_observed`. Per-case sub-counts available as a drilldown. The numbers are exactly what `compute_capacity_metrics()` returns; the panel does not compute its own metrics.

**Per-case open/close timeline**. A horizontal bar per case showing `open` timestamp to `close` timestamp (or "open" if no close yet). This is the cross-case shape that V1 cannot render: V1 shows a single bar; the Laboratory shows N bars stacked.

**Refutation density**. Count of `refutation` events per case, sorted descending. Useful for surfacing which cases are doing the load-bearing refutation work Article I/III/V/VI structurally invite. The display is a counts column, not a heatmap; heatmaps invite the "this case is good/bad" framing that Article VII (capacity vs truth) forbids.

**Correction events surfaced as first-class**. Per Audit B §B4.5 + `memory_logger.py` `emit_correction` line 399, corrections are NEW events that supersede a target via `supersedes_event_id`; the original line is NEVER mutated. The panel surfaces both the original event AND the correction in the timeline, with a visual link between them. Truncating either side would violate Article III audit-trail discipline. The supersede-only discipline is preserved at the rendering layer.

### §2.3 What the panel does NOT render

- Any computed "case quality" score (no truth-framing).
- Any "operator productivity" metric (no engagement-loop framing per `elif_audit_b_user_experience.md` §B2.7-2.8 + #36).
- Any aggregate that converts case counts into trend lines without an explicit "INVITATION TO TEST" framing per `elif_audit_c_media_communication.md` §C7.4 (V1 copy linguistic-audit standard applies recursively to V2+).
- Any prediction about future cases from past events (counts-not-predictions per OD-C-3).

### §2.4 Read semantics

The panel re-reads the JSONL on every render. There is no maintained state between renders. If the operator closes the laboratory for six weeks and reopens it, the panel renders exactly what the JSONL contents are at reopen time, including any corrections appended in the interval. This is the pausability commitment (§8 below) made operational at the panel level.

---

## §3. Article VII observability panel — CAPACITY only

### §3.1 What capacity looks like rendered honestly

CURRENT EVIDENCE. Article VII names capacity in the language of the v0.4 constitutional layer: faster arbitration on similar-shape problems (time-to-arbitration trend), compositional reuse (case N references case N-1 structures), pattern emergence + refutation rates. Per `elif_audit_synthesis.md` §4.5 Phase 5 deliverable:

> A test corpus of cross-case behavior: case N+1's per-step output influenced by case N's MemoryLogger content in a measurable way (time-to-arbitration trend, compositional-reuse frequency).

The Article VII panel renders these measurements honestly. The discipline is operational: each tile traces to a specific measurement on the JSONL substrate that is well-defined whether the system has accumulated capacity or not.

### §3.2 Panel tiles

**Time-to-arbitration trend (cross-case)**. For each cluster of structurally-similar cases (see §3.4 below on closed-set cluster identification), render a sequence: case N's elapsed time from `open` to `close`, case N+1's elapsed time, etc. The PLAUSIBLE FUTURE Article VII commitment is that N+1 ≤ N for similar-shape problems; the rendering shows the actual sequence. If the trend is flat or rising, the panel renders that honestly — there is no smoothing, no "trending toward improvement" framing. The display: a sparkline of per-case elapsed-times within a cluster, plus the literal sequence of values.

**Compositional reuse frequency**. Count of `reuse_detected` events per case; cross-case sum from `compute_capacity_metrics()['reuse_count_total']`. The display: a per-case table column. PLAUSIBLE FUTURE (G5-gated): once `reuse_detected` is emitted in live runs, this column has non-zero entries. At v0.1 alpha it is zero across all cases — and the panel renders zero honestly.

**Pattern emergence count**. Count of `pattern_recognized` events per case + cross-case sum. PLAUSIBLE FUTURE same as above; v0.1 alpha is zero.

**Pattern refutation count**. Count of events with `event_type == "refutation"` that name a previously-recognized pattern in their payload. PLAUSIBLE FUTURE: refutation density per pattern is a load-bearing measurement against pattern-as-prestige (risk #24 in v0.4 risk matrix); see §6 below.

**Cases observed**. The literal count from `compute_capacity_metrics()['cases_observed']`. At v0.1 alpha this is 3 (the operator-locked reference cases). PLAUSIBLE FUTURE: as cases accumulate, this counter rises.

### §3.3 What the panel renders as CAPACITY

The panel uses the vocabulary established in `elif_constitutional_layer.md` v0.4 anchor "capacity-vs-truth": "ELIF can now arbitrate a structurally-similar problem with fewer steps" / "ELIF has engaged the following patterns across cases" / "ELIF has refuted the following patterns when subsequent evidence required it." All three are observable, all three are framed as the system's behavior (what it can DO), not as accumulated content (what it KNOWS).

### §3.4 Cluster identification at v0.1 of the Laboratory

PLAUSIBLE FUTURE / SPECULATION boundary. Per `elif_audit_c_media_communication.md` §C1.10 + §C4.1, ELIF cases cluster by problem-shape (the three case clusters A/B/C — scientific-evidential ambiguity / policy-governance-bundle / operational-organizational-bundle — already present in the alpha). At v0.1 of the Laboratory, cluster labels are **operator-authored metadata on the input frame**, not a computed surface. The Laboratory renders the operator's labels.

SPECULATION (deferred): automated problem-shape fingerprinting (computing a cluster label from the input frame content) is out of scope for Laboratory v0.1. It is a v0.2+ question, and even then is gated by evidence of stable cluster shapes across ≥ 10 cases per `elif_audit_synthesis.md` §4.3 Phase 3 deliverable. The Laboratory v0.1 does not pre-empt the fingerprinting question.

### §3.5 Surface design choice: side-by-side with refutation

The Article VII capacity panel renders capacity tiles side-by-side with refutation density (from §2.2). This is the structural defence against the "ELIF is accumulating mastery" mis-reading: every time the operator looks at "patterns engaged," the refutation density is visible at the same level. The pairing is deliberate; it is also what makes the next section (§4) doctrinally enforceable.

---

## §4. Capacity-vs-truth visibility — the Article VII core commitment

### §4.1 The doctrinal text

Article VII (capacity vs truth) is the constitutional anchor `elif_constitutional_layer.md` v0.4 marks as the "governing distinction." Per `elif_audit_b_user_experience.md` §B2.9:

> The laboratory mode is LOAD-BEARING because Article VII is operationally meaningful only if its observables are inspectable. A non-rendered MemoryLogger satisfies the persistence requirement but not the longitudinal-observation requirement that distinguishes capacity-watching from prestige-accumulating.

Per `elif_audit_b_user_experience.md` §B4.3 V3 prerequisites (re-scoped to V2-mature per `elif_audit_synthesis.md` §2.4 resolution path):

> The UI separates "ELIF can now do X faster / with more composition" (capacity, permitted) from any framing that would imply "ELIF knows X" (truth, forbidden). This is a structural UI commitment to Article VII.

### §4.2 UI commitment (load-bearing)

The Laboratory v0.1 is structurally committed to:
- **DISPLAY** capacity metrics: time-to-arbitration trend, compositional reuse frequency, pattern emergence count, pattern refutation count, cases observed.
- **NOT DISPLAY** any framing that implies truth-accumulation. This includes:
  - "What ELIF has learned"
  - "What ELIF knows about <topic>"
  - "Accumulated knowledge" / "knowledge base" / "knowledge graph"
  - "Most-engaged shape" / "top patterns" / "validated pattern"
  - Any leaderboard
  - Any "hall of fame"
  - Any framing that converts an engagement count into a prediction or validation

The list is closed at this v0.1 specification. Adding a forbidden framing requires explicit operator-approved doctrine revision, mirroring the closed-set discipline of `_VALID_EVENT_TYPES` and `_VALID_CHANGE_TYPES`.

### §4.3 Surface design choices preserving the distinction at substrate level

Vocabulary, layout, and framing are all substrate-level commitments — not stylistic choices. The Laboratory's structural defences:

**Vocabulary**. The panel headers use the verbs `engaged` / `refuted` / `recognized` / `arbitrated`. The panel headers never use `learned` / `knows` / `mastered` / `accumulated knowledge`. The vocabulary is closed-set at the rendering layer.

**Layout**. The capacity tiles and the refutation tiles share the same row. There is no "main panel" of capacity with refutation hidden behind a drilldown. Symmetry of prominence enforces symmetry of doctrinal weight (Article VII pattern_engaged ↔ pattern_refuted).

**Framing**. Every pattern tile carries the explicit phrase "INVITATION TO TEST" (or the equivalent doctrinal text from `elif_constitutional_layer.md` v0.4 anchor) at the same prominence as the count. The phrase is not a tooltip; it is on the tile itself, in the same text weight as the number. Per `elif_audit_c_media_communication.md` §C7.4:

> Every Article VII pattern_engaged event must be presented as INVITATION TO TEST, not VALIDATION.

**Linguistic audit at every iteration**. Per `elif_audit_c_media_communication.md` §C7.4 the V1 standard is "≥0 occurrences of unhedged claim-language permitted in V1 copy." The Laboratory v0.1 inherits this standard: ≥0 occurrences of unhedged claim-language permitted; if even one slips in, the copy is failing.

### §4.4 The structural test

A Laboratory v0.1 implementation passes the Article VII commitment test if, and only if, the following are simultaneously true at every rendering:
- Every capacity tile traces to a measurement on the JSONL substrate per `memory_logger.py` API.
- Every capacity tile is paired with its refutation counterpart at equal prominence.
- The vocabulary check (engaged/refuted/recognized/arbitrated only) passes.
- The "INVITATION TO TEST" framing is on every pattern tile.
- No truth-accumulation framing appears in any panel text.

Failure on any single item invalidates the Laboratory's Article VII compliance.

---

## §5. Pattern engagement panel

### §5.1 The closed-set under v0.2 substrate

PLAUSIBLE FUTURE (G5-gated). Once MemoryLogger v0.2 emits `pattern_recognized` and `pattern_engaged` events (per `_VALID_EVENT_TYPES` lines 47-59 of `memory_logger.py` — the event types are closed-set already; what v0.2 adds is the active emission of `pattern_recognized`), the Laboratory renders the cross-case pattern set.

The closed-set members of "pattern" at v0.2 are:
- The patterns ELIF has engaged across cases (each `pattern_recognized` or `pattern_engaged` event references a pattern id or label).
- Per pattern: engagement count (sum of events referencing it), last-engaged case_id, last-engaged timestamp, deprecation status (whether a subsequent refutation event has fired for it).

### §5.2 Per-pattern display

Each pattern is rendered as a row with the following columns, all derived from the JSONL substrate:
- Pattern label (operator-authored or closed-set, per §13 operator decision queued).
- Engagement count (literal sum from JSONL).
- First-engaged case_id + timestamp.
- Last-engaged case_id + timestamp.
- Deprecation status: ACTIVE / REFUTED. ACTIVE means no refutation event has fired; REFUTED means at least one refutation event has fired against this pattern label in a subsequent case.
- "INVITATION TO TEST" framing line (see §4.3).

### §5.3 Framing — INVITATION TO TEST, not VALIDATED PATTERN

Every pattern row carries the explicit phrase "INVITATION TO TEST." This is not a stylistic choice; it is the structural defence against pattern-as-prestige (risk #24 — Memory Logger as prestige store, per the v0.4 risk matrix).

Per `elif_audit_b_user_experience.md` §B4.3:

> Pattern recognition is rendered as "shape recognized; INVITATION TO TEST" not as "answer."

Per `elif_audit_b_user_experience.md` §B4.4 non-recommendation:

> No prestige surface (no leaderboard of patterns; no "most-engaged shape" trophy; the system must not have a hall of fame).

The Laboratory v0.1 inherits this without modification.

### §5.4 Anti-prestige discipline as load-bearing

The pattern panel has no sort-by-engagement-count default. The default sort is by last-engaged timestamp (most recent first), which surfaces freshness rather than accumulation. Operators may re-sort, but the system does not lead with a most-popular framing.

The pattern panel has no "trending" column. There is no week-over-week count delta. The panel renders the current state of the JSONL; it does not compute change-over-time as a prominence signal.

The pattern panel has no "endorsed" or "blessed" markers. There is no curation surface inside the Laboratory. If an operator wants to mark a pattern as worth re-engaging, that intention is captured via `emit_correction()` on the underlying events, NOT via a curation flag in the Laboratory rendering. Read-only discipline (§9) is recursive: the Laboratory cannot mark, tag, or score patterns.

### §5.5 What the pattern panel does NOT render

- "Top patterns" / "Most-engaged shapes" (anti-prestige discipline).
- "Pattern confidence" / "Pattern strength" / "Prediction strength" (counts-not-predictions per OD-C-3).
- "Recommended pattern for this case" (no recommendation framing per `elif_audit_c_media_communication.md` §C5.2 — the procedure does not produce recommendations).
- "Pattern category" / "Pattern domain" (no pedagogical-taxonomy import per `elif_audit_c_media_communication.md` §C7.8 educational contamination warning).

---

## §6. Deprecation visibility

### §6.1 Why deprecation is first-class

CURRENT EVIDENCE. Per `elif_constitutional_layer.md` v0.4 failure-mode #32 (Pattern dogmatization, added 2026-05-27 per the memory note `elif_constitutional_layer`):

> Defended via UI exposure of refutation events as prominent.

The dogmatization failure-mode is the canonical risk in any pattern panel: a pattern engaged 7 times across 10 cases is structurally inviting "this is true" framing. The Article VII defence is to surface the refutation events at the same prominence as the engagement events. Hiding refutation behind a drilldown would import the dogmatization failure at the rendering layer.

### §6.2 What deprecation visibility looks like

A pattern that has been engaged in N cases and then refuted in M subsequent cases is rendered:
- The engagement count is N.
- The refutation count is M.
- The deprecation status is REFUTED (if M > 0) or ACTIVE (if M = 0).
- Both counts are at the same text prominence on the row.

In addition, the Laboratory has a dedicated "Deprecation events" tile (separate from the pattern panel) that surfaces all refutation events with their associated pattern, the case in which the refutation fired, and the timestamp. This tile is on the Laboratory's main view, not in a sub-page.

### §6.3 Failure-mode defence via UI exposure

Per the v0.4 failure-mode #32 doctrinal anchor, the deprecation visibility is defensive. The Laboratory v0.1 commits to:
- Deprecation events are rendered on the main view (not in a separate tab).
- Deprecation events are not auto-collapsed; the operator does not need to expand them to see them.
- The deprecation tile has the same prominence as the capacity tile (§3.2).
- A pattern whose `REFUTED` status fired most recently is sorted near the top of the pattern panel by default-secondary sort.

These choices are structural commitments, not preferences. They can be revised only by explicit doctrine revision under operator authority.

### §6.4 What deprecation does NOT do

Deprecation in the Laboratory v0.1 does not delete or hide the original pattern. The original `pattern_recognized` events remain in the JSONL (append-only discipline; per `memory_logger.py` `emit_correction` semantics, lines 405-450). The refutation is a new event that supersedes the pattern's ACTIVE status; it does NOT erase the pattern's engagement history.

This preserves the audit trail discipline at the rendering layer. The operator can always see: this pattern was engaged in cases N, N+1, N+3; it was refuted in case N+5; it remained REFUTED through case N+8. The full history is visible; only the status changes.

---

## §7. Sterile-equilibrium + fragmentation detector surfaces

### §7.1 Substrate consumed

CURRENT EVIDENCE. The sterile-equilibrium detector is already specified at `memory_logger.py` `detect_sterile_equilibrium()` line 455, with signature:

```
detect_sterile_equilibrium(case_id: Optional[str] = None) -> Dict
```

It returns:

```
{
    "sterile_equilibrium": bool,
    "scope": "case" | "cross_case",
    "case_id": str | None,
    "signals": {
        "reuse_count_total": int,
        "capacity_change_records": int,
        "patterns_recognized": int,
        "total_events": int,
    },
}
```

When `case_id=None`, the detector operates over ALL known cases. Sterile equilibrium fires when `reuse_count_total == 0` AND `capacity_change_records == 0` AND `patterns_recognized == 0` AND `total_events > 0` (per lines 508-513).

PLAUSIBLE FUTURE. Per `elif_audit_synthesis.md` §4.5 Phase 5 deliverable, sterile-equilibrium detector v0.1 ships at the end of Phase 5. The Laboratory v0.1 consumes its outputs without re-implementing the detector.

### §7.2 How the Laboratory renders the detector's verdict

The detector's verdict appears as a single tile on the Laboratory main view labelled "Sterile-equilibrium signal." The tile shows:
- The literal Boolean (`sterile_equilibrium`).
- The four signal counts at equal prominence: `reuse_count_total`, `capacity_change_records`, `patterns_recognized`, `total_events`.
- The scope ("cross_case" when the Laboratory invokes the detector without `case_id`).

The tile is **NOT** styled as an alert. It does not change color when `sterile_equilibrium == True`. It does not produce a banner. It does not emit a notification.

Per `elif_audit_b_user_experience.md` §B4.3:

> Sterile-equilibrium and fragmentation detector outputs: surface the MemoryLogger's signature detectors as observability tiles in the laboratory. Not as alerts (no engagement-loop), but as inspectable signals.

The Laboratory inherits this exactly. The detector's verdict is information; what it implies is operator judgment.

### §7.3 Fragmentation detector (PLAUSIBLE FUTURE)

PLAUSIBLE FUTURE. The four-pole failure mode #3 (fragmentation) is named in `elif_constitutional_layer.md` v0.4 but does not yet have a deterministic substrate detector in `memory_logger.py`. Per `elif_v0_1_what_remains.md` §5.3 the four-pole taxonomy is untested at this pole in the alpha; the fragmentation detector is a v0.2+ specification question, not a v0.1 Laboratory specification question.

The Laboratory v0.1 specifies the slot for a future fragmentation detector tile (same layout as the sterile-equilibrium tile, same non-alert discipline). The slot is rendered as "Fragmentation signal: not yet operational" until the detector v0.1 ships. This is a placeholder, not an implementation request — naming the slot prevents future implementations from inflating to a "fragmentation dashboard" that includes scoring, alerts, or recommendations.

### §7.4 What the detector surfaces do NOT do

- They do not page the operator. There is no alerting infrastructure.
- They do not auto-halt anything. The detector is observation; halting authority remains with `governance_kernel` per `elif_audit_c_media_communication.md` §C1.14 single-carrier-exclusivity discipline.
- They do not aggregate over time as a "sterile-equilibrium trend." The detector is a point-in-time read; the Laboratory renders the current verdict.
- They do not produce a "health score" for the system. There is no system-level score.

---

## §8. Stateless-read architecture — the pausability constraint

### §8.1 Doctrinal anchor

Per `elif_audit_b_user_experience.md` §B4.5 + the memory note `momentum_capture_warning`:

> The laboratory is a VIEW over append-only JSONL, derivable on demand. Background processes maintaining live laboratory state are the pausability-failure mode; if the laboratory cannot be left for weeks and re-entered without rebuild, the architecture has over-coupled to its own execution.

Per `elif_audit_synthesis.md` §1.9:

> Pausability is the maturity test... Any version of ELIF (V1, V2, V3) whose surface cannot be left for weeks and re-entered without state-rebuild has failed the maturity test.

The momentum-capture warning is constitutional (`elif_constitutional_layer.md` memory note, locked 2026-05-27). The Laboratory v0.1 inherits this without modification.

### §8.2 What stateless-read means operationally

The Laboratory v0.1 is structurally a **derivation** over:
- The JSONL files at `<base_persistence_dir>/<case_id>/article_vii_tracking.jsonl` for each case.
- The per-step output JSONs (only insofar as a panel may need to surface a `case_id` ↔ step_committed payload pointer; no rendering of step content beyond the V1 boundary).
- The metadata accessible through the `MemoryLogger` read API (`read_case_state`, `find_reuse_candidates`, `compute_capacity_metrics`, `detect_sterile_equilibrium`).

On every render, the Laboratory:
1. Iterates `_iter_case_dirs()` to discover all known cases (cost: one directory scan).
2. Reads each `article_vii_tracking.jsonl` (cost: linear in event count).
3. Computes its panel-level aggregates on the fly (cost: linear in event count).
4. Renders.

There is **no** background process maintaining a live cache. There is **no** indexing daemon. There is **no** materialized view. There is **no** queue.

### §8.3 The pause/resume invariant

The operator can close the Laboratory and reopen it six weeks later. The first render at reopen produces the exact derivation over the current JSONL state. Any events appended during the six-week pause appear in the render. Any corrections appended supersede their targets in the render. Any sterile-equilibrium verdict reflects the current cross-case signal counts.

Nothing about the Laboratory needs to "catch up." There is no migration. There is no warm-up. There is no state to reconcile.

This is the V3-grade momentum-capture defence per `elif_audit_b_user_experience.md` §B4.5. The Laboratory v0.1 commits to it preemptively — not as an aspirational property to add later, but as the structural shape of the surface from inception.

### §8.4 Cost-of-render bound

PLAUSIBLE FUTURE. At v0.1 with 3-10 cases, the render cost is sub-second. The per-case JSONL is bounded by the number of events written per case (per `elif_v0_1_alpha_replay_report.md` §case_01.6, 14 events per alpha case under refuse-halt; PLAUSIBLE FUTURE under Position B refuse-closure, possibly 16-20 events per case). With cases counted in the low tens, the cross-case scan is bounded by tens-of-thousands of events at most.

SPECULATION. The cost model holds up to ~10,000 cases (~200,000 events) under the simple linear-scan approach. Beyond that, the operator may want to introduce per-render caching — but introducing caching is a doctrinal commitment requiring explicit operator approval per the pausability test, because any cache is a state-machine outside the JSONL substrate. This v0.1 specification does NOT pre-authorize caching; it explicitly defers the question.

### §8.5 What this constraint forbids

- No background indexing service.
- No live event subscriber.
- No webhook ingestion.
- No incremental aggregation maintained between renders.
- No "Laboratory daemon."
- No "Laboratory cache directory" maintained separately from the JSONL.

If a future implementation proposes any of the above, the proposal violates the pausability constraint and requires explicit doctrine revision under operator authority.

---

## §9. Read-only discipline

### §9.1 The substrate-anchor commitment

The Laboratory NEVER writes back to MemoryLogger. The Laboratory is a stateless read; it has no write surface to the JSONL.

Per `elif_audit_b_user_experience.md` §B-non-recommendations 4 + the substrate-anchor audit per `elif_audit_c_media_communication.md` §C7.5:

> Every visible surface must trace to substrate behaviour. Surfaces that exist only for aesthetic mass... are structurally rejected on cognitive density doctrine grounds.

The corollary: surfaces that produce side effects beyond rendering — including marking, tagging, deleting, editing, or upvoting events — are structurally rejected. Any such side effect is a substrate mutation, and mutations happen only via the `MemoryLogger.emit_correction()` code path, not via the Laboratory UI.

### §9.2 How corrections happen

Per `memory_logger.py` `emit_correction()` (line 399), corrections are emitted in code by callers who hold a `MemoryLogger` instance. The correction is a NEW event with `event_type="correction"` and `supersedes_event_id=target_event_id`. The original is NEVER touched.

The Laboratory does not host a correction UI. If the operator observes an event that requires correction, the operator's path is:
1. Identify the event_id in the Laboratory rendering.
2. Outside the Laboratory, in code or via a tool that wraps `MemoryLogger.emit_correction()`, emit the correction with the supplied event_id and correction payload.
3. Re-open the Laboratory; the rendering now reflects the correction.

This is deliberate friction. Per `elif_audit_c_media_communication.md` §C1.8 (friction-preserving as judgment-preserving):

> ELIF's analogue: turn the 11-step procedure into a one-click "Get Verdict" button that hides the steps the operator was supposed to engage with. That would collapse the procedure into a magic-8-ball.

A correction button inside the Laboratory would be the magic-8-ball failure at the rendering layer. The discipline is to keep corrections in code so the operator engages with the substrate, not with a UI affordance.

### §9.3 Why this discipline is structural, not preference

Per `elif_audit_b_user_experience.md` §B4.5 + Article I (Sovereignty Preservation, per `elif_constitutional_layer.md` v0.4):

The Laboratory is a rendering surface over a substrate the operator owns. Permitting the rendering surface to mutate the substrate inverts the relationship: the surface becomes sovereign over the substrate it claims to render. Article I refuses this inversion at the architectural level; the read-only discipline refuses it at the rendering level.

### §9.4 What the Laboratory does NOT do

- No "edit event" affordance.
- No "delete event" affordance.
- No "annotate event" affordance.
- No "upvote pattern" affordance.
- No "save view" affordance (no persisted state per §8).
- No "share Laboratory view" affordance (no public surface per `elif_audit_b_user_experience.md` §B-non-recommendations 9).
- No "export to Limova" affordance (no cross-product runtime coupling per §1.7 of the synthesis).

---

## §10. Rendering LoC budget

### §10.1 The doctrinal anchor

Per `elif_audit_c_media_communication.md` §C7.6:

> Ratio of LoC in rendering layer to LoC in substrate layer. Currently the alpha is 8,424 LoC of substrate + 0 LoC of rendering. At V1, the rendering layer should be a small fraction of substrate LoC (target: rendering ≤ 0.3 × substrate). If rendering LoC exceeds substrate LoC, the system has become a rendering platform with an arbitration backend.

Per `elif_audit_synthesis.md` §1.5 + §3 table:

> Rendering layer ≤ 0.3 × substrate is a defensible bound.

### §10.2 Laboratory LoC tracked separately from V1

The 0.3 × substrate budget is on the combined rendering layer (V1 + Laboratory). The Laboratory is a subset.

PLAUSIBLE FUTURE / CURRENT EVIDENCE. The alpha substrate is 5,129 LoC code + 3,295 LoC tests (per `elif_v0_1_what_remains.md` §6 + `elif_audit_b_user_experience.md`'s reading of the cost-complexity report). Substrate-as-code is the 5,129 LoC. The total rendering budget at 0.3 × substrate is ≤ 1,539 LoC. V1 rendering is projected at ~500-1,000 LoC for CLI / ~1,500-2,500 LoC for minimal HTML (per `elif_audit_c_media_communication.md` §C6.1).

This means the Laboratory v0.1 has roughly **400-1,000 LoC of headroom** within the 0.3 × budget, assuming V1 is at the lower end. If V1 takes the upper end, the Laboratory v0.1 must remain at or near zero LoC of additional rendering machinery — which means the Laboratory must lean heavily on V1's renderer as a substrate.

### §10.3 Tracking discipline

The Laboratory's LoC count is tracked separately from V1's in any implementation. The tracking file (when implementation begins) is a separate `LOC_BUDGET.md` or equivalent that names:
- V1 rendering LoC.
- Laboratory rendering LoC.
- Sum vs. 0.3 × substrate.
- Surplus / deficit.

If the sum exceeds 0.3 × substrate, the implementation has drifted. The discipline is to refuse the next rendering addition, not to relax the budget.

### §10.4 Implication for v0.1 specification

The Laboratory v0.1 is **deliberately small**. The 12 numbered sections of this document specify, in aggregate:
- 4 panels (MemoryLogger observability, Article VII capacity, pattern engagement, deprecation visibility).
- 2 detector tiles (sterile-equilibrium, fragmentation placeholder).
- 1 cross-case timeline.
- 1 case-list view.

That is the entire visible surface. There are no settings pages, no filter builders, no chart configuration menus, no theme selectors, no help overlays. The smallness is structural; it is what makes the LoC budget feasible.

---

## §11. Cross-case pattern visibility — counts ONLY

### §11.1 The discipline

Per `elif_audit_c_media_communication.md` §OD-C-3 + `elif_audit_synthesis.md` §2.2 resolution path:

> The dashboard surfaces frequencies (which axes recur, which uncertainty-sources recur, which hypothesis-shape patterns recur) WITHOUT computing "prediction strength" or "pattern confidence" — the surface presents counts, not predictions.

Per `elif_audit_b_user_experience.md` §B4.3:

> Pattern recognition is rendered as "shape recognized; INVITATION TO TEST" not as "answer."

### §11.2 The closed-set of computations

The Laboratory v0.1 performs exactly these computations over the JSONL substrate, and no others:
- **Counts** of events by `event_type` per case + cross-case.
- **Counts** of events by `change_type` (per `_VALID_CHANGE_TYPES`) per case + cross-case.
- **Counts** of refutation events targeting a given pattern label.
- **Last-engaged timestamp** per pattern label (max of `committed_at_iso` for events referencing the pattern).
- **First-engaged timestamp** per pattern label (min of `committed_at_iso` for events referencing the pattern).
- **Elapsed time per case** (`close` timestamp minus `open` timestamp).
- **Pass-through of `detect_sterile_equilibrium()` verdict and signal counts**.
- **Pass-through of `compute_capacity_metrics()` output**.
- **Pass-through of `find_reuse_candidates()` output** (when invoked on demand).

That is the complete list. Anything beyond — exponential moving averages, regression fits, predicted-next-engagement-count, pattern-similarity computations, embedding-distance scores — is NOT in v0.1 of the Laboratory.

### §11.3 What the discipline forbids at the rendering layer

- No "trending up" or "trending down" arrows beyond raw direction from a literal count delta (and even then, the delta is the literal number, not a styled indicator).
- No "this pattern is gaining engagement" copy.
- No "this case is structurally similar to case X" claim without an explicit invocation of `find_reuse_candidates()` and rendering of its literal score output (the Jaccard score from `memory_logger.py` line 97).
- No machine-learning model trained on event histories.
- No anomaly detection beyond the deterministic sterile-equilibrium detector.

### §11.4 Why counts-only is doctrinally load-bearing

Per `elif_audit_c_media_communication.md` §C7.4 risk #23 (capacity framed as truth):

> Any UI text that reads "the answer is" or "the right decision is" or "based on prior patterns, this is" without explicit refutation framing is doctrine-violating.

A "prediction strength" or "pattern confidence" score is by construction a claim about the future. Any such number is a truth-claim wearing the costume of a measurement. The discipline of counts-only is the rendering layer's structural defence against this drift.

Per the v0.4 risk matrix #36 (referenced via `elif_constitutional_layer.md`): pattern recognition treated as prediction is the structural failure the entire Article VII commitment exists to prevent. The Laboratory v0.1 inherits the structural defence.

---

## §12. Substrate dependencies — G5 prerequisites

### §12.1 What MemoryLogger v0.2 must ship

PLAUSIBLE FUTURE (G5 is a synthesis gate per `elif_audit_synthesis.md` §5; the Laboratory does not open before G5 closes). The substrate prerequisites the Laboratory derives its panels from:

**Cross-case state replay** (per `elif_v0_1_what_remains.md` §8.3 v0.2 acceptance scope). The `MemoryLogger` API must support reading and aggregating events across multiple case directories without the operator providing an explicit list — the existing `_iter_case_dirs()` (line 179) is the foundation; v0.2 must extend this with cross-case state derivation routines that the Laboratory consumes (`compute_capacity_metrics`, `find_reuse_candidates`, `detect_sterile_equilibrium` already exist).

**Pattern-engagement event types**. The existing `_VALID_EVENT_TYPES` already includes `pattern_recognized` (line 56) and `reuse_detected` (line 55); v0.2 must make these emit in live runs, gated by the substrate behavior that produces them (compositional reuse across cases). Until they emit, the pattern panel renders zero rows.

**Capacity-change event types**. The existing `_VALID_CHANGE_TYPES` already includes the five capacity-change kinds (lines 63-69); v0.2 must make these emit in live runs. The Laboratory renders them as they appear; until they emit, the capacity tile renders zero.

**Sterile-equilibrium detector v0.1**. The detector signature already exists in code (`detect_sterile_equilibrium`, line 455). The Phase 5 deliverable per `elif_audit_synthesis.md` §4.5 is the detector tested on cases producing convergent vs divergent shapes. The Laboratory consumes the existing API.

**Either G0=B or G0=A modified**. Per `elif_audit_synthesis.md` §4.0 + §5 gate G2:

> G2 — Position B was chosen at G0, or Position A was modified at Phase 4 to permit Step 10/11 on refuse.

Until Step 10/11 emit on refuse paths, the Laboratory has only the structural events (open / step_committed / refutation / close) to render. With Position A unmodified, the pattern panel and capacity tile remain at zero indefinitely. With Position B (or Position A modified), the content events emit, and the panels become populated.

### §12.2 The Laboratory does not specify HOW v0.2 ships

This is the substrate boundary. The Laboratory v0.1 specification does not specify:
- How `pattern_recognized` events come to be emitted in live runs (that is the `memory_logger` Step 11 content-pass scope per `elif_v0_1_what_remains.md` §1.7).
- How `capacity_change` events come to be emitted (same).
- How cross-case state replay is implemented (v0.2 acceptance scope).
- How the sterile-equilibrium detector is tested on convergent/divergent test cases (Phase 5 deliverable per the synthesis).
- How the refuse-halt question is adjudicated (G0; operator-only per `elif_audit_synthesis.md` §4.0).

These are upstream questions. The Laboratory consumes the answers; it does not produce them.

### §12.3 Behavior when prerequisites are not yet met

The Laboratory v0.1 specification commits to a graceful degradation when its substrate is incomplete:
- If `compute_capacity_metrics()` returns zeros, the panels render zeros. They do NOT render placeholder text like "no data yet" — they render the literal numbers.
- If `find_reuse_candidates()` returns an empty list, the reuse column is empty. No "ELIF is still learning" framing.
- If `detect_sterile_equilibrium()` returns `total_events == 0`, the tile renders `total_events=0` and `sterile_equilibrium=False` (the latter being correct because the detector's `total_events > 0` precondition is not met).
- If no patterns have been recognized, the pattern panel renders zero rows. No "pending patterns" framing.

The graceful-degradation discipline is structural: the Laboratory does not editorialize about the substrate's state. It renders what is there.

---

## §13. Operator decisions queued

The Laboratory v0.1 surfaces three decisions for operator deliberation. Each is named with its trade-offs; none is recommended.

### §13.1 Lab rendering target — HTML / TUI / both?

The Laboratory may be rendered as:
- **HTML** — a static or near-static page served from a local web view. Maps cleanly to the V1 minimal HTML view per `elif_audit_c_media_communication.md` §C6.1 (1,500-2,500 LoC for V1 HTML; Laboratory inherits and extends).
- **TUI** — a terminal-based view. Maps cleanly to the V1 CLI view per the same audit (500-1,000 LoC for V1 CLI).
- **Both** — V1 ships HTML and the Laboratory ships HTML; or V1 ships CLI and the Laboratory ships TUI; or both formats for both surfaces.

Trade-offs:
- HTML imports browser dependency but is more legible for the cross-case timeline and the side-by-side capacity/refutation layout (§3.5 + §4.3).
- TUI is leaner (lower LoC, lower dependency footprint) and naturally supports the stateless-read constraint (§8) but is harder for rendering the panel layouts in the spec.
- Both doubles the LoC budget impact (§10).

The operator decision determines which path closes first under the 0.3 × substrate budget.

### §13.2 Pattern naming convention — free-text vs closed-set IDs?

When a `pattern_recognized` event is emitted, the pattern referenced may be:
- **Free-text labels** — operators (or the MemoryLogger emission code) attach a descriptive string. Pro: expressive. Con: drift, synonym proliferation, the closed-set discipline that protects `_VALID_EVENT_TYPES` does not apply to pattern names.
- **Closed-set pattern IDs** — patterns are members of a registered closed set (analogous to `_VALID_EVENT_TYPES`), with adding a new pattern requiring doctrine revision. Pro: discipline-preserving, anti-monoculture-compatible. Con: requires a pattern-registration ceremony that may slow live runs.

PLAUSIBLE FUTURE / SPECULATION boundary. Per `elif_audit_c_media_communication.md` §C1.10 + §C4.1, the closed-set discipline is favored when the cardinality is small and stable. At v0.1 of the Laboratory the operator has neither evidence of pattern cardinality nor of stability. The decision is queued; it gates the pattern-panel design at implementation time.

### §13.3 Deprecation event display prominence

Per §6, deprecation events are first-class. The granularity question is:
- **Main-view tile** — a dedicated deprecation tile on the Laboratory's main view, at equal prominence to the capacity tile.
- **Pattern-row inline** — the deprecation status is shown only on the pattern row in the pattern panel (no separate tile).
- **Both** — main-view tile AND pattern-row inline.

Trade-offs:
- Main-view tile is more prominent and harder to miss; risks crowding the main view.
- Pattern-row inline is leaner; risks the deprecation events being missed by an operator browsing the capacity tile only.
- Both is the maximally defensive choice; costs LoC.

The operator decision determines the layout commitment.

---

## §14. What this specification does NOT include

This section is load-bearing for the non-expansionary stance. It mirrors the synthesis §6 discipline at Laboratory scope.

1. **No implementation.** This is a specification; no code. The implementation cannot begin before G5 closes per `elif_audit_synthesis.md` §5.

2. **No specification of the cross-case state replay mechanism itself.** That is MemoryLogger v0.2 scope per `elif_v0_1_what_remains.md` §8.3 and `elif_audit_synthesis.md` §4.5. The Laboratory consumes the v0.2 outputs; it does not specify how v0.2 produces them.

3. **No multi-operator dashboard.** Multi-operator surfaces are V3 (per the synthesis §2.4 resolution path) and explicitly SPECULATION per `elif_audit_c_media_communication.md` §C6.3. The Laboratory v0.1 is single-operator. Adding multi-operator infrastructure requires Phase 9 of the synthesis roadmap to open, which may never happen.

4. **No prediction computation.** No "pattern confidence," no "prediction strength," no "trend forecast," no machine-learning model fit on event histories. Counts-only per §11.

5. **No confidence computation.** No "case quality score," no "operator skill metric," no "system health score." There is no system-level scoring of any kind.

6. **No audio surface.** Per `elif_audit_b_user_experience.md` §B2.7 and `elif_audit_c_media_communication.md` §C3.10, audio is DECORATIVE and structurally rejected. The Laboratory has no audio output, no narrated tour, no spoken summaries.

7. **No video surface.** Per the same audits §B2.8 and §C3.11, video is DECORATIVE and structurally rejected. The Laboratory has no video output, no animated transitions beyond minimal CSS, no recorded walkthroughs.

8. **No chatbot surface.** Per `elif_audit_b_user_experience.md` §B1.1 and the synthesis §1.1, chatbot is ACTIVELY COUNTERPRODUCTIVE. The Laboratory does not have a "ask the lab" affordance, a natural-language query interface, or a conversational front-end.

9. **No LLM-prose summary layer.** Per the synthesis §1.5 + `elif_audit_b_user_experience.md` §B-non-recommendations 4, the structured output IS the deliverable. The Laboratory does not produce prose summaries of the panel contents. Operators read the counts directly.

10. **No simulation workspace inside the Laboratory.** Per the synthesis §1.1 + `elif_audit_b_user_experience.md` §B1.5, simulation belongs outside ELIF. The Laboratory does not host simulation outputs.

11. **No world-model integration.** Per the synthesis §4.7 + §4.8, world-model integration is Phase 7-8 and may never open. The Laboratory v0.1 specification does not pre-empt these phases. There is no "simulator-anchored capacity" tile in v0.1; that is a Phase 8 question deferred until G8/G9 close.

12. **No knowledge graph.** Per the synthesis §3 and `elif_audit_b_user_experience.md` §B-non-recommendations 11, knowledge-graph framing is truth-accumulation framing and is forbidden. The Laboratory does not produce a graph of patterns related to other patterns.

13. **No leaderboard, hall of fame, or prestige surface.** Per `elif_audit_b_user_experience.md` §B4.3 and §5.4 above. The Laboratory has no top-N pattern view, no most-engaged-shape view, no operator-engagement leaderboard.

14. **No cross-product runtime coupling.** Per the synthesis §1.7. The Laboratory does not consume from OSG, Limova, Continuity Layer, or any other organ. The data substrate is exclusively the MemoryLogger JSONL.

15. **No public-facing variant.** Per `elif_audit_b_user_experience.md` §B-non-recommendations 9. The Laboratory is operator-facing. There is no shared-link affordance, no public view, no embed code.

16. **No persistent UI state.** Per §8. There is no "save view" button, no bookmark feature, no last-viewed-position memory. Every render is a fresh derivation.

17. **No write-back affordance of any kind.** Per §9. Corrections go through `MemoryLogger.emit_correction()` in code.

18. **No new event types, change types, or schema fields.** The closed-sets at `memory_logger.py` lines 47-69 are frozen at v0.4. The Laboratory consumes them; it does not extend them.

19. **No new procedure step, no new component, no new Article.** Per the synthesis §1.2 + the operator's absolute constraints. The Laboratory is a rendering of the existing substrate.

20. **No Laboratory v0.2 / v0.3 roadmap.** Per the synthesis §6 non-recommendation 6. This specification is for v0.1. Future versions, if any, are gated on evidence not yet held; specifying them now would be the canonical momentum-capture failure.

---

## §15. Closing note

The Laboratory v0.1 is small, precise, and substrate-anchored. It does not invent. It renders.

What it renders is what the MemoryLogger v0.2 will produce — counts of events, counts of pattern engagements, counts of refutations, the verdict of the sterile-equilibrium detector, the literal output of `compute_capacity_metrics()`, the literal output of `find_reuse_candidates()`. The rendering is a translation from JSONL to a per-surface layout; the structured substrate is the deliverable, and the Laboratory is its cross-case translation.

What it does not render is what the audits independently rejected: predictions, validations, "what ELIF has learned," knowledge graphs, hall-of-fame patterns, leaderboards, audio briefings, video summaries, conversational interfaces, simulation outputs, multi-operator dashboards, public surfaces. These are PERMANENTLY out of scope under v0.4 doctrine.

What it commits to is structural: the Laboratory is stateless. The operator can leave and return. The substrate is read-only from the Laboratory's perspective. Corrections go through code. Counts replace predictions. INVITATION TO TEST replaces VALIDATED. The capacity-vs-truth distinction is preserved at vocabulary, layout, and framing levels — not as preference, as structural commitment.

The substrate that produces all of this is already substantially present in `src/elif_v0_1/components/memory_logger.py`. The 569-line MemoryLogger implementation already has `read_case_state`, `find_reuse_candidates`, `compute_capacity_metrics`, `emit_correction`, and `detect_sterile_equilibrium` as committed API surfaces with their semantics specified inline. The Laboratory v0.1 consumes these surfaces; it does not extend them.

The Laboratory will open when G5 closes. Until then, this specification stays on the shelf.

---

**End of specification.**
