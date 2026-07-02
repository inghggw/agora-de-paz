from functools import lru_cache

from app.infrastructure.ai.common_good_filter import PermissiveCommonGoodFilter
from app.infrastructure.ai.synthesis_engine import NaiveSynthesisEngine
from app.infrastructure.database.repositories import (
    InMemoryChatRepository,
    InMemoryConsensusRepository,
    InMemoryCycleRepository,
)


@lru_cache
def get_chat_repository() -> InMemoryChatRepository:
    return InMemoryChatRepository()


@lru_cache
def get_consensus_repository() -> InMemoryConsensusRepository:
    return InMemoryConsensusRepository()


@lru_cache
def get_cycle_repository() -> InMemoryCycleRepository:
    return InMemoryCycleRepository()


@lru_cache
def get_synthesis_engine() -> NaiveSynthesisEngine:
    return NaiveSynthesisEngine()


@lru_cache
def get_common_good_filter() -> PermissiveCommonGoodFilter:
    return PermissiveCommonGoodFilter()
