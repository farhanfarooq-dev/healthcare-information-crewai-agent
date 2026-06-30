"""CrewAI agent definitions for the healthcare information assistant.

Step 3 adds the agents only. The full app execution will be connected later in
app.py and crew.py.
"""

from crewai import Agent
from crewai.tools import BaseTool

from tools.symptom_classifier_tool import SymptomClassifierTool
from tools.health_knowledge_tool import HealthKnowledgeTool
from tools.red_flag_checker_tool import RedFlagCheckerTool


class SymptomClassifierCrewTool(BaseTool):
    """CrewAI-compatible wrapper around our standalone SymptomClassifierTool."""

    name: str = "Symptom Classifier Tool"
    description: str = "Detects health topics, symptoms, and question category from a user question."

    def _run(self, question: str):
        """CrewAI calls _run when an agent uses this tool."""
        return SymptomClassifierTool().run(question)


class HealthKnowledgeCrewTool(BaseTool):
    """CrewAI-compatible wrapper around our standalone HealthKnowledgeTool."""

    name: str = "Health Knowledge Tool"
    description: str = "Retrieves safe general healthcare information from the local JSON knowledge base."

    def _run(self, topic: str):
        """CrewAI calls _run when an agent uses this tool."""
        return HealthKnowledgeTool().run(topic)


class RedFlagCheckerCrewTool(BaseTool):
    """CrewAI-compatible wrapper around our custom RedFlagCheckerTool."""

    name: str = "Red Flag Checker Tool"
    description: str = "Checks a health question for serious red-flag symptoms and safety recommendations."

    def _run(self, symptom_text: str):
        """CrewAI calls _run when an agent uses this tool."""
        return RedFlagCheckerTool().run(symptom_text)


def create_agents():
    """Create and return the four CrewAI agents used in this project.

    Each agent has one clear responsibility. This makes the workflow easier to
    understand during the demo and safer than asking one agent to do everything.
    """
    symptom_classifier_tool = SymptomClassifierCrewTool()
    health_knowledge_tool = HealthKnowledgeCrewTool()
    red_flag_checker_tool = RedFlagCheckerCrewTool()

    question_agent = Agent(
        role="Patient Question Understanding Agent",
        goal="Understand the user health question, detect symptoms or topic, and prepare structured information for the next agent.",
        backstory=(
            "You are a careful healthcare intake assistant. You organize user "
            "questions clearly and avoid making medical diagnoses."
        ),
        tools=[symptom_classifier_tool],
        verbose=True,
        allow_delegation=False,
    )

    information_agent = Agent(
        role="Healthcare Information Agent",
        goal="Retrieve safe general healthcare information from the local knowledge base.",
        backstory=(
            "You are a healthcare information researcher. You use available "
            "reference content and avoid unsupported medical claims."
        ),
        tools=[health_knowledge_tool],
        verbose=True,
        allow_delegation=False,
    )

    safety_agent = Agent(
        role="Safety Review Agent",
        goal="Check the user question for red-flag symptoms and unsafe advice.",
        backstory=(
            "You are a medical safety reviewer. You do not diagnose. You identify "
            "serious warning signs and recommend professional help when needed."
        ),
        tools=[red_flag_checker_tool],
        verbose=True,
        allow_delegation=False,
    )

    writer_agent = Agent(
        role="Final Response Writer Agent",
        goal="Write a clear, simple, safe healthcare information response in markdown.",
        backstory=(
            "You are a patient-friendly healthcare writer. You explain information "
            "clearly and always include a safety disclaimer."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    return question_agent, information_agent, safety_agent, writer_agent
