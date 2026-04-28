"""
backend/main.py — FastAPI server for Amazon OTDS

Run:  uvicorn backend.main:app --reload
  or: python -m backend.main
"""

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# ── Add scripts/ to path so we can import search ─────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from search import search_and_summarize  # noqa: E402

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="Amazon OTDS — AI Review Intelligence")

# Serve static frontend files
STATIC_DIR = ROOT / "frontend" / "static"
ASSETS_DIR = ROOT / "assets"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Models ────────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    query: str
    product_id: str | None = None


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/search")
def api_search(req: SearchRequest):
    """Run semantic search and return structured results."""
    result = search_and_summarize(req.query, product_id=req.product_id)
    return result


@app.get("/")
def serve_index():
    """Serve the frontend HTML."""
    return FileResponse(str(STATIC_DIR / "index.html"))


# ── Dev entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
