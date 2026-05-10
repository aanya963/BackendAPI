````md
# Distributed AI Log Analysis Platform

An event-driven distributed log processing and AI-powered debugging platform built using FastAPI, .NET workers, RabbitMQ, PostgreSQL, Redis, and LLM tool-calling.

The system enables scalable log ingestion, asynchronous processing, intelligent log querying, and contextual debugging insights through an AI agent.

---

# 🚀 Features

- Distributed log ingestion pipeline
- Event-driven architecture using RabbitMQ
- Asynchronous log processing with worker services
- PostgreSQL log persistence
- Redis-based caching and conversational memory
- AI-powered debugging assistant using LLM tool-calling
- REST APIs for querying logs
- Retry and fault handling
- Dockerized multi-service architecture
- Scalable backend design

---

# 🏗️ System Architecture

```text
                +-------------------+
                |   Client / UI     |
                +---------+---------+
                          |
                          v
                +-------------------+
                |   FastAPI API     |
                | Log Ingestion API |
                +---------+---------+
                          |
                          v
                +-------------------+
                |    RabbitMQ       |
                | Message Queue     |
                +---------+---------+
                          |
                          v
                +-------------------+
                |  .NET Worker      |
                | Log Processor     |
                +---------+---------+
                          |
             +------------+-------------+
             |                          |
             v                          v
    +----------------+        +----------------+
    | PostgreSQL     |        | Redis          |
    | Log Storage    |        | Cache/Memory   |
    +----------------+        +----------------+

                          |
                          v
                +-------------------+
                |   AI Agent        |
                | Tool Calling LLM  |
                +-------------------+
````

---

# 🧠 How It Works

## 1. Log Ingestion

Clients send logs to the FastAPI ingestion service through REST APIs.

Example:

* Application logs
* Error traces
* Service events
* Debugging information

The API validates and publishes logs to RabbitMQ asynchronously.

---

## 2. Message Queue Processing

RabbitMQ decouples ingestion from processing.

Benefits:

* Scalability
* Fault tolerance
* Asynchronous workflows
* Retry handling
* Reduced API response latency

---

## 3. Worker Processing

A .NET background worker consumes messages from RabbitMQ.

The worker:

* Parses logs
* Performs validation
* Handles retries
* Stores logs into PostgreSQL

---

## 4. AI Debugging Assistant

An LLM-powered AI agent retrieves logs through tool-calling APIs.

The AI assistant:

* Searches logs
* Analyzes failures
* Summarizes issues
* Generates debugging insights
* Maintains conversational context using Redis

---

# 🛠️ Tech Stack

## Backend

* FastAPI
* ASP.NET /.NET Worker Services
* REST APIs

## Messaging

* RabbitMQ

## Database

* PostgreSQL

## Caching & Memory

* Redis

## AI

* LangChain
* LLM Tool Calling
* Llama-3 (Groq API)

## DevOps

* Docker
* Docker Compose

---

# 📂 Project Structure

```text
project-root/
│
├── fastapi-service/
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── main.py
│
├── dotnet-worker/
│   ├── Consumers/
│   ├── Services/
│   ├── Models/
│   └── Program.cs
│
├── ai-agent/
│   ├── tools/
│   ├── memory/
│   ├── chains/
│   └── agent.py
│
├── docker-compose.yml
│
└── README.md
```

---

# ⚙️ Local Setup

## Prerequisites

Make sure you have installed:

* Docker
* Docker Compose
* Python 3.11+
* .NET SDK
* PostgreSQL
* Redis

---

# 🔧 Environment Variables

Create a `.env` file:

```env
POSTGRES_HOST=postgres
POSTGRES_DB=logsdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

REDIS_HOST=redis

RABBITMQ_HOST=rabbitmq

GROQ_API_KEY=your_api_key
```

---

# 🐳 Running with Docker Compose

```bash
docker compose up --build
```

This starts:

* FastAPI service
* RabbitMQ
* PostgreSQL
* Redis
* .NET worker
* AI agent

---

# 📡 API Endpoints

## Ingest Log

```http
POST /logs
```

### Request Body

```json
{
  "service": "payment-service",
  "level": "ERROR",
  "message": "Database timeout occurred"
}
```

---

## Query Logs

```http
GET /logs?service=payment-service
```

---

# 🤖 AI Agent Example

Example prompt:

```text
Why is the payment service failing?
```

The AI agent:

1. Calls log retrieval tools
2. Fetches related logs
3. Analyzes failures
4. Generates debugging insights

---

# 🔄 Retry & Fault Handling

The system supports:

* Message acknowledgements
* Retry mechanisms
* Fault-tolerant processing
* Durable queues
* Error logging

---

# 📈 Future Improvements

* Kubernetes deployment
* OpenTelemetry tracing
* Grafana dashboards
* Vector database integration
* Role-based authentication
* Streaming responses
* Multi-agent workflows

---

# 🧪 Example Use Cases

* Centralized logging
* Observability platforms
* AI-assisted debugging
* Distributed system monitoring
* Production incident analysis

---

# 🎯 Key Engineering Concepts Demonstrated

* Distributed systems
* Event-driven architecture
* Async processing
* Queue-based communication
* Backend scalability
* Fault tolerance
* AI tool-calling workflows
* Caching strategies
* Containerized deployments

---

# 👩‍💻 Author

Aanya Kumari

* GitHub: [https://github.com/aanya963](https://github.com/aanya963)
* LinkedIn: [https://linkedin.com/in/aanya-kumari](https://linkedin.com/in/aanya-kumari)

```
```
