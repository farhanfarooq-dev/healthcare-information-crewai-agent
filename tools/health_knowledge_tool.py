"""Health Knowledge Tool.

This tool reads safe, general healthcare information from the local JSON file.
It does not diagnose, prescribe medicine, or replace professional medical care.
"""

import json
from pathlib import Path
import sys

# This makes the fallback folder importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from fallback.fallback_handler import handle_missing_file, handle_missing_topic, handle_tool_error


class HealthKnowledgeTool:
    """Look up a supported health topic in the local knowledge base."""

    name = "Health Knowledge Tool"
    description = "Retrieves general health information from a local JSON knowledge base."

    def __init__(self, knowledge_base_path=None):
        self.knowledge_base_path = Path(knowledge_base_path) if knowledge_base_path else PROJECT_ROOT / "data" / "health_knowledge_base.json"

    def run(self, topic):
        """Return matching knowledge base content or a fallback dictionary."""
        topic_text = str(topic or "").strip().lower()

        try:
            if not self.knowledge_base_path.exists():
                return handle_missing_file(str(self.knowledge_base_path))

            with self.knowledge_base_path.open("r", encoding="utf-8-sig") as file:
                knowledge_base = json.load(file)

            for item in knowledge_base.get("topics", []):
                if item.get("topic", "").lower() == topic_text:
                    return {
                        "status": "success",
                        "data": item,
                    }

            return handle_missing_topic(topic_text)
        except Exception as error:
            return handle_tool_error(self.name, str(error))


if __name__ == "__main__":
    tool = HealthKnowledgeTool()
    sample_topic = "headache"
    print(tool.run(sample_topic))

