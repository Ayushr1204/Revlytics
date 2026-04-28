"""
scripts/search.py  —  Production semantic search over laptop review chunks.

Pipeline:
    query → embed → Qdrant search → rerank → filter → group → summarize → answer

Embedding model : all-MiniLM-L6-v2  (dim=384)
Qdrant collection: review_chunks (local on-disk)
"""

import json
import logging
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ── Configuration ─────────────────────────────────────────────────────────────

COLLECTION   = "review_chunks"
EMBED_MODEL  = "all-MiniLM-L6-v2"
TOP_K        = 30           # raw retrieval from Qdrant
RERANK_TOP   = 10           # after re-ranking
DISPLAY_TOP  = 5            # final results shown

SIM_WEIGHT   = 0.7          # similarity contribution
RAT_WEIGHT   = 0.3          # rating contribution

QDRANT_PATH  = Path(__file__).resolve().parent / "qdrant_data"
DATA_ROOT    = Path(__file__).resolve().parent.parent / "data"
REVIEWS_PATH = DATA_ROOT / "reviews.json"

# ── Bootstrap ─────────────────────────────────────────────────────────────────

log.info("Loading model '%s' ...", EMBED_MODEL)
model  = SentenceTransformer(EMBED_MODEL)
client = QdrantClient(path=str(QDRANT_PATH))

PRODUCT_NAMES: dict[str, str] = {}
if REVIEWS_PATH.exists():
    with open(REVIEWS_PATH, "r", encoding="utf-8") as fh:
        for p in json.load(fh).get("products", []):
            PRODUCT_NAMES[p["product_id"]] = p["name"]

log.info("Ready  (%d products loaded)\n", len(PRODUCT_NAMES))


# ══════════════════════════════════════════════════════════════════════════════
#  LOOKUPS  &  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

TOPIC_KEYWORDS = {
    "battery":     ["battery", "charge", "hours", "drain", "lasting", "dies", "lasts"],
    "heat":        ["heat", "hot", "warm", "temperature", "thermal", "overheat", "°c"],
    "performance": ["cpu", "fps", "lag", "performance", "speed", "slow", "fast", "stutter"],
    "noise":       ["noise", "fan", "loud", "db", "quiet", "silent", "decibel"],
    "build":       ["build", "hinge", "flex", "plastic", "premium", "sturdy", "flimsy"],
    "display":     ["display", "screen", "brightness", "color", "nit", "panel", "oled"],
}

TOPIC_LABELS = {
    "battery":     "battery life",
    "heat":        "thermal performance",
    "performance": "processing performance",
    "noise":       "noise levels",
    "build":       "build quality",
    "display":     "display quality",
    "general":     "overall experience",
}

_POS_WORDS = {"good", "great", "best", "excellent", "strong", "impressive",
              "reliable", "amazing", "outstanding", "solid", "long-lasting",
              "smooth", "comfortable", "cool", "quiet", "stellar"}
_NEG_WORDS = {"bad", "poor", "worst", "terrible", "disappointing", "weak",
              "drain", "overheat", "dealbreaker", "struggle", "barely",
              "dies", "frustrating", "uncomfortable", "loud", "unpleasant",
              "painful", "pitiful", "flimsy"}


# ══════════════════════════════════════════════════════════════════════════════
#  UTILITY HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def product_name(pid: str) -> str:
    return PRODUCT_NAMES.get(pid, pid)


def detect_topic(text: str) -> str:
    """Best-match topic for *text*."""
    t = text.lower()
    best, best_n = "general", 0
    for topic, kws in TOPIC_KEYWORDS.items():
        n = sum(1 for kw in kws if kw in t)
        if n > best_n:
            best, best_n = topic, n
    return best


def clean_text(text: str) -> str:
    """Normalize units, capitalize, add period."""
    text = text.strip()
    text = re.sub(r'(\d+\.?\d*)\s*c\b', r'\1°C', text, flags=re.IGNORECASE)
    text = re.sub(r'(\d+\.?\d*)\s*db\b', r'\1 dB', text, flags=re.IGNORECASE)
    if text:
        text = text[0].upper() + text[1:]
    if text and text[-1] not in ".!?":
        text += "."
    return text


def extract_insights(text: str) -> list[str]:
    """Pull numeric facts from chunk text (hours, °C, dB, fps)."""
    patterns = [
        (r'(\d+\.?\d*)\s*hours?',   "{} hours"),
        (r'(\d+\.?\d*)\s*°?c\b',    "{}°C",    re.IGNORECASE),
        (r'(\d+\.?\d*)\s*db\b',     "{} dB",   re.IGNORECASE),
        (r'(\d+\.?\d*)\s*fps',      "{} FPS",  re.IGNORECASE),
    ]
    facts: list[str] = []
    for pat in patterns:
        flags = pat[2] if len(pat) == 3 else 0
        m = re.search(pat[0], text, flags)
        if m:
            facts.append(pat[1].format(m.group(1)))
    return facts


def get_chunk_sentiment(text: str, rating: int) -> str:
    """Classify a single chunk — keywords first, rating fallback."""
    words = set(text.lower().split())
    has_neg = bool(words & _NEG_WORDS)
    has_pos = bool(words & _POS_WORDS)

    if has_neg and not has_pos:
        return "negative"
    if has_pos and not has_neg:
        return "positive"
    if has_neg and has_pos:
        return "negative"        # negative takes priority

    if rating <= 2:
        return "negative"
    if rating >= 4:
        return "positive"
    return "neutral"


# ══════════════════════════════════════════════════════════════════════════════
#  CORE  PIPELINE   (each step is a clean, testable function)
# ══════════════════════════════════════════════════════════════════════════════


# ── 1. Embed ──────────────────────────────────────────────────────────────────

def embed_query(query: str) -> list[float]:
    """Encode a natural-language query into a 384-d vector."""
    return model.encode(query).tolist()


# ── 2. Vector search ─────────────────────────────────────────────────────────

def search_qdrant(query: str,
                  limit: int = TOP_K,
                  product_id: str | None = None) -> list[dict]:
    """Retrieve raw results from Qdrant.

    Optionally filter by *product_id*.
    Returns list of dicts: text, product_id, rating, similarity, topic.
    """
    vec = embed_query(query)

    # Build Qdrant filter if product_id is specified
    qfilter = None
    if product_id:
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        qfilter = Filter(must=[
            FieldCondition(key="product_id", match=MatchValue(value=product_id))
        ])

    response = client.query_points(
        collection_name=COLLECTION,
        query=vec,
        limit=limit,
        query_filter=qfilter,
    )

    results = []
    for pt in response.points:
        p = pt.payload
        results.append({
            "text":       p["text"],
            "product_id": p["product_id"],
            "rating":     p["rating"],
            "similarity": pt.score,
            "topic":      detect_topic(p["text"]),
        })

    log.info("Qdrant returned %d chunks", len(results))
    return results


# ── 3. Re-rank ───────────────────────────────────────────────────────────────

def rerank_results(chunks: list[dict], top_n: int = RERANK_TOP) -> list[dict]:
    """Re-rank by  final_score = similarity×0.7 + (rating/5)×0.3 ."""
    for c in chunks:
        normalized_rating = c["rating"] / 5.0
        c["score"] = round(
            (c["similarity"] * SIM_WEIGHT) + (normalized_rating * RAT_WEIGHT),
            4,
        )
    chunks.sort(key=lambda c: c["score"], reverse=True)
    return chunks[:top_n]


# ── 4. Query intent ──────────────────────────────────────────────────────────

def parse_query(query: str) -> tuple[str | None, str]:
    """Extract (topic, sentiment) from the user query.

    sentiment is 'positive', 'negative', or 'neutral'.
    """
    q = query.lower()

    topic = None
    for t, kws in TOPIC_KEYWORDS.items():
        if any(kw in q for kw in kws):
            topic = t
            break

    words = set(q.split())
    if words & {"great", "good", "best", "excellent", "strong",
                "impressive", "reliable", "amazing"}:
        sentiment = "positive"
    elif words & {"bad", "poor", "worst", "terrible",
                  "disappointing", "weak", "drain"}:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return topic, sentiment


# ── 5. Post-retrieval filter ─────────────────────────────────────────────────

def filter_by_intent(chunks: list[dict],
                     topic: str | None,
                     sentiment: str) -> list[dict]:
    """Keep only chunks matching query intent.  Falls back to all if empty."""
    if topic is None and sentiment == "neutral":
        return chunks

    filtered = []
    for c in chunks:
        if topic and c["topic"] != topic:
            continue
        if sentiment != "neutral":
            if get_chunk_sentiment(c["text"], c["rating"]) != sentiment:
                continue
        filtered.append(c)

    return filtered if filtered else chunks


# ── 6. Group by product ──────────────────────────────────────────────────────

def group_by_product(chunks: list[dict]) -> dict:
    """{ pid: {texts, ratings, topics, scores} }"""
    products: dict = {}
    for c in chunks:
        pid = c["product_id"]
        if pid not in products:
            products[pid] = {"texts": [], "ratings": [], "topics": set(), "scores": []}
        products[pid]["texts"].append(c["text"])
        products[pid]["ratings"].append(c["rating"])
        products[pid]["topics"].add(c["topic"])
        products[pid]["scores"].append(c["score"])
    return products


# ── 7. Product-level sentiment ────────────────────────────────────────────────

def compute_product_sentiment(texts: list[str], ratings: list[int]) -> str:
    """One vote per chunk → majority wins → single label per product."""
    pos = neg = neu = 0
    for txt, rat in zip(texts, ratings):
        s = get_chunk_sentiment(txt, rat)
        if s == "positive":
            pos += 1
        elif s == "negative":
            neg += 1
        else:
            neu += 1

    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


# ── 8. Build product summary ─────────────────────────────────────────────────

def build_product_summary(grouped: dict) -> dict:
    """{pid: {name, sentiment, avg_rating, example, topic, best_score, insights}}"""
    summary = {}
    for pid, d in grouped.items():
        example_text = d["texts"][0]
        summary[pid] = {
            "name":       product_name(pid),
            "sentiment":  compute_product_sentiment(d["texts"], d["ratings"]),
            "avg_rating": round(sum(d["ratings"]) / len(d["ratings"]), 1),
            "example":    clean_text(example_text),
            "topic":      next(iter(d["topics"])),
            "best_score": max(d["scores"]),
            "insights":   extract_insights(example_text),
        }
    return summary


# ── 9. Final answer ──────────────────────────────────────────────────────────

def build_final_answer(product_summary: dict, query: str) -> str:
    """Generate answer purely from product-level sentiment — no query bias."""
    if not product_summary:
        return "No relevant results found for your query."

    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for ps in product_summary.values():
        counts[ps["sentiment"]] += 1

    total = sum(counts.values())
    pos_r = counts["positive"] / total
    neg_r = counts["negative"] / total

    names = [ps["name"] for ps in list(product_summary.values())[:3]]
    names_str = ", ".join(names)

    topic_label = TOPIC_LABELS.get(detect_topic(query), "overall experience")

    if pos_r >= 0.6:
        return (f"Among the products reviewed, {names_str} stand out "
                f"for strong {topic_label}.")
    if neg_r >= 0.6:
        return (f"Products like {names_str} were frequently mentioned "
                f"for {topic_label} concerns by reviewers.")
    return (f"Reviewers gave mixed feedback on {topic_label} "
            f"across products like {names_str}.")


# ══════════════════════════════════════════════════════════════════════════════
#  PUBLIC  API   (consumed by app.py / Streamlit)
# ══════════════════════════════════════════════════════════════════════════════


def search_and_summarize(query: str, product_id: str | None = None) -> dict:
    """Full pipeline: search → rerank → filter → group → summarize.

    Returns::

        {
            "results":      [ {product_name, product_id, rating, text,
                               topic, score, sentiment_label} ],
            "summary":      [ str, ... ],
            "final_answer":  str,
            "metadata":     { topics, topic_sentiments, contrast }
        }
    """

    # Step 1 – vector search
    raw = search_qdrant(query, product_id=product_id)
    if not raw:
        t = detect_topic(query)
        return _empty_response(t)

    # Step 2 – re-rank  (similarity × 0.7 + rating × 0.3)
    ranked = rerank_results(raw)

    # Step 3 – filter by query intent
    topic, sentiment = parse_query(query)
    filtered = filter_by_intent(ranked, topic, sentiment)

    # Step 4 – group by product
    grouped = group_by_product(filtered)

    # Step 5 – product-level summary
    product_summary = build_product_summary(grouped)

    # Sort products by best_score
    sorted_pids = sorted(
        product_summary,
        key=lambda pid: product_summary[pid]["best_score"],
        reverse=True,
    )

    # ── results list (one per product, for UI cards) ──────────────────────
    results = []
    for pid in sorted_pids[:DISPLAY_TOP]:
        ps = product_summary[pid]
        insight_str = ""
        if ps["insights"]:
            insight_str = "  (" + ", ".join(ps["insights"]) + ")"
        results.append({
            "product_name":    ps["name"],
            "product_id":      pid,
            "rating":          int(ps["avg_rating"]),
            "text":            ps["example"] + insight_str,
            "topic":           ps["topic"],
            "score":           ps["best_score"],
            "sentiment_label": ps["sentiment"],
        })

    # ── summary bullets ───────────────────────────────────────────────────
    summary = []
    for pid in sorted_pids[:DISPLAY_TOP]:
        ps = product_summary[pid]
        tl = TOPIC_LABELS.get(ps["topic"], ps["topic"])
        insight = f" ({', '.join(ps['insights'])})" if ps["insights"] else ""
        if ps["sentiment"] == "positive":
            summary.append(f"{ps['name']} shows strong {tl}{insight}.")
        elif ps["sentiment"] == "negative":
            summary.append(f"{ps['name']} has {tl} concerns{insight}.")
        else:
            summary.append(f"{ps['name']} shows mixed {tl}{insight}.")

    # ── final answer ──────────────────────────────────────────────────────
    final_answer = build_final_answer(product_summary, query)

    # ── metadata (backward compat with app.py) ────────────────────────────
    q_topic = topic if topic else detect_topic(query)

    return {
        "results":     results,
        "summary":     summary,
        "final_answer": final_answer,
        "metadata": {
            "topics":          [q_topic],
            "topic_sentiments": {q_topic: sentiment},
            "contrast":        False,
        },
    }


def _empty_response(topic: str) -> dict:
    return {
        "results": [],
        "summary": [],
        "final_answer": "No relevant results found for your query.",
        "metadata": {
            "topics": [topic],
            "topic_sentiments": {topic: "neutral"},
            "contrast": False,
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
#  CLI  DISPLAY
# ══════════════════════════════════════════════════════════════════════════════


def display_results(product_summary: dict, query: str):
    """Pretty-print results for terminal use."""

    if not product_summary:
        print("  No relevant information found.\n")
        return

    sorted_items = sorted(
        product_summary.items(),
        key=lambda kv: kv[1]["best_score"],
        reverse=True,
    )

    # ── Top Results ───────────────────────────────────────────────────────
    print("\n  Top Results:\n")
    for i, (pid, ps) in enumerate(sorted_items[:DISPLAY_TOP], 1):
        stars = "⭐" * int(ps["avg_rating"])
        insights = ""
        if ps["insights"]:
            insights = "  📊 " + ", ".join(ps["insights"])
        print(f"  {i}. {ps['name']} [{pid}]  {stars}  (score: {ps['best_score']:.4f})")
        print(f"     {ps['example']}{insights}")
        print()

    # ── Summary ───────────────────────────────────────────────────────────
    print("  Summary:\n")
    for pid, ps in sorted_items[:DISPLAY_TOP]:
        tl = TOPIC_LABELS.get(ps["topic"], ps["topic"])
        s = ps["sentiment"]
        tag = "strong" if s == "positive" else ("concerns" if s == "negative" else "mixed")
        print(f"  • {ps['name']} [{pid}] → {tag} {tl}")

    # ── Final Answer ──────────────────────────────────────────────────────
    print(f"\n  Final Answer:\n")
    print(f"  {build_final_answer(product_summary, query)}")
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  CLI  ENTRY  POINT
# ══════════════════════════════════════════════════════════════════════════════


def search(query: str):
    """CLI search — full pipeline."""
    topic, sentiment = parse_query(query)

    print(f"  Query:      {query}")
    print(f"  Topic:      {topic or 'general'}")
    print(f"  Sentiment:  {sentiment}")
    print()

    raw = search_qdrant(query)
    if not raw:
        print("  No results found.\n")
        return

    ranked = rerank_results(raw)
    filtered = filter_by_intent(ranked, topic, sentiment)
    grouped = group_by_product(filtered)
    product_summary = build_product_summary(grouped)
    display_results(product_summary, query)


# ── Interactive loop ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  Amazon OTDS — AI Review Intelligence")
    print("  Type a question, or 'quit' to exit")
    print("=" * 60)

    while True:
        query = input("\n🔍 Query: ").strip()
        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        search(query)
