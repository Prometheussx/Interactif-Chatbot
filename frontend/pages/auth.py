import streamlit as st
from components.forms import render_login_form, render_register_form
from utils.helpers import init_session_state

def render_auth_page():
    """Render authentication page"""
    init_session_state()
    
    st.title("🤖 Interactif Chatbot")
    st.markdown("### Welcome to the customizable chatbot platform for businesses")
    
    # Create tabs for login and register
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_register_form()
    
    # Additional information
    st.divider()
    
    st.markdown("## 🌟 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤖 Multiple AI Providers**
        - OpenAI GPT models
        - Claude by Anthropic
        - Google Gemini
        """)
    
    with col2:
        st.markdown("""
        **📚 RAG Support**
        - Document-based responses
        - LangChain integration
        - Custom knowledge bases
        """)
    
    with col3:
        st.markdown("""
        **🔧 Customizable**
        - Custom system prompts
        - Configurable parameters
        - API integration
        """)
    
    st.divider()
    
    st.markdown("## 🚀 Getting Started")
    st.markdown("""
    1. **Register** for a new account or **Login** if you already have one
    2. **Create** your first chatbot configuration
    3. **Configure** AI provider, model, and parameters
    4. **Test** your chatbot using the built-in chat interface
    5. **Integrate** using the provided API token
    """)
    
    st.divider()
    
    st.markdown("## 📖 Documentation")
    st.markdown("""
    - [API Documentation](http://localhost:8000/docs)
    - [GitHub Repository](https://github.com/Prometheussx/Interactif-Chatbot)
    - [User Guide](https://github.com/Prometheussx/Interactif-Chatbot/blob/main/README.md)
    """)