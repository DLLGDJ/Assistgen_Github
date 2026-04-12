from __future__ import annotations

from dataclasses import dataclass

from ..infra.llm_client import LLMClient
from ..infra.repositories.in_memory_conversation_repository import InMemoryConversationRepository
from ..infra.repositories.sqlite_knowledge_repository import SQLiteKnowledgeRepository
from ..infra.repositories.sqlite_conversation_repository import SQLiteConversationRepository
from ..infra.sqlite import initialize_database
from ..services.chat_service import ChatService
from ..services.conversation_service import ConversationService
from ..services.knowledge_service import KnowledgeService
from ..services.langgraph_service import LangGraphService
from ..services.upload_service import UploadService
from .settings import load_settings


@dataclass
class AppContainer:
    conversation_service: ConversationService
    chat_service: ChatService
    knowledge_service: KnowledgeService
    upload_service: UploadService
    langgraph_service: LangGraphService


def build_container() -> AppContainer:
    settings = load_settings()
    initialize_database(settings.db_path)
    if settings.conversation_store == "memory":
        repo = InMemoryConversationRepository()
    else:
        repo = SQLiteConversationRepository(settings.db_path)

    conversation_service = ConversationService(repo)
    knowledge_repository = SQLiteKnowledgeRepository(settings.db_path)
    llm_client = LLMClient(
        provider=settings.llm_provider,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        default_model=settings.llm_default_model,
        timeout_seconds=settings.llm_timeout_seconds,
    )

    return AppContainer(
        conversation_service=conversation_service,
        chat_service=ChatService(conversation_service, llm_client),
        knowledge_service=KnowledgeService(knowledge_repository),
        upload_service=UploadService(knowledge_repository),
        langgraph_service=LangGraphService(),
    )


