from typing import Dict, Any
import os
from pathlib import Path

# Application settings
APP_NAME = "Excel Məlumat Analizi Chatbot"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Excel fayllarının Azərbaycan dilində analizi və xülasəsi"

# File settings
ALLOWED_EXTENSIONS = {'.xlsx', '.xls'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
TEMP_DIR = Path("temp")
UPLOAD_DIR = Path("uploads")

# Create necessary directories
TEMP_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

# Streamlit settings
STREAMLIT_CONFIG = {
    "theme": {
        "primaryColor": "#1E88E5",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans serif"
    },
    "page_title": APP_NAME,
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Visualization settings
PLOTLY_TEMPLATE = "plotly_white"
CHART_HEIGHT = 600
CHART_WIDTH = 800

# NLP settings
MAX_QUERY_LENGTH = 500
SUPPORTED_LANGUAGES = ["az", "en"]
DEFAULT_LANGUAGE = "az"

# Cache settings
CACHE_TTL = 3600  # 1 hour in seconds
MAX_CACHE_SIZE = 100  # Maximum number of cached results

def get_settings() -> Dict[str, Any]:
    """
    Get all application settings.
    
    Returns:
        Dict containing all settings
    """
    return {
        "app": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "description": APP_DESCRIPTION
        },
        "file": {
            "allowed_extensions": ALLOWED_EXTENSIONS,
            "max_size": MAX_FILE_SIZE,
            "temp_dir": str(TEMP_DIR),
            "upload_dir": str(UPLOAD_DIR)
        },
        "streamlit": STREAMLIT_CONFIG,
        "visualization": {
            "template": PLOTLY_TEMPLATE,
            "height": CHART_HEIGHT,
            "width": CHART_WIDTH
        },
        "nlp": {
            "max_query_length": MAX_QUERY_LENGTH,
            "supported_languages": SUPPORTED_LANGUAGES,
            "default_language": DEFAULT_LANGUAGE
        },
        "cache": {
            "ttl": CACHE_TTL,
            "max_size": MAX_CACHE_SIZE
        }
    }

def get_environment_variables() -> Dict[str, str]:
    """
    Get environment variables with defaults.
    
    Returns:
        Dict containing environment variables
    """
    return {
        "DEBUG": os.getenv("DEBUG", "False"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development")
    } 