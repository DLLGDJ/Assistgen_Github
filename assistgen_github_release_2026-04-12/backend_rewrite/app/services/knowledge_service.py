from __future__ import annotations

from ..infra.repositories.sqlite_knowledge_repository import SQLiteKnowledgeRepository

class KnowledgeService:
    def __init__(self, knowledge_repository: SQLiteKnowledgeRepository) -> None:
        self._knowledge_repository = knowledge_repository

    def reason(self, query: str, mode: str) -> dict:
        hits = self._knowledge_repository.search(query, top_k=3)
        return {
            "query": query,
            "mode": mode,
            "steps": [
                "澄清问题范围",
                "检索上下文",
                "生成答复",
                "输出可执行建议",
            ],
            "evidence": hits,
        }

    def search(self, query: str, top_k: int) -> dict:
        hits = self._knowledge_repository.search(query, top_k)
        return {"query": query, "hits": hits}


