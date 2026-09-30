"""
TD-171 remediation tranche (WP-23 Charter §21a), R-01: governed-act
parsing and validation (`services/bar_governed_act.py`).

Pure-text tests against the approved §17.1.3 convention (OD-1 two-part
act, OD-3 `| Field | Value |` metadata). No database is touched. Fixture
acts use a deliberately fictitious identifier and reference so no test
resembles a real registering act.
"""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

import pytest

from services.bar_governed_act import (
    AUTHORIZATION_FIELDS,
    EXECUTION_FIELDS,
    GovernedActAddendumMismatch,
    GovernedActError,
    GovernedActErrorCode,
    GovernedActIdentityMismatch,
    GovernedActMalformed,
    GovernedActMissing,
    load_governed_act,
    parse_governed_act,
)

SOURCE = "ADR-9001_Test_Registering_Act.md"

AUTHORIZATION = {
    "governing_act_id": "ADR-9001",
    "act_type": "BAR-REGISTRATION-AUTHORIZATION",
    "business_activity_reference": "BA-01 (TEST ONLY)",
    "owning_capability": "C-999",
    "owning_work_package": "WP-TEST-01",
    "retroactive": "false",
    "registration_intent": "REGISTER",
    "authorization_reference": "ROD-TEST-0001",
    "governance_authority": "Repository Owner",
}
EXECUTION = {
    "act_type": "BAR-REGISTRATION-EXECUTION",
    "addendum_of": "ADR-9001",
    "bar_business_activity_identifier": "BA-000042",
    "business_activity_reference": "BA-01 (TEST ONLY)",
    "owning_capability": "C-999",
    "owning_work_package": "WP-TEST-01",
    "registration_intent": "REGISTER",
    "execution_reference": "correlation-test-0001",
    "executed_on": "2026-09-30",
}


def _table(title: str, rows: dict[str, str] | list[tuple[str, str]], *, title_style: str = "bold") -> str:
    items = rows.items() if isinstance(rows, dict) else rows
    heading = f"**{title}**" if title_style == "bold" else f"### {title}"
    body = "\n".join(f"| `{field}` | {value} |" for field, value in items)
    return f"{heading}\n\n| Field | Value |\n|---|---|\n{body}\n"


def _act(authorization=AUTHORIZATION, execution=None, **kwargs) -> str:
    text = "# ADR-9001 — Test registering act\n\nHuman-readable decision text.\n\n"
    if authorization is not None:
        text += _table("BAR Registration Authorization", authorization, **kwargs) + "\n"
    if execution is not None:
        text += "## Execution Addendum (2026-09-30)\n\n"
        text += _table("BAR Registration Execution", execution, **kwargs)
    return text


def _with(base: dict[str, str], **changes: str) -> dict[str, str]:
    updated = dict(base)
    updated.update(changes)
    return updated


def _without(base: dict[str, str], field: str) -> dict[str, str]:
    return {key: value for key, value in base.items() if key != field}


def _expect(error_type, code: GovernedActErrorCode, text: str, source: str = SOURCE) -> GovernedActError:
    with pytest.raises(error_type) as info:
        parse_governed_act(text, source_name=source)
    assert info.value.code is code
    return info.value


# ---------------------------------------------------------------- valid acts


def test_authorization_only_act_parses_but_is_not_complete():
    act = parse_governed_act(_act(), source_name=SOURCE)
    assert act.authorization.governing_act_id == "ADR-9001"
    assert act.authorization.business_activity_reference == "BA-01 (TEST ONLY)"
    assert act.authorization.owning_capability == "C-999"
    assert act.authorization.owning_work_package == "WP-TEST-01"
    assert act.authorization.retroactive is False
    assert act.execution is None
    assert act.is_complete is False
    with pytest.raises(GovernedActMissing) as info:
        act.require_complete()
    assert info.value.code is GovernedActErrorCode.MISSING_SECTION


def test_two_part_act_parses_and_is_complete():
    act = parse_governed_act(_act(execution=EXECUTION), source_name=SOURCE)
    assert act.is_complete is True
    execution = act.require_complete()
    assert execution.bar_business_activity_identifier == "BA-000042"
    assert execution.addendum_of == act.authorization.governing_act_id
    assert execution.executed_on == date(2026, 9, 30)


def test_retroactive_true_is_parsed_as_boolean():
    act = parse_governed_act(_act(authorization=_with(AUTHORIZATION, retroactive="true")), source_name=SOURCE)
    assert act.authorization.retroactive is True


def test_heading_style_titles_and_unquoted_cells_are_accepted():
    text = _act(execution=EXECUTION, title_style="heading").replace("`", "")
    act = parse_governed_act(text, source_name=SOURCE)
    assert act.is_complete is True


@pytest.mark.parametrize("source", ["ADR-9001.md", "ADR-9001_Anything.md", "ADR-9001-Anything.md", "dir/ADR-9001_X.md"])
def test_file_identity_accepts_matching_record_names(source):
    act = parse_governed_act(_act(), source_name=source)
    assert act.authorization.governing_act_id == "ADR-9001"


def test_load_governed_act_reads_from_disk(tmp_path: Path):
    path = tmp_path / SOURCE
    path.write_text(_act(execution=EXECUTION), encoding="utf-8")
    act = load_governed_act(path)
    assert act.source_name == SOURCE
    assert act.is_complete is True


# ------------------------------------------------------------ missing acts


def test_missing_file_is_missing_act(tmp_path: Path):
    with pytest.raises(GovernedActMissing) as info:
        load_governed_act(tmp_path / "ADR-9001_absent.md")
    assert info.value.code is GovernedActErrorCode.MISSING_ACT


@pytest.mark.parametrize("text", ["", "   \n\n  "])
def test_empty_act_is_missing_act(text):
    _expect(GovernedActMissing, GovernedActErrorCode.MISSING_ACT, text)


def test_act_without_authorization_table_is_missing_section():
    _expect(GovernedActMissing, GovernedActErrorCode.MISSING_SECTION, "# ADR-9001\n\nFree text only.\n")


def test_execution_addendum_without_authorization_is_missing_section():
    _expect(GovernedActMissing, GovernedActErrorCode.MISSING_SECTION, _act(authorization=None, execution=EXECUTION))


# --------------------------------------------------------- malformed tables


def test_title_without_table_is_malformed():
    _expect(GovernedActMalformed, GovernedActErrorCode.MALFORMED_TABLE, "**BAR Registration Authorization**\n\nNo table.\n")


def test_wrong_header_is_malformed():
    text = _act().replace("| Field | Value |", "| Name | Setting |")
    _expect(GovernedActMalformed, GovernedActErrorCode.MALFORMED_TABLE, text)


def test_missing_separator_is_malformed():
    text = _act().replace("|---|---|\n", "")
    _expect(GovernedActMalformed, GovernedActErrorCode.MALFORMED_TABLE, text)


def test_row_with_three_cells_is_malformed():
    rows = list(AUTHORIZATION.items())
    text = _act(authorization=rows).replace("| `retroactive` | false |", "| `retroactive` | false | extra |")
    _expect(GovernedActMalformed, GovernedActErrorCode.MALFORMED_TABLE, text)


def test_duplicate_authorization_table_is_rejected():
    text = _act() + "\n" + _table("BAR Registration Authorization", AUTHORIZATION)
    _expect(GovernedActMalformed, GovernedActErrorCode.DUPLICATE_SECTION, text)


def test_second_execution_addendum_is_rejected():
    text = _act(execution=EXECUTION) + "\n" + _table("BAR Registration Execution", EXECUTION)
    _expect(GovernedActMalformed, GovernedActErrorCode.DUPLICATE_SECTION, text)


def test_duplicate_field_is_rejected():
    rows = list(AUTHORIZATION.items()) + [("owning_capability", "C-998")]
    _expect(GovernedActMalformed, GovernedActErrorCode.DUPLICATE_FIELD, _act(authorization=rows))


def test_unknown_field_is_rejected():
    _expect(
        GovernedActMalformed,
        GovernedActErrorCode.UNKNOWN_FIELD,
        _act(authorization=_with(AUTHORIZATION, owning_capabilty="C-999")),
    )


@pytest.mark.parametrize("field", AUTHORIZATION_FIELDS)
def test_every_authorization_field_is_required(field):
    _expect(GovernedActMalformed, GovernedActErrorCode.MISSING_FIELD, _act(authorization=_without(AUTHORIZATION, field)))


@pytest.mark.parametrize("field", AUTHORIZATION_FIELDS)
def test_blank_authorization_field_is_missing(field):
    _expect(GovernedActMalformed, GovernedActErrorCode.MISSING_FIELD, _act(authorization=_with(AUTHORIZATION, **{field: ""})))


@pytest.mark.parametrize("field", EXECUTION_FIELDS)
def test_every_execution_field_is_required(field):
    _expect(
        GovernedActMalformed,
        GovernedActErrorCode.MISSING_FIELD,
        _act(execution=_without(EXECUTION, field)),
    )


# ---------------------------------------------------------- literals/format


@pytest.mark.parametrize(
    "field, value",
    [
        ("act_type", "BAR-REGISTRATION-EXECUTION"),
        ("act_type", "bar-registration-authorization"),
        ("registration_intent", "DEREGISTER"),
        ("governance_authority", "Platform Engineering"),
    ],
)
def test_authorization_literals_are_enforced(field, value):
    _expect(GovernedActMalformed, GovernedActErrorCode.INVALID_LITERAL, _act(authorization=_with(AUTHORIZATION, **{field: value})))


def test_execution_act_type_literal_is_enforced():
    _expect(
        GovernedActMalformed,
        GovernedActErrorCode.INVALID_LITERAL,
        _act(execution=_with(EXECUTION, act_type="BAR-REGISTRATION-AUTHORIZATION")),
    )


@pytest.mark.parametrize(
    "field, value",
    [
        ("governing_act_id", "adr 9001"),
        ("owning_capability", "CAP-999"),
        ("owning_capability", "C-99"),
        ("owning_work_package", "wp-22"),
        ("owning_work_package", "WP 22"),
        ("retroactive", "yes"),
        ("retroactive", "True"),
        ("business_activity_reference", "x" * 256),
    ],
)
def test_authorization_formats_are_enforced(field, value):
    authorization = _with(AUTHORIZATION, **{field: value})
    source = SOURCE if field != "governing_act_id" else "adr 9001.md"
    _expect(GovernedActMalformed, GovernedActErrorCode.INVALID_FORMAT, _act(authorization=authorization), source)


@pytest.mark.parametrize("identifier", ["BA-42", "BA-0000042", "XX-000042", "BA000042", "ba-000042"])
def test_bar_identifier_format_is_enforced(identifier):
    _expect(
        GovernedActMalformed,
        GovernedActErrorCode.INVALID_FORMAT,
        _act(execution=_with(EXECUTION, bar_business_activity_identifier=identifier)),
    )


@pytest.mark.parametrize("value", ["30-09-2026", "2026-9-30", "2026-02-30"])
def test_executed_on_must_be_a_valid_iso_date(value):
    _expect(GovernedActMalformed, GovernedActErrorCode.INVALID_FORMAT, _act(execution=_with(EXECUTION, executed_on=value)))


# ------------------------------------------------------------ identity/link


@pytest.mark.parametrize("source", ["ADR-9002_Test.md", "ADR-90010_Test.md", "ROD-9001.md", "Test_ADR-9001.md"])
def test_governing_act_id_must_identify_its_own_record(source):
    _expect(GovernedActIdentityMismatch, GovernedActErrorCode.IDENTITY_MISMATCH, _act(), source)


def test_addendum_of_must_equal_governing_act_id():
    _expect(
        GovernedActAddendumMismatch,
        GovernedActErrorCode.ADDENDUM_MISMATCH,
        _act(execution=_with(EXECUTION, addendum_of="ADR-9002")),
    )


@pytest.mark.parametrize(
    "field, value",
    [
        ("business_activity_reference", "BA-02 (TEST ONLY)"),
        ("owning_capability", "C-998"),
        ("owning_work_package", "WP-TEST-02"),
    ],
)
def test_addendum_must_echo_the_authorization(field, value):
    _expect(
        GovernedActAddendumMismatch,
        GovernedActErrorCode.ADDENDUM_MISMATCH,
        _act(execution=_with(EXECUTION, **{field: value})),
    )


# ---------------------------------------------------------------- contract


def test_all_failures_share_the_typed_base_class():
    for error_type in (GovernedActMissing, GovernedActMalformed, GovernedActIdentityMismatch, GovernedActAddendumMismatch):
        assert issubclass(error_type, GovernedActError)
        assert issubclass(error_type, ValueError)


def test_validator_has_no_database_or_write_dependency():
    source = Path(__file__).resolve().parents[1] / "services" / "bar_governed_act.py"
    imported: set[str] = set()
    for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    forbidden = {
        name
        for name in imported
        if name.startswith(("services.", "repositories.", "sqlalchemy", "models.database"))
    }
    assert not forbidden, f"governed-act validator must stay pure; imports {sorted(forbidden)}"
