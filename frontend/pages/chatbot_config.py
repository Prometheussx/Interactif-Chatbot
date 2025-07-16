import streamlit as st
from components.forms import render_chatbot_form
from utils.helpers import show_success, show_error, display_chatbot_info, format_datetime

def render_chatbot_config():
    """Render chatbot configuration page"""
    st.title("🤖 Chatbot Management")
    
    # Navigation tabs
    if 'current_chatbot_tab' not in st.session_state:
        st.session_state.current_chatbot_tab = "list"
    
    tab1, tab2 = st.tabs(["📋 My Chatbots", "➕ Create New"])
    
    with tab1:
        render_chatbot_list()
    
    with tab2:
        render_chatbot_form()

def render_chatbot_list():
    """Render the list of user's chatbots"""
    try:
        chatbots_data = st.session_state.api_client.get_chatbots()
        chatbots = chatbots_data.get('chatbots', [])
        
        if not chatbots:
            st.info("No chatbots found. Create your first chatbot to get started!")
            return
        
        st.subheader(f"📋 Your Chatbots ({len(chatbots)})")
        
        # Search and filter
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("🔍 Search chatbots", placeholder="Search by name...")
        
        with col2:
            provider_filter = st.selectbox(
                "Filter by Provider",
                options=["All", "openai", "claude", "gemini"],
                index=0
            )
        
        # Filter chatbots
        filtered_chatbots = chatbots
        
        if search_term:
            filtered_chatbots = [c for c in filtered_chatbots if search_term.lower() in c['name'].lower()]
        
        if provider_filter != "All":
            filtered_chatbots = [c for c in filtered_chatbots if c['ai_provider'] == provider_filter]
        
        # Display chatbots
        for chatbot in filtered_chatbots:
            with st.expander(f"🤖 {chatbot['name']} ({chatbot['ai_provider']} - {chatbot['model_name']})"):
                display_chatbot_info(chatbot)
                
                st.subheader("🔑 API Token")
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.code(chatbot['api_token'], language="text")
                
                with col2:
                    if st.button("🔄 Regenerate", key=f"regen_{chatbot['id']}"):
                        try:
                            result = st.session_state.api_client.regenerate_token(chatbot['id'])
                            show_success("API token regenerated successfully!")
                            st.rerun()
                        except Exception as e:
                            show_error(f"Failed to regenerate token: {str(e)}")
                
                st.subheader("⚡ Actions")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("💬 Test Chat", key=f"test_chat_{chatbot['id']}"):
                        st.session_state.selected_chatbot = chatbot
                        st.session_state.current_page = "chat_test"
                        st.rerun()
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{chatbot['id']}"):
                        st.session_state.selected_chatbot = chatbot
                        st.session_state.current_page = "chatbot_edit"
                        st.rerun()
                
                with col3:
                    if st.button("📊 Analytics", key=f"analytics_{chatbot['id']}"):
                        st.session_state.selected_chatbot = chatbot
                        st.session_state.current_page = "analytics"
                        st.rerun()
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{chatbot['id']}"):
                        st.session_state.delete_chatbot_id = chatbot['id']
                        st.session_state.show_delete_confirm = True
                        st.rerun()
        
        # Delete confirmation dialog
        if st.session_state.get('show_delete_confirm'):
            render_delete_confirmation()
    
    except Exception as e:
        show_error(f"Failed to load chatbots: {str(e)}")

def render_delete_confirmation():
    """Render delete confirmation dialog"""
    st.subheader("⚠️ Confirm Deletion")
    st.warning("Are you sure you want to delete this chatbot? This action cannot be undone.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, Delete", type="primary"):
            try:
                st.session_state.api_client.delete_chatbot(st.session_state.delete_chatbot_id)
                show_success("Chatbot deleted successfully!")
                st.session_state.show_delete_confirm = False
                st.session_state.delete_chatbot_id = None
                st.rerun()
            except Exception as e:
                show_error(f"Failed to delete chatbot: {str(e)}")
    
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.show_delete_confirm = False
            st.session_state.delete_chatbot_id = None
            st.rerun()

def render_chatbot_edit():
    """Render chatbot edit page"""
    st.title("✏️ Edit Chatbot")
    
    if 'selected_chatbot' not in st.session_state:
        st.error("No chatbot selected for editing.")
        if st.button("← Back to Chatbots"):
            st.session_state.current_page = "chatbots"
            st.rerun()
        return
    
    chatbot = st.session_state.selected_chatbot
    
    # Back button
    if st.button("← Back to Chatbots"):
        st.session_state.current_page = "chatbots"
        st.rerun()
    
    st.divider()
    
    # Edit form
    render_chatbot_form(chatbot)

def render_chatbot_create():
    """Render chatbot creation page"""
    st.title("➕ Create New Chatbot")
    
    # Back button
    if st.button("← Back to Chatbots"):
        st.session_state.current_page = "chatbots"
        st.rerun()
    
    st.divider()
    
    # Create form
    render_chatbot_form()

def render_api_documentation():
    """Render API documentation section"""
    st.subheader("📖 API Documentation")
    
    st.markdown("""
    ### Authentication
    All API requests require authentication using the API token in the Authorization header:
    
    ```
    Authorization: Bearer YOUR_API_TOKEN
    ```
    
    ### Send Chat Message
    **Endpoint:** `POST /api/v1/chat/`
    
    **Request Body:**
    ```json
    {
        "message": "Hello, how are you?",
        "user_identifier": "user123",
        "conversation_id": null
    }
    ```
    
    **Response:**
    ```json
    {
        "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
        "conversation_id": 123
    }
    ```
    
    ### Get Conversation History
    **Endpoint:** `GET /api/v1/chat/conversations/{conversation_id}/history`
    
    **Response:**
    ```json
    {
        "messages": [
            {
                "role": "user",
                "content": "Hello",
                "timestamp": "2024-01-01T12:00:00"
            },
            {
                "role": "assistant",
                "content": "Hello! How can I help you?",
                "timestamp": "2024-01-01T12:00:01"
            }
        ]
    }
    ```
    
    ### Example Code
    
    **Python:**
    ```python
    import requests
    
    url = "http://localhost:8000/api/v1/chat/"
    headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
    data = {
        "message": "Hello, world!",
        "user_identifier": "user123"
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    print(result["response"])
    ```
    
    **JavaScript:**
    ```javascript
    const response = await fetch('http://localhost:8000/api/v1/chat/', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer YOUR_API_TOKEN',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: 'Hello, world!',
            user_identifier: 'user123'
        })
    });
    
    const result = await response.json();
    console.log(result.response);
    ```
    
    For complete API documentation, visit: [http://localhost:8000/docs](http://localhost:8000/docs)
    """)