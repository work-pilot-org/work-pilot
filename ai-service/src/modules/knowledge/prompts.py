"""
Prompt builders for the Knowledge Agent.
"""

from __future__ import annotations


def build_document_search_prompt(
    user_query: str,
    context: str,
) -> str:
    """
    Prompt for answering questions using retrieved documents.
    """

    return f"""
You are the WorkPilot Knowledge Agent.

Answer the user's question ONLY using the provided context.

If the answer is not available in the context, reply exactly:

"I couldn't find that information in the knowledge base."

Be concise, accurate, and professional.

------------------------
Context:
{context}
------------------------

User Question:
{user_query}

Answer:
"""


def build_faq_prompt(
    user_query: str,
    context: str,
) -> str:
    """
    Prompt for FAQ retrieval.
    """

    return f"""
You are answering a frequently asked question.

Use only the FAQ information below.

FAQ:

{context}

Question:

{user_query}

Answer:
"""


def build_policy_prompt(
    user_query: str,
    context: str,
) -> str:
    """
    Prompt for company policy questions.
    """

    return f"""
You are a company policy assistant.

Only answer using the policy documents below.

Policy Documents:

{context}

Question:

{user_query}

Answer:
"""