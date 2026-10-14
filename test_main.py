"""Tests for the Task Manager API using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

from main import app, tasks


@pytest.fixture
def client():
    """Fresh TestClient with empty tasks before each test."""
    tasks.clear()
    return TestClient(app)


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, World!"}


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_empty(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []


def test_create_task(client):
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Buy milk"
    assert body["done"] is False


def test_create_task_missing_title(client):
    r = client.post("/tasks", json={"done": True})
    assert r.status_code == 422


def test_get_task_by_id(client):
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    r = client.get("/tasks/1")
    assert r.status_code == 200
    assert r.json()["title"] == "Task B"


def test_get_task_not_found(client):
    r = client.get("/tasks/99")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_update_task(client):
    client.post("/tasks", json={"title": "Task A"})
    r = client.put("/tasks/0", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True
    assert r.json()["title"] == "Task A"


def test_delete_task(client):
    client.post("/tasks", json={"title": "Task A"})
    r = client.delete("/tasks/0")
    assert r.status_code == 204
    assert client.get("/tasks").json() == []
