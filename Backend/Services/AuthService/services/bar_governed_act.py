"""
Enterprise BAR — TD-171 remediation tranche (WP-23 Charter §21a), R-01:
machine-verifiable governing-act parsing and validation.

Implements the approved governed-act convention
(`TDS-WP23-TD-171-R3-Remediation-Design-and-Readiness.md` §17.1.3; OD-1
two-part act, OD-3 structured `| Field | Value |` metadata), authorized
for repository implementation before R3 acceptance by the Repository
Owner's implementation authorization. It does NOT satisfy R3.

Scope boundary:
  * Pure validation. No database access, no BAR write, no act registry:
    the governing act is a repository governance record (ADR/ROD-style
    Markdown), and this module only reads its text.
  * The authorization component is validated before any identifier
    exists. The execution addendum records the identifier issued at BAR
    registration (D5 unchanged). A registration is governed only when
    both parts are present and linked (`GovernedAct.require_complete()`).
  * BAR identifier semantics are reused, not redefined:
    `BAR_IDENTIFIER_PREFIX` and the `bar_registration` column lengths
    come from the existing models.

Parsing rule for the convention's "table titled …" wording: a title line
whose text (ignoring leading `#` heading markers and surrounding `**`)
equals the table title exactly, followed (after optional blank lines) by
a `| Field | Value |` table. Cells are trimmed, and one pair of
surrounding backticks is removed from field names and values.

Every validation failure raises a `GovernedActError` subclass carrying a
`GovernedActErrorCode`, so callers can distinguish missing, malformed,
identity-mismatched and addendum-mismatched acts deterministically.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path

from models.bar_identifier_ledger import BAR_IDENTIFIER_PREFIX
from models.bar_registration import BarRegistration

AUTHORIZATION_TITLE = "BAR Registration Authorization"
EXECUTION_TITLE = "BAR Registration Execution"

AUTHORIZATION_ACT_TYPE = "BAR-REGISTRATION-AUTHORIZATION"
EXECUTION_ACT_TYPE = "BAR-REGISTRATION-EXECUTION"
REGISTRATION_INTENT = "REGISTER"
GOVERNANCE_AUTHORITY = "Repository Owner"

AUTHORIZATION_FIELDS = (
    "governing_act_id",
    "act_type",
    "business_activity_reference",
    "owning_capability",
    "owning_work_package",
    "retroactive",
    "registration_intent",
    "authorization_reference",
    "governance_authority",
)
EXECUTION_FIELDS = (
    "act_type",
    "addendum_of",
    "bar_business_activity_identifier",
    "business_activity_reference",
    "owning_capability",
    "owning_work_package",
    "registration_intent",
    "execution_reference",
    "executed_on",
)
# Execution-addendum fields that must equal the authorization component.
_ECHOED_FIELDS = (
    "business_activity_reference",
    "owning_capability",
    "owning_work_package",
    "registration_intent",
)

_BAR_IDENTIFIER_RE = re.compile(rf"^{re.escape(BAR_IDENTIFIER_PREFIX)}-\d{{6}}$")
_GOVERNING_ACT_ID_RE = re.compile(r"^[A-Z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)+$")
_CAPABILITY_RE = re.compile(r"^C-\d{3}$")
_WORK_PACKAGE_RE = re.compile(r"^WP-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")

# Values that are persisted into `bar_registration` must fit its columns.
_COLUMN_LIMITS = {
    "business_activity_reference": BarRegistration.__table__.c.business_activity_reference.type.length,
    "owning_capability": BarRegistration.__table__.c.owning_capability.type.length,
    "owning_work_package": BarRegistration.__table__.c.owning_work_package.type.length,
    "governing_act_id": BarRegistration.__table__.c.registering_act.type.length,
}


class GovernedActErrorCode(str, Enum):
    MISSING_ACT = "MISSING_ACT"
    MISSING_SECTION = "MISSING_SECTION"
    MALFORMED_TABLE = "MALFORMED_TABLE"
    DUPLICATE_SECTION = "DUPLICATE_SECTION"
    DUPLICATE_FIELD = "DUPLICATE_FIELD"
    UNKNOWN_FIELD = "UNKNOWN_FIELD"
    MISSING_FIELD = "MISSING_FIELD"
    INVALID_LITERAL = "INVALID_LITERAL"
    INVALID_FORMAT = "INVALID_FORMAT"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    ADDENDUM_MISMATCH = "ADDENDUM_MISMATCH"


class GovernedActError(ValueError):
    """Base class for every governed-act validation failure."""

    def __init__(self, code: GovernedActErrorCode, message: str) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code


class GovernedActMissing(GovernedActError):
    """The act, or a required component of it, does not exist."""


class GovernedActMalformed(GovernedActError):
    """The act exists but its metadata is structurally or semantically invalid."""


class GovernedActIdentityMismatch(GovernedActError):
    """`governing_act_id` does not identify the record it is written in."""


class GovernedActAddendumMismatch(GovernedActError):
    """The execution addendum is not linked to, or disagrees with, its authorization."""


@dataclass(frozen=True)
class GovernedActAuthorization:
    governing_act_id: str
    business_activity_reference: str
    owning_capability: str
    owning_work_package: str
    retroactive: bool
    registration_intent: str
    authorization_reference: str
    governance_authority: str


@dataclass(frozen=True)
class GovernedActExecution:
    addendum_of: str
    bar_business_activity_identifier: str
    business_activity_reference: str
    owning_capability: str
    owning_work_package: str
    registration_intent: str
    execution_reference: str
    executed_on: date


@dataclass(frozen=True)
class GovernedAct:
    source_name: str
    authorization: GovernedActAuthorization
    execution: GovernedActExecution | None

    @property
    def is_complete(self) -> bool:
        """True only when both parts exist and are linked (OD-1)."""
        return self.execution is not None

    def require_complete(self) -> GovernedActExecution:
        if self.execution is None:
            raise GovernedActMissing(
                GovernedActErrorCode.MISSING_SECTION,
                f"'{self.source_name}' has no '{EXECUTION_TITLE}' addendum; the "
                "registration is not governed until the execution addendum exists.",
            )
        return self.execution


def load_governed_act(path: Path | str) -> GovernedAct:
    """Read and validate the governing act stored at `path`."""
    act_path = Path(path)
    if not act_path.is_file():
        raise GovernedActMissing(
            GovernedActErrorCode.MISSING_ACT, f"governing act '{act_path}' does not exist."
        )
    return parse_governed_act(act_path.read_text(encoding="utf-8"), source_name=act_path.name)


def parse_governed_act(text: str, *, source_name: str) -> GovernedAct:
    """Parse and validate a governing act's metadata. Raises `GovernedActError`."""
    if not text or not text.strip():
        raise GovernedActMissing(
            GovernedActErrorCode.MISSING_ACT, f"governing act '{source_name}' is empty."
        )
    lines = text.splitlines()
    authorization_rows = _single_table(lines, AUTHORIZATION_TITLE, source_name)
    execution_rows = _single_table(lines, EXECUTION_TITLE, source_name)
    if authorization_rows is None:
        raise GovernedActMissing(
            GovernedActErrorCode.MISSING_SECTION,
            f"'{source_name}' has no '{AUTHORIZATION_TITLE}' table.",
        )

    authorization = _build_authorization(authorization_rows, source_name)
    execution = (
        _build_execution(execution_rows, authorization, source_name)
        if execution_rows is not None
        else None
    )
    return GovernedAct(source_name=source_name, authorization=authorization, execution=execution)


def declares_governed_act(text: str) -> bool:
    """Whether `text` carries an authorization or execution title, i.e. is a governed act to validate."""
    return any(_title_text(line) in (AUTHORIZATION_TITLE, EXECUTION_TITLE) for line in text.splitlines())


def table_cells(line: str) -> list[str]:
    """One Markdown table row's cells, trimmed and unquoted exactly as act metadata cells are."""
    return [_unquote(cell) for cell in _cells(line)]


def _single_table(lines: list[str], title: str, source_name: str) -> dict[str, str] | None:
    title_indexes = [i for i, line in enumerate(lines) if _title_text(line) == title]
    if not title_indexes:
        return None
    if len(title_indexes) > 1:
        raise GovernedActMalformed(
            GovernedActErrorCode.DUPLICATE_SECTION,
            f"'{source_name}' contains more than one '{title}' table.",
        )
    return _read_table(lines, title_indexes[0] + 1, title, source_name)


def _title_text(line: str) -> str:
    text = line.strip().lstrip("#").strip()
    if text.startswith("**") and text.endswith("**") and len(text) > 4:
        text = text[2:-2].strip()
    return text


def _read_table(lines: list[str], start: int, title: str, source_name: str) -> dict[str, str]:
    index = start
    while index < len(lines) and not lines[index].strip():
        index += 1
    table: list[list[str]] = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        table.append(_cells(lines[index]))
        index += 1

    def malformed(detail: str) -> GovernedActMalformed:
        return GovernedActMalformed(
            GovernedActErrorCode.MALFORMED_TABLE, f"'{source_name}' table '{title}': {detail}"
        )

    if len(table) < 2:
        raise malformed("expected a '| Field | Value |' header and separator row.")
    if table[0] != ["Field", "Value"]:
        raise malformed(f"header must be '| Field | Value |', found {table[0]}.")
    if len(table[1]) != 2 or not all(_SEPARATOR_CELL_RE.match(cell) for cell in table[1]):
        raise malformed("second row must be the '|---|---|' separator.")

    rows: dict[str, str] = {}
    for cells in table[2:]:
        if len(cells) != 2:
            raise malformed(f"every row must have exactly two cells, found {cells}.")
        field, value = (_unquote(cell) for cell in cells)
        if field in rows:
            raise GovernedActMalformed(
                GovernedActErrorCode.DUPLICATE_FIELD,
                f"'{source_name}' table '{title}' repeats field '{field}'.",
            )
        rows[field] = value
    return rows


def _cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _unquote(cell: str) -> str:
    if len(cell) >= 2 and cell.startswith("`") and cell.endswith("`"):
        return cell[1:-1].strip()
    return cell


def _check_fields(rows: dict[str, str], expected: tuple[str, ...], title: str, source_name: str) -> None:
    for field in rows:
        if field not in expected:
            raise GovernedActMalformed(
                GovernedActErrorCode.UNKNOWN_FIELD,
                f"'{source_name}' table '{title}' has unknown field '{field}'.",
            )
    for field in expected:
        if not rows.get(field):
            raise GovernedActMalformed(
                GovernedActErrorCode.MISSING_FIELD,
                f"'{source_name}' table '{title}' is missing required field '{field}'.",
            )


def _require_literal(rows: dict[str, str], field: str, expected: str, title: str, source_name: str) -> None:
    if rows[field] != expected:
        raise GovernedActMalformed(
            GovernedActErrorCode.INVALID_LITERAL,
            f"'{source_name}' table '{title}': '{field}' must be '{expected}', found '{rows[field]}'.",
        )


def _require_format(rows: dict[str, str], field: str, pattern: re.Pattern[str], title: str, source_name: str) -> None:
    if not pattern.match(rows[field]):
        raise GovernedActMalformed(
            GovernedActErrorCode.INVALID_FORMAT,
            f"'{source_name}' table '{title}': '{field}' has invalid format '{rows[field]}'.",
        )


def _require_length(rows: dict[str, str], title: str, source_name: str) -> None:
    for field, limit in _COLUMN_LIMITS.items():
        if field in rows and limit is not None and len(rows[field]) > limit:
            raise GovernedActMalformed(
                GovernedActErrorCode.INVALID_FORMAT,
                f"'{source_name}' table '{title}': '{field}' exceeds {limit} characters.",
            )


def _build_authorization(rows: dict[str, str], source_name: str) -> GovernedActAuthorization:
    title = AUTHORIZATION_TITLE
    _check_fields(rows, AUTHORIZATION_FIELDS, title, source_name)
    _require_literal(rows, "act_type", AUTHORIZATION_ACT_TYPE, title, source_name)
    _require_literal(rows, "registration_intent", REGISTRATION_INTENT, title, source_name)
    _require_literal(rows, "governance_authority", GOVERNANCE_AUTHORITY, title, source_name)
    _require_format(rows, "governing_act_id", _GOVERNING_ACT_ID_RE, title, source_name)
    _require_format(rows, "owning_capability", _CAPABILITY_RE, title, source_name)
    _require_format(rows, "owning_work_package", _WORK_PACKAGE_RE, title, source_name)
    if rows["retroactive"] not in ("true", "false"):
        raise GovernedActMalformed(
            GovernedActErrorCode.INVALID_FORMAT,
            f"'{source_name}' table '{title}': 'retroactive' must be 'true' or 'false', "
            f"found '{rows['retroactive']}'.",
        )
    _require_length(rows, title, source_name)
    _require_file_identity(rows["governing_act_id"], source_name)
    return GovernedActAuthorization(
        governing_act_id=rows["governing_act_id"],
        business_activity_reference=rows["business_activity_reference"],
        owning_capability=rows["owning_capability"],
        owning_work_package=rows["owning_work_package"],
        retroactive=rows["retroactive"] == "true",
        registration_intent=rows["registration_intent"],
        authorization_reference=rows["authorization_reference"],
        governance_authority=rows["governance_authority"],
    )


def _require_file_identity(governing_act_id: str, source_name: str) -> None:
    stem = Path(source_name).name
    if stem.endswith(".md"):
        stem = stem[:-3]
    if stem == governing_act_id or stem.startswith((f"{governing_act_id}_", f"{governing_act_id}-")):
        return
    raise GovernedActIdentityMismatch(
        GovernedActErrorCode.IDENTITY_MISMATCH,
        f"governing_act_id '{governing_act_id}' does not identify record '{source_name}'.",
    )


def _build_execution(
    rows: dict[str, str], authorization: GovernedActAuthorization, source_name: str
) -> GovernedActExecution:
    title = EXECUTION_TITLE
    _check_fields(rows, EXECUTION_FIELDS, title, source_name)
    _require_literal(rows, "act_type", EXECUTION_ACT_TYPE, title, source_name)
    _require_format(rows, "bar_business_activity_identifier", _BAR_IDENTIFIER_RE, title, source_name)
    if not _ISO_DATE_RE.match(rows["executed_on"]):
        raise GovernedActMalformed(
            GovernedActErrorCode.INVALID_FORMAT,
            f"'{source_name}' table '{title}': 'executed_on' must be YYYY-MM-DD, "
            f"found '{rows['executed_on']}'.",
        )
    try:
        executed_on = date.fromisoformat(rows["executed_on"])
    except ValueError as exc:
        raise GovernedActMalformed(
            GovernedActErrorCode.INVALID_FORMAT,
            f"'{source_name}' table '{title}': 'executed_on' is not a valid date "
            f"'{rows['executed_on']}'.",
        ) from exc

    if rows["addendum_of"] != authorization.governing_act_id:
        raise GovernedActAddendumMismatch(
            GovernedActErrorCode.ADDENDUM_MISMATCH,
            f"'{source_name}': addendum_of '{rows['addendum_of']}' does not equal "
            f"governing_act_id '{authorization.governing_act_id}'.",
        )
    for field in _ECHOED_FIELDS:
        if rows[field] != getattr(authorization, field):
            raise GovernedActAddendumMismatch(
                GovernedActErrorCode.ADDENDUM_MISMATCH,
                f"'{source_name}': execution addendum '{field}' '{rows[field]}' does not "
                f"equal the authorization's '{getattr(authorization, field)}'.",
            )
    return GovernedActExecution(
        addendum_of=rows["addendum_of"],
        bar_business_activity_identifier=rows["bar_business_activity_identifier"],
        business_activity_reference=rows["business_activity_reference"],
        owning_capability=rows["owning_capability"],
        owning_work_package=rows["owning_work_package"],
        registration_intent=rows["registration_intent"],
        execution_reference=rows["execution_reference"],
        executed_on=executed_on,
    )
