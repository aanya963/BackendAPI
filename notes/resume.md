Built a distributed log processing system using FastAPI, RabbitMQ, and .NET backend.

Designed an asynchronous pipeline where logs are ingested via API, queued using RabbitMQ, processed by background workers, and persisted to a PostgreSQL database.

Implemented retry mechanisms with dead-letter queues (DLQ) to handle failures and ensure reliability.

Integrated an AI agent using LLM + tool-calling to analyze logs and detect performance bottlenecks.

Optimized system for scalability by decoupling services and handling high-throughput log ingestion.