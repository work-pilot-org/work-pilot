"""
Tool Executor for the Coordinator Agent.

This module is responsible for executing the sequence of steps defined by the Planner.
It fetches the correct specialist agent from the Registry and feeds it the tasks 
one by one, collecting the results. It handles execution failures gracefully with retries.
"""

from typing import Any, Dict, List

from core.logger import get_logger
from modules.coordinator.constants import MAX_TOOL_RETRIES
from modules.coordinator.exceptions import ToolExecutionError
from modules.coordinator.planner import ExecutionPlan
from modules.coordinator.registry import agent_registry


logger = get_logger(__name__)


class ToolExecutor:
    """
    Executes an Orchestration Plan by delegating tasks to the specialist agents.
    """

    async def execute_plan(
        self, 
        domain: str, 
        plan: ExecutionPlan, 
        user_message: str,
        headers: dict[str, str] | None = None
    ) -> List[Dict[str, Any]]:
        """
        Iterates over the execution plan and invokes the specialist agent for each step.
        
        Args:
            domain (str): The domain string used to fetch the specialist agent.
            plan (ExecutionPlan): The ordered execution plan from the Planner.
            user_message (str): The original natural language request.
            headers (dict | None): Trusted headers to safely forward downstream.
            
        Returns:
            List[Dict]: An aggregated list of results from all executed steps.
            
        Raises:
            ToolExecutionError: If a step fails completely after max retries.
        """
        # 1. Fetch the correct specialist agent (e.g., HRAgent) via the registry.
        # This prevents the Coordinator from tightly coupling to the HR codebase.
        specialist_agent = agent_registry.get_agent(domain)
        
        logger.info(
            "Starting plan execution", 
            domain=domain, 
            total_steps=len(plan.plan)
        )
        
        results = []
        accumulated_context = ""

        # 2. Execute steps sequentially
        for step in plan.plan:
            logger.info("Executing step", step_number=step.step_number, description=step.description)
            
            # Provide the agent with context of what has already happened
            # so it can correlate entities (like passing a newly generated Employee ID to the next step).
            step_message = (
                f"Original User Request:\n{user_message}\n\n"
                f"Context from previous steps:\n{accumulated_context}\n\n"
                f"Current Task to Execute:\n{step.description}"
            ) if accumulated_context else (
                f"Original User Request:\n{user_message}\n\n"
                f"Current Task to Execute:\n{step.description}"
            )

            # 3. Handle failures gracefully via retries
            step_result = await self._execute_with_retries(
                agent=specialist_agent,
                message=step_message,
                agent_name=domain,
                headers=headers,
            )
            
            # 4. Collect results from all executed tasks
            results.append({
                "step_number": step.step_number,
                "description": step.description,
                "result": step_result,
            })
            
            # Append this result to the context so the next step knows what happened
            accumulated_context += f"\nStep {step.step_number} Result: {step_result}"

        logger.info("Plan execution completed successfully")
        
        return results

    async def _execute_with_retries(
        self, 
        agent: Any, 
        message: str, 
        agent_name: str,
        headers: dict[str, str] | None
    ) -> Any:
        """
        Helper method to invoke the specialist agent with graceful retry logic.
        """
        last_error = None
        
        for attempt in range(1, MAX_TOOL_RETRIES + 1):
            try:
                # We strictly reuse the existing `run` interface found on your agents
                return await agent.run(message=message, headers=headers)
                
            except Exception as e:
                last_error = e
                logger.warning(
                    "Specialist agent execution failed, retrying...",
                    agent_name=agent_name,
                    attempt=attempt,
                    error=str(e)
                )
                
        # If all retries are exhausted, bubble up a strongly-typed orchestration error
        logger.error("Max retries reached for specialist agent", agent_name=agent_name)
        raise ToolExecutionError(agent_name=agent_name, message=str(last_error))


# Singleton instance for the coordinator module
tool_executor = ToolExecutor()
