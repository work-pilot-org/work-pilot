"""
Centralized logging configuration for the WorkPilot AI Service.
"""

from __future__ import annotations

import logging
import sys

import structlog

from core.config import settings


def configure_logging() -> None:
    """
    Configure application-wide structured logging.

    This function should be called only once during
    application startup.
    """

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(message)s",
        stream=sys.stdout,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Return a configured logger.

    Args:
        name: Usually __name__ from the calling module.

    Returns:
        Structlog logger instance.
    """
    return structlog.get_logger(name)