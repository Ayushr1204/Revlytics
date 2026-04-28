import json
import random

INPUT_FILE = "C:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/reviews.json"
OUTPUT_FILE = "C:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/reviews_humanized.json"

HUMANIZE_RATIO = 0.3

casual_phrases = [
    "tbh", "honestly", "kinda", "pretty much", "idk",
    "ngl", "sort of", "a bit", "overall", "for me"
]

def humanize_text(text):
    sentences = text.split(". ")

    new_sentences = []

    for s in sentences:
        if not s.strip():
            continue

        # randomly shorten or keep
        if random.random() < 0.3:
            s = s.split(",")[0]

        # add casual phrase
        if random.random() < 0.4:
            s = random.choice(casual_phrases) + " " + s.lower()

        # slight grammar mess
        if random.random() < 0.3:
            s = s.replace(" is ", " ").replace(" are ", " ")

        new_sentences.append(s.strip())

    # sometimes reduce to 1-2 sentences
    if len(new_sentences) > 2 and random.random() < 0.5:
        new_sentences = random.sample(new_sentences, 2)

    return ". ".join(new_sentences)


def main():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    reviews = data["reviews"]

    num_to_modify = int(len(reviews) * HUMANIZE_RATIO)
    indices = set(random.sample(range(len(reviews)), num_to_modify))

    for i in indices:
        original = reviews[i]["text"]
        reviews[i]["text"] = humanize_text(original)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Humanized {num_to_modify} reviews out of {len(reviews)}")


if __name__ == "__main__":
    main()