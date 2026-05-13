from fastapi.testclient import TestClient

from app.main import create_app


def test_health(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(tmp_path / "smoke.sqlite3"))
    client = TestClient(create_app())
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_conversation_lifecycle(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(tmp_path / "smoke.sqlite3"))
    client = TestClient(create_app())

    create_resp = client.post("/api/conversations", json={"user_id": "u1", "name": "demo"})
    assert create_resp.status_code == 200
    cid = create_resp.json()["data"]["id"]

    list_resp = client.get("/api/conversations/user/u1")
    assert list_resp.status_code == 200
    assert len(list_resp.json()["data"]) >= 1

    rename_resp = client.put(f"/api/conversations/{cid}/name", json={"name": "renamed"})
    assert rename_resp.status_code == 200
    assert rename_resp.json()["data"]["name"] == "renamed"

    delete_resp = client.delete(f"/api/conversations/{cid}")
    assert delete_resp.status_code == 200

