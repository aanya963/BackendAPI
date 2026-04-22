from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
import os 
from groq import Groq
from dotenv import load_dotenv
import requests  # requests is a Python library used to make HTTP calls

load_dotenv()
app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# data model using pydantic. : Validates input automatically, Prevents wrong data, Very common in backend systems

# 3️⃣ Request model
class analyzeRequest(BaseModel):
    query: str
    logs: list[str]

# 4️⃣ 🔥 TOOL FUNCTION (ADD HERE)
def get_logs(service_name: str):
    response = requests.get(
        f"http://localhost:5124/api/logs/service/{service_name}"
    )
    return response.json()


# 5️⃣ TOOL DEFINITION (for AI)
tools = [
    {
        "type": "function",
        "function":{
            "name":"get_logs",
            "description": "Get logs for a specific service",
            "parameters":{
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service like auth, payment"
                    }
                },
                "required": ["service_name"]
            }
        }
    }
]

@app.post("/analyze")
def analyze_data(req : analyzeRequest):
    try:
        # STEP 1 : Ask AI what to do
        response = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a debugging assistant. Always use the get_logs tool when user asks about system issues."},
                {"role": "user", "content": req.query}
            ],
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # STEP 2: Did AI ask for a tool?
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name

            # Convert arguments string → dict
            import json
            arguments = json.loads(tool_call.function.arguments)

            # STEP 3: Execute tool
            if function_name == "get_logs":
                logs = get_logs(arguments["service_name"])

                # Convert logs → readable text
                logs_text = "\n".join([
                    f"{log['service']}: {log['message']}, latency: {log['latency']}ms"
                    for log in logs
                ])

                # STEP 4: Send logs back to AI

                final_response = client.chat.completions.create(
                    model = "llama-3.1-8b-instant",
                    messages = [
                        {"role": "system", "content": "You are a debugging assistant. Always use the get_logs tool when user asks about system issues."},
                        {"role": "user", "content": req.query},

                        # AI previously called tool

                        {
                            "role": "assistant",
                            "content": None,
                            "tool_calls": message.tool_calls
                        },

                        # Tool result

                        {
                            "role": "tool",
                            "content": logs_text,
                            "tool_call_id": message.tool_calls[0].id
                        }
                    ]
                )

                answer = final_response.choices[0].message.content

                return {
                    "analysis": answer
                }
        # fallback no tool used
        return {"analysis": message.content}
    
    except Exception as e:
        return {"error": str(e)}
