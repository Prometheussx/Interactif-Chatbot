import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random
from utils.helpers import show_error, show_info

def render_analytics():
    """Render analytics page"""
    st.title("📈 Analytics")
    
    # Check if user is admin for system-wide analytics
    is_admin = st.session_state.user_data.get('subscription_tier') == 'admin'
    
    if is_admin:
        tab1, tab2 = st.tabs(["📊 My Analytics", "🏢 System Analytics"])
        
        with tab1:
            render_user_analytics()
        
        with tab2:
            render_admin_analytics()
    else:
        render_user_analytics()

def render_user_analytics():
    """Render user-specific analytics"""
    st.subheader("📊 Your Chatbot Analytics")
    
    try:
        chatbots_data = st.session_state.api_client.get_chatbots()
        chatbots = chatbots_data.get('chatbots', [])
        
        if not chatbots:
            st.info("No chatbots found. Create a chatbot to start tracking analytics.")
            return
        
        # Chatbot selector
        selected_chatbot = st.selectbox(
            "Select Chatbot",
            options=chatbots,
            format_func=lambda x: f"{x['name']} ({x['ai_provider']})"
        )
        
        st.divider()
        
        # Generate mock analytics data for demonstration
        analytics_data = generate_mock_analytics_data()
        
        # Overview metrics
        render_overview_metrics(analytics_data)
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            render_usage_chart(analytics_data)
        
        with col2:
            render_response_time_chart(analytics_data)
        
        # More detailed analytics
        st.divider()
        
        render_conversation_analytics(analytics_data)
        
        # Model performance
        st.divider()
        
        render_model_performance(selected_chatbot, analytics_data)
        
    except Exception as e:
        show_error(f"Failed to load analytics: {str(e)}")

def render_admin_analytics():
    """Render admin analytics"""
    st.subheader("🏢 System Analytics")
    
    try:
        admin_stats = st.session_state.api_client.get_admin_stats()
        
        # System overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", admin_stats['total_users'])
        
        with col2:
            st.metric("Total Chatbots", admin_stats['total_chatbots'])
        
        with col3:
            st.metric("Total Conversations", admin_stats['total_conversations'])
        
        with col4:
            avg_chatbots = admin_stats['total_chatbots'] / max(admin_stats['total_users'], 1)
            st.metric("Avg Chatbots/User", f"{avg_chatbots:.1f}")
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Subscription distribution
            subscription_data = admin_stats['subscription_distribution']
            if subscription_data:
                fig = px.pie(
                    values=list(subscription_data.values()),
                    names=list(subscription_data.keys()),
                    title="Subscription Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Provider distribution
            provider_data = admin_stats['provider_distribution']
            if provider_data:
                fig = px.bar(
                    x=list(provider_data.keys()),
                    y=list(provider_data.values()),
                    title="AI Provider Usage"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # System health metrics
        st.divider()
        render_system_health()
        
    except Exception as e:
        show_error(f"Failed to load admin analytics: {str(e)}")

def render_overview_metrics(analytics_data):
    """Render overview metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Messages", analytics_data['total_messages'])
    
    with col2:
        st.metric("Active Conversations", analytics_data['active_conversations'])
    
    with col3:
        st.metric("Avg Response Time", f"{analytics_data['avg_response_time']:.1f}s")
    
    with col4:
        st.metric("Success Rate", f"{analytics_data['success_rate']:.1f}%")

def render_usage_chart(analytics_data):
    """Render usage chart"""
    st.subheader("📊 Daily Usage")
    
    df = pd.DataFrame(analytics_data['daily_usage'])
    
    fig = px.line(
        df, 
        x='date', 
        y='messages',
        title="Daily Message Count",
        markers=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_response_time_chart(analytics_data):
    """Render response time chart"""
    st.subheader("⏱️ Response Time Trends")
    
    df = pd.DataFrame(analytics_data['response_times'])
    
    fig = px.line(
        df,
        x='timestamp',
        y='response_time',
        title="Response Time (seconds)",
        markers=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_conversation_analytics(analytics_data):
    """Render conversation analytics"""
    st.subheader("💬 Conversation Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Conversation length distribution
        lengths = analytics_data['conversation_lengths']
        fig = px.histogram(
            x=lengths,
            nbins=20,
            title="Conversation Length Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # User engagement by hour
        hourly_data = analytics_data['hourly_engagement']
        fig = px.bar(
            x=list(hourly_data.keys()),
            y=list(hourly_data.values()),
            title="Messages by Hour of Day"
        )
        st.plotly_chart(fig, use_container_width=True)

def render_model_performance(chatbot, analytics_data):
    """Render model performance metrics"""
    st.subheader("🎯 Model Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Current Model:** {chatbot['model_name']}")
        st.write(f"**Provider:** {chatbot['ai_provider']}")
        st.write(f"**Temperature:** {chatbot['temperature']}")
        st.write(f"**Max Tokens:** {chatbot['max_tokens']}")
    
    with col2:
        # Performance metrics
        performance = analytics_data['model_performance']
        st.metric("Avg Tokens/Response", performance['avg_tokens'])
        st.metric("Error Rate", f"{performance['error_rate']:.1f}%")
        st.metric("User Satisfaction", f"{performance['satisfaction']:.1f}/5")
    
    # Token usage over time
    st.subheader("📊 Token Usage")
    
    token_data = analytics_data['token_usage']
    df = pd.DataFrame(token_data)
    
    fig = px.area(
        df,
        x='date',
        y='tokens',
        title="Daily Token Usage"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_system_health():
    """Render system health metrics"""
    st.subheader("🏥 System Health")
    
    # Generate mock health data
    health_data = {
        'api_uptime': 99.9,
        'avg_response_time': 0.5,
        'error_rate': 0.1,
        'active_connections': 42
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API Uptime", f"{health_data['api_uptime']:.1f}%")
    
    with col2:
        st.metric("Avg Response Time", f"{health_data['avg_response_time']:.1f}s")
    
    with col3:
        st.metric("Error Rate", f"{health_data['error_rate']:.1f}%")
    
    with col4:
        st.metric("Active Connections", health_data['active_connections'])
    
    # Health status indicators
    st.subheader("🚦 Service Status")
    
    services = [
        ("API Server", "🟢 Healthy"),
        ("Database", "🟢 Healthy"),
        ("Redis Cache", "🟢 Healthy"),
        ("AI Providers", "🟡 Degraded"),
        ("File Storage", "🟢 Healthy")
    ]
    
    for service, status in services:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(f"**{service}:**")
        with col2:
            st.write(status)

def generate_mock_analytics_data():
    """Generate mock analytics data for demonstration"""
    # Generate dates for the last 30 days
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
    
    return {
        'total_messages': random.randint(500, 2000),
        'active_conversations': random.randint(50, 200),
        'avg_response_time': random.uniform(0.5, 2.0),
        'success_rate': random.uniform(95, 99.5),
        'daily_usage': [
            {'date': date, 'messages': random.randint(10, 100)}
            for date in dates
        ],
        'response_times': [
            {
                'timestamp': f"{date} {random.randint(0, 23):02d}:00",
                'response_time': random.uniform(0.2, 3.0)
            }
            for date in dates[-7:]  # Last 7 days
            for _ in range(random.randint(1, 5))
        ],
        'conversation_lengths': [random.randint(1, 50) for _ in range(100)],
        'hourly_engagement': {
            str(hour): random.randint(0, 50) for hour in range(24)
        },
        'model_performance': {
            'avg_tokens': random.randint(100, 500),
            'error_rate': random.uniform(0.1, 2.0),
            'satisfaction': random.uniform(4.0, 5.0)
        },
        'token_usage': [
            {'date': date, 'tokens': random.randint(1000, 10000)}
            for date in dates
        ]
    }

def render_export_analytics():
    """Render analytics export functionality"""
    st.subheader("📤 Export Analytics")
    
    export_format = st.selectbox("Export Format", ["CSV", "JSON", "PDF"])
    date_range = st.date_input("Date Range", value=[datetime.now() - timedelta(days=30), datetime.now()])
    
    if st.button("Export Analytics", use_container_width=True):
        st.success(f"Analytics exported as {export_format}!")
        # Export functionality would go here