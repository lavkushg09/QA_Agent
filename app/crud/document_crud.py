from sqlalchemy.orm import Session
from app.models import DocumentMetadata
from app.schema import DocumentMetadataCreate

def create_document(db: Session, doc: DocumentMetadataCreate):
    db_doc = DocumentMetadata(**doc.model_dump())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_documents(db: Session):
    return db.query(DocumentMetadata).all()
