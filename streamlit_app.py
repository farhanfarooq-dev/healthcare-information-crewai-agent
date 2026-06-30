"""Simple Streamlit web UI for the healthcare CrewAI assistant.

This file does not change the CrewAI workflow. It only provides a browser-based
form where a user can type a health question and view the final response.
"""

from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Healthcare Information CrewAI Assistant",
    layout="wide",
)

from dotenv import load_dotenv

from crew import run_healthcare_crew


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "healthcare_response.md"


MODE_DETAILS = {
    "Knowledge Base Demo Mode": {
        "default_question": "I have chest pain and shortness of breath. What should I do?",
        "helper_text": (
            "This mode demonstrates the assignment workflow using the local "
            "knowledge base, tools, fallback, and safety review."
        ),
    },
    "Open Health Question Mode": {
        "default_question": "What is diabetes?",
        "helper_text": (
            "This mode allows open general health questions. If local reference "
            "content is not available, the assistant gives safe general information "
            "using the LLM."
        ),
    },
}

EXAMPLE_QUESTIONS = [
    "What is diabetes?",
    "What should I know about stomach pain?",
    "Why do I feel tired all the time?",
    "Can I take medicine for fever?",
    "I have chest pain and shortness of breath. What should I do?",
]


def save_response_to_file(response: str, output_path: Path):
    """Save the assistant response so the demo output is available after a run."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(str(response), encoding="utf-8")


st.sidebar.header("Example Questions")
for example_question in EXAMPLE_QUESTIONS:
    st.sidebar.markdown(f"- {example_question}")

left, main, right = st.columns([1, 4, 1])

with main:
    st.title("Healthcare Information CrewAI Assistant")

    st.warning(
        "This tool provides general health information only. It does not diagnose, "
        "prescribe medicine, or replace a doctor or emergency service. For serious "
        "symptoms such as chest pain, shortness of breath, fainting, confusion, or "
        "severe symptoms, seek urgent medical help."
    )

    selected_mode = st.radio(
        "Choose assistant mode",
        options=["Knowledge Base Demo Mode", "Open Health Question Mode"],
        index=0,
    )

    mode_info = MODE_DETAILS[selected_mode]
    st.caption(mode_info["helper_text"])

    user_question = st.text_area(
        "Enter your healthcare-related question",
        value=mode_info["default_question"],
        height=180,
    )

    st.caption(
        "You can ask any general health question. This tool gives general "
        "information only and does not diagnose or prescribe medicine."
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
