import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools import get_logs, get_slow_requests
from cache import add_history, get_cache, get_history, set_cache

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
    },
    {
        "type": "function",
        "function": {
            "name": "get_slow_requests",
            "description": "Get slow requests with high latency",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

SYSTEM_PROMPT = """
You are a backend debugging expert.

- Use get_logs for specific services
- Use get_slow_requests when user asks about latency or slowness
- Always choose the most relevant tool
- Avoid guessing without data
"""


def run_agent(query: str, session_id: str = "default"):
    steps = []

    cache_key = f"ai:{query.lower().strip()}"

    # 🧠 STEP 0: Check cache
    cached = get_cache(cache_key)
    if cached:
        return {
            "analysis": cached,
            "steps": ["Returned from cache"]
        }

    # 🧠 STEP 1: Get conversation history
    history = get_history(session_id)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    for h in history:
        messages.append({"role": "user", "content": h})

    messages.append({"role": "user", "content": query})

    # 🧠 STEP 2: First LLM call
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # 🧠 STEP 3: Tool calling logic
    if message.tool_calls:

        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name

        steps.append(f"AI decided to call {function_name}")

        import json
        args = json.loads(tool_call.function.arguments or "{}")

        # 🔹 TOOL 1: get_logs
        if function_name == "get_logs":
            logs = get_logs(args["service_name"])
            steps.append(f"Fetched {len(logs)} logs")

        # 🔹 TOOL 2: get_slow_requests
        elif function_name == "get_slow_requests":
            logs = get_slow_requests()
            steps.append(f"Fetched {len(logs)} slow logs")

        else:
            logs = []
            steps.append("Unknown tool called")

        # 🧠 Convert logs to text
        logs_text = "\n".join([
            f"{log['service']}: {log['message']}, latency: {log['latency']}ms"
            for log in logs
        ])

        steps.append("Analyzing logs using LLM")

        # 🧠 STEP 4: Final LLM reasoning
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
                    "tool_call_id": tool_call.id
                }
            ]
        )

        answer = final_response.choices[0].message.content

        # 🧠 Save history + cache
        add_history(session_id, query)
        set_cache(cache_key, answer)

        return {
            "analysis": answer,
            "steps": steps
        }

    # 🧠 STEP 5: No tool used
    steps.append("AI answered directly (no tool used)")

    answer = message.content

    add_history(session_id, query)
    set_cache(cache_key, answer)

    return {
        "analysis": answer,
        "steps": steps
    }