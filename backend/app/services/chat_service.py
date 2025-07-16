from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime
from ..models.conversation import Conversation
from ..models.chatbot import ChatbotConfig
from ..schemas.conversation import ConversationCreate, ChatRequest, ChatResponse
from .ai_service import AIService

class ChatService:
    """Service for handling chat operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        db_conversation = Conversation(
            chatbot_id=conversation_data.chatbot_id,
            user_identifier=conversation_data.user_identifier,
            messages=conversation_data.messages or []
        )
        
        self.db.add(db_conversation)
        self.db.commit()
        self.db.refresh(db_conversation)
        
        return db_conversation
    
    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID"""
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    def get_conversations_by_chatbot(self, chatbot_id: int) -> List[Conversation]:
        """Get all conversations for a chatbot"""
        return self.db.query(Conversation).filter(Conversation.chatbot_id == chatbot_id).all()
    
    def add_message_to_conversation(self, conversation_id: int, role: str, content: str) -> Conversation:
        """Add a message to an existing conversation"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        messages = conversation.messages or []
        messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        conversation.messages = messages
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation
    
    def process_chat_request(self, api_token: str, chat_request: ChatRequest) -> ChatResponse:
        """Process a chat request using the appropriate AI provider"""
        # Get chatbot config by API token
        chatbot_config = self.db.query(ChatbotConfig).filter(
            ChatbotConfig.api_token == api_token
        ).first()
        
        if not chatbot_config:
            raise ValueError("Invalid API token")
        
        # Get or create conversation
        conversation = None
        if chat_request.conversation_id:
            conversation = self.get_conversation(chat_request.conversation_id)
            if not conversation or conversation.chatbot_id != chatbot_config.id:
                raise ValueError("Invalid conversation ID")
        else:
            # Create new conversation
            conversation_data = ConversationCreate(
                chatbot_id=chatbot_config.id,
                user_identifier=chat_request.user_identifier,
                messages=[]
            )
            conversation = self.create_conversation(conversation_data)
        
        # Add user message to conversation
        conversation = self.add_message_to_conversation(
            conversation.id, 
            "user", 
            chat_request.message
        )
        
        # Prepare messages for AI service
        messages = []
        
        # Add system prompt if available
        if chatbot_config.system_prompt:
            messages.append({
                "role": "system",
                "content": chatbot_config.system_prompt
            })
        
        # Add conversation history
        for msg in conversation.messages:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Get AI response
        try:
            ai_response = self.ai_service.get_completion(
                provider=chatbot_config.ai_provider,
                model=chatbot_config.model_name,
                messages=messages,
                temperature=chatbot_config.temperature,
                max_tokens=chatbot_config.max_tokens
            )
        except Exception as e:
            raise ValueError(f"AI service error: {str(e)}")
        
        # Add AI response to conversation
        conversation = self.add_message_to_conversation(
            conversation.id,
            "assistant",
            ai_response
        )
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conversation.id
        )
    
    def get_conversation_history(self, conversation_id: int) -> List[Dict[str, Any]]:
        """Get conversation history"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        return conversation.messages or []