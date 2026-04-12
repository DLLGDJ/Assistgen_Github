from __future__ import annotations

from ..infra.repositories.sqlite_knowledge_repository import SQLiteKnowledgeRepository


class UploadService:
    def __init__(self, knowledge_repository: SQLiteKnowledgeRepository) -> None:
        self._knowledge_repository = knowledge_repository

    def file_meta(self, filename: str | None, content_type: str | None, content: bytes) -> dict:
        safe_filename = filename or "uploaded-file"
        text = content.decode("utf-8", errors="ignore").strip()
        preview = text[:120]
        saved = self._knowledge_repository.add(safe_filename, text or safe_filename)
        return {
            "id": saved.id,
            "filename": safe_filename,
            "content_type": content_type,
            "bytes": len(content),
            "preview": preview,
        }

    def image_meta(self, filename: str | None, content: bytes) -> dict:
        return {
            "filename": filename,
            "bytes": len(content),
        }



