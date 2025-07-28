"""
Database Models for Astro AI Companion
Personal Family Use - SQLite Database Models
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """User model for Astro AI Companion."""
    telegram_id: str
    chat_id: str  # Added for direct messaging
    name: str
    birth_date: str
    birth_time: str
    birth_place: str
    language_preference: str = 'en'  # Updated field name
    daily_reports_enabled: bool = True
    realtime_guidance_enabled: bool = True


@dataclass
class FamilyMember:
    """Family member model for Astro AI Companion."""
    name: str
    relationship: str
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    birth_place: Optional[str] = None


@dataclass
class Prediction:
    """Prediction model for Astro AI Companion."""
    user_id: int
    prediction_type: str
    prediction_text: str
    created_at: Optional[datetime] = None


@dataclass
class UserPreference:
    """User preference model for Astro AI Companion."""
    user_id: int
    preference_key: str
    preference_value: str
    created_at: Optional[datetime] = None
