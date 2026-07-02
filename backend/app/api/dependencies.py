from functools import lru_cache

from app.core.config import get_settings
from app.domain.chat.interfaces import ConversationalAssistant
from app.domain.consensus.interfaces import CommonGoodFilter, SynthesisEngine
from app.infrastructure.ai.common_good_filter import OllamaCommonGoodFilter
from app.infrastructure.ai.conversational_assistant import OllamaConversationalAssistant
from app.infrastructure.ai.ollama_client import OllamaClient
from app.infrastructure.ai.synthesis_engine import OllamaSynthesisEngine
from app.infrastructure.database.repositories import (
    InMemoryChatRepository,
    InMemoryConsensusRepository,
    InMemoryCycleRepository,
    PostgresChatRepository,
    PostgresConsensusRepository,
    PostgresCycleRepository,
)
from app.infrastructure.database.session import make_session_factory


@lru_cache
def get_session_factory():
    return make_session_factory(get_settings())


@lru_cache
def _memory_chat_repository() -> InMemoryChatRepository:
    return InMemoryChatRepository()


@lru_cache
def _postgres_chat_repository() -> PostgresChatRepository:
    return PostgresChatRepository(get_session_factory())


def get_chat_repository():
    if get_settings().repository_backend == "postgres":
        return _postgres_chat_repository()
    return _memory_chat_repository()


@lru_cache
def _memory_consensus_repository() -> InMemoryConsensusRepository:
    return InMemoryConsensusRepository()


@lru_cache
def _postgres_consensus_repository() -> PostgresConsensusRepository:
    return PostgresConsensusRepository(get_session_factory())


def get_consensus_repository():
    if get_settings().repository_backend == "postgres":
        return _postgres_consensus_repository()
    return _memory_consensus_repository()


@lru_cache
def _memory_cycle_repository() -> InMemoryCycleRepository:
    return InMemoryCycleRepository()


@lru_cache
def _postgres_cycle_repository() -> PostgresCycleRepository:
    return PostgresCycleRepository(get_session_factory())


def get_cycle_repository():
    if get_settings().repository_backend == "postgres":
        return _postgres_cycle_repository()
    return _memory_cycle_repository()


@lru_cache
def get_ollama_client() -> OllamaClient:
    return OllamaClient(get_settings())


@lru_cache
def get_conversational_assistant() -> ConversationalAssistant:
    return OllamaConversationalAssistant(get_ollama_client())


@lru_cache
def get_synthesis_engine() -> SynthesisEngine:
    return OllamaSynthesisEngine(get_ollama_client())


@lru_cache
def get_common_good_filter() -> CommonGoodFilter:
    return OllamaCommonGoodFilter(get_ollama_client())
