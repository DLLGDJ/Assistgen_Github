from __future__ import annotations

from typing import Protocol

from .models import Conversation, Message


class ConversationRepository(Protocol):
    def create(self, user_id: str, name: str) -> Conversation: ...

    def list_by_user(self, user_id: str) -> list[Conversation]: ...

    def get(self, conversation_id: str) -> Conversation | None: ...

    def add_message(self, conversation_id: str, role: str, content: str) -> Message: ...

    def rename(self, conversation_id: str, name: str) -> Conversation: ...

    def delete(self, conversation_id: str) -> bool: ...

