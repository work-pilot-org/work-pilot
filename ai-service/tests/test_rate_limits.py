import pytest
from unittest.mock import AsyncMock, MagicMock
from google.genai import errors
from infrastructure.providers.gemini_provider import GeminiProvider
from infrastructure.providers.exceptions import GeminiRateLimitError, GeminiQuotaExhaustedError

def make_mock_api_error(code: int, retry_delay_sec: str = None) -> errors.APIError:
    error_dict = {
        "error": {
            "code": code,
            "message": "Quota exceeded",
            "status": "RESOURCE_EXHAUSTED"
        }
    }
    
    if retry_delay_sec is not None:
        error_dict["error"]["details"] = [
            {
                "@type": "type.googleapis.com/google.rpc.RetryInfo",
                "retryDelay": f"{retry_delay_sec}s"
            }
        ]
        
    try:
        exc = errors.APIError(message="Quota exceeded", code=code, status="RESOURCE_EXHAUSTED", details=error_dict["error"].get("details"))
    except TypeError:
        # Some SDK versions might just take the dict
        class MockAPIError(errors.APIError):
            def __init__(self):
                self.code = code
                self.message = "Quota exceeded"
                self.details = error_dict["error"].get("details")
        exc = MockAPIError()
    exc.code = code
    exc.details = error_dict["error"].get("details")
    return exc

@pytest.mark.asyncio
async def test_transient_429_exhausted_retries():
    """Verify that a transient 429 error (short retry delay) is eventually raised as GeminiRateLimitError if retries fail."""
    provider = GeminiProvider()
    
    # Mock to always throw 429
    mock_generate = AsyncMock(side_effect=make_mock_api_error(429, retry_delay_sec="30"))
    provider._client = MagicMock()
    provider._client.aio = MagicMock()
    provider._client.aio.models = MagicMock()
    provider._client.aio.models.generate_content = mock_generate
    
    # Configure tenacity to run instantly for tests
    provider.generate.retry.sleep = AsyncMock()
    
    with pytest.raises(GeminiRateLimitError):
        await provider.generate("Test prompt")
        
    assert mock_generate.call_count == 4  # stop_after_attempt(4)

@pytest.mark.asyncio
async def test_hard_quota_429():
    """Verify that a hard quota error (no retry delay, or very large) raises GeminiQuotaExhaustedError immediately."""
    provider = GeminiProvider()
    
    # Mock to throw 429 with no retry delay
    mock_generate = AsyncMock(side_effect=make_mock_api_error(429))
    provider._client = MagicMock()
    provider._client.aio = MagicMock()
    provider._client.aio.models = MagicMock()
    provider._client.aio.models.generate_content = mock_generate
    
    provider.generate.retry.sleep = MagicMock()
    
    with pytest.raises(GeminiQuotaExhaustedError):
        await provider.generate("Test prompt")
        
    # Should not retry because it wasn't considered transient
    assert mock_generate.call_count == 1
