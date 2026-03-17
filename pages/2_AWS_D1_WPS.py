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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "⚡ SMAW (5.1)",
    "🔩 SAW (5.2)",
    "🌀 GMAW (5.3)",
    "🔥 FCAW (5.4)",
    "🌡️ Preheat (5.11)",
    "📐 PJP Min Size (5.8)",
    "🏗️ Base Metals (5.6)",
    "🔧 Filler Metals (5.7)",
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

st.divider()
st.caption("📖 Reference: AWS D1.1/D1.1M:2025 — Clause 5 | For educational reference only. Always verify against the official published standard.")
