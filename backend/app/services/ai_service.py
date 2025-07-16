from typing import Optional, Dict, Any
from ..config import settings

class AIService:
    """Service for handling AI provider integrations"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI provider clients"""
        try:
            if settings.OPENAI_API_KEY:
                import openai
                self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        except ImportError:
            pass
        
        try:
            if settings.ANTHROPIC_API_KEY:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        except ImportError:
            pass
        
        # Note: Gemini integration would go here
    
    def get_completion(self, 
                      provider: str, 
                      model: str, 
                      messages: list, 
                      temperature: float = 0.7,
                      max_tokens: int = 1000) -> str:
        """Get completion from specified AI provider"""
        
        if provider.lower() == "openai":
            return self._get_openai_completion(model, messages, temperature, max_tokens)
        elif provider.lower() == "claude":
            return self._get_claude_completion(model, messages, temperature, max_tokens)
        elif provider.lower() == "gemini":
            return self._get_gemini_completion(model, messages, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
    
    def _get_openai_completion(self, model: str, messages: list, temperature: float, max_tokens: int) -> str:
        """Get completion from OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Check API key.")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"OpenAI API error: {str(e)}")
    
    def _get_claude_completion(self, model: str, messages: list, temperature: float, max_tokens: int) -> str:
        """Get completion from Claude"""
        if not self.anthropic_client:
            raise ValueError("Claude client not initialized. Check API key.")
        
        try:
            # Convert messages to Claude format
            claude_messages = []
            system_message = ""
            
            for message in messages:
                if message["role"] == "system":
                    system_message = message["content"]
                else:
                    claude_messages.append({
                        "role": message["role"],
                        "content": message["content"]
                    })
            
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=claude_messages
            )
            
            return response.content[0].text
        except Exception as e:
            raise ValueError(f"Claude API error: {str(e)}")
    
    def _get_gemini_completion(self, model: str, messages: list, temperature: float, max_tokens: int) -> str:
        """Get completion from Gemini"""
        # Placeholder for Gemini integration
        raise NotImplementedError("Gemini integration not yet implemented")
    
    def validate_provider_config(self, provider: str) -> bool:
        """Validate if provider is configured correctly"""
        if provider.lower() == "openai":
            return self.openai_client is not None
        elif provider.lower() == "claude":
            return self.anthropic_client is not None
        elif provider.lower() == "gemini":
            return False  # Not implemented yet
        else:
            return False