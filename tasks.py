"""CrewAI task definitions for the healthcare information assistant.

Step 3 adds task definitions only. The full CrewAI execution will be connected
in a later step.
"""

from crewai import Task


def create_tasks(question_agent, information_agent, safety_agent, writer_agent, user_question):
    """Create and return the four tasks for the healthcare workflow.

    The tasks are ordered so each agent can build on earlier work:
    1. Understand the question.
    2. Retrieve general information.
    3. Review safety and red flags.
    4. Write the final markdown response.
    """
    question_task = Task(
        description=(
            "Read the user's health question below. Use the Symptom Classifier Tool "
            "to identify symptoms, topics, and question category.\n\n"
            f"User health question: {user_question}"
        ),
        expected_output=(
            "A structured summary containing:\n"
            "- original question\n"
            "- detected topics\n"
            "- detected symptoms\n"
            "- question category"
        ),
        agent=question_agent,
    )

    information_task = Task(
        description=(
            "Use the detected topic from the previous task and retrieve general "
            "information from the local health knowledge base using the Health "
            "Knowledge Tool. If there are multiple detected topics, choose the most "
            "important topic for the user's question. If no topic is available, "
            "explain that the topic is not found in the local knowledge base."
        ),
        expected_output="Relevant general healthcare information from the local knowledge base.",
        agent=information_agent,
        context=[question_task],
    )

    safety_task = Task(
        description=(
            "Check the original user question for red-flag symptoms using the Red "
            "Flag Checker Tool. If serious symptoms are found, clearly recommend "
            "urgent medical help.\n\n"
            f"Original user health question: {user_question}"
        ),
        expected_output=(
            "Safety review containing:\n"
            "- red flag detected true or false\n"
            "- warning level\n"
            "- matched red flags\n"
            "- safety message\n"
            "- recommendation"
        ),
        agent=safety_agent,
        context=[question_task],
    )

    final_response_task = Task(
        description=(
            "Create a final markdown healthcare response using the outputs from the "
            "previous tasks. The response must include:\n"
            "- User question summary\n"
            "- General healthcare information\n"
            "- Safety review\n"
            "- Recommended next steps\n"
            "- Clear disclaimer: This is general information only and not a medical diagnosis."
        ),
        expected_output="A complete markdown response ready to save in outputs/healthcare_response.md.",
        agent=writer_agent,
        context=[question_task, information_task, safety_task],
    )

    return question_task, information_task, safety_task, final_response_task
