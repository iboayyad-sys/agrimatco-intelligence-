"""Authentication API endpoints."""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    decode_token,
)
from app.core.exceptions import UnauthorizedError, ConflictError
from app.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    SuccessResponse,
)

router = APIRouter()


@router.post("/register", response_model=SuccessResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ConflictError(detail="User with this email already exists")

    # Create new user
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role,
        country=user_data.country,
        region=user_data.region,
        phone=user_data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return SuccessResponse(
        message="User registered successfully",
        data={"user_id": user.id, "email": user.email},
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return tokens."""
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise UnauthorizedError(detail="Invalid email or password")

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise UnauthorizedError(detail="Invalid email or password")

    # Check if user is active
    if not user.is_active:
        raise UnauthorizedError(detail="User account is inactive")

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "email": user.email})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=86400,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """Refresh access token."""
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise UnauthorizedError(detail="Invalid refresh token")

    user_id = payload.get("sub")
    email = payload.get("email")

    # Create new access token
    access_token = create_access_token(data={"sub": user_id, "email": email})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=86400,
    )


@router.post("/verify-token")
async def verify_token_endpoint(token: str):
    """Verify if a token is valid."""
    payload = decode_token(token)
    if not payload:
        raise UnauthorizedError(detail="Invalid or expired token")

    return {
        "valid": True,
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
    }
