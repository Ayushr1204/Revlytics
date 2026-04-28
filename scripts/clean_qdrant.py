from qdrant_client import QdrantClient
import os
import shutil

# ---------- CONFIG ----------
COLLECTION_NAME = "review_chunks"
QDRANT_PATH = "qdrant_data"   # same path you used in your project


# ---------- METHOD 1: SAFE DELETE (recommended) ----------
def delete_collection():
    client = QdrantClient(path=QDRANT_PATH)

    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME in names:
        print(f"⚠️ Deleting collection: {COLLECTION_NAME}")
        client.delete_collection(collection_name=COLLECTION_NAME)
        print("✅ Collection deleted")
    else:
        print("ℹ️ Collection not found")


# ---------- METHOD 2: FULL WIPE (hard reset) ----------
def wipe_storage():
    if os.path.exists(QDRANT_PATH):
        print("🔥 Deleting entire Qdrant storage folder...")
        shutil.rmtree(QDRANT_PATH)
        print("✅ Storage wiped completely")
    else:
        print("ℹ️ No storage folder found")


# ---------- MAIN ----------
if __name__ == "__main__":
    print("\nChoose reset type:")
    print("1 → Delete only collection")
    print("2 → FULL WIPE (recommended for clean restart)")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        delete_collection()
    elif choice == "2":
        wipe_storage()
    else:
        print("❌ Invalid choice")