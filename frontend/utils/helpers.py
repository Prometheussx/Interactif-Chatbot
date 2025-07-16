import streamlit as st
from typing import Dict, Any
import datetime

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'api_client' not in st.session_state:
        from .api_client import APIClient
        st.session_state.api_client = APIClient()

def logout():
    """Logout user and clear session state"""
    st.session_state.authenticated = False
    st.session_state.user_data = None
    st.session_state.api_client.clear_token()

def format_datetime(dt_str: str) -> str:
    """Format datetime string for display"""
    try:
        dt = datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return dt_str

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def show_error(message: str):
    """Display error message"""
    st.error(f"❌ {message}")

def show_success(message: str):
    """Display success message"""
    st.success(f"✅ {message}")

def show_info(message: str):
    """Display info message"""
    st.info(f"ℹ️ {message}")

def show_warning(message: str):
    """Display warning message"""
    st.warning(f"⚠️ {message}")

def create_card(title: str, content: str, actions: list = None):
    """Create a card component"""
    with st.container():
        st.markdown(f"### {title}")
        st.markdown(content)
        if actions:
            cols = st.columns(len(actions))
            for i, action in enumerate(actions):
                with cols[i]:
                    if st.button(action['label'], key=action.get('key', f"action_{i}")):
                        action['callback']()

def display_chatbot_info(chatbot: Dict[str, Any]):
    """Display chatbot information in a formatted way"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {chatbot['name']}")
        st.write(f"**AI Provider:** {chatbot['ai_provider']}")
        st.write(f"**Model:** {chatbot['model_name']}")
        st.write(f"**Temperature:** {chatbot['temperature']}")
        st.write(f"**Max Tokens:** {chatbot['max_tokens']}")
    
    with col2:
        st.write(f"**Internet Access:** {'✅' if chatbot['internet_access'] else '❌'}")
        st.write(f"**RAG Enabled:** {'✅' if chatbot['rag_enabled'] else '❌'}")
        st.write(f"**Voice Enabled:** {'✅' if chatbot['voice_enabled'] else '❌'}")
        st.write(f"**Image Enabled:** {'✅' if chatbot['image_enabled'] else '❌'}")
        st.write(f"**Created:** {format_datetime(chatbot['created_at'])}")
    
    if chatbot.get('system_prompt'):
        st.write("**System Prompt:**")
        st.text_area("", value=chatbot['system_prompt'], height=100, disabled=True)

def get_ai_provider_options():
    """Get available AI provider options"""
    return {
        "openai": "OpenAI",
        "claude": "Claude (Anthropic)",
        "gemini": "Google Gemini"
    }

def get_model_options(provider: str):
    """Get model options for a specific provider"""
    models = {
        "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        "claude": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"],
        "gemini": ["gemini-pro", "gemini-pro-vision"]
    }
    return models.get(provider, [])