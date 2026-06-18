"""User API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.core.exceptions import NotFoundError
from app.schemas import UserResponse, SuccessResponse, PaginatedResponse

router = APIRouter()


def get_current_user(token: str, db: Session) -> User:
    """Get current authenticated user."""
    from app.core.security import decode_token

    payload = decode_token(token)
    if not payload:
        raise NotFoundError(resource="User")

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError(resource="User")

    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    authorization: str,
    db: Session = Depends(get_db),
):
    """Get current user information."""
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    return user


@router.get("/", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all users (Admin only)."""
    query = db.query(User)
    total = query.count()

    users = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        items=[UserResponse.from_orm(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError(resource="User")

    return user
