import os
from fastapi import APIRouter, status
from app.utils import routes_consents
from app.logger import logger
from app.services import EmbeddingService
from app.services import FileProcessor
from app.schema import AskQueryRequest
from app.logger import logger
from fastapi.responses import JSONResponse
from app.services import run_query
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router = APIRouter()


@router.post("/")
async def ask_question(request: AskQueryRequest):
    try:
        query_runner = run_query()
        res = query_runner.run(request.query, k=request.top_k)
        if 'error' in res:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "status": "failed",
                    "message": f"Error processing query: {res['error']}"
                }
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "Successfully retrieved context about query",
                "answer": res.get('answer', 'No answer generated'),
            }
        )
    except Exception as e:
        logger.error(f"Error in ask_question: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "failed",
                "message": f"Internal server error: {str(e)}"
            }
        )
