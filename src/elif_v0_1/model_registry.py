"""
ELIF v0.1 Model Registry
Stability layer for hard-versioned LLM artifacts.
"""

MODEL_REGISTRY = {
    "sonnet": "claude-4-5-sonnet",
    "deepseek-chat": "deepseek-chat",
    "deepseek-reasoner": "deepseek-reasoner",
}

def resolve_model_id(key: str) -> str:
    """
    Resolves a logical model key to a hard-versioned API string.
    Supports Anthropic (deprecated) and DeepSeek (current).
    """
    return MODEL_REGISTRY.get(key, MODEL_REGISTRY["deepseek-chat"])
