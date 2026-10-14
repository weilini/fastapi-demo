"""Tests for the Task Manager API — using a separate test database."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app, get_db

TEST_DB_URL = "sqlite:///./test_tasks.db"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
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
    assert "id" in body


def test_create_task_missing_title(client):
    r = client.post("/tasks", json={"done": True})
    assert r.status_code == 422


def test_get_task_by_id(client):
    client.post("/tasks", json={"title": "Task A"})
    r2 = client.post("/tasks", json={"title": "Task B"})
    task_id = r2.json()["id"]

    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Task B"


def test_get_task_not_found(client):
    r = client.get("/tasks/9999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_update_task(client):
    r = client.post("/tasks", json={"title": "Task A"})
    task_id = r.json()["id"]

    r = client.put(f"/tasks/{task_id}", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True
    assert r.json()["title"] == "Task A"


def test_delete_task(client):
    r = client.post("/tasks", json={"title": "Task A"})
    task_id = r.json()["id"]

    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204

    assert client.get("/tasks").json() == []