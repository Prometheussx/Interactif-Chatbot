# Deployment Guide

This guide provides step-by-step instructions for deploying the Interactif-Chatbot platform.

## Prerequisites

- Docker and Docker Compose installed
- Domain name (for production)
- SSL certificate (for production)
- AI provider API keys (OpenAI, Claude, Gemini)

## Development Deployment

### Quick Start with Docker Compose

1. **Clone the repository**:
```bash
git clone https://github.com/Prometheussx/Interactif-Chatbot.git
cd Interactif-Chatbot
```

2. **Configure environment variables**:
```bash
cp .env.example .env
nano .env  # Edit with your configuration
```

3. **Start the services**:
```bash
docker-compose up -d
```

4. **Access the application**:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Development

1. **Set up Python environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up database**:
```bash
# Start PostgreSQL and Redis with Docker
docker-compose up -d db redis

# Run migrations
alembic upgrade head
```

4. **Start development server**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development

1. **Set up Python environment**:
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Start development server**:
```bash
streamlit run app.py --server.port 8501
```

## Production Deployment

### Option 1: Docker Compose (Recommended)

1. **Prepare production environment**:
```bash
cp .env.example .env
```

2. **Configure production settings in .env**:
```env
# Database
DATABASE_URL=postgresql://user:secure_password@db:5432/chatbot_db

# Redis
REDIS_URL=redis://redis:6379

# Security
JWT_SECRET_KEY=your-very-secure-secret-key-here
ENVIRONMENT=production
DEBUG=false

# AI Provider API Keys
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GEMINI_API_KEY=your-gemini-api-key
```

3. **Create production Docker Compose file**:
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: chatbot_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@db:5432/chatbot_db
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - ENVIRONMENT=production
      - DEBUG=false
    depends_on:
      - db
      - redis
    restart: unless-stopped

  frontend:
    build: ./frontend
    environment:
      - API_BASE_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

4. **Deploy**:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Kubernetes Deployment

1. **Create Kubernetes manifests**:
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: interactif-chatbot
```

2. **Deploy to Kubernetes**:
```bash
kubectl apply -f k8s/
```

### Option 3: Cloud Platform Deployment

#### AWS ECS/Fargate

1. **Create ECS task definitions**
2. **Set up Application Load Balancer**
3. **Configure RDS for PostgreSQL**
4. **Set up ElastiCache for Redis**

#### Google Cloud Run

1. **Build and push images to Google Container Registry**
2. **Deploy services to Cloud Run**
3. **Configure Cloud SQL and Memorystore**

#### Azure Container Instances

1. **Create resource group and container registry**
2. **Deploy container instances**
3. **Configure Azure Database for PostgreSQL**

## Environment Configuration

### Required Environment Variables

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/database

# Redis Configuration
REDIS_URL=redis://host:6379

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Provider API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...

# Application Settings
ENVIRONMENT=production
DEBUG=false
PROJECT_NAME=Interactif Chatbot
API_V1_STR=/api/v1
```

### Optional Environment Variables

```env
# CORS Settings
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# File Upload Settings
MAX_UPLOAD_SIZE=10485760  # 10MB
UPLOAD_DIRECTORY=/app/uploads

# Email Configuration (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## SSL/TLS Configuration

### Using Let's Encrypt with Certbot

1. **Install Certbot**:
```bash
sudo apt-get install certbot python3-certbot-nginx
```

2. **Generate certificates**:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Configure auto-renewal**:
```bash
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Database Setup

### PostgreSQL Configuration

1. **Create database**:
```sql
CREATE DATABASE chatbot_db;
CREATE USER chatbot_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
```

2. **Run migrations**:
```bash
cd backend
alembic upgrade head
```

### Redis Configuration

1. **Configure Redis persistence**:
```conf
# redis.conf
save 900 1
save 300 10
save 60 10000
appendonly yes
```

## Monitoring and Logging

### Application Monitoring

1. **Install monitoring tools**:
```bash
# Prometheus and Grafana
docker-compose -f monitoring/docker-compose.yml up -d
```

2. **Configure alerts**:
```yaml
# alerting/rules.yml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High error rate detected
```

### Log Management

1. **Configure log rotation**:
```bash
# /etc/logrotate.d/interactif-chatbot
/var/log/interactif-chatbot/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
```

## Security Considerations

### Network Security

1. **Configure firewall**:
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **Use VPN for database access**
3. **Implement rate limiting**
4. **Regular security updates**

### Application Security

1. **Keep dependencies updated**:
```bash
pip install --upgrade -r requirements.txt
```

2. **Use secrets management**:
```bash
# AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault
```

3. **Enable HTTPS only**
4. **Implement proper authentication**
5. **Validate all inputs**

## Backup and Recovery

### Database Backup

1. **Automated backups**:
```bash
#!/bin/bash
# backup.sh
pg_dump -h localhost -U chatbot_user chatbot_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

2. **Schedule backups**:
```bash
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### Application Backup

1. **Configuration backup**
2. **User data backup**
3. **Log backup**

## Performance Optimization

### Database Optimization

1. **Index optimization**:
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_chatbot_configs_user_id ON chatbot_configs(user_id);
CREATE INDEX idx_conversations_chatbot_id ON conversations(chatbot_id);
```

2. **Query optimization**
3. **Connection pooling**

### Application Optimization

1. **Redis caching**
2. **CDN for static assets**
3. **Load balancing**
4. **Horizontal scaling**

## Troubleshooting

### Common Issues

1. **Database connection errors**:
```bash
# Check database status
docker-compose ps db
docker-compose logs db
```

2. **Redis connection errors**:
```bash
# Check Redis status
docker-compose ps redis
redis-cli ping
```

3. **Application errors**:
```bash
# Check application logs
docker-compose logs backend
docker-compose logs frontend
```

### Debug Mode

1. **Enable debug logging**:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

2. **Use development server**:
```bash
uvicorn app.main:app --reload --log-level debug
```

## Maintenance

### Regular Tasks

1. **Update dependencies**
2. **Monitor disk usage**
3. **Check log files**
4. **Review security settings**
5. **Test backup/restore procedures**

### Scaling

1. **Horizontal scaling**:
```yaml
# docker-compose.yml
backend:
  deploy:
    replicas: 3
```

2. **Load balancing**:
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

## Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Open an issue on GitHub
4. Contact support team

## Next Steps

After successful deployment:
1. Set up monitoring and alerting
2. Configure backup procedures
3. Test all functionality
4. Train users on the platform
5. Plan for scaling and updates