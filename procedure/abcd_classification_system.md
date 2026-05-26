# A/B/C/D Classification System

Every procedure step and every observed behavior must be tagged with one of four categories.

## Tags

| Tag | Meaning | Example |
|---|---|---|
| **A** | Canonical component behavior | Frame validation → Frame Validator |
| **B** | Candidate component behavior — may graduate, may collapse, may be removed | Hidden assumption extraction |
| **C** | Procedural artifact / execution-only behavior — not architecture-worthy unless proven otherwise | Recommendation + confidence packet |
| **D** | Candidate removal / non-persistent behavior — may be killed if it never engages | (none currently) |

## Reclassification pressure

After each benchmark case, every B-tagged step must be classified along:

- **engaged / dormant / collapses into component X / emerges as distinct / unresolved**
- **frequency: 0/3, 1/3, 2/3, 3/3**

After each benchmark case, every D-tagged behavior must be classified along:

- **absent across cases / portable to prompting / redundant with another component / operationally low-value / removal recommended / removal deferred**

## Retention bars

- A C-tagged behavior only graduates to B/A if it produces a behavior that survives across cases, is not reproducible through structured prompting alone, and appears architecture-dependent rather than stylistic.
- A B-tagged behavior only graduates to A if it engages in ≥2/3 cases AND produces operational differentiation.
- A component (A) demotes to D if it never engages across the case set.

## Why this matters

Without the four-category system, the architecture can only expand or stabilize — never compress. That recreates the exact drift problem the benchmark process was designed to prevent.

See `doctrine/02_locked_rules.md` Rule 2 — Failure-Permitted Architecture.
