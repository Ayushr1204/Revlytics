<![CDATA[# Revlytics — AI-Powered Review Intelligence

> Semantic search engine for laptop product reviews, powered by vector embeddings and intelligent re-ranking.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC382D)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-FF6F00?logo=huggingface&logoColor=white)

---

## Overview

Revlytics is a semantic review intelligence platform that lets users search through laptop product reviews using natural language queries. Instead of simple keyword matching, it uses **vector embeddings** to understand the *meaning* behind queries like _"great battery life"_ or _"overheating issues"_, returning the most relevant products with AI-generated summaries.

### Key Features

- **Semantic Search** — Queries are embedded using `all-MiniLM-L6-v2` and matched against review chunks stored in Qdrant
- **Intelligent Re-ranking** — Results are scored using a weighted formula: `similarity × 0.7 + normalized_rating × 0.3`
- **Query Intent Parsing** — Automatically detects topic (battery, heat, performance, noise, build, display) and sentiment (positive/negative/neutral) from natural language
- **Post-Retrieval Filtering** — Filters results by detected topic and sentiment to match user intent
- **Product-Level Aggregation** — Groups chunk-level results by product to eliminate bias and provide per-product summaries
- **AI Summary Generation** — Produces concise, structured insights and a final answer for each query
- **Dual Frontend** — Both a Streamlit app and a custom FastAPI + vanilla JS frontend

---

## Architecture

```
query → embed (MiniLM-L6-v2) → Qdrant vector search (top-30)
      → re-rank (similarity + rating)
      → intent filter (topic + sentiment)
      → group by product
      → summarize → final answer
```

---

## Tech Stack

| Layer       | Technology                              |
|-------------|----------------------------------------|
| Embeddings  | `all-MiniLM-L6-v2` (384-dim)          |
| Vector DB   | Qdrant (local on-disk)                 |
| Backend     | FastAPI + Uvicorn                      |
| Frontend    | Vanilla HTML/CSS/JS, Streamlit         |
| Language    | Python 3.10+                           |

---

## Project Structure

```
├── app.py                    # Streamlit frontend
├── backend/
│   ├── main.py               # FastAPI server (serves API + static frontend)
│   ├── config.py             # Environment configuration
│   ├── embeddings.py         # Embedding utilities
│   ├── intent_parser.py      # Query intent extraction
│   ├── semantic_ranker.py    # Re-ranking logic
│   ├── review_summarizer.py  # Summary generation
│   ├── review_qa_rag.py      # RAG-based Q&A
│   └── models/               # Pydantic request/response models
├── frontend/
│   └── static/
│       ├── index.html        # Custom HTML frontend
│       ├── styles.css         # Styling
│       └── script.js          # Client-side logic
├── scripts/
│   ├── search.py             # Core search pipeline
│   ├── 1_generate_dataset.py # Synthetic review generation
│   ├── 2_chunk_review.py     # Review chunking
│   └── 3_embed_and_store.py  # Embedding + Qdrant indexing
├── data/                     # Review datasets (JSON)
└── assets/                   # Static assets (logo, etc.)
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Ayushr1204/Revlytics.git
cd Revlytics

# Create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
QDRANT_URL=your_qdrant_url        # optional, defaults to local
QDRANT_API_KEY=your_qdrant_key    # optional, defaults to local
```

### Data Pipeline

Run these scripts in order to prepare the review data:

```bash
python scripts/1_generate_dataset.py    # Generate synthetic laptop reviews
python scripts/2_chunk_review.py        # Chunk reviews into passages
python scripts/3_embed_and_store.py     # Embed chunks and index into Qdrant
```

### Running the App

**Option 1 — FastAPI (custom frontend):**
```bash
uvicorn backend.main:app --reload
# Open http://localhost:8000
```

**Option 2 — Streamlit:**
```bash
streamlit run app.py
# Open http://localhost:8501
```

**Option 3 — CLI:**
```bash
python scripts/search.py
# Interactive search in the terminal
```

---

## API

### `POST /api/search`

```json
{
  "query": "great battery life",
  "product_id": null
}
```

**Response:**

```json
{
  "results": [
    {
      "product_name": "...",
      "product_id": "...",
      "rating": 4,
      "text": "...",
      "topic": "battery",
      "score": 0.8523,
      "sentiment_label": "positive"
    }
  ],
  "summary": ["Product X shows strong battery life (8 hours)."],
  "final_answer": "Among the products reviewed, Product X stands out for strong battery life.",
  "metadata": {
    "topics": ["battery"],
    "topic_sentiments": {"battery": "positive"}
  }
}
```

### `GET /health`

Returns `{"status": "ok"}`

---

## License

This project is for educational and research purposes.
]]>
