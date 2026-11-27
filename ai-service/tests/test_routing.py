import pytest
from unittest.mock import patch, MagicMock
from modules.coordinator.agent import coordinator_agent
from modules.coordinator.exceptions import UnknownDomainError

@pytest.mark.asyncio
async def test_coordinator_agent_greeting_short_circuit():
    with patch("modules.coordinator.intent_detector.intent_detector.detect_intent") as mock_detect:
        # Mocking the classification
        mock_detect.return_value = MagicMock(domain="general", intent="GREETING")
        
        response = await coordinator_agent.process(user_message="Hello AI", user_context={"sub": "123"})
        
        assert "Hello! I'm your WorkPilot AI assistant" in response
        mock_detect.assert_called_once()
        # Planner should not be called

@pytest.mark.asyncio
async def test_coordinator_agent_thanks_short_circuit():
    with patch("modules.coordinator.intent_detector.intent_detector.detect_intent") as mock_detect:
        mock_detect.return_value = MagicMock(domain="general", intent="THANKS")
        
        response = await coordinator_agent.process(user_message="Thank you!", user_context={"sub": "123"})
        
        assert "You're welcome!" in response
        mock_detect.assert_called_once()

@pytest.mark.asyncio
async def test_coordinator_agent_unknown_domain_raises_error():
    with patch("modules.coordinator.intent_detector.intent_detector.detect_intent") as mock_detect:
        mock_detect.return_value = MagicMock(domain="unknown", intent="BOOK_FLIGHT")
        
        with pytest.raises(Exception) as excinfo:
            await coordinator_agent.process(user_message="Book me a flight to Mars", user_context={"sub": "123"})
            
        assert "unknown" in str(excinfo.value)
