import json

# ---------- PATHS ----------
INPUT_FILE = "c:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/review_chunks_clean.json"
OUTPUT_FILE = "c:/Users/ayush/OneDrive/Desktop/Amazon_OTDS/data/review_chunks_clean.json"

# ---------- TYPO FIX ----------
def fix_typos(text):
    replacements = {
        "dongles not": "does not",
        "dongles its": "does its",
        "dongles": "does"
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


# ---------- MAIN ----------
def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen = set()
    cleaned_chunks = []

    for chunk in data["chunks"]:
        text = chunk["text"].strip()

        # Fix typos
        text = fix_typos(text)

        # Deduplicate
        if text in seen:
            continue
        seen.add(text)

        # Update text
        chunk["text"] = text

        cleaned_chunks.append(chunk)

    # Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"chunks": cleaned_chunks}, f, indent=2)

    print("✅ Cleaning complete")
    print(f"Original chunks: {len(data['chunks'])}")
    print(f"After deduplication: {len(cleaned_chunks)}")


if __name__ == "__main__":
    main()