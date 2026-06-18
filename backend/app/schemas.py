"""Pydantic schemas for API requests and responses."""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


# ============== User Schemas ==============

class UserRole(str, Enum):
    """User roles."""
    ADMIN = "admin"
    AGRONOMIST = "agronomist"
    SALES_REPRESENTATIVE = "sales_representative"
    FARMER = "farmer"


class UserCreate(BaseModel):
    """User creation schema."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    role: UserRole = UserRole.FARMER
    country: Optional[str] = None
    region: Optional[str] = None
    phone: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    email: str
    full_name: str
    role: UserRole
    country: Optional[str] = None
    region: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# ============== Crop & Disease Schemas ==============

class CropResponse(BaseModel):
    """Crop response schema."""
    id: int
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    scientific_name: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class DiseaseResponse(BaseModel):
    """Disease response schema."""
    id: int
    name: str
    name_ar: Optional[str] = None
    description: str
    symptoms: List[str]
    causes: List[str]
    severity_level: str
    crop_id: int

    class Config:
        from_attributes = True


class GrowthStageResponse(BaseModel):
    """Growth stage response schema."""
    id: int
    name: str
    name_ar: Optional[str] = None
    days_from_planting: int
    description: Optional[str] = None
    crop_id: int

    class Config:
        from_attributes = True


# ============== Product Schemas ==============

class ProductResponse(BaseModel):
    """Product response schema."""
    id: int
    name: str
    name_ar: Optional[str] = None
    category: str
    description: str
    active_ingredient: str
    concentration: str
    dosage: str
    safety_info: str
    pre_harvest_interval: Optional[int] = None
    brochure_url: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    stock_available: int
    price: Optional[float] = None

    class Config:
        from_attributes = True


# ============== Diagnosis Schemas ==============

class DiagnosisStatus(str, Enum):
    """Diagnosis status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DiagnosisCreate(BaseModel):
    """Diagnosis creation schema."""
    crop_type: str
    country: str
    region: str
    plant_age_days: Optional[int] = None
    growth_stage: Optional[str] = None
    irrigation_method: Optional[str] = None
    greenhouse: bool = False


class DiagnosisResponse(BaseModel):
    """Diagnosis response schema."""
    id: int
    user_id: int
    image_url: str
    crop_type: str
    country: str
    region: str
    status: DiagnosisStatus
    detected_problem: str
    symptoms_observed: List[str]
    possible_causes: List[str]
    confidence_score: float
    diagnosis_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Recommendation Schemas ==============

class RecommendationResponse(BaseModel):
    """Recommendation response schema."""
    id: int
    diagnosis_id: int
    product_id: int
    recommendation_type: str
    reason: str
    application_program: Optional[List[dict]] = None
    product: ProductResponse

    class Config:
        from_attributes = True


class DiagnosisDetailResponse(BaseModel):
    """Detailed diagnosis response with recommendations."""
    id: int
    user_id: int
    image_url: str
    crop_type: str
    country: str
    region: str
    status: DiagnosisStatus
    detected_problem: str
    symptoms_observed: List[str]
    possible_causes: List[str]
    confidence_score: float
    diagnosis_notes: Optional[str] = None
    recommendations: List[RecommendationResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Chat Schemas ==============

class ChatMessageCreate(BaseModel):
    """Chat message creation schema."""
    content: str
    diagnosis_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Chat message response schema."""
    id: int
    user_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============== Quotation Request Schemas ==============

class QuotationRequestCreate(BaseModel):
    """Quotation request creation schema."""
    message: str


class QuotationRequestResponse(BaseModel):
    """Quotation request response schema."""
    id: int
    user_id: int
    message: str
    status: str
    sales_rep_assigned: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============== Pagination Schemas ==============

class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel):
    """Paginated response schema."""
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


# ============== API Response Schemas ==============

class SuccessResponse(BaseModel):
    """Success response schema."""
    status: str = "success"
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    status: str = "error"
    message: str
    error_code: str
