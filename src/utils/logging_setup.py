"""
Logging Setup for Astro AI Companion
Personal Family Use - Structured Logging
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

# Remove default loguru handler
logger.remove()

# Add custom handler for console output
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Add file handler for logs
log_path = Path("logs")
log_path.mkdir(exist_ok=True)

logger.add(
    "logs/astro_ai.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="1 day",
    retention="30 days",
    compression="zip"
)

# Add error file handler
logger.add(
    "logs/errors.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="1 day",
    retention="30 days",
    compression="zip"
)


def get_logger(name: str) -> logger:
    """Get a logger instance with the given name."""
    return logger.bind(name=name)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration."""
    # Configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": level,
                "colorize": True
            }
        ]
    )
    
    # Add file handler if specified
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="1 day",
            retention="30 days",
            compression="zip"
        )


# Initialize logging
setup_logging() 