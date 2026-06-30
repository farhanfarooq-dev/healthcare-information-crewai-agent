"""CrewAI crew assembly module.

Step 4 connects the agents and tasks into one sequential CrewAI workflow. The
main app entry point and file saving will be added later in app.py.
"""

from crewai import Crew, Process

from agents import create_agents
from tasks import create_tasks


def create_healthcare_crew(user_question: str):
    """Create the CrewAI healthcare workflow for one user question.

    A Crew is the object that holds the agents, tasks, and execution process.
    Here we keep the process sequential so the output of earlier tasks can guide
    the later safety review and final response.
    """
    question_agent, information_agent, safety_agent, writer_agent = create_agents()

    question_task, information_task, safety_task, final_response_task = create_tasks(
        question_agent=question_agent,
        information_agent=information_agent,
        safety_agent=safety_agent,
        writer_agent=writer_agent,
        user_question=user_question,
    )

    crew = Crew(
        agents=[
            question_agent,
            information_agent,
            safety_agent,
            writer_agent,
        ],
        tasks=[
            question_task,
            information_task,
            safety_task,
            final_response_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def run_healthcare_crew(user_question: str):
    """Run the healthcare CrewAI workflow and return the final result."""
    crew = create_healthcare_crew(user_question)
    result = crew.kickoff()
    return result


if __name__ == "__main__":
    sample_question = "I have chest pain and shortness of breath. What should I do?"
    result = run_healthcare_crew(sample_question)
    print(result)
