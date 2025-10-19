from app.db import get_vector_collection
import os
import uuid
import asyncio
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from app.logger import logger
load_dotenv()


class EmbeddingService():
    def __init__(self):
        self.model = self.get_model()
        self.vector_collection = get_vector_collection()
        logger.info("Successfully embedding service initialized.")

    def get_model(self):
        model_name = os.getenv('EMBEDDING_MODEL', 'multi-qa-MiniLM-L6-cos-v1')
        logger.info(f"Initializing embedding model with model_name {model_name}")
        return SentenceTransformer(model_name)
    
    def _get_or_create_event():
        try:
            loop = asyncio.get_running_loop()
            logger.info("Find already running event loop")
            return loop
        except RuntimeError as err:
            logger.warning(err.message)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        
    async def encode_string(self, text: str):
        try:
            encoding = self.model.encode(text)
            logger.info("Text embedding completed successfully!")
            return {
                "success": True,
                "encoding_data": encoding
            }
        except Exception as err:
            logger.error(f"Getting error while embedding text", err)
            return {
                "success": False,
                "encoding_data": None
            }

    async def embed_and_store(self, chunk_text: str, chunk_inx: int, file_name: str, page_num: int):
        logger.info("Text encoding and saving into db initiated")
        loop = self._get_or_create_event()
        embedding = await loop.run_in_executor(None, self.model.encode, chunk_text)
        self.vector_collection.add(
            embeddings=[embedding.tolist()],
            documents=[chunk_text],
            metadatas=[{"page": page_num, "file_name": file_name}],
            ids=[f"{str(uuid.uuid4())}_page_number{page_num}_inx{chunk_inx}"]
        )
        logger.info("Successfully text embedded and stored in collection!")


