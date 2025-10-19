import aiofiles
from fastapi import File
import fitz
import os
from app.logger import logger
import asyncio
from app.utils import get_text_splitter
# from langchain.text_splitter import RecursiveCharacterTextSplitter

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path

    async def write_chuck_into_disk(self, file: File, file_path: str):
        async with aiofiles.open(file_path, "wb") as buff:
            while chunk := await file.read(1024 * 1024):
                await buff.write(chunk)
        logger.info(
            f"Successfully file stored in to disk! file_name:{file.filename}")
        return file_path


    async def process_pdf_file(self, file_path:str, file_name:str, embedding_service):
        doc = fitz.open(file_path)
        tasks = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text").strip()
            if not text:
                continue


            text_splitter = get_text_splitter()
            chunk_list = text_splitter.split_text(text)
            for inx, chunk in enumerate(chunk_list):
                tasks.append(embedding_service.embed_and_store(chunk, inx, file_name, page_num))
                if len(tasks) >= 5:
                    await asyncio.gather(*tasks)
                    tasks = []
            
        if tasks:
            await asyncio.gather(*tasks)
        
        logger.info(f"File chunking and embedding completed successfully! {file_name}")
