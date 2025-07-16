from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class ChatbotConfig(Base):
    __tablename__ = "chatbot_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    ai_provider = Column(String(50), nullable=False)  # openai, claude, gemini
    model_name = Column(String(100), nullable=False)
    system_prompt = Column(Text, nullable=True)
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=1000)
    internet_access = Column(Boolean, default=False)
    rag_enabled = Column(Boolean, default=False)
    rag_provider = Column(String(50), nullable=True)  # langchain, llamaindex
    voice_enabled = Column(Boolean, default=False)
    image_enabled = Column(Boolean, default=False)
    api_token = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chatbots")
    conversations = relationship("Conversation", back_populates="chatbot")
    rag_documents = relationship("RagDocument", back_populates="chatbot")