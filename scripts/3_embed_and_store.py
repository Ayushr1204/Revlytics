"""
scripts/embed_and_store.py

Generates embeddings for cleaned review chunks using sentence-transformers
and stores them in local Qdrant (on-disk).

Embedding model : all-MiniLM-L6-v2  (dim=384)
Data source     : data/review_chunks_clean.json  →  data["chunks"]
Qdrant collection: "review_chunks"
"""

import json
import sys
from pathlib import Path

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
)

# ── Configuration ─────────────────────────────────────────────────────────────

COLLECTION_NAME = "review_chunks"
VECTOR_SIZE     = 384
BATCH_SIZE      = 32
EMBED_MODEL     = "all-MiniLM-L6-v2"

DATA_PATH   = Path(__file__).resolve().parent.parent / "data" / "review_chunks_clean.json"
QDRANT_PATH = Path(__file__).resolve().parent / "qdrant_data"

# ── Load chunks ───────────────────────────────────────────────────────────────

def load_chunks():
    if not DATA_PATH.exists():
        print(f"[ERROR] Data file not found: {DATA_PATH}")
        sys.exit(1)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data["chunks"]
    print(f"[INFO]  Loaded {len(chunks)} chunks from {DATA_PATH.name}")
    return chunks

# ── Qdrant setup ──────────────────────────────────────────────────────────────

def get_qdrant_client():
    QDRANT_PATH.mkdir(parents=True, exist_ok=True)
    client = QdrantClient(path=str(QDRANT_PATH))
    print(f"[INFO]  Qdrant local storage at {QDRANT_PATH}")
    return client


def recreate_collection(client):
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in existing:
        client.delete_collection(collection_name=COLLECTION_NAME)
        print(f"[INFO]  Deleted existing collection '{COLLECTION_NAME}'")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"[INFO]  Created collection '{COLLECTION_NAME}' (dim={VECTOR_SIZE}, cosine)")

# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline():
    # 1. Load data
    chunks = load_chunks()

    # 2. Load local embedding model
    print(f"[INFO]  Loading embedding model '{EMBED_MODEL}' ...")
    model = SentenceTransformer(EMBED_MODEL)
    print(f"[INFO]  Model loaded successfully")

    # 3. Connect to local Qdrant and recreate collection
    client = get_qdrant_client()
    recreate_collection(client)

    # 4. Batch embed and upsert
    total = len(chunks)
    n_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    inserted = 0

    print(f"\n[INFO]  Starting embedding + upsert ({total} chunks, batch={BATCH_SIZE})\n")

    for batch_idx in range(n_batches):
        start = batch_idx * BATCH_SIZE
        end = min(start + BATCH_SIZE, total)
        batch = chunks[start:end]

        texts = [c["text"] for c in batch]

        # Embed
        vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        vectors = vectors.tolist()

        # Build Qdrant points
        points = []
        for chunk, vector in zip(batch, vectors):
            points.append(
                PointStruct(
                    id=chunk["chunk_id"],
                    vector=vector,
                    payload={
                        "text":       chunk["text"],
                        "product_id": chunk["product_id"],
                        "review_id":  chunk["review_id"],
                        "rating":     chunk["rating"],
                    },
                )
            )

        # Upsert
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        inserted += len(points)

        print(f"  Batch {batch_idx + 1}/{n_batches} — inserted {len(points)} points")

    # 5. Summary
    info = client.get_collection(COLLECTION_NAME)
    print(f"\n{'=' * 55}")
    print(f"  Pipeline complete")
    print(f"  Inserted : {inserted}")
    print(f"  Total    : {total}")
    print(f"Qdrant points count: {info.points_count}")
    print(f"{'=' * 55}\n")

    client.close()


if __name__ == "__main__":
    run_pipeline()