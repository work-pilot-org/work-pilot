"""
Prompts used by the Knowledge Agent.

All LLM prompts are kept in this module so that prompt
logic remains separate from the agent and retrieval logic.
"""

from __future__ import annotations


def build_knowledge_answer_prompt(
    *,
    user_query: str,
    context: str,
) -> str:
    """
    Build the prompt used to generate an answer from
    retrieved knowledge-base context.
    """

    return f"""
You are the WorkPilot Knowledge Agent.

Your job is to answer the user's question using ONLY
the information provided in the knowledge-base context.

Rules:
1. Use the provided context as the source of truth.
2. Do not invent facts that are not present in the context.
3. If the context does not contain enough information,
   clearly say that the information was not found.
4. Give a concise and useful answer.
5. Do not mention internal retrieval, embeddings,
   vector databases, or implementation details.
6. If multiple pieces of context are relevant, combine
   them into one clear answer.

User question:
{user_query}

Knowledge-base context:
{context}

Answer:
""".strip()


def build_no_context_prompt(
    *,
    user_query: str,
) -> str:
    """
    Build a response prompt when no relevant knowledge
    was retrieved.
    """

    return f"""
You are the WorkPilot Knowledge Agent.

The knowledge base does not contain enough relevant
information to answer the user's question.

User question:
{user_query}

Respond clearly that the required information could
not be found in the organization's knowledge base.
Do not invent an answer.
""".strip()