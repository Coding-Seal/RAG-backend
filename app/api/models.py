from pydantic import BaseModel
from typing import Optional, List

from app.core.chunker import Metadata

class DocumentIngest(BaseModel):
    doc_id: str
    text: str
    metadata: Optional[Metadata] = {}

class RetrievedChunk(BaseModel):
    doc_id: str
    text: str
    distance: float
    metadata: Metadata

class RetrieveResponse(BaseModel):
    results: List[RetrievedChunk]

