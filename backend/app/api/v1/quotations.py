"""Quotation request API endpoints."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import QuotationRequest, User
from app.core.exceptions import NotFoundError
from app.schemas import QuotationRequestCreate, QuotationRequestResponse, SuccessResponse

router = APIRouter()


@router.post("/request", response_model=SuccessResponse)
async def create_quotation_request(
    request_data: QuotationRequestCreate,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Create a quotation request."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError(resource="User")

    quotation = QuotationRequest(
        user_id=user_id,
        message=request_data.message,
        status="pending",
    )
    db.add(quotation)
    db.commit()
    db.refresh(quotation)

    return SuccessResponse(
        message="Quotation request created successfully",
        data={"quotation_id": quotation.id},
    )


@router.get("/", response_model=List[QuotationRequestResponse])
async def list_quotation_requests(
    user_id: int = Query(None),
    status: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List quotation requests."""
    query = db.query(QuotationRequest)

    if user_id:
        query = query.filter(QuotationRequest.user_id == user_id)
    if status:
        query = query.filter(QuotationRequest.status == status)

    requests = query.offset(skip).limit(limit).order_by(
        QuotationRequest.created_at.desc()
    ).all()
    return requests


@router.get("/{quotation_id}", response_model=QuotationRequestResponse)
async def get_quotation_request(quotation_id: int, db: Session = Depends(get_db)):
    """Get quotation request by ID."""
    quotation = db.query(QuotationRequest).filter(
        QuotationRequest.id == quotation_id
    ).first()
    if not quotation:
        raise NotFoundError(resource="Quotation Request")
    return quotation
