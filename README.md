# AI Chat API

A **Flask-based REST API** that integrates with [Ollama](https://ollama.ai/) for AI chat responses and uses **PostgreSQL (Supabase)** for data persistence.  
The API manages **users** and **chat messages**, with built-in pagination and clean separation of services, controllers, and routes.  

---

## Table of Contents
- [API Documentation](#api-documentation)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
  - [Environment Variables](#3-environment-variables)
  - [Run Locally](#4-run-locally)
  - [Ollama Setup](#5-setup-ollama)
  - [Run with Docker](#docker-setup)
- [Database](#database)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)



---

## API Documentation

The full API documentation with request details and examples is available at:

[View API Documentation](https://documenter.getpostman.com/view/7117783/2sB3BLk8CM)


---

## Features
- User management (create, fetch, etc.)  
- AI-powered chat with Ollama REST API  
- Chat history stored in PostgreSQL (Supabase)
- Pagination utility for APIs
- User input and DB validations
- Modular folder structure (controllers, services, routes, utils)  
- Dockerized for easy deployment  

---

##  Tech Stack
- **Python 3.11+**  
- **Flask** (REST API framework)  
- **PostgreSQL (Supabase)**  
- **SQLAlchemy (ORM)**  
- **Docker & Docker Compose**  
- **Ollama API** for AI responses  ((LLM integration))

---


## Setup & Installation

### 1. Clone Repository
```bash
git clone https://github.com/mazenaboelanin/ai-chat-api.git
cd ai-chat-api
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

### 3. Environment Variables

Create a .env file in the root directory and configure your variables:

```bash
OLLAMA_URL="http://localhost:11434/api/generate"
DATABASE_URL=postgresql://username:password@localhost:5432/ai_chat_db
```

### 4. Run Locally

```bash
export FLASK_APP=app.app
flask run
```

The API will be available at: http://localhost:5000

### 5. Setup Ollama

Run Ollama Container
```bash
docker run -d -p 11434:11434 ollama/ollama
```

Check running containers
```bash
docker ps
```

Pull gemma3:1b Model
```bash
docker exec -it <container_id> ollama pull gemma3:1b
```

### 6. migration commands

```bash
flask db init       # setup migrations folder
flask db migrate -m "create user and message tables"
flask db upgrade    # apply to database
```


## Docker Setup

This project includes a `Dockerfile` and `docker-compose.yml` for easy containerized setup.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- Supabase connection string and `.env` file ready

Build and start the containers:
```bash
docker-compose up --build
```
Stop Containers
```bash
docker-compose down
```

Restart Containers

```bash
docker-compose up
```

Access Ollama Service and pull gemma3:1b model "IMPORTANT TO GET ANSWERS FROM AGENT"
```bash
docker-compose exec ollama ollama pull gemma3:1b
```

This will download the model and make it available for use inside your API.
Ollama REST API will be exposed at: http://localhost:11434

The app reads environment variables from the file specified in env_file (.env).

Ensure your .env file contains valid Supabase URL.

## Database Setup

Supabase (PostgreSQL) is used as the main database.

- Update your `.env` with the correct `DATABASE_URL`.
- Apply migrations (if using **Alembic** or **Flask-Migrate**).

---

## API Endpoints

### Chat Routes
- **POST** `/api/v1/chat/ask` → ask a question to the AI agent and get the answer.  
- **GET** `/api/v1/chat/history/<user_id>?page=1&per_page=5` → Get chat history for a user - paginated.  
- **GET** `/api/v1/chat/all?page=1&per_page=5` → Get all chat history across all users - paginated.  


### User Routes
- **POST** `/api/v1/users` → Create a new user.  
- **GET** `/api/v1/users/<id>` → Get user details.  
- **GET** `/api/v1/users?page=1&per_page=5` → Get all user - paginated.



##  Project Structure

```bash
app/
├── controllers/      # API route controllers
├── models/           # SQLAlchemy models
├── routes/           # API route definitions
├── services/         # Business logic and external API integrations
│   ├── api/          # Ollama API integration
│   └── db/           # Database service logic
├── utils/            # Utility functions and pagination
└── app.py            # Main Flask app entry point

config/
├── db.py             # Database connection setup

.env                  # Environment variables
requirements.txt      # Python dependencies
docker-compose.yml    # Docker services (API, Ollama)
Dockerfile            # Docker build file for Flask API

```