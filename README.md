# Healthcare Information CrewAI Assistant

## Project Objective

Healthcare Information CrewAI Assistant is a CrewAI-based agentic healthcare information assistant. It answers general healthcare questions using a multi-agent workflow, local tools, fallback handling, optional Langfuse observability, and MCP-aware design.

The project demonstrates how multiple agents can work together to understand a user question, retrieve safe general information, check for red-flag symptoms, and generate a clear final response.

## Important Healthcare Disclaimer

This project provides general health information only.

It does not diagnose medical conditions. It does not prescribe medicine. It does not replace a doctor, pharmacist, emergency service, or qualified healthcare professional.

For serious symptoms such as chest pain, shortness of breath, fainting, confusion, severe headache, weakness on one side, or blue lips, users should seek urgent medical help or contact emergency services.

## Problem Statement

Users may ask basic health questions or describe symptoms, but healthcare-related answers must be structured, cautious, and safe. A single LLM prompt may provide a useful answer, but it can also miss important safety checks or mix different responsibilities together.

This project separates the workflow into multiple CrewAI agents. One agent understands the user question, one retrieves general information from a local knowledge base, one checks safety and red flags, and one writes the final response. This makes the workflow easier to understand, test, monitor, and explain.

## Why Agentic Workflow Is Useful

An agentic workflow is useful because it separates responsibilities instead of asking one model to do everything at once.

- Separate agents handle understanding, information retrieval, safety review, and final writing.
- Tools allow the workflow to use a local healthcare knowledge base instead of relying only on the LLM.
- A dedicated safety review checks for red-flag symptoms.
- Fallback handling gives safe responses when files, topics, tools, or workflows fail.
- Langfuse-style observability makes important workflow events visible.
- The design is easier to test, maintain, and extend.

## Agent Design

| Agent | Role | Goal | Tools Used | Responsibility |
|---|---|---|---|---|
| Patient Question Understanding Agent | Intake and classification agent | Understand the user health question, detect symptoms or topic, and prepare structured information. | SymptomClassifierTool | Reads the question and identifies detected topics, symptoms, and category. |
| Healthcare Information Agent | Healthcare information researcher | Retrieve safe general healthcare information from the local knowledge base. | HealthKnowledgeTool | Looks up relevant information and avoids unsupported medical claims. |
| Safety Review Agent | Medical safety reviewer | Check the user question for red-flag symptoms and unsafe advice. | RedFlagCheckerTool | Detects serious warning signs and recommends professional help when needed. |
| Final Response Writer Agent | Patient-friendly response writer | Write a clear, simple, safe healthcare information response in markdown. | None | Combines previous outputs into a final response with safety notes and disclaimer. |

## Task Workflow

| Step | Task | Agent | Description | Expected Output |
|---|---|---|---|---|
| 1 | Understand and classify question | Patient Question Understanding Agent | Uses the SymptomClassifierTool to identify symptoms, topics, and question category. | Structured summary with original question, detected topics, detected symptoms, and category. |
| 2 | Retrieve general health information | Healthcare Information Agent | Uses the detected topic to search the local healthcare knowledge base. | Relevant general healthcare information from the local JSON file. |
| 3 | Check red flags and safety | Safety Review Agent | Uses the RedFlagCheckerTool to detect serious symptoms and safety concerns. | Red-flag status, warning level, matched red flags, safety message, and recommendation. |
| 4 | Generate final healthcare response | Final Response Writer Agent | Creates the final markdown response using the earlier task outputs. | Markdown response ready to save in `outputs/healthcare_response.md`. |

## Tools

| Tool | Custom Built? | Input | Output | Used By | Purpose |
|---|---|---|---|---|---|
| SymptomClassifierTool | No | User health question text | Detected topics, symptoms, and question category | Patient Question Understanding Agent | Structures the user question before retrieval and safety review. |
| HealthKnowledgeTool | No | Health topic string | Matching topic information from `data/health_knowledge_base.json` | Healthcare Information Agent | Retrieves safe general information from the local knowledge base. |
| RedFlagCheckerTool | Yes | User question or symptom text | Red-flag status, warning level, matched red flags, safety message, and recommendation | Safety Review Agent | Detects urgent warning symptoms and helps prevent unsafe responses. |

## Custom Tool Explanation

`RedFlagCheckerTool` is the custom-built tool for this assignment. It uses keyword-based red-flag matching to detect serious warning symptoms such as chest pain, shortness of breath, difficulty breathing, fainting, weakness on one side, severe headache, confusion, and blue lips.

The tool returns whether a red flag was detected, the warning level, matched red-flag phrases, a safety message, and a recommendation. This helps the workflow avoid unsafe healthcare responses and recommend urgent medical help when serious symptoms are present.

## Fallback Mechanism

The project includes visible fallback handling so the application can fail safely instead of crashing or giving unsafe output.

Fallback examples include:

- Missing knowledge base file: returns a clear missing-file message.
- Topic not found: explains that the topic is not available in the local knowledge base.
- Tool error: returns a structured error dictionary with a recommendation.
- Urgent symptom warning: recommends urgent medical help for serious symptoms.
- CrewAI workflow failure: `app.py` catches the exception, prints a graceful message, and saves an error response to `outputs/healthcare_response.md`.
- Langfuse keys missing: the app prints `Langfuse not configured. Running without remote tracing.` and continues normally.

## Langfuse Observability

`monitoring/langfuse_config.py` provides optional Langfuse-style monitoring support. The project reads Langfuse settings from environment variables only and does not hardcode keys.

Tracked events include:

- Application start
- Sample question loaded
- CrewAI workflow started
- CrewAI workflow completed
- Response saved
- Error or fallback events

If Langfuse keys are missing, the app still runs. This is important for demos because the project remains usable without remote tracing credentials.

## MCP Awareness

This project does not fully implement MCP, but it is MCP-aware.

In a larger version, the local JSON knowledge base could be replaced or extended by MCP servers such as:

- Trusted health knowledge base server
- Hospital FAQ database
- Appointment booking system
- Pharmacy information API
- Red-flag triage service

MCP would help by standardizing how agents connect to external tools and data sources. It would make it easier to replace the local JSON file with a trusted healthcare information service, connect the Healthcare Information Agent to verified medical reference content, and connect the Safety Review Agent to a scalable red-flag triage service.

## Project Structure

```text
healthcare-information-crewai-agent/
├── app.py
├── crew.py
├── agents.py
├── tasks.py
├── tools/
│   ├── symptom_classifier_tool.py
│   ├── health_knowledge_tool.py
│   └── red_flag_checker_tool.py
├── fallback/
│   └── fallback_handler.py
├── monitoring/
│   └── langfuse_config.py
├── data/
│   ├── sample_questions.txt
│   └── health_knowledge_base.json
├── outputs/
│   └── healthcare_response.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

Open PowerShell and run:

```powershell
cd "C:\Personal\Trainings\Agentic AI\Crew AI\healthcare-information-crewai-agent"

py -3.11 -m venv .venv

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel

python -m pip install -r requirements.txt
```

## Environment Variables

Real keys should be placed in a local `.env` file. Do not commit real keys to GitHub.

Use `.env.example` as a template:

```env
OPENAI_API_KEY=your_openai_api_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

Langfuse variables are optional for local testing. The application still runs without them.

## How to Run

```powershell
python app.py
```

The application reads sample question number 2 from `data/sample_questions.txt`, runs the CrewAI workflow, prints the final answer in the terminal, and saves the response to `outputs/healthcare_response.md`.

## Example Input

```text
I have chest pain and shortness of breath. What should I do?
```

## Example Output Summary

The final output includes:

- Question summary
- General healthcare information
- Safety review
- Urgent medical help recommendation when red flags are detected
- Disclaimer that the response is general information only and not a medical diagnosis

## Demo Video Script

Use this short script for a 2-5 minute trainer demo.

1. Show the project folder structure and explain that this is a separate CrewAI healthcare information assistant.
2. Open `agents.py` and explain the four agents: question understanding, healthcare information, safety review, and final response writing.
3. Open the `tools/` folder and explain the three tools. Highlight that `RedFlagCheckerTool` is the custom-built tool.
4. Open `data/health_knowledge_base.json` and show that the app uses a local knowledge base for general information.
5. Open `fallback/fallback_handler.py` and explain how missing files, missing topics, tool errors, and urgent warnings are handled safely.
6. Run the app:

```powershell
python app.py
```

7. Show the selected question in the terminal: `I have chest pain and shortness of breath. What should I do?`
8. Explain that the workflow runs sequentially through all agents and tasks.
9. Show the final terminal output and point out the safety review, urgent recommendation, and disclaimer.
10. Open `outputs/healthcare_response.md` and show that the response was saved.
11. Explain Langfuse observability by showing `monitoring/langfuse_config.py` and the monitoring events in `app.py`.
12. Explain MCP awareness: future versions could connect to trusted healthcare servers, hospital FAQs, appointment systems, pharmacy APIs, or triage services through MCP.

## Assessment Mapping

| Assignment Criteria | How This Project Meets It |
|---|---|
| Use case clarity | The project focuses on a healthcare information assistant for general questions and symptom descriptions. |
| CrewAI agent design | Four agents are defined with clear roles, goals, backstories, and responsibilities. |
| Task workflow | Four tasks are implemented for classification, information retrieval, safety review, and final response generation. |
| Tool integration | The workflow uses three tools connected to CrewAI agents. |
| Custom tool | `RedFlagCheckerTool` is custom-built for red-flag safety detection. |
| Fallback | The project includes fallbacks for missing files, unknown topics, tool errors, urgent symptoms, workflow failure, and missing Langfuse keys. |
| Langfuse monitoring | Optional monitoring hooks track application and workflow events without hardcoded keys. |
| MCP awareness | README explains how MCP could connect agents to trusted healthcare services in a future version. |
| Code quality and reproducibility | The project has a clear folder structure, setup commands, environment template, and runnable entry point. |

## Final Student Note

This project demonstrates a structured, monitorable, and safe agentic AI workflow using CrewAI.
