"""
Response Builder for the Coordinator Agent.

This module takes the raw, technical results from the Tool Executor and 
formats them into a unified, user-friendly natural language response.
It also safely formats error messages.
"""

from typing import Any, Dict, List

from core.logger import get_logger
from infrastructure.llm.gemini_client import gemini_client
from modules.coordinator.exceptions import CoordinatorError


logger = get_logger(__name__)


# Prompt template for summarizing the final execution results
RESPONSE_BUILDER_PROMPT = """\
You are the final Response Builder for a multi-agent orchestration system.
Your job is to read the results of executed tasks and summarize them into a 
single, clear, and friendly natural language response for the user.

Original User Request:
{user_message}

Task Execution Results:
{execution_results}

Rules:
1. Provide a direct, polite summary of what was accomplished.
2. If any step failed, explain what failed and why in a helpful manner.
3. Do not invent or hallucinate details; rely entirely on the provided execution results.
4. Keep the response concise but complete.
"""


class ResponseBuilder:
    """
    Transforms raw execution results and errors into unified final responses.
    """

    async def build_success_response(
        self, 
        user_message: str, 
        execution_results: List[Dict[str, Any]]
    ) -> str:
        """
        Uses the LLM to summarize the executed steps into a natural language string.
        
        Args:
            user_message (str): The original user request.
            execution_results (list): The collected results from the Tool Executor.
            
        Returns:
            str: The final, unified text response.
        """
        logger.info("Building final success response")
        
        # Format the dictionary results into a readable string for the LLM prompt
        results_str = ""
        for res in execution_results:
            results_str += f"Step {res.get('step_number')}: {res.get('description')}\n"
            results_str += f"Outcome: {res.get('result')}\n\n"
            
        prompt = RESPONSE_BUILDER_PROMPT.format(
            user_message=user_message,
            execution_results=results_str.strip()
        )
        
        try:
            # We use the raw gemini client here because we want natural language text,
            # not structured JSON (which is what coordinator_llm_client enforces).
            final_response = await gemini_client.generate(prompt=prompt)
            return final_response.strip()
            
        except Exception as e:
            logger.error("LLM failed to build summary, falling back to raw output", error=str(e))
            # Fallback gracefully so the user still gets their data if the LLM hiccups
            return (
                f"Your request was processed, but the final summary generation failed. "
                f"Raw execution results: {execution_results}"
            )

    def build_error_response(self, error: Exception) -> str:
        """
        Formats internal exceptions into a safe, user-friendly error string.
        Ensures internal system stack traces or sensitive data are not leaked.
        """
        logger.info("Building error response for exception", error_type=type(error).__name__)
        
        if isinstance(error, CoordinatorError):
            # These are our controlled orchestration errors (IntentDetectionError, etc.)
            return f"I encountered an issue while coordinating your request: {str(error)}"
            
        # Catch-all for unexpected crashes (database drops, syntax errors, etc.)
        return "An unexpected internal error occurred while trying to fulfill your request. Please try again later."


# Singleton instance for the coordinator module
response_builder = ResponseBuilder()
