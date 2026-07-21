from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from services.bootstrap_service import BootstrapService


def test_health_reports_healthy_when_database_reachable(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["dependencies"]["database"] == "healthy"


def test_ready_reports_not_ready_before_bootstrap(client: TestClient) -> None:
    """
    Readiness must be false-by-default: an AuthService instance whose
    database is reachable but has never run bootstrap cannot yet serve a
    Platform Administrator login, so /ready must fail closed (503), not
    report healthy just because the DB connection works.
    """
    response = client.get("/ready")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["reason"] == "bootstrap_not_applied"


async def test_ready_reports_ready_after_bootstrap(
    client: TestClient, db_session: AsyncSession
) -> None:
    await BootstrapService(db_session).run()

    response = client.get("/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["bootstrap"] == "complete"
    assert "ff_identity_auth_v1" in body["feature_flags"]


def test_health_and_ready_responses_carry_correlation_id_header(client: TestClient) -> None:
    """
    Observability requirement (roadmap Operational Observability
    framework): every response — including health/readiness probes used
    by orchestrators, not just business requests — must be traceable.
    """
    response = client.get("/health")
    assert "X-Correlation-ID" in response.headers
