from __future__ import annotations


class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid or missing."""
    pass


class LLMTimeoutError(LLMError):
    """Raised when LLM request times out."""
    pass


class LLMProviderError(LLMError):
    """Raised when LLM provider returns an error."""
    pass


class StructuredOutputError(LLMError):
    """Raised when LLM output cannot be parsed into structured format."""
    pass
