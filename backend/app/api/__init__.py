"""API v1 routes."""
from fastapi import APIRouter

from app.api.v1 import auth, crops, diagnoses, products, users, chat, quotations

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(crops.router, prefix="/crops", tags=["Crops"])
api_router.include_router(diagnoses.router, prefix="/diagnoses", tags=["Diagnoses"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(quotations.router, prefix="/quotations", tags=["Quotations"])
