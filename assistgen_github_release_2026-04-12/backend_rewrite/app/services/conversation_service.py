from __future__ import annotations

from dataclasses import asdict

from ..domain.errors import ConversationNotFoundError
from ..domain.repositories import ConversationRepository


class ConversationService:
    def __init__(self, repository: ConversationRepository) -> None:
        self._repository = repository

    def create(self, user_id: str, name: str) -> dict:
        return asdict(self._repository.create(user_id, name))

    def list_by_user(self, user_id: str) -> list[dict]:
        return [asdict(c) for c in self._repository.list_by_user(user_id)]

    def get_messages(self, conversation_id: str) -> list[dict]:
        conv = self._repository.get(conversation_id)
        if conv is None:
            raise ConversationNotFoundError("conversation not found")
        return [asdict(m) for m in conv.messages]

    def rename(self, conversation_id: str, name: str) -> dict:
        conv = self._repository.get(conversation_id)
        if conv is None:
            raise ConversationNotFoundError("conversation not found")
        return asdict(self._repository.rename(conversation_id, name))

    def delete(self, conversation_id: str) -> bool:
        ok = self._repository.delete(conversation_id)
        if not ok:
            raise ConversationNotFoundError("conversation not found")
        return ok

    def append_message(self, conversation_id: str, role: str, content: str) -> dict:
        conv = self._repository.get(conversation_id)
        if conv is None:
            raise ConversationNotFoundError("conversation not found")
        return asdict(self._repository.add_message(conversation_id, role, content))

