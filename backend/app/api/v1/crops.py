"""Crop API endpoints."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Crop, Disease, GrowthStage
from app.core.exceptions import NotFoundError
from app.schemas import CropResponse, DiseaseResponse, GrowthStageResponse

router = APIRouter()


@router.get("/", response_model=List[CropResponse])
async def list_crops(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all crops."""
    crops = db.query(Crop).filter(Crop.is_active == True).offset(skip).limit(limit).all()
    return crops


@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """Get crop by ID."""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise NotFoundError(resource="Crop")
    return crop


@router.get("/{crop_id}/diseases", response_model=List[DiseaseResponse])
async def get_crop_diseases(crop_id: int, db: Session = Depends(get_db)):
    """Get diseases for a crop."""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise NotFoundError(resource="Crop")

    diseases = db.query(Disease).filter(
        Disease.crop_id == crop_id,
        Disease.is_active == True,
    ).all()
    return diseases


@router.get("/{crop_id}/growth-stages", response_model=List[GrowthStageResponse])
async def get_crop_growth_stages(crop_id: int, db: Session = Depends(get_db)):
    """Get growth stages for a crop."""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise NotFoundError(resource="Crop")

    stages = db.query(GrowthStage).filter(GrowthStage.crop_id == crop_id).all()
    return stages
