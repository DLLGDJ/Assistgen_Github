from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Message:
    id: str
    role: str
    content: str
    created_at: str


@dataclass
class Conversation:
    id: str
    user_id: str
    name: str
    created_at: str
    updated_at: str
    messages: list[Message] = field(default_factory=list)

