                ┌────────────────────┐
                │   Auth Service     │
                │  Payment Service   │
                │   Order Service    │
                └─────────┬──────────┘
                          │
                          │ (logs generated automatically)
                          ▼
                ┌────────────────────┐
                │    RabbitMQ        │
                │   (logs_queue)     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Worker Service   │
                │ (Python Consumer)  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   .NET Backend     │
                │  (LogsController)  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   PostgreSQL DB    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   AI Agent Layer   │
                │ (LLM + Tool Calls) │
                └────────────────────┘

“Multiple backend services generate logs during execution.
Instead of writing directly to the database, logs are pushed to RabbitMQ.
A worker consumes these logs asynchronously and sends them to the .NET backend, which stores them in PostgreSQL.
On top of this, I built an AI agent that analyzes logs and helps identify performance issues.”


1. Producers (services)
    Auth, Payment, Order
    Generate logs automatically

    👉 No manual API in real system
2. Queue (RabbitMQ)
    Acts as buffer
    Handles spikes in traffic
    Decouples services
3. Worker
    Reads logs from queue
    Sends to backend
    Handles:
        retries
        failures (DLQ)
4. Backend (.NET)
    Saves logs
    Provides APIs:
    /logs
    /logs/slow
    /logs/service/{name}
5. AI Layer (your highlight 🔥)
    Takes query like:
    “Why is auth slow?”
    Calls tools:
        get logs
        get slow requests
        Uses LLM to analyze
“I separated ingestion, processing, storage, and analysis into different layers to make the system scalable and fault-tolerant.”
“I also implemented retry logic and a dead-letter queue to handle failures in log processing.”

Queue → handles load
Worker → async processing
DB → persistent storage
AI → intelligent debugging