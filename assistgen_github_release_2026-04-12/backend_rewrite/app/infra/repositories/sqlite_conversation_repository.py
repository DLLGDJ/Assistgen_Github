from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ...domain.models import Conversation, Message
from ..sqlite import default_db_path, initialize_database, open_connection


class SQLiteConversationRepository:
    """SQLite-backed conversation repository used by the rewrite backend."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = Path(db_path) if db_path is not None else default_db_path()
        initialize_database(self._db_path)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    @staticmethod
    def _conversation_from_row(row, messages: list[Message] | None = None) -> Conversation:
        return Conversation(
            id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            messages=messages or [],
        )

    @staticmethod
    def _message_from_row(row) -> Message:
        return Message(
            id=row["id"],
            role=row["role"],
            content=row["content"],
            created_at=row["created_at"],
        )

    def _load_messages(self, conversation_id: str) -> list[Message]:
        with open_connection(self._db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, role, content, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY created_at ASC, rowid ASC
                """,
                (conversation_id,),
            ).fetchall()
        return [self._message_from_row(row) for row in rows]

    def create(self, user_id: str, name: str) -> Conversation:
        now = self._now()
        conversation_id = uuid4().hex
        with open_connection(self._db_path) as conn:
            conn.execute(
                """
                INSERT INTO conversations (id, user_id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (conversation_id, user_id, name, now, now),
            )
        return Conversation(
            id=conversation_id,
            user_id=user_id,
            name=name,
            created_at=now,
            updated_at=now,
            messages=[],
        )

    def list_by_user(self, user_id: str) -> list[Conversation]:
        with open_connection(self._db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, user_id, name, created_at, updated_at
                FROM conversations
                WHERE user_id = ?
                ORDER BY created_at ASC, id ASC
                """,
                (user_id,),
            ).fetchall()
        return [self._conversation_from_row(row) for row in rows]

    def get(self, conversation_id: str) -> Conversation | None:
        with open_connection(self._db_path) as conn:
            row = conn.execute(
                """
                SELECT id, user_id, name, created_at, updated_at
                FROM conversations
                WHERE id = ?
                """,
                (conversation_id,),
            ).fetchone()
        if row is None:
            return None
        return self._conversation_from_row(row, self._load_messages(conversation_id))

    def add_message(self, conversation_id: str, role: str, content: str) -> Message:
        message = Message(
            id=uuid4().hex,
            role=role,
            content=content,
            created_at=self._now(),
        )
        with open_connection(self._db_path) as conn:
            exists = conn.execute(
                "SELECT 1 FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone()
            if exists is None:
                raise KeyError(conversation_id)

            conn.execute(
                """
                INSERT INTO messages (id, conversation_id, role, content, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (message.id, conversation_id, message.role, message.content, message.created_at),
            )
            conn.execute(
                "UPDATE conversations SET updated_at = ? WHERE id = ?",
                (message.created_at, conversation_id),
            )
        return message

    def rename(self, conversation_id: str, name: str) -> Conversation:
        updated_at = self._now()
        with open_connection(self._db_path) as conn:
            cur = conn.execute(
                "UPDATE conversations SET name = ?, updated_at = ? WHERE id = ?",
                (name, updated_at, conversation_id),
            )
            if cur.rowcount == 0:
                raise KeyError(conversation_id)
        conv = self.get(conversation_id)
        if conv is None:
            raise KeyError(conversation_id)
        return conv

    def delete(self, conversation_id: str) -> bool:
        with open_connection(self._db_path) as conn:
            cur = conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            return cur.rowcount > 0

