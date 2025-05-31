"""
Resource modules for the Excel Summarization Chatbot.
"""

from .az_language import (
    get_az_translations,
    get_common_queries,
    get_error_messages,
    get_success_messages
)

__all__ = [
    'get_az_translations',
    'get_common_queries',
    'get_error_messages',
    'get_success_messages'
] 