from app.infra.repositories.sqlite_conversation_repository import SQLiteConversationRepository


def test_sqlite_repository_persists_between_instances(tmp_path) -> None:
    db_path = tmp_path / "repo.sqlite3"

    repo1 = SQLiteConversationRepository(db_path)
    conv = repo1.create("u1", "demo")
    repo1.add_message(conv.id, "user", "hello")

    repo2 = SQLiteConversationRepository(db_path)
    loaded = repo2.get(conv.id)

    assert loaded is not None
    assert loaded.id == conv.id
    assert loaded.user_id == "u1"
    assert len(loaded.messages) == 1
    assert loaded.messages[0].content == "hello"


def test_sqlite_repository_delete_cascades_messages(tmp_path) -> None:
    db_path = tmp_path / "repo.sqlite3"

    repo = SQLiteConversationRepository(db_path)
    conv = repo.create("u1", "demo")
    repo.add_message(conv.id, "user", "hello")

    assert repo.delete(conv.id) is True
    assert repo.get(conv.id) is None

