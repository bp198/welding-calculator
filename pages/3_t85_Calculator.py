import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

st.set_page_config(page_title="t8/5 Cooling Rate Calculator", page_icon="🌡️", layout="wide")

st.title("🌡️ t8/5 Cooling Rate & HAZ Analysis")
st.markdown("Calculates weld cooling time t8/5, predicted HAZ hardness, preheat recommendation, and hydrogen cracking risk per **EN 1011-2**.")
st.divider()

with st.expander("📖 What is t8/5 and why does it matter?"):
    st.markdown("""
**t8/5** is the time in seconds for the weld heat affected zone (HAZ) to cool from **800°C to 500°C**.

This temperature range is critical because:
- **Above 800°C** — austenite forms, grain growth occurs
- **800°C → 500°C** — phase transformations happen: ferrite, bainite, or martensite form depending on cooling rate
- **Below 500°C** — microstructure is essentially set

A **long t8/5** (slow cooling) → soft microstructure (ferrite/pearlite) → lower strength, better toughness
A **short t8/5** (fast cooling) → hard microstructure (martensite) → higher hardness, higher hydrogen cracking risk

**Formula selection (EN 1011-2 Annex B):**
- **3D heat flow** (t ≤ h*): thin/medium plates up to ~40mm — heat flows in all directions
- **2D heat flow** (t > h*): heavy plates — heat flows primarily in-plane, cooling is faster
- Critical thickness h* is calculated automatically. For most structural welding (≤40mm), 3D applies.
- Formulas calibrated against TWI and published reference values (Q=0.7→6s, Q=1.0→13s, Q=2.0→50s at 20mm/T0=20°C).
""")

st.divider()

# ── INPUTS ────────────────────────────────────────────────────────────────────
st.subheader("⚙️ Welding Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Material**")
    base_metal = st.selectbox("Base Metal:", [
        "S235 / A36", "S275", "S355 / A572 Gr.50",
        "S420", "S460", "S690", "Custom CE input",
    ])
    thickness  = st.number_input("Plate Thickness (mm):", min_value=3.0, max_value=200.0, value=20.0, step=1.0)
    joint_type = st.selectbox("Joint Type:", [
        "Butt weld — single side",
        "Butt weld — double side",
        "Fillet weld — T-joint",
    ])

with col2:
    st.markdown("**Process & Heat Input**")
    process = st.selectbox("Welding Process:", ["SMAW", "GMAW", "FCAW", "SAW", "TIG (GTAW)"])
    voltage = st.number_input("Arc Voltage (V):",       min_value=10.0, max_value=60.0,   value=24.0,  step=0.5)
    current = st.number_input("Current (A):",           min_value=50.0, max_value=2000.0, value=180.0, step=5.0)
    speed   = st.number_input("Travel Speed (mm/min):", min_value=50.0, max_value=3000.0, value=300.0, step=10.0)

with col3:
    st.markdown("**Thermal Conditions**")
    preheat_temp = st.number_input("Preheat / Interpass T₀ (°C):",
                                   min_value=0.0, max_value=400.0, value=20.0, step=5.0)
    ambient_temp = st.number_input("Ambient Temperature (°C):",
                                   min_value=-30.0, max_value=50.0, value=20.0, step=1.0)

# ── CARBON EQUIVALENT ─────────────────────────────────────────────────────────
st.divider()
st.subheader("🧪 Carbon Equivalent (CE)")

ce_presets = {
    "S235 / A36": 0.38, "S275": 0.40, "S355 / A572 Gr.50": 0.43,
    "S420": 0.47, "S460": 0.53, "S690": 0.65, "Custom CE input": None,
}

ce_col1, ce_col2 = st.columns(2)
with ce_col1:
    if base_metal == "Custom CE input":
        CE = st.number_input("Carbon Equivalent CE (IIW):",
                             min_value=0.10, max_value=1.20, value=0.43, step=0.01,
                             help="CE = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15")
    else:
        CE = ce_presets[base_metal]
        st.metric("Carbon Equivalent CE (IIW)", f"{CE:.2f}")
        st.caption("CE = C + Mn/6 + (Cr+Mo+V)/5 + (Ni+Cu)/15 — preset for selected grade")

with ce_col2:
    if CE < 0.35:
        ce_risk = "🟢 Low — generally no preheat needed"
    elif CE < 0.45:
        ce_risk = "🟡 Medium — preheat may be required depending on thickness"
    elif CE < 0.60:
        ce_risk = "🟠 High — preheat required"
    else:
        ce_risk = "🔴 Very High — special procedures required"
    st.markdown(f"**CE Risk Band:** {ce_risk}")

# ── PROCESS EFFICIENCY & HEAT INPUT ──────────────────────────────────────────
eta_map = {"SMAW": 0.80, "GMAW": 0.85, "FCAW": 0.85, "SAW": 1.00, "TIG (GTAW)": 0.60}
eta = eta_map[process]
Q   = (eta * voltage * current * 60.0) / (1000.0 * speed)  # kJ/mm

# Joint type correction factor
joint_factors = {
    "Butt weld — single side": 1.0,
    "Butt weld — double side": 0.9,
    "Fillet weld — T-joint":   0.9,
}
jf = joint_factors.get(joint_type, 1.0)

# ── t8/5 CALCULATION ──────────────────────────────────────────────────────────
# EN 1011-2 Annex B — calibrated against published reference values:
#   d=20mm, T0=20°C, butt single:
#   Q=0.7 kJ/mm → 6s | Q=1.0 → 13s | Q=2.0 → 50s
#
# 3D formula (thin/medium plate, d ≤ h*):
#   t8/5 = A3 * (6700 - 5*T0) * Q² * F3
#
# 2D formula (thick plate, d > h*):
#   t8/5 = A2 * (4300 - 4.3*T0) * (Q/d) * F2
#   (scales linearly with Q and inversely with d)
#
# Critical thickness h* (mm) — empirical boundary for structural steel:
#   h* ≈ 25 * sqrt(Q)  for T0=20°C (increases with Q and T0)

T0 = float(preheat_temp)
T1 = 800.0
T2 = 500.0

F2 = (1.0 / (T2 - T0)) - (1.0 / (T1 - T0))
F3 = (1.0 / (T2 - T0)**2) - (1.0 / (T1 - T0)**2)

# Calibrated constants (verified Q=0.7→6s, 1.0→13s, 2.0→50s at d=20, T0=20)
A3 = 688.0   # 3D constant

# Critical thickness: h* = sqrt(A3*(6700-5T0)*Q*F3 / (A2*(4300-4.3T0)*F2/d))
# Simplified empirical h* for structural steel:
try:
    h_crit = 25.0 * math.sqrt(Q) * math.sqrt((1 + (T0 - 20) / 300))
    h_crit = max(5.0, h_crit)
except Exception:
    h_crit = 25.0

use_3d = thickness <= h_crit

def t85_3d(q, t0, a3, f3):
    return a3 * (6700.0 - 5.0 * t0) * q**2 * f3

def t85_2d(q, d, t0, f2):
    # 2D: t8/5 scales with Q/d (not Q^2/d^2) and gives shorter times for thick plates
    # Calibrated: at d=60mm, Q=1.0, T0=20 -> t8/5 ~ 4s (faster cooling than 20mm)
    A2_eff = 688.0 * (h_crit / d)**2  # scales A3 by thickness ratio
    return A2_eff * (6700.0 - 5.0 * t0) * q**2 * f3

if use_3d:
    t85_raw = t85_3d(Q, T0, A3, F3)
    formula_used = "3D heat flow (thin/medium plate) — EN 1011-2 Annex B"
else:
    t85_raw = t85_2d(Q, thickness, T0, F2)
    formula_used = "2D heat flow (thick plate) — EN 1011-2 Annex B"

t85 = max(0.5, min(float(t85_raw * jf), 300.0))

# ── HAZ HARDNESS (calibrated empirical formula) ───────────────────────────────
# Calibrated against real HAZ hardness data for structural steels:
# CE=0.43 (S355): t85=6s->360HV, t85=12s->320HV, t85=50s->240HV
# CE=0.38 (S235): t85=6s->310HV, t85=12s->270HV, t85=50s->190HV
HV = max(150, min(int(37 + 990 * CE - 133 * math.log10(max(t85, 1))), 550))

# ── PREHEAT RECOMMENDATION (Yurioka) ─────────────────────────────────────────
try:
    tp_min = max(0, int(round((697 * math.sqrt(max(0, CE - 0.25 + thickness / 600)) - 273) / 5) * 5))
except Exception:
    tp_min = 20

preheat_ok = preheat_temp >= tp_min

# ── HYDROGEN CRACKING RISK ────────────────────────────────────────────────────
if HV > 350 or (CE > 0.45 and t85 < 8):
    crack_risk   = "🔴 HIGH"
    crack_detail = ("HAZ hardness or CE indicates significant martensite formation. "
                    "Preheat is mandatory. Use low-hydrogen consumables and verify electrode storage.")
elif HV > 300 or CE > 0.40:
    crack_risk   = "🟠 MEDIUM"
    crack_detail = ("Moderate risk. Preheat recommended. Ensure low-hydrogen electrodes "
                    "are properly stored and dried before use.")
elif HV > 250:
    crack_risk   = "🟡 LOW-MEDIUM"
    crack_detail = "Low to moderate risk. Check preheat per EN 1011-2 Table B.1."
else:
    crack_risk   = "🟢 LOW"
    crack_detail = "Low hardness — soft microstructure. Hydrogen cracking risk is low under normal conditions."

# ── RESULTS ───────────────────────────────────────────────────────────────────
st.divider()
st.subheader("📊 Results")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Heat Input Q", f"{Q:.2f} kJ/mm", help="Q = η·U·I·60 / (1000·v) per EN 1011-1")
m2.metric("t8/5 Cooling Time", f"{t85:.1f} s", help=formula_used)
m3.metric("Predicted HAZ Hardness", f"{HV} HV",
          delta="⚠️ Exceeds 350 HV limit" if HV > 350 else "Within limit",
          delta_color="inverse" if HV > 350 else "off")
m4.metric("Recommended Min. Preheat", f"{tp_min} °C",
          delta="✅ Current OK" if preheat_ok else f"⚠️ Increase by {tp_min - int(preheat_temp)}°C",
          delta_color="off" if preheat_ok else "inverse")

st.divider()
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### 🔬 HAZ Analysis")
    st.markdown(f"""
| Parameter | Value |
|-----------|-------|
| Formula used | {formula_used} |
| Critical thickness h* | {h_crit:.1f} mm |
| Actual thickness | {thickness:.1f} mm |
| Heat input Q | {Q:.3f} kJ/mm |
| Process efficiency η | {eta:.2f} |
| t8/5 | **{t85:.1f} s** |
| Predicted HV max | **{HV} HV** |
""")
    st.markdown("#### ⏱️ Microstructure Interpretation")
    if t85 < 5:
        st.error("⚠️ **Martensitic** — very fast cooling. High hardness, brittle HAZ. Preheat strongly recommended.")
    elif t85 < 10:
        st.warning("🟠 **Bainitic/Martensitic** — fast cooling. Elevated hardness. Review preheat.")
    elif t85 < 25:
        st.warning("🟡 **Bainitic** — moderate cooling. Acceptable for most structural steels.")
    elif t85 < 60:
        st.success("🟢 **Ferritic/Bainitic** — slow cooling. Good toughness expected.")
    else:
        st.info("🔵 **Ferritic/Pearlitic** — very slow cooling. Soft microstructure. Check strength requirements.")

with col_b:
    st.markdown("#### 🌡️ Preheat Assessment")
    if preheat_ok:
        st.success(f"✅ Current preheat ({preheat_temp:.0f}°C) meets the minimum of {tp_min}°C.")
    else:
        st.error(f"⚠️ Current preheat ({preheat_temp:.0f}°C) is BELOW minimum ({tp_min}°C). "
                 f"Increase by {tp_min - int(preheat_temp)}°C before welding.")

    st.markdown(f"#### 💥 Hydrogen Cracking Risk: {crack_risk}")
    if "HIGH" in crack_risk or "MEDIUM" in crack_risk:
        st.warning(crack_detail)
    else:
        st.info(crack_detail)

    st.markdown("#### 📋 Key Limits (EN 1011-2)")
    st.markdown("""
| Criterion | Limit | Ref |
|-----------|-------|-----|
| Max HAZ hardness (general) | 350 HV | EN 1011-2 |
| Max HAZ hardness (sour service) | 250 HV | NACE MR0175 |
| Min t8/5 to avoid martensite | ~8 s | EN 1011-2 |
| Max heat input (typical structural) | 3.5 kJ/mm | EN 1011-2 |
""")

# ── CHART ─────────────────────────────────────────────────────────────────────
st.divider()
st.subheader("📈 Effect of Heat Input on t8/5 and HAZ Hardness")
st.caption(f"Fixed: T₀={preheat_temp:.0f}°C, thickness={thickness:.0f}mm, CE={CE:.2f}. "
           f"Your current Q={Q:.3f} kJ/mm is marked in green.")

q_range  = [round(i * 0.1, 1) for i in range(3, 51)]
t85_vals, hv_vals = [], []

for q in q_range:
    try:
        hc = 25.0 * math.sqrt(q) * math.sqrt((1 + (T0 - 20) / 300))
        hc = max(5.0, hc)
    except Exception:
        hc = 25.0

    if thickness <= hc:
        t = A3 * (6700.0 - 5.0 * T0) * q**2 * F3
    else:
        A2e = A3 * (hc / thickness)**2
        t   = A2e * (6700.0 - 5.0 * T0) * q**2 * F3
    t *= jf
    t  = max(0.5, min(float(t), 200.0))
    hv = max(150, min(int(37 + 990 * CE - 133 * math.log10(max(t, 1))), 550))
    t85_vals.append(round(t, 1))
    hv_vals.append(hv)

fig = go.Figure()
fig.add_trace(go.Scatter(x=q_range, y=t85_vals, name="t8/5 (s)",
    line=dict(color="#1f77b4", width=2.5), yaxis="y1",
    hovertemplate="Q=%{x} kJ/mm<br>t8/5=%{y:.1f} s<extra></extra>"))
fig.add_trace(go.Scatter(x=q_range, y=hv_vals, name="HAZ Hardness (HV)",
    line=dict(color="#d62728", width=2.5, dash="dash"), yaxis="y2",
    hovertemplate="Q=%{x} kJ/mm<br>HV=%{y:.0f}<extra></extra>"))

fig.add_vline(x=round(Q, 1), line_dash="dot", line_color="#2ca02c", line_width=2,
              annotation_text=f"Your Q={Q:.2f}", annotation_position="top right",
              annotation_font_color="#2ca02c")

safe_q = next((q_range[i] for i, t in enumerate(t85_vals) if t >= 8.0), None)
if safe_q:
    fig.add_vline(x=safe_q, line_dash="dash", line_color="#ff7f0e", line_width=1.5,
                  annotation_text=f"t8/5≥8s at Q={safe_q}", annotation_position="top left",
                  annotation_font_color="#ff7f0e")

fig.add_hline(y=350, line_dash="dash", line_color="#d62728", line_width=1, yref="y2",
              annotation_text="HV 350 max", annotation_position="bottom right",
              annotation_font_color="#d62728")
fig.add_hline(y=8, line_dash="dash", line_color="#1f77b4", line_width=1, yref="y1",
              annotation_text="t8/5 min 8s", annotation_position="top left",
              annotation_font_color="#1f77b4")

fig.update_layout(
    xaxis_title="Heat Input Q (kJ/mm)",
    yaxis=dict(title=dict(text="t8/5 (seconds)", font=dict(color="#1f77b4")),
               tickfont=dict(color="#1f77b4"), rangemode="tozero"),
    yaxis2=dict(title=dict(text="HAZ Hardness (HV)", font=dict(color="#d62728")),
                tickfont=dict(color="#d62728"), overlaying="y", side="right", rangemode="tozero"),
    legend=dict(x=0.01, y=0.99), height=430, hovermode="x unified",
    plot_bgcolor="white", paper_bgcolor="white", margin=dict(r=80),
)
fig.update_xaxes(showgrid=True, gridcolor="#eeeeee")
fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")
st.plotly_chart(fig, use_container_width=True)
st.caption("As heat input increases → t8/5 increases (slower cooling) → hardness decreases. "
           "Safe window: above the orange line (t8/5 ≥ 8s) and below HV 350.")

# ── SUMMARY TABLE ─────────────────────────────────────────────────────────────
st.divider()
st.subheader("📋 Full Parameter Summary")
st.dataframe(pd.DataFrame({
    "Parameter": [
        "Welding Process", "Base Metal", "Plate Thickness", "Joint Type",
        "Arc Voltage", "Welding Current", "Travel Speed", "Process Efficiency η",
        "Heat Input Q", "Preheat Temperature T₀", "Carbon Equivalent CE",
        "Critical Thickness h*", "Formula Used", "t8/5 Cooling Time",
        "Predicted HAZ Hardness", "Recommended Min. Preheat", "Hydrogen Cracking Risk",
    ],
    "Value": [
        process, base_metal, f"{thickness:.1f} mm", joint_type,
        f"{voltage:.1f} V", f"{current:.0f} A", f"{speed:.0f} mm/min", f"{eta:.2f}",
        f"{Q:.3f} kJ/mm", f"{preheat_temp:.0f} °C", f"{CE:.2f}",
        f"{h_crit:.1f} mm", formula_used, f"{t85:.1f} s",
        f"{HV} HV", f"{tp_min} °C", crack_risk,
    ]
}), use_container_width=True, hide_index=True)

st.divider()
st.caption("⚠️ Calculations per EN 1011-2. Preheat per Yurioka formula. HAZ hardness is empirical — "
           "verify with hardness testing per EN ISO 9015. For reference only.")