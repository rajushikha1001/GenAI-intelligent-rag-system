from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

embedding_model = OpenAIEmbeddings(
    api_key=settings.OPENAI_API_KEY,
    model="text-embedding-3-small"
)


def create_embeddings(chunks):
    return embedding_model.embed_documents(chunks)