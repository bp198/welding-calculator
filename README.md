# 🔩 Welding Engineering Toolbox

A professional welding engineering reference and calculation platform built with Streamlit.  
Covers AWS D1.1/D1.1M:2025 prequalified WPS requirements, EN 1011 heat input calculations, and AI-assisted welding procedure interpretation.

**Live app:** [welding-calculator on Streamlit Cloud](https://welding-calculator-xpnd6lnbgaxjon5zk5ou6a.streamlit.app/)

---

## Features

### 🔥 Heat Input Calculator (EN 1011)
- Calculates welding heat input per EN 1011 standard
- Supports SMAW, MIG/MAG, TIG, SAW, and FCAW processes
- Interactive charts and process comparison

### 📋 AWS D1.1 WPS Reference
Interactive reference for AWS D1.1/D1.1M:2025 Clause 5 — Prequalified WPS Requirements:

| Tab | Content |
|-----|---------|
| ⚡ SMAW (5.1) | Electrode limits, bead thickness, fillet size |
| 🔩 SAW (5.2) | Current limits, electrode diameter, layer width |
| 🌀 GMAW (5.3) | Wire diameter, minimum current, bead limits |
| 🔥 FCAW (5.4) | Electrode diameter by position and thickness |
| 🌡️ Preheat (5.11) | Minimum preheat and interpass temperatures |
| 📐 PJP Min Size (5.8) | Minimum partial joint penetration weld sizes |
| 🏗️ Base Metals (5.6) | Prequalified base metal groups and properties |
| 🔧 Filler Metals (5.7) | Matching filler metal classifications |
| 🤖 AI Assistant | RAG-powered welding engineering assistant |
| 📄 WPS Generator | Generate PDF and Word WPS documents |

### 🤖 AI Welding Assistant (RAG-powered)
- Powered by LLaMA 3.3 70b via Groq API
- Retrieval-Augmented Generation (RAG) over indexed welding standards
- Full conversation memory — ask follow-up questions naturally
- Expert IWE-level system prompt with 9 engineering behaviour rules
- Grounded answers with clause citations — not generic responses
- Covers: electrode limits, preheat, environmental risks, go/no-go recommendations

### 📄 WPS Generator
- Generate complete Welding Procedure Specifications
- Export to PDF (ReportLab) and Word (.docx)
- AWS D1.1 Form J-2 compliant format

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Charts | Plotly |
| Data | Pandas |
| AI Model | LLaMA 3.3 70b (Groq API) |
| RAG Engine | ChromaDB + sentence-transformers |
| PDF extraction | PyMuPDF |
| PDF generation | ReportLab |
| Word generation | python-docx |
| Embeddings | all-MiniLM-L6-v2 |

---

## Project Structure

```
welding-calculator/
├── Home.py                    # Landing page
├── rag_engine.py              # RAG engine — PDF indexing and clause retrieval
├── generate_knowledge.py      # Converts table data to natural language for RAG
├── pages/
│   ├── 1_Heat_Input.py        # EN 1011 heat input calculator
│   └── 2_AWS_D1_WPS.py        # AWS D1.1 reference + AI assistant + WPS generator
├── images/
│   └── figure_5_1.png         # AWS D1.1 Figure 5.1 joint illustration
├── requirements.txt
└── .gitignore
```

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/bp198/welding-calculator.git
cd welding-calculator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
Get a free API key at [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run Home.py
```

---

## RAG Setup (optional — local only)

The AI assistant works without RAG using hardcoded table data. For full clause-level retrieval:

### 1. Install RAG dependencies
```bash
pip install pymupdf chromadb sentence-transformers
```

### 2. Add your standard PDFs
Create a `standards/` folder (gitignored — never committed) and add your PDFs:
```
standards/
├── AWS_D1_1_2025.pdf
├── EN_ISO_15614-1.pdf
├── EN-1011-2.pdf
└── ...
```

### 3. Generate the knowledge base
```bash
python generate_knowledge.py
```
This creates `standards/welding_knowledge.txt` — 107 structured facts from AWS D1.1 Clause 5.

### 4. Index in the app
Run the app → sidebar → upload PDFs + `welding_knowledge.txt` → click "Index uploaded PDFs"

> **Legal note:** Standard PDFs are copyrighted. The `standards/` and `chroma_db/` folders are gitignored and must never be committed or deployed publicly.

---

## Standards Covered

| Standard | Coverage |
|----------|---------|
| AWS D1.1/D1.1M:2025 | Structural Welding — Steel (full Clause 5) |
| AWS D1.1/D1.1M:2020 | Previous edition for reference |
| EN ISO 15614-1:2017 | Welding procedure qualification |
| BS EN 1011-1:2009 | Welding recommendations — Part 1 |
| BS EN 1011-2 | Arc welding of ferritic steels |
| BS EN 1011-3:2018 | Arc welding of stainless steels |
| BS EN 1011-6:2018 | Laser beam welding |

---

## About

Built by **Babak Pirzadi** — Welding Engineer & Master's student in Engineering Technology for Strategy and Security, University of Genova, Italy.

---

## Disclaimer

This tool is for engineering reference only. Always verify all requirements against the current official edition of the relevant standard before production welding. The author accepts no liability for decisions made based on this tool.# welding-calculator
