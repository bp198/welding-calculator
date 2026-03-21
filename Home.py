import streamlit as st

st.set_page_config(
    page_title="Welding Engineering Toolbox",
    page_icon="🔩",
    layout="wide"
)

st.title("🔩 Welding Engineering Toolbox")
st.markdown("### Professional welding reference, calculation, and AI assistance platform")
st.markdown(
    "Built on **AWS D1.1/D1.1M:2025**, **EN 1011**, and **EN ISO 15614** — "
    "covering prequalified WPS requirements, heat input, cooling rate analysis, and AI-assisted procedure interpretation."
)
st.divider()

# ── THREE TOOL CARDS ──────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(height=220, border=True):
        st.markdown("### 🔥 Heat Input Calculator")
        st.markdown(
            "Calculate net heat input per **EN 1011-1** with process efficiency correction. "
            "Supports SMAW, GMAW, FCAW, SAW, and TIG. "
            "Includes multi-pass comparison and interactive charts."
        )
    if st.button("Open Heat Input Calculator →", use_container_width=True):
        st.switch_page("pages/1_Heat_Input.py")

with col2:
    with st.container(height=220, border=True):
        st.markdown("### 📋 AWS D1.1 WPS Reference")
        st.markdown(
            "Interactive lookup for **AWS D1.1/D1.1M:2025** Clause 5 prequalified WPS requirements. "
            "Electrode limits, bead thickness, preheat tables, base metals, filler metals, "
            "WPS generator, and RAG-powered AI assistant."
        )
    if st.button("Open WPS Reference & AI Assistant →", use_container_width=True):
        st.switch_page("pages/2_AWS_D1_WPS.py")

with col3:
    with st.container(height=220, border=True):
        st.markdown("### 🌡️ t8/5 Cooling Rate & HAZ Analysis")
        st.markdown(
            "Calculate HAZ cooling time t8/5 per **EN 1011-2** with automatic 2D/3D formula selection. "
            "Predicts HAZ hardness, minimum preheat temperature, "
            "and hydrogen cracking risk for your specific welding conditions."
        )
    if st.button("Open t8/5 Calculator →", use_container_width=True):
        st.switch_page("pages/3_t85_Calculator.py")

st.divider()

# ── STANDARDS COVERAGE ────────────────────────────────────────────────────────
st.subheader("📚 Standards Coverage")

s1, s2, s3 = st.columns(3)

with s1:
    st.markdown("""
**AWS Standards**
- AWS D1.1/D1.1M:2025 — Structural Welding Steel
- AWS D1.1/D1.1M:2020 — Previous edition reference
""")

with s2:
    st.markdown("""
**EN ISO Standards**
- EN ISO 15614-1:2017 — WPS Qualification
- BS EN 1011-1:2009 — Welding Recommendations
- BS EN 1011-2 — Arc Welding of Ferritic Steels
- BS EN 1011-3:2018 — Arc Welding of Stainless Steels
""")

with s3:
    st.markdown("""
**AI Knowledge Base**
- 6,700+ indexed standard clauses
- RAG-powered clause retrieval
- LLaMA 3.3 70b via Groq API
- IWE-level expert system prompt
""")

st.divider()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.caption(
    "Built by **Babak Pirzadi** — Welding Engineer | "
    "Master's student in Engineering Technology for Strategy and Security, University of Genova | "
    
)