from .vector_db.vector_chromadb import VectorDb
from .vector_db import get_vector_collection
from app.logger import logger
from .postgres_db.postgres_db import SessionLocal

DB_CLIENTS = {
    "VECTOR_DB": VectorDb,
}


# def get_db_instance(type_of_db:str):
#     db_type = type_of_db.upper().strip()
#     db_client = DB_CLIENTS.get(db_type, None)
#     if not db_client:
#         logger.error(f"Unsupported database type found. {db_type=}")
#         raise ValueError(f"Unsupported database type found: {type_of_db}")
#     return db_client().get_client()

# def get_vector_collection():
#     vector_db = VectorDb()
#     client_instance = vector_db.get_client()
#     return vector_db.get_co("knowledge_embedding_v2")
#     \


def get_sql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
