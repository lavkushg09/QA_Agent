import os
from fastapi import  APIRouter, UploadFile, File, status
from app.utils import routes_consents
from app.logger import logger
from app.services import EmbeddingService
from app.services import FileProcessor
from app.logger import logger
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)



router = APIRouter()

@router.post('/')
async def upload_knowledge_base(file: UploadFile=File(...)):
    logger.info("File upload initiated")
    if  file.content_type not in routes_consents.ALLOWED_FILE_CONTENT_TYPE:
        logger.warning("Given media type is not supported currently.",{"content_type":file.content_type})
        return {
            "status_code": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "message": "Given media type is not supported."
        }

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    if os.path.exists(file_path):
        logger.info("File path already exist")
    

    embedding_service = EmbeddingService()
    file_processor = FileProcessor(file_path)
    await file_processor.write_chuck_into_disk(file, file_path)
    await file_processor.process_pdf_file(file_path, file.filename, embedding_service)
    

    
    return {
        "status":"success",
        "message":"successfully knowledge base upload!",
        "file_name":file.filename
    }