"""Database models for Agrimatco Smart Crop Advisor."""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserRole(str, Enum):
    """User roles."""
    ADMIN = "admin"
    AGRONOMIST = "agronomist"
    SALES_REPRESENTATIVE = "sales_representative"
    FARMER = "farmer"


class DiagnosisStatus(str, Enum):
    """Diagnosis status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.FARMER)
    country = Column(String, nullable=True)
    region = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    diagnoses = relationship("Diagnosis", back_populates="user", cascade="all, delete-orphan")
    quotation_requests = relationship("QuotationRequest", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_created_at', 'created_at'),
    )


class Crop(Base):
    """Crop type model."""
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    name_ar = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    scientific_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    diseases = relationship("Disease", back_populates="crop")
    growth_stages = relationship("GrowthStage", back_populates="crop")
    products = relationship("Product", back_populates="applicable_crops", secondary="crop_product")


class Disease(Base):
    """Disease model."""
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), index=True)
    name = Column(String, index=True)
    name_ar = Column(String, nullable=True)
    description = Column(Text)
    symptoms = Column(JSON)  # List of symptoms
    causes = Column(JSON)  # List of causes
    severity_level = Column(String)  # Low, Medium, High, Critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    crop = relationship("Crop", back_populates="diseases")
    diagnoses = relationship("Diagnosis", back_populates="disease")
    recommended_products = relationship("Product", back_populates="target_diseases", secondary="disease_product")


class GrowthStage(Base):
    """Crop growth stage model."""
    __tablename__ = "growth_stages"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), index=True)
    name = Column(String)
    name_ar = Column(String, nullable=True)
    days_from_planting = Column(Integer)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    crop = relationship("Crop", back_populates="growth_stages")


class Product(Base):
    """Agrimatco product model."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    name_ar = Column(String, nullable=True)
    category = Column(String, index=True)  # Fungicide, Insecticide, Herbicide, Fertilizer
    description = Column(Text)
    active_ingredient = Column(String)
    concentration = Column(String)  # e.g., "50% WP"
    dosage = Column(String)  # e.g., "2-4 ml/L"
    safety_info = Column(Text)
    pre_harvest_interval = Column(Integer, nullable=True)  # Days
    brochure_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    stock_available = Column(Integer, default=0)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applicable_crops = relationship("Crop", back_populates="products", secondary="crop_product")
    target_diseases = relationship("Disease", back_populates="recommended_products", secondary="disease_product")
    recommendations = relationship("Recommendation", back_populates="product")

    __table_args__ = (
        Index('idx_product_category', 'category'),
        Index('idx_product_active_ingredient', 'active_ingredient'),
    )


class Diagnosis(Base):
    """Diagnosis record model."""
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=True)
    image_url = Column(String)
    crop_type = Column(String)
    country = Column(String)
    region = Column(String)
    plant_age_days = Column(Integer, nullable=True)
    growth_stage = Column(String, nullable=True)
    irrigation_method = Column(String, nullable=True)
    greenhouse = Column(Boolean, default=False)
    status = Column(SQLEnum(DiagnosisStatus), default=DiagnosisStatus.PENDING, index=True)
    detected_problem = Column(String)
    symptoms_observed = Column(JSON)  # List of symptoms
    possible_causes = Column(JSON)  # List of causes
    confidence_score = Column(Float)  # 0-100
    diagnosis_notes = Column(Text, nullable=True)
    ai_response = Column(JSON, nullable=True)  # Raw AI response
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="diagnoses")
    disease = relationship("Disease", back_populates="diagnoses")
    recommendations = relationship("Recommendation", back_populates="diagnosis", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_diagnosis_user_id', 'user_id'),
        Index('idx_diagnosis_created_at', 'created_at'),
        Index('idx_diagnosis_status', 'status'),
    )


class Recommendation(Base):
    """Product recommendation for a diagnosis."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    recommendation_type = Column(String)  # primary, alternative, complementary
    reason = Column(Text)
    application_program = Column(JSON, nullable=True)  # List of application steps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    diagnosis = relationship("Diagnosis", back_populates="recommendations")
    product = relationship("Product", back_populates="recommendations")


class ChatMessage(Base):
    """Chat conversation message."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=True)
    role = Column(String)  # user or assistant
    content = Column(Text)
    ai_response = Column(JSON, nullable=True)  # Raw AI response data
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="chat_messages")


class QuotationRequest(Base):
    """Quotation request from customers."""
    __tablename__ = "quotation_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message = Column(Text)
    status = Column(String, default="pending")  # pending, contacted, completed
    sales_rep_assigned = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="quotation_requests")


class AuditLog(Base):
    """Audit log for system actions."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, index=True)
    resource_type = Column(String)
    resource_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_audit_log_user_id', 'user_id'),
        Index('idx_audit_log_action', 'action'),
        Index('idx_audit_log_created_at', 'created_at'),
    )
