# Agrimatco Smart Crop Advisor

An AI-powered agricultural assistant for crop health diagnosis using image analysis and personalized Agrimatco product recommendations.

## 🌾 Features

- **AI-Powered Diagnosis**: Upload crop images for instant AI analysis
- **Intelligent Chat**: Discuss crop health issues with an AI assistant
- **Product Recommendations**: Get personalized Agrimatco product suggestions
- **Multi-language Support**: Available in English and Arabic
- **Quotation Requests**: Request bulk product quotations
- **User Analytics**: Track diagnosis history and recommendations

## 📋 Tech Stack

### Frontend
- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Zustand (State Management)
- React Hook Form (Form Management)

### Backend
- FastAPI (Python)
- PostgreSQL 15
- Redis 7
- SQLAlchemy ORM
- Pydantic (Validation)

### Deployment
- Docker & Docker Compose
- Nginx (Reverse Proxy)
- PostgreSQL (Database)
- Redis (Caching)

## 🚀 Quick Start

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/iboayyad-sys/agrimatco-intelligence-.git
cd agrimatco-intelligence-
```

2. **Start Services**
```bash
docker-compose up -d
```

3. **Run Migrations**
```bash
docker-compose exec backend bash scripts/migrate.sh
```

4. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive production setup instructions.

## 📁 Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── core/              # Core utilities (security, config)
│   │   └── main.py            # FastAPI app
│   ├── alembic/               # Database migrations
│   ├── scripts/               # Utility scripts
│   └── requirements.txt        # Python dependencies
├── frontend/                   # Next.js frontend
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── styles/                # Global styles
│   └── package.json           # Node dependencies
├── nginx/                      # Nginx configuration
├── docker-compose.yml          # Local development
├── docker-compose.prod.yml     # Production
└── DEPLOYMENT.md              # Deployment guide
```

## 🔐 Environment Variables

See `.env.example` for all available configuration options:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📚 API Documentation

Full API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Database

Migrations are handled with Alembic:

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is proprietary and confidential.

## 📧 Contact

- Email: info@agrimatco.com
- Website: https://www.agrimatco.com

## 🙏 Acknowledgments

- FastAPI documentation
- Next.js documentation
- PostgreSQL documentation
