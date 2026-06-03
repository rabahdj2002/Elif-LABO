# ELIF Case Intake Template (v1.0)
<!-- 
This is the standard interface for "Case Analysis." 
The goal is to provide ELIF with a "Bundle" to analyze.
Fill out the sections below. Be precise. Avoid marketing language.
-->

## 0. Meta Information
- **Case Name:** [Title of the decision/proposal]
- **Author:** [Name/Role]
- **Security/Priority Level:** [Low/Medium/High/Critical]

---

## 1. The Proposition (The "Bundle")
**Provide a 1-paragraph summary of the proposed action or the question being asked.**
> *e.g., "The 'Global Electroculture Pilot' proposes a $50M investment in magneticulture, electroculture antenna arrays, and high-frequency soil stimulation across 10 regions, combined with a new research agency to oversee the deployment."*

---

## 2. Core Constraints (The "Locked Rules")
**What rules MUST NOT be broken? What are the hard boundaries?**
- [Constraint 1: e.g., "Must be budget neutral by Year 3"]
- [Constraint 2: e.g., "Must not rely on non-peer-reviewed 'quantum' soil theories"]
- [Constraint 3]

---

## 3. High-Fidelity Details (The "Substrate")
**Briefly list the specific components within the proposal.**
- **Component A:** [Entity/Method]
- **Component B:** [Entity/Method]
- **Component C:** [Entity/Method]

---

## 4. Current Uncertainties
**What is your gut feeling about where this proposal is "weak" or "blurry"?**
- [Uncertainty 1: e.g., "I'm not sure if Method A and Method B actually work on the same principles."]
- [Uncertainty 2: e.g., "The ROI seems based on field-scale data we don't actually have yet."]

---

## 5. Decision-Maker Intention
**What does "success" look like for this analysis?**
- [ ] **Verdict Only:** Just tell me Yes/No/Wait (Decision Room).
- [ ] **Structural Analysis:** Tell me how to split the bundle (Exploration Lens).
- [ ] **Red-Teaming:** Find the "Object Drift" (where we might lie to ourselves later).

---

### [Internal Use Only] ELIF Configuration
- **Model:** `claude-3-5-sonnet-20240620` (default)
- **Framework:** `elif_v0_1`
- **Doctrines:** `doctrine/02_locked_rules.md`, `doctrine/03_preserve_over_chase.md`
