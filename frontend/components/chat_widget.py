import streamlit as st
from typing import Dict, Any, List
from datetime import datetime

def render_chat_widget(api_token: str, chatbot_name: str):
    """Render the chat widget component"""
    st.subheader(f"💬 Chat with {chatbot_name}")
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_conversation_id' not in st.session_state:
        st.session_state.current_conversation_id = None
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message.get("timestamp"):
                    st.caption(f"Sent at: {message['timestamp']}")
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat history
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.chat_history.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.api_client.send_chat_message(
                        api_token=api_token,
                        message=user_input,
                        user_identifier="streamlit_user",
                        conversation_id=st.session_state.current_conversation_id
                    )
                    
                    ai_response = response["response"]
                    st.session_state.current_conversation_id = response["conversation_id"]
                    
                    # Add AI response to chat history
                    ai_message = {
                        "role": "assistant",
                        "content": ai_response,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.chat_history.append(ai_message)
                    
                    st.write(ai_response)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Rerun to update the chat display
        st.rerun()
    
    # Chat controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.current_conversation_id = None
            st.rerun()
    
    with col2:
        if st.button("📥 Export Chat", use_container_width=True):
            export_chat_history()

def export_chat_history():
    """Export chat history to a downloadable file"""
    if not st.session_state.chat_history:
        st.warning("No chat history to export.")
        return
    
    # Create export content
    export_content = "# Chat History Export\n\n"
    export_content += f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for i, message in enumerate(st.session_state.chat_history):
        role = "User" if message["role"] == "user" else "Assistant"
        export_content += f"## {role} ({message.get('timestamp', 'Unknown time')})\n"
        export_content += f"{message['content']}\n\n"
    
    # Create download button
    st.download_button(
        label="📥 Download Chat History",
        data=export_content,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

def render_message_bubble(message: Dict[str, Any], is_user: bool = True):
    """Render a message bubble"""
    if is_user:
        st.markdown(f"""
        <div style="
            background-color: #007bff;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: right;
            margin-left: 20%;
        ">
            {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background-color: #f1f1f1;
            color: black;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            text-align: left;
            margin-right: 20%;
        ">
            {message['content']}
        </div>
        """, unsafe_allow_html=True)

def render_chat_statistics():
    """Render chat statistics"""
    if not st.session_state.chat_history:
        st.info("No chat history available.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_messages = len(st.session_state.chat_history)
        st.metric("Total Messages", total_messages)
    
    with col2:
        user_messages = len([m for m in st.session_state.chat_history if m["role"] == "user"])
        st.metric("User Messages", user_messages)
    
    with col3:
        ai_messages = len([m for m in st.session_state.chat_history if m["role"] == "assistant"])
        st.metric("AI Messages", ai_messages)
    
    # Word count analysis
    if st.session_state.chat_history:
        user_words = sum(len(m["content"].split()) for m in st.session_state.chat_history if m["role"] == "user")
        ai_words = sum(len(m["content"].split()) for m in st.session_state.chat_history if m["role"] == "assistant")
        
        st.subheader("Word Count Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("User Words", user_words)
        
        with col2:
            st.metric("AI Words", ai_words)