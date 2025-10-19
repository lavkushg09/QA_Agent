from typing import Union

from fastapi import FastAPI
from app.routes import document_upload

app = FastAPI(title="Q%A Chat boat!")

app.include_router(document_upload.router, prefix="/upload", tags=["Upload"])


@app.get('/')
async def root_route():
    return {"Message":"Welcome to the Q&A Chat boat!"}