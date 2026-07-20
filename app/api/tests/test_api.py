import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app(f"sqlite:///{tmp_path}/test.db")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_healthz_ok(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_readyz_ok_when_db_reachable(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ready"


def test_create_task_and_list(client):
    resp = client.post("/api/tasks", json={"title": "provision the cluster"})
    assert resp.status_code == 201
    created = resp.get_json()
    assert created["title"] == "provision the cluster"
    assert created["done"] is False

    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    tasks = resp.get_json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == created["id"]


def test_create_task_requires_title(client):
    resp = client.post("/api/tasks", json={"done": True})
    assert resp.status_code == 400
    assert "title" in resp.get_json()["error"]


def test_tasks_listed_in_insertion_order(client):
    for title in ["first", "second", "third"]:
        client.post("/api/tasks", json={"title": title})
    titles = [t["title"] for t in client.get("/api/tasks").get_json()]
    assert titles == ["first", "second", "third"]
