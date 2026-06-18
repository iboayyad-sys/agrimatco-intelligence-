"""Diagnosis API endpoints."""
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Diagnosis, DiagnosisStatus
from app.core.exceptions import NotFoundError
from app.schemas import (
    DiagnosisCreate,
    DiagnosisResponse,
    DiagnosisDetailResponse,
    SuccessResponse,
)

router = APIRouter()


@router.post("/analyze", response_model=SuccessResponse)
async def create_diagnosis(
    crop_type: str = Form(...),
    country: str = Form(...),
    region: str = Form(...),
    plant_age_days: int = Form(None),
    growth_stage: str = Form(None),
    irrigation_method: str = Form(None),
    greenhouse: bool = Form(False),
    image: UploadFile = File(...),
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Upload image and create diagnosis."""
    diagnosis = Diagnosis(
        user_id=user_id,
        crop_type=crop_type,
        country=country,
        region=region,
        plant_age_days=plant_age_days,
        growth_stage=growth_stage,
        irrigation_method=irrigation_method,
        greenhouse=greenhouse,
        image_url="/uploads/placeholder.jpg",
        status=DiagnosisStatus.PENDING,
        detected_problem="",
        symptoms_observed=[],
        possible_causes=[],
        confidence_score=0.0,
    )

    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    return SuccessResponse(
        message="Diagnosis created successfully",
        data={"diagnosis_id": diagnosis.id},
    )


@router.get("/", response_model=List[DiagnosisResponse])
async def list_diagnoses(
    user_id: int = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List diagnoses for a user."""
    diagnoses = db.query(Diagnosis).filter(
        Diagnosis.user_id == user_id,
    ).offset(skip).limit(limit).order_by(Diagnosis.created_at.desc()).all()
    return diagnoses


@router.get("/{diagnosis_id}", response_model=DiagnosisDetailResponse)
async def get_diagnosis(diagnosis_id: int, db: Session = Depends(get_db)):
    """Get diagnosis with details and recommendations."""
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not diagnosis:
        raise NotFoundError(resource="Diagnosis")
    return diagnosis
