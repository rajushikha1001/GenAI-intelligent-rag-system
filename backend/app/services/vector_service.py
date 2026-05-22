import chromadb
from app.core.config import settings

client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
collection = client.get_or_create_collection("documents")


def store_vectors(chunks, embeddings):
    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )