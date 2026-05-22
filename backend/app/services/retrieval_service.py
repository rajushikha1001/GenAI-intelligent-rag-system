from app.services.vector_service import collection
from app.services.embedding_service import embedding_model


def retrieve_context(query: str):
    query_embedding = embedding_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]