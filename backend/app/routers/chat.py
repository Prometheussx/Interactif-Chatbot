from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..schemas.conversation import ChatRequest, ChatResponse, ConversationResponse
from ..services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """Send a chat message and get AI response"""
    # Extract API token from Authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    api_token = authorization.split(" ", 1)[1]
    
    chat_service = ChatService(db)
    
    try:
        response = chat_service.process_chat_request(api_token, chat_request)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """Get conversation details"""
    # Extract API token from Authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    api_token = authorization.split(" ", 1)[1]
    
    chat_service = ChatService(db)
    
    # Verify API token and get chatbot
    from ..models.chatbot import ChatbotConfig
    chatbot_config = db.query(ChatbotConfig).filter(
        ChatbotConfig.api_token == api_token
    ).first()
    
    if not chatbot_config:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token"
        )
    
    conversation = chat_service.get_conversation(conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Verify conversation belongs to the chatbot
    if conversation.chatbot_id != chatbot_config.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this conversation"
        )
    
    return ConversationResponse.from_orm(conversation)

@router.get("/conversations/{conversation_id}/history")
async def get_conversation_history(
    conversation_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """Get conversation message history"""
    # Extract API token from Authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    api_token = authorization.split(" ", 1)[1]
    
    chat_service = ChatService(db)
    
    # Verify API token and get chatbot
    from ..models.chatbot import ChatbotConfig
    chatbot_config = db.query(ChatbotConfig).filter(
        ChatbotConfig.api_token == api_token
    ).first()
    
    if not chatbot_config:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token"
        )
    
    conversation = chat_service.get_conversation(conversation_id)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Verify conversation belongs to the chatbot
    if conversation.chatbot_id != chatbot_config.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this conversation"
        )
    
    try:
        history = chat_service.get_conversation_history(conversation_id)
        return {"messages": history}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )