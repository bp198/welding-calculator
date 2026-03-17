import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Welding Engineering Toolbox",
    page_icon="🔩",
    layout="wide"
)

st.title("🔩 Welding Engineering Toolbox")
st.markdown("### Your professional welding reference and calculation platform")
st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(height=180, border=True):
        st.markdown("""
        ### 🔥 Heat Input Calculator
        Calculate welding heat input according to **EN 1011** standard.
        Supports MMA, MIG/MAG, TIG, SAW and FCAW processes.
        """)
    if st.button("Open Calculator →", use_container_width=True):
        st.switch_page("pages/1_Heat_Input.py")

with col2:
    with st.container(height=180, border=True):
        st.markdown("""
        ### 📋 AWS D1.1 WPS Reference
        Interactive prequalified WPS requirements lookup.
        Find electrode, current, bead thickness limits instantly.
        """)
    if st.button("Open WPS Reference →", use_container_width=True):
        st.switch_page("pages/2_AWS_D1_WPS.py")

st.divider()
st.caption("Built by Babak Pirzadi — Welding Engineer & Python Developer")

# 🧪 THIS SECTION IS FOR TEST ONLY