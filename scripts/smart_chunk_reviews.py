import json
import uuid
import re

# ---------- CONFIG ----------
INPUT_FILE = "c:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/reviews_humanized.json"
OUTPUT_FILE = "c:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/review_chunks_clean.json"

MIN_WORDS = 2     # ultra-light filter
MAX_WORDS = 40

FILLER_WORDS = [
    "idk", "tbh", "kinda", "ngl",
    "sort of", "a bit", "pretty much",
    "honestly", "for me"
]

# ---------- CLEANING ----------
def clean_text(text):
    text = text.lower()

    for word in FILLER_WORDS:
        text = text.replace(word, "")

    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_text(text):
    text = text.strip()

    if text:
        text = text[0].upper() + text[1:]

    return text


# ---------- SPLITTING ----------
def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)


def split_long_sentence(sentence):
    words = sentence.split()
    chunks = []

    for i in range(0, len(words), MAX_WORDS):
        chunk = " ".join(words[i:i + MAX_WORDS])
        chunks.append(chunk)

    return chunks


# ---------- FILTER (OPTION C - MINIMAL ONLY) ----------
def is_good_chunk(text):
    words = text.split()

    # Only remove useless garbage like "ok", "nice"
    if len(words) < MIN_WORDS:
        return False

    return True


# ---------- PROCESS ----------
def process_review(text):
    text = clean_text(text)
    sentences = split_sentences(text)

    final_chunks = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        # Split long sentences
        if len(sentence.split()) > MAX_WORDS:
            parts = split_long_sentence(sentence)
        else:
            parts = [sentence]

        for chunk in parts:
            chunk = normalize_text(chunk)

            if is_good_chunk(chunk):
                final_chunks.append(chunk)

    return final_chunks


# ---------- MAIN ----------
def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunked_data = []

    for review in data["reviews"]:
        review_id = review["review_id"]
        product_id = review["product_id"]
        rating = review["rating"]

        chunks = process_review(review["text"])

        for i, chunk in enumerate(chunks):
            chunked_data.append({
                "chunk_id": str(uuid.uuid4()),
                "review_id": review_id,
                "product_id": product_id,
                "rating": rating,
                "chunk_index": i,
                "text": chunk,
                "length": len(chunk.split())   # ⭐ useful for ranking later
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunked_data}, f, indent=2)

    print("✅ Chunking complete (minimal filtering)")
    print(f"Total chunks: {len(chunked_data)}")


if __name__ == "__main__":
    main()