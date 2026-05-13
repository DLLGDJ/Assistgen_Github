from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from ...domain.errors import ConversationNotFoundError
from ...schemas import ApiResponse, ChatRequest, ReasonRequest, SearchRequest
from ..dependencies import get_container
from ...core.container import AppContainer

router = APIRouter()


@router.post("/api/chat")
async def chat(req: ChatRequest, container: AppContainer = Depends(get_container)):
    try:
        if req.stream:
            return StreamingResponse(
                container.chat_service.stream(
                    req.message,
                    req.user_id,
                    req.conversation_id,
                    req.model,
                ),
                media_type="text/event-stream",
            )

        return JSONResponse(
            ApiResponse(
                data=await container.chat_service.chat_once(
                    req.message,
                    req.user_id,
                    req.conversation_id,
                    req.model,
                )
            ).model_dump()
        )
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/api/reason")
def reason(req: ReasonRequest, container: AppContainer = Depends(get_container)):
    return ApiResponse(data=container.knowledge_service.reason(req.query, req.mode))


@router.post("/api/search")
def search(req: SearchRequest, container: AppContainer = Depends(get_container)):
    return ApiResponse(data=container.knowledge_service.search(req.query, req.top_k))


