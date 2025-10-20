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
        logger.info(
            f"Initializing embedding model with model_name {model_name}")
        return SentenceTransformer(model_name)

    def _get_or_create_event(self):
        """Checking existing event loop if not exist creating and returning loop for execution

        Returns:
            asyncio.loop: loop instance
        """
        try:
            loop = asyncio.get_running_loop()
            return loop
        except RuntimeError as err:
            logger.warning(err.message)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

    def encode_string(self, text: str):
        """Embedding given text in vector

        Args:
            text (str): text which we want to embedding 

        Returns:
            dict: have success status along with embedding vector
        """
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
        """
            Encode a text chunk and store it in the vector collection.
            Args:
                chunk_text (str): Text content of the chunk.
                chunk_inx (int): Index of the chunk.
                file_name (str): Name of the source file.
                page_num (int): Page number of the chunk.
         """
        logger.info(
            f"Text encoding and saving into db initiated. {chunk_inx=} {file_name=} {page_num=}")
        loop = self._get_or_create_event()
        embedding = await loop.run_in_executor(None, self.model.encode, chunk_text)
        self.vector_collection.add(
            embeddings=[embedding.tolist()],
            documents=[chunk_text],
            metadatas=[{"page": page_num, "file_name": file_name}],
            ids=[f"{str(uuid.uuid4())}_page_number{page_num}_inx{chunk_inx}"]
        )
        logger.info(
            f"Successfully text embedded and stored in collection! {chunk_inx=} {file_name=} {page_num=}")

    async def retrieve_top_k_embedding(self, query_embedding, tok_k=3):
        """
        Retrieve the top-k most similar documents for a given embedding.
        Args:
            query_embedding: The embedding vector to query against the vector collection.
            top_k: Number of top results to return (default is 3).
        Returns:
            A single string combining the top-k retrieved documents separated by newlines.
        """
        results = self.vector_collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=tok_k,
            include=['distances', 'documents', 'metadatas']
        )
        retrieved_docs = results.get('documents', [[]])[0]
        if not retrieved_docs:
            return ""
        return "\n".join(retrieved_docs)
