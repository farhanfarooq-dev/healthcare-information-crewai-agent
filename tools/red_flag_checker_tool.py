"""Red Flag Checker Tool.

This is the custom-built tool for the assignment. It uses simple keyword matching
to detect serious symptoms and return a cautious safety recommendation.
"""


class RedFlagCheckerTool:
    """Check text for serious red-flag symptoms."""

    name = "Red Flag Checker Tool"
    description = "Detects possible urgent symptoms and returns a safety warning."

    def run(self, symptom_text):
        """Return red-flag status, warning level, matched phrases, and advice."""
        text = str(symptom_text or "")
        lower_text = text.lower()

        # These phrases are intentionally simple for a beginner-friendly demo.
        red_flag_keywords = [
            "chest pain",
            "shortness of breath",
            "severe chest pain",
            "difficulty breathing",
            "fainting",
            "weakness on one side",
            "severe headache",
            "confusion",
            "blue lips",
        ]

        matched_red_flags = [keyword for keyword in red_flag_keywords if keyword in lower_text]

        if matched_red_flags:
            return {
                "red_flag_detected": True,
                "warning_level": "high",
                "matched_red_flags": matched_red_flags,
                "safety_message": "One or more serious symptoms were detected. This tool cannot diagnose the cause, but these symptoms may require urgent attention.",
                "recommendation": "Please seek urgent medical help or contact emergency services if symptoms are severe or sudden.",
            }

        return {
            "red_flag_detected": False,
            "warning_level": "low",
            "matched_red_flags": [],
            "safety_message": "No serious red-flag keywords were detected by this simple tool.",
            "recommendation": "Monitor symptoms and consult a healthcare professional if symptoms continue or get worse.",
        }


if __name__ == "__main__":
    tool = RedFlagCheckerTool()
    sample_text = "I have chest pain and shortness of breath. What should I do?"
    print(tool.run(sample_text))
