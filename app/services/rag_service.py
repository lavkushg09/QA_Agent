import os
import requests
import json
from dotenv import load_dotenv
from app.logger import logger
from app.db.vector_db.vector_chromadb import get_vector_collection
from .llm.ollam_llm import OllamaLLm

load_dotenv()


class QueryRunner:
    def __init__(self):
        self.vector_collection = None
        self.llm_service = OllamaLLm()
        self._initialize_vectorstore()
        self.ollama_url = "http://localhost:11434/api/generate"

    def _initialize_vectorstore(self):
        try:
            self.vector_collection = get_vector_collection()
            logger.info("Query runner initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing query runner: {str(e)}")
            raise e

    def _query_ollama(self, prompt: str):
        """Query Ollama LLM"""
        try:
            payload = {
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "No response from LLM")

        except Exception as e:
            logger.error(f"Error querying Ollama: {str(e)}")
            return f"Error: {str(e)}"

    def run(self, query: str, k: int = 3):
        """
        Run a query against the RAG system
        """
        try:
            if not self.vector_collection:
                self._initialize_vectorstore()

            # Get query embedding using the embedding service
            from app.services.embedding_service import EmbeddingService
            embedding_service = EmbeddingService()
            query_embedding_result = embedding_service.encode_string(query)

            if not query_embedding_result.get('success', False):
                return {"error": "Failed to encode query"}

            query_embedding = query_embedding_result['encoding_data']

            # Search for similar documents
            results = self.vector_collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=k,
                include=['distances', 'documents', 'metadatas']
            )

            if not results['documents'][0]:
                return {"answer": "No relevant documents found.", "context": []}

            # Prepare context from retrieved documents
            context_docs = results['documents'][0]
            context = "\n\n".join(context_docs)

            # Create prompt for LLM
            prompt = f"""
                    Answer the question using the context below. If the answer is not in the context, say 'Not found'.
                    Context:{context}
                    Question: {query}
                    Answer (max 50 words):
                    """

            # Get answer from LLM
            # answer = self._query_ollama(prompt)
            answer = self.llm_service.make_llm_call(prompt, os.getenv("LLM_MODEL","llama3.2:1b"))


            print(answer)
            print("=======================", prompt)
            # print(answer1)

            # Prepare context metadata
            context_list = []
            for i, doc in enumerate(context_docs):
                context_list.append({
                    "metadata": results['metadatas'][0][i] if i < len(results['metadatas'][0]) else {},
                    "content_preview": doc[:200]
                })

            return {
                "answer": answer,
                "context": context_list
            }

        except Exception as e:
            logger.error(f"Error running query: {str(e)}")
            return {"error": str(e)}


def run_query():
    """Factory function to create a QueryRunner instance"""
    return QueryRunner()
