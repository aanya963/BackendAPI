from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI()

class analyzeRequest(BaseModel):
    query: str
    logs: list[str]

@app.get("/")
def read_root():
    return {"message": "Python service is running"}


@app.get("/analyze")
def analyze_data(req : analyzeRequest):
    return{
        "received_query": req.query,
        "log_count": len(req.logs),
        "summary": f"You sent {len(req.logs)} logs for analysis"
    }
