import chromadb
from chromadb.utils import embedding_functions

from app.core.config import settings

chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=settings.EMBEDDING_MODEL
)

collection = chroma_client.get_or_create_collection(
    name=settings.COLLECTION_NAME, 
    embedding_function=embedding_func
)