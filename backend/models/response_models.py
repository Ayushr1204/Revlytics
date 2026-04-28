"""Response model placeholders."""

from pydantic import BaseModel


class ReviewSearchResponse(BaseModel):
    """Placeholder response for review search."""

    answer: str = ""
