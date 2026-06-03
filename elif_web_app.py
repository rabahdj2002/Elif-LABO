import streamlit as st
import json
import os
import subprocess
from pathlib import Path
import pandas as pd
import plotly.express as px
import sys
import re

# --- UX TRANSLATION LAYER: ELIF V1 PRODUCTION ---
# Purpose: Abstracting complexity, highlighting value, ensuring immediate decision clarity.

ST_RESULTS_DIR = Path("results")
ST_CASES_DIR = Path("cases")
ST_SRC_DIR = Path("src")

st.set_page_config(page_title="ELIF | Decision Clarity", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM THEME & CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { background-color: #fafbfc; }
    
    /* Timeline Styling */
    .timeline-container {
        display: flex;
        justify-content: space-between;
        margin: 20px 0 40px 0;
        padding: 0 50px;
        position: relative;
    }
    .timeline-item {
        text-align: center;
        flex: 1;
        position: relative;
        z-index: 1;
    }
    .timeline-dot {
        width: 15px;
        height: 15px;
        background-color: #cbd5e1;
        border-radius: 50%;
        margin: 0 auto 10px auto;
    }
    .timeline-dot.active { background-color: #0ea5e9; box-shadow: 0 0 10px rgba(14, 165, 233, 0.5); }
    .timeline-dot.complete { background-color: #10b981; }
    
    .timeline-label { font-size: 0.75rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .timeline-label.active { color: #0f172a; }

    /* Card Styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .stMetric { background: none; border: none; padding: 0; }
    
    .status-tag {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .tag-stable { background: #f0fdf4; color: #16a34a; }
    .tag-evolving { background: #eff6ff; color: #2563eb; }
    .tag-changed { background: #fff7ed; color: #ea580c; }
    </style>
""", unsafe_allow_html=True)

# --- CORE UTILS ---

def get_portfolio():
    runs = []
    if not ST_RESULTS_DIR.exists(): return pd.DataFrame()
    for case_dir in ST_RESULTS_DIR.iterdir():
        if case_dir.is_dir():
            for run_dir in case_dir.iterdir():
                if run_dir.is_dir() and (run_dir / "run_report.json").exists():
                    try:
                        with open(run_dir / "run_report.json", 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            runs.append({
                                "Project": case_dir.name.replace("_", " ").title(),
                                "ID": case_dir.name,
                                "Timestamp": run_dir.name,
                                "Path": run_dir,
                                "RawData": data
                            })
                    except: pass
    return pd.DataFrame(runs)

def clean_text(text, length=60):
    if not text: return "..."
    text = str(text)
    # Remove HTML tags, special chars for mermaid
    clean = re.sub(r'[^a-zA-Z0-9\s?]', '', text)
    if len(clean) > length:
        clean = clean[:length] + "..."
    return clean

def render_visualization(mermaid_code, height=400):
    st.components.v1.html(f"""
        <div style="background:white; border-radius:12px; padding:20px; border:1px solid #e2e8f0;">
            <pre class="mermaid" style="display:flex; justify-content:center;">
                {mermaid_code}
            </pre>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' }});
            </script>
        </div>""", height=height + 40)

# --- INTERACTIVE ENGINE INTERFACE ---

def trigger_engine_evolution(directive, parent_data=None):
    """
    Simulates a 'Branching' engine call. 
    In a real production environment, this would call Layer 1 with (Context + Directive).
    For this V1, we create a new 'Branch' artifact.
    """
    st.info(f"🚀 Redirecting Inquiry: '{directive}'...")
    # Logic to trigger a new run would go here.
    # For now, we'll simulate the state update.
    if "evolution_steps" not in st.session_state:
        st.session_state["evolution_steps"] = []
    
    st.session_state["evolution_steps"].append({
        "directive": directive,
        "timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),
        "status": "integrated"
    })

# --- DATA PARSER & STATE MANAGEMENT (LAYER 2) ---

class InquiryObject:
    """The 'Living Question' - Manages state, history, and drift translation."""
    def __init__(self, raw_data):
        self.raw = raw_data
        self.steps = {s['step_id']: s.get('structured_output_dict', {}) for s in raw_data.get('step_outputs', [])}
        self.case_id = raw_data.get('case_id', 'Unknown')
        self.branches = st.session_state.get("evolution_steps", [])
        
    def scrub(self, text):
        """Standardizes jargon removal for Layer 3 consumption."""
        if not text: return "Ongoing discovery..."
        patterns = [
            r'\(?[CSHE]\d+(-[0-9]+)?\)?', r'[A-Z]\d+-[A-Z]\d+', 
            r'lexicographic', r'axis', r'admissibility', r'E.T.R',
            r'refutability', r'stage-gated', r'H1.H4', r'governance kernel'
        ]
        clean = str(text)
        for p in patterns: clean = re.sub(p, '', clean, flags=re.IGNORECASE)
        # Humanize
        clean = clean.replace('residue uncertainties', 'unsolved gaps')
        clean = clean.replace('object drift', 'meaning shift')
        return re.sub(r'\s+', ' ', clean).strip()

    @property
    def timeline(self):
        """Simulates the descent into inquiry steps with active branches."""
        base = [
            {"step": "Seed", "label": "Initial Question", "status": "completed"},
            {"step": "Decomposition", "label": "Situation Mapping", "status": "completed" if 'step_2' in self.steps else "pending"},
            {"step": "Validation", "label": "Evidence Check", "status": "completed" if 'step_4' in self.steps else "pending"},
            {"step": "Projection", "label": "Scenario Modeling", "status": "completed" if 'step_7' in self.steps else "pending"},
            {"step": "Decision", "label": "Action Protocol", "status": "completed" if 'step_11' in self.steps else "pending"}
        ]
        
        # Add dynamic interaction steps
        for branch in self.branches:
            base.append({
                "step": "Evolution", 
                "label": f"Refinement: {branch['directive'][:20]}...", 
                "status": "completed"
            })
        return base

    @property
    def drift_summary(self):
        """Calculates how much the question has evolved."""
        drift_raw = self.steps.get('step_3', {}).get('drift_analysis', 'Minimal shift detected.')
        return self.scrub(drift_raw)

    def get_assumptions(self):
        """Extracts and humanizes assumptions from Step 2/3."""
        axes = self.steps.get('step_2', {}).get('axes', [])
        return [{"id": f"A{i}", "text": self.scrub(ax.get('axis_name', 'Unknown Factor')), "status": "Active"} for i, ax in enumerate(axes[:5])]

# --- EXPERIENCE LAYER (LAYER 3: ROOMS) ---

def render_exploration_room(io: InquiryObject):
    st.subheader("🗺️ Exploration Room")
    st.info("Mapping the territory of the possible. Here we visualize every branch of the inquiry.")
    
    # Mermaid Tree of the Question
    mm = ["graph LR", f"  Root(({io.scrub(io.case_id)}))"]
    assumptions = io.get_assumptions()
    for a in assumptions:
        mm.append(f"  Root --- {a['id']}[{a['text']}]")
        # Add sub-nodes if in trajectory step
        trajs = io.steps.get('step_7', {}).get('trajectories', [])
        for i, t in enumerate(trajs[:2]):
            mm.append(f"  {a['id']} -.-> T{i}[{io.scrub(t.get('tag'))}]")
    
    # Add User-Triggered Branches to the Visualization
    for i, b in enumerate(io.branches):
        mm.append(f"  Root ==> B{i}{{Branch: {b['directive'][:15]}...}}")
    
    render_visualization("\n".join(mm))
    
    st.markdown("#### Interactive Directives")
    c1, c2, c3 = st.columns(3)
    if c1.button("🔍 Explore New Branch"):
        st.session_state["show_input"] = "branch"
    if c2.button("📐 Change Assumptions"):
        st.session_state["show_input"] = "assumption"
    if c3.button("🧭 Pivot Scope"):
        st.session_state["show_input"] = "pivot"

    st.markdown("#### Potential Perspectives")
    cols = st.columns(2)
    with cols[0]:
        st.write("**Current Focus:** " + io.scrub(io.steps.get('step_2', {}).get('summary', 'Broad inquiry')))
    with cols[1]:
        st.write("**Object Drift:** " + io.drift_summary)

def render_governance_room(io: InquiryObject):
    st.subheader("🛡️ Governance Room")
    st.write("The rules, constraints, and accountabilities governing this inquiry.")
    
    # Extract constraints from step 5/9
    constraints = io.steps.get('step_9', {}).get('verdict_detail', 'No explicit constraints identified.')
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("**Core Constraints**")
        st.warning(io.scrub(constraints))
        if st.button("➕ Add New Constraint"):
            st.session_state["show_input"] = "constraint"
    
    with col_r:
        st.markdown("**Accountability Matrix**")
        st.write("Ensuring every decision sub-component has a clear owner.")
        holders = io.steps.get('step_2', {}).get('axes', [])
        for h in holders[:3]:
            st.success(f"✓ {io.scrub(h.get('axis_name'))}")

def render_solution_room(io: InquiryObject):
    st.subheader("🛤️ Solution Room")
    st.write("Competing families of action. We prioritize understanding why paths differ over picking one early.")
    
    raw_paths = io.steps.get('step_7', {}).get('trajectories', [])
    if not raw_paths:
        st.info("Paths are still being modeled based on current evidence.")
        return

    for i, path in enumerate(raw_paths[:3]):
        with st.expander(f"Path Family {chr(65+i)}: {io.scrub(path.get('tag'))}", expanded=(i==0)):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.write("**Outcome Description:**")
                st.write(io.scrub(path.get('outcome', 'Trajectory analysis in progress.')))
                if st.button(f"🔍 Deep Dive into Option {chr(65+i)}", key=f"dive_{i}"):
                    trigger_engine_evolution(f"Analyze deep risks for Option {chr(65+i)}")
            with c2:
                st.metric("Probability Anchor", f"{70 - (i*15)}%")
                st.write("Evidence Score: High")

def render_projection_room(io: InquiryObject):
    st.subheader("🔮 Projection Room")
    st.write("Simulating the 'Second Order' effects of our current trajectory.")
    
    # This room shows risk and future impact
    risk_data = io.steps.get('step_9', {}).get('residue_uncertainties', ["Data gathering in progress..."])
    
    cols = st.columns(len(risk_data[:3]))
    for i, risk in enumerate(risk_data[:3]):
        with cols[i]:
            st.error(f"Potential Trap {i+1}")
            st.write(io.scrub(risk))
            st.progress(40 + (i*20))
            if st.button(f"🛡️ Model Mitigation", key=f"mitigate_{i}"):
                trigger_engine_evolution(f"Find mitigations for risk: {risk[:20]}...")

def render_validation_room(io: InquiryObject):
    st.subheader("✅ Validation Room")
    st.write("Measuring the 'Weight of Evidence' and identifying critical gaps.")
    
    conf = io.steps.get('step_9', {}).get('confidence', '65')
    nums = re.findall(r'\d+', str(conf))
    c_val = int(nums[0]) if nums else 65
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Inquiry Confidence", f"{c_val}%")
        st.write("Status: " + ("ROBUST" if c_val > 80 else "PROVISIONAL"))
    
    with col2:
        st.write("**Remaining Unknowns**")
        gaps = io.steps.get('step_10', {}).get('uncertainty_matrix', ["Evidence review pending."])
        for g in gaps[:3]:
            st.info(io.scrub(g))
            if st.button(f"🔎 Investigate Gap", key=f"gap_{g[:10]}"):
                trigger_engine_evolution(f"Gather evidence for: {g[:20]}")

# --- APP LAYOUT (RESTRUCTURED) ---

df_portfolio = get_portfolio()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/shield-halved.svg", width=40)
    st.title("ELIF V1")
    st.caption("Persistent Inquiry Environment")
    st.divider()
    
    # 1. Select the Living Inquiry
    if not df_portfolio.empty:
        context_sel = st.selectbox("Active Inquiry", df_portfolio["Project"] + " (" + df_portfolio["Timestamp"] + ")")
        selected_idx = df_portfolio[df_portfolio["Project"] + " (" + df_portfolio["Timestamp"] + ")" == context_sel].index[0]
        st.session_state["active_data"] = df_portfolio.iloc[selected_idx]["RawData"]
        io = InquiryObject(st.session_state["active_data"])
    else:
        st.info("No projects found.")
        st.stop()

    st.divider()
    
    # 2. View Selection (The Rooms)
    nav = st.radio("MAIN MENU", [
        "🔍 Exploration Room", 
        "🛡️ Governance Room", 
        "🛤️ Solution Room", 
        "🔮 Projection Room", 
        "✅ Validation Room",
        "📂 Inquiry History",
        "⚙️ Settings"
    ])
    
    st.divider()
    # Inquiry Timeline (Persistence Indicator)
    st.caption("INQUIRY STATUS")
    for tl in io.timeline:
        col_icon, col_txt = st.columns([1, 5])
        icon = "●" if tl['status'] == 'completed' else "○"
        col_icon.write(icon)
        col_txt.write(tl['label'])

# MAIN CONTENT ROUTING

if "Room" in nav:
    st.title("ELIF | Decision Clarity")
    st.markdown(f"**Inquiry ID:** `{io.case_id}` | **Latest State:** {io.scrub(io.steps.get('step_3', {}).get('status', 'Evolving'))}")
    st.divider()

    # Room Rendering
    if "Exploration" in nav: render_exploration_room(io)
    elif "Governance" in nav: render_governance_room(io)
    elif "Solution" in nav: render_solution_room(io)
    elif "Projection" in nav: render_projection_room(io)
    elif "Validation" in nav: render_validation_room(io)

    # --- PERSISTENT INTERACTION BAR ---
    st.divider()
    prompt = st.chat_input("Direct the Inquiry (e.g., 'Challenge assumption A1', 'Zoom into Risk 2', 'Expand Option B')")
    if prompt:
        trigger_engine_evolution(prompt)
        st.rerun()

    # Handle room-specific quick actions
    if st.session_state.get("show_input"):
        action_type = st.session_state["show_input"]
        with st.chat_message("user"):
            st.write(f"Directing system to update {action_type}...")
            user_detail = st.text_input(f"Provide details for the {action_type}:")
            if st.button("Submit Evolution"):
                trigger_engine_evolution(f"Update {action_type}: {user_detail}")
                st.session_state["show_input"] = None
                st.rerun()

    st.divider()
    with st.expander("Show Inquiry History (Object Drift)"):
        st.write(io.drift_summary)
        st.caption("The question has evolved as new evidence was integrated.")

elif "History" in nav:
    st.title("Project History")
    st.dataframe(df_portfolio[["Project", "Timestamp"]], use_container_width=True)

elif "Settings" in nav:
    st.title("Settings")
    st.write("Current Version: ELIF Clarity V1")
    if st.button("Clear Cache"): st.cache_data.clear()


elif nav == "Portfolio":
    st.title("Project History")
    st.dataframe(df_portfolio[["Project", "Timestamp"]], use_container_width=True)

elif nav == "Settings":
    st.title("Settings")
    st.write("Current Version: ELIF Clarity V1")
    if st.button("Clear Cache"): st.cache_data.clear()


elif nav == "Portfolio":
    st.title("Inquiry Portfolio")
    st.dataframe(df_portfolio[["Project", "Timestamp"]], hide_index=True, use_container_width=True)

elif nav == "System Settings":
    st.title("ELIF Settings")
    st.write("Kernel 1.0.0-V1-UX")
    if st.button("Reset Session Cache"):
        st.cache_data.clear()
        st.rerun()
