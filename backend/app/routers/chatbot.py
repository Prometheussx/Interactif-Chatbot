from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.chatbot import ChatbotConfig
from ..schemas.chatbot import ChatbotConfigCreate, ChatbotConfigResponse, ChatbotConfigUpdate, ChatbotConfigList
from ..utils.helpers import generate_unique_api_token, validate_ai_provider, validate_model_name
from .auth import get_current_user_dependency

router = APIRouter(prefix="/chatbots", tags=["chatbots"])

@router.post("/", response_model=ChatbotConfigResponse)
async def create_chatbot(
    chatbot_data: ChatbotConfigCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Create a new chatbot configuration"""
    # Validate AI provider
    if not validate_ai_provider(chatbot_data.ai_provider):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid AI provider"
        )
    
    # Validate model name
    if not validate_model_name(chatbot_data.ai_provider, chatbot_data.model_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid model name for the specified provider"
        )
    
    # Generate unique API token
    existing_tokens = {config.api_token for config in db.query(ChatbotConfig).all()}
    api_token = generate_unique_api_token(existing_tokens)
    
    # Create chatbot configuration
    db_chatbot = ChatbotConfig(
        user_id=current_user.id,
        name=chatbot_data.name,
        ai_provider=chatbot_data.ai_provider,
        model_name=chatbot_data.model_name,
        system_prompt=chatbot_data.system_prompt,
        temperature=chatbot_data.temperature,
        max_tokens=chatbot_data.max_tokens,
        internet_access=chatbot_data.internet_access,
        rag_enabled=chatbot_data.rag_enabled,
        rag_provider=chatbot_data.rag_provider,
        voice_enabled=chatbot_data.voice_enabled,
        image_enabled=chatbot_data.image_enabled,
        api_token=api_token
    )
    
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    
    return ChatbotConfigResponse.from_orm(db_chatbot)

@router.get("/", response_model=ChatbotConfigList)
async def get_chatbots(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get all chatbot configurations for the current user"""
    chatbots = db.query(ChatbotConfig).filter(ChatbotConfig.user_id == current_user.id).all()
    
    return ChatbotConfigList(
        chatbots=[ChatbotConfigResponse.from_orm(chatbot) for chatbot in chatbots],
        total=len(chatbots)
    )

@router.get("/{chatbot_id}", response_model=ChatbotConfigResponse)
async def get_chatbot(
    chatbot_id: int,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get a specific chatbot configuration"""
    chatbot = db.query(ChatbotConfig).filter(
        ChatbotConfig.id == chatbot_id,
        ChatbotConfig.user_id == current_user.id
    ).first()
    
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    return ChatbotConfigResponse.from_orm(chatbot)

@router.put("/{chatbot_id}", response_model=ChatbotConfigResponse)
async def update_chatbot(
    chatbot_id: int,
    chatbot_data: ChatbotConfigUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Update a chatbot configuration"""
    chatbot = db.query(ChatbotConfig).filter(
        ChatbotConfig.id == chatbot_id,
        ChatbotConfig.user_id == current_user.id
    ).first()
    
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    # Update fields
    update_data = chatbot_data.dict(exclude_unset=True)
    
    # Validate AI provider and model if being updated
    if "ai_provider" in update_data:
        if not validate_ai_provider(update_data["ai_provider"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid AI provider"
            )
    
    if "model_name" in update_data:
        provider = update_data.get("ai_provider", chatbot.ai_provider)
        if not validate_model_name(provider, update_data["model_name"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid model name for the specified provider"
            )
    
    for field, value in update_data.items():
        setattr(chatbot, field, value)
    
    db.commit()
    db.refresh(chatbot)
    
    return ChatbotConfigResponse.from_orm(chatbot)

@router.delete("/{chatbot_id}")
async def delete_chatbot(
    chatbot_id: int,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Delete a chatbot configuration"""
    chatbot = db.query(ChatbotConfig).filter(
        ChatbotConfig.id == chatbot_id,
        ChatbotConfig.user_id == current_user.id
    ).first()
    
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    db.delete(chatbot)
    db.commit()
    
    return {"message": "Chatbot deleted successfully"}

@router.post("/{chatbot_id}/regenerate-token")
async def regenerate_api_token(
    chatbot_id: int,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Regenerate API token for a chatbot"""
    chatbot = db.query(ChatbotConfig).filter(
        ChatbotConfig.id == chatbot_id,
        ChatbotConfig.user_id == current_user.id
    ).first()
    
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    
    # Generate new unique API token
    existing_tokens = {config.api_token for config in db.query(ChatbotConfig).all()}
    new_token = generate_unique_api_token(existing_tokens)
    
    chatbot.api_token = new_token
    db.commit()
    db.refresh(chatbot)
    
    return {"api_token": new_token}