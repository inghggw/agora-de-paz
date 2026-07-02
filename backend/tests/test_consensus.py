from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.dependencies import get_common_good_filter, get_synthesis_engine
from app.domain.consensus.interfaces import CommonGoodFilter, SynthesisEngine
from app.main import app


class FakeSynthesisEngine(SynthesisEngine):
    def synthesize(self, topic: str, texts: list[str]) -> str:
        return f"Consenso emergente: prueba sobre {topic}"


class AlwaysAlignedFilter(CommonGoodFilter):
    def is_aligned(self, summary: str) -> bool:
        return True


class NeverAlignedFilter(CommonGoodFilter):
    def is_aligned(self, summary: str) -> bool:
        return False


client = TestClient(app)


def test_synthesize_consensus_approved_by_filter():
    app.dependency_overrides[get_synthesis_engine] = lambda: FakeSynthesisEngine()
    app.dependency_overrides[get_common_good_filter] = lambda: AlwaysAlignedFilter()
    try:
        response = client.post(
            "/api/v1/consensus/synthesize",
            json={"cycle_id": str(uuid4()), "topic": "educacion", "texts": ["a", "b"]},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "proposed"
        assert "educacion" in body["summary"]
    finally:
        app.dependency_overrides.pop(get_synthesis_engine, None)
        app.dependency_overrides.pop(get_common_good_filter, None)


def test_synthesize_consensus_rejected_by_filter():
    app.dependency_overrides[get_synthesis_engine] = lambda: FakeSynthesisEngine()
    app.dependency_overrides[get_common_good_filter] = lambda: NeverAlignedFilter()
    try:
        response = client.post(
            "/api/v1/consensus/synthesize",
            json={"cycle_id": str(uuid4()), "topic": "vivienda", "texts": ["a"]},
        )
        assert response.status_code == 201
        assert response.json()["status"] == "not_aligned"
    finally:
        app.dependency_overrides.pop(get_synthesis_engine, None)
        app.dependency_overrides.pop(get_common_good_filter, None)


def test_get_unknown_consensus_returns_404():
    response = client.get(f"/api/v1/consensus/{uuid4()}")
    assert response.status_code == 404
