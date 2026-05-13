from fastapi.testclient import TestClient

from app.main import create_app


def test_chat_sse_contract_done_frame(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(tmp_path / "contract.sqlite3"))
    client = TestClient(create_app())

    with client.stream("POST", "/api/chat", json={"message": "hello", "stream": True}) as resp:
        assert resp.status_code == 200
        body = "".join(resp.iter_text())

    assert "data: [DONE]" in body


def test_chat_with_conversation_context_appends_history(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(tmp_path / "contract.sqlite3"))
    client = TestClient(create_app())

    created = client.post(
        "/api/conversations",
        json={"user_id": "u2", "name": "ctx"},
    )
    cid = created.json()["data"]["id"]

    chat_resp = client.post(
        "/api/chat",
        json={
            "user_id": "u2",
            "conversation_id": cid,
            "message": "question",
            "stream": False,
        },
    )
    assert chat_resp.status_code == 200

    messages = client.get(f"/api/conversations/{cid}/messages")
    assert messages.status_code == 200
    payload = messages.json()["data"]
    assert len(payload) == 2
    assert payload[0]["role"] == "user"
    assert payload[1]["role"] == "assistant"


def test_langgraph_contract_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(tmp_path / "contract.sqlite3"))
    client = TestClient(create_app())

    query = client.post(
        "/api/langgraph/query",
        json={"thread_id": "t1", "query": "next"},
    )
    assert query.status_code == 200
    assert query.json()["data"]["status"] == "ready_for_resume"

    resume = client.post(
        "/api/langgraph/resume",
        json={"thread_id": "t1", "checkpoint": "cp_rewrite_001"},
    )
    assert resume.status_code == 200
    assert resume.json()["data"]["status"] == "completed"


def test_sqlite_persistence_survives_new_app_instance(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "persist.sqlite3"
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(db_path))

    client1 = TestClient(create_app())
    created = client1.post("/api/conversations", json={"user_id": "u3", "name": "persist"})
    cid = created.json()["data"]["id"]
    client1.post(
        "/api/chat",
        json={
            "user_id": "u3",
            "conversation_id": cid,
            "message": "hello sqlite",
            "stream": False,
        },
    )

    client2 = TestClient(create_app())
    conversations = client2.get("/api/conversations/user/u3")
    assert conversations.status_code == 200
    assert len(conversations.json()["data"]) == 1

    messages = client2.get(f"/api/conversations/{cid}/messages")
    assert messages.status_code == 200
    assert len(messages.json()["data"]) == 2
    assert messages.json()["data"][0]["content"] == "hello sqlite"


def test_chat_invalid_conversation_returns_404(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(tmp_path / "contract.sqlite3"))
    client = TestClient(create_app())

    resp = client.post(
        "/api/chat",
        json={
            "user_id": "u404",
            "conversation_id": "missing-id",
            "message": "hello",
            "stream": False,
        },
    )
    assert resp.status_code == 404


def test_upload_then_search_roundtrip(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ASSISTGEN_DB_PATH", str(tmp_path / "contract.sqlite3"))
    client = TestClient(create_app())

    upload = client.post(
        "/api/upload",
        files={"file": ("taobao_rules.txt", "七天无理由退货规则", "text/plain")},
    )
    assert upload.status_code == 200

    search = client.post("/api/search", json={"query": "七天无理由", "top_k": 3})
    assert search.status_code == 200
    hits = search.json()["data"]["hits"]
    assert len(hits) >= 1
    assert hits[0]["title"] == "taobao_rules.txt"

