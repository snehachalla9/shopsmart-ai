
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "store_policies.txt"
DB_DIR = BASE_DIR.parent / "chroma_db"

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Create persistent ChromaDB client
client = chromadb.PersistentClient(path=str(DB_DIR))

# Create or access collection
collection = client.get_or_create_collection(
    name="shopsmart_policies"
)


def split_text(text, chunk_size=500, overlap=50):
    """Split a document into overlapping chunks."""

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def index_documents():
    """Read, split, embed and store policy documents."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Policy file not found: {DATA_FILE}")

    text = DATA_FILE.read_text(encoding="utf-8")

    chunks = split_text(text)

    # Rebuild this collection to avoid duplicate chunks
    if collection.count() > 0:
        existing_ids = collection.get()["ids"]
        collection.delete(ids=existing_ids)

    embeddings = embedding_model.encode(chunks).tolist()

    ids = [f"policy_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return len(chunks)


def retrieve_documents(question, top_k=3):
    """Find the most relevant policy chunks."""

    question_embedding = embedding_model.encode(
        [question]
    ).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=min(top_k, collection.count())
    )

    return results["documents"][0] if results["documents"] else []
