🔵 1. Python (FastAPI) → AI + Queue

    👉 http://localhost:8000/docs

    This handles:

    /analyze → AI agent
    /ingest-log → pushes to queue

🟢 2. .NET Backend → Database

    👉 http://localhost:5124/swagger/index.html

    This handles:

    /api/logs → store logs in DB
    /api/logs/slow → fetch slow logs

Step	        ->      Who does it

Receive log	    ->      FastAPI
Queue push	    ->      Redis
Queue pop	    ->      Worker
Send to backend	->      Worker
Save	        ->      .NET
Fetch	        ->      DB


DOING THIS QUEUE THING SO THAT DB DON'T GET OVERWHELEMED

# FastAPI (8000)
    👉 [API] Received log
    👉 [QUEUE] Adding to Redis
# Worker (runs continuously)
    🔄 Checking queue...
    👉 [QUEUE] Popped from Redis
    🚀 Processing log
# Worker calls .NET
    📡 Sent to .NET
# .NET (5124)
    👉 Received log
    👉 Saved to DB

***
    👉 Worker is always running in loop
    👉 It “wakes up” every 2 sec and checks queue
    So it’s not: API → Worker instantly
    It’s: API → Queue → (Worker picks later)


======================== REDIS To RABBITMQ ===============================

# What Redis does well
    Very fast ⚡ (in-memory)
    Very simple
    Push → Pop
# Where Redis falls short
    1. No guarantee of processing
        If worker crashes after popping : Log is gone ❌
    2. No acknowledgment system
        Redis does NOT know : Did worker actually finish the job?
    3. No real “queue system features”
        No retries
        No dead-letter queue
        No routing
        No priorities

# What is RabbitMQ?
    Instead of a bucket, you now have:
        📮 Producers (you)
        📦 Queues
        🧠 Broker (RabbitMQ)
        🧑‍✈️ Consumers (worker)
    Smart routing (advanced)
        RabbitMQ can decide : Which worker should get which log
    Producer → Exchange → Queue → Consumer → ACK