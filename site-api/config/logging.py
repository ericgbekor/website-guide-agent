import logging
import json
from typing import Optional
from google.cloud import logging as gcp_logging
from google.cloud.logging.handlers import CloudLoggingHandler
from google.oauth2 import service_account


def setup_logging(project_id: Optional[str] = None, log_level: str = "INFO", credentials_dict: Optional[dict] = None):
    """
    Set up Google Cloud Logging for the application.
    
    Args:
        project_id (Optional[str]): Google Cloud project ID
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        credentials_dict (Optional[dict]): Google Cloud service account credentials as dictionary
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger("website-api")
    
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if project_id and credentials_dict:
        try:
            credentials = service_account.Credentials.from_service_account_info(credentials_dict)
            client = gcp_logging.Client(project=project_id, credentials=credentials)
            
            cloud_handler = CloudLoggingHandler(client, name="website-api")
            cloud_handler.setLevel(getattr(logging, log_level.upper()))
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            cloud_handler.setFormatter(formatter)
            
            logger.addHandler(cloud_handler)
            logger.info("Google Cloud Logging configured successfully")
            
        except Exception as e:
            logger.warning(f"Failed to configure Google Cloud Logging: {e}")
            _setup_console_logging(logger, log_level)
    else:
        if not credentials_dict:
            logger.info("No Google Cloud credentials provided, using console logging")
        _setup_console_logging(logger, log_level)
    
    return logger


def _setup_console_logging(logger: logging.Logger, log_level: str):
    """
    Fallback to console logging when Google Cloud Logging is not available.
    
    Args:
        logger (logging.Logger): Logger instance
        log_level (str): Logging level
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.info("Console logging configured as fallback")


def get_logger() -> logging.Logger:
    """
    Get the configured logger instance.
    
    Returns:
        logging.Logger: The application logger
    """
    return logging.getLogger("website-api")