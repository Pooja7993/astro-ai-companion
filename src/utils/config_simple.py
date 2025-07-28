"""
Simple Configuration Management for Astro AI Companion
Personal Family Use - Minimal Configuration
"""

import os
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field, validator, SecretStr
from pydantic_settings import BaseSettings
import logging

class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    database_url: str = Field(default="sqlite:///data/astro_companion.db", description="Database connection string")
    
    class Config:
        env_prefix = "DB_"
        case_sensitive = False

class LoggingConfig(BaseSettings):
    """Logging configuration."""
    
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/simple_astro.log", description="Log file path")
    log_rotation: str = Field(default="1 day", description="Log rotation interval")
    log_retention: str = Field(default="7 days", description="Log retention period")
    
    class Config:
        env_prefix = "LOG_"
        case_sensitive = False

class AstrologyConfig(BaseSettings):
    """Astrology-specific configuration."""
    
    default_language: str = Field(default="en", description="Default language")
    supported_languages: List[str] = Field(default=["en", "mr"], description="Supported languages")
    
    # Prediction settings
    prediction_cache_ttl: int = Field(default=3600, description="Prediction cache TTL in seconds")
    max_prediction_length: int = Field(default=1000, description="Maximum prediction text length")
    
    class Config:
        env_prefix = "ASTRO_"
        case_sensitive = False

class TelegramConfig(BaseSettings):
    """Telegram bot configuration."""
    
    telegram_bot_token: Optional[SecretStr] = Field(default=None, description="Telegram bot token")
    telegram_chat_id: Optional[str] = Field(default=None, description="Default Telegram chat ID")
    
    # Bot settings
    bot_polling_timeout: int = Field(default=30, description="Bot polling timeout in seconds")
    
    # Message settings
    max_message_length: int = Field(default=4096, description="Maximum message length")
    enable_message_retry: bool = Field(default=True, description="Enable message retry on failure")
    message_retry_attempts: int = Field(default=3, description="Message retry attempts")
    
    class Config:
        env_prefix = "TELEGRAM_"
        case_sensitive = False

class SchedulerConfig(BaseSettings):
    """Scheduler configuration."""
    
    # Daily settings
    enable_daily_reminders: bool = Field(default=True, description="Enable daily reminders")
    morning_time: str = Field(default="07:00", description="Morning guidance time")
    evening_time: str = Field(default="18:00", description="Evening guidance time")
    night_time: str = Field(default="21:30", description="Night guidance time")
    
    # Timezone
    default_timezone: str = Field(default="UTC", description="Default timezone")
    
    class Config:
        env_prefix = "SCHEDULER_"
        case_sensitive = False

class Config(BaseSettings):
    """Main application configuration for personal family use."""
    
    # Environment
    environment: str = Field(default="development", description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Database
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # Logging
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Astrology
    astrology: AstrologyConfig = Field(default_factory=AstrologyConfig)
    
    # Telegram
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    
    # Scheduler
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    
    # File paths
    data_dir: str = Field(default="./data", description="Data directory")
    logs_dir: str = Field(default="./logs", description="Logs directory")
    config_dir: str = Field(default="./config", description="Config directory")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
        extra = "ignore"  # Ignore extra fields
    
    @validator('environment')
    def validate_environment(cls, v):
        """Validate environment setting."""
        if v not in ['development', 'production', 'testing']:
            raise ValueError('Environment must be development, production, or testing')
        return v
    
    @validator('data_dir', 'logs_dir', 'config_dir')
    def create_directories(cls, v):
        """Create directories if they don't exist."""
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    def get_database_url(self) -> str:
        """Get database URL with fallback."""
        return self.database.database_url
    
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"
    
    def get_log_level(self) -> int:
        """Get logging level as integer."""
        return getattr(logging, self.logging.log_level.upper(), logging.INFO)
    
    def has_telegram_token(self) -> bool:
        """Check if telegram token is available."""
        return self.telegram.telegram_bot_token is not None

# Global configuration instance
_config: Optional[Config] = None

def get_config() -> Config:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config

def get_database_config() -> DatabaseConfig:
    """Get database configuration."""
    return get_config().database

def get_logging_config() -> LoggingConfig:
    """Get logging configuration."""
    return get_config().logging

def get_astrology_config() -> AstrologyConfig:
    """Get astrology configuration."""
    return get_config().astrology

def get_telegram_config() -> TelegramConfig:
    """Get telegram configuration."""
    return get_config().telegram

def get_scheduler_config() -> SchedulerConfig:
    """Get scheduler configuration."""
    return get_config().scheduler 