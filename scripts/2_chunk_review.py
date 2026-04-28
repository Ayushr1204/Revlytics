import json
import uuid
import re

# ---------- PATHS ----------
INPUT_FILE = "C:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/synthetic_laptop_reviews.json"
OUTPUT_FILE = "C:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/review_chunks_clean.json"

def get_sentiment(text, rating):
    t = text.lower()

    # 🔴 STRONG NEGATIVE FIRST
    if any(w in t for w in [
        "bad", "poor", "struggles", "heats", "loud",
        "bulky", "dull", "not the best", "could be better",
        "limiting", "drops"
    ]):
        return "negative"

    # 🟢 POSITIVE
    if any(w in t for w in [
        "good", "great", "smooth", "sharp", "excellent",
        "solid", "premium", "easy", "quiet"
    ]):
        return "positive"

    # ⚖️ fallback to rating
    if rating >= 4:
        return "positive"
    elif rating <= 2:
        return "negative"
    else:
        return "neutral"


# ---------- SENTENCE SPLIT ----------
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.split()) > 5]


# ---------- TOPIC DETECTION ----------
def detect_topic(text):
    t = text.lower()

    if "battery" in t or "hours" in t:
        return "battery"
    if "heat" in t or "temperature" in t or "cool" in t:
        return "thermal"
    if "fps" in t or "performance" in t:
        return "performance"
    if "display" in t or "screen" in t or "panel" in t:
        return "display"
    if "fan" in t or "noise" in t:
        return "noise"
    if "keyboard" in t or "trackpad" in t:
        return "keyboard"
    if "kg" in t or "weight" in t:
        return "portability"
    if "ram" in t or "storage" in t:
        return "storage"
    if "build" in t or "chassis" in t:
        return "build"
    if "price" in t or "value" in t or "cost" in t:
        return "value"

    return "general"


# ---------- MAIN ----------
def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunked_data = []

    for review in data["reviews"]:
        review_id = review["review_id"]
        product_id = review["product_id"]
        product_name = review.get("product_name", "")
        rating = review["rating"]
        sentiment = review["sentiment"]

        sentences = split_sentences(review["text"])

        for i, sentence in enumerate(sentences):
            topic = detect_topic(sentence)

            # 🔥 REMOVE USELESS CHUNKS
            if topic == "general":
                continue

            chunk_sentiment = get_sentiment(sentence, rating)

            chunked_data.append({
                "chunk_id": str(uuid.uuid4()),
                "review_id": review_id,
                "product_id": product_id,
                "product_name": product_name,
                "chunk_index": i,
                "text": sentence,
                "rating": rating,
                "topic": topic,
                "sentiment": chunk_sentiment   # ✅ FIXED
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunked_data}, f, indent=2)

    print("✅ Clean chunking complete")
    print(f"Total chunks: {len(chunked_data)}")


if __name__ == "__main__":
    main()