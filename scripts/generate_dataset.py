import json, random, re
from datetime import datetime, timedelta
from product_names import NAMES
from templates import T, TOPICS, RANGES, CHUNK_TOPIC_MAP

random.seed(42)

def rval(key):
    lo, hi = RANGES[key]
    if isinstance(lo, float):
        return round(random.uniform(lo, hi), 1)
    return random.randint(lo, hi)

def gen_products():
    products = []
    pid = 1
    for cat in ["laptops","smartphones","headphones","monitors"]:
        for name in NAMES[cat]:
            products.append({"product_id":f"p{pid:03d}","name":name,"category":cat})
            pid += 1
    return products

def pick_sentiment():
    r = random.random()
    if r < 0.3: return "pos"
    elif r < 0.7: return "neu"
    else: return "neg"

def rating_from_sentiment(s):
    if s == "pos": return random.choice([4,5])
    elif s == "neu": return random.choice([3,3,3,4])
    else: return random.choice([1,2,2])

def fill_template(tmpl, name, cat, topic, sent):
    s = tmpl.replace("{n}", name)
    # Fill {v} based on topic
    vmap = {
        "battery": f"battery_{sent}",
        "heat": f"temp_{sent}",
        "noise": f"noise_{sent}",
        "performance": None,
        "build": None,
        "camera": None,
        "display": None,
        "comfort": None,
        "anc": None,
        "brightness": f"bright_{sent}",
        "refresh": f"refresh_{sent}",
        "color": None,
    }
    vkey = vmap.get(topic)
    if "{v}" in s:
        if vkey:
            s = s.replace("{v}", str(rval(vkey)))
        elif topic == "performance":
            # pick fps or lag or cpu depending on template content
            if "FPS" in s or "fps" in s:
                s = s.replace("{v}", str(rval(f"fps_{sent}")))
            elif "ms" in s or "lag" in s.lower():
                s = s.replace("{v}", str(rval(f"lag_{sent}")))
            elif "CPU" in s or "%" in s:
                s = s.replace("{v}", str(rval(f"cpu_{sent}")))
            else:
                s = s.replace("{v}", str(rval(f"fps_{sent}")))
    if "{v2}" in s:
        if topic == "performance":
            if "CPU" in s or "%" in s:
                s = s.replace("{v2}", str(rval(f"cpu_{sent}")))
            elif "FPS" in s:
                s = s.replace("{v2}", str(rval(f"fps_{sent}")))
            else:
                s = s.replace("{v2}", str(rval(f"cpu_{sent}")))
    return s

def random_date():
    start = datetime(2023, 1, 1)
    end = datetime(2026, 4, 1)
    delta = end - start
    d = start + timedelta(days=random.randint(0, delta.days))
    return d.strftime("%Y-%m-%d")

def split_to_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 10]

def classify_chunk_sentiment(sentence):
    neg_words = ["rough","poor","disappointing","barely","frustrating","weak","cheap",
                 "flimsy","uncomfortable","sluggish","lag","drains","dies","struggles",
                 "pain","worse","horrible","unbearable","hot","overheat","crack","broke",
                 "fuzzy","washed","dull","choppy","wobbl","creak","flimsily","distort",
                 "harsh","hollow","nonexistent","useless","impossible","unacceptable",
                 "forces","miserable","hurting","worry","defeat","hiss","bleed","uneven"]
    pos_words = ["excellent","impressive","outstanding","stunning","solid","premium",
                 "comfortable","smooth","crisp","beautiful","stellar","incredible",
                 "perfect","easily","pleasure","confident","durable","exceptional",
                 "vivid","gorgeous","buttery","immersive","precise","naturally",
                 "weightless","peaceful","reliable","plush","satisfying","wow",
                 "fluid","remarkable","purposeful","inspire"]
    low = sentence.lower()
    neg_count = sum(1 for w in neg_words if w in low)
    pos_count = sum(1 for w in pos_words if w in low)
    if neg_count > pos_count: return "negative"
    elif pos_count > neg_count: return "positive"
    return "neutral"

def infer_chunk_topic(sentence, category, review_topics):
    low = sentence.lower()
    kw_map = {
        "battery": ["battery","charge","hour","charger","dies","drain","lasts"],
        "performance": ["fps","lag","cpu","stutter","frame","multitask","smooth","compil",
                       "docker","switching","app","load","speed","choke"],
        "heat": ["heat","thermal","temperature","warm","cool","hot","overheat","°c"," c "],
        "noise": ["noise","fan","db","loud","silent","quiet","acoustic","pitch","whisper"],
        "build": ["build","hinge","creak","flex","chassis","material","plastic","metal",
                  "premium","flimsy","snap","wobbl","bezel","cable","fold","pad"],
        "display": ["display","screen","panel","pixel","bright","nit","color","black",
                    "viewing","resolution","text","image","hdr","backlight","banding"],
        "audio": ["sound","bass","treble","audio","vocal","soundstage","music","clarity",
                  "anc","noise cancellation","cancell","hiss","immersive","distort"],
        "camera": ["camera","photo","portrait","autofocus","bokeh","video","stabiliz",
                   "night shot","grain","snap","megapixel"],
        "general": [],
    }
    scores = {}
    for topic, kws in kw_map.items():
        scores[topic] = sum(1 for kw in kws if kw in low)
    best = max(scores, key=scores.get)
    if scores[best] > 0:
        return CHUNK_TOPIC_MAP.get(best, best)
    # fallback to review topics
    if review_topics:
        return CHUNK_TOPIC_MAP.get(review_topics[0], "general")
    return "general"

def generate_all():
    products = gen_products()
    reviews = []
    chunks = []
    rid = 1
    cid = 1

    for prod in products:
        cat = prod["category"]
        name = prod["name"]
        num_reviews = random.randint(20, 40)
        topics_list = TOPICS[cat]

        for _ in range(num_reviews):
            sentiment = pick_sentiment()
            rating = rating_from_sentiment(sentiment)
            num_sentences = random.randint(2, 4)

            # Pick 2-3 distinct topics for this review
            num_topics = min(random.randint(2, 3), num_sentences)
            chosen_topics = random.sample(topics_list, num_topics)

            # Sometimes mix sentiments within a review
            sentences = []
            review_topic_list = []
            for i in range(num_sentences):
                topic = chosen_topics[i % len(chosen_topics)]
                # 20% chance of flipping sentiment for mixed reviews
                if random.random() < 0.2:
                    s_options = ["pos","neu","neg"]
                    s_options.remove(sentiment)
                    s = random.choice(s_options)
                else:
                    s = sentiment

                tmpls = T[cat][topic][s]
                tmpl = random.choice(tmpls)
                sent_text = fill_template(tmpl, name, cat, topic, s)
                sentences.append(sent_text)
                review_topic_list.append(topic)

            # Ensure sentences end with period
            full_text = ". ".join(s.rstrip(".") for s in sentences) + "."

            review = {
                "review_id": f"r{rid:04d}",
                "product_id": prod["product_id"],
                "text": full_text,
                "rating": rating,
                "created_at": random_date()
            }
            reviews.append(review)

            # Generate chunks
            raw_sents = split_to_sentences(full_text)
            for sent in raw_sents:
                words = sent.split()
                if len(words) < 4:
                    continue
                chunk_topic = infer_chunk_topic(sent, cat, review_topic_list)
                chunk_sent = classify_chunk_sentiment(sent)
                chunk = {
                    "chunk_id": f"c{cid:05d}",
                    "review_id": review["review_id"],
                    "product_id": prod["product_id"],
                    "text": sent if sent.endswith(".") else sent + ".",
                    "topic": chunk_topic,
                    "sentiment": chunk_sent
                }
                chunks.append(chunk)
                cid += 1

            rid += 1

    return {"products": products, "reviews": reviews, "review_chunks": chunks}

if __name__ == "__main__":
    print("Generating dataset...")
    data = generate_all()
    print(f"Products: {len(data['products'])}")
    print(f"Reviews: {len(data['reviews'])}")
    print(f"Chunks: {len(data['review_chunks'])}")

    with open("dataset.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved to dataset.json")
