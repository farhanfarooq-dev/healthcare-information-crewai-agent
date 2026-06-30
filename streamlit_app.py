"""Simple Streamlit web UI for the healthcare CrewAI assistant.

This file does not change the CrewAI workflow. It only provides a browser-based
form where a user can type a health question and view the final response.
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from crew import run_healthcare_crew


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "healthcare_response.md"


def save_response_to_file(response: str, output_path: Path):
    """Save the assistant response so the demo output is available after a run."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(str(response), encoding="utf-8")


st.set_page_config(
    page_title="Healthcare Information CrewAI Assistant",
    page_icon="healthcare",
    layout="centered",
)

st.title("Healthcare Information CrewAI Assistant")

st.warning(
    "This tool provides general health information only. It does not diagnose, "
    "prescribe medicine, or replace a doctor or emergency service. For serious "
    "symptoms such as chest pain, shortness of breath, fainting, confusion, or "
    "severe symptoms, seek urgent medical help."
)

user_question = st.text_area(
    "Enter your healthcare-related question",
    value="I have chest pain and shortness of breath. What should I do?",
    height=140,
)

if st.button("Run Healthcare Assistant", type="primary"):
    cleaned_question = user_question.strip()

    if not cleaned_question:
        st.warning("Please enter a healthcare-related question before running the assistant.")
    else:
        try:
            with st.spinner("Running the CrewAI healthcare workflow..."):
                result = run_healthcare_crew(cleaned_question)
                final_response = str(result)
                save_response_to_file(final_response, OUTPUT_PATH)

            st.success("Healthcare response generated successfully.")
            st.markdown(final_response)
            st.caption(f"Response saved to: {OUTPUT_PATH}")
        except Exception as error:
            st.error("The healthcare assistant could not complete the workflow.")
            st.write("Please check your environment variables, dependencies, and terminal logs.")
            st.code(str(error))
