# Distributed Logging & AI Debugging System

A distributed log processing and observability backend that ingests logs asynchronously, processes them through worker services, stores them reliably, and uses an LLM-powered AI agent to analyze logs and generate debugging insights.

---

# 1. Problem Statement

Modern distributed applications generate massive volumes of logs across multiple services. Traditional logging systems often struggle with:

* High-throughput ingestion
* Fault-tolerant processing
* Real-time debugging assistance
* Centralized observability
* Intelligent error analysis

This project solves these problems by building a scalable event-driven logging system with asynchronous processing and AI-powered debugging assistance.

The system:

* Collects logs from services through REST APIs
* Queues logs using RabbitMQ
* Processes logs asynchronously through workers
* Stores logs in PostgreSQL
* Uses Redis for caching and session memory
* Integrates Llama-3 via Groq for AI-based log analysis

---

# 2. Architecture Diagram

```text
                    +------------------+
                    | Client Services  |
                    |  / Applications  |
                    +--------+---------+
                             |
                             v
                  +--------------------+
                  | FastAPI Ingestion  |
                  |      Service       |
                  +---------+----------+
                            |
                            v
                     +-------------+
                     | RabbitMQ    |
                     | Message Bus |
                     +------+------+ 
                            |
          +-----------------+------------------+
          |                                    |
          v                                    v
+----------------------+         +----------------------+
| Log Processing Worker|         | Retry / Failure Queue|
|      (.NET / C#)     |         |                      |
+----------+-----------+         +----------------------+
           |
           v
+----------------------+
| PostgreSQL Database  |
|   Log Persistence    |
+----------+-----------+
           |
           v
+----------------------+
| AI Debugging Agent   |
| (Llama-3 via Groq)   |
+----------+-----------+
           |
    +------+------+
    | Redis Cache |
    | Session Mem |
    +-------------+
```

---

# 3. Tech Stack

## Backend

* Python
* FastAPI
* C#
* .NET

## Messaging & Distributed Processing

* RabbitMQ

## Databases & Caching

* PostgreSQL
* Redis

## AI Integration

* Llama-3
* Groq API

## APIs & Communication

* REST APIs

---

# 4. Flow Explanation

## Step 1 — Log Ingestion

Applications send logs to the FastAPI ingestion service through REST APIs.

## Step 2 — Message Queueing

The ingestion service publishes logs to RabbitMQ queues for asynchronous processing.

## Step 3 — Distributed Processing

Worker services consume logs from queues and process them independently.

This ensures:

* Scalability
* Decoupled architecture
* Fault tolerance
* Better throughput

## Step 4 — Persistence

Processed logs are stored in PostgreSQL for querying and analysis.

## Step 5 — Failure Handling

Failed log processing attempts are retried through retry queues.

## Step 6 — AI Analysis

The AI agent:

* Fetches logs through APIs
* Understands system errors
* Generates debugging insights
* Explains possible root causes
* Suggests fixes

## Step 7 — Caching & Memory

Redis is used for:

* Response caching
* Session memory
* Faster repeated queries

---

# 5. Features

* Distributed log ingestion architecture
* Event-driven asynchronous processing
* RabbitMQ-based decoupled communication
* Retry and failure queue handling
* PostgreSQL log persistence
* AI-powered debugging assistant
* Redis caching and conversational memory
* REST API integration
* Scalable worker-based design
* Fault-tolerant processing pipeline

---

# 6. Local Setup

## Clone Repository

```bash
git clone https://github.com/yourusername/repository-name.git
cd repository-name
```

---

## Backend Setup (FastAPI)

```bash
cd ingestion-service

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## .NET Worker Setup

```bash
cd worker-service

dotnet restore

dotnet run
```

---

## RabbitMQ Setup

Using Docker:

```bash
docker run -d \
--hostname rabbitmq \
--name rabbitmq \
-p 5672:5672 \
-p 15672:15672 \
rabbitmq:3-management
```

RabbitMQ Dashboard:

* [http://localhost:15672](http://localhost:15672)

Default credentials:

```text
username: guest
password: guest
```

---

## PostgreSQL Setup

Create database:

```sql
CREATE DATABASE logsdb;
```

Update connection string in configuration files.

---

## Redis Setup

Using Docker:

```bash
docker run -d -p 6379:6379 redis
```

---

## Environment Variables

Create `.env`:

```env
DATABASE_URL=your_postgres_url
RABBITMQ_URL=your_rabbitmq_url
REDIS_URL=your_redis_url
GROQ_API_KEY=your_api_key
```

---

# 7. Screenshots

## API Log Ingestion

```md
Add screenshot here:
screenshots/log-ingestion.png
```

---

## RabbitMQ Queues

```md
Add screenshot here:
screenshots/rabbitmq-dashboard.png
```

---

## PostgreSQL Stored Logs

```md
Add screenshot here:
screenshots/postgres-logs.png
```

---

## AI Debugging Response

```md
Add screenshot here:
screenshots/ai-analysis.png
```

---

# 8. Future Improvements

* Real-time log streaming dashboard
* Kubernetes deployment support
* OpenTelemetry integration
* Elasticsearch support
* Grafana visualization
* Role-based authentication
* Multi-tenant architecture
* AI anomaly detection
* Alerting system
* Vector database integration for semantic log search
* Distributed tracing support
* Docker Compose production setup

---

# Sample AI Debugging Query

```text
"Why are payment requests failing with HTTP 500 errors?"
```

## Example AI Response

```text
Possible root cause:
- Database connection pool exhaustion

Detected patterns:
- Increased timeout exceptions
- Spike in failed queries

Suggested fixes:
- Increase DB pool size
- Add retry logic
- Optimize slow queries
```

---

# Author

**Your Name**

GitHub:
[https://github.com/yourusername](https://github.com/yourusername)
