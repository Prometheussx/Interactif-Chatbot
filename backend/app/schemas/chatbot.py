from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatbotConfigBase(BaseModel):
    name: str
    ai_provider: str  # openai, claude, gemini
    model_name: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    internet_access: bool = False
    rag_enabled: bool = False
    rag_provider: Optional[str] = None
    voice_enabled: bool = False
    image_enabled: bool = False

class ChatbotConfigCreate(ChatbotConfigBase):
    pass

class ChatbotConfigUpdate(BaseModel):
    name: Optional[str] = None
    ai_provider: Optional[str] = None
    model_name: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    internet_access: Optional[bool] = None
    rag_enabled: Optional[bool] = None
    rag_provider: Optional[str] = None
    voice_enabled: Optional[bool] = None
    image_enabled: Optional[bool] = None

class ChatbotConfigResponse(ChatbotConfigBase):
    id: int
    user_id: int
    api_token: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatbotConfigList(BaseModel):
    chatbots: List[ChatbotConfigResponse]
    total: int