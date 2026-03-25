from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title="RAG Service Prototype", 
    version="1.0.0",
    description="Configurable RAG service using FastAPI and ChromaDB"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=True
    )