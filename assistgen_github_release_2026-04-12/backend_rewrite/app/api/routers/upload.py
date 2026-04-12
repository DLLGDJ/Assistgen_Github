from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from ...core.container import AppContainer
from ...schemas import ApiResponse
from ..dependencies import get_container

router = APIRouter()


@router.post("/api/upload")
async def upload(file: UploadFile = File(...), container: AppContainer = Depends(get_container)):
    content = await file.read()
    return ApiResponse(
        data=container.upload_service.file_meta(file.filename, file.content_type, content)
    )


@router.post("/api/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    container: AppContainer = Depends(get_container),
):
    content = await file.read()
    return ApiResponse(data=container.upload_service.image_meta(file.filename, content))

