import os
from fastapi import APIRouter, status
from app.utils import routes_consents
from app.logger import logger
from app.services import EmbeddingService
from app.services import FileProcessor
from app.schema import AskQueryRequest
from app.logger import logger
from fastapi.responses import JSONResponse
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router = APIRouter()


@router.post("/")
async def ask_question(request: AskQueryRequest):
    embedding_service = EmbeddingService()
    query_embedding = await embedding_service.encode_string(request.query)
    print(query_embedding)
    if not query_embedding.get('success', False):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={
                "status": "failed",
                "message": "Embedding service is down! contact to dev for resolve."
            })
    query_context = await embedding_service.retrieve_top_k_embedding(query_embedding.get('encoding_data'))
    logger.info(query_context)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Successfully retrieve context about query",
            "context": query_context
        }
    )
