import chromadb
from chromadb import Client, PersistentClient, HttpClient
import os
from .config import settings
from typing import Optional
from app.logger.logger_setup import logger


class VectorDb():

    _client:Optional[Client] = None

    @classmethod
    def get_client(cls)->Client:
        """
        Class method to use to create and return client instance
        if exist return that same instance if 
        not created the new one and return 

        Raises:
            ValueError: if db mode is not exist in set of this raising value error

        Returns:
            Client: chromadb instance 
        """
        if cls._client is not None:
            logger.info("Returning existing client")
            return cls._client
        
        db_mode = settings.chroma_mode.lower()
        logger.info(f"Initializing chroma db client in mode {db_mode}")

        if db_mode == "persistent":
            os.makedirs(settings.chroma_db_path, exist_ok=True)
            cls._client = PersistentClient(path=settings.chroma_db_path)
        elif db_mode == "http":
            cls._client = HttpClient(host=settings.chroma_host,port=settings.chroma_port)
        elif db_mode == "memory":
            cls._client = Client()
        else :
            raise ValueError(f"Invalid db mode found. {db_mode}")

        logger.info(f"Successfully chroma db client creation done for mode {db_mode}")
        return cls._client
