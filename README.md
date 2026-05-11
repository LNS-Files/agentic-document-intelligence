# 🧬 AI Benefits Architect: Local HIPAA-Compliant Analysis

<p align="center">
  <img src="output_demo.png" alt="Benefits AI Demo" width="700">
  <br>
  <em>Figure 1: Local Llama 3 extracting healthcare data and providing expert reasoning.</em>
</p>


An end-to-end **Agentic AI Pipeline** designed to transform unstructured healthcare Summary of Benefits (SBC) PDFs into structured, actionable insights. 

### 🌟 Project Highlights
- **Privacy-First (HIPAA Ready):** Built with a local-only architecture using **Ollama (Llama 3)**. Sensitive insurance data never leaves the local machine, eliminating cloud-based PHI (Protected Health Information) risks.
- **Agentic Reasoning:** Beyond simple extraction, this system features a **Counselor Agent** that cross-references extracted data against specific user medical scenarios to provide tailored recommendations.
- **Strict Schema Enforcement:** Uses **Pydantic** models to ensure 100% data integrity when transforming messy PDF tables into JSON.

### 🛠️ Tech Stack
*   **Orchestration:** [LangChain](https://langchain.com)
*   **Intelligence:** [Ollama](https://ollama.com) (Llama 3:8b-instruct-q4_K_M)
*   **PDF Engine:** [PyMuPDF (fitz)](https://readthedocs.io)
*   **Validation:** [Pydantic v2](https://pydantic.dev)

### 🚀 Key Features
- **Intelligent Extraction:** Automatically identifies Deductibles, Out-of-Pocket Maximums, and Copays from standardized SBC documents.
- **Scenario-Based Counseling:** Analyzes plan suitability for specific profiles (e.g., "Frequent doctor visits" vs. "High-deductible seeker").
- **Local Performance Optimization:** Configured with specific context window (`num_ctx`) and threading adjustments to run efficiently on standard CPU hardware.

### 📁 Repository Structure
*   `main.py`: The system entry point and master orchestrator.
*   `extractor.py`: Handles PDF parsing and LLM-based data structuring.
*   `counselor.py`: Contains the logic for the expert reasoning agent.
*   `schema.py`: Defines the validated data models for benefits.
*   `data/`: Directory for input healthcare PDFs (ignored by Git for privacy).

### 🔧 Installation & Setup
1. **Clone the repo:** `git clone https://github.com`
2. **Install dependencies:** `pip install -r requirements.txt` (or install manually)
3. **Pull the model:** `ollama pull llama3:8b-instruct-q4_K_M`
4. **Run:** `python main.py`

---


---