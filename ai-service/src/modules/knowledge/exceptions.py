"""
Custom exceptions for the Knowledge Agent.
"""


class KnowledgeAgentException(Exception):
    """
    Base exception for all Knowledge Agent errors.
    """

    pass


class DocumentNotFoundError(KnowledgeAgentException):
    """
    Raised when a requested document cannot be found.
    """

    pass


class RetrievalError(KnowledgeAgentException):
    """
    Raised when document retrieval fails.
    """

    pass


class EmbeddingError(KnowledgeAgentException):
    """
    Raised when embedding generation fails.
    """

    pass


class VectorStoreError(KnowledgeAgentException):
    """
    Raised when vector database operations fail.
    """

    pass


class IngestionError(KnowledgeAgentException):
    """
    Raised when document ingestion fails.
    """

    pass


class UnsupportedFileTypeError(KnowledgeAgentException):
    """
    Raised when attempting to ingest an unsupported file type.
    """

    pass


class EmptyKnowledgeBaseError(KnowledgeAgentException):
    """
    Raised when the knowledge base contains no indexed documents.
    """

    pass