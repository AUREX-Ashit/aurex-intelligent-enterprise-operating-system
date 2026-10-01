"""
Shared fixtures for the TD-171 repository-evidence and reconciliation tests.

A test repository is a temporary directory holding the REAL
`architecture/00-Governance/BAR-INDEX.md` text from this checkout, with
only its §3 placeholder row replaced by the rows a test needs, plus
fictitious governed acts (ADR-92xx, C-999, WP-TEST-GOV). Execution
addenda are produced by the real `render_execution_addendum`. Nothing
here is a real registration.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path

from services.bar_governance_evidence import BAR_INDEX_RELATIVE_PATH, DEFAULT_REPOSITORY_ROOT
from services.bar_governed_act import parse_governed_act
from services.bar_governed_registration import render_execution_addendum
from services.bar_reconciliation import RegistrationSnapshot

REAL_INDEX_TEXT = (DEFAULT_REPOSITORY_ROOT / BAR_INDEX_RELATIVE_PATH).read_text(encoding="utf-8")
EMPTY_REGISTER_ROW = "| *(no entries)* | | | | | | | |"
ACT_DIR = Path("architecture/07-Decisions")
EXECUTED_ON = date(2026, 10, 1)


def authorization_text(act_id: str, reference: str, *, retroactive: bool = False, **overrides: str) -> str:
    rows = {
        "governing_act_id": act_id,
        "act_type": "BAR-REGISTRATION-AUTHORIZATION",
        "business_activity_reference": reference,
        "owning_capability": "C-999",
        "owning_work_package": "WP-TEST-GOV",
        "retroactive": "true" if retroactive else "false",
        "registration_intent": "REGISTER",
        "authorization_reference": "ROD-TEST-9200",
        "governance_authority": "Repository Owner",
    }
    rows.update(overrides)
    body = "\n".join(f"| `{k}` | {v} |" for k, v in rows.items())
    return f"# {act_id} — test registering act\n\n**BAR Registration Authorization**\n\n| Field | Value |\n|---|---|\n{body}\n"


def addendum_text(authorization: str, act_id: str, identifier: str, *, executed_on: date = EXECUTED_ON) -> str:
    parsed = parse_governed_act(authorization, source_name=f"{act_id}_Test.md").authorization
    return render_execution_addendum(
        parsed, bar_business_activity_identifier=identifier, execution_reference="test-execution-ref", executed_on=executed_on
    )


def index_row(
    identifier: str,
    reference: str,
    act_id: str,
    *,
    capability: str = "C-999",
    work_package: str = "WP-TEST-GOV",
    status: str = "Registered",
    registered_on: str = EXECUTED_ON.isoformat(),
    retroactive: str = "No",
) -> str:
    return f"| `{identifier}` | {reference} | {capability} | {work_package} | {status} | {act_id} | {registered_on} | {retroactive} |"


@dataclass
class GovernanceRepository:
    root: Path

    def write_index(self, *rows: str) -> None:
        assert REAL_INDEX_TEXT.count(EMPTY_REGISTER_ROW) == 1, "BAR-INDEX.md §3 placeholder row changed"
        replacement = "\n".join(rows) if rows else EMPTY_REGISTER_ROW
        self.write(BAR_INDEX_RELATIVE_PATH, REAL_INDEX_TEXT.replace(EMPTY_REGISTER_ROW, replacement))

    def write_act(self, act_id: str, text: str, *, name: str | None = None) -> Path:
        return self.write(ACT_DIR / (name or f"{act_id}_Test_Registering_Act.md"), text)

    def governed(self, act_id: str, reference: str, identifier: str, *, retroactive: bool = False, index: bool = True) -> str:
        """A complete two-part act; returns the matching index row (written only by the caller)."""
        authorization = authorization_text(act_id, reference, retroactive=retroactive)
        self.write_act(act_id, authorization + "\n" + addendum_text(authorization, act_id, identifier))
        return index_row(identifier, reference, act_id, retroactive="Yes" if retroactive else "No")

    def write(self, relative: Path, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


def snapshot(
    identifier: str,
    reference: str,
    act_id: str,
    *,
    capability: str = "C-999",
    work_package: str = "WP-TEST-GOV",
    retroactive: bool = False,
    registered_at: datetime = datetime(2026, 10, 1, 9, 30, tzinfo=timezone.utc),
    status: str = "REGISTERED",
) -> RegistrationSnapshot:
    return RegistrationSnapshot(
        identifier=identifier,
        business_activity_reference=reference,
        owning_capability=capability,
        owning_work_package=work_package,
        registration_status=status,
        registering_act=act_id,
        registered_at=registered_at,
        is_retroactive=retroactive,
    )
