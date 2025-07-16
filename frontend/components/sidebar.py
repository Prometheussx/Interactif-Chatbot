import streamlit as st
from utils.helpers import logout

def render_sidebar():
    """Render the main sidebar"""
    with st.sidebar:
        st.title("🤖 Interactif Chatbot")
        
        if st.session_state.authenticated:
            st.write(f"Welcome, {st.session_state.user_data.get('username', 'User')}!")
            st.write(f"Company: {st.session_state.user_data.get('company_name', 'N/A')}")
            st.write(f"Tier: {st.session_state.user_data.get('subscription_tier', 'free')}")
            
            st.divider()
            
            # Navigation
            st.subheader("Navigation")
            
            # Dashboard
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
            
            # Chatbot Management
            if st.button("🤖 My Chatbots", use_container_width=True):
                st.session_state.current_page = "chatbots"
                st.rerun()
            
            # Chat Test
            if st.button("💬 Test Chat", use_container_width=True):
                st.session_state.current_page = "chat_test"
                st.rerun()
            
            # Analytics
            if st.button("📈 Analytics", use_container_width=True):
                st.session_state.current_page = "analytics"
                st.rerun()
            
            # Admin (if user is admin)
            if st.session_state.user_data.get('subscription_tier') == 'admin':
                if st.button("⚙️ Admin", use_container_width=True):
                    st.session_state.current_page = "admin"
                    st.rerun()
            
            st.divider()
            
            # Logout
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        
        else:
            st.write("Please log in to access the application.")
            
            st.divider()
            
            # Login/Register buttons
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
            
            if st.button("📝 Register", use_container_width=True):
                st.session_state.current_page = "register"
                st.rerun()
        
        st.divider()
        
        # App info
        st.subheader("About")
        st.write("Interactif Chatbot v1.0")
        st.write("Customizable AI chatbot solutions for businesses")
        
        # API Documentation
        st.subheader("Resources")
        st.markdown("[API Documentation](http://localhost:8000/docs)")
        st.markdown("[GitHub Repository](https://github.com/Prometheussx/Interactif-Chatbot)")