from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# data model using pydantic. : Validates input automatically, Prevents wrong data, Very common in backend systems

class analyzeRequest(BaseModel):
    query: str
    logs: list[str]


@app.post("/analyze")
def analyze_data(req : analyzeRequest):
    logs_text = "\n".join(req.logs)

    # create a prompt 
    prompt = f""" 
        You are a backend system debugging assistant.

        User Question: {req.query}

        Logs : {logs_text}

        Instructions :
            - Identify possible reasons for the issue
            - Focus on latency, errors, or patterns
            - Give a short explanation
    """

    # For now, simulate reasoning (we'll plug real LLM next)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a debugging assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    answer = response.choices[0].message.content

    return {
        "analysis": answer,
        "logs_analyzed": len(req.logs)
    }

