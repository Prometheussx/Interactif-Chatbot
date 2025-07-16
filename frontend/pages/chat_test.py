import streamlit as st
from components.chat_widget import render_chat_widget, render_chat_statistics
from utils.helpers import show_error, show_info

def render_chat_test():
    """Render chat testing page"""
    st.title("💬 Chat Test")
    
    # Check if chatbot is selected
    if 'selected_chatbot' not in st.session_state:
        render_chatbot_selection()
        return
    
    chatbot = st.session_state.selected_chatbot
    
    # Back button and chatbot info
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("← Back"):
            st.session_state.selected_chatbot = None
            st.rerun()
    
    with col2:
        st.info(f"Testing chatbot: **{chatbot['name']}** ({chatbot['ai_provider']} - {chatbot['model_name']})")
    
    # Chat interface
    st.divider()
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Statistics", "⚙️ Settings"])
    
    with tab1:
        render_chat_widget(chatbot['api_token'], chatbot['name'])
    
    with tab2:
        render_chat_statistics()
    
    with tab3:
        render_chat_settings(chatbot)

def render_chatbot_selection():
    """Render chatbot selection interface"""
    st.subheader("🤖 Select a Chatbot to Test")
    
    try:
        chatbots_data = st.session_state.api_client.get_chatbots()
        chatbots = chatbots_data.get('chatbots', [])
        
        if not chatbots:
            st.info("No chatbots found. Create a chatbot first to test it.")
            if st.button("➕ Create New Chatbot", use_container_width=True):
                st.session_state.current_page = "chatbot_create"
                st.rerun()
            return
        
        # Display chatbots as cards
        for chatbot in chatbots:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.subheader(f"🤖 {chatbot['name']}")
                    st.write(f"**Provider:** {chatbot['ai_provider']}")
                    st.write(f"**Model:** {chatbot['model_name']}")
                
                with col2:
                    st.write(f"**Temperature:** {chatbot['temperature']}")
                    st.write(f"**Max Tokens:** {chatbot['max_tokens']}")
                    st.write(f"**RAG:** {'✅' if chatbot['rag_enabled'] else '❌'}")
                
                with col3:
                    if st.button("💬 Test", key=f"test_{chatbot['id']}", use_container_width=True):
                        st.session_state.selected_chatbot = chatbot
                        # Clear previous chat history
                        st.session_state.chat_history = []
                        st.session_state.current_conversation_id = None
                        st.rerun()
                
                st.divider()
    
    except Exception as e:
        show_error(f"Failed to load chatbots: {str(e)}")

def render_chat_settings(chatbot):
    """Render chat settings and configuration"""
    st.subheader("⚙️ Chat Settings")
    
    # Display current configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Current Configuration:**")
        st.json({
            "ai_provider": chatbot['ai_provider'],
            "model_name": chatbot['model_name'],
            "temperature": chatbot['temperature'],
            "max_tokens": chatbot['max_tokens'],
            "rag_enabled": chatbot['rag_enabled'],
            "voice_enabled": chatbot['voice_enabled'],
            "image_enabled": chatbot['image_enabled']
        })
    
    with col2:
        st.write("**System Prompt:**")
        if chatbot.get('system_prompt'):
            st.text_area("", value=chatbot['system_prompt'], height=200, disabled=True)
        else:
            st.info("No system prompt configured")
    
    # Chat test options
    st.subheader("🧪 Test Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Show response time", value=True, key="show_response_time")
        st.checkbox("Show token usage", value=True, key="show_token_usage")
    
    with col2:
        st.checkbox("Auto-save conversations", value=True, key="auto_save")
        st.checkbox("Show debug info", value=False, key="show_debug")
    
    # Quick test messages
    st.subheader("🚀 Quick Test Messages")
    
    quick_messages = [
        "Hello! How are you?",
        "What can you help me with?",
        "Tell me about yourself",
        "What's the weather like?",
        "Can you help me with programming?"
    ]
    
    cols = st.columns(len(quick_messages))
    
    for i, message in enumerate(quick_messages):
        with cols[i]:
            if st.button(message, key=f"quick_{i}"):
                # Add to chat history and trigger response
                st.session_state.quick_message = message
                st.rerun()
    
    # API testing
    st.subheader("🔧 API Testing")
    
    if st.button("Test API Connection", use_container_width=True):
        test_api_connection(chatbot)

def test_api_connection(chatbot):
    """Test API connection with the chatbot"""
    try:
        with st.spinner("Testing API connection..."):
            response = st.session_state.api_client.send_chat_message(
                api_token=chatbot['api_token'],
                message="Test message",
                user_identifier="test_user"
            )
        
        st.success("✅ API connection successful!")
        st.json(response)
    
    except Exception as e:
        st.error(f"❌ API connection failed: {str(e)}")

def render_conversation_manager():
    """Render conversation management interface"""
    st.subheader("📋 Conversation Manager")
    
    # This would show conversation history and allow management
    # For now, just show placeholder
    st.info("Conversation management features coming soon!")
    
    # Mock conversation list
    conversations = [
        {"id": 1, "user": "user123", "messages": 5, "created": "2024-01-01"},
        {"id": 2, "user": "user456", "messages": 3, "created": "2024-01-02"},
    ]
    
    for conv in conversations:
        with st.expander(f"Conversation {conv['id']} - {conv['user']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**User:** {conv['user']}")
            
            with col2:
                st.write(f"**Messages:** {conv['messages']}")
            
            with col3:
                st.write(f"**Created:** {conv['created']}")
            
            if st.button("View Details", key=f"view_{conv['id']}"):
                st.info("Conversation details coming soon!")

def render_chat_export():
    """Render chat export functionality"""
    st.subheader("📤 Export Chat")
    
    if 'chat_history' not in st.session_state or not st.session_state.chat_history:
        st.info("No chat history to export.")
        return
    
    export_format = st.selectbox("Export Format", ["JSON", "CSV", "Markdown", "PDF"])
    
    if st.button("Export Chat History", use_container_width=True):
        # Export functionality would go here
        st.success(f"Chat history exported as {export_format}!")
        st.download_button(
            label="Download Export",
            data="Sample export data",
            file_name=f"chat_export.{export_format.lower()}",
            mime="text/plain"
        )