from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .core.container import build_container


def create_app() -> FastAPI:
    app = FastAPI(title="AssistGen Rewrite API", version="0.2.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.container = build_container()
    app.include_router(api_router)
    return app


app = create_app()

