from __future__ import annotations

from fastapi import APIRouter, Depends

from ...core.container import AppContainer
from ...schemas import ApiResponse, LangGraphQueryRequest, LangGraphResumeRequest
from ..dependencies import get_container

router = APIRouter()


@router.post("/api/langgraph/query")
def langgraph_query(
    req: LangGraphQueryRequest,
    container: AppContainer = Depends(get_container),
):
    return ApiResponse(data=container.langgraph_service.query(req.thread_id, req.query))


@router.post("/api/langgraph/resume")
def langgraph_resume(
    req: LangGraphResumeRequest,
    container: AppContainer = Depends(get_container),
):
    return ApiResponse(data=container.langgraph_service.resume(req.thread_id, req.checkpoint))

