"""Main application entry point for the healthcare CrewAI assistant.

Step 6 adds optional Langfuse-style monitoring events. The healthcare workflow
still runs even when Langfuse keys are not configured.
"""

import os

from dotenv import load_dotenv

from crew import run_healthcare_crew
from monitoring.langfuse_config import log_event


load_dotenv()


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SAMPLE_QUESTIONS_PATH = os.path.join(PROJECT_ROOT, "data", "sample_questions.txt")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "outputs", "healthcare_response.md")


def read_sample_question(file_path: str, question_number: int = 1):
    """Read one question from the sample questions file.

    The sample file uses numbered lines like "1. Question text". This function
    removes the number and returns only the question text.
    """
    fallback_question = "What is high blood pressure?"

    if not os.path.exists(file_path):
        return fallback_question

    with open(file_path, "r", encoding="utf-8-sig") as file:
        questions = [line.strip() for line in file.readlines() if line.strip()]

    if not questions:
        return fallback_question

    if question_number < 1 or question_number > len(questions):
        question_number = 1

    selected_question = questions[question_number - 1]

    # Remove the leading number from lines like "2. I have chest pain...".
    if ". " in selected_question:
        selected_question = selected_question.split(". ", 1)[1]

    return selected_question


def save_response_to_file(response: str, output_path: str):
    """Save the final response to a markdown file using UTF-8 encoding."""
    output_folder = os.path.dirname(output_path)
    os.makedirs(output_folder, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(str(response))


if __name__ == "__main__":
    print("Healthcare Information CrewAI Assistant")
    print("This tool provides general health information only. It does not diagnose or replace a doctor.")
    print()

    log_event("application_start", {"app_name": "healthcare-information-crewai-agent"})

    user_question = read_sample_question(SAMPLE_QUESTIONS_PATH, question_number=2)
    log_event("sample_question_loaded", {"question": user_question, "question_number": 2})

    print(f"Selected question: {user_question}")
    print()

    try:
        log_event("crewai_workflow_started", {"question": user_question})
        final_response = run_healthcare_crew(user_question)
        final_response_text = str(final_response)
        log_event("crewai_workflow_completed", {"response_length": len(final_response_text)})

        print("Final healthcare response:")
        print(final_response_text)

        save_response_to_file(final_response_text, OUTPUT_PATH)
        log_event("response_saved_to_file", {"output_path": OUTPUT_PATH})

        print()
        print(f"Response saved to: {OUTPUT_PATH}")
    except Exception as error:
        log_event("workflow_error_or_fallback", {"error": str(error)})

        error_response = (
            "# Healthcare Response\n\n"
            "The CrewAI workflow could not complete successfully.\n\n"
            f"Error message: {error}\n\n"
            "This tool provides general health information only and is not a medical diagnosis. "
            "Please consult a qualified healthcare professional for personal medical advice."
        )

        print("The application could not complete the CrewAI workflow.")
        print(f"Error message: {error}")

        save_response_to_file(error_response, OUTPUT_PATH)
        log_event("error_response_saved_to_file", {"output_path": OUTPUT_PATH})
        print(f"Error response saved to: {OUTPUT_PATH}")

