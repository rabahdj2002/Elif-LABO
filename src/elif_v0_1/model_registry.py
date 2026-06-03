"""
ELIF v0.1 Model Registry
Stability layer for hard-versioned LLM artifacts.
"""

MODEL_REGISTRY = {
    "sonnet": "claude-sonnet-4-6",
}

def resolve_model_id(key: str) -> str:
    """
    Resolves a logical model key to a hard-versioned API string.
    Only Anthropic Sonnet is supported (Article II Stability Lock).
    """
    return MODEL_REGISTRY.get("sonnet")
