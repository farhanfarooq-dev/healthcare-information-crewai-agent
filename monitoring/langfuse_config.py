"""Optional Langfuse observability helper.

This project should run even when Langfuse keys are missing. For that reason,
all monitoring code is written as a safe helper: it prints useful demo messages
and never stops the healthcare assistant if monitoring fails.
"""

import os


_langfuse_warning_printed = False
_langfuse_client = None


def is_langfuse_configured():
    """Return True only when the required Langfuse keys are available."""
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    return bool(public_key and secret_key)


def _get_langfuse_client():
    """Create a Langfuse client if the installed SDK supports it.

    Langfuse SDK versions can differ. This helper tries the common import path
    and returns None if the SDK is missing or behaves differently.
    """
    global _langfuse_client

    if _langfuse_client is not None:
        return _langfuse_client

    try:
        from langfuse import Langfuse

        _langfuse_client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )
        return _langfuse_client
    except Exception as error:
        print(f"Langfuse SDK logging is unavailable: {error}")
        return None


def log_event(event_name: str, metadata: dict | None = None):
    """Log a simple monitoring event without breaking the app.

    If Langfuse is not configured, the function prints the required fallback
    message and returns safely. If Langfuse is configured, it tries to create a
    simple trace/event using the installed SDK.
    """
    global _langfuse_warning_printed

    metadata = metadata or {}

    if not is_langfuse_configured():
        if not _langfuse_warning_printed:
            print("Langfuse not configured. Running without remote tracing.")
            _langfuse_warning_printed = True
        return

    print(f"Langfuse event would be logged: {event_name} | metadata={metadata}")

    try:
        client = _get_langfuse_client()
        if client is None:
            return

        # Many Langfuse SDK versions support trace(). Some also support event().
        # We try both patterns in a safe way for demo-friendly compatibility.
        trace = None
        if hasattr(client, "trace"):
            trace = client.trace(name=event_name, metadata=metadata)

        if trace is not None and hasattr(trace, "event"):
            trace.event(name=event_name, metadata=metadata)
        elif hasattr(client, "event"):
            client.event(name=event_name, metadata=metadata)

        if hasattr(client, "flush"):
            client.flush()
    except Exception as error:
        print(f"Langfuse logging failed, but the app will continue: {error}")
