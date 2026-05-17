# Agentic Document Intelligence

An end-to-end **Agentic AI Pipeline** that transforms unstructured healthcare Summary of Benefits (SBC) PDFs into structured, actionable insights — with a privacy-first, fully local architecture.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![LangChain](https://img.shields.io/badge/LangChain-Ollama-green) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![Pydantic](https://img.shields.io/badge/Validation-Pydantic_v2-purple)

---

## Project Highlights

- **Privacy-First (HIPAA-Ready):** Built on a local-only architecture using **Ollama (Llama 3)**. Sensitive insurance data never leaves the machine — zero cloud exposure of PHI (Protected Health Information).
- **Agentic Reasoning:** A dedicated **Counselor Agent** cross-references extracted plan data against the user's specific medical scenario to deliver a personalized recommendation — not just raw extraction.
- **Robust JSON Parsing:** Custom fallback parser handles LLM output variance (prose, markdown fences, partial JSON) so the pipeline never silently fails.
- **Strict Schema Enforcement:** Pydantic v2 models guarantee data integrity when converting messy PDF tables into structured JSON.
- **Streamlit Web UI:** Upload PDFs, get a comparison table, and download results as JSON or CSV — no terminal required.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Runtime | [Ollama](https://ollama.com) — Llama 3 8B (local, CPU-friendly) |
| Orchestration | [LangChain](https://langchain.com) |
| PDF Parsing | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io) |
| Data Validation | [Pydantic v2](https://pydantic.dev) |
| Web UI | [Streamlit](https://streamlit.io) |
| Data Export | Pandas, JSON, CSV |

---

## Features

- **Multi-PDF Support:** Upload and compare multiple insurance plans simultaneously.
- **Intelligent Extraction:** Automatically identifies Deductibles, Out-of-Pocket Maximums, ER costs, Primary Care copays, Specialist copays, and Prescription tiers.
- **Scenario-Based Counseling:** Analyzes plan suitability for a specific profile (e.g., "I have a chronic condition and visit my doctor monthly").
- **Export Results:** Download the structured comparison as JSON or CSV directly from the UI.
- **CLI Mode:** Run headless via `python main.py` — auto-discovers all PDFs in the `data/` folder.

---

## Repository Structure

```
agentic-document-intelligence/
├── app.py              # Streamlit web UI
├── main.py             # CLI entry point — orchestrates the full pipeline
├── extractor.py        # PDF parsing + LLM-based structured extraction
├── counselor.py        # Counselor agent — personalized plan recommendation
├── schema.py           # Pydantic data models for benefits validation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── data/               # Place input PDFs here (gitignored for privacy)
```

---

## Setup & Usage

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally

### 1. Clone the repo
```bash
git clone https://github.com/LNS-Files/agentic-document-intelligence.git
cd agentic-document-intelligence
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Pull the model
```bash
ollama pull llama3:8b-instruct-q4_K_M
```

### 4. Configure environment (optional)
```bash
cp .env.example .env
# Edit .env to set your USER_SCENARIO
```

### 5. Run

**Web UI (recommended):**
```bash
streamlit run app.py
```

**CLI (headless):**
```bash
# Place PDFs in data/ and run:
python main.py

# Or pass files directly:
python main.py plan_a.pdf plan_b.pdf
```

---

## How It Works

```
PDF(s) → extract_text_from_pdf() → parse_benefits() [LLM + Pydantic] → BenefitPlan objects
                                                                              ↓
                                                               compare_plans() [Counselor LLM]
                                                                              ↓
                                                              Recommendation + JSON/CSV export
```

1. **Extraction:** PyMuPDF reads the first 3 pages of each SBC PDF and passes the text to a local Llama 3 model with a strict JSON prompt.
2. **Validation:** The LLM response is parsed by a robust fallback parser and validated against the `BenefitPlan` Pydantic schema.
3. **Counseling:** All extracted plans are passed to the Counselor Agent along with the user's health profile. The agent returns a structured recommendation with specific cost comparisons.
4. **Export:** Results are available as JSON and CSV.

---

## Privacy & Security

All processing runs **entirely on-device** via Ollama. No PDF content, extracted data, or user health information is sent to any external API or cloud service. The `data/` directory and all `.pdf` files are excluded from version control via `.gitignore`.
