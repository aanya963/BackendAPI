import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools import get_logs

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_logs",
            "description": "Get logs for a specific service",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {"type": "string"}
                },
                "required": ["service_name"]
            }
        }
    }
]

SYSTEM_PROMPT = """
You are a backend system debugging expert.

- Be specific
- Mention exact causes
- Use logs carefully
- Avoid generic answers
- If logs are insufficient, say so clearly
"""

def run_agent(query: str):
    # Step 1
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Step 2: tool call
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)

        logs = get_logs(args["service_name"])

        logs_text = "\n".join([
            f"{log['service']}: {log['message']}, latency: {log['latency']}ms"
            for log in logs
        ])

        # Step 3: final reasoning
        final_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": message.tool_calls
                },
                {
                    "role": "tool",
                    "content": logs_text,
                    "tool_call_id": message.tool_calls[0].id
                }
            ]
        )

        return final_response.choices[0].message.content

    return message.content