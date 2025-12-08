"""Logging setup for Elfactory."""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Setup logging to both file and console.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"elfactory_{timestamp}.log"

    # Setup main logger
    logger = logging.getLogger("elfactory")
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.handlers.clear()

    # Setup agent logger (child logger)
    agent_logger = logging.getLogger("elfactory.agents")
    agent_logger.setLevel(getattr(logging, log_level.upper()))
    agent_logger.handlers.clear()

    # File handler - catches everything (DEBUG and up)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler - respects log level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers to both loggers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Agent logger uses same handlers (propagates to parent)
    agent_logger.propagate = True

    logger.info(f"Logging initialized - log file: {log_file}")

    return logger
