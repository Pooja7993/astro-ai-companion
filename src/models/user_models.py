"""
User Models for PostgreSQL Database
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.config.database import Base

class User(Base):
    """User model for family members."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    telegram_chat_id = Column(String, nullable=False)
    
    # Personal Information
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    
    # Birth Details
    birth_date = Column(String, nullable=False)  # YYYY-MM-DD
    birth_time = Column(String, nullable=False)  # HH:MM
    birth_place = Column(String, nullable=False)
    birth_latitude = Column(Float, nullable=True)
    birth_longitude = Column(Float, nullable=True)
    
    # Family Relationship
    family_id = Column(Integer, ForeignKey("families.id"), nullable=True)
    relationship_to_head = Column(String, nullable=True)  # head, spouse, child, parent, etc.
    
    # Preferences
    language = Column(String, default="en")
    timezone = Column(String, default="UTC")
    
    # Settings
    daily_reports_enabled = Column(Boolean, default=True)
    notifications_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    family = relationship("Family", back_populates="members")
    birth_chart = relationship("BirthChart", back_populates="user", uselist=False)
    predictions = relationship("Prediction", back_populates="user")
    
    @property
    def full_name(self):
        """Get full name."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

class Family(Base):
    """Family model to group related users."""
    __tablename__ = "families"
    
    id = Column(Integer, primary_key=True, index=True)
    family_name = Column(String, nullable=False)
    head_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Settings
    family_timezone = Column(String, default="UTC")
    family_language = Column(String, default="en")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    members = relationship("User", back_populates="family")

class BirthChart(Base):
    """Birth chart data for each user."""
    __tablename__ = "birth_charts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Vedic Astrology Data
    sun_sign = Column(String, nullable=True)
    moon_sign = Column(String, nullable=True)
    ascendant = Column(String, nullable=True)
    nakshatra = Column(String, nullable=True)
    
    # Planetary Positions (JSON stored as text)
    planetary_positions = Column(Text, nullable=True)  # JSON string
    house_positions = Column(Text, nullable=True)  # JSON string
    aspects = Column(Text, nullable=True)  # JSON string
    
    # Numerology Data
    life_path_number = Column(Integer, nullable=True)
    destiny_number = Column(Integer, nullable=True)
    soul_number = Column(Integer, nullable=True)
    
    # Lal Kitab Data
    lal_kitab_analysis = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="birth_chart")

class Prediction(Base):
    """Predictions and guidance for users."""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Prediction Details
    prediction_type = Column(String, nullable=False)  # daily, weekly, monthly
    prediction_date = Column(String, nullable=False)  # YYYY-MM-DD
    
    # Unified Guidance
    vedic_guidance = Column(Text, nullable=True)
    numerology_guidance = Column(Text, nullable=True)
    lal_kitab_guidance = Column(Text, nullable=True)
    unified_guidance = Column(Text, nullable=False)
    
    # Remedies
    remedies = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="predictions")