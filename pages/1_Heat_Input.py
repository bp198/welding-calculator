import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Welding Heat Input Calculator", page_icon="🔥", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        .result-box {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
        .safe { background-color: #1a3a2a; color: #00ff88; }
        .warning { background-color: #3a3a1a; color: #ffdd00; }
        .danger { background-color: #3a1a1a; color: #ff4444; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🔥 Welding Heat Input Calculator")
st.markdown("Calculate heat input according to **EN 1011** standard")
st.divider()

# --- INPUTS ---
col1, col2 = st.columns(2)

with col1:
    voltage = st.number_input("⚡ Voltage (V)", min_value=1.0, max_value=100.0, value=24.0, step=0.5)
    current = st.number_input("🔌 Current (A)", min_value=1.0, max_value=1000.0, value=200.0, step=5.0)

with col2:
    speed = st.number_input("💨 Travel Speed (mm/min)", min_value=1.0, max_value=2000.0, value=300.0, step=10.0)
    efficiency = st.selectbox("🔧 Welding Process (Thermal Efficiency)", 
                               ["MMA - 0.80", "MIG/MAG - 0.80", "TIG - 0.60", "SAW - 1.00", "FCAW - 0.80"])

# --- EXTRACT EFFICIENCY VALUE ---
k = float(efficiency.split("- ")[1])

# --- CALCULATE ---
if st.button("⚙️ Calculate Heat Input", use_container_width=True):
    heat_input = (voltage * current * 60 * k) / (speed * 1000)
    
    st.divider()
    st.subheader("📊 Results")
    
    # Show main result
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Voltage", f"{voltage} V")
    col_b.metric("Current", f"{current} A")
    col_c.metric("Travel Speed", f"{speed} mm/min")
    
    st.divider()
    
    # Color-coded result
    if heat_input < 0.5:
        st.markdown(f'<div class="result-box danger">⚠️ Heat Input: {heat_input:.3f} kJ/mm — TOO LOW</div>', 
                    unsafe_allow_html=True)
        st.warning("Heat input is below recommended minimum. Risk of lack of fusion.")
    elif heat_input <= 2.5:
        st.markdown(f'<div class="result-box safe">✅ Heat Input: {heat_input:.3f} kJ/mm — OPTIMAL</div>', 
                    unsafe_allow_html=True)
        st.success("Heat input is within the recommended range for most structural steels.")
    else:
        st.markdown(f'<div class="result-box warning">⚠️ Heat Input: {heat_input:.3f} kJ/mm — TOO HIGH</div>', 
                    unsafe_allow_html=True)
        st.warning("Heat input exceeds 2.5 kJ/mm. Risk of grain coarsening and reduced toughness.")

    st.divider()
    st.caption("Formula: Q = (U × I × 60 × k) / (v × 1000) — Based on EN 1011 standard")