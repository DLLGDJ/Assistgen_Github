from __future__ import annotations


class LangGraphService:
    @staticmethod
    def query(thread_id: str, query: str) -> dict:
        return {
            "thread_id": thread_id,
            "status": "ready_for_resume",
            "checkpoint": "cp_rewrite_001",
            "reply": f"[rewrite] 已处理 query: {query}",
        }

    @staticmethod
    def resume(thread_id: str, checkpoint: str) -> dict:
        return {
            "thread_id": thread_id,
            "checkpoint": checkpoint,
            "status": "completed",
            "reply": "[rewrite] 工作流已恢复并完成。",
        }

