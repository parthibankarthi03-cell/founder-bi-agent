from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    trace: List[Dict[str, Any]]