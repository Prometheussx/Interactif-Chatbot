from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from ..database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbot_configs.id"), nullable=False)
    user_identifier = Column(String(255), nullable=True)  # End user identifier
    messages = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    chatbot = relationship("ChatbotConfig", back_populates="conversations")

class RagDocument(Base):
    __tablename__ = "rag_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbot_configs.id"), nullable=False)
    filename = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    # Note: VECTOR type would require pgvector extension
    # embeddings = Column(VECTOR(1536), nullable=True)  # OpenAI embeddings size
    metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    chatbot = relationship("ChatbotConfig", back_populates="rag_documents")