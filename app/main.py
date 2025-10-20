from fastapi import FastAPI
from app.routes import document_upload
from app.routes import query
from app.db.postgres_db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Q&A Chat boat!"
)

app.include_router(document_upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/ask", tags=["ask"])


@app.get('/')
async def root_route():
    return {"Message":"Welcome to the Q&A Chat boat!"}