"""
Custom exceptions for the Knowledge Agent.
"""


class KnowledgeAgentException(Exception):
    """
    Base exception for all Knowledge Agent errors.
    """


class DocumentNotFoundError(KnowledgeAgentException):
    """
    Raised when a requested document cannot be found.
    """


class KnowledgeRetrievalError(KnowledgeAgentException):
    """
    Raised when document retrieval fails.
    """


class NoRelevantDocumentsFound(KnowledgeAgentException):
    """
    Raised when no relevant documents are found
    for the requested query.
    """


class EmbeddingError(KnowledgeAgentException):
    """
    Raised when embedding generation fails.
    """


class VectorStoreError(KnowledgeAgentException):
    """
    Raised when vector database operations fail.
    """


class IngestionError(KnowledgeAgentException):
    """
    Raised when document ingestion fails.
    """


class UnsupportedFileTypeError(KnowledgeAgentException):
    """
    Raised when attempting to ingest an unsupported file type.
    """


class EmptyKnowledgeBaseError(KnowledgeAgentException):
    """
    Raised when the knowledge base contains no indexed documents.
    """