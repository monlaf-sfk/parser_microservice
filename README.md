
# Async Parser Microservice

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121-009688?logo=fastapi&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.12-orange?logo=rabbitmq&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-red?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![uv](https://img.shields.io/badge/uv-0.4-purple)

A scalable, asynchronous microservice architecture for parsing web pages. This project demonstrates the **Producer-Consumer** pattern using **FastAPI** as the interface, **RabbitMQ** for task distribution, and **Taskiq** for background worker management.

## 🚀 Features

* **Asynchronous Architecture:** Non-blocking API that delegates heavy parsing tasks to background workers.
* **Modern Python Stack:** Built with Python 3.12 and **uv** for lightning-fast dependency management.
* **Reliable Messaging:** Uses **RabbitMQ** to ensure tasks are processed even under high load.
* **Result Caching:** Stores parsing results in **Redis** for fast retrieval and TTL management.
* **Containerized:** Fully Dockerized setup with `docker-compose` for one-command deployment.
* **Scraping:** Uses `httpx` and `BeautifulSoup4` for efficient HTML parsing.

## 🛠️ Tech Stack

* **Web API:** FastAPI
* **Task Queue:** Taskiq (Modern alternative to Celery, fully async)
* **Broker:** RabbitMQ (via `aio-pika`)
* **Result Backend:** Redis
* **Package Manager:** uv
* **Infrastructure:** Docker & Docker Compose

## 🏗️ Architecture Flow

1.  **Client** sends a `POST /parse` request with a URL.
2.  **FastAPI (Producer)** pushes the parsing task to the **RabbitMQ** queue and immediately returns a `task_id`.
3.  **Worker (Consumer)** picks up the task, scrapes the website using `httpx` and `BeautifulSoup`, and processes the data.
4.  **Worker** saves the result (or error) into **Redis**.
5.  **Client** polls `GET /result/{task_id}` to retrieve the data from **Redis**.

## ⚡ Quick Start

You only need **Docker** and **Docker Compose** installed.

1.  **Clone the repository**
    ```bash
    git clone <YOUR_REPO_URL>
    cd parser_microservice
    ```

2.  **Run with Docker Compose**
    This command builds the images and starts all services (Web, Worker, RabbitMQ, Redis).
    ```bash
    docker-compose up --build
    ```

3.  **Access the API**
    Open your browser and go to the interactive Swagger documentation:
    **http://localhost:8000/docs**

## 🔌 API Usage

### 1. Submit a Task
**Endpoint:** `POST /parse`

```bash
curl -X 'POST' \
  'http://localhost:8000/parse?url=https%3A%2F%2Fpython.org' \
  -H 'accept: application/json'
````

**Response:**

```json
{
  "task_id": "3f6b8a1c-...",
  "message": "Parsing started"
}
```

### 2\. Get Result

**Endpoint:** `GET /result/{task_id}`

```bash
curl -X 'GET' \
  'http://localhost:8000/result/3f6b8a1c-...' \
  -H 'accept: application/json'
```

**Response (Pending):**

```json
{
  "status": "processing"
}
```

**Response (Completed):**

```json
{
  "status": "ready",
  "data": {
    "url": "[https://python.org](https://python.org)",
    "title": "Welcome to Python.org",
    "status": "done"
  }
}
```

## 💻 Local Development (without Docker)

If you want to run it locally, you will need `uv` installed.

1.  **Install dependencies**

    ```bash
    uv sync
    ```

2.  **Start Infrastructure (RabbitMQ & Redis)**
    You still need the brokers running.

    ```bash
    docker-compose up -d rabbitmq redis
    ```

3.  **Run the API**

    ```bash
    uv run uvicorn main:app --reload
    ```

4.  **Run the Worker**

    ```bash
    uv run taskiq worker broker:broker_obj tasks
    ```

## 📝 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

