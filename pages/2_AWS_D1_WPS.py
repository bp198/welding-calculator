import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="AWS D1.1 WPS Reference", page_icon="📋", layout="wide")

st.title("📋 AWS D1.1/D1.1M:2025 — Prequalified WPS Requirements")
st.markdown("Interactive reference for Clause 5 — select a process and filter by position.")
st.divider()

# ════════════════════════════════════════════════════════
# ALL PREVIOUS DATA (keep exactly as before)
# ════════════════════════════════════════════════════════

smaw_data = [
    {"Variable": "Electrode Diameter", "Position": "Flat", "Weld Type": "Fillet", "Requirement": "5/16 in [8.0 mm] max.", "Exceptions": "Except root pass"},
    {"Variable": "Electrode Diameter", "Position": "Flat", "Weld Type": "Groove", "Requirement": "1/4 in [6.4 mm] max.", "Exceptions": "Except root pass"},
    {"Variable": "Electrode Diameter", "Position": "Flat", "Weld Type": "Root Pass", "Requirement": "3/16 in [4.8 mm] max.", "Exceptions": ""},
    {"Variable": "Electrode Diameter", "Position": "Horizontal", "Weld Type": "Fillet", "Requirement": "1/4 in [6.4 mm] max.", "Exceptions": ""},
    {"Variable": "Electrode Diameter", "Position": "Horizontal", "Weld Type": "Groove", "Requirement": "3/16 in [4.8 mm] max.", "Exceptions": ""},
    {"Variable": "Electrode Diameter", "Position": "Vertical", "Weld Type": "All", "Requirement": "3/16 in [4.8 mm] max.", "Exceptions": "5/32 in [4.0 mm] max for EXX14 and low-hydrogen electrodes"},
    {"Variable": "Electrode Diameter", "Position": "Overhead", "Weld Type": "All", "Requirement": "3/16 in [4.8 mm] max.", "Exceptions": "5/32 in [4.0 mm] max for EXX14 and low-hydrogen electrodes"},
    {"Variable": "Current", "Position": "All", "Weld Type": "All", "Requirement": "Within range recommended by filler metal manufacturer", "Exceptions": ""},
    {"Variable": "Root Bead Thickness", "Position": "Flat", "Weld Type": "Groove/Fillet", "Requirement": "3/8 in [10 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Horizontal", "Weld Type": "Groove/Fillet", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Vertical", "Weld Type": "Groove/Fillet", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Overhead", "Weld Type": "Groove/Fillet", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Fill & Cap Bead Thickness", "Position": "All", "Weld Type": "Groove/Fillet", "Requirement": "3/16 in [5 mm] max.", "Exceptions": ""},
    {"Variable": "Single Pass Fillet Size", "Position": "Flat", "Weld Type": "Fillet", "Requirement": "3/8 in [10 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Horizontal", "Weld Type": "Fillet", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Vertical", "Weld Type": "Fillet", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Overhead", "Weld Type": "Fillet", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.6.2"},
]

saw_data = [
    {"Variable": "Electrode Diameter", "Position": "Flat", "Weld Type": "All", "Single Electrode": "1/4 in [6.4 mm] max.", "Parallel Electrodes": "—", "Multiple Electrodes": "—", "Exceptions": ""},
    {"Variable": "Electrode Diameter", "Position": "Horizontal", "Weld Type": "Fillet", "Single Electrode": "1/4 in [6.4 mm] max.", "Parallel Electrodes": "—", "Multiple Electrodes": "—", "Exceptions": ""},
    {"Variable": "Current — Fillet", "Position": "Flat & Horizontal", "Weld Type": "Fillet", "Single Electrode": "1000 A max.", "Parallel Electrodes": "1200 A max.", "Multiple Electrodes": "Unlimited", "Exceptions": ""},
    {"Variable": "Current — Groove root (with opening)", "Position": "Flat & Horizontal", "Weld Type": "Groove", "Single Electrode": "600 A max.", "Parallel Electrodes": "700 A max.", "Multiple Electrodes": "—", "Exceptions": ""},
    {"Variable": "Current — Groove root (no opening)", "Position": "Flat & Horizontal", "Weld Type": "Groove", "Single Electrode": "900 A max.", "Parallel Electrodes": "—", "Multiple Electrodes": "—", "Exceptions": ""},
    {"Variable": "Current — Groove fill beads", "Position": "Flat & Horizontal", "Weld Type": "Groove", "Single Electrode": "1200 A max.", "Parallel Electrodes": "—", "Multiple Electrodes": "—", "Exceptions": ""},
    {"Variable": "Current — Groove cap bead", "Position": "Flat & Horizontal", "Weld Type": "Groove", "Single Electrode": "Unlimited", "Parallel Electrodes": "—", "Multiple Electrodes": "Unlimited", "Exceptions": ""},
    {"Variable": "Root Bead Thickness", "Position": "Flat & Horizontal", "Weld Type": "All", "Single Electrode": "Unlimited", "Parallel Electrodes": "Unlimited", "Multiple Electrodes": "Unlimited", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Fill & Cap Bead Thickness", "Position": "Flat & Horizontal", "Weld Type": "All", "Single Electrode": "1/4 in [6 mm] max.", "Parallel Electrodes": "1/4 in [6 mm] max.", "Multiple Electrodes": "Unlimited", "Exceptions": ""},
    {"Variable": "Single Pass Fillet Size", "Position": "Flat & Horizontal", "Weld Type": "Fillet", "Single Electrode": "5/16 in [8 mm] max.", "Parallel Electrodes": "5/16 in [8 mm] max.", "Multiple Electrodes": "1/2 in [12 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Layer Width — Root", "Position": "Flat & Horizontal", "Weld Type": "Root Bead", "Single Electrode": "Split root layer", "Parallel Electrodes": "Split root layer", "Multiple Electrodes": "Split root layer", "Exceptions": "For groove opening > 1/2 in [12 mm]"},
    {"Variable": "Layer Width — Fill & cap", "Position": "Flat & Horizontal", "Weld Type": "All", "Single Electrode": "Split if w > 5/8 in, max 1 in", "Parallel Electrodes": "Split if w > 5/8 in, max 1-1/8 in", "Multiple Electrodes": "Split if w > 1 in, max 1-1/4 in", "Exceptions": ""},
]

gmaw_data = [
    {"Variable": "Electrode Diameter", "Position": "All", "Weld Type": "All", "Requirement": "0.0625 in [1.6 mm] max.", "Exceptions": ""},
    {"Variable": "Current (min. amperage)", "Position": "All", "Weld Type": "All", "Requirement": "0.030→190A | 0.035→210A | 0.040→230A | 0.045→260A | 0.0625→300A min.", "Exceptions": "Manufacturer recs may be used if not short circuit"},
    {"Variable": "Pulsed Spray (min.)", "Position": "All", "Weld Type": "All", "Requirement": "0.035→100A | 0.045→110A | 0.052→120A | 0.0625→140A min.", "Exceptions": "Manufacturer recommendations may be used"},
    {"Variable": "Root Bead Thickness", "Position": "Flat", "Weld Type": "Fillet/Groove", "Requirement": "3/8 in [10 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Horizontal", "Weld Type": "Fillet/Groove", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Vertical", "Weld Type": "Fillet/Groove", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Overhead", "Weld Type": "Fillet/Groove", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Fill & Cap Bead Thickness", "Position": "All", "Weld Type": "Fillet/Groove", "Requirement": "1/4 in [6 mm] max.", "Exceptions": ""},
    {"Variable": "Single Pass Fillet Size", "Position": "Flat", "Weld Type": "Fillet", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Horizontal", "Weld Type": "Fillet", "Requirement": "3/8 in [10 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Vertical", "Weld Type": "Fillet", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Overhead", "Weld Type": "Fillet", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Layer Width", "Position": "Flat/Horizontal/Overhead", "Weld Type": "Groove/Fillet", "Requirement": "Split layers if w > 5/8 in [16 mm]", "Exceptions": ""},
    {"Variable": "Single Pass Layer Width", "Position": "Vertical", "Weld Type": "Groove/Fillet", "Requirement": "Split layers if w > 1 in [25 mm]", "Exceptions": ""},
]

fcaw_data = [
    {"Variable": "Electrode Dia — FCAW", "Position": "Flat/Horizontal", "T Condition": "T ≤ 3/8 in", "Requirement": "0.030 in [0.8 mm] min.", "Exceptions": ""},
    {"Variable": "Electrode Dia — GMAW Cored", "Position": "Flat/Horizontal", "T Condition": "T ≤ 3/8 in", "Requirement": "No minimum", "Exceptions": ""},
    {"Variable": "Electrode Dia — FCAW & GMAW Cored", "Position": "Flat/Horizontal", "T Condition": "T > 3/8 in", "Requirement": "0.045 in [1 mm] min.", "Exceptions": ""},
    {"Variable": "Electrode Dia max — FCAW", "Position": "Flat/Horizontal", "T Condition": "T > 3/8 in", "Requirement": "1/8 in [3.2 mm] max.", "Exceptions": ""},
    {"Variable": "Electrode Dia — FCAW", "Position": "Vertical", "T Condition": "T ≤ 3/8 in", "Requirement": "0.030 in [0.8 mm] min.", "Exceptions": ""},
    {"Variable": "Electrode Dia max — FCAW", "Position": "Vertical", "T Condition": "T > 3/8 in", "Requirement": "3/32 in [2.4 mm] max.", "Exceptions": ""},
    {"Variable": "Electrode Dia max — FCAW", "Position": "Overhead", "T Condition": "T > 3/8 in", "Requirement": "5/64 in [2.2 mm] max.", "Exceptions": ""},
    {"Variable": "Current", "Position": "All", "T Condition": "All", "Requirement": "Within range recommended by filler metal manufacturer", "Exceptions": ""},
    {"Variable": "Root Bead Thickness", "Position": "Flat", "T Condition": "—", "Requirement": "3/8 in [10 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Horizontal", "T Condition": "—", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Vertical", "T Condition": "—", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Root Bead Thickness", "Position": "Overhead", "T Condition": "—", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.8.2.1"},
    {"Variable": "Fill & Cap Bead Thickness", "Position": "All", "T Condition": "—", "Requirement": "1/4 in [6 mm] max.", "Exceptions": ""},
    {"Variable": "Single Pass Fillet Size", "Position": "Flat", "T Condition": "—", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Horizontal", "T Condition": "—", "Requirement": "3/8 in [10 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Vertical", "T Condition": "—", "Requirement": "1/2 in [12 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Single Pass Fillet Size", "Position": "Overhead", "T Condition": "—", "Requirement": "5/16 in [8 mm] max.", "Exceptions": "See 5.6.2"},
    {"Variable": "Layer Width — Groove root opening ≥ 1/2 in", "Position": "All", "T Condition": "—", "Requirement": "Split root layer, max bead 1 in [25 mm]", "Exceptions": ""},
    {"Variable": "Layer Width — Fill & cap", "Position": "Flat/Horizontal/Overhead", "T Condition": "—", "Requirement": "Split if w > 5/8 in [16 mm]", "Exceptions": ""},
    {"Variable": "Layer Width — Fill & cap", "Position": "Vertical", "T Condition": "—", "Requirement": "Split if w > 1 in [25 mm]", "Exceptions": ""},
]

preheat_data = [
    {"Category": "A", "Process": "SMAW (non low-hydrogen)", "Thickness": "1/8 to 3/4 in incl.", "Min Preheat °F": "32°F", "Min Preheat °C": "0°C", "Notes": "If base metal < 32°F, preheat to 70°F min"},
    {"Category": "A", "Process": "SMAW (non low-hydrogen)", "Thickness": "Over 3/4 to 1-1/2 in", "Min Preheat °F": "150°F", "Min Preheat °C": "65°C", "Notes": ""},
    {"Category": "A", "Process": "SMAW (non low-hydrogen)", "Thickness": "Over 1-1/2 to 2-1/2 in", "Min Preheat °F": "225°F", "Min Preheat °C": "110°C", "Notes": ""},
    {"Category": "A", "Process": "SMAW (non low-hydrogen)", "Thickness": "Over 2-1/2 in", "Min Preheat °F": "300°F", "Min Preheat °C": "150°C", "Notes": ""},
    {"Category": "B", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "1/8 to 3/4 in incl.", "Min Preheat °F": "32°F", "Min Preheat °C": "0°C", "Notes": ""},
    {"Category": "B", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "Over 3/4 to 1-1/2 in", "Min Preheat °F": "50°F", "Min Preheat °C": "10°C", "Notes": ""},
    {"Category": "B", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "Over 1-1/2 to 2-1/2 in", "Min Preheat °F": "150°F", "Min Preheat °C": "65°C", "Notes": ""},
    {"Category": "B", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "Over 2-1/2 in", "Min Preheat °F": "225°F", "Min Preheat °C": "110°C", "Notes": ""},
    {"Category": "C", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "1/8 to 3/4 in incl.", "Min Preheat °F": "50°F", "Min Preheat °C": "10°C", "Notes": ""},
    {"Category": "C", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "Over 3/4 to 1-1/2 in", "Min Preheat °F": "150°F", "Min Preheat °C": "65°C", "Notes": ""},
    {"Category": "C", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "Over 1-1/2 to 2-1/2 in", "Min Preheat °F": "225°F", "Min Preheat °C": "110°C", "Notes": ""},
    {"Category": "C", "Process": "SMAW (low-hydrogen), SAW, GMAW, FCAW", "Thickness": "Over 2-1/2 in", "Min Preheat °F": "300°F", "Min Preheat °C": "150°C", "Notes": ""},
]

pjp_size_data = [
    {"Base Metal Thickness (in)": "1/8 to 3/16 incl.", "Base Metal Thickness (mm)": "3 to 5 incl.", "Min Weld Size (in)": "1/16", "Min Weld Size (mm)": "2"},
    {"Base Metal Thickness (in)": "Over 3/16 to 1/4 incl.", "Base Metal Thickness (mm)": "Over 5 to 6 incl.", "Min Weld Size (in)": "1/8", "Min Weld Size (mm)": "3"},
    {"Base Metal Thickness (in)": "Over 1/4 to 1/2 incl.", "Base Metal Thickness (mm)": "Over 6 to 12 incl.", "Min Weld Size (in)": "3/16", "Min Weld Size (mm)": "5"},
    {"Base Metal Thickness (in)": "Over 1/2 to 3/4 incl.", "Base Metal Thickness (mm)": "Over 12 to 20 incl.", "Min Weld Size (in)": "1/4", "Min Weld Size (mm)": "6"},
    {"Base Metal Thickness (in)": "Over 3/4 to 1-1/2 incl.", "Base Metal Thickness (mm)": "Over 20 to 38 incl.", "Min Weld Size (in)": "5/16", "Min Weld Size (mm)": "8"},
    {"Base Metal Thickness (in)": "Over 1-1/2 to 2-1/4 incl.", "Base Metal Thickness (mm)": "Over 38 to 57 incl.", "Min Weld Size (in)": "3/8", "Min Weld Size (mm)": "10"},
    {"Base Metal Thickness (in)": "Over 2-1/4 to 6 incl.", "Base Metal Thickness (mm)": "Over 57 to 150 incl.", "Min Weld Size (in)": "1/2", "Min Weld Size (mm)": "12"},
    {"Base Metal Thickness (in)": "Over 6", "Base Metal Thickness (mm)": "Over 150", "Min Weld Size (in)": "5/8", "Min Weld Size (mm)": "16"},
]

# ════════════════════════════════════════════════════════
# NEW: TABLE 5.6 — BASE METALS
# ════════════════════════════════════════════════════════
base_metals = [
    # GROUP I
    {"Group": "I", "Specification": "ASTM A36", "Grade/Condition": "≤3/4 in [20 mm]", "Min Yield (ksi)": 36, "Min Yield (MPa)": 250, "Tensile Range (ksi)": "58–80", "Tensile Range (MPa)": "400–550"},
    {"Group": "I", "Specification": "ASTM A53", "Grade/Condition": "Grade B", "Min Yield (ksi)": 35, "Min Yield (MPa)": 240, "Tensile Range (ksi)": "60 min.", "Tensile Range (MPa)": "415 min."},
    {"Group": "I", "Specification": "ASTM A106", "Grade/Condition": "Grade B", "Min Yield (ksi)": 35, "Min Yield (MPa)": 240, "Tensile Range (ksi)": "60 min.", "Tensile Range (MPa)": "415 min."},
    {"Group": "I", "Specification": "ASTM A131", "Grade/Condition": "Grades A, B, D, E", "Min Yield (ksi)": 34, "Min Yield (MPa)": 235, "Tensile Range (ksi)": "58–75", "Tensile Range (MPa)": "400–520"},
    {"Group": "I", "Specification": "ASTM A500", "Grade/Condition": "Grade B", "Min Yield (ksi)": 46, "Min Yield (MPa)": 315, "Tensile Range (ksi)": "58 min.", "Tensile Range (MPa)": "400 min."},
    {"Group": "I", "Specification": "ASTM A500", "Grade/Condition": "Grade C", "Min Yield (ksi)": 50, "Min Yield (MPa)": 345, "Tensile Range (ksi)": "62 min.", "Tensile Range (MPa)": "425 min."},
    {"Group": "I", "Specification": "ASTM A516", "Grade/Condition": "Grade 55", "Min Yield (ksi)": 30, "Min Yield (MPa)": 205, "Tensile Range (ksi)": "55–75", "Tensile Range (MPa)": "380–515"},
    {"Group": "I", "Specification": "ASTM A516", "Grade/Condition": "Grade 60", "Min Yield (ksi)": 32, "Min Yield (MPa)": 220, "Tensile Range (ksi)": "60–80", "Tensile Range (MPa)": "415–550"},
    {"Group": "I", "Specification": "API 5L", "Grade/Condition": "Grade B", "Min Yield (ksi)": 35, "Min Yield (MPa)": 241, "Tensile Range (ksi)": "60 min.", "Tensile Range (MPa)": "414 min."},
    {"Group": "I", "Specification": "API 5L", "Grade/Condition": "Grade X42", "Min Yield (ksi)": 42, "Min Yield (MPa)": 290, "Tensile Range (ksi)": "60 min.", "Tensile Range (MPa)": "414 min."},
    # GROUP II
    {"Group": "II", "Specification": "ASTM A36", "Grade/Condition": "All thicknesses", "Min Yield (ksi)": 36, "Min Yield (MPa)": 250, "Tensile Range (ksi)": "58–80", "Tensile Range (MPa)": "400–550"},
    {"Group": "II", "Specification": "ASTM A572", "Grade/Condition": "Grade 42", "Min Yield (ksi)": 42, "Min Yield (MPa)": 290, "Tensile Range (ksi)": "60 min.", "Tensile Range (MPa)": "415 min."},
    {"Group": "II", "Specification": "ASTM A572", "Grade/Condition": "Grade 50", "Min Yield (ksi)": 50, "Min Yield (MPa)": 345, "Tensile Range (ksi)": "65 min.", "Tensile Range (MPa)": "450 min."},
    {"Group": "II", "Specification": "ASTM A572", "Grade/Condition": "Grade 55", "Min Yield (ksi)": 55, "Min Yield (MPa)": 380, "Tensile Range (ksi)": "70 min.", "Tensile Range (MPa)": "485 min."},
    {"Group": "II", "Specification": "ASTM A588", "Grade/Condition": "≤4 in [100 mm]", "Min Yield (ksi)": 50, "Min Yield (MPa)": 345, "Tensile Range (ksi)": "70 min.", "Tensile Range (MPa)": "485 min."},
    {"Group": "II", "Specification": "ASTM A709", "Grade/Condition": "Grade 50", "Min Yield (ksi)": 50, "Min Yield (MPa)": 345, "Tensile Range (ksi)": "65 min.", "Tensile Range (MPa)": "450 min."},
    {"Group": "II", "Specification": "ASTM A992", "Grade/Condition": "—", "Min Yield (ksi)": "50–65", "Min Yield (MPa)": "345–450", "Tensile Range (ksi)": "65 min.", "Tensile Range (MPa)": "450 min."},
    {"Group": "II", "Specification": "API 5L", "Grade/Condition": "Grade X52", "Min Yield (ksi)": 52, "Min Yield (MPa)": 359, "Tensile Range (ksi)": "66 min.", "Tensile Range (MPa)": "455 min."},
    # GROUP III
    {"Group": "III", "Specification": "ASTM A572", "Grade/Condition": "Grade 60", "Min Yield (ksi)": 60, "Min Yield (MPa)": 415, "Tensile Range (ksi)": "75 min.", "Tensile Range (MPa)": "520 min."},
    {"Group": "III", "Specification": "ASTM A572", "Grade/Condition": "Grade 65", "Min Yield (ksi)": 65, "Min Yield (MPa)": 450, "Tensile Range (ksi)": "80 min.", "Tensile Range (MPa)": "550 min."},
    {"Group": "III", "Specification": "ASTM A913", "Grade/Condition": "Grade 60", "Min Yield (ksi)": 60, "Min Yield (MPa)": 415, "Tensile Range (ksi)": "75 min.", "Tensile Range (MPa)": "520 min."},
    {"Group": "III", "Specification": "ASTM A913", "Grade/Condition": "Grade 65", "Min Yield (ksi)": 65, "Min Yield (MPa)": 450, "Tensile Range (ksi)": "80 min.", "Tensile Range (MPa)": "550 min."},
    # GROUP IV
    {"Group": "IV", "Specification": "ASTM A709", "Grade/Condition": "Grade HPS70W", "Min Yield (ksi)": 70, "Min Yield (MPa)": 485, "Tensile Range (ksi)": "85–110", "Tensile Range (MPa)": "585–760"},
    {"Group": "IV", "Specification": "ASTM A913", "Grade/Condition": "Grade 70", "Min Yield (ksi)": 70, "Min Yield (MPa)": 485, "Tensile Range (ksi)": "90 min.", "Tensile Range (MPa)": "620 min."},
    {"Group": "IV", "Specification": "ASTM A1066", "Grade/Condition": "Grade 70", "Min Yield (ksi)": 70, "Min Yield (MPa)": 485, "Tensile Range (ksi)": "85 min.", "Tensile Range (MPa)": "585 min."},
    # GROUP V
    {"Group": "V", "Specification": "ASTM A913", "Grade/Condition": "Grade 80", "Min Yield (ksi)": 80, "Min Yield (MPa)": 550, "Tensile Range (ksi)": "95 min.", "Tensile Range (MPa)": "655 min."},
]

# ════════════════════════════════════════════════════════
# NEW: TABLE 5.7 — FILLER METALS (SMAW & SAW)
# ════════════════════════════════════════════════════════
filler_metals = [
    {"Base Metal Group": "I", "Process": "SMAW", "AWS Spec": "A5.1 Carbon Steel", "Electrode Classifications": "F60XX, E70XX"},
    {"Base Metal Group": "I", "Process": "SMAW", "AWS Spec": "A5.5 Low-Alloy Steel", "Electrode Classifications": "E70XX-A1, E70XX-C1L, E70XX-C2L, E70XX-C3L, E7010-P1, E7018-W1"},
    {"Base Metal Group": "I", "Process": "SAW", "AWS Spec": "A5.17 Carbon Steel", "Electrode Classifications": "F6XX-EXXX, F6XX-ECXXX, F7XX-EXXX, F7XX-ECXXX"},
    {"Base Metal Group": "I", "Process": "SAW", "AWS Spec": "A5.23 Low-Alloy Steel", "Electrode Classifications": "F7XX-E(C)XXX-A1, F7XX-E(C)XXX-A2, F7XX-E(C)XXX-A4, F7XX-E(C)XXX-Ni1, F7XX-E(C)XXX-Ni2"},
    {"Base Metal Group": "II", "Process": "SMAW", "AWS Spec": "A5.1 Carbon Steel", "Electrode Classifications": "E7015, E7016, E7018, E7028"},
    {"Base Metal Group": "II", "Process": "SMAW", "AWS Spec": "A5.5 Low-Alloy Steel", "Electrode Classifications": "E7015-A1, E7016-A1, E7018-A1, E7015-C2L, E7016-C2L, E7018-C2L, E7018-C3L, E7018-W1"},
    {"Base Metal Group": "II", "Process": "SAW", "AWS Spec": "A5.17 Carbon Steel", "Electrode Classifications": "F7XX-EXXX, F7XX-ECXXX"},
    {"Base Metal Group": "II", "Process": "SAW", "AWS Spec": "A5.23 Low-Alloy Steel", "Electrode Classifications": "F7XX-E(C)XXX-A1, F7XX-E(C)XXX-A2, F7XX-E(C)XXX-A4, F7XX-E(C)XXX-Ni1, F7XX-E(C)XXX-Ni2"},
    {"Base Metal Group": "III", "Process": "SMAW", "AWS Spec": "A5.5 Low-Alloy Steel", "Electrode Classifications": "E8016-C1, E8018-C1, E8016-C2, E8018-C2, E8016-C3, E8018-C3, E8016-C4, E8018-C4, E8018-MN1, E8018-W2"},
    {"Base Metal Group": "III", "Process": "SAW", "AWS Spec": "A5.23 Low-Alloy Steel", "Electrode Classifications": "F8AX-E(C)XXX-A1 thru A4, F8AX-E(C)XXX-Ni1 thru Ni5, F8AX-E(C)XXX-W"},
    {"Base Metal Group": "IV", "Process": "SMAW", "AWS Spec": "A5.5 Low-Alloy Steel", "Electrode Classifications": "E9018M, E9018-P2"},
    {"Base Metal Group": "IV", "Process": "SAW", "AWS Spec": "A5.23 Low-Alloy Steel", "Electrode Classifications": "F9AX-E(C)XXX-A1, A2, A3, F3, M2, Ni4"},
    {"Base Metal Group": "V", "Process": "SMAW", "AWS Spec": "A5.5 Low-Alloy Steel", "Electrode Classifications": "E10018M, E10045-P2"},
    {"Base Metal Group": "V", "Process": "SAW", "AWS Spec": "A5.23 Low-Alloy Steel", "Electrode Classifications": "F10AX-EXX-XX, F10AX-ECXX-XX"},
]

# ════════════════════════════════════════════════════════
# NEW: TABLE 5.10 — SHIELDING GASES FOR GMAW
# ════════════════════════════════════════════════════════
shielding_gas_data = [
    {"Electrode": "ER70S-X (except ER70S-G) and E70C-X metal cored", "Shielding Gas Type": "Ar/CO₂ combinations", "Composition": "Ar 75–90% / CO₂ 10–25%"},
    {"Electrode": "ER70S-X (except ER70S-G) and E70C-X metal cored", "Shielding Gas Type": "Ar/O₂ combinations", "Composition": "Ar 95–98% / O₂ 2–5%"},
    {"Electrode": "ER70S-X (except ER70S-G) and E70C-X metal cored", "Shielding Gas Type": "100% CO₂", "Composition": "100% CO₂"},
]

# ════════════════════════════════════════════════════════
# UI — TABS (now 8 tabs)
# ════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "⚡ SMAW (5.1)",
    "🔩 SAW (5.2)",
    "🌀 GMAW (5.3)",
    "🔥 FCAW (5.4)",
    "🌡️ Preheat (5.11)",
    "📐 PJP Min Size (5.8)",
    "🏗️ Base Metals (5.6)",
    "🔧 Filler Metals (5.7)",
    "🤖 AI Assistant",
    "📄 WPS Generator",
])

def position_filter(df, pos):
    if pos == "All":
        return df
    return df[df["Position"].str.contains(pos, case=False, na=False)]

# ── TAB 1: SMAW ──
with tab1:
    st.subheader("Table 5.1 — Prequalified SMAW WPS Requirements")
    st.caption("Shielded Metal Arc Welding")
    pos = st.selectbox("Filter by Position:", ["All", "Flat", "Horizontal", "Vertical", "Overhead"], key="smaw_pos")
    df = pd.DataFrame(smaw_data)
    st.dataframe(position_filter(df, pos), use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("📐 Joint Illustration — Figure 5.1")

    from PIL import Image
    import os

    image_path = "images/figure_5_1.png"

    if os.path.exists(image_path):
        image = Image.open(image_path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Figure 5.1 — Prequalified CJP Groove Welded Joint Details — AWS D1.1/D1.1M:2025", width=500)
    else:
        st.warning("⚠️ Image not found. Please add figure_5_1.png to the images folder.")

        
# ── TAB 2: SAW ──
with tab2:
    st.subheader("Table 5.2 — Prequalified SAW WPS Requirements")
    st.caption("Submerged Arc Welding")
    pos = st.selectbox("Filter by Position:", ["All", "Flat", "Horizontal"], key="saw_pos")
    df = pd.DataFrame(saw_data)
    st.dataframe(position_filter(df, pos), use_container_width=True, hide_index=True)
    st.info("⚠️ SAW is only prequalified for Flat and Horizontal positions.")

# ── TAB 3: GMAW ──
with tab3:
    st.subheader("Table 5.3 — Prequalified GMAW (Solid Wire) WPS Requirements")
    st.caption("Gas Metal Arc Welding — solid wire only. GMAW-S is NOT prequalified.")
    pos = st.selectbox("Filter by Position:", ["All", "Flat", "Horizontal", "Vertical", "Overhead"], key="gmaw_pos")
    df = pd.DataFrame(gmaw_data)
    st.dataframe(position_filter(df, pos), use_container_width=True, hide_index=True)
    st.warning("⚠️ GMAW-S (short circuit transfer) is NOT prequalified. Must use CV power source.")

# ── TAB 4: FCAW ──
with tab4:
    st.subheader("Table 5.4 — Prequalified FCAW & GMAW Metal Cored WPS Requirements")
    pos = st.selectbox("Filter by Position:", ["All", "Flat", "Horizontal", "Vertical", "Overhead"], key="fcaw_pos")
    df = pd.DataFrame(fcaw_data)
    st.dataframe(position_filter(df, pos), use_container_width=True, hide_index=True)

# ── TAB 5: PREHEAT ──
with tab5:
    st.subheader("Table 5.11 — Minimum Preheat & Interpass Temperature")
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("Filter by Category:", ["All", "A", "B", "C"], key="preheat_cat")
    with col2:
        unit = st.radio("Temperature Unit:", ["°F", "°C"], horizontal=True)
    df = pd.DataFrame(preheat_data)
    if cat != "All":
        df = df[df["Category"] == cat]
    if unit == "°F":
        df = df.drop(columns=["Min Preheat °C"])
    else:
        df = df.drop(columns=["Min Preheat °F"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    with st.expander("📋 Category Steel Specifications"):
        st.markdown("""
**Category A** — A36 (≤3/4 in), A53 Gr.B, A106 Gr.B, A131, A139, A381, A500, A501, A516 Gr.55/60, A524, A573, A709 Gr.36, A1008/A1011/A1018 SS, API 5L Gr.B & X42, ABS Gr.A,B,D,E

**Category B** — A36 (all), A131 AH/DH/EH 32/36, A216, A501 Gr.B, A516 Gr.65/70, A529, A537 Cl.1/2, A572 Gr.42/50/55, A588, A595, A606, A618, A633 Gr.A/C/D, A709 Gr.36/50/50W/50S/HPS50W, A710, A847, A913 Gr.50/60/65, A992, A1008/A1011/A1018 HSLAS, API 2H/2MT1/2W/2Y Gr.42/50, API 5L X52, ABS AH/DH/EH 32/36

**Category C** — A572 Gr.60/65, A633 Gr.E, A709 HPS70W, A710 (Class 2/3), A913 Gr.70, A1018 HSLAS Gr.60/70 Cl.2, A1066 Gr.60/65/70, API 2W/2Y Gr.60, API 5L X52
        """)

# ── TAB 6: PJP MIN SIZE ──
with tab6:
    st.subheader("Table 5.8 — Minimum Prequalified PJP Groove Weld Size")
    st.caption("Per 5.4.2.3(1) — weld size need not exceed thickness of the thinner part joined")
    unit = st.radio("Display units:", ["Both", "Inches only", "mm only"], horizontal=True, key="pjp_unit")
    df = pd.DataFrame(pjp_size_data)
    if unit == "Inches only":
        df = df[["Base Metal Thickness (in)", "Min Weld Size (in)"]]
    elif unit == "mm only":
        df = df[["Base Metal Thickness (mm)", "Min Weld Size (mm)"]]
    st.dataframe(df, use_container_width=True, hide_index=True)

# ── TAB 7: BASE METALS ──
with tab7:
    st.subheader("Table 5.6 — Approved Base Metals for Prequalified WPSs")
    st.caption("Only these base metals may be used in prequalified WPSs (see 5.3)")

    col1, col2 = st.columns(2)
    with col1:
        group_filter = st.selectbox("Filter by Group:", ["All", "I", "II", "III", "IV", "V"])
    with col2:
        search = st.text_input("Search specification (e.g. A572, A36, API):", "")

    df = pd.DataFrame(base_metals)
    if group_filter != "All":
        df = df[df["Group"] == group_filter]
    if search:
        df = df[df["Specification"].str.contains(search, case=False, na=False)]

    st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("ℹ️ Group Notes"):
        st.markdown("""
- **Group I** — Lower strength steels (Fy ≤ 36 ksi / 250 MPa typically)
- **Group II** — Medium strength steels (Fy up to ~55 ksi / 380 MPa)
- **Group III** — Higher strength steels (Fy 60–65 ksi / 415–450 MPa)
- **Group IV** — High strength steels (Fy ~70 ksi / 485 MPa)
- **Group V** — Very high strength steels (Fy ~80 ksi / 550 MPa)

**Note:** In joints with base metals of different groups, use filler metal matching the higher strength base metal, or use filler matching the lower strength base metal if it produces a low-hydrogen deposit.
        """)

# ── TAB 8: FILLER METALS ──
with tab8:
    st.subheader("Table 5.7 — Filler Metals for Matching Strength")
    st.caption("SMAW and SAW filler metals for Table 5.6 Groups I–V")

    col1, col2 = st.columns(2)
    with col1:
        grp = st.selectbox("Base Metal Group:", ["All", "I", "II", "III", "IV", "V"], key="fm_group")
    with col2:
        proc = st.selectbox("Process:", ["All", "SMAW", "SAW"], key="fm_proc")

    df = pd.DataFrame(filler_metals)
    if grp != "All":
        df = df[df["Base Metal Group"] == grp]
    if proc != "All":
        df = df[df["Process"] == proc]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Table 5.10 — Shielding Gas Options for GMAW (AWS A5.18/A5.18M)")
    st.dataframe(pd.DataFrame(shielding_gas_data), use_container_width=True, hide_index=True)

    with st.expander("📋 Weathering Steel Requirements (Table 5.9 — see 5.6.3)"):
        st.markdown("""
For **exposed bare unpainted weathering steel** applications:

| Process | AWS Spec | Approved Electrodes |
|---|---|---|
| SMAW | A5.5/A5.5M | All electrodes depositing weld metal with B2L, C1, C1L, C2, C2L, C3, or WX analysis |
| SAW | A5.23/A5.23M | All electrode-flux combinations depositing weld metal with Ni1, Ni2, Ni3, Ni4, or WX analysis |
| FCAW | A5.29/A5.29M | All electrodes depositing weld metal with B2L, K2, Ni1, Ni2, Ni3, Ni4, or WX analysis |
| GMAW | A5.28/A5.28M | All electrodes meeting B2L, G, Ni1, Ni2, Ni3 analysis requirements |

**Exceptions (5.6.3.1 & 5.6.3.2):** Single-pass groove welds and small single-pass fillet welds (SMAW ≤ 1/4 in, SAW/GMAW/FCAW ≤ 5/16 in) may use any Group II filler metal from Table 5.7.
        """)

with tab9:
    st.subheader("🤖 AI Welding Assistant")
    st.markdown("Answer the questions below and the AI will interpret the AWS D1.1 requirements for your specific situation.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        process = st.selectbox("Welding Process:",
            ["SMAW", "SAW", "GMAW", "FCAW"])

        position = st.selectbox("Welding Position:",
            ["Flat", "Horizontal", "Vertical", "Overhead"])

        weld_type = st.selectbox("Weld Type:",
            ["Fillet", "Groove", "Root Pass"])

    with col2:
        base_metal = st.selectbox("Base Metal:",
            ["ASTM A36", "ASTM A572 Gr.50", "ASTM A572 Gr.60",
             "ASTM A588", "ASTM A709 Gr.50", "ASTM A992",
             "API 5L Gr.B", "Other"])

        thickness = st.number_input("Material Thickness (mm):",
            min_value=1.0, max_value=200.0, value=12.0, step=0.5)

        electrode = st.text_input("Electrode/Wire (optional):",
            placeholder="e.g. E7018, ER70S-6")

    col3, col4 = st.columns(2)
    with col3:
        ambient_temp = st.number_input("Ambient Temperature (°C):",
            min_value=-50.0, max_value=50.0, value=20.0, step=1.0)
        humidity = st.selectbox("Humidity/Weather Condition:",
            ["Normal (indoor)", "High humidity", "Rain/Snow nearby",
             "Strong wind", "Extreme cold (below 0°C)", "Extreme heat (above 35°C)"])
    with col4:
        location = st.selectbox("Welding Location:",
            ["Indoor — controlled environment",
             "Outdoor — sheltered",
             "Outdoor — exposed",
             "Offshore / marine environment",
             "Underground"])
        criticality = st.selectbox("Structure Criticality:",
            ["Standard structure",
             "Critical structure (bridges, pressure vessels)",
             "Seismic zone",
             "Impact/dynamic loading"])

    additional = st.text_area("Describe your full situation in detail:",
        placeholder="e.g. I am welding a structural beam connection outdoors in winter. Temperature is -20°C. Wind is present. The structure is a bridge...",
        height=120)

    st.divider()

    if st.button("🤖 Get AI Interpretation", use_container_width=True):
        with st.spinner("🔍 AI is analyzing your welding situation..."):

            from groq import Groq
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])

            # ── Pull exact data from our tables ──
            smaw_rules = {
                "Flat": {
                    "Fillet": {"max_electrode": "5/16 in [8.0 mm]", "exception": "Except root pass"},
                    "Groove": {"max_electrode": "1/4 in [6.4 mm]", "exception": "Except root pass"},
                    "Root Pass": {"max_electrode": "3/16 in [4.8 mm]", "exception": ""},
                },
                "Horizontal": {
                    "Fillet": {"max_electrode": "1/4 in [6.4 mm]", "exception": ""},
                    "Groove": {"max_electrode": "3/16 in [4.8 mm]", "exception": ""},
                },
                "Vertical": {"All": {"max_electrode": "3/16 in [4.8 mm]", "exception": "5/32 in [4.0 mm] for EXX14 and low-hydrogen electrodes"}},
                "Overhead": {"All": {"max_electrode": "3/16 in [4.8 mm]", "exception": "5/32 in [4.0 mm] for EXX14 and low-hydrogen electrodes"}},
            }

            saw_rules = {
                "max_electrode": "1/4 in [6.4 mm]",
                "positions": "Flat and Horizontal only",
                "current_fillet": "1000A max (single), 1200A max (parallel), Unlimited (multiple)",
                "current_groove_root_with_opening": "600A max (single), 700A max (parallel)",
                "current_groove_root_no_opening": "900A max (single)",
                "current_groove_fill": "1200A max (single)",
            }

            gmaw_rules = {
                "max_electrode": "0.0625 in [1.6 mm]",
                "note": "GMAW-S is NOT prequalified. Must use CV power source.",
                "min_current": "190A for 0.030in | 210A for 0.035in | 230A for 0.040in | 260A for 0.045in | 300A for 0.0625in",
            }

            fcaw_rules = {
                "flat_horizontal_T_less_10mm": "0.030 in [0.8 mm] min (FCAW), No min (GMAW Cored)",
                "flat_horizontal_T_more_10mm": "0.045 in [1 mm] min, 1/8 in [3.2 mm] max (FCAW)",
                "vertical_T_more_10mm": "3/32 in [2.4 mm] max",
                "overhead_T_more_10mm": "5/64 in [2.2 mm] max",
            }

            bead_limits = {
                "SMAW": {
                    "root_bead": {"Flat": "3/8 in [10 mm]", "Horizontal": "5/16 in [8 mm]", "Vertical": "1/2 in [12 mm]", "Overhead": "5/16 in [8 mm]"},
                    "fill_cap": "3/16 in [5 mm] all positions",
                    "single_pass_fillet": {"Flat": "3/8 in [10 mm]", "Horizontal": "5/16 in [8 mm]", "Vertical": "1/2 in [12 mm]", "Overhead": "5/16 in [8 mm]"},
                },
                "SAW": {
                    "root_bead": "Unlimited (Flat & Horizontal only)",
                    "fill_cap_single": "1/4 in [6 mm] max",
                    "fill_cap_multiple": "Unlimited",
                    "single_pass_fillet": {"single": "5/16 in [8 mm]", "parallel": "5/16 in [8 mm]", "multiple": "1/2 in [12 mm]"},
                },
                "GMAW": {
                    "root_bead": {"Flat": "3/8 in [10 mm]", "Horizontal": "5/16 in [8 mm]", "Vertical": "1/2 in [12 mm]", "Overhead": "5/16 in [8 mm]"},
                    "fill_cap": "1/4 in [6 mm] all positions",
                    "single_pass_fillet": {"Flat": "1/2 in [12 mm]", "Horizontal": "3/8 in [10 mm]", "Vertical": "1/2 in [12 mm]", "Overhead": "5/16 in [8 mm]"},
                },
                "FCAW": {
                    "root_bead": {"Flat": "3/8 in [10 mm]", "Horizontal": "5/16 in [8 mm]", "Vertical": "1/2 in [12 mm]", "Overhead": "5/16 in [8 mm]"},
                    "fill_cap": "1/4 in [6 mm] all positions",
                    "single_pass_fillet": {"Flat": "1/2 in [12 mm]", "Horizontal": "3/8 in [10 mm]", "Vertical": "1/2 in [12 mm]", "Overhead": "5/16 in [8 mm]"},
                },
            }

            preheat_rules = {
                "ASTM A36": {
                    "category": "A (SMAW non-LH) or B (SMAW LH, SAW, GMAW, FCAW)",
                    "Cat_A": {
                        "up_to_19mm": "32°F [0°C] min",
                        "19_to_38mm": "150°F [65°C] min",
                        "38_to_65mm": "225°F [110°C] min",
                        "over_65mm": "300°F [150°C] min",
                    },
                    "Cat_B": {
                        "up_to_19mm": "32°F [0°C] min",
                        "19_to_38mm": "50°F [10°C] min",
                        "38_to_65mm": "150°F [65°C] min",
                        "over_65mm": "225°F [110°C] min",
                    },
                },
                "ASTM A572 Gr.50": {
                    "category": "B",
                    "Cat_B": {
                        "up_to_19mm": "32°F [0°C] min",
                        "19_to_38mm": "50°F [10°C] min",
                        "38_to_65mm": "150°F [65°C] min",
                        "over_65mm": "225°F [110°C] min",
                    },
                },
                "ASTM A572 Gr.60": {
                    "category": "C",
                    "Cat_C": {
                        "up_to_19mm": "50°F [10°C] min",
                        "19_to_38mm": "150°F [65°C] min",
                        "38_to_65mm": "225°F [110°C] min",
                        "over_65mm": "300°F [150°C] min",
                    },
                },
            }

            # ── Get relevant data for this situation ──
            process_data = ""
            if process == "SMAW":
                wt = weld_type if weld_type in smaw_rules.get(position, {}) else "All"
                rule = smaw_rules.get(position, {}).get(wt, smaw_rules.get(position, {}).get("All", {}))
                process_data = f"Max electrode diameter: {rule.get('max_electrode', 'N/A')} | Exception: {rule.get('exception', 'None')}"
            elif process == "SAW":
                process_data = str(saw_rules)
            elif process == "GMAW":
                process_data = str(gmaw_rules)
            elif process == "FCAW":
                process_data = str(fcaw_rules)

            bead_data = str(bead_limits.get(process, {}))
            preheat_data = str(preheat_rules.get(base_metal, "Refer to Table 5.11 for specific requirements"))

            # ── Determine thickness category ──
            if thickness <= 19:
                thickness_cat = "up_to_19mm"
            elif thickness <= 38:
                thickness_cat = "19_to_38mm"
            elif thickness <= 65:
                thickness_cat = "38_to_65mm"
            else:
                thickness_cat = "over_65mm"

            context = f"""
You are a strict and precise expert welding engineer specializing in AWS D1.1/D1.1M:2025.
You MUST use ONLY the exact data provided below from the official AWS D1.1 tables.
Do NOT use general knowledge — only use the numbers from the tables provided.

═══════════════════════════════════════════
USER'S WELDING SITUATION
═══════════════════════════════════════════
- Welding Process: {process}
- Welding Position: {position}
- Weld Type: {weld_type}
- Base Metal: {base_metal}
- Material Thickness: {thickness} mm (Category: {thickness_cat})
- Electrode/Wire: {electrode if electrode else "Not specified"}
- Ambient Temperature: {ambient_temp}°C
- Weather/Humidity: {humidity}
- Welding Location: {location}
- Structure Criticality: {criticality}
- Additional Description: {additional if additional else "None provided"}

═══════════════════════════════════════════
EXACT AWS D1.1 TABLE DATA FOR THIS SITUATION
═══════════════════════════════════════════
PROCESS REQUIREMENTS (from Tables 5.1-5.4):
{process_data}

BEAD THICKNESS LIMITS (from Tables 5.1-5.4):
{bead_data}

PREHEAT REQUIREMENTS (from Table 5.11):
{preheat_data}
Thickness category for this job: {thickness_cat}

═══════════════════════════════════════════
PLEASE PROVIDE YOUR ANALYSIS WITH THESE SECTIONS:
═══════════════════════════════════════════

1. ⚡ ELECTRODE/WIRE REQUIREMENTS
   - State the EXACT maximum diameter from the table data above
   - Mention any exceptions

2. 🔌 CURRENT REQUIREMENTS
   - Refer to manufacturer recommendations
   - Any process-specific limits

3. 📏 BEAD THICKNESS LIMITS
   - State EXACT root bead limit from table data
   - State EXACT fill and cap bead limit
   - State EXACT single pass fillet size limit

4. 🌡️ PREHEAT REQUIREMENTS
   - State the EXACT minimum preheat temperature from table data for this thickness
   - ⚠️ IMPORTANT: The ambient temperature is {ambient_temp}°C
   - If ambient temp is BELOW the minimum preheat → give a STRONG WARNING
   - If ambient temp is below 0°C → warn about hydrogen cracking risk
   - State interpass temperature requirements

5. 🌍 ENVIRONMENTAL ASSESSMENT
   - Analyze the impact of: {humidity}, {location}, ambient temp {ambient_temp}°C
   - Give specific recommendations for these conditions
   - If conditions are severe → recommend additional precautions
   - Consider impact on: electrode storage, moisture, wind, visibility

6. 🏗️ STRUCTURE CRITICALITY ASSESSMENT
   - Consider that this is a: {criticality}
   - Give additional requirements or precautions for this criticality level
   - Mention any additional NDT or inspection requirements

7. ⚠️ WARNINGS & CRITICAL POINTS
   - List all critical warnings specific to this situation
   - Be especially strict about environmental conditions
   - Mention hydrogen cracking risk if relevant

8. ✅ SUMMARY & RECOMMENDATIONS
   - Clear action list for the welder
   - Most critical points to remember
   - Go/No-Go recommendation based on current conditions

Be direct, specific, and safety-focused. Use the EXACT numbers from the table data provided.
"""

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a strict welding engineering expert. Always use exact numbers from the provided AWS D1.1 table data. Never make up numbers. Always prioritize safety especially in harsh environmental conditions."
                        },
                        {
                            "role": "user",
                            "content": context
                        }
                    ],
                    max_tokens=2000,
                    temperature=0.1,
                )

                result = response.choices[0].message.content

                st.success("✅ AI Analysis Complete!")
                st.divider()
                st.markdown(result)
                st.divider()
                st.caption("⚠️ This AI interpretation is for reference only. Always verify against the official AWS D1.1/D1.1M:2025 standard before production welding.")

            except Exception as e:
                st.error(f"❌ Error connecting to AI: {str(e)}")
                st.info("Please check your API key in .streamlit/secrets.toml")

with tab10:
    st.subheader("📄 WPS Generator — AWS D1.1 Annex J Form J-2")
    st.markdown("Generate a professional WPS document matching the **official AWS D1.1/D1.1M Annex J** format.")
    st.divider()

    # ── SECTION 1: HEADER INFO ──
    st.markdown("### 🏢 Header Information")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        company_name = st.text_input("Company Name:", placeholder="e.g. Genova Steel Ltd")
    with col2:
        wps_number = st.text_input("WPS No.:", placeholder="e.g. WPS-001-2025")
    with col3:
        rev_number = st.text_input("Rev. No.:", value="0")
    with col4:
        wps_date = st.date_input("Date:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        authorized_by = st.text_input("Authorized By:", placeholder="e.g. Babak Pirzadi")
    with col2:
        auth_date = st.date_input("Authorization Date:")
    with col3:
        supporting_pqr = st.text_input("Supporting PQR(s):", placeholder="e.g. PQR-001-2025")
    with col4:
        cvn_report = st.text_input("CVN Report:", placeholder="e.g. N/A")

    st.divider()

    # ── SECTION 2: BASE METALS ──
    st.markdown("### 🏗️ Base Metals")
    col1, col2 = st.columns(2)
    with col1:
        bm_spec = st.text_input("Base Material Specification:", placeholder="e.g. ASTM A36")
        bm_type_grade = st.text_input("Type or Grade:", placeholder="e.g. Grade B")
        bm_aws_group = st.text_input("AWS Group No.:", placeholder="e.g. Group I")
        bm_welded_to = st.text_input("Welded To (Specification):", placeholder="e.g. ASTM A572 Gr.50")
        bm_backing = st.text_input("Backing Material:", placeholder="e.g. Steel / None")
        bm_diameter = st.text_input("Diameter (pipe/tube):", placeholder="e.g. 168.3 mm OD / N/A")

    with col2:
        st.markdown("**Base Metal Thickness Ranges:**")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("*As-Welded*")
            thick_cjp_aw = st.text_input("CJP Groove Welds:", placeholder="e.g. 6-25 mm", key="cjp_aw")
            thick_cjp_cvn_aw = st.text_input("CJP Groove w/CVN:", placeholder="e.g. N/A", key="cjp_cvn_aw")
            thick_pjp_aw = st.text_input("PJP Groove Welds:", placeholder="e.g. 6-50 mm", key="pjp_aw")
            thick_fillet_aw = st.text_input("Fillet Welds:", placeholder="e.g. All", key="fillet_aw")
        with col_b:
            st.markdown("*With PWHT*")
            thick_cjp_pwht = st.text_input("CJP Groove Welds:", placeholder="e.g. N/A", key="cjp_pwht")
            thick_cjp_cvn_pwht = st.text_input("CJP Groove w/CVN:", placeholder="e.g. N/A", key="cjp_cvn_pwht")
            thick_pjp_pwht = st.text_input("PJP Groove Welds:", placeholder="e.g. N/A", key="pjp_pwht")
            thick_fillet_pwht = st.text_input("Fillet Welds:", placeholder="e.g. N/A", key="fillet_pwht")

    st.divider()

    # ── SECTION 3: JOINT DETAILS ──
    st.markdown("### 🔧 Joint Details")
    col1, col2 = st.columns(2)
    with col1:
        groove_type = st.selectbox("Groove Type:",
            ["Single-V", "Double-V", "Single-Bevel", "Double-Bevel",
             "Single-U", "Double-U", "Square", "Fillet"])
        groove_angle = st.text_input("Groove Angle:", placeholder="e.g. 60°")
        root_opening = st.text_input("Root Opening:", placeholder="e.g. 0-3 mm")
        root_face = st.text_input("Root Face:", placeholder="e.g. 0-3 mm")
        backgouging = st.selectbox("Backgouging:", ["Yes", "No"])
        backgouging_method = st.text_input("Backgouging Method:", placeholder="e.g. Carbon arc / Grinding / N/A")
    with col2:
        st.markdown("**Joint Sketch Description:**")
        joint_sketch = st.text_area("Joint Sketch Notes:",
            placeholder="Describe the joint geometry or reference drawing number...",
            height=180)

    st.divider()

    # ── SECTION 4: POSTWELD HEAT TREATMENT ──
    st.markdown("### 🔥 Postweld Heat Treatment (PWHT)")
    col1, col2, col3 = st.columns(3)
    with col1:
        pwht_temp = st.text_input("Temperature:", placeholder="e.g. N/A or 620°C")
    with col2:
        pwht_time = st.text_input("Time at Temperature:", placeholder="e.g. N/A or 1 hour")
    with col3:
        pwht_other = st.text_input("Other:", placeholder="e.g. Heating rate 150°C/hr")

    st.divider()

    # ── SECTION 5: PROCEDURE ──
    st.markdown("### ⚡ Procedure")
    col1, col2 = st.columns(2)
    with col1:
        weld_layers = st.text_input("Weld Layer(s):", placeholder="e.g. All / 1 / 2-n")
        weld_passes = st.text_input("Weld Pass(es):", placeholder="e.g. All / Root / Fill")
        process = st.text_input("Process:", value="SAW")
        process_type = st.selectbox("Type:",
            ["Semiautomatic", "Mechanized", "Automatic", "Manual"])
        position = st.selectbox("Position:",
            ["Flat (1G/1F)", "Horizontal (2G/2F)", "Vertical-Up (3G/3F)",
             "Overhead (4G/4F)", "Fixed Pipe (5G)", "All (6G)"])
    with col2:
        filler_spec = st.text_input("Filler Metal (AWS Spec.):", placeholder="e.g. AWS A5.17")
        aws_class = st.text_input("AWS Classification:", placeholder="e.g. EM12K")
        electrode_dia = st.text_input("Electrode Diameter:", placeholder="e.g. 4.0 mm")
        electrode_flux = st.text_input("Electrode/Flux Classification:", placeholder="e.g. F7A2-EM12K")
        manufacturer = st.text_input("Manufacturer/Trade Name:", placeholder="e.g. Lincoln Electric")
        supplemental_filler = st.text_input("Supplemental Filler Metal:", placeholder="e.g. N/A")
        preheat_temp = st.text_input("Preheat Temperature:", placeholder="e.g. 10°C [50°F] min")
        interpass_temp = st.text_input("Interpass Temperature:", placeholder="e.g. 250°C [480°F] max")

    st.divider()

    # ── SECTION 6: ELECTRICAL CHARACTERISTICS ──
    st.markdown("### 🔌 Electrical Characteristics")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        current_polarity = st.selectbox("Current Type & Polarity:",
            ["DCEP", "DCEN", "AC", "Pulsed DCEP"])
    with col2:
        amps = st.text_input("Amps:", placeholder="e.g. 500-700 A")
    with col3:
        volts = st.text_input("Volts:", placeholder="e.g. 28-34 V")
    with col4:
        wire_feed = st.text_input("Wire Feed Speed:", placeholder="e.g. 1200-1800 mm/min")
    with col5:
        travel_speed = st.text_input("Travel Speed:", placeholder="e.g. 400-600 mm/min")

    col1, col2 = st.columns(2)
    with col1:
        max_heat_input = st.text_input("Maximum Heat Input:", placeholder="e.g. 3.5 kJ/mm")
    with col2:
        shielding_gas = st.text_input("Shielding Gas (if applicable):", placeholder="e.g. N/A for SAW")

    st.divider()

    # ── SECTION 7: TECHNIQUE ──
    st.markdown("### 🛠️ Technique")
    col1, col2, col3 = st.columns(3)
    with col1:
        stringer_weave = st.selectbox("Stringer or Weave:", ["Stringer", "Weave", "Both"])
        multi_single_pass = st.selectbox("Multi or Single Pass (per side):",
            ["Multi-pass", "Single pass", "Both"])
        num_electrodes = st.text_input("Number of Electrodes:", placeholder="e.g. 1 / 2 (tandem)")
    with col2:
        long_spacing = st.text_input("Longitudinal Spacing of Arcs:", placeholder="e.g. N/A")
        lateral_spacing = st.text_input("Lateral Spacing of Arcs:", placeholder="e.g. N/A")
        angle_parallel = st.text_input("Angle of Parallel Electrodes:", placeholder="e.g. N/A")
        angle_electrode = st.text_input("Angle of Electrode (Mech./Auto.):", placeholder="e.g. 90°")
    with col3:
        normal_direction = st.text_input("Normal To Direction of Travel:", placeholder="e.g. 90°")
        oscillation = st.text_input("Oscillation (Mech./Auto.):", placeholder="e.g. N/A")
        traverse_length = st.text_input("Traverse Length:", placeholder="e.g. N/A")
        traverse_speed = st.text_input("Traverse Speed:", placeholder="e.g. N/A")
        dwell_time = st.text_input("Dwell Time:", placeholder="e.g. N/A")

    col1, col2, col3 = st.columns(3)
    with col1:
        peening = st.text_input("Peening:", placeholder="e.g. None")
    with col2:
        interpass_cleaning = st.text_input("Interpass Cleaning:", placeholder="e.g. Wire brush / Grinding")
    with col3:
        other_technique = st.text_input("Other:", placeholder="e.g. N/A")

    st.divider()

    # ── GENERATE BUTTONS ──
    st.markdown("### 📥 Generate WPS Document")
    col1, col2 = st.columns(2)
    with col1:
        generate_pdf = st.button("📄 Generate PDF", use_container_width=True)
    with col2:
        generate_docx = st.button("📝 Generate Word (.docx)", use_container_width=True)

    # ════════════════════════════════════════════════════════
    # PDF GENERATION
    # ════════════════════════════════════════════════════════
    if generate_pdf:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import mm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
            import io

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                rightMargin=10*mm, leftMargin=10*mm,
                topMargin=10*mm, bottomMargin=10*mm)

            styles = getSampleStyleSheet()
            story = []

            # Colors
            dark_blue = colors.HexColor('#1a3a5c')
            light_blue = colors.HexColor('#d6e4f0')
            light_gray = colors.HexColor('#f5f5f5')
            mid_gray = colors.HexColor('#e0e0e0')

            # Styles
            hdr_style = ParagraphStyle('Hdr', fontSize=7, fontName='Helvetica-Bold',
                textColor=colors.white)
            cell_style = ParagraphStyle('Cell', fontSize=7, fontName='Helvetica')
            cell_bold = ParagraphStyle('CellBold', fontSize=7, fontName='Helvetica-Bold')
            title_style = ParagraphStyle('Title', fontSize=12, fontName='Helvetica-Bold',
                textColor=dark_blue, alignment=TA_CENTER)
            sub_style = ParagraphStyle('Sub', fontSize=8, fontName='Helvetica',
                textColor=dark_blue, alignment=TA_CENTER)

            W = 190*mm  # total width

            def hdr(text):
                return Paragraph(f'<b>{text}</b>', hdr_style)

            def cell(text):
                return Paragraph(str(text) if text else '—', cell_style)

            def field(label, value):
                return [Paragraph(f'<b>{label}</b>', cell_bold),
                        Paragraph(str(value) if value else '—', cell_style)]

            def section_hdr(text, colspan=4):
                t = Table([[hdr(text)]], colWidths=[W])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), dark_blue),
                    ('TOPPADDING', (0,0), (-1,-1), 3),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                    ('LEFTPADDING', (0,0), (-1,-1), 5),
                ]))
                return t

            def make_table(rows, col_widths, bg=True):
                t = Table(rows, colWidths=col_widths)
                style = [
                    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                    ('LEFTPADDING', (0,0), (-1,-1), 4),
                ]
                if bg:
                    for i in range(len(rows)):
                        bg_color = light_gray if i % 2 == 0 else colors.white
                        style.append(('BACKGROUND', (0,i), (-1,i), bg_color))
                t.setStyle(TableStyle(style))
                return t

            # ── TITLE ──
            story.append(Paragraph('WELDING PROCEDURE SPECIFICATION (WPS)', title_style))
            story.append(Paragraph('AWS D1.1/D1.1M:2020 — Annex J, Form J-2', sub_style))
            story.append(Spacer(1, 3*mm))

            # ── HEADER BLOCK ──
            hdr_rows = [
                [hdr('Company Name'), cell(company_name),
                 hdr('WPS No.'), cell(wps_number),
                 hdr('Rev. No.'), cell(rev_number),
                 hdr('Date'), cell(str(wps_date))],
                [hdr('Authorized By'), cell(authorized_by),
                 hdr('Auth. Date'), cell(str(auth_date)),
                 hdr('Supporting PQR(s)'), cell(supporting_pqr),
                 hdr('CVN Report'), cell(cvn_report)],
            ]
            hdr_table = Table(hdr_rows,
                colWidths=[25*mm, 35*mm, 18*mm, 25*mm, 18*mm, 20*mm, 18*mm, 25*mm])
            hdr_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), dark_blue),
                ('BACKGROUND', (2,0), (2,-1), dark_blue),
                ('BACKGROUND', (4,0), (4,-1), dark_blue),
                ('BACKGROUND', (6,0), (6,-1), dark_blue),
                ('BACKGROUND', (1,0), (1,-1), light_blue),
                ('BACKGROUND', (3,0), (3,-1), light_blue),
                ('BACKGROUND', (5,0), (5,-1), light_blue),
                ('BACKGROUND', (7,0), (7,-1), light_blue),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(hdr_table)
            story.append(Spacer(1, 2*mm))

            # ── BASE METALS + JOINT DETAILS (side by side) ──
            story.append(section_hdr('BASE METALS'))
            bm_left = [
                [hdr('Specification'), hdr('Type or Grade'), hdr('AWS Group No.')],
                [cell(bm_spec), cell(bm_type_grade), cell(bm_aws_group)],
                [hdr('Base Material'), hdr('Welded To'), hdr('Backing Material')],
                [cell(bm_spec), cell(bm_welded_to), cell(bm_backing)],
                [hdr('Diameter'), cell(bm_diameter), ''],
            ]
            bm_table = Table(bm_left, colWidths=[W/3, W/3, W/3])
            bm_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), dark_blue),
                ('BACKGROUND', (0,2), (-1,2), dark_blue),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [light_gray, colors.white]),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
                ('SPAN', (1,4), (2,4)),
            ]))
            story.append(bm_table)

            # Thickness table
            thick_rows = [
                [hdr('BASE METAL THICKNESS'), hdr('As-Welded'), hdr('With PWHT')],
                [cell('CJP Groove Welds'), cell(thick_cjp_aw), cell(thick_cjp_pwht)],
                [cell('CJP Groove w/CVN'), cell(thick_cjp_cvn_aw), cell(thick_cjp_cvn_pwht)],
                [cell('PJP Groove Welds'), cell(thick_pjp_aw), cell(thick_pjp_pwht)],
                [cell('Fillet Welds'), cell(thick_fillet_aw), cell(thick_fillet_pwht)],
            ]
            thick_table = Table(thick_rows, colWidths=[W/3, W/3, W/3])
            thick_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), dark_blue),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [light_gray, colors.white]),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(thick_table)
            story.append(Spacer(1, 2*mm))

            # ── JOINT DETAILS ──
            story.append(section_hdr('JOINT DETAILS'))
            jd_rows = [
                [hdr('Groove Type'), cell(groove_type),
                 hdr('Root Opening'), cell(root_opening)],
                [hdr('Groove Angle'), cell(groove_angle),
                 hdr('Root Face'), cell(root_face)],
                [hdr('Backgouging'), cell(backgouging),
                 hdr('Method'), cell(backgouging_method)],
                [hdr('Joint Sketch Notes'), cell(joint_sketch), '', ''],
            ]
            jd_table = Table(jd_rows, colWidths=[W/4, W/4, W/4, W/4])
            jd_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), dark_blue),
                ('BACKGROUND', (2,0), (2,2), dark_blue),
                ('ROWBACKGROUNDS', (1,0), (1,-1), [light_gray, colors.white, light_gray, colors.white]),
                ('ROWBACKGROUNDS', (3,0), (3,-1), [light_gray, colors.white, light_gray, colors.white]),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('SPAN', (1,3), (3,3)),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(jd_table)
            story.append(Spacer(1, 2*mm))

            # ── PWHT ──
            story.append(section_hdr('POSTWELD HEAT TREATMENT'))
            pwht_rows = [
                [hdr('Temperature'), hdr('Time at Temperature'), hdr('Other')],
                [cell(pwht_temp), cell(pwht_time), cell(pwht_other)],
            ]
            pwht_table = Table(pwht_rows, colWidths=[W/3, W/3, W/3])
            pwht_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), dark_blue),
                ('BACKGROUND', (0,1), (-1,1), light_gray),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(pwht_table)
            story.append(Spacer(1, 2*mm))

            # ── PROCEDURE ──
            story.append(section_hdr('PROCEDURE'))
            proc_rows = [
                [hdr('Weld Layer(s)'), cell(weld_layers),
                 hdr('Weld Pass(es)'), cell(weld_passes),
                 hdr('Process'), cell(process),
                 hdr('Type'), cell(process_type)],
                [hdr('Position'), cell(position),
                 hdr('Filler Metal (AWS Spec.)'), cell(filler_spec),
                 hdr('AWS Classification'), cell(aws_class),
                 hdr('Electrode Dia.'), cell(electrode_dia)],
                [hdr('Electrode/Flux Class.'), cell(electrode_flux),
                 hdr('Manufacturer/Trade Name'), cell(manufacturer),
                 hdr('Supplemental Filler'), cell(supplemental_filler),
                 hdr(''), cell('')],
                [hdr('Preheat Temperature'), cell(preheat_temp),
                 hdr('Interpass Temperature'), cell(interpass_temp),
                 hdr('Shielding Gas'), cell(shielding_gas),
                 hdr(''), cell('')],
            ]
            proc_table = Table(proc_rows,
                colWidths=[W/8, W/8, W/8, W/8, W/8, W/8, W/8, W/8])
            proc_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), dark_blue),
                ('BACKGROUND', (2,0), (2,-1), dark_blue),
                ('BACKGROUND', (4,0), (4,-1), dark_blue),
                ('BACKGROUND', (6,0), (6,-1), dark_blue),
                ('ROWBACKGROUNDS', (1,0), (1,-1), [light_gray, colors.white, light_gray, colors.white]),
                ('ROWBACKGROUNDS', (3,0), (3,-1), [light_gray, colors.white, light_gray, colors.white]),
                ('ROWBACKGROUNDS', (5,0), (5,-1), [light_gray, colors.white, light_gray, colors.white]),
                ('ROWBACKGROUNDS', (7,0), (7,-1), [light_gray, colors.white, light_gray, colors.white]),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(proc_table)
            story.append(Spacer(1, 2*mm))

            # ── ELECTRICAL CHARACTERISTICS ──
            story.append(section_hdr('ELECTRICAL CHARACTERISTICS'))
            elec_rows = [
                [hdr('Current Type & Polarity'), hdr('Amps'),
                 hdr('Volts'), hdr('Wire Feed Speed'),
                 hdr('Travel Speed'), hdr('Max Heat Input')],
                [cell(current_polarity), cell(amps),
                 cell(volts), cell(wire_feed),
                 cell(travel_speed), cell(max_heat_input)],
            ]
            elec_table = Table(elec_rows,
                colWidths=[W/6, W/6, W/6, W/6, W/6, W/6])
            elec_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), dark_blue),
                ('BACKGROUND', (0,1), (-1,1), light_gray),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(elec_table)
            story.append(Spacer(1, 2*mm))

            # ── TECHNIQUE ──
            story.append(section_hdr('TECHNIQUE'))
            tech_rows = [
                [hdr('Stringer or Weave'), cell(stringer_weave),
                 hdr('Multi/Single Pass'), cell(multi_single_pass),
                 hdr('No. of Electrodes'), cell(num_electrodes)],
                [hdr('Long. Spacing of Arcs'), cell(long_spacing),
                 hdr('Lateral Spacing of Arcs'), cell(lateral_spacing),
                 hdr('Angle of Parallel Electrodes'), cell(angle_parallel)],
                [hdr('Angle of Electrode'), cell(angle_electrode),
                 hdr('Normal to Direction of Travel'), cell(normal_direction),
                 hdr('Oscillation'), cell(oscillation)],
                [hdr('Traverse Length'), cell(traverse_length),
                 hdr('Traverse Speed'), cell(traverse_speed),
                 hdr('Dwell Time'), cell(dwell_time)],
                [hdr('Peening'), cell(peening),
                 hdr('Interpass Cleaning'), cell(interpass_cleaning),
                 hdr('Other'), cell(other_technique)],
            ]
            tech_table = Table(tech_rows,
                colWidths=[W/6, W/6, W/6, W/6, W/6, W/6])
            tech_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,-1), dark_blue),
                ('BACKGROUND', (2,0), (2,-1), dark_blue),
                ('BACKGROUND', (4,0), (4,-1), dark_blue),
                ('ROWBACKGROUNDS', (1,0), (1,-1), [light_gray, colors.white, light_gray, colors.white, light_gray]),
                ('ROWBACKGROUNDS', (3,0), (3,-1), [light_gray, colors.white, light_gray, colors.white, light_gray]),
                ('ROWBACKGROUNDS', (5,0), (5,-1), [light_gray, colors.white, light_gray, colors.white, light_gray]),
                ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#aaaaaa')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(tech_table)
            story.append(Spacer(1, 3*mm))

            # ── FOOTER ──
            footer_rows = [
                [Paragraph('Form J-2 | AWS D1.1/D1.1M:2020 — Annex J | '
                           'Generated by Welding Engineering Toolbox | '
                           'For official use, verify against the current edition of AWS D1.1',
                           ParagraphStyle('Footer', fontSize=6,
                           textColor=colors.gray, alignment=TA_CENTER))]
            ]
            footer_table = Table(footer_rows, colWidths=[W])
            footer_table.setStyle(TableStyle([
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('LINEABOVE', (0,0), (-1,0), 0.5, colors.gray),
            ]))
            story.append(footer_table)

            doc.build(story)
            buffer.seek(0)

            st.success("✅ PDF generated successfully!")
            st.download_button(
                label="📥 Download WPS PDF",
                data=buffer,
                file_name=f"WPS_{wps_number}_{wps_date}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")

    # ════════════════════════════════════════════════════════
    # DOCX GENERATION
    # ════════════════════════════════════════════════════════
    if generate_docx:
        try:
            from docx import Document as DocxDocument
            from docx.shared import Pt, RGBColor, Cm
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            from docx.enum.table import WD_TABLE_ALIGNMENT
            from docx.oxml.ns import qn
            from docx.oxml import OxmlElement
            import io

            docx_buffer = io.BytesIO()
            document = DocxDocument()

            section = document.sections[0]
            section.top_margin = Cm(1.5)
            section.bottom_margin = Cm(1.5)
            section.left_margin = Cm(1.5)
            section.right_margin = Cm(1.5)

            def set_cell_bg(cell, hex_color):
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), hex_color)
                tcPr.append(shd)

            def set_cell_text(cell, text, bold=False, white=False, size=8):
                cell.text = str(text) if text else '—'
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.font.size = Pt(size)
                        run.font.bold = bold
                        if white:
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

            def add_section_header(doc, title):
                table = doc.add_table(rows=1, cols=1)
                table.style = 'Table Grid'
                cell = table.rows[0].cells[0]
                set_cell_bg(cell, '1a3a5c')
                set_cell_text(cell, title, bold=True, white=True, size=9)

            def add_two_col_table(doc, rows_data):
                table = doc.add_table(rows=len(rows_data), cols=2)
                table.style = 'Table Grid'
                for i, (label, value) in enumerate(rows_data):
                    row = table.rows[i]
                    set_cell_bg(row.cells[0], 'd6e4f0')
                    set_cell_text(row.cells[0], label, bold=True, size=8)
                    bg = 'f5f5f5' if i % 2 == 0 else 'ffffff'
                    set_cell_bg(row.cells[1], bg)
                    set_cell_text(row.cells[1], value, size=8)
                doc.add_paragraph()

            # Title
            title_para = document.add_paragraph()
            title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = title_para.add_run('WELDING PROCEDURE SPECIFICATION (WPS)')
            run.font.bold = True
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0x1a, 0x3a, 0x5c)

            sub_para = document.add_paragraph()
            sub_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = sub_para.add_run('AWS D1.1/D1.1M:2020 — Annex J, Form J-2')
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x1a, 0x3a, 0x5c)

            document.add_paragraph()

            # Header block
            add_section_header(document, 'DOCUMENT HEADER')
            add_two_col_table(document, [
                ('Company Name:', company_name),
                ('WPS No.:', wps_number),
                ('Rev. No.:', rev_number),
                ('Date:', str(wps_date)),
                ('Authorized By:', authorized_by),
                ('Authorization Date:', str(auth_date)),
                ('Supporting PQR(s):', supporting_pqr),
                ('CVN Report:', cvn_report),
            ])

            # Base metals
            add_section_header(document, 'BASE METALS')
            add_two_col_table(document, [
                ('Specification:', bm_spec),
                ('Type or Grade:', bm_type_grade),
                ('AWS Group No.:', bm_aws_group),
                ('Welded To:', bm_welded_to),
                ('Backing Material:', bm_backing),
                ('Diameter:', bm_diameter),
                ('CJP Groove Welds (As-Welded):', thick_cjp_aw),
                ('CJP Groove Welds (With PWHT):', thick_cjp_pwht),
                ('CJP Groove w/CVN (As-Welded):', thick_cjp_cvn_aw),
                ('CJP Groove w/CVN (With PWHT):', thick_cjp_cvn_pwht),
                ('PJP Groove Welds (As-Welded):', thick_pjp_aw),
                ('PJP Groove Welds (With PWHT):', thick_pjp_pwht),
                ('Fillet Welds (As-Welded):', thick_fillet_aw),
                ('Fillet Welds (With PWHT):', thick_fillet_pwht),
            ])

            # Joint details
            add_section_header(document, 'JOINT DETAILS')
            add_two_col_table(document, [
                ('Groove Type:', groove_type),
                ('Groove Angle:', groove_angle),
                ('Root Opening:', root_opening),
                ('Root Face:', root_face),
                ('Backgouging:', backgouging),
                ('Backgouging Method:', backgouging_method),
                ('Joint Sketch Notes:', joint_sketch),
            ])

            # PWHT
            add_section_header(document, 'POSTWELD HEAT TREATMENT')
            add_two_col_table(document, [
                ('Temperature:', pwht_temp),
                ('Time at Temperature:', pwht_time),
                ('Other:', pwht_other),
            ])

            # Procedure
            add_section_header(document, 'PROCEDURE')
            add_two_col_table(document, [
                ('Weld Layer(s):', weld_layers),
                ('Weld Pass(es):', weld_passes),
                ('Process:', process),
                ('Type:', process_type),
                ('Position:', position),
                ('Filler Metal (AWS Spec.):', filler_spec),
                ('AWS Classification:', aws_class),
                ('Electrode Diameter:', electrode_dia),
                ('Electrode/Flux Classification:', electrode_flux),
                ('Manufacturer/Trade Name:', manufacturer),
                ('Supplemental Filler Metal:', supplemental_filler),
                ('Preheat Temperature:', preheat_temp),
                ('Interpass Temperature:', interpass_temp),
                ('Shielding Gas:', shielding_gas),
            ])

            # Electrical
            add_section_header(document, 'ELECTRICAL CHARACTERISTICS')
            add_two_col_table(document, [
                ('Current Type & Polarity:', current_polarity),
                ('Amps:', amps),
                ('Volts:', volts),
                ('Wire Feed Speed:', wire_feed),
                ('Travel Speed:', travel_speed),
                ('Maximum Heat Input:', max_heat_input),
            ])

            # Technique
            add_section_header(document, 'TECHNIQUE')
            add_two_col_table(document, [
                ('Stringer or Weave:', stringer_weave),
                ('Multi or Single Pass (per side):', multi_single_pass),
                ('Number of Electrodes:', num_electrodes),
                ('Longitudinal Spacing of Arcs:', long_spacing),
                ('Lateral Spacing of Arcs:', lateral_spacing),
                ('Angle of Parallel Electrodes:', angle_parallel),
                ('Angle of Electrode (Mech./Auto.):', angle_electrode),
                ('Normal To Direction of Travel:', normal_direction),
                ('Oscillation:', oscillation),
                ('Traverse Length:', traverse_length),
                ('Traverse Speed:', traverse_speed),
                ('Dwell Time:', dwell_time),
                ('Peening:', peening),
                ('Interpass Cleaning:', interpass_cleaning),
                ('Other:', other_technique),
            ])

            # Footer
            footer_para = document.add_paragraph()
            footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = footer_para.add_run(
                'Form J-2 | AWS D1.1/D1.1M:2020 Annex J | '
                'Generated by Welding Engineering Toolbox | '
                'Verify against current standard edition')
            run.font.size = Pt(7)
            run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

            document.save(docx_buffer)
            docx_buffer.seek(0)

            st.success("✅ Word document generated successfully!")
            st.download_button(
                label="📥 Download WPS Word (.docx)",
                data=docx_buffer,
                file_name=f"WPS_{wps_number}_{wps_date}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"❌ Error generating Word document: {str(e)}")

st.divider()
st.caption("📖 Reference: AWS D1.1/D1.1M:2025 — Clause 5 | For educational reference only. Always verify against the official published standard.")
