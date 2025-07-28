"""
Utility functions for configuration and environment variable management.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Utility to get environment variables with a default value
def get_env(key: str, default=None):
    """
    Returns the value of the environment variable or a default.
    """
    return os.getenv(key, default) 