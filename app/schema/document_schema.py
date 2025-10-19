from pydantic import BaseModel
from datetime import datetime

class DocumentMetadataCreate(BaseModel):
    document_name: str
    source: str | None = None
    author: str | None = None
    chunk_ids: str | None = []
    description: str | None = None

class DocumentMetadataResponse(DocumentMetadataCreate):
    id: int
    upload_date: datetime

    class Config:
        orm_mode = True
