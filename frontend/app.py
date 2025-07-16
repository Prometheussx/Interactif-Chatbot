import streamlit as st
from components.sidebar import render_sidebar
from pages.auth import render_auth_page
from pages.dashboard import render_dashboard
from pages.chatbot_config import render_chatbot_config, render_chatbot_edit, render_chatbot_create
from pages.chat_test import render_chat_test
from pages.analytics import render_analytics
from utils.helpers import init_session_state

# Page configuration
st.set_page_config(
    page_title="Interactif Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Initialize current page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "auth" if not st.session_state.authenticated else "dashboard"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .chat-message {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
    }
    
    .user-message {
        background: #e3f2fd;
        text-align: right;
    }
    
    .assistant-message {
        background: #f5f5f5;
        text-align: left;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
    }
    
    .stSelectbox > div > div {
        border-radius: 0.5rem;
    }
    
    .stTextInput > div > div {
        border-radius: 0.5rem;
    }
    
    .stTextArea > div > div {
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        render_auth_page()
    else:
        # Handle authenticated pages
        page = st.session_state.current_page
        
        if page == "dashboard":
            render_dashboard()
        elif page == "chatbots":
            render_chatbot_config()
        elif page == "chatbot_create":
            render_chatbot_create()
        elif page == "chatbot_edit":
            render_chatbot_edit()
        elif page == "chat_test":
            render_chat_test()
        elif page == "analytics":
            render_analytics()
        elif page == "admin":
            render_admin_page()
        else:
            # Default to dashboard
            render_dashboard()

def render_admin_page():
    """Render admin page"""
    st.title("⚙️ Admin Panel")
    
    # Check if user is admin
    if st.session_state.user_data.get('subscription_tier') != 'admin':
        st.error("Access denied. Admin privileges required.")
        return
    
    # Admin tabs
    tab1, tab2, tab3 = st.tabs(["👥 Users", "🤖 Chatbots", "📊 Statistics"])
    
    with tab1:
        render_admin_users()
    
    with tab2:
        render_admin_chatbots()
    
    with tab3:
        render_admin_statistics()

def render_admin_users():
    """Render admin users management"""
    st.subheader("👥 User Management")
    
    try:
        # This would call an admin API to get all users
        # For now, show placeholder
        st.info("User management features coming soon!")
        
        # Mock user data
        users = [
            {"id": 1, "username": "user1", "email": "user1@example.com", "tier": "free"},
            {"id": 2, "username": "user2", "email": "user2@example.com", "tier": "pro"},
        ]
        
        for user in users:
            with st.expander(f"👤 {user['username']} ({user['email']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**ID:** {user['id']}")
                    st.write(f"**Tier:** {user['tier']}")
                
                with col2:
                    if st.button("Edit", key=f"edit_user_{user['id']}"):
                        st.info("Edit user functionality coming soon!")
                
                with col3:
                    if st.button("Delete", key=f"delete_user_{user['id']}"):
                        st.warning("Delete user functionality coming soon!")
    
    except Exception as e:
        st.error(f"Failed to load users: {str(e)}")

def render_admin_chatbots():
    """Render admin chatbots management"""
    st.subheader("🤖 Chatbot Management")
    
    try:
        # This would call an admin API to get all chatbots
        st.info("Admin chatbot management features coming soon!")
        
    except Exception as e:
        st.error(f"Failed to load chatbots: {str(e)}")

def render_admin_statistics():
    """Render admin statistics"""
    st.subheader("📊 System Statistics")
    
    try:
        admin_stats = st.session_state.api_client.get_admin_stats()
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", admin_stats['total_users'])
        
        with col2:
            st.metric("Total Chatbots", admin_stats['total_chatbots'])
        
        with col3:
            st.metric("Total Conversations", admin_stats['total_conversations'])
        
        # More detailed stats
        st.subheader("📈 Detailed Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Subscription Distribution:**")
            for tier, count in admin_stats.get('subscription_distribution', {}).items():
                st.write(f"- {tier}: {count}")
        
        with col2:
            st.write("**Provider Distribution:**")
            for provider, count in admin_stats.get('provider_distribution', {}).items():
                st.write(f"- {provider}: {count}")
    
    except Exception as e:
        st.error(f"Failed to load statistics: {str(e)}")

if __name__ == "__main__":
    main()