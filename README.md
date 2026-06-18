# Agrimatco Smart Crop Advisor

An AI-powered agricultural assistant that analyzes crop images and provides agronomic diagnoses with personalized product recommendations from the Agrimatco product portfolio.

## Project Overview

The Agrimatco Smart Crop Advisor is a comprehensive web application designed to help farmers, agronomists, and sales representatives make informed decisions about crop health and treatment options. The platform leverages AI vision models to analyze plant health and provides intelligent product recommendations from the Agrimatco product database.

## Core Features

- 🖼️ **Image Analysis**: Upload and analyze crop, leaf, fruit, stem, root, and soil images
- 🤖 **AI Diagnosis Engine**: Powered by GPT-4 Vision for accurate disease and pest detection
- 📋 **Agronomic Questionnaire**: Contextual information collection for precise recommendations
- 💊 **Product Recommendation**: Intelligent matching of Agrimatco products to detected issues
- 💬 **AI Chat Assistant**: Interactive Q&A about crop health and product usage
- 📊 **Admin Dashboard**: Comprehensive management and analytics
- 📄 **PDF Reports**: Generate downloadable diagnosis and recommendation reports
- 🌍 **Multi-language Support**: Arabic and English interfaces
- 🎨 **Dark Mode**: Professional dark theme support

## Tech Stack

### Frontend
- **Next.js 15**: React framework with SSR/SSG capabilities
- **React 19**: UI component library
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe development
- **Zustand**: State management
- **React Hook Form**: Form handling
- **Zod**: Schema validation
- **Next-intl**: Internationalization (i18n)

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and settings management
- **JWT**: Authentication and authorization
- **OpenAI API**: Vision and language models
- **Langchain**: RAG implementation
- **Redis**: Caching and session management

### Database
- **PostgreSQL**: Primary relational database
- **pgvector**: Vector operations for embeddings
- **Pinecone/Weaviate**: Vector database for RAG

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Azure/AWS/DigitalOcean**: Cloud deployment targets

## Project Structure

```
agrimatco-intelligence/
├── frontend/                      # Next.js frontend application
│   ├── app/                      # Next.js app directory
│   ├── components/               # Reusable React components
│   ├── hooks/                    # Custom React hooks
│   ├── lib/                      # Utilities and helpers
│   ├── public/                   # Static assets
│   ├── styles/                   # Global styles
│   └── middleware.ts             # Next.js middleware
├── backend/                      # FastAPI backend application
│   ├── app/                      # Application core
│   ├── api/                      # API routes
│   ├── models/                   # SQLAlchemy models
│   ├── schemas/                  # Pydantic schemas
│   ├── services/                 # Business logic
│   ├── utils/                    # Helper functions
│   └── config.py                 # Configuration
├── database/                     # Database schemas and migrations
│   ├── migrations/               # Alembic migrations
│   └── seeds/                    # Initial data
├── docker/                       # Docker configuration
├── docs/                         # Documentation
├── .env.example                  # Environment variables template
└── docker-compose.yml            # Multi-container setup
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/iboayyad-sys/agrimatco-intelligence-.git
   cd agrimatco-intelligence
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Manual Setup - Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m alembic upgrade head
   uvicorn app.main:app --reload
   ```

5. **Manual Setup - Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## API Documentation

- Backend API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## User Roles

- **Admin**: Full system access, user management, product management
- **Agronomist**: Image analysis, diagnosis creation, report generation
- **Sales Representative**: Product recommendations, customer quotes, sales tracking
- **Farmer**: Image upload, diagnosis retrieval, product information

## Authentication

The application uses JWT-based authentication with role-based access control (RBAC). All API endpoints require valid JWT tokens except for public endpoints.

## Deployment

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment
See `docs/DEPLOYMENT.md` for detailed instructions for Azure, AWS, and DigitalOcean.

## Configuration

All configuration is managed through environment variables. See `.env.example` for all available options.

## Database Schema

See `database/schema.sql` for complete database structure.

## API Endpoints

See `docs/API.md` for comprehensive API documentation.

## Development

### Frontend Development
```bash
cd frontend
npm run dev
# Available at http://localhost:3000
```

### Backend Development
```bash
cd backend
uv icorn app.main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Contributing

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open a Pull Request

## Code Standards

- Backend: PEP 8, type hints, docstrings
- Frontend: ESLint, Prettier, TypeScript strict mode
- Database: Named migrations, seed data

## Security

- JWT token-based authentication
- Role-based access control
- Input validation and sanitization
- HTTPS required in production
- Secure password hashing (bcrypt)
- Environment variable protection
- CORS configuration
- Rate limiting

## Performance

- Caching with Redis
- Database query optimization
- Image compression
- CDN for static assets
- API response pagination
- Database indexing

## License

All rights reserved - Agrimatco

## Support

For support, please contact: support@agrimatco.com

## Roadmap

- [ ] Mobile native apps (iOS/Android)
- [ ] Offline mode support
- [ ] Advanced analytics
- [ ] IoT sensor integration
- [ ] Weather API integration
- [ ] Blockchain for product verification
- [ ] ML model training pipeline

---

**Made with ❤️ for agriculture**
