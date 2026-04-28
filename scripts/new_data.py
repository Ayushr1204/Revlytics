import json
import ast
import uuid
import random
from datetime import datetime

# -------- FILE PATHS --------
REVIEWS_FILE = r"C:\Users\ayush\OneDrive\Desktop\Amazon_OTDS\dataset\reviews_Electronics.json"
META_FILE = r"C:\Users\ayush\OneDrive\Desktop\Amazon_OTDS\dataset\meta_Electronics.json"
OUTPUT_FILE = r"C:\Users\ayush\OneDrive\Desktop\Amazon_OTDS\data\otds_dataset.json"

# -------- CONFIG --------
MAX_PRODUCTS = 50
REVIEWS_PER_PRODUCT = (20, 40)

# -------- SAFE PARSER --------
def parse_line(line):
    try:
        return json.loads(line)
    except:
        try:
            return ast.literal_eval(line)
        except:
            return None

# -------- CATEGORY --------
def map_category(cat):
    c = cat.lower()

    if "laptop" in c or "computer" in c:
        return "laptops"
    if "phone" in c:
        return "smartphones"
    if "headphone" in c or "audio" in c:
        return "headphones"
    if "monitor" in c or "display" in c:
        return "monitors"
    if "keyboard" in c:
        return "keyboards"

    return "general"

# -------- CLEAN --------
def clean_review(text):
    if not text:
        return None

    text = text.replace("\n", " ").strip()

    if len(text.split(".")) < 2:
        return None

    if len(text.split()) < 20:
        return None

    return text

# -------- ENRICH --------
def enrich(text):
    t = text.lower()
    additions = []

    if "battery" not in t:
        additions.append(f"Battery lasts around {round(random.uniform(4,10),1)} hours during regular use.")

    if "°c" not in t and "temperature" not in t:
        additions.append(f"Temperature reaches about {random.randint(40,48)}°C under load.")

    if "db" not in t and "noise" not in t:
        additions.append(f"Fan noise peaks near {random.randint(35,55)} dB.")

    if "fps" not in t:
        additions.append(f"Performance stays around {random.randint(50,120)} FPS during gaming.")

    if "lag" not in t:
        additions.append(f"Lag spikes up to {random.randint(100,300)} ms when multitasking.")

    if additions:
        text += " " + random.choice(additions)

    return text

# -------- TOPIC --------
def classify_topic(text):
    t = text.lower()

    if "battery" in t or "hours" in t:
        return "battery"
    if "°c" in t or "temperature" in t:
        return "heat"
    if "db" in t or "noise" in t:
        return "noise"
    if "fps" in t or "lag" in t:
        return "performance"
    if "build" in t:
        return "build"
    if "display" in t:
        return "display"

    return "general"

# -------- SENTIMENT --------
def classify_sentiment(text):
    t = text.lower()

    if any(x in t for x in ["9 hours", "8 hours", "smooth", "stable"]):
        return "positive"

    if any(x in t for x in ["3 hours", "48°c", "50 dB", "lag spikes"]):
        return "negative"

    return "neutral"

# -------- MAIN --------
def generate_dataset():

    meta_map = {}

    with open(META_FILE, "r", encoding="utf-8") as f:
        for line in f:
            m = parse_line(line)
            if not m or "asin" not in m:
                continue
            meta_map[m["asin"]] = m

    products = []
    asin_to_pid = {}
    pid = 1

    for asin, m in meta_map.items():
        if pid > MAX_PRODUCTS:
            break

        category_raw = m.get("categories", [["general"]])[0][0]
        category = map_category(category_raw)

        product = {
            "product_id": f"p{pid:05}",
            "name": m.get("title", f"Product {asin}"),
            "category": category
        }

        products.append(product)
        asin_to_pid[asin] = product["product_id"]
        pid += 1

    reviews = []
    chunks = []
    product_review_count = {p["product_id"]: 0 for p in products}

    rid = 1

    with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            r = parse_line(line)
            if not r or "asin" not in r:
                continue

            if r["asin"] not in asin_to_pid:
                continue

            pid_val = asin_to_pid[r["asin"]]

            if product_review_count[pid_val] >= random.randint(*REVIEWS_PER_PRODUCT):
                continue

            text = clean_review(r.get("reviewText"))
            if not text:
                continue

            text = enrich(text)

            review = {
                "review_id": f"r{rid:07}",
                "product_id": pid_val,
                "text": text,
                "rating": int(r.get("overall", 3)),
                "created_at": datetime.fromtimestamp(r["unixReviewTime"]).strftime("%Y-%m-%d")
            }

            reviews.append(review)
            product_review_count[pid_val] += 1

            sentences = [s.strip() for s in text.split(".") if len(s.split()) >= 6]

            for s in sentences:
                chunks.append({
                    "chunk_id": f"c{uuid.uuid4().hex[:10]}",
                    "review_id": review["review_id"],
                    "product_id": pid_val,
                    "text": s,
                    "topic": classify_topic(s),
                    "sentiment": classify_sentiment(s),
                    "embedding": []
                })

            rid += 1

    return {
        "products": products,
        "reviews": reviews,
        "review_chunks": chunks
    }

# -------- RUN --------
if __name__ == "__main__":
    dataset = generate_dataset()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print("✅ OTDS dataset generated successfully!")