import json
import random
import uuid

OUTPUT_FILE = "C:\\Users\\ayush\\OneDrive\\Desktop\\Amazon_OTDS\\data\\synthetic_laptop_reviews.json"

NUM_PRODUCTS = 50
REVIEWS_PER_PRODUCT = (30, 40)

BRANDS = ["ZenBook", "ThinkMate", "GameForge", "CreatorBook", "NimbusBook", "UltraNote", "CodeBook"]
SUFFIX = ["Pro", "Edge", "Ultra", "Flex", "Vision", "Strike", "Air"]

ENDINGS = [
    "Overall, it meets my expectations.",
    "Overall, it's a decent machine for the price.",
    "In the end, it works fine for my needs.",
    "Not perfect, but gets the job done.",
    "I would still recommend it for casual use."
]


def generate_product_name():
    return f"{random.choice(BRANDS)} {random.choice(SUFFIX)} {random.randint(13,17)}"


def generate_review(product_id, product_name):
    aspects = [
        "battery", "thermal", "performance", "display",
        "build", "noise", "keyboard", "portability",
        "storage", "value"
    ]

    chosen_aspects = random.sample(aspects, random.randint(2, 4))

    sentiment = random.choices(
        ["positive", "negative", "neutral"],
        weights=[0.4, 0.3, 0.3]
    )[0]

    sentences = []
    asp_sentiment_map = {}  # 🔥 track per-aspect sentiment

    for asp in chosen_aspects:
        if sentiment == "positive":
            asp_sentiment = random.choices(["positive", "neutral"], weights=[0.7, 0.3])[0]
        elif sentiment == "negative":
            asp_sentiment = random.choices(["negative", "neutral"], weights=[0.7, 0.3])[0]
        else:
            asp_sentiment = random.choice(["positive", "neutral", "negative"])

        asp_sentiment_map[asp] = asp_sentiment

        # ---------- BATTERY ----------
        if asp == "battery":
            if asp_sentiment == "positive":
                hrs = round(random.uniform(7, 10.5), 1)
            elif asp_sentiment == "negative":
                hrs = round(random.uniform(2.5, 5), 1)
            else:
                hrs = round(random.uniform(5, 7), 1)

            if asp_sentiment == "positive":
                sentences.append(f"I get around {hrs} hours of battery which easily lasts through my day")
            elif asp_sentiment == "negative":
                sentences.append(f"Battery life is poor, barely reaching {hrs} hours")
            else:
                sentences.append(f"Battery life sits around {hrs} hours which feels average")

        # ---------- THERMAL ----------
        elif asp == "thermal":
            temp = random.randint(35, 60)

            if asp_sentiment == "positive":
                sentences.append(f"It stays cool with temperatures around {temp}°C under load")
            elif asp_sentiment == "negative":
                sentences.append(f"It heats up quickly and reaches about {temp}°C")
            else:
                sentences.append(f"Thermals hover around {temp}°C which is acceptable")

        # ---------- PERFORMANCE ----------
        elif asp == "performance":
            if asp_sentiment == "positive":
                fps = random.randint(80, 140)
            elif asp_sentiment == "negative":
                fps = random.randint(30, 70)
            else:
                fps = random.randint(60, 90)

            if asp_sentiment == "positive":
                sentences.append(f"Performance is smooth and handles tasks easily with around {fps} fps in games")
            elif asp_sentiment == "negative":
                sentences.append(f"Performance drops under load and struggles around {fps} fps")
            else:
                sentences.append(f"Performance is decent but not exceptional at around {fps} fps")

        # ---------- DISPLAY ----------
        elif asp == "display":
            sentences.append(random.choice([
                "The display is sharp with good colors",
                "Screen quality is decent but not very bright",
                "Display looks vibrant and clear",
                "The panel feels a bit dull compared to others"
            ]))

        # ---------- BUILD ----------
        elif asp == "build":
            sentences.append(random.choice([
                "Build quality feels solid and premium",
                "There is some flex in the chassis",
                "The design feels sturdy and well built",
                "Build quality is average for the price"
            ]))

        # ---------- NOISE ----------
        elif asp == "noise":
            db = random.randint(30, 55)

            if asp_sentiment == "positive":
                sentences.append(f"Fan noise stays around {db} dB and is barely noticeable")
            elif asp_sentiment == "negative":
                sentences.append(f"Fans get loud reaching around {db} dB under load")
            else:
                sentences.append(f"Noise levels are manageable most of the time")

        # ---------- KEYBOARD ----------
        elif asp == "keyboard":
            sentences.append(random.choice([
                "Typing feels comfortable with good key travel",
                "Keyboard is a bit shallow but usable",
                "Trackpad is responsive and smooth",
                "Keyboard could be better for long typing sessions"
            ]))

        # ---------- PORTABILITY ----------
        elif asp == "portability":
            if asp_sentiment == "positive":
                weight = round(random.uniform(1.2, 1.6), 1)
            elif asp_sentiment == "negative":
                weight = round(random.uniform(2.0, 2.5), 1)
            else:
                weight = round(random.uniform(1.5, 2.0), 1)

            if asp_sentiment == "positive":
                sentences.append(f"It weighs around {weight} kg and is easy to carry")
            elif asp_sentiment == "negative":
                sentences.append(f"It feels bulky at around {weight} kg")
            else:
                sentences.append(f"It weighs about {weight} kg which is manageable")

        # ---------- STORAGE ----------
        elif asp == "storage":
            if asp_sentiment == "positive":
                ram = random.choice([16, 32])
                sentences.append(f"{ram}GB RAM is enough for my workflow")
            elif asp_sentiment == "negative":
                ram = random.choice([8])
                sentences.append(f"{ram}GB RAM feels limiting for heavy tasks")
            else:
                ram = random.choice([8, 16])
                sentences.append(f"{ram}GB RAM works fine for most use cases")

        # ---------- VALUE ----------
        elif asp == "value":
            sentences.append(random.choice([
                "Overall, it feels worth the price",
                "Not the best value for money",
                "Pricing seems fair for what it offers",
                "Could be better considering the cost"
            ]))

    # ---------- FINAL TEXT ----------
    context = random.choice([
        "during my daily work",
        "while traveling",
        "for coding and browsing",
        "during long sessions"
    ])

    ending = random.choice(ENDINGS)

    review_text = (
        f"I have been using the {product_name} {context}. "
        + ". ".join(sentences)
        + ". "
        + ending
    )

    # ---------- RATING FROM ACTUAL CONTENT ----------
    score = 0
    for s in asp_sentiment_map.values():
        if s == "positive":
            score += 1
        elif s == "negative":
            score -= 1

    if score >= 2:
        rating = random.uniform(4.2, 5.0)
    elif score == 1:
        rating = random.uniform(3.5, 4.2)
    elif score == 0:
        rating = random.uniform(2.5, 3.5)
    elif score == -1:
        rating = random.uniform(1.8, 2.5)
    else:
        rating = random.uniform(1.0, 1.8)

    if rating >= 4:
        final_sentiment = "positive"
    elif rating <= 2:
        final_sentiment = "negative"
    else:
        final_sentiment = "neutral"

    return {
        "review_id": str(uuid.uuid4()),
        "product_id": product_id,
        "product_name": product_name,
        "text": review_text,
        "rating": round(rating, 1),
        "topic": chosen_aspects[0],
        "sentiment": final_sentiment
    }


def main():
    dataset = {"reviews": []}

    for i in range(NUM_PRODUCTS):
        product_id = f"p{i:03d}"
        product_name = generate_product_name()

        for _ in range(random.randint(*REVIEWS_PER_PRODUCT)):
            dataset["reviews"].append(generate_review(product_id, product_name))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print("✅ FINAL CLEAN DATASET GENERATED")


if __name__ == "__main__":
    main()