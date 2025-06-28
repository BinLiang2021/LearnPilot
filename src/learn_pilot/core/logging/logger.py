""" 
@file_name: logger.py
@author: bin.liang
@date: 2025-06-28
@description: Loguru logger configuration with beautiful formatting
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from loguru import logger


def setup_logger(
    log_level: str = "INFO",
    log_dir: str = "logs",
    rotation: str = "10 MB",
    retention: str = "30 days",
    compression: str = "zip"
):
    """
    Setup beautiful loguru logger with file and console handlers
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        rotation: When to rotate log files (size like "10 MB" or time like "1 day")
        retention: How long to keep log files
        compression: Compression format for rotated files
    """
    # Remove default handler
    logger.remove()
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Console handler with beautiful formatting
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        format=console_format,
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # File handler for all logs
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    )
    
    logger.add(
        log_path / "app_{time:YYYY-MM-DD}.log",
        format=file_format,
        level=log_level,
        rotation=rotation,
        retention=retention,
        compression=compression,
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    # Error file handler (only for ERROR and above)
    logger.add(
        log_path / "error_{time:YYYY-MM-DD}.log",
        format=file_format,
        level="ERROR",
        rotation=rotation,
        retention=retention,
        compression=compression,
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    
    # Debug file handler (only for DEBUG level)
    if log_level == "DEBUG":
        logger.add(
            log_path / "debug_{time:YYYY-MM-DD}.log",
            format=file_format,
            level="DEBUG",
            rotation=rotation,
            retention=retention,
            compression=compression,
            backtrace=True,
            diagnose=True,
            enqueue=True
        )
    
    logger.info(f"Logger initialized with level: {log_level}")
    logger.info(f"Log files will be stored in: {log_path.absolute()}")
    
    return logger


# Initialize logger with default settings
logger = setup_logger()

# Export logger for easy import
__all__ = ["logger", "setup_logger"]

