from __future__ import annotations

from .domain.models import Conversation, Message
from .infra.repositories.sqlite_conversation_repository import SQLiteConversationRepository

# Compatibility alias for earlier imports in this rewrite project.
InMemoryConversationStore = SQLiteConversationRepository

__all__ = ["Message", "Conversation", "InMemoryConversationStore"]
