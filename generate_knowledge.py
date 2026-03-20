"""
generate_knowledge.py
=====================
Run this script once from your project root:
    python generate_knowledge.py

It converts all AWS D1.1 hardcoded table data into natural language
sentences and saves them to standards/welding_knowledge.txt

That file can then be indexed by the RAG engine alongside your PDFs,
giving much more reliable retrieval for Clause 5 data.
"""

output_lines = []

def add(text):
    output_lines.append(text.strip())

# ── SECTION 1: SMAW ELECTRODE LIMITS ─────────────────────────────────────────
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.1 — SMAW Prequalified WPS Requirements")
add("")

add("For SMAW in the Flat position, Fillet weld: the maximum electrode diameter is 5/16 in [8.0 mm], except for the root pass. AWS D1.1 Table 5.1.")
add("For SMAW in the Flat position, Groove weld: the maximum electrode diameter is 1/4 in [6.4 mm], except for the root pass. AWS D1.1 Table 5.1.")
add("For SMAW in the Flat position, Root Pass: the maximum electrode diameter is 3/16 in [4.8 mm]. AWS D1.1 Table 5.1.")
add("For SMAW in the Horizontal position, Fillet weld: the maximum electrode diameter is 1/4 in [6.4 mm]. AWS D1.1 Table 5.1.")
add("For SMAW in the Horizontal position, Groove weld: the maximum electrode diameter is 3/16 in [4.8 mm]. AWS D1.1 Table 5.1.")
add("For SMAW in the Vertical position, all weld types: the maximum electrode diameter is 3/16 in [4.8 mm]. For EXX14 and low-hydrogen electrodes, the maximum is 5/32 in [4.0 mm]. AWS D1.1 Table 5.1.")
add("For SMAW in the Overhead position, all weld types: the maximum electrode diameter is 3/16 in [4.8 mm]. For EXX14 and low-hydrogen electrodes, the maximum is 5/32 in [4.0 mm]. AWS D1.1 Table 5.1.")
add("For SMAW, current must be within the range recommended by the filler metal manufacturer for all positions and weld types. AWS D1.1 Table 5.1.")

# ── SECTION 2: SMAW BEAD THICKNESS LIMITS ────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.1 — SMAW Bead Thickness Limits")
add("")

add("For SMAW in the Flat position: the maximum root bead thickness is 3/8 in [10 mm]. See Clause 5.8.2.1. AWS D1.1 Table 5.1.")
add("For SMAW in the Horizontal position: the maximum root bead thickness is 5/16 in [8 mm]. See Clause 5.8.2.1. AWS D1.1 Table 5.1.")
add("For SMAW in the Vertical position: the maximum root bead thickness is 1/2 in [12 mm]. See Clause 5.8.2.1. AWS D1.1 Table 5.1.")
add("For SMAW in the Overhead position: the maximum root bead thickness is 5/16 in [8 mm]. See Clause 5.8.2.1. AWS D1.1 Table 5.1.")
add("For SMAW, the maximum fill and cap bead thickness is 3/16 in [5 mm] for all positions. AWS D1.1 Table 5.1.")
add("For SMAW in the Flat position, single pass fillet weld: the maximum size is 3/8 in [10 mm]. See Clause 5.6.2. AWS D1.1 Table 5.1.")
add("For SMAW in the Horizontal position, single pass fillet weld: the maximum size is 5/16 in [8 mm]. See Clause 5.6.2. AWS D1.1 Table 5.1.")
add("For SMAW in the Vertical position, single pass fillet weld: the maximum size is 1/2 in [12 mm]. See Clause 5.6.2. AWS D1.1 Table 5.1.")
add("For SMAW in the Overhead position, single pass fillet weld: the maximum size is 5/16 in [8 mm]. See Clause 5.6.2. AWS D1.1 Table 5.1.")

# ── SECTION 3: SAW REQUIREMENTS ──────────────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.2 — SAW Prequalified WPS Requirements")
add("")

add("For SAW: the maximum electrode diameter is 1/4 in [6.4 mm]. SAW is only prequalified for Flat and Horizontal positions. AWS D1.1 Table 5.2.")
add("For SAW, Fillet weld, single electrode: maximum current is 1000 A. AWS D1.1 Table 5.2.")
add("For SAW, Fillet weld, parallel electrodes: maximum current is 1200 A. AWS D1.1 Table 5.2.")
add("For SAW, Fillet weld, multiple electrodes: current is unlimited. AWS D1.1 Table 5.2.")
add("For SAW, Groove weld, root pass with joint opening, single electrode: maximum current is 600 A. AWS D1.1 Table 5.2.")
add("For SAW, Groove weld, root pass with joint opening, parallel electrodes: maximum current is 700 A. AWS D1.1 Table 5.2.")
add("For SAW, Groove weld, root pass without joint opening, single electrode: maximum current is 900 A. AWS D1.1 Table 5.2.")
add("For SAW, Groove weld, fill beads, single electrode: maximum current is 1200 A. AWS D1.1 Table 5.2.")
add("For SAW, fill and cap bead thickness, single electrode: maximum is 1/4 in [6 mm]. AWS D1.1 Table 5.2.")
add("For SAW, fill and cap bead thickness, multiple electrodes: unlimited. AWS D1.1 Table 5.2.")
add("For SAW, single pass fillet size, single or parallel electrode: maximum is 5/16 in [8 mm]. AWS D1.1 Table 5.2.")
add("For SAW, single pass fillet size, multiple electrodes: maximum is 1/2 in [12 mm]. AWS D1.1 Table 5.2.")

# ── SECTION 4: GMAW REQUIREMENTS ─────────────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.3 — GMAW Prequalified WPS Requirements")
add("")

add("For GMAW: the maximum electrode diameter is 0.0625 in [1.6 mm] for all positions and weld types. AWS D1.1 Table 5.3.")
add("GMAW-S (short circuit transfer) is NOT prequalified under AWS D1.1. A constant voltage (CV) power source must be used. AWS D1.1 Table 5.3.")
add("For GMAW, minimum current by wire size: 0.030 in wire requires 190 A minimum; 0.035 in wire requires 210 A minimum; 0.040 in wire requires 230 A minimum; 0.045 in wire requires 260 A minimum; 0.0625 in wire requires 300 A minimum. AWS D1.1 Table 5.3.")
add("For GMAW in the Flat position: maximum root bead thickness is 3/8 in [10 mm]. AWS D1.1 Table 5.3.")
add("For GMAW in the Horizontal position: maximum root bead thickness is 5/16 in [8 mm]. AWS D1.1 Table 5.3.")
add("For GMAW in the Vertical position: maximum root bead thickness is 1/2 in [12 mm]. AWS D1.1 Table 5.3.")
add("For GMAW in the Overhead position: maximum root bead thickness is 5/16 in [8 mm]. AWS D1.1 Table 5.3.")
add("For GMAW, the maximum fill and cap bead thickness is 1/4 in [6 mm] for all positions. AWS D1.1 Table 5.3.")
add("For GMAW in the Flat position, single pass fillet weld: maximum size is 1/2 in [12 mm]. AWS D1.1 Table 5.3.")
add("For GMAW in the Horizontal position, single pass fillet weld: maximum size is 3/8 in [10 mm]. AWS D1.1 Table 5.3.")
add("For GMAW in the Vertical position, single pass fillet weld: maximum size is 1/2 in [12 mm]. AWS D1.1 Table 5.3.")
add("For GMAW in the Overhead position, single pass fillet weld: maximum size is 5/16 in [8 mm]. AWS D1.1 Table 5.3.")

# ── SECTION 5: FCAW REQUIREMENTS ─────────────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.4 — FCAW Prequalified WPS Requirements")
add("")

add("For FCAW in Flat or Horizontal position, thickness 3/8 in [10 mm] or less: minimum electrode diameter is 0.030 in [0.8 mm]. AWS D1.1 Table 5.4.")
add("For GMAW Metal Cored in Flat or Horizontal position, thickness 3/8 in [10 mm] or less: no minimum electrode diameter. AWS D1.1 Table 5.4.")
add("For FCAW and GMAW Metal Cored in Flat or Horizontal position, thickness over 3/8 in [10 mm]: minimum electrode diameter is 0.045 in [1 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in Flat or Horizontal position, thickness over 3/8 in [10 mm]: maximum electrode diameter is 1/8 in [3.2 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in Vertical position, thickness over 3/8 in [10 mm]: maximum electrode diameter is 3/32 in [2.4 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in Overhead position, thickness over 3/8 in [10 mm]: maximum electrode diameter is 5/64 in [2.2 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in the Flat position: maximum root bead thickness is 3/8 in [10 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in the Horizontal position: maximum root bead thickness is 5/16 in [8 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in the Vertical position: maximum root bead thickness is 1/2 in [12 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in the Overhead position: maximum root bead thickness is 5/16 in [8 mm]. AWS D1.1 Table 5.4.")
add("For FCAW, the maximum fill and cap bead thickness is 1/4 in [6 mm] for all positions. AWS D1.1 Table 5.4.")
add("For FCAW in the Flat position, single pass fillet weld: maximum size is 1/2 in [12 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in the Horizontal position, single pass fillet weld: maximum size is 3/8 in [10 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in the Vertical position, single pass fillet weld: maximum size is 1/2 in [12 mm]. AWS D1.1 Table 5.4.")
add("For FCAW in the Overhead position, single pass fillet weld: maximum size is 5/16 in [8 mm]. AWS D1.1 Table 5.4.")

# ── SECTION 6: PREHEAT REQUIREMENTS ──────────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.11 — Minimum Preheat and Interpass Temperature")
add("")

# Category A
add("Preheat Category A applies to SMAW using non-low-hydrogen electrodes (e.g. E6010, E6011, E7014). AWS D1.1 Table 5.11.")
add("For Category A steels, SMAW non-low-hydrogen, thickness up to 3/4 in [19 mm]: minimum preheat is 32°F [0°C]. If base metal temperature is below 32°F [0°C], preheat to 70°F [20°C] minimum. AWS D1.1 Table 5.11.")
add("For Category A steels, SMAW non-low-hydrogen, thickness over 3/4 in to 1-1/2 in [19 mm to 38 mm]: minimum preheat is 150°F [65°C]. AWS D1.1 Table 5.11.")
add("For Category A steels, SMAW non-low-hydrogen, thickness over 1-1/2 in to 2-1/2 in [38 mm to 65 mm]: minimum preheat is 225°F [110°C]. AWS D1.1 Table 5.11.")
add("For Category A steels, SMAW non-low-hydrogen, thickness over 2-1/2 in [65 mm]: minimum preheat is 300°F [150°C]. AWS D1.1 Table 5.11.")

# Category B
add("Preheat Category B applies to SMAW using low-hydrogen electrodes (e.g. E7018, E7016), SAW, GMAW, and FCAW. AWS D1.1 Table 5.11.")
add("For Category B steels, SMAW low-hydrogen or SAW or GMAW or FCAW, thickness up to 3/4 in [19 mm]: minimum preheat is 32°F [0°C]. AWS D1.1 Table 5.11.")
add("For Category B steels, SMAW low-hydrogen or SAW or GMAW or FCAW, thickness over 3/4 in to 1-1/2 in [19 mm to 38 mm]: minimum preheat is 50°F [10°C]. AWS D1.1 Table 5.11.")
add("For Category B steels, SMAW low-hydrogen or SAW or GMAW or FCAW, thickness over 1-1/2 in to 2-1/2 in [38 mm to 65 mm]: minimum preheat is 150°F [65°C]. AWS D1.1 Table 5.11.")
add("For Category B steels, SMAW low-hydrogen or SAW or GMAW or FCAW, thickness over 2-1/2 in [65 mm]: minimum preheat is 225°F [110°C]. AWS D1.1 Table 5.11.")

# Category C
add("Preheat Category C applies to higher strength steels such as ASTM A572 Gr.60 and Gr.65. AWS D1.1 Table 5.11.")
add("For Category C steels, thickness up to 3/4 in [19 mm]: minimum preheat is 50°F [10°C]. AWS D1.1 Table 5.11.")
add("For Category C steels, thickness over 3/4 in to 1-1/2 in [19 mm to 38 mm]: minimum preheat is 150°F [65°C]. AWS D1.1 Table 5.11.")
add("For Category C steels, thickness over 1-1/2 in to 2-1/2 in [38 mm to 65 mm]: minimum preheat is 225°F [110°C]. AWS D1.1 Table 5.11.")
add("For Category C steels, thickness over 2-1/2 in [65 mm]: minimum preheat is 300°F [150°C]. AWS D1.1 Table 5.11.")

# Steel assignments
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.11 — Steel Category Assignments")
add("")
add("ASTM A36 steel is assigned to Category A when welded with SMAW non-low-hydrogen electrodes, and Category B when welded with SMAW low-hydrogen electrodes, SAW, GMAW, or FCAW. AWS D1.1 Table 5.11.")
add("ASTM A572 Grade 42 and Grade 50 steel is assigned to preheat Category B for all prequalified processes. AWS D1.1 Table 5.11.")
add("ASTM A572 Grade 60 and Grade 65 steel is assigned to preheat Category C for all prequalified processes. AWS D1.1 Table 5.11.")
add("ASTM A588 steel is assigned to preheat Category B for all prequalified processes. AWS D1.1 Table 5.11.")
add("ASTM A709 Grade 50 steel is assigned to preheat Category B for all prequalified processes. AWS D1.1 Table 5.11.")
add("ASTM A992 steel is assigned to preheat Category B for all prequalified processes. AWS D1.1 Table 5.11.")
add("API 5L Grade B steel is assigned to preheat Category B for all prequalified processes. AWS D1.1 Table 5.11.")

# Practical preheat rules
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Clause 5.11 — Practical Preheat Rules")
add("")
add("When the ambient temperature is below 0°C [32°F], the base metal shall be preheated to a minimum of 20°C [70°F] regardless of the normal preheat requirement. AWS D1.1 Clause 5.11.")
add("The preheat and interpass temperature must be maintained throughout the entire welding operation, not just at the start. AWS D1.1 Clause 5.11.")
add("The maximum interpass temperature for most structural steels under AWS D1.1 is 230°C [450°F], unless otherwise specified by the engineer. AWS D1.1 Clause 5.11.")
add("Preheat temperature must be checked at a distance of at least 75 mm [3 in] from the weld joint on each side before welding begins. AWS D1.1 Clause 5.11.")
add("Wind can accelerate heat loss from preheated steel and cause the preheat temperature to drop below the minimum before or during welding. Shelter or continuous monitoring is required in windy conditions. AWS D1.1 Clause 5.11.")

# ── SECTION 7: PJP MINIMUM WELD SIZES ────────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.8 — Minimum PJP Weld Size")
add("")
add("For base metal thickness 1/8 to 3/16 in [3 to 5 mm]: minimum PJP weld size is 1/16 in [2 mm]. AWS D1.1 Table 5.8.")
add("For base metal thickness over 3/16 to 1/4 in [5 to 6 mm]: minimum PJP weld size is 1/8 in [3 mm]. AWS D1.1 Table 5.8.")
add("For base metal thickness over 1/4 to 1/2 in [6 to 12 mm]: minimum PJP weld size is 3/16 in [5 mm]. AWS D1.1 Table 5.8.")
add("For base metal thickness over 1/2 to 3/4 in [12 to 20 mm]: minimum PJP weld size is 1/4 in [6 mm]. AWS D1.1 Table 5.8.")
add("For base metal thickness over 3/4 to 1-1/2 in [20 to 38 mm]: minimum PJP weld size is 5/16 in [8 mm]. AWS D1.1 Table 5.8.")
add("For base metal thickness over 1-1/2 to 2-1/4 in [38 to 57 mm]: minimum PJP weld size is 3/8 in [10 mm]. AWS D1.1 Table 5.8.")
add("For base metal thickness over 2-1/4 to 6 in [57 to 150 mm]: minimum PJP weld size is 1/2 in [12 mm]. AWS D1.1 Table 5.8.")
add("For base metal thickness over 6 in [150 mm]: minimum PJP weld size is 5/8 in [16 mm]. AWS D1.1 Table 5.8.")

# ── SECTION 8: BASE METALS ────────────────────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Table 5.6 — Prequalified Base Metals")
add("")
add("ASTM A36 (thickness up to 3/4 in [20 mm]) is a Group I prequalified base metal with minimum yield strength 36 ksi [250 MPa] and tensile range 58–80 ksi [400–550 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A572 Grade 42 is a Group II prequalified base metal with minimum yield strength 42 ksi [290 MPa] and minimum tensile strength 60 ksi [415 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A572 Grade 50 is a Group II prequalified base metal with minimum yield strength 50 ksi [345 MPa] and minimum tensile strength 65 ksi [450 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A572 Grade 55 is a Group II prequalified base metal with minimum yield strength 55 ksi [380 MPa] and minimum tensile strength 70 ksi [485 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A588 (thickness up to 4 in [100 mm]) is a Group II prequalified base metal with minimum yield strength 50 ksi [345 MPa] and minimum tensile strength 70 ksi [485 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A992 is a Group II prequalified base metal with yield strength range 50–65 ksi [345–450 MPa] and minimum tensile strength 65 ksi [450 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A572 Grade 60 is a Group III prequalified base metal with minimum yield strength 60 ksi [415 MPa] and minimum tensile strength 75 ksi [520 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A572 Grade 65 is a Group III prequalified base metal with minimum yield strength 65 ksi [450 MPa] and minimum tensile strength 80 ksi [550 MPa]. AWS D1.1 Table 5.6.")
add("ASTM A709 Grade HPS70W is a Group IV prequalified base metal with minimum yield strength 70 ksi [485 MPa] and tensile range 85–110 ksi [585–760 MPa]. AWS D1.1 Table 5.6.")
add("API 5L Grade B is a Group I prequalified base metal with minimum yield strength 35 ksi [241 MPa] and minimum tensile strength 60 ksi [414 MPa]. AWS D1.1 Table 5.6.")

# ── SECTION 9: ENVIRONMENTAL CONDITIONS ──────────────────────────────────────
add("")
add("SOURCE: AWS D1.1/D1.1M:2025 Clause 5.12 — Environmental Conditions")
add("")
add("Welding shall not be done when the ambient temperature is below -18°C [0°F], when surfaces are wet, when rain or snow is falling on the weld area, or when wind velocity exceeds 5 mph [8 km/h] — unless the welder and work are protected by a shelter. AWS D1.1 Clause 5.12.")
add("SMAW does not use an external shielding gas. Wind affects SMAW welding primarily by accelerating cooling of the weld and preheat zone, increasing the risk of hydrogen cracking and brittle fracture, not by disrupting shielding gas. AWS D1.1 Clause 5.12.")
add("For GMAW and FCAW, wind can disrupt the shielding gas coverage, causing porosity and lack of fusion. A windscreen must be used when wind velocity exceeds 5 mph [8 km/h]. AWS D1.1 Clause 5.12.")
add("When the base metal temperature is below 0°C [32°F], preheat to at least 20°C [70°F] before welding, even if the standard preheat requirement is lower. AWS D1.1 Clause 5.12.")
add("Low-hydrogen electrodes such as E7018 must be stored in a heated oven at 120–150°C [250–300°F] and issued in small quantities. Exposure to moisture for more than 4 hours requires re-drying. AWS D1.1 Clause 5.12.")
add("In cold weather, low-hydrogen electrodes absorb moisture from the atmosphere much faster than in normal conditions, increasing hydrogen cracking risk. AWS D1.1 Clause 5.12.")

# ── WRITE OUTPUT FILE ─────────────────────────────────────────────────────────
import os
os.makedirs("standards", exist_ok=True)

output_path = "standards/welding_knowledge.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

total = len([l for l in output_lines if l and not l.startswith("SOURCE:")])
print(f"✅ Done — {total} knowledge sentences written to {output_path}")
print(f"   Index this file in the app sidebar alongside your PDFs.")