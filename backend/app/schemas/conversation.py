from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MessageBase(BaseModel):
    role: str  # user, assistant, system
    content: str
    timestamp: Optional[datetime] = None

class ConversationBase(BaseModel):
    user_identifier: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = []

class ConversationCreate(ConversationBase):
    chatbot_id: int

class ConversationUpdate(BaseModel):
    messages: Optional[List[Dict[str, Any]]] = None

class ConversationResponse(ConversationBase):
    id: int
    chatbot_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    user_identifier: Optional[str] = None
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: int
    message_id: Optional[str] = None

class RagDocumentBase(BaseModel):
    filename: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class RagDocumentCreate(RagDocumentBase):
    chatbot_id: int

class RagDocumentResponse(RagDocumentBase):
    id: int
    chatbot_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True