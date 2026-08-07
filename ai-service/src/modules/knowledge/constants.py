"""
Knowledge Agent constants.
"""

# ===========================
# Collection
# ===========================

COLLECTION_NAME = "workpilot_knowledge"

# ===========================
# Retrieval
# ===========================

TOP_K = 5

SIMILARITY_THRESHOLD = 0.75

# ===========================
# Chunking
# ===========================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ===========================
# Embeddings
# ===========================

EMBEDDING_MODEL = "models/text-embedding-004"

# ===========================
# LLM
# ===========================

LLM_MODEL = "gemini-2.5-flash"

# ===========================
# Supported Files
# ===========================

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".md",
    ".txt",
}

# ===========================
# Metadata
# ===========================

DEFAULT_SOURCE = "Knowledge Base"