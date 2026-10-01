"""
TD-171 remediation tranche (WP-23 Charter §21a), slice 3: the repository
CI check between `BAR-INDEX.md` §3 and the governed acts
(`services/bar_governance_evidence.py`, `scripts/bar_index_check.py`).

Repository-only: no database. Test repositories start from the real
`BAR-INDEX.md` text (see `tests/bar_governance_fixtures.py`), and the real
checkout itself is checked as the CI gate.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from scripts import bar_index_check
from services.bar_governance_evidence import (
    BAR_INDEX_RELATIVE_PATH,
    DEFAULT_REPOSITORY_ROOT,
    BarIndexUnreadable,
    EvidenceFindingCode,
    check_repository,
    parse_bar_index,
)
from tests.bar_governance_fixtures import (
    GovernanceRepository,
    addendum_text,
    authorization_text,
    index_row,
)

C = EvidenceFindingCode


@pytest.fixture
def repo(tmp_path: Path) -> GovernanceRepository:
    repository = GovernanceRepository(tmp_path)
    repository.write_index()
    return repository


def _codes(root: Path) -> list[tuple[EvidenceFindingCode, bool]]:
    return sorted(((f.code, f.blocking) for f in check_repository(root)), key=lambda t: t[0].value)


# --------------------------------------------------- the real repository (CI)


def test_this_repository_is_consistent():
    """The CI gate: the checkout's own BAR-INDEX.md and acts agree."""
    assert check_repository(DEFAULT_REPOSITORY_ROOT) == []


def test_real_index_parses_as_an_empty_register():
    assert parse_bar_index((DEFAULT_REPOSITORY_ROOT / BAR_INDEX_RELATIVE_PATH).read_text(encoding="utf-8")) == []


def test_ci_check_is_read_only(repo):
    repo.write_index(repo.governed("ADR-9201", "BA-01 (GOV TEST)", "BA-000001"))
    repo.write_act("ADR-9202", authorization_text("ADR-9202", "BA-02 (GOV TEST)"))

    def digest() -> dict[str, str]:
        return {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(repo.root.rglob("*")) if p.is_file()}

    before = digest()
    check_repository(repo.root)
    assert bar_index_check.main(["--repository-root", str(repo.root)]) == bar_index_check.EXIT_CLEAN
    assert digest() == before


# ---------------------------------------------------------------- clean


def test_empty_repository_is_clean(repo):
    assert _codes(repo.root) == []


def test_complete_act_with_matching_index_row_is_clean(repo):
    repo.write_index(
        repo.governed("ADR-9203", "BA-01 (GOV TEST)", "BA-000001"),
        repo.governed("ADR-9204", "BA-02 (GOV TEST)", "BA-000002", retroactive=True),
    )
    assert _codes(repo.root) == []


def test_authorization_awaiting_execution_is_a_non_blocking_notice(repo):
    repo.write_act("ADR-9205", authorization_text("ADR-9205", "BA-01 (GOV TEST)"))
    assert _codes(repo.root) == [(C.AUTHORIZATION_PENDING_EXECUTION, False)]
    assert bar_index_check.main(["--repository-root", str(repo.root)]) == bar_index_check.EXIT_CLEAN


# ------------------------------------------------------ index -> acts


def test_index_row_without_act_is_missing_act(repo):
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9206"))
    assert _codes(repo.root) == [(C.MISSING_ACT, True)]


def test_index_row_citing_authorization_only_act_is_incomplete(repo):
    repo.write_act("ADR-9207", authorization_text("ADR-9207", "BA-01 (GOV TEST)"))
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9207"))
    assert _codes(repo.root) == [(C.INCOMPLETE_ACT, True)]


def test_index_identifier_differing_from_addendum_is_identifier_mismatch(repo):
    repo.governed("ADR-9208", "BA-01 (GOV TEST)", "BA-000001")
    repo.write_index(index_row("BA-000007", "BA-01 (GOV TEST)", "ADR-9208"))
    codes = _codes(repo.root)
    # index -> act (wrong identifier) and act -> index (BA-000001 not indexed)
    assert codes == [(C.IDENTIFIER_MISMATCH, True), (C.MISSING_INDEX_ENTRY, True)]


@pytest.mark.parametrize(
    "overrides",
    [
        {"capability": "C-998"},
        {"work_package": "WP-TEST-OTHER"},
        {"retroactive": "Yes"},
    ],
)
def test_index_field_differing_from_act_is_field_mismatch(repo, overrides):
    repo.governed("ADR-9209", "BA-01 (GOV TEST)", "BA-000001")
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9209", **overrides))
    assert _codes(repo.root) == [(C.FIELD_MISMATCH, True)]


def test_index_reference_differing_from_act_is_field_mismatch(repo):
    repo.governed("ADR-9210", "BA-01 (GOV TEST)", "BA-000001")
    repo.write_index(index_row("BA-000001", "BA-01 (RENAMED)", "ADR-9210"))
    assert _codes(repo.root) == [(C.FIELD_MISMATCH, True)]


def test_index_date_differing_from_execution_is_stale(repo):
    repo.governed("ADR-9211", "BA-01 (GOV TEST)", "BA-000001")
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9211", registered_on="2026-09-30"))
    assert _codes(repo.root) == [(C.STALE_INDEX_ENTRY, True)]


@pytest.mark.parametrize(
    "row",
    [
        index_row("BA-1", "BA-01 (GOV TEST)", "ADR-9212"),
        index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9212", status="Pending"),
        index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9212", registered_on="1 Oct 2026"),
        index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9212", retroactive="true"),
        index_row("BA-000001", "", "ADR-9212"),
        "| `BA-000001` | BA-01 (GOV TEST) | C-999 |",
    ],
)
def test_malformed_index_row_is_reported(repo, row):
    repo.governed("ADR-9212", "BA-01 (GOV TEST)", "BA-000001")
    repo.write_index(row)
    codes = _codes(repo.root)
    assert (C.MALFORMED_INDEX_ENTRY, True) in codes


# ------------------------------------------------------ acts -> index


def test_complete_act_without_index_row_is_missing_index_entry(repo):
    repo.governed("ADR-9213", "BA-01 (GOV TEST)", "BA-000001")
    assert _codes(repo.root) == [(C.MISSING_INDEX_ENTRY, True)]


def test_identifier_indexed_under_another_act_is_identifier_mismatch(repo):
    repo.governed("ADR-9214", "BA-01 (GOV TEST)", "BA-000001")
    repo.governed("ADR-9215", "BA-02 (GOV TEST)", "BA-000002")
    # Both rows cite ADR-9215: BA-000001's own act is not the one indexed.
    repo.write_index(
        index_row("BA-000001", "BA-02 (GOV TEST)", "ADR-9215"),
        index_row("BA-000002", "BA-02 (GOV TEST)", "ADR-9215"),
    )
    codes = [code for code, _ in _codes(repo.root)]
    assert C.IDENTIFIER_MISMATCH in codes
    assert C.DUPLICATE_REFERENCE in codes


def test_execution_addendum_without_authorization_is_unexpected_evidence(repo):
    authorization = authorization_text("ADR-9216", "BA-01 (GOV TEST)")
    repo.write_act("ADR-9216", "# ADR-9216\n\n" + addendum_text(authorization, "ADR-9216", "BA-000001"))
    assert _codes(repo.root) == [(C.UNEXPECTED_REGISTRATION_EVIDENCE, True)]


def test_malformed_act_is_reported_and_not_also_missing(repo):
    repo.write_act("ADR-9217", authorization_text("ADR-9217", "BA-01 (GOV TEST)", governance_authority="Someone Else"))
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9217"))
    assert _codes(repo.root) == [(C.MALFORMED_ACT, True)]


def test_addendum_disagreeing_with_its_authorization_is_malformed(repo):
    authorization = authorization_text("ADR-9218", "BA-01 (GOV TEST)")
    addendum = addendum_text(authorization, "ADR-9218", "BA-000001").replace("| C-999 |", "| C-998 |")
    repo.write_act("ADR-9218", authorization + "\n" + addendum)
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9218"))
    assert _codes(repo.root) == [(C.MALFORMED_ACT, True)]


# ---------------------------------------------------------- duplicates


def test_duplicate_identifier_in_index(repo):
    repo.write_index(
        repo.governed("ADR-9219", "BA-01 (GOV TEST)", "BA-000001"),
        index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9219"),
    )
    codes = [code for code, _ in _codes(repo.root)]
    assert C.DUPLICATE_IDENTIFIER in codes
    assert C.DUPLICATE_REFERENCE in codes


def test_two_acts_issuing_the_same_identifier(repo):
    repo.write_index(
        repo.governed("ADR-9220", "BA-01 (GOV TEST)", "BA-000001"),
        repo.governed("ADR-9221", "BA-02 (GOV TEST)", "BA-000001"),
    )
    assert C.DUPLICATE_IDENTIFIER in [code for code, _ in _codes(repo.root)]


def test_two_acts_authorizing_the_same_activity(repo):
    repo.write_act("ADR-9222", authorization_text("ADR-9222", "BA-01 (GOV TEST)"))
    repo.write_act("ADR-9223", authorization_text("ADR-9223", "BA-01 (GOV TEST)"))
    assert (C.DUPLICATE_REFERENCE, True) in _codes(repo.root)


def test_one_act_identifier_declared_by_two_records(repo):
    text = authorization_text("ADR-9224", "BA-01 (GOV TEST)")
    repo.write_act("ADR-9224", text)
    repo.write_act("ADR-9224", text, name="ADR-9224-copy.md")
    assert (C.DUPLICATE_ACT, True) in _codes(repo.root)


# ------------------------------------------------- unreadable evidence


def test_missing_index_is_unreadable(tmp_path):
    with pytest.raises(BarIndexUnreadable):
        check_repository(tmp_path)
    assert bar_index_check.main(["--repository-root", str(tmp_path)]) == bar_index_check.EXIT_UNREADABLE


@pytest.mark.parametrize(
    "mutate",
    [
        lambda t: t.replace("## 3. Register", "## 3. Registry"),
        lambda t: t.replace("| Business Activity Identifier | Business Activity Reference |", "| Identifier | Reference |", 1),
    ],
)
def test_index_without_a_readable_register_is_unreadable(repo, mutate):
    path = repo.root / BAR_INDEX_RELATIVE_PATH
    path.write_text(mutate(path.read_text(encoding="utf-8")), encoding="utf-8")
    assert bar_index_check.main(["--repository-root", str(repo.root)]) == bar_index_check.EXIT_UNREADABLE


# --------------------------------------------------------- exit status


def test_blocking_findings_exit_non_zero(repo, capsys):
    repo.write_index(index_row("BA-000001", "BA-01 (GOV TEST)", "ADR-9225"))
    assert bar_index_check.main(["--repository-root", str(repo.root)]) == bar_index_check.EXIT_BLOCKING
    assert "[BLOCKING] MISSING_ACT" in capsys.readouterr().out


def test_documents_without_act_titles_are_not_treated_as_acts(repo):
    repo.write(Path("architecture/06-Reviews/ROD-TEST.md"), 'The act carries a table titled "BAR Registration Authorization".\n')
    assert _codes(repo.root) == []
