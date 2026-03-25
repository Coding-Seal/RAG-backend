from pydantic import BaseModel
from typing import Optional, List

class DocumentIngest(BaseModel):
    doc_id: str
    text: str
    metadata: Optional[dict] = {}

class RetrievedChunk(BaseModel):
    doc_id: str
    text: str
    distance: float
    metadata: dict

class RetrieveResponse(BaseModel):
    results: List[RetrievedChunk]

