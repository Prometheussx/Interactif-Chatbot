import requests
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    """API client for communicating with the backend"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.api_v1_url = f"{self.base_url}/api/v1"
        self.session = requests.Session()
        self.token = None
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def clear_token(self):
        """Clear authentication token"""
        self.token = None
        self.session.headers.pop("Authorization", None)
    
    def register(self, email: str, username: str, password: str, company_name: str = None) -> Dict[str, Any]:
        """Register a new user"""
        data = {
            "email": email,
            "username": username,
            "password": password,
            "company_name": company_name
        }
        response = self.session.post(f"{self.api_v1_url}/auth/register", json=data)
        response.raise_for_status()
        return response.json()
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        data = {"email": email, "password": password}
        response = self.session.post(f"{self.api_v1_url}/auth/login", json=data)
        response.raise_for_status()
        token_data = response.json()
        self.set_token(token_data["access_token"])
        return token_data
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current user info"""
        response = self.session.get(f"{self.api_v1_url}/auth/me")
        response.raise_for_status()
        return response.json()
    
    def create_chatbot(self, chatbot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new chatbot"""
        response = self.session.post(f"{self.api_v1_url}/chatbots/", json=chatbot_data)
        response.raise_for_status()
        return response.json()
    
    def get_chatbots(self) -> Dict[str, Any]:
        """Get all chatbots for current user"""
        response = self.session.get(f"{self.api_v1_url}/chatbots/")
        response.raise_for_status()
        return response.json()
    
    def get_chatbot(self, chatbot_id: int) -> Dict[str, Any]:
        """Get specific chatbot"""
        response = self.session.get(f"{self.api_v1_url}/chatbots/{chatbot_id}")
        response.raise_for_status()
        return response.json()
    
    def update_chatbot(self, chatbot_id: int, chatbot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update chatbot"""
        response = self.session.put(f"{self.api_v1_url}/chatbots/{chatbot_id}", json=chatbot_data)
        response.raise_for_status()
        return response.json()
    
    def delete_chatbot(self, chatbot_id: int) -> Dict[str, Any]:
        """Delete chatbot"""
        response = self.session.delete(f"{self.api_v1_url}/chatbots/{chatbot_id}")
        response.raise_for_status()
        return response.json()
    
    def regenerate_token(self, chatbot_id: int) -> Dict[str, Any]:
        """Regenerate API token for chatbot"""
        response = self.session.post(f"{self.api_v1_url}/chatbots/{chatbot_id}/regenerate-token")
        response.raise_for_status()
        return response.json()
    
    def send_chat_message(self, api_token: str, message: str, user_identifier: str = None, conversation_id: int = None) -> Dict[str, Any]:
        """Send chat message using API token"""
        headers = {"Authorization": f"Bearer {api_token}"}
        data = {
            "message": message,
            "user_identifier": user_identifier,
            "conversation_id": conversation_id
        }
        response = requests.post(f"{self.api_v1_url}/chat/", json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_conversation_history(self, api_token: str, conversation_id: int) -> Dict[str, Any]:
        """Get conversation history"""
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(f"{self.api_v1_url}/chat/conversations/{conversation_id}/history", headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_admin_stats(self) -> Dict[str, Any]:
        """Get admin statistics"""
        response = self.session.get(f"{self.api_v1_url}/admin/stats")
        response.raise_for_status()
        return response.json()