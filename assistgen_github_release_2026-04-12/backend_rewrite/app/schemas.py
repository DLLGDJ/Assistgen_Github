from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str | None = None
    conversation_id: str | None = None
    message: str = Field(min_length=1)
    stream: bool = True
    model: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ReasonRequest(BaseModel):
    query: str = Field(min_length=1)
    mode: str = "step"


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class ConversationCreateRequest(BaseModel):
    user_id: str
    name: str = "新会话"


class ConversationRenameRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class LangGraphQueryRequest(BaseModel):
    thread_id: str
    query: str


class LangGraphResumeRequest(BaseModel):
    thread_id: str
    checkpoint: str


class ApiResponse(BaseModel):
    code: int = 0
    message: str = "ok"
    data: Any = None

