"""
Constants for the Knowledge Agent.

These values define the default behaviour of document
processing and knowledge retrieval.
"""

# Number of document chunks retrieved for a knowledge query.
DEFAULT_TOP_K = 5

# Maximum number of characters in a document chunk.
DEFAULT_CHUNK_SIZE = 1000

# Number of characters shared between consecutive chunks.
DEFAULT_CHUNK_OVERLAP = 200

# Minimum similarity score required for a document
# to be considered relevant.
DEFAULT_MIN_RELEVANCE_SCORE = 0.50

# Supported document types for the initial Knowledge Agent.
SUPPORTED_DOCUMENT_TYPES = frozenset(
    {
        ".pdf",
        ".txt",
        ".md",
    }
)

# Maximum number of documents that can be processed
# in a single ingestion operation.
MAX_DOCUMENTS_PER_INGESTION = 10