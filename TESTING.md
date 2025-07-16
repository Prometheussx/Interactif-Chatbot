# Testing Guide

This guide explains how to test the Interactif-Chatbot platform.

## Quick Testing with Docker

### 1. Start the Application
```bash
# Clone the repository
git clone https://github.com/Prometheussx/Interactif-Chatbot.git
cd Interactif-Chatbot

# Set up environment
cp .env.example .env
# Edit .env with your API keys (at minimum, add an OpenAI API key)

# Start services
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
docker-compose logs -f backend | grep "Application startup complete"
```

### 2. Test the Backend API

#### Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

#### API Documentation
Open: http://localhost:8000/docs

#### Register a User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123",
    "company_name": "Test Company"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
# Save the access_token from response
```

### 3. Test the Frontend Application

#### Access the Application
Open: http://localhost:8501

#### Test User Registration
1. Click "Register" tab
2. Fill in:
   - Email: test@example.com
   - Username: testuser
   - Password: TestPassword123
   - Confirm Password: TestPassword123
   - Company Name: Test Company
3. Click "Register"
4. Should see success message

#### Test User Login
1. Click "Login" tab
2. Fill in:
   - Email: test@example.com
   - Password: TestPassword123
3. Click "Login"
4. Should redirect to dashboard

#### Test Chatbot Creation
1. Navigate to "My Chatbots"
2. Click "Create New" tab
3. Fill in:
   - Name: Test Chatbot
   - AI Provider: OpenAI
   - Model: gpt-3.5-turbo
   - System Prompt: You are a helpful assistant.
4. Click "Create Chatbot"
5. Should see success message and API token

#### Test Chat Functionality
1. Go to "Test Chat"
2. Select your created chatbot
3. Type: "Hello, how are you?"
4. Should receive AI response

## Manual Testing Checklist

### Authentication Tests
- [ ] User registration works
- [ ] User login works
- [ ] Invalid credentials rejected
- [ ] JWT token authentication works
- [ ] Protected routes require authentication

### Chatbot Management Tests
- [ ] Create chatbot works
- [ ] Edit chatbot works
- [ ] Delete chatbot works
- [ ] List chatbots works
- [ ] API token generation works
- [ ] API token regeneration works

### Chat Functionality Tests
- [ ] Send message works
- [ ] Receive AI response works
- [ ] Conversation history maintained
- [ ] Multiple conversations supported
- [ ] Different AI providers work

### Frontend Interface Tests
- [ ] All pages load correctly
- [ ] Navigation works
- [ ] Forms submit properly
- [ ] Error messages display
- [ ] Success messages display
- [ ] Responsive design works

### API Integration Tests
- [ ] All endpoints respond correctly
- [ ] Error handling works
- [ ] Rate limiting works (if configured)
- [ ] Authentication required for protected endpoints

## Automated Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
python -m pytest tests/ -v
```

### Integration Tests
```bash
# Run full integration test suite
python -m pytest integration_tests/ -v
```

## Performance Testing

### Load Testing with Apache Bench
```bash
# Test registration endpoint
ab -n 100 -c 10 -H "Content-Type: application/json" \
  -p registration_data.json \
  http://localhost:8000/api/v1/auth/register

# Test chat endpoint
ab -n 100 -c 10 -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -p chat_data.json \
  http://localhost:8000/api/v1/chat/
```

### Stress Testing
```bash
# Install stress testing tool
pip install locust

# Run stress tests
locust -f tests/stress_tests.py --host=http://localhost:8000
```

## Common Issues and Solutions

### Database Connection Issues
```bash
# Check database status
docker-compose ps db

# View database logs
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up -d
```

### Redis Connection Issues
```bash
# Check Redis status
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

### API Key Issues
```bash
# Check environment variables
docker-compose exec backend env | grep API_KEY

# Test API key validity
curl -H "Authorization: Bearer sk-..." https://api.openai.com/v1/models
```

### Frontend Issues
```bash
# Check frontend logs
docker-compose logs frontend

# Access frontend container
docker-compose exec frontend bash
```

## Test Data

### Sample User Data
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "TestPassword123",
  "company_name": "Test Company"
}
```

### Sample Chatbot Configuration
```json
{
  "name": "Test Chatbot",
  "ai_provider": "openai",
  "model_name": "gpt-3.5-turbo",
  "system_prompt": "You are a helpful assistant.",
  "temperature": 0.7,
  "max_tokens": 1000,
  "internet_access": false,
  "rag_enabled": false,
  "voice_enabled": false,
  "image_enabled": false
}
```

### Sample Chat Message
```json
{
  "message": "Hello, how are you?",
  "user_identifier": "test_user",
  "conversation_id": null
}
```

## Expected Responses

### Successful Registration
```json
{
  "id": 1,
  "email": "test@example.com",
  "username": "testuser",
  "company_name": "Test Company",
  "subscription_tier": "free",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### Successful Login
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Successful Chat Response
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "conversation_id": 1,
  "message_id": null
}
```

## Troubleshooting

### Check Service Status
```bash
# Check all services
docker-compose ps

# Check specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
docker-compose logs redis
```

### Debug Mode
```bash
# Enable debug mode
export DEBUG=true

# Start with debug logging
docker-compose up --build
```

### Reset Everything
```bash
# Complete reset
docker-compose down -v
docker system prune -a
docker-compose up --build
```

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs [service]`
2. Verify environment variables
3. Check API key validity
4. Ensure all services are running
5. Check network connectivity
6. Review error messages carefully

For persistent issues, open an issue on GitHub with:
- Error messages
- Log outputs
- Steps to reproduce
- Environment details