import pytest
from unittest.mock import AsyncMock, MagicMock
from modules.hr.tool_definitions import get_hr_tool_definitions
from infrastructure.providers.gemini_provider import GeminiProvider

@pytest.mark.asyncio
async def test_get_hr_tool_definitions_valid():
    """Verify that all tools generated from schemas can be dumped without errors."""
    tools = get_hr_tool_definitions()
    assert len(tools) > 0
    # If any unsupported types like anyOf were accidentally passed, they won't 
    # immediately throw until passed to genai, but we can check for them manually
    for tool in tools:
        schema_dict = tool.model_dump(exclude_none=True)
        # Ensure no arbitrary exceptions
        assert isinstance(schema_dict, dict)
        
        # We can also recursively check that there are no 'anyOf' keys in the parameters
        def check_no_any_of(obj):
            if isinstance(obj, dict):
                assert "anyOf" not in obj, f"Found anyOf in tool {tool.name}"
                for v in obj.values():
                    check_no_any_of(v)
            elif isinstance(obj, list):
                for item in obj:
                    check_no_any_of(item)
        
        check_no_any_of(schema_dict)

@pytest.mark.asyncio
async def test_hr_tool_calling_mock():
    """Test Gemini Provider handling of HR tools with mocked client."""
    provider = GeminiProvider()
    
    # Mock the internal client
    mock_response = MagicMock()
    mock_response.text = ""
    mock_response.function_calls = []
    
    mock_generate = AsyncMock(return_value=mock_response)
    
    provider._client = MagicMock()
    provider._client.aio = MagicMock()
    provider._client.aio.models = MagicMock()
    provider._client.aio.models.generate_content = mock_generate
    
    tools = get_hr_tool_definitions()
    
    contents = "Allocate 10 days of SICK leave to all employees for the year 2026."
    
    res = await provider.generate_with_tools(contents=contents, tools=tools)
    
    # Should not raise any Gemini API request failed errors.
    assert mock_generate.call_count == 1
