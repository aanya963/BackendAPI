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
   return {"analysis": result}