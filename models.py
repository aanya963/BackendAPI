from pydantic import BaseModel
from typing import List

class AnalyzeRequest(BaseModel):
    query: str
    logs: List[str] = []