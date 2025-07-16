from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.chatbot import ChatbotConfig
from ..schemas.user import UserResponse
from ..schemas.chatbot import ChatbotConfigResponse
from .auth import get_current_user_dependency

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    # Basic admin check - in production, implement proper role-based access control
    if current_user.subscription_tier != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    users = db.query(User).all()
    return [UserResponse.from_orm(user) for user in users]

@router.get("/chatbots", response_model=List[ChatbotConfigResponse])
async def get_all_chatbots(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get all chatbots (admin only)"""
    # Basic admin check - in production, implement proper role-based access control
    if current_user.subscription_tier != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    chatbots = db.query(ChatbotConfig).all()
    return [ChatbotConfigResponse.from_orm(chatbot) for chatbot in chatbots]

@router.get("/stats")
async def get_system_stats(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get system statistics (admin only)"""
    # Basic admin check - in production, implement proper role-based access control
    if current_user.subscription_tier != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    from ..models.conversation import Conversation
    
    total_users = db.query(User).count()
    total_chatbots = db.query(ChatbotConfig).count()
    total_conversations = db.query(Conversation).count()
    
    # User distribution by subscription tier
    subscription_stats = db.query(User.subscription_tier, db.func.count(User.id)).group_by(User.subscription_tier).all()
    
    # AI provider distribution
    provider_stats = db.query(ChatbotConfig.ai_provider, db.func.count(ChatbotConfig.id)).group_by(ChatbotConfig.ai_provider).all()
    
    return {
        "total_users": total_users,
        "total_chatbots": total_chatbots,
        "total_conversations": total_conversations,
        "subscription_distribution": dict(subscription_stats),
        "provider_distribution": dict(provider_stats)
    }