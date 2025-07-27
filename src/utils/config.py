"""
Enhanced Configuration Management for Astro AI Companion
Implements secure, validated configuration with environment-specific settings
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, SecretStr
from pydantic_settings import BaseSettings
import logging

class SecurityConfig(BaseSettings):
    """Security-related configuration."""
    
    # JWT Settings
    jwt_secret_key: SecretStr = Field(..., description="JWT secret key for API authentication")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_hours: int = Field(default=24, description="JWT token expiration in hours")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Requests per minute per user")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")
    
    # CORS Settings
    cors_origins: List[str] = Field(default=["http://localhost:3000"], description="Allowed CORS origins")
    cors_credentials: bool = Field(default=True, description="Allow CORS credentials")
    
    # API Security
    api_key_header: str = Field(default="X-API-Key", description="API key header name")
    enable_api_auth: bool = Field(default=True, description="Enable API authentication")
    
    class Config:
        env_prefix = "SECURITY_"
        case_sensitive = False

class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    database_url: str = Field(..., description="Database connection string")
    database_pool_size: int = Field(default=10, description="Database connection pool size")
    database_max_overflow: int = Field(default=20, description="Database max overflow connections")
    database_pool_timeout: int = Field(default=30, description="Database pool timeout in seconds")
    database_pool_recycle: int = Field(default=3600, description="Database pool recycle time")
    
    # Backup settings
    backup_enabled: bool = Field(default=True, description="Enable automated backups")
    backup_interval_hours: int = Field(default=24, description="Backup interval in hours")
    backup_retention_days: int = Field(default=30, description="Backup retention in days")
    
    class Config:
        env_prefix = "DB_"
        case_sensitive = False

class LoggingConfig(BaseSettings):
    """Logging configuration."""
    
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    log_file: str = Field(default="logs/astro_ai.log", description="Log file path")
    log_rotation: str = Field(default="1 day", description="Log rotation interval")
    log_retention: str = Field(default="30 days", description="Log retention period")
    
    # Structured logging
    enable_structured_logging: bool = Field(default=True, description="Enable structured logging")
    log_correlation_id: bool = Field(default=True, description="Include correlation ID in logs")
    
    class Config:
        env_prefix = "LOG_"
        case_sensitive = False

class MonitoringConfig(BaseSettings):
    """Monitoring and observability configuration."""
    
    # Metrics
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=9090, description="Metrics server port")
    
    # Health checks
    health_check_interval: int = Field(default=30, description="Health check interval in seconds")
    health_check_timeout: int = Field(default=10, description="Health check timeout in seconds")
    
    # Tracing
    enable_tracing: bool = Field(default=True, description="Enable distributed tracing")
    tracing_endpoint: Optional[str] = Field(default=None, description="Tracing endpoint URL")
    
    # Alerting
    alert_webhook_url: Optional[str] = Field(default=None, description="Alert webhook URL")
    alert_email: Optional[str] = Field(default=None, description="Alert email address")
    
    class Config:
        env_prefix = "MONITORING_"
        case_sensitive = False

class AstrologyConfig(BaseSettings):
    """Astrology-specific configuration."""
    
    ephemeris_path: Optional[str] = Field(default=None, description="Swiss Ephemeris data path")
    default_language: str = Field(default="en", description="Default language")
    supported_languages: List[str] = Field(default=["en", "mr"], description="Supported languages")
    
    # Prediction settings
    prediction_cache_ttl: int = Field(default=3600, description="Prediction cache TTL in seconds")
    max_prediction_length: int = Field(default=1000, description="Maximum prediction text length")
    
    # Quality assurance
    min_prediction_score: float = Field(default=0.7, description="Minimum prediction quality score")
    enable_auto_regeneration: bool = Field(default=True, description="Enable automatic prediction regeneration")
    
    class Config:
        env_prefix = "ASTRO_"
        case_sensitive = False

class TelegramConfig(BaseSettings):
    """Telegram bot configuration."""
    
    telegram_bot_token: SecretStr = Field(..., description="Telegram bot token")
    telegram_chat_id: Optional[str] = Field(default=None, description="Default Telegram chat ID")
    
    # Bot settings
    bot_webhook_url: Optional[str] = Field(default=None, description="Webhook URL for bot")
    bot_polling_timeout: int = Field(default=30, description="Bot polling timeout in seconds")
    bot_max_connections: int = Field(default=100, description="Maximum bot connections")
    
    # Message settings
    max_message_length: int = Field(default=4096, description="Maximum message length")
    enable_message_retry: bool = Field(default=True, description="Enable message retry on failure")
    message_retry_attempts: int = Field(default=3, description="Message retry attempts")
    
    class Config:
        env_prefix = "TELEGRAM_"
        case_sensitive = False

class SchedulerConfig(BaseSettings):
    """Scheduler configuration."""
    
    # 24/7 settings
    enable_24_7_mode: bool = Field(default=True, description="Enable 24/7 real-time guidance")
    morning_time: str = Field(default="07:00", description="Morning guidance time")
    evening_time: str = Field(default="18:00", description="Evening guidance time")
    night_time: str = Field(default="21:30", description="Night guidance time")
    
    # Real-time settings
    realtime_scan_interval: int = Field(default=900, description="Real-time scan interval in seconds")
    opportunity_alert_threshold: float = Field(default=0.8, description="Opportunity alert threshold")
    
    # Timezone
    default_timezone: str = Field(default="UTC", description="Default timezone")
    
    class Config:
        env_prefix = "SCHEDULER_"
        case_sensitive = False

class OllamaConfig(BaseSettings):
    """Ollama local AI model configuration."""
    
    # Ollama server settings
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama server base URL")
    ollama_timeout: int = Field(default=30, description="Ollama request timeout in seconds")
    ollama_retry_attempts: int = Field(default=3, description="Number of retry attempts for Ollama requests")
    
    # Model settings
    default_model: str = Field(default="llama2", description="Default Ollama model to use")
    available_models: List[str] = Field(default=["llama2", "llama2:13b", "llama2:70b", "mistral", "codellama"], description="Available Ollama models")
    
    # Generation settings
    temperature: float = Field(default=0.7, description="Temperature for text generation")
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate")
    top_p: float = Field(default=0.9, description="Top-p sampling parameter")
    top_k: int = Field(default=40, description="Top-k sampling parameter")
    
    # Context settings
    context_window: int = Field(default=4096, description="Context window size")
    max_input_length: int = Field(default=3072, description="Maximum input length")
    
    # Fallback settings
    enable_fallback: bool = Field(default=True, description="Enable fallback to simpler models")
    fallback_models: List[str] = Field(default=["llama2", "mistral"], description="Fallback models in order")
    
    # Performance settings
    enable_streaming: bool = Field(default=False, description="Enable streaming responses")
    batch_size: int = Field(default=1, description="Batch size for multiple requests")
    
    class Config:
        env_prefix = "OLLAMA_"
        case_sensitive = False

class Config(BaseSettings):
    """Main application configuration with all subsystems."""
    
    # Environment
    environment: str = Field(default="development", description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Security
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # Database
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # Logging
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Monitoring (removed - using simple logging)
    
    # Astrology
    astrology: AstrologyConfig = Field(default_factory=AstrologyConfig)
    
    # Telegram
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    
    # Scheduler
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    
    # Ollama (removed - using simple astrology engine)
    
    # External services (removed commercial dependencies)
    
    # File paths
    data_dir: str = Field(default="./data", description="Data directory")
    logs_dir: str = Field(default="./logs", description="Logs directory")
    config_dir: str = Field(default="./config", description="Config directory")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
    
    @validator('environment')
    def validate_environment(cls, v):
        allowed = ['development', 'staging', 'production', 'testing']
        if v not in allowed:
            raise ValueError(f'Environment must be one of: {allowed}')
        return v
    
    @validator('data_dir', 'logs_dir', 'config_dir')
    def create_directories(cls, v):
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    def get_database_url(self) -> str:
        """Get database URL with fallback to SQLite."""
        if self.database.database_url:
            return self.database.database_url
        return f"sqlite:///{self.data_dir}/astro_companion.db"
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"
    
    def get_log_level(self) -> int:
        """Get logging level as integer."""
        return getattr(logging, self.logging.log_level.upper())
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins with environment-specific defaults."""
        if self.is_production():
            return self.security.cors_origins
        return ["http://localhost:3000", "http://127.0.0.1:3000"] + self.security.cors_origins

# Global configuration instance
config = Config()

# Convenience functions
def get_config() -> Config:
    """Get the global configuration instance."""
    return config

def get_security_config() -> SecurityConfig:
    """Get security configuration."""
    return config.security

def get_database_config() -> DatabaseConfig:
    """Get database configuration."""
    return config.database

def get_logging_config() -> LoggingConfig:
    """Get logging configuration."""
    return config.logging

def get_monitoring_config() -> None:
    """Get monitoring configuration (removed - using simple logging)."""
    return None

def get_astrology_config() -> AstrologyConfig:
    """Get astrology configuration."""
    return config.astrology

def get_telegram_config() -> TelegramConfig:
    """Get Telegram configuration."""
    return config.telegram

def get_scheduler_config() -> SchedulerConfig:
    """Get scheduler configuration."""
    return config.scheduler

def get_ollama_config() -> None:
    """Get Ollama configuration (removed - using simple astrology engine)."""
    return None
