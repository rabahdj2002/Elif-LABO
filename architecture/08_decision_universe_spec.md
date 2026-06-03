# ELIF DECISION UNIVERSE: VISUAL SPECIFICATION V1.0

## 1. PHENOMENOLOGICAL MAPPING (THE METAPHOR)

| ELIF Concept | Celestial Entity | Visual Property |
| :--- | :--- | :--- |
| **Core Inquiry** | **Singularity / Pulsar** | Central gravity source. Pulses based on "Engine Activity". Core Question text floats in a halo around it. |
| **Reasoning Stages** | **Planets** | 11 Planets in 3 orbital rings. Size = Data Density. Color = Status (Blue: Active, Green: Stable, Red: Conflict). |
| **Hypotheses** | **Moons** | Orbiting their parent Stage. Number of moons = Number of parallel possibilities. Brightness = Confidence. |
| **Logic Branches** | **Wormholes** | Portals leading to "Parallel Universes" (Alternative Inquiries). Visually represented as warping space-time lines. |
| **Constraints** | **Nebula Clouds** | Viscous regions that slow down the "Engine Particle" movement. Color-coded by constraint type (Bio, Admin, Tech). |
| **Uncertainty** | **Dark Matter / Fog** | Unexplored sectors are shrouded in shifting gas clouds. As the engine completes steps, the "fog" dissipates. |
| **Evidence Gaps** | **Asteroid Belts** | Fragmented knowledge regions that require "Stability" (Audit) to clear. |
| **Solutions** | **Constellations** | Connecting the "Verdict" planets into a final meaningful pattern at the edge of the system. |

## 2. ORBITAL STRATIGRAPHY

### Ring 1: The Core Logic (Inner)
* **Planet 01: Frame Validator**
* **Planet 02: Object Decomposer**
* **Planet 03: Normalization Layer**
* *Visuals: High rotational speed, tight orbit, glowing core.*

### Ring 2: The Empirical Mantle (Middle)
* **Planet 04: Hypothesis Construction**
* **Planet 05: Falsification Design**
* **Planet 06: Multi-Scale Propagation**
* **Planet 07: Outside-Frame Generation**
* *Visuals: Stable movement, multiple moons (Hypotheses), visible evidence rings.*

### Ring 3: The Verdict Rim (Outer)
* **Planet 08: Stage-Gated Roadmap**
* **Planet 09: Constraint Synthesis**
* **Planet 10: Verdict Engine**
* **Planet 11: Audit / Drift Layer**
* *Visuals: Slow, majestic orbits. This is where the constellation forms.*

## 3. USER INTERACTION FLOW (EXPLORATORY NAVIGATION)

1. **The Grand Overview (Galaxy View)**: Initial zoom level showing all 11 planets and the Pulsar.
2. **The Descent (Planet View)**: Clicking a planet performs a "Smooth Zoom" (Cinematic Transition). Camera enters the planet's atmosphere (Step Details page).
3. **The Pivot (Wormhole Travel)**: Clicking a "Divergence Branch" triggers a camera pan through a wormhole animation, landing in a new "Parallel Universe" (The Branch Detail).
4. **The Scan (Telemetry Overlay)**: Hovering over a planet shows a minimal HUD with "Confidence %", "Evidence Weight", and "Active Constraints".

## 4. VISUAL HIERARCHY & PALETTE

* **Background**: Deep Space (#020617) with static stars and shifting nebulas.
* **Core Inquiry**: White/Blue (#3b82f6) with high-intensity bloom.
* **Active Status**: Electric Blue / Cyan.
* **Conflict / Decomposition**: Pulsing Violet (#a855f7).
* **Resolved / Stable**: Emerald Green (#10b981).
* **Uncertainty**: Charcoal / Smoke Gray.

## 5. ANIMATION CONCEPTS
* **Engine Pulse**: When `run_engine_pulse` is active, the Pulsar expands and shoots "Logic Particles" out to the planets.
* **Gravitational Bending**: Planet paths slightly deviate toward "Heavy Constraints".
* **Nebula Drift**: Dust clouds move slowly in the background to prevent the UI from feeling static.

## 6. COMPONENT HIERARCHY (TECH STACK)
1. **SystemContainer (Three.js/Canvas)**: Orchestrates the 3D/2D space.
2. **CelestialBody (Planet/Moon)**: Reusable object with status-based shaders.
3. **GravityField (Constraint Shader)**: Visual distortion around specific nodes.
4. **HUD (Tailwind Overlay)**: Data transparency and copy-to-clipboard tools.
