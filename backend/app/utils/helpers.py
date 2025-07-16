import secrets
import string
from typing import Optional
from datetime import datetime

def generate_api_token(length: int = 32) -> str:
    """Generate a secure random API token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_unique_api_token(existing_tokens: Optional[set] = None) -> str:
    """Generate a unique API token that doesn't exist in the provided set"""
    if existing_tokens is None:
        existing_tokens = set()
    
    while True:
        token = generate_api_token()
        if token not in existing_tokens:
            return token

def validate_ai_provider(provider: str) -> bool:
    """Validate if the AI provider is supported"""
    supported_providers = ["openai", "claude", "gemini"]
    return provider.lower() in supported_providers

def validate_model_name(provider: str, model: str) -> bool:
    """Validate if the model is supported for the given provider"""
    model_mapping = {
        "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        "claude": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"],
        "gemini": ["gemini-pro", "gemini-pro-vision"]
    }
    
    return provider.lower() in model_mapping and model in model_mapping[provider.lower()]

def format_timestamp(dt: datetime) -> str:
    """Format datetime for API responses"""
    return dt.isoformat()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove potentially dangerous characters
    import re
    return re.sub(r'[^\w\-_\.]', '_', filename)