from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI()

# data model using pydantic. : Validates input automatically, Prevents wrong data, Very common in backend systems
class analyzeRequest(BaseModel):
    query: str
    logs: list[str]

@app.get("/")
def read_root():
    return {"message": "Python service is running"}


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

    if "1200" in logs_text or "slow" in logs_text.lower():
        analysis = "The system appears slow due to high latency in requests."
    elif "timeout" in logs_text.lower():
        analysis = "Timeout errors suggest backend or database delays."
    else : 
        analysis = "No obvious issue detected from logs."
    
    return {
        "analysis": analysis,
        "logs_analyzed": len(req.logs)
    }

