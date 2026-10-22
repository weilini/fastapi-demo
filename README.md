# Task Manager API

[FastAPI CI](https://github.com/weilini/fastapi-demo/actions/workflows/ci.yml/badge.svg)

A simple REST API built with FastAPI — my first Software Engineering project.

 **Live API Demo:** [https://fastapi-demo-hbqh.onrender.com/docs](https://fastapi-demo-hbqh.onrender.com/docs)



## Endpoints

- `GET /` — root
- `GET /health` — health check
- `GET /tasks` — list all tasks
- `GET /tasks/{id}` — get one task
- `POST /tasks` — create a task
- `PUT /tasks/{id}` — update a task
- `DELETE /tasks/{id}` — delete a task

## Tech Stack

- FastAPI — modern Python web framework
- Pydantic — data validation
- Uvicorn — ASGI server
- pytest + TestClient — 9 automated tests

## Setup

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Server runs at http://127.0.0.1:8000
API docs at http://127.0.0.1:8000/docs

## Run tests

pytest test_main.py -v

## What I learned

- FastAPI routing (GET, POST, PUT, DELETE)
- Pydantic models for request/response validation
- Path parameters and error handling (HTTPException)
- Automatic OpenAPI documentation
- Testing FastAPI apps with pytest + TestClient
