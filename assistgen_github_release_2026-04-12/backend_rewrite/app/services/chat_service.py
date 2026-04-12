from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator

from ..infra.llm_client import LLMClient
from ..services.conversation_service import ConversationService


class ChatService:
    def __init__(self, conversation_service: ConversationService, llm_client: LLMClient) -> None:
        self._conversation_service = conversation_service
        self._llm_client = llm_client

    async def stream(
        self,
        message: str,
        user_id: str | None,
        conversation_id: str | None,
        model: str | None = None,
    ) -> AsyncIterator[str]:
        chunks: list[str] = []

        if conversation_id and user_id:
            self._conversation_service.append_message(conversation_id, "user", message)

        async for item in self._llm_client.stream(message, model):
            payload = {"delta": item}
            yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            chunks.append(item)
            await asyncio.sleep(0.05)

        if conversation_id and user_id:
            self._conversation_service.append_message(
                conversation_id,
                "assistant",
                "".join(chunks),
            )

        yield "data: [DONE]\n\n"

    async def chat_once(
        self,
        message: str,
        user_id: str | None,
        conversation_id: str | None,
        model: str | None = None,
    ) -> dict:
        answer = await self._llm_client.complete(message, model)

        if conversation_id and user_id:
            self._conversation_service.append_message(conversation_id, "user", message)
            self._conversation_service.append_message(conversation_id, "assistant", answer)

        return {"answer": answer}


