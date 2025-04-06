import os
import logging
from typing import Any, Optional

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up and configure logging"""
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Create console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger if it doesn't already have one
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger

def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """
    Get an environment variable or return a default value
    
    Args:
        var_name: Name of the environment variable
        default: Default value if the environment variable is not set
        
    Returns:
        Value of the environment variable or the default value
        
    Raises:
        ValueError: If the environment variable is not set and no default is provided
    """
    value = os.environ.get(var_name)
    if value is None:
        if default is not None:
            return default
        raise ValueError(f"Environment variable {var_name} is not set and no default provided")
    return value

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."