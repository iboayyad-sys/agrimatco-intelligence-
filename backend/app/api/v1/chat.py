"""Chat API endpoints."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChatMessage, User
from app.core.exceptions import NotFoundError
from app.schemas import ChatMessageCreate, ChatMessageResponse, SuccessResponse

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    message_data: ChatMessageCreate,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Send a chat message."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError(resource="User")

    user_message = ChatMessage(
        user_id=user_id,
        diagnosis_id=message_data.diagnosis_id,
        role="user",
        content=message_data.content,
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    return ChatMessageResponse(
        id=user_message.id,
        user_id=user_message.user_id,
        role=user_message.role,
        content=user_message.content,
        created_at=user_message.created_at,
    )


@router.get("/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    user_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get chat messages for a user."""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id,
    ).offset(skip).limit(limit).order_by(ChatMessage.created_at.asc()).all()
    return messages
