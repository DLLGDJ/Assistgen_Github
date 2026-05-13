from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import uuid

from ..sqlite import open_connection


@dataclass
class KnowledgeItem:
    id: str
    filename: str
    content: str
    created_at: str


class SQLiteKnowledgeRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def add(self, filename: str, content: str) -> KnowledgeItem:
        now = datetime.now(timezone.utc).isoformat()
        item_id = str(uuid.uuid4())
        with open_connection(self._db_path) as conn:
            conn.execute(
                "INSERT INTO knowledge_items (id, filename, content, created_at) VALUES (?, ?, ?, ?)",
                (item_id, filename, content, now),
            )
        return KnowledgeItem(id=item_id, filename=filename, content=content, created_at=now)

    def search(self, query: str, top_k: int) -> list[dict]:
        token = query.strip()
        if not token:
            return []

        like_query = f"%{token}%"
        with open_connection(self._db_path) as conn:
            rows = conn.execute(
                """
                SELECT id, filename, content, created_at
                FROM knowledge_items
                WHERE content LIKE ? OR filename LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (like_query, like_query, top_k),
            ).fetchall()

        hits: list[dict] = []
        for row in rows:
            content = row["content"] or ""
            score = min(1.0, max(0.1, content.lower().count(token.lower()) * 0.2 + 0.4))
            snippet = content[:180]
            hits.append(
                {
                    "id": row["id"],
                    "title": row["filename"],
                    "snippet": snippet,
                    "score": round(score, 2),
                    "created_at": row["created_at"],
                }
            )
        return hits

