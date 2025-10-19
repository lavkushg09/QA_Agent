from sqlalchemy import Column, Integer, String, DateTime, Text, ARRAY
from datetime import datetime
from app.db.postgres_db import Base

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, nullable=False)
    source = Column(String, nullable=True)
    author = Column(String, nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    chunk_ids = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)

