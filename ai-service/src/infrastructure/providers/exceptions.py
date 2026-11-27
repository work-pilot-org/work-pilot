"""
Exceptions for LLM Providers.
"""

class LLMProviderError(RuntimeError):
    """Base class for all LLM provider errors."""
    pass

class GeminiRateLimitError(LLMProviderError):
    """Raised when Gemini API encounters a transient rate limit (e.g. RPM limit)."""
    pass

class GeminiQuotaExhaustedError(LLMProviderError):
    """Raised when Gemini API encounters a hard quota exhaustion (e.g. RPD limit)."""
    pass
