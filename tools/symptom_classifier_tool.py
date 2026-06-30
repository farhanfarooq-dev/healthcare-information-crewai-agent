"""Symptom Classifier Tool.

This beginner-friendly tool uses simple keyword matching to organize a user's
health question before the CrewAI agents are added in a later step.
"""


class SymptomClassifierTool:
    """Classify a health question into topics, symptoms, and a question category."""

    name = "Symptom Classifier Tool"
    description = "Detects basic health topics and symptoms from a user question."

    def run(self, question):
        """Return a structured dictionary for the user's question."""
        question_text = str(question or "")
        lower_question = question_text.lower()

        detected_topics = []
        detected_symptoms = []

        # Each keyword list maps everyday words to one supported knowledge topic.
        topic_keywords = {
            "headache": ["headache", "head pain"],
            "fever": ["fever", "temperature"],
            "high blood pressure": ["high blood pressure", "blood pressure", "bp"],
            "dehydration": ["thirsty", "dehydration", "dehydrated", "water", "hydration"],
            "cough": ["cough", "coughing"],
            "chest pain": ["chest pain", "severe chest pain"],
            "diabetes": ["diabetes", "blood sugar", "glucose"],
            "stomach pain": ["stomach pain", "abdominal pain", "belly pain"],
            "medication safety": ["medicine", "medication", "dosage", "dose", "treatment"],
        }

        symptom_keywords = {
            "headache": ["headache", "head pain"],
            "fever": ["fever", "temperature"],
            "breathing difficulty": ["shortness of breath", "difficulty breathing"],
            "dizziness": ["dizzy", "dizziness"],
            "cough": ["cough", "coughing"],
            "chest pain": ["chest pain", "severe chest pain"],
            "thirst": ["thirsty", "dehydrated", "dehydration"],
            "stomach pain": ["stomach pain", "abdominal pain", "belly pain"],
            "medication question": ["medicine", "medication", "dosage", "dose", "treatment"],
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in lower_question for keyword in keywords):
                detected_topics.append(topic)

        for symptom, keywords in symptom_keywords.items():
            if any(keyword in lower_question for keyword in keywords):
                detected_symptoms.append(symptom)

        urgent_keywords = [
            "chest pain",
            "shortness of breath",
            "severe chest pain",
            "difficulty breathing",
            "dizzy",
            "dizziness",
        ]

        if any(keyword in lower_question for keyword in urgent_keywords):
            question_category = "urgent_symptom_question"
        elif "water" in lower_question or "hydration" in lower_question or "dehydration" in lower_question:
            question_category = "hydration_advice"
        elif detected_symptoms:
            question_category = "symptom_information"
        elif "what is" in lower_question or "explain" in lower_question:
            question_category = "health_topic_explanation"
        else:
            question_category = "unknown"

        return {
            "original_question": question_text,
            "detected_topics": detected_topics,
            "detected_symptoms": detected_symptoms,
            "question_category": question_category,
        }


if __name__ == "__main__":
    tool = SymptomClassifierTool()
    sample_question = "I have a headache and mild fever. What general information should I know?"
    print(tool.run(sample_question))

