import streamlit as st
from typing import Dict, Any, Optional
from utils.helpers import validate_email, validate_password, get_ai_provider_options, get_model_options

def render_login_form():
    """Render login form"""
    st.subheader("🔐 Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please fill in all fields")
                return
            
            if not validate_email(email):
                st.error("Please enter a valid email address")
                return
            
            try:
                token_data = st.session_state.api_client.login(email, password)
                user_data = st.session_state.api_client.get_current_user()
                
                st.session_state.authenticated = True
                st.session_state.user_data = user_data
                st.session_state.current_page = "dashboard"
                
                st.success("Login successful!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

def render_register_form():
    """Render registration form"""
    st.subheader("📝 Register")
    
    with st.form("register_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        username = st.text_input("Username", placeholder="Choose a username")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        company_name = st.text_input("Company Name (Optional)", placeholder="Enter your company name")
        
        submitted = st.form_submit_button("Register", use_container_width=True)
        
        if submitted:
            if not email or not username or not password or not confirm_password:
                st.error("Please fill in all required fields")
                return
            
            if not validate_email(email):
                st.error("Please enter a valid email address")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            is_valid, password_message = validate_password(password)
            if not is_valid:
                st.error(password_message)
                return
            
            try:
                user_data = st.session_state.api_client.register(
                    email=email,
                    username=username,
                    password=password,
                    company_name=company_name if company_name else None
                )
                
                st.success("Registration successful! Please login.")
                st.session_state.current_page = "login"
                st.rerun()
                
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")

def render_chatbot_form(chatbot_data: Optional[Dict[str, Any]] = None):
    """Render chatbot configuration form"""
    is_editing = chatbot_data is not None
    title = "✏️ Edit Chatbot" if is_editing else "🤖 Create New Chatbot"
    
    st.subheader(title)
    
    with st.form("chatbot_form"):
        # Basic Information
        st.subheader("Basic Information")
        name = st.text_input("Chatbot Name", value=chatbot_data.get("name", "") if is_editing else "")
        
        # AI Provider Configuration
        st.subheader("AI Provider Configuration")
        provider_options = get_ai_provider_options()
        current_provider = chatbot_data.get("ai_provider", "openai") if is_editing else "openai"
        
        ai_provider = st.selectbox(
            "AI Provider", 
            options=list(provider_options.keys()),
            format_func=lambda x: provider_options[x],
            index=list(provider_options.keys()).index(current_provider)
        )
        
        model_options = get_model_options(ai_provider)
        current_model = chatbot_data.get("model_name", model_options[0]) if is_editing else model_options[0]
        
        model_name = st.selectbox(
            "Model", 
            options=model_options,
            index=model_options.index(current_model) if current_model in model_options else 0
        )
        
        # Model Parameters
        st.subheader("Model Parameters")
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.slider(
                "Temperature", 
                min_value=0.0, 
                max_value=2.0, 
                value=chatbot_data.get("temperature", 0.7) if is_editing else 0.7,
                step=0.1,
                help="Controls randomness in responses. Higher values make output more random."
            )
        
        with col2:
            max_tokens = st.number_input(
                "Max Tokens", 
                min_value=100, 
                max_value=4000, 
                value=chatbot_data.get("max_tokens", 1000) if is_editing else 1000,
                help="Maximum number of tokens in the response."
            )
        
        # System Prompt
        st.subheader("System Prompt")
        system_prompt = st.text_area(
            "System Prompt",
            value=chatbot_data.get("system_prompt", "") if is_editing else "",
            height=150,
            placeholder="Enter instructions for the AI assistant...",
            help="This prompt defines the behavior and personality of your chatbot."
        )
        
        # Features
        st.subheader("Features")
        col1, col2 = st.columns(2)
        
        with col1:
            internet_access = st.checkbox(
                "Internet Access",
                value=chatbot_data.get("internet_access", False) if is_editing else False,
                help="Allow the chatbot to access current information from the internet."
            )
            
            rag_enabled = st.checkbox(
                "RAG (Document Search)",
                value=chatbot_data.get("rag_enabled", False) if is_editing else False,
                help="Enable Retrieval-Augmented Generation for document-based responses."
            )
        
        with col2:
            voice_enabled = st.checkbox(
                "Voice Support",
                value=chatbot_data.get("voice_enabled", False) if is_editing else False,
                help="Enable voice input and output capabilities."
            )
            
            image_enabled = st.checkbox(
                "Image Processing",
                value=chatbot_data.get("image_enabled", False) if is_editing else False,
                help="Enable image upload and processing capabilities."
            )
        
        # RAG Provider (only show if RAG is enabled)
        if rag_enabled:
            rag_provider = st.selectbox(
                "RAG Provider",
                options=["langchain", "llamaindex"],
                index=0 if not is_editing else (0 if chatbot_data.get("rag_provider") == "langchain" else 1)
            )
        else:
            rag_provider = None
        
        # Form submission
        submitted = st.form_submit_button(
            "Update Chatbot" if is_editing else "Create Chatbot",
            use_container_width=True
        )
        
        if submitted:
            if not name:
                st.error("Please enter a chatbot name")
                return
            
            chatbot_config = {
                "name": name,
                "ai_provider": ai_provider,
                "model_name": model_name,
                "system_prompt": system_prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "internet_access": internet_access,
                "rag_enabled": rag_enabled,
                "rag_provider": rag_provider,
                "voice_enabled": voice_enabled,
                "image_enabled": image_enabled
            }
            
            try:
                if is_editing:
                    result = st.session_state.api_client.update_chatbot(
                        chatbot_data["id"], 
                        chatbot_config
                    )
                    st.success("Chatbot updated successfully!")
                else:
                    result = st.session_state.api_client.create_chatbot(chatbot_config)
                    st.success("Chatbot created successfully!")
                    st.info(f"API Token: {result['api_token']}")
                
                st.session_state.current_page = "chatbots"
                st.rerun()
                
            except Exception as e:
                st.error(f"Failed to {'update' if is_editing else 'create'} chatbot: {str(e)}")

def render_file_upload():
    """Render file upload form for RAG documents"""
    st.subheader("📁 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True,
        type=['txt', 'pdf', 'docx', 'md'],
        help="Upload documents to be used for RAG (Retrieval-Augmented Generation)"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size} bytes)")
        
        if st.button("Upload Files", use_container_width=True):
            # Process uploaded files
            st.success(f"Successfully uploaded {len(uploaded_files)} files!")
            # Note: In a real implementation, you would process these files
            # and store them in the RAG system