"""Request model placeholders."""

from pydantic import BaseModel


class ReviewSearchRequest(BaseModel):
    """Placeholder request for review search."""

    query: str = ""
