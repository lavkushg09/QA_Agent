from pydantic import BaseModel

class AskQueryRequest(BaseModel):
    query:str
    top_k:int = 5