from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ...core.container import AppContainer
from ...domain.errors import ConversationNotFoundError
from ...schemas import ApiResponse, ConversationCreateRequest, ConversationRenameRequest
from ..dependencies import get_container

router = APIRouter()


@router.post("/api/conversations")
def create_conversation(
    req: ConversationCreateRequest,
    container: AppContainer = Depends(get_container),
):
    return ApiResponse(data=container.conversation_service.create(req.user_id, req.name))


@router.get("/api/conversations/user/{user_id}")
def list_conversations(user_id: str, container: AppContainer = Depends(get_container)):
    return ApiResponse(data=container.conversation_service.list_by_user(user_id))


@router.get("/api/conversations/{conversation_id}/messages")
def get_messages(conversation_id: str, container: AppContainer = Depends(get_container)):
    try:
        return ApiResponse(data=container.conversation_service.get_messages(conversation_id))
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/api/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, container: AppContainer = Depends(get_container)):
    try:
        container.conversation_service.delete(conversation_id)
        return ApiResponse(data={"deleted": True})
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/api/conversations/{conversation_id}/name")
def rename_conversation(
    conversation_id: str,
    req: ConversationRenameRequest,
    container: AppContainer = Depends(get_container),
):
    try:
        return ApiResponse(data=container.conversation_service.rename(conversation_id, req.name))
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

