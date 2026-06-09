import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks


MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "isu_dining_guide"
TOP_K = 5

_model = None


def get_model():
    """
    Load the embedding model once and reuse it.
    """
    global _model

    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def get_chroma_client():
    """
    Create a local persistent ChromaDB client.
    ChromaDB will save files inside the chroma_db folder.
    """
    return chromadb.PersistentClient(path=CHROMA_PATH)


def reset_collection(client):
    """
    Delete and recreate the ChromaDB collection.

    This is useful while developing because if we change chunks,
    we want the vector store to rebuild from scratch.
    """
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    return client.create_collection(name=COLLECTION_NAME)


def build_vector_store():
    """
    Build the vector database from chunks.
    """
    chunks = build_chunks()

    if not chunks:
        raise ValueError("No chunks found. Run python ingest.py first.")

    client = get_chroma_client()
    collection = reset_collection(client)

    documents = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    model = get_model()

    print(f"Embedding {len(documents)} chunks...")
    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Stored {collection.count()} chunks in ChromaDB.")
    return collection


def load_collection():
    """
    Load the existing ChromaDB collection.
    """
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def retrieve(query, top_k=TOP_K):
    """
    Retrieve the top-k most relevant chunks for a user query.
    """
    collection = load_collection()

    if collection.count() == 0:
        print("Vector store is empty. Building it now...")
        collection = build_vector_store()

    model = get_model()
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(documents, metadatas, distances):
        retrieved_chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_chunks


def print_retrieval_results(query, results):
    """
    Print retrieval results in a readable format.
    """
    print()
    print("=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    for i, result in enumerate(results, start=1):
        source = result["metadata"]["source"]
        chunk_index = result["metadata"]["chunk_index"]
        distance = result["distance"]
        text = result["text"]

        print(f"\nResult {i}")
        print(f"Source: {source}")
        print(f"Chunk index: {chunk_index}")
        print(f"Distance: {distance:.4f}")
        print("-" * 100)
        print(text[:1000])
        print("-" * 100)


if __name__ == "__main__":
    build_vector_store()

    test_queries = [
        "What do students say is the best food on campus?",
        "Are ISU meal plans worth it?",
        "What restaurants near campus do students recommend?",
    ]

    for query in test_queries:
        results = retrieve(query, top_k=TOP_K)
        print_retrieval_results(query, results)