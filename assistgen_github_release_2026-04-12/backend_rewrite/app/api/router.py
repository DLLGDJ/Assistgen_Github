from __future__ import annotations

from fastapi import APIRouter

from .routers.chat import router as chat_router
from .routers.conversations import router as conversations_router
from .routers.health import router as health_router
from .routers.langgraph import router as langgraph_router
from .routers.upload import router as upload_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(conversations_router)
api_router.include_router(upload_router)
api_router.include_router(langgraph_router)

