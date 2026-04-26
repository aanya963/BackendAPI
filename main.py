from agent import run_agent
from fastapi import FastAPI # type: ignore
import os 
from groq import Groq
from dotenv import load_dotenv
from models import AnalyzeRequest

load_dotenv()
app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.post("/analyze")
def analyze_data(req : AnalyzeRequest):
    result = run_agent(req.query)
    return {
        "ai_response": result
    }


# from queue_manager import log_queue
from queue_manager import push_log

import queue_manager
print(queue_manager.__file__)

@app.post("/ingest-log")
def ingest_log(log: dict):
    print("\n👉 [API] Received log:", log)
    push_log(log)
    print("👉 [API] Pushed to Redis queue")
    return {"status": "log added to queue"}
