# core/utils/logger.py

from functools import partial
import logging
from core.utils.env import EnvConfig
from core.utils.config import config

# Define valid log levels
VALID_LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
DEFAULT_LOG_LEVEL = "INFO"


def configure_logging():
    """Configure the logging settings based on environment configuration."""
    # Validate and set the log level
    log_level = (
        EnvConfig.LOG_LEVEL
        if EnvConfig.LOG_LEVEL in VALID_LOG_LEVELS
        else DEFAULT_LOG_LEVEL
    )

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    return logger


# Initialize the logger
logger = configure_logging()

logger.error = partial(logging.error, exc_info=EnvConfig.DEBUG_MCP)
