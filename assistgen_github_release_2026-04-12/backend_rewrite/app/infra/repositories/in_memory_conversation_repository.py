from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from ...domain.models import Conversation, Message


class InMemoryConversationRepository:
    """Thread-safe in-memory repository used by the rewrite backend."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._conversations: dict[str, Conversation] = {}

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    def create(self, user_id: str, name: str) -> Conversation:
        with self._lock:
            now = self._now()
            conv = Conversation(
                id=uuid4().hex,
                user_id=user_id,
                name=name,
                created_at=now,
                updated_at=now,
            )
            self._conversations[conv.id] = conv
            return conv

    def list_by_user(self, user_id: str) -> list[Conversation]:
        with self._lock:
            return [c for c in self._conversations.values() if c.user_id == user_id]

    def get(self, conversation_id: str) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def add_message(self, conversation_id: str, role: str, content: str) -> Message:
        with self._lock:
            conv = self._conversations[conversation_id]
            msg = Message(
                id=uuid4().hex,
                role=role,
                content=content,
                created_at=self._now(),
            )
            conv.messages.append(msg)
            conv.updated_at = msg.created_at
            return msg

    def rename(self, conversation_id: str, name: str) -> Conversation:
        with self._lock:
            conv = self._conversations[conversation_id]
            conv.name = name
            conv.updated_at = self._now()
            return conv

    def delete(self, conversation_id: str) -> bool:
        with self._lock:
            return self._conversations.pop(conversation_id, None) is not None
