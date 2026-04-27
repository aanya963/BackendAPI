from agent import run_agent
from fastapi import FastAPI # type: ignore
import os 
from groq import Groq
from dotenv import load_dotenv
from models import AnalyzeRequest
from rabbitmq_producer import publish_log

load_dotenv()
app = FastAPI()
from rabbitmq_producer import publish_log, init_rabbitmq

@app.on_event("startup")
def startup_event():
    print("🚀 Starting app...")
    init_rabbitmq()

    
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.post("/analyze")
def analyze_data(req : AnalyzeRequest):
    result = run_agent(req.query)
    return {
        "ai_response": result
    }



from fastapi import BackgroundTasks

@app.post("/ingest-log")
def ingest_log(log: dict, background_tasks: BackgroundTasks):
    print("\n👉 [API] Received log:", log)

    background_tasks.add_task(publish_log, log)

    return {"status": "log added to queue"}

