import json
import re

INPUT_FILE = "C:\\Users\\ayush\\OneDrive\\Desktop\\Amazon_OTDS\\data\\review_chunks_clean.json"
OUTPUT_FILE = "C:\\Users\\ayush\\OneDrive\\Desktop\\Amazon_OTDS\\data\\review_chunks_enriched.json"

# ---------------- TOPIC DETECTION ----------------
TOPIC_KEYWORDS = {
    "battery": ["battery", "hours", "charge"],
    "thermal": ["temp", "thermal", "°c", "heat", "warm"],
    "noise": ["fan", "db", "noise", "loud", "quiet"],
    "performance": ["fps", "lag", "ms", "performance", "speed"],
    "build": ["build", "hinge", "chassis", "flex", "quality"],
}

def detect_topic(text):
    text = text.lower()
    for topic, words in TOPIC_KEYWORDS.items():
        if any(w in text for w in words):
            return topic
    return "general"


# ---------------- SENTIMENT DETECTION ----------------
def extract_number(text):
    nums = re.findall(r"\d+\.?\d*", text)
    return float(nums[0]) if nums else None


def detect_sentiment(text):
    text = text.lower()

    # strong negative words
    if any(w in text for w in ["dealbreaker", "barely", "unusable", "poor", "bad"]):
        return "negative"

    # strong positive words
    if any(w in text for w in ["excellent", "great", "amazing", "solid", "impressive"]):
        return "positive"

    # battery logic
    if "hour" in text:
        num = extract_number(text)
        if num:
            if num >= 8:
                return "positive"
            elif num <= 4:
                return "negative"
            else:
                return "neutral"

    # temperature logic
    if "°c" in text or "c" in text:
        num = extract_number(text)
        if num:
            if num >= 50:
                return "negative"
            elif num <= 40:
                return "positive"
            else:
                return "neutral"

    return "neutral"


# ---------------- MAIN ----------------
def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    enriched = []

    for chunk in data["chunks"]:
        text = chunk["text"]

        topic = detect_topic(text)
        sentiment = detect_sentiment(text)

        chunk["topic"] = topic
        chunk["sentiment"] = sentiment

        enriched.append(chunk)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"chunks": enriched}, f, indent=2)

    print("✅ Enriched dataset created")
    print(f"Total chunks: {len(enriched)}")


if __name__ == "__main__":
    main()