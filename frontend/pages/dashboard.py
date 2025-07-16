import streamlit as st
from utils.helpers import show_success, show_error, format_datetime

def render_dashboard():
    """Render the main dashboard"""
    st.title("📊 Dashboard")
    st.markdown(f"Welcome back, **{st.session_state.user_data.get('username')}**!")
    
    # Quick stats
    try:
        chatbots_data = st.session_state.api_client.get_chatbots()
        chatbots = chatbots_data.get('chatbots', [])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Chatbots", len(chatbots))
        
        with col2:
            active_chatbots = len([c for c in chatbots if c])  # All existing chatbots are considered active
            st.metric("Active Chatbots", active_chatbots)
        
        with col3:
            subscription_tier = st.session_state.user_data.get('subscription_tier', 'free')
            st.metric("Subscription", subscription_tier.title())
        
        with col4:
            # Calculate total conversations (placeholder for now)
            st.metric("Total Conversations", "0")
        
    except Exception as e:
        show_error(f"Failed to load dashboard data: {str(e)}")
        return
    
    st.divider()
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    if not chatbots:
        st.info("No chatbots created yet. Create your first chatbot to get started!")
        if st.button("🤖 Create First Chatbot", use_container_width=True):
            st.session_state.current_page = "chatbot_create"
            st.rerun()
    else:
        # Show recent chatbots
        st.markdown("### Recently Created Chatbots")
        for chatbot in chatbots[-3:]:  # Show last 3 chatbots
            with st.expander(f"🤖 {chatbot['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Provider:** {chatbot['ai_provider']}")
                    st.write(f"**Model:** {chatbot['model_name']}")
                    st.write(f"**Created:** {format_datetime(chatbot['created_at'])}")
                
                with col2:
                    st.write(f"**Temperature:** {chatbot['temperature']}")
                    st.write(f"**Max Tokens:** {chatbot['max_tokens']}")
                    st.write(f"**RAG Enabled:** {'✅' if chatbot['rag_enabled'] else '❌'}")
                
                # Quick actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💬 Test Chat", key=f"test_{chatbot['id']}"):
                        st.session_state.selected_chatbot = chatbot
                        st.session_state.current_page = "chat_test"
                        st.rerun()
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{chatbot['id']}"):
                        st.session_state.selected_chatbot = chatbot
                        st.session_state.current_page = "chatbot_edit"
                        st.rerun()
                
                with col3:
                    st.code(chatbot['api_token'][:20] + "...", language="text")
    
    st.divider()
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Create New Chatbot", use_container_width=True):
            st.session_state.current_page = "chatbot_create"
            st.rerun()
    
    with col2:
        if st.button("📋 View All Chatbots", use_container_width=True):
            st.session_state.current_page = "chatbots"
            st.rerun()
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = "analytics"
            st.rerun()
    
    st.divider()
    
    # System notifications
    st.subheader("🔔 System Notifications")
    
    # Show some example notifications
    st.info("ℹ️ Welcome to Interactif Chatbot! Start by creating your first chatbot.")
    
    if st.session_state.user_data.get('subscription_tier') == 'free':
        st.warning("⚠️ You're on the free tier. Upgrade to unlock more features!")
    
    # Tips and tricks
    st.subheader("💡 Tips & Tricks")
    
    with st.expander("🎯 Best Practices for Chatbot Configuration"):
        st.markdown("""
        - **System Prompt**: Be specific about the chatbot's role and behavior
        - **Temperature**: Use lower values (0.1-0.3) for consistent responses, higher (0.7-1.0) for creative responses
        - **Max Tokens**: Set appropriate limits based on your use case
        - **RAG**: Enable document search for knowledge-based chatbots
        """)
    
    with st.expander("🔧 API Integration"):
        st.markdown("""
        - Use the provided API token to integrate your chatbot
        - Make POST requests to `/api/v1/chat/` endpoint
        - Include the Authorization header with your API token
        - Check the [API Documentation](http://localhost:8000/docs) for details
        """)
    
    with st.expander("📈 Monitoring & Analytics"):
        st.markdown("""
        - Monitor your chatbot's performance in the Analytics section
        - Track conversation metrics and user engagement
        - Use the feedback to improve your chatbot's configuration
        """)

def render_user_profile():
    """Render user profile section"""
    st.subheader("👤 User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Username:** {st.session_state.user_data.get('username')}")
        st.write(f"**Email:** {st.session_state.user_data.get('email')}")
        st.write(f"**Company:** {st.session_state.user_data.get('company_name', 'Not specified')}")
    
    with col2:
        st.write(f"**Subscription:** {st.session_state.user_data.get('subscription_tier', 'free')}")
        st.write(f"**Member Since:** {format_datetime(st.session_state.user_data.get('created_at', ''))}")
    
    if st.button("✏️ Edit Profile"):
        st.info("Profile editing feature coming soon!")