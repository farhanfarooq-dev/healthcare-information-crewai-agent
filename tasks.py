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
            "Knowledge Tool. You must call the Health Knowledge Tool once before "
            "writing your answer. If there are multiple detected topics, choose the "
            "most important topic for the user's question. If no topic was detected, "
            "infer a short topic from the original user question and call the Health "
            "Knowledge Tool with that topic. Start your answer with either "
            "'Local knowledge status: found' or 'Local knowledge status: not_found'. "
            "If the local knowledge base does not contain the topic, include this "
            "exact sentence: Local reference content was not available for this topic. "
            "Then provide safe general information using the LLM. If the user asks "
            "about medicine, dosage, or treatment, do not provide exact medicine "
            "names, dosage, or prescription advice. Give general medication safety "
            "guidance and recommend asking a doctor or pharmacist."
        ),
        expected_output="Relevant general healthcare information from the local knowledge base, or safe general LLM information when local reference content is not available.",
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
            "- Medication safety note when the user asks about medicine, dosage, or treatment\n"
            "- If the Healthcare Information Agent says Local knowledge status: not_found, include this exact sentence: Local reference content was not available for this topic.\n"
            "- If the Healthcare Information Agent says Local knowledge status: found, do not say local reference content was unavailable\n"
            "- Medication safety note when the user asks about medicine, dosage, or treatment. Do not mention specific medicine names, dosages, or prescriptions.\n"
            "- Clear disclaimer using this exact sentence: This is general information only and not a medical diagnosis."
        ),
        expected_output="A complete markdown response ready to save in outputs/healthcare_response.md.",
        agent=writer_agent,
        context=[question_task, information_task, safety_task],
    )

    return question_task, information_task, safety_task, final_response_task



