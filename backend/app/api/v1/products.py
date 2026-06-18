"""Product API endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.core.exceptions import NotFoundError
from app.schemas import ProductResponse

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    category: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all active products."""
    query = db.query(Product).filter(Product.is_active == True)

    if category:
        query = query.filter(Product.category == category)

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundError(resource="Product")
    return product


@router.get("/search/", response_model=List[ProductResponse])
async def search_products(
    query: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search products by name or ingredient."""
    search_term = f"%{query}%"
    products = db.query(Product).filter(
        Product.is_active == True,
        (Product.name.ilike(search_term) | Product.active_ingredient.ilike(search_term)),
    ).offset(skip).limit(limit).all()
    return products
