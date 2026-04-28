"""Singleton Qdrant client provider."""

import logging
from functools import lru_cache

from qdrant_client import QdrantClient

from backend.config import QDRANT_API_KEY, QDRANT_URL

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    """Return one shared Qdrant client instance."""
    if not QDRANT_URL:
        raise ValueError("QDRANT_URL is required to initialize Qdrant client.")

    logger.info("Initializing Qdrant client.")
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
