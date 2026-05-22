from app.utils.chunking import chunk_text
from app.services.embedding_service import create_embeddings
from app.services.vector_service import store_vectors
from langchain_community.document_loaders import PyPDFLoader


def process_document(filename: str, content: bytes):
    temp_path = f"/tmp/{filename}"

    with open(temp_path, "wb") as f:
        f.write(content)

    loader = PyPDFLoader(temp_path)
    pages = loader.load()

    full_text = "\n".join([page.page_content for page in pages])

    chunks = chunk_text(full_text)

    embeddings = create_embeddings(chunks)

    store_vectors(chunks, embeddings)

    return {
        "chunks": len(chunks)
    }