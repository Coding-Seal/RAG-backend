from fastapi import APIRouter, Query, HTTPException, status

from app.core.config import settings
from app.db.chroma import collection
from app.api.models import *

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "db_path": settings.CHROMA_PERSIST_DIR,
        "collection": settings.COLLECTION_NAME,
        "embedding_model": settings.EMBEDDING_MODEL
    }

@router.get("/retrieve", response_model=RetrieveResponse)
async def retrieve_context(
    query: str = Query(..., min_length=1, description="The search query string"),
    n_results: int = Query(default=3, ge=1, le=100, description="Number of results to return")):

    if not query.strip():
        raise HTTPException(
            status_code=400, 
            detail="Query cannot be empty or whitespace only"
        )
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        formatted_results = []
        
        if not results['ids'] or not results['ids'][0]:
            return RetrieveResponse(results=[])

        ids = results['ids'][0]
        documents = results['documents'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]

        for i in range(len(ids)):
            formatted_results.append(RetrievedChunk(
                doc_id=ids[i],
                text=documents[i],
                distance=distances[i],
                metadata=metadatas[i]
            ))

        return RetrieveResponse(query=query_req.query, results=formatted_results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_document(doc: DocumentIngest):
    try:
        collection.add(
            ids=[doc.doc_id],
            documents=[doc.text],
            metadatas=[doc.metadata]
        )
        return {"message": f"Document {doc.doc_id} ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

