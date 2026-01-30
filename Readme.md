# Event ingestion and analytics
Backend application built with FastAPI using Pydantic, Docker, Redis, PostgreSQL.

## Quick Start (Locally)
### 1. Clone the repository

> git clone git@github.com:LobiSZ9Iblami/event_ingestion.git


### 2. Create and activate a virtual environment

> python -m venv .venv

> Windows
> 
> .venv\Scripts\activate
> 
> Linux/macOS
> 
> source .venv/bin/activate
 

### 3. Install dependencies

> pip install -r requirements.txt
 

### 4. Create a .env file in the project root

HOST=0.0.0.0  
PORT=8000

### Running Tests

> pytest

## Running with Docker
###  1. Build and run the container with docker-compose
> docker-compose up --build

### Open in browser

http://localhost:8000

```
Common Docker Commands

Build and start:
> docker-compose up --build 

To run a benchmark:
> docker compose —profile benchmark up

Stop
> docker-compose down

List of containers
> docker ps
```
### 2. Comments to Docker
Separate services, separate Dockerfiles, and containers have been created for the benchmark and worker.   
To run the benchmark, you need to initialize it with a separate docker command - see the separate command above.

> Dockerfile.worker
> 
> To check if worker runs - ___docker-compose logs worker -f___



> Dockerfile.load_generator


## DB

### Add Postgresql & Redis via the docker
#### 1. In the .env add DB parameters 
```
    # Postgresql db settings
    POSTGRES_USER = postgres
    POSTGRES_PASSWORD = postgres_123
    POSTGRES_DB = postgres
    POSTGRES_HOST = postgres
    POSTGRES_PORT = 5432


    # Redis settings
    REDIS_HOST = redis
    REDIS_PORT = 6379
    REDIS_PASSWORD = 123 <optional>
```

#### 2. Build and run the container with docker-compose
> docker-compose up --build



## DB Migrations
### To create a DB migrations via Docker:
#### 1. You can autogenerate your migration file:
> docker compose exec backend alembic revision --autogenerate -m "your message here"

#### 2. Run migration:
> compose exec backend alembic upgrade head



## Benchmark

⚡ Total events: 100000  
✅ Success: 100000, ❌ Errors: 0   
⏱ Total time: 2204.66s  
🚀 Throughput: 45.36 events/sec

Performed load testing - loaded 100,000 events via the POST /events endpoint.  
100,000 events processed without a single error, but a performance of 45 events/sec is quite low.

### Bottleneck:

1. Redis XREADGROUP:
   2. xreadgroup(..., count=10, block=1000) - limits processing to only 10 messages per cycle.
3. There was a separate insert for each separate event - INSERT INTO events () VALUES ()

### How to fix:
1. Run the benchmark in multiple threads.
2. Increase message processing per cycle to 100 or even 1000.
3. Reduce the block to 100 ms or even 50 ms.
4. Increase ___requests___ and ___batch_size___