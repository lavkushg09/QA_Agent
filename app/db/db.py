from .vector_db.vector_chromadb import VectorDb
from app.logger import logger
from .postgres_db.postgres_db import SessionLocal

DB_CLIENTS = {
    "VECTOR_DB": VectorDb,
}


def get_db_instance(type_of_db:str):
    db_type = type_of_db.upper().strip()
    db_client = DB_CLIENTS.get(db_type, None)
    if not db_client:
        logger.error(f"Unsupported database type found. {db_type=}")
        raise ValueError(f"Unsupported database type found: {type_of_db}")
    return db_client().get_client()

def get_vector_collection():
    client_instance = get_db_instance("VECTOR_DB")
    logger.info("Vector db client initialize successfully!")
    return client_instance.get_or_create_collection("knowledge_embedding_v2")


def get_sql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
