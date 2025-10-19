import os
from fastapi import APIRouter, UploadFile, File, status, Form, HTTPException, Depends
from app.utils import routes_consents
from app.logger import logger
from app.services import EmbeddingService
from app.services import FileProcessor
from app.logger import logger
from fastapi.responses import JSONResponse
from typing import Optional
from app.crud import create_document, get_documents
from app.schema import DocumentMetadataCreate
from app.db import get_sql_db
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router = APIRouter()


@router.post('/')
async def upload_knowledge_base(file: UploadFile = File(...),
                                document_name: str = Form(...),
                                author: Optional[str] = Form(None),
                                source: Optional[str] = Form(None), db=Depends(get_sql_db)):
    if file.content_type not in routes_consents.ALLOWED_FILE_CONTENT_TYPE:
        logger.warning(
            "Given media type is not supported currently.",
            {"content_type": file.content_type}
        )
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                "status": "Failed",
                "message": "Given media type is not supported."
            }
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    if os.path.exists(file_path):
        logger.info("File path already exists")
        # return JSONResponse(
        #     status_code=status.HTTP_406_NOT_ACCEPTABLE,
        #     content={
        #         "status": "Failed",
        #         "message": "Duplicate file name not allowed for now. Please change the name and try again."
        #     }
        # )

    try:
        embedding_service = EmbeddingService()
        file_processor = FileProcessor(file_path)
        doc_data = DocumentMetadataCreate(
            document_name=document_name,
            author=author,
            source=source,
            file_path=file_path
        )

        db_ins = create_document(
            db=db,
            doc=doc_data
        )
        logger.info(f"Document metadata successfully created in DB.")
        print(db_ins)

        await file_processor.write_chuck_into_disk(file, file_path)
        await file_processor.process_pdf_file(file_path, file.filename, embedding_service)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status": "success",
                "message": "Successfully uploaded knowledge base!",
                "file_name": file.filename
            }
        )
    except Exception as err:
        logger.error("Knowledge base update failed", exc_info=err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "Failed",
                "message": "Knowledge base update failed",
                "file_name": file.filename
            }
        )
