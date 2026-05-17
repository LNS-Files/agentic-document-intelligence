import io
import json
import os
import tempfile

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from counselor import compare_plans
from extractor import extract_text_from_pdf, parse_benefits

load_dotenv()

st.set_page_config(
    page_title="Agentic Document Intelligence",
    page_icon="🏥",
    layout="wide",
)

st.title("Agentic Document Intelligence")
st.caption("Privacy-first benefits analysis — your data never leaves this device")

# --- Sidebar ---
with st.sidebar:
    st.header("Your Profile")
    user_scenario = st.text_area(
        "Describe your health situation",
        value="I have a chronic condition, visit my doctor monthly, and want low copays.",
        height=120,
    )
    st.divider()
    st.info("All analysis runs locally via Ollama. No data is sent to any cloud service.")

# --- File Upload ---
uploaded_files = st.file_uploader(
    "Upload one or more SBC PDF files",
    type=["pdf"],
    accept_multiple_files=True,
)

if uploaded_files:
    if st.button("Analyze Plans", type="primary", use_container_width=True):
        plans = []
        errors = []
        total = len(uploaded_files)
        progress = st.progress(0, text="Starting...")

        for i, uploaded_file in enumerate(uploaded_files):
            progress.progress(i / total, text=f"Processing {uploaded_file.name}...")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                pdf_text = extract_text_from_pdf(tmp_path)
                plan = parse_benefits(pdf_text)
                plans.append(plan)
            except Exception as e:
                errors.append(f"{uploaded_file.name}: {e}")
            finally:
                os.unlink(tmp_path)

        progress.progress(1.0, text="Extraction complete.")

        for err in errors:
            st.error(err)

        if plans:
            with st.spinner("Generating counselor recommendation..."):
                recommendation = compare_plans(
                    [p.model_dump() for p in plans], user_scenario
                )
            st.session_state["plans"] = plans
            st.session_state["recommendation"] = recommendation
            st.session_state["user_scenario"] = user_scenario

# --- Results (persisted via session_state) ---
if "plans" in st.session_state:
    plans = st.session_state["plans"]
    recommendation = st.session_state["recommendation"]

    st.divider()

    # Plan comparison table
    st.subheader("Extracted Plan Data")
    df = pd.DataFrame([p.model_dump() for p in plans])
    df.columns = [c.replace("_", " ").title() for c in df.columns]
    st.dataframe(df, use_container_width=True)

    # Counselor recommendation
    st.subheader("Counselor Recommendation")
    st.markdown(f"**Client Profile:** {st.session_state['user_scenario']}")
    st.info(recommendation)

    # Export
    st.subheader("Export Results")
    col1, col2 = st.columns(2)
    plans_data = [p.model_dump() for p in plans]

    with col1:
        st.download_button(
            label="Download JSON",
            data=json.dumps(plans_data, indent=2),
            file_name="benefits_analysis.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buf.getvalue(),
            file_name="benefits_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )
