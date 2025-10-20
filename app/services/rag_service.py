import os
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

    def _initialize_vectorstore(self):
        try:
            self.vector_collection = get_vector_collection()
            logger.info("Query runner initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing query runner: {str(e)}")
            raise e

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
            context_docs = results.get('documents',[[]])[0]

            context = ""
            if context_docs:
                context = "\n\n".join(context_docs)
            

            # llm agent prompt which use to find use appropriate answer
            prompt = f"""
                        You are a specialized expert for the given context.
                        Answer the question using the context below. 
                        If the answer is not in the context, respond with 'Not found'.

                        Context:{context}

                        Question:{query}

                        Answer (concise, max 50 words):
                    """

            answer = self.llm_service.make_llm_call(prompt, os.getenv("LLM_MODEL","llama3.2:1b"))


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
