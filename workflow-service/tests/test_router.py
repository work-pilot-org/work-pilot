import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import BackgroundTasks
from shared_infrastructure.events import EventEnvelope

from src.modules.workflow.router import approve_task, start_workflow_execution
from src.modules.workflow.schemas import ApprovalDecision, WorkflowExecutionCreate

@pytest.mark.asyncio
async def test_approve_task_publishes_events():
    # Setup mocks
    mock_db = MagicMock()
    mock_bg_tasks = MagicMock(spec=BackgroundTasks)
    mock_current_user = {"sub": "user_123", "role": "MANAGER", "schema_name": "tenant_1"}
    mock_credentials = MagicMock(credentials="fake_token")
    
    mock_approval = MagicMock()
    mock_approval.id = "step_1"
    mock_approval.execution_id = "exec_1"
    mock_approval.decision = "approved"
    mock_approval.approver_id = "user_123"
    mock_approval.decided_at = None
    
    mock_execution = MagicMock()
    mock_execution.id = "exec_1"
    mock_execution.workflow_id = "wf_1"
    mock_execution.entity_type = "leave_request"
    mock_execution.status = "completed"
    mock_execution.current_step = 1
    
    # Mock WorkflowService
    with patch("src.modules.workflow.router.WorkflowService") as MockService:
        service_instance = MockService.return_value
        service_instance.approve_step = AsyncMock(return_value=mock_approval)
        service_instance.get_execution.return_value = mock_execution
        
        # Call the router function directly
        decision = ApprovalDecision(decision="approved", comments="LGTM")
        result = await approve_task(
            task_id="task_123",
            data=decision,
            background_tasks=mock_bg_tasks,
            _rbac=None,
            db=mock_db,
            current_user=mock_current_user,
            credentials=mock_credentials
        )
        
        # Assertions
        assert result == mock_approval
        service_instance.approve_step.assert_called_once_with(
            task_id="task_123",
            user_id="user_123",
            user_role="MANAGER",
            decision_data=decision,
            token="fake_token"
        )
        
        # Verify background tasks were added for publishing events
        assert mock_bg_tasks.add_task.call_count == 2
        
        # First call should be step approved
        call1_args = mock_bg_tasks.add_task.call_args_list[0][0]
        assert call1_args[1] == "workflow.execution" # topic
        event1 = call1_args[2]
        assert isinstance(event1, EventEnvelope)
        assert event1.event_type == "workflow.step.approved"
        assert event1.tenant_id == "tenant_1"
        assert event1.payload["step_id"] == "step_1"
        
        # Second call should be execution completed (since status == "completed")
        call2_args = mock_bg_tasks.add_task.call_args_list[1][0]
        assert call2_args[1] == "workflow.execution"
        event2 = call2_args[2]
        assert event2.event_type == "workflow.execution.completed"
        assert event2.payload["execution_id"] == "exec_1"
