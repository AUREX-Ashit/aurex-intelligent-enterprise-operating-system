"""
TD-171 remediation tranche (WP-23 Charter §21a), slice 2: the governed BAR
registration operation (`services/bar_governed_registration.py`).

Runs against a dedicated SQLite file standing in for the *repository-side*
deployment write connection. This exercises the operation's control
logic and its use of the unchanged `BarRegistrationService.register()`.
It is NOT PostgreSQL evidence and NOT evidence of database-role
separation (EP-02, EP-04 remain external prerequisites).

Harness note: the operation creates its own engine from the capability URL,
so the transactional SQLite recipe of `test_bar_transaction_safety.py`
(driver autocommit off, explicit BEGIN, `PRAGMA foreign_keys=ON`) is applied
to every engine created during a test through class-level listeners that are
removed afterwards. Without it pysqlite does not nest the services'
SAVEPOINTs in a real transaction and rollback cannot be observed.

Fixture acts use fictitious identifiers (ADR-91xx, C-999, WP-TEST-GOV) so
no test resembles a real registering act.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import models  # noqa: F401  (registers every table on Base.metadata)
from models.bar_identifier_ledger import BarIdentifierLedger
from models.bar_registration import BarRegistration
from models.database import Base
from repositories.bar_identifier_repository import BarIdentifierRepository
from services.bar_governed_act import (
    GovernedActAddendumMismatch,
    GovernedActErrorCode,
    GovernedActMalformed,
    GovernedActMissing,
    load_governed_act,
)
from services.bar_governed_registration import (
    DEPLOYMENT_WRITE_URL_ENV,
    DeploymentWriteCapability,
    DeploymentWriteCapabilityInvalid,
    DeploymentWriteCapabilityUnavailable,
    GovernedActAlreadyExecuted,
    GovernedBarRegistrationOperation,
    GovernedRegistrationErrorCode,
    GovernedRegistrationEvidenceMismatch,
    GovernedRegistrationMissing,
    GovernedRegistrationRequest,
    GovernedRegistrationRequestMismatch,
)
from services.bar_registration_service import BarRegistrationAlreadyExists, BarRegistrationService

RUNTIME_URL = "postgresql+asyncpg://runtime-user@runtime-host:5432/authservice"


def _authorization_table(act_id: str, reference: str, **overrides: str) -> str:
    rows = {
        "governing_act_id": act_id,
        "act_type": "BAR-REGISTRATION-AUTHORIZATION",
        "business_activity_reference": reference,
        "owning_capability": "C-999",
        "owning_work_package": "WP-TEST-GOV",
        "retroactive": "false",
        "registration_intent": "REGISTER",
        "authorization_reference": "ROD-TEST-9100",
        "governance_authority": "Repository Owner",
    }
    rows.update(overrides)
    body = "\n".join(f"| `{k}` | {v} |" for k, v in rows.items())
    return (
        f"# {act_id} — test registering act\n\nTest-only decision text.\n\n"
        f"**BAR Registration Authorization**\n\n| Field | Value |\n|---|---|\n{body}\n"
    )


def _request(reference: str = "BA-01 (GOV TEST)", **overrides) -> GovernedRegistrationRequest:
    values = {
        "business_activity_reference": reference,
        "owning_capability": "C-999",
        "owning_work_package": "WP-TEST-GOV",
        "is_retroactive": False,
        "registration_intent": "REGISTER",
    }
    values.update(overrides)
    return GovernedRegistrationRequest(**values)


@pytest.fixture
def transactional_sqlite():
    def on_connect(dbapi_connection, _record):
        dbapi_connection.isolation_level = None  # SQLAlchemy emits BEGIN itself
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def on_begin(conn):
        conn.exec_driver_sql("BEGIN")

    event.listen(Engine, "connect", on_connect)
    event.listen(Engine, "begin", on_begin)
    yield
    event.remove(Engine, "connect", on_connect)
    event.remove(Engine, "begin", on_begin)


@pytest.fixture
async def write_db(tmp_path: Path, transactional_sqlite):
    url = f"sqlite+aiosqlite:///{(tmp_path / 'bar_governed_write.db').as_posix()}"
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    sessions = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield url, sessions
    await engine.dispose()


@pytest.fixture
def operation(write_db):
    url, _ = write_db
    return GovernedBarRegistrationOperation(DeploymentWriteCapability.validate(url, runtime_database_url=RUNTIME_URL))


@pytest.fixture
def act_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "acts"
    directory.mkdir()
    return directory


def _write_act(act_dir: Path, act_id: str, reference: str = "BA-01 (GOV TEST)", **overrides: str) -> Path:
    path = act_dir / f"{act_id}_Test_Registering_Act.md"
    path.write_text(_authorization_table(act_id, reference, **overrides), encoding="utf-8")
    return path


def _append(path: Path, text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + "\n" + text, encoding="utf-8")


async def _rows(sessions) -> list[BarRegistration]:
    async with sessions() as s:
        return list((await s.execute(select(BarRegistration).order_by(BarRegistration.identifier))).scalars())


async def _ledger_count(sessions) -> int:
    async with sessions() as s:
        return (await s.execute(select(func.count()).select_from(BarIdentifierLedger))).scalar_one()


# ----------------------------------------------------- A, P: success path


async def test_execute_then_confirm_is_a_governed_registration(operation, write_db, act_dir):
    _, sessions = write_db
    act_path = _write_act(act_dir, "ADR-9101")

    executed = await operation.execute(act_path, _request(), actor_id="deploy-operator")
    assert executed.governing_act_id == "ADR-9101"
    assert executed.bar_business_activity_identifier == "BA-000001"

    rows = await _rows(sessions)  # P: committed, visible from an independent session
    assert [r.identifier for r in rows] == ["BA-000001"]
    assert rows[0].registering_act == "ADR-9101"
    assert rows[0].business_activity_reference == "BA-01 (GOV TEST)"
    assert rows[0].owning_capability == "C-999"
    assert rows[0].owning_work_package == "WP-TEST-GOV"
    assert rows[0].is_retroactive is False

    _append(act_path, executed.execution_addendum)
    confirmed = await operation.confirm(act_path, actor_id="deploy-operator")
    assert confirmed.bar_business_activity_identifier == "BA-000001"
    assert confirmed.execution_reference == executed.execution_reference


async def test_retroactive_authorization_is_registered_as_retroactive(operation, write_db, act_dir):
    _, sessions = write_db
    act_path = _write_act(act_dir, "ADR-9121", retroactive="true")
    executed = await operation.execute(act_path, _request(is_retroactive=True))
    rows = await _rows(sessions)
    assert [(r.identifier, r.is_retroactive) for r in rows] == [(executed.bar_business_activity_identifier, True)]
    _append(act_path, executed.execution_addendum)
    await operation.confirm(act_path)


async def test_rendered_addendum_round_trips_through_the_slice1_validator(operation, act_dir):
    act_path = _write_act(act_dir, "ADR-9102")
    executed = await operation.execute(act_path, _request())
    _append(act_path, executed.execution_addendum)

    act = load_governed_act(act_path)
    execution = act.require_complete()
    assert execution.addendum_of == "ADR-9102"
    assert execution.bar_business_activity_identifier == executed.bar_business_activity_identifier
    assert execution.execution_reference == executed.execution_reference
    assert execution.executed_on == executed.executed_on


# --------------------------------------------- B, C, D, E: act failures


async def test_confirm_rejects_authorization_only_act(operation, act_dir):
    act_path = _write_act(act_dir, "ADR-9103")
    await operation.execute(act_path, _request())
    with pytest.raises(GovernedActMissing) as info:
        await operation.confirm(act_path)
    assert info.value.code is GovernedActErrorCode.MISSING_SECTION


@pytest.mark.parametrize("phase", ["execute", "confirm"])
async def test_missing_act_is_rejected(operation, write_db, act_dir, phase):
    _, sessions = write_db
    missing = act_dir / "ADR-9104_absent.md"
    with pytest.raises(GovernedActMissing) as info:
        if phase == "execute":
            await operation.execute(missing, _request())
        else:
            await operation.confirm(missing)
    assert info.value.code is GovernedActErrorCode.MISSING_ACT
    assert await _rows(sessions) == []


async def test_malformed_act_is_rejected_before_any_write(operation, write_db, act_dir):
    _, sessions = write_db
    act_path = _write_act(act_dir, "ADR-9105", governance_authority="Platform Engineering")
    with pytest.raises(GovernedActMalformed) as info:
        await operation.execute(act_path, _request())
    assert info.value.code is GovernedActErrorCode.INVALID_LITERAL
    assert await _rows(sessions) == []
    assert await _ledger_count(sessions) == 0


async def test_authorization_execution_mismatch_is_rejected(operation, act_dir):
    act_path = _write_act(act_dir, "ADR-9106")
    executed = await operation.execute(act_path, _request())
    _append(act_path, executed.execution_addendum.replace("| C-999 |", "| C-998 |"))
    with pytest.raises(GovernedActAddendumMismatch):
        await operation.confirm(act_path)


async def test_executing_an_already_executed_act_is_refused(operation, write_db, act_dir):
    _, sessions = write_db
    act_path = _write_act(act_dir, "ADR-9107")
    executed = await operation.execute(act_path, _request())
    _append(act_path, executed.execution_addendum)
    with pytest.raises(GovernedActAlreadyExecuted) as info:
        await operation.execute(act_path, _request())
    assert info.value.code is GovernedRegistrationErrorCode.ALREADY_EXECUTED
    assert len(await _rows(sessions)) == 1


# --------------------------------------------- F: identifier/evidence mismatch


async def test_addendum_identifier_without_registration_is_rejected(operation, act_dir):
    act_path = _write_act(act_dir, "ADR-9108")
    executed = await operation.execute(act_path, _request())
    _append(act_path, executed.execution_addendum.replace("BA-000001", "BA-000099"))
    with pytest.raises(GovernedRegistrationMissing) as info:
        await operation.confirm(act_path)
    assert info.value.code is GovernedRegistrationErrorCode.REGISTRATION_MISSING


async def test_addendum_pointing_at_another_acts_registration_is_rejected(operation, act_dir):
    first = _write_act(act_dir, "ADR-9109", "BA-01 (GOV TEST)")
    second = _write_act(act_dir, "ADR-9110", "BA-02 (GOV TEST)")
    first_run = await operation.execute(first, _request("BA-01 (GOV TEST)"))
    second_run = await operation.execute(second, _request("BA-02 (GOV TEST)"))
    # The first act's addendum claims the identifier issued to the second act.
    _append(
        first,
        first_run.execution_addendum.replace(
            first_run.bar_business_activity_identifier, second_run.bar_business_activity_identifier
        ),
    )
    with pytest.raises(GovernedRegistrationEvidenceMismatch) as info:
        await operation.confirm(first)
    assert info.value.code is GovernedRegistrationErrorCode.EVIDENCE_MISMATCH
    assert info.value.field == "registering_act"


# ----------------------------------------- G, H, I, J: request mismatches


@pytest.mark.parametrize(
    "field, value",
    [
        ("business_activity_reference", "BA-99 (GOV TEST)"),
        ("owning_capability", "C-998"),
        ("owning_work_package", "WP-TEST-OTHER"),
        ("registration_intent", "DEREGISTER"),
        ("is_retroactive", True),
    ],
)
async def test_request_must_match_the_authorization(operation, write_db, act_dir, field, value):
    _, sessions = write_db
    act_path = _write_act(act_dir, "ADR-9111")
    with pytest.raises(GovernedRegistrationRequestMismatch) as info:
        await operation.execute(act_path, _request(**{field: value}))
    assert info.value.code is GovernedRegistrationErrorCode.REQUEST_MISMATCH
    assert info.value.field == field
    assert await _rows(sessions) == []
    assert await _ledger_count(sessions) == 0


# --------------------------------------- K, L: deployment write capability


@pytest.mark.parametrize("environ", [{}, {DEPLOYMENT_WRITE_URL_ENV: ""}, {DEPLOYMENT_WRITE_URL_ENV: "   "}])
def test_absent_write_capability_fails_closed(environ):
    with pytest.raises(DeploymentWriteCapabilityUnavailable) as info:
        DeploymentWriteCapability.from_environment(environ, runtime_database_url=RUNTIME_URL)
    assert info.value.code is GovernedRegistrationErrorCode.WRITE_CAPABILITY_UNAVAILABLE


@pytest.mark.parametrize("candidate", [None, "sqlite+aiosqlite:///x.db"])
def test_operation_requires_a_validated_capability_object(candidate):
    with pytest.raises(DeploymentWriteCapabilityUnavailable):
        GovernedBarRegistrationOperation(candidate)


def test_unparseable_write_capability_is_invalid():
    with pytest.raises(DeploymentWriteCapabilityInvalid) as info:
        DeploymentWriteCapability.from_environment(
            {DEPLOYMENT_WRITE_URL_ENV: "not a url"}, runtime_database_url=RUNTIME_URL
        )
    assert info.value.code is GovernedRegistrationErrorCode.WRITE_CAPABILITY_INVALID


def test_runtime_connection_is_not_accepted_as_the_write_capability():
    with pytest.raises(DeploymentWriteCapabilityInvalid) as info:
        DeploymentWriteCapability.from_environment({DEPLOYMENT_WRITE_URL_ENV: RUNTIME_URL}, runtime_database_url=RUNTIME_URL)
    assert "separate deployment connection" in str(info.value)


def test_configured_separate_capability_is_accepted():
    capability = DeploymentWriteCapability.from_environment(
        {DEPLOYMENT_WRITE_URL_ENV: "postgresql+asyncpg://deploy-writer@deploy-host:5432/authservice"},
        runtime_database_url=RUNTIME_URL,
    )
    assert capability.database_url.startswith("postgresql+asyncpg://deploy-writer@")


# ---------------------------------------------------- M: duplicates


async def test_second_act_for_the_same_activity_is_rejected_by_the_existing_service(operation, write_db, act_dir):
    _, sessions = write_db
    first = _write_act(act_dir, "ADR-9112")
    second = _write_act(act_dir, "ADR-9113")
    await operation.execute(first, _request())
    with pytest.raises(BarRegistrationAlreadyExists):
        await operation.execute(second, _request())
    rows = await _rows(sessions)
    assert [r.registering_act for r in rows] == ["ADR-9112"]


async def test_re_executing_an_authorization_before_its_addendum_is_rejected(operation, write_db, act_dir):
    _, sessions = write_db
    act_path = _write_act(act_dir, "ADR-9114")
    await operation.execute(act_path, _request())
    with pytest.raises(BarRegistrationAlreadyExists):
        await operation.execute(act_path, _request())
    assert len(await _rows(sessions)) == 1


# --------------------------------- N, O, R: collision, errors, rollback


async def test_identifier_collision_is_retried_by_the_existing_service(operation, write_db, act_dir, monkeypatch):
    _, sessions = write_db
    async with sessions() as s:
        s.add(BarIdentifierLedger(identifier="BA-000001"))
        await s.commit()
    real = BarIdentifierRepository.max_identifier_sequence
    calls = {"n": 0}

    async def stale_once(self):
        calls["n"] += 1
        return 0 if calls["n"] == 1 else await real(self)

    monkeypatch.setattr(BarIdentifierRepository, "max_identifier_sequence", stale_once)
    act_path = _write_act(act_dir, "ADR-9115")
    executed = await operation.execute(act_path, _request())
    assert executed.bar_business_activity_identifier == "BA-000002"
    assert "| BA-000002 |" in executed.execution_addendum
    assert calls["n"] >= 2


async def test_non_collision_error_propagates_unchanged_and_writes_nothing(operation, write_db, act_dir, monkeypatch):
    _, sessions = write_db

    async def failing_register(self, **_kwargs):
        raise RuntimeError("simulated non-collision failure")

    monkeypatch.setattr(BarRegistrationService, "register", failing_register)
    with pytest.raises(RuntimeError, match="simulated non-collision failure"):
        await operation.execute(_write_act(act_dir, "ADR-9116"), _request())
    assert await _rows(sessions) == []


async def test_failure_after_register_rolls_back_and_preserves_prior_registrations(
    operation, write_db, act_dir, monkeypatch
):
    _, sessions = write_db
    first = _write_act(act_dir, "ADR-9117", "BA-01 (GOV TEST)")
    await operation.execute(first, _request("BA-01 (GOV TEST)"))
    before = [(r.identifier, r.registering_act, r.registered_at) for r in await _rows(sessions)]

    real_register = BarRegistrationService.register

    async def register_then_fail(self, **kwargs):
        await real_register(self, **kwargs)
        raise RuntimeError("failure after the registration insert")

    monkeypatch.setattr(BarRegistrationService, "register", register_then_fail)
    with pytest.raises(RuntimeError, match="after the registration insert"):
        await operation.execute(_write_act(act_dir, "ADR-9118", "BA-02 (GOV TEST)"), _request("BA-02 (GOV TEST)"))

    after = [(r.identifier, r.registering_act, r.registered_at) for r in await _rows(sessions)]
    assert after == before  # O: nothing from the failed run persisted; R: prior row unchanged
    assert await _ledger_count(sessions) == 1


# ------------------------------------------------- Q: audit/event evidence


def _records(caplog, logger_name: str) -> list[dict]:
    return [json.loads(r.getMessage()) for r in caplog.records if r.name == logger_name]


async def test_audit_and_event_evidence_link_the_act_and_execution_reference(operation, act_dir, caplog):
    caplog.set_level(logging.INFO, logger="authservice.audit")
    caplog.set_level(logging.INFO, logger="authservice.events")
    act_path = _write_act(act_dir, "ADR-9119")
    executed = await operation.execute(act_path, _request(), actor_id="deploy-operator")

    audits = _records(caplog, "authservice.audit")
    register_audit = [a for a in audits if a["action"] == "BAR_REGISTER_BUSINESS_ACTIVITY" and a["status"] == "SUCCESS"]
    assert len(register_audit) == 1
    assert register_audit[0]["metadata"]["registering_act"] == "ADR-9119"
    assert register_audit[0]["correlation_id"] == executed.execution_reference
    assert register_audit[0]["actor_id"] == "deploy-operator"
    events = _records(caplog, "authservice.events")
    registered = [e for e in events if e["event_type"] == "BAR_BUSINESS_ACTIVITY_REGISTERED"]
    assert len(registered) == 1
    assert registered[0]["correlation_id"] == executed.execution_reference
    assert registered[0]["payload"]["identifier"] == executed.bar_business_activity_identifier

    _append(act_path, executed.execution_addendum)
    await operation.confirm(act_path, actor_id="deploy-operator")
    confirms = [a for a in _records(caplog, "authservice.audit") if a["action"] == "BAR_GOVERNED_REGISTRATION"]
    assert confirms[-1]["status"] == "SUCCESS"
    assert confirms[-1]["metadata"]["phase"] == "confirm"
    assert confirms[-1]["metadata"]["execution_reference"] == executed.execution_reference


async def test_refusals_are_audited_as_denied(operation, act_dir, caplog):
    caplog.set_level(logging.INFO, logger="authservice.audit")
    with pytest.raises(GovernedRegistrationRequestMismatch):
        await operation.execute(_write_act(act_dir, "ADR-9120"), _request(owning_capability="C-998"))
    denied = [a for a in _records(caplog, "authservice.audit") if a["action"] == "BAR_GOVERNED_REGISTRATION"]
    assert denied and denied[-1]["status"] == "DENIED"
    assert denied[-1]["metadata"] == {
        "governing_act_id": "ADR-9120",
        "code": "REQUEST_MISMATCH",
        "field": "owning_capability",
    }


# ------------------------------------------------------- boundaries


def test_operation_does_not_use_the_runtime_session_manager():
    source = (Path(__file__).resolve().parents[1] / "services" / "bar_governed_registration.py").read_text(encoding="utf-8")
    assert "db_manager" not in source
    assert "models.database" not in source
