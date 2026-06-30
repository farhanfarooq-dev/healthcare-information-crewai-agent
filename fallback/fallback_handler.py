"""Reusable fallback messages for the healthcare assistant.

Fallbacks help the app fail safely. Each function returns the same dictionary
shape so future agents can handle problems in a simple, predictable way.
"""


def handle_missing_file(file_path):
    """Return a clear message when a required local file cannot be found."""
    return {
        "status": "missing_file",
        "message": f"The required file was not found: {file_path}",
        "recommendation": "Please check that the file exists in the project folder before running the tool again.",
    }


def handle_missing_topic(topic):
    """Return a safe message when the local knowledge base has no matching topic."""
    return {
        "status": "missing_topic",
        "message": f"The topic '{topic}' is not available in the local healthcare knowledge base.",
        "recommendation": "Please ask about one of the supported demo topics or consult a healthcare professional for personal advice.",
    }


def handle_tool_error(tool_name, error):
    """Return a simple error message when a tool fails unexpectedly."""
    return {
        "status": "tool_error",
        "message": f"{tool_name} could not complete its work. Error: {error}",
        "recommendation": "Please review the input and try again. If the problem continues, check the tool code and data files.",
    }


def handle_urgent_warning(reason):
    """Return an urgent safety warning for serious symptoms."""
    return {
        "status": "urgent_warning",
        "message": f"A possible urgent health warning was detected: {reason}",
        "recommendation": "Please seek urgent medical help or contact emergency services if symptoms are severe or sudden.",
    }
