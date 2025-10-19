# from crewai import Agent, Task, Crew
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.llms import OpenAI  # or another model

# # 1️⃣ Initialize embeddings
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# # 2️⃣ Load your existing Chroma vector store
# vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# # 3️⃣ Define a retriever task for QA
# qa_agent = Agent(
#     role="Knowledge Assistant",
#     goal="Retrieve and answer questions based on stored document embeddings",
#     backstory="This agent provides factual answers grounded in uploaded documents."
# )

# qa_task = Task(
#     description="Answer user query using RAG pipeline",
#     expected_output="Concise factual answer based on document context"
# )

# # 4️⃣ Create the Crew with one agent
# crew = Crew(agents=[qa_agent], tasks=[qa_task])

# def answer_query(query: str):
#     # Retrieve top documents from Chroma
#     docs = vectorstore.similarity_search(query, k=3)
#     context = "\n".join([d.page_content for d in docs])

#     # Combine context + query for the agent
#     result = crew.run(inputs={"query": query, "context": context})
#     return result



from crewai import Agent, Task, Crew
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
load_dotenv()

vector_db_path = os.getenv('CHROMA_DB_PATH',"data/chroma")
embedding_model = os.getenv('EMBEDDING_MODEL',"BAAI/bge-base-en-v1.5")


if not os.path.exists(vector_db_path):
    raise RuntimeError(f"Chroma DB path not found: {vector_db_path}")

embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

vectorstore = Chroma(
    persist_directory=vector_db_path,
    embedding_function=embeddings
)

# ------------------------------------------------------------
# 3️⃣ Define the CrewAI Agent and Task
# ------------------------------------------------------------
llm = Ollama(model="deepdeepseek-r1:8b")  # or use OpenAI(model="gpt-4") if preferred

qa_agent = Agent(
    role="Knowledge Assistant",
    goal="Retrieve relevant information from stored documents and provide a factual, concise answer.",
    backstory="You are an expert document analyst who uses retrieved context to answer user questions accurately.",
    llm=llm,
)

qa_task = Task(
    description="Answer the user's query using the given document context.",
    expected_output="A factual and concise answer that only uses provided context.",
    agent=qa_agent
)

crew = Crew(agents=[qa_agent], tasks=[qa_task])
def answer_query(query: str, k: int = 3):
    """
    Perform RAG QA:
    - Retrieve top-k relevant chunks
    - Generate an answer using CrewAI agent
    """
    try:
       
        docs = vectorstore.similarity_search(query, k=k)
        print(vectorstore,"=========", docs)
        if not docs:
            return {"answer": "No relevant documents found.", "context": []}

        context = "\n\n".join([d.page_content for d in docs])
        print(context)
        result = crew.run(inputs={"query": query, "context": context})

        return {
            "answer": str(result),
            "context": [
                {"metadata": d.metadata, "content_preview": d.page_content[:200]}
                for d in docs
            ]
        }

    except Exception as e:
        return {"error": str(e)}

