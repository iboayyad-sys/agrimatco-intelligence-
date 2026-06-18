# Agrimatco Smart Crop Advisor - Deployment Guide

## Overview

This document provides comprehensive deployment instructions for the Agrimatco Smart Crop Advisor application.

## Architecture

The application uses a microservices architecture with the following components:

- **Frontend**: Next.js 15 application
- **Backend**: FastAPI application with Python
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Web Server**: Nginx

## Local Development Setup

### Prerequisites
- Docker & Docker Compose
- Git
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/iboayyad-sys/agrimatco-intelligence-.git
cd agrimatco-intelligence-
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start services:
```bash
docker-compose up -d
```

4. Run migrations:
```bash
docker-compose exec backend bash scripts/migrate.sh
```

5. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Production Deployment

### Prerequisites
- Docker & Docker Compose installed on server
- SSL certificates (Let's Encrypt recommended)
- Domain name configured
- Ubuntu 20.04+ LTS recommended

### Server Setup

1. Connect to your server:
```bash
ssh user@your-server-ip
```

2. Install Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

3. Install Docker Compose:
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

4. Clone repository:
```bash
git clone https://github.com/iboayyad-sys/agrimatco-intelligence-.git
cd agrimatco-intelligence-
```

### Environment Configuration

1. Create production environment file:
```bash
cp .env.production.example .env.production
```

2. Edit `.env.production` with production values:
```bash
# Database
DB_USER=agrimatco_prod
DB_PASSWORD=<secure-password>
DB_NAME=agrimatco_prod

# Redis
REDIS_PASSWORD=<secure-password>

# Application
SECRET_KEY=<generate-with-openssl-rand-hex-32>
API_URL=https://api.yourdomain.com

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=<app-password>

# Monitoring
SENTRY_DSN=<your-sentry-dsn>
```

### SSL Setup

1. Install Certbot:
```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx -y
```

2. Generate SSL certificates:
```bash
sudo certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com
```

3. Update Nginx configuration with certificate paths

### Database Migration

1. Before starting services, run migrations:
```bash
docker-compose -f docker-compose.prod.yml run --rm backend bash scripts/migrate.sh
```

2. Seed initial data (optional):
```bash
docker-compose -f docker-compose.prod.yml run --rm backend bash scripts/seed.sh
```

### Start Production Services

1. Build images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Start services:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Verify services:
```bash
docker-compose -f docker-compose.prod.yml ps
```

## Monitoring & Maintenance

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Database Backup

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U agrimatco_prod agrimatco_prod > backup-$(date +%Y%m%d).sql

# Restore backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U agrimatco_prod agrimatco_prod < backup-20240101.sql
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run migrations if needed
docker-compose -f docker-compose.prod.yml run --rm backend bash scripts/migrate.sh
```

## Health Checks

The application includes health check endpoints:

- Backend health: `GET /health`
- Database: `GET /health/db`
- Redis: `GET /health/redis`

## Scaling

### Horizontal Scaling

To run multiple backend instances:

```yaml
# In docker-compose.prod.yml
backend:
  deploy:
    replicas: 3
```

Then update Nginx configuration to load balance.

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Remove containers and start fresh
docker-compose down -v
docker-compose up -d
```

### Database connection errors
```bash
# Check PostgreSQL is running
docker-compose exec postgres psql -U agrimatco -d agrimatco_db -c "SELECT 1;"
```

### Redis connection issues
```bash
# Check Redis is running
docker-compose exec redis redis-cli ping
```

## Security Considerations

1. **Never commit `.env` files** - Use `.env.example` templates
2. **Change default passwords** - Update all default credentials
3. **Use strong secrets** - Generate with: `openssl rand -hex 32`
4. **Enable HTTPS** - Always use SSL certificates
5. **Configure firewalls** - Restrict port access
6. **Regular backups** - Automate database backups
7. **Update dependencies** - Keep Docker images updated

## Support

For issues or questions:
- GitHub Issues: https://github.com/iboayyad-sys/agrimatco-intelligence-/issues
- Documentation: https://docs.agrimatco.com
