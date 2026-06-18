#!/usr/bin/env bash
set -e

echo "Creating superuser..."

if [ -z "$ADMIN_EMAIL" ]; then
  ADMIN_EMAIL="admin@agrimatco.com"
fi

if [ -z "$ADMIN_PASSWORD" ]; then
  ADMIN_PASSWORD="admin123456"
fi

if [ -z "$ADMIN_NAME" ]; then
  ADMIN_NAME="Administrator"
fi

echo "Creating admin user with email: $ADMIN_EMAIL"

# Using Python to create user
python -c "
import os
os.environ.setdefault('DATABASE_URL', '$DATABASE_URL')

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import User, Base
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()
existing_user = db.query(User).filter(User.email == '$ADMIN_EMAIL').first()

if not existing_user:
    user = User(
        email='$ADMIN_EMAIL',
        full_name='$ADMIN_NAME',
        hashed_password=hash_password('$ADMIN_PASSWORD'),
        role='admin',
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    print(f'Admin user created successfully with email: $ADMIN_EMAIL')
else:
    print(f'Admin user already exists with email: $ADMIN_EMAIL')

db.close()
"
