# Interactif-Chatbot

A Python full-stack chatbot platform that provides customizable AI chatbot solutions for businesses. Built with FastAPI backend and Streamlit frontend.

## Features

- **Multi-Provider AI Support**: OpenAI, Claude (Anthropic), Google Gemini
- **Customizable Chatbots**: Configure system prompts, parameters, and behavior
- **RAG (Retrieval-Augmented Generation)**: Document-based knowledge integration
- **Real-time Chat Interface**: Built-in testing and interaction tools
- **API Integration**: RESTful API for external application integration
- **User Management**: Authentication, authorization, and user profiles
- **Analytics Dashboard**: Conversation metrics and performance tracking
- **Admin Panel**: System-wide monitoring and management

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **PostgreSQL**: Primary database
- **Redis**: Session and caching
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **JWT**: Authentication tokens
- **Pydantic**: Data validation

### Frontend
- **Streamlit**: Python web framework
- **Plotly**: Interactive charts and analytics
- **Requests**: API client communication

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Prometheussx/Interactif-Chatbot.git
cd Interactif-Chatbot
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. Start the application:
```bash
docker-compose up -d
```

### Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Project Structure

```
interactif-chatbot/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utility functions
│   ├── alembic/               # Database migrations
│   └── requirements.txt
├── frontend/                   # Streamlit frontend application
│   ├── pages/                 # Application pages
│   ├── components/            # Reusable components
│   ├── utils/                 # Utility functions
│   └── requirements.txt
├── docker-compose.yml          # Docker services configuration
└── README.md
```

## Development

### Local Development Setup

1. **Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Database Setup**:
```bash
# Run migrations
alembic upgrade head
```

3. **Start Backend**:
```bash
uvicorn app.main:app --reload
```

4. **Frontend Setup**:
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

5. **Start Frontend**:
```bash
streamlit run app.py
```

### API Usage

#### Authentication
```python
import requests

# Register a new user
response = requests.post("http://localhost:8000/api/v1/auth/register", json={
    "email": "user@example.com",
    "username": "username",
    "password": "password123"
})

# Login
response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "email": "user@example.com",
    "password": "password123"
})
token = response.json()["access_token"]
```

#### Chat with AI
```python
# Send chat message
headers = {"Authorization": f"Bearer {api_token}"}
response = requests.post("http://localhost:8000/api/v1/chat/", 
    json={
        "message": "Hello, how are you?",
        "user_identifier": "user123"
    },
    headers=headers
)
print(response.json()["response"])
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-secret-key-change-this-in-production

# AI Provider API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GEMINI_API_KEY=your-gemini-api-key
```

### Chatbot Configuration

When creating a chatbot, you can configure:

- **AI Provider**: OpenAI, Claude, or Gemini
- **Model**: Specific model within the provider
- **Temperature**: Response randomness (0.0-2.0)
- **Max Tokens**: Maximum response length
- **System Prompt**: Personality and behavior instructions
- **RAG**: Document-based knowledge integration
- **Features**: Voice, image, and internet access

## Deployment

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

2. Access logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Production Considerations

- Change default passwords and secrets
- Configure proper SSL/TLS certificates
- Set up monitoring and logging
- Configure backup strategies
- Implement proper rate limiting
- Set up health checks

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the maintainers.

## Roadmap

- [ ] Multi-language support
- [ ] Advanced RAG with vector databases
- [ ] Voice input/output capabilities
- [ ] Image processing and analysis
- [ ] Workflow automation
- [ ] Enterprise features
- [ ] Mobile application
- [ ] Third-party integrations

## Acknowledgments

- FastAPI for the excellent web framework
- Streamlit for the intuitive frontend framework
- OpenAI, Anthropic, and Google for AI provider APIs
- The open-source community for various libraries and tools