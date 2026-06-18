# Agrimatco Smart Crop Advisor - Backend

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 6+ (optional)

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:
```bash
bash scripts/migrate.sh
```

5. Seed database (optional):
```bash
bash scripts/seed.sh
```

6. Create superuser:
```bash
bash scripts/create-superuser.sh
```

7. Run development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

Alembic is used for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Migration description"

# Apply migrations
alembic upgrade head

# Revert to previous migration
alembic downgrade -1
```

## Testing

```bash
pytest
pytest --cov=app  # With coverage
```
