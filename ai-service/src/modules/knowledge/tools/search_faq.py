"""
FAQ search tool for the Knowledge Agent.

This tool provides the Knowledge Agent with access to
frequently asked questions stored in the tenant's
knowledge base.
"""

from __future__ import annotations

from modules.knowledge.exceptions import (
    KnowledgeRetrievalError,
)
from modules.knowledge.rag.retriever import KnowledgeRetriever
from modules.knowledge.registry import tool_registry
from modules.knowledge.schemas import RetrievedDocument


async def search_faq(
    query: str,
    top_k: int = 5,
    *,
    tenant_id: str,
    retriever: KnowledgeRetriever,
) -> list[RetrievedDocument]:
    """
    Search the organization's knowledge base for FAQ-related
    information.

    Args:
        query:
            Natural-language FAQ question or search query.

        top_k:
            Maximum number of relevant document chunks to return.

        tenant_id:
            Tenant whose knowledge base should be searched.
            This value is injected by WorkPilot and must never
            come from the LLM.

        retriever:
            Knowledge retrieval service injected by the application.

    Returns:
        A list of relevant document chunks.

    Raises:
        KnowledgeRetrievalError:
            If the query or tenant ID is invalid.
    """

    if not query.strip():
        raise KnowledgeRetrievalError(
            "FAQ search query cannot be empty."
        )

    if not tenant_id.strip():
        raise KnowledgeRetrievalError(
            "Tenant ID is required."
        )

    if top_k <= 0:
        raise KnowledgeRetrievalError(
            "top_k must be greater than zero."
        )

    return await retriever.retrieve(
        query=query,
        top_k=top_k,
        tenant_id=tenant_id,
    )


tool_registry.register(
    "search_faq",
    search_faq,
)