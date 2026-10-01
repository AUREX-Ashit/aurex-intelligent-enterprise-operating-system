"""
Enterprise BAR — TD-171 remediation tranche (WP-23 Charter §21a), R-04:
repository governance evidence and the CI repository check.

Reads the two repository-side halves of a governed BAR registration and
checks them against each other in both directions:

  * `BAR-INDEX.md` §3 (the governance catalogue, RD-23-03 Option D);
  * the governed acts (OD-1 two-part acts, OD-3 metadata convention),
    discovered under `architecture/` and validated by
    `services.bar_governed_act` (slice 1), never re-parsed here.

Repository-only and read-only (TDS §6): it opens no database connection,
never asserts deployed state, and never creates or modifies an act or the
index. Runtime-row comparison is reconciliation's job
(`services.bar_reconciliation`), which reuses this module's evidence.

`[IMPLEMENTATION DESIGN]` finding codes, disclosed rather than assumed:
  * an act whose authorization has no execution addendum and which no
    index row cites is `AUTHORIZATION_PENDING_EXECUTION`, the legitimate
    state between committing an authorization and running the governed
    operation (OD-1 step 1). It is reported and is NOT blocking;
  * an execution addendum in a record with no authorization component is
    `UNEXPECTED_REGISTRATION_EVIDENCE`;
  * an index row whose status or registration date no longer agrees with
    the act it cites is `STALE_INDEX_ENTRY`.
Every other finding is blocking.

Not checked here (not specifiable from repository content today): whether
an act is "Accepted" (§17.1.3 defines no acceptance field), and the
canonical environment (OD-4, external).
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path

from services.bar_governed_act import (
    GovernedAct,
    GovernedActError,
    GovernedActErrorCode,
    declares_governed_act,
    parse_governed_act,
    table_cells,
)

# The repository checkout this module runs from (Backend/Services/AuthService/services/ -> root).
DEFAULT_REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
BAR_INDEX_RELATIVE_PATH = Path("architecture/00-Governance/BAR-INDEX.md")
ACT_SEARCH_RELATIVE_ROOT = Path("architecture")

INDEX_REGISTER_HEADING = "## 3. Register"
INDEX_COLUMNS = (
    "Business Activity Identifier",
    "Business Activity Reference",
    "Owning Capability",
    "Owning Work Package",
    "Registration Status",
    "Registering Act",
    "Registration Date",
    "Retroactive",
)
INDEX_STATUS_REGISTERED = "Registered"
INDEX_RETROACTIVE_VALUES = {"Yes": True, "No": False}
_INDEX_EMPTY_MARKER = "*(no entries)*"
_INDEX_IDENTIFIER_RE = re.compile(r"^BA-\d{6}$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")


class BarIndexUnreadable(RuntimeError):
    """`BAR-INDEX.md` is absent, or its §3 Register cannot be located or read as a table."""


class EvidenceFindingCode(str, Enum):
    MISSING_ACT = "MISSING_ACT"
    MISSING_INDEX_ENTRY = "MISSING_INDEX_ENTRY"
    IDENTIFIER_MISMATCH = "IDENTIFIER_MISMATCH"
    FIELD_MISMATCH = "FIELD_MISMATCH"
    DUPLICATE_IDENTIFIER = "DUPLICATE_IDENTIFIER"
    DUPLICATE_REFERENCE = "DUPLICATE_REFERENCE"
    DUPLICATE_ACT = "DUPLICATE_ACT"
    MALFORMED_ACT = "MALFORMED_ACT"
    MALFORMED_INDEX_ENTRY = "MALFORMED_INDEX_ENTRY"
    INCOMPLETE_ACT = "INCOMPLETE_ACT"
    STALE_INDEX_ENTRY = "STALE_INDEX_ENTRY"
    UNEXPECTED_REGISTRATION_EVIDENCE = "UNEXPECTED_REGISTRATION_EVIDENCE"
    AUTHORIZATION_PENDING_EXECUTION = "AUTHORIZATION_PENDING_EXECUTION"


NON_BLOCKING_CODES = frozenset({EvidenceFindingCode.AUTHORIZATION_PENDING_EXECUTION})


@dataclass(frozen=True)
class EvidenceFinding:
    code: EvidenceFindingCode
    subject: str
    detail: str

    @property
    def blocking(self) -> bool:
        return self.code not in NON_BLOCKING_CODES


# ------------------------------------------------------------------- index


@dataclass(frozen=True)
class IndexEntry:
    """One `BAR-INDEX.md` §3 row, as written. `line` is 1-based."""

    line: int
    identifier: str
    business_activity_reference: str
    owning_capability: str
    owning_work_package: str
    registration_status: str
    registering_act: str
    registration_date: str
    retroactive: str
    column_count: int = len(INDEX_COLUMNS)

    @property
    def subject(self) -> str:
        return f"BAR-INDEX.md:{self.line} ({self.identifier or 'no identifier'})"


def parse_bar_index(text: str) -> list[IndexEntry]:
    """The §3 Register rows. Raises `BarIndexUnreadable` if the Register table cannot be read."""
    lines = text.splitlines()
    try:
        heading = next(i for i, line in enumerate(lines) if line.strip() == INDEX_REGISTER_HEADING)
    except StopIteration:
        raise BarIndexUnreadable(f"no '{INDEX_REGISTER_HEADING}' section.") from None
    try:
        header = next(i for i in range(heading + 1, len(lines)) if lines[i].lstrip().startswith("|"))
    except StopIteration:
        raise BarIndexUnreadable("the Register section has no table.") from None
    if any(lines[i].startswith("## ") for i in range(heading + 1, header)):
        raise BarIndexUnreadable("the Register section has no table.")
    if tuple(table_cells(lines[header])) != INDEX_COLUMNS:
        raise BarIndexUnreadable(f"the Register table header is not {INDEX_COLUMNS}.")
    if header + 1 >= len(lines) or not all(_SEPARATOR_CELL_RE.match(c) for c in table_cells(lines[header + 1])):
        raise BarIndexUnreadable("the Register table has no separator row.")

    entries: list[IndexEntry] = []
    for i in range(header + 2, len(lines)):
        if not lines[i].lstrip().startswith("|"):
            break
        cells = table_cells(lines[i])
        if cells[0] == _INDEX_EMPTY_MARKER and not any(cells[1:]):
            continue
        padded = (cells + [""] * len(INDEX_COLUMNS))[: len(INDEX_COLUMNS)]
        entries.append(IndexEntry(i + 1, *padded, column_count=len(cells)))
    return entries


def index_entry_problems(entry: IndexEntry) -> list[str]:
    """Format problems in one index row (empty when the row is well formed)."""
    problems = []
    if entry.column_count != len(INDEX_COLUMNS):
        problems.append(f"row has {entry.column_count} columns, expected {len(INDEX_COLUMNS)}")
    if not _INDEX_IDENTIFIER_RE.match(entry.identifier):
        problems.append(f"identifier '{entry.identifier}' is not BA-NNNNNN")
    for name in ("business_activity_reference", "owning_capability", "owning_work_package", "registering_act"):
        if not getattr(entry, name):
            problems.append(f"'{name}' is empty")
    if entry.registration_status != INDEX_STATUS_REGISTERED:
        problems.append(f"registration status '{entry.registration_status}' is not '{INDEX_STATUS_REGISTERED}'")
    if entry_date(entry) is None:
        problems.append(f"registration date '{entry.registration_date}' is not YYYY-MM-DD")
    if entry.retroactive not in INDEX_RETROACTIVE_VALUES:
        problems.append(f"retroactive '{entry.retroactive}' is not Yes/No")
    return problems


def entry_date(entry: IndexEntry) -> date | None:
    if not _ISO_DATE_RE.match(entry.registration_date):
        return None
    try:
        return date.fromisoformat(entry.registration_date)
    except ValueError:
        return None


# -------------------------------------------------------------------- acts


@dataclass(frozen=True)
class ActFailure:
    """A record that declares a governed act but does not validate."""

    path: str
    error: GovernedActError


@dataclass(frozen=True)
class DiscoveredAct:
    path: str
    act: GovernedAct


@dataclass
class GovernanceEvidence:
    index_entries: list[IndexEntry]
    acts: list[DiscoveredAct] = field(default_factory=list)
    act_failures: list[ActFailure] = field(default_factory=list)


def discover_acts(repository_root: Path) -> tuple[list[DiscoveredAct], list[ActFailure]]:
    """Every Markdown record under `architecture/` that declares a governed act, validated."""
    acts: list[DiscoveredAct] = []
    failures: list[ActFailure] = []
    for path in sorted((repository_root / ACT_SEARCH_RELATIVE_ROOT).rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not declares_governed_act(text):
            continue
        relative = path.relative_to(repository_root).as_posix()
        try:
            acts.append(DiscoveredAct(relative, parse_governed_act(text, source_name=path.name)))
        except GovernedActError as exc:
            failures.append(ActFailure(relative, exc))
    return acts, failures


def load_governance_evidence(repository_root: Path) -> GovernanceEvidence:
    """Read the index and every act. Raises `BarIndexUnreadable` / `OSError` when the evidence cannot be read."""
    index_path = repository_root / BAR_INDEX_RELATIVE_PATH
    if not index_path.is_file():
        raise BarIndexUnreadable(f"'{BAR_INDEX_RELATIVE_PATH.as_posix()}' does not exist.")
    entries = parse_bar_index(index_path.read_text(encoding="utf-8"))
    acts, failures = discover_acts(repository_root)
    return GovernanceEvidence(entries, acts, failures)


def failure_is_execution_only(failure: ActFailure) -> bool:
    return failure.error.code is GovernedActErrorCode.MISSING_SECTION


def failure_names_act(failure: ActFailure, governing_act_id: str) -> bool:
    """Whether a failed record is the record `governing_act_id` would identify (slice 1 identity rule)."""
    stem = Path(failure.path).stem
    return stem == governing_act_id or stem.startswith((f"{governing_act_id}_", f"{governing_act_id}-"))


# ---------------------------------------------------------------- CI check


def check_repository_evidence(evidence: GovernanceEvidence) -> list[EvidenceFinding]:
    """Bidirectional index <-> act check. Pure; reads nothing beyond `evidence`."""
    findings: list[EvidenceFinding] = []
    add = lambda code, subject, detail: findings.append(EvidenceFinding(code, subject, detail))  # noqa: E731

    for failure in evidence.act_failures:
        if failure_is_execution_only(failure):
            add(
                EvidenceFindingCode.UNEXPECTED_REGISTRATION_EVIDENCE,
                failure.path,
                f"registration evidence without an authorization component: {failure.error}",
            )
        else:
            add(EvidenceFindingCode.MALFORMED_ACT, failure.path, str(failure.error))

    by_act_id: dict[str, list[DiscoveredAct]] = defaultdict(list)
    by_issued: dict[str, list[DiscoveredAct]] = defaultdict(list)
    by_act_pair: dict[tuple[str, str], list[DiscoveredAct]] = defaultdict(list)
    for discovered in evidence.acts:
        authorization = discovered.act.authorization
        by_act_id[authorization.governing_act_id].append(discovered)
        by_act_pair[(authorization.owning_work_package, authorization.business_activity_reference)].append(discovered)
        if discovered.act.execution is not None:
            by_issued[discovered.act.execution.bar_business_activity_identifier].append(discovered)
    for act_id, group in by_act_id.items():
        if len(group) > 1:
            add(EvidenceFindingCode.DUPLICATE_ACT, act_id, f"declared by {[d.path for d in group]}")
    for identifier, group in by_issued.items():
        if len(group) > 1:
            add(EvidenceFindingCode.DUPLICATE_IDENTIFIER, identifier, f"issued by more than one act: {[d.path for d in group]}")
    for pair, group in by_act_pair.items():
        if len(group) > 1:
            add(EvidenceFindingCode.DUPLICATE_REFERENCE, f"{pair[0]} / {pair[1]}", f"authorized by more than one act: {[d.path for d in group]}")

    by_entry_id: dict[str, list[IndexEntry]] = defaultdict(list)
    by_entry_pair: dict[tuple[str, str], list[IndexEntry]] = defaultdict(list)
    for entry in evidence.index_entries:
        by_entry_id[entry.identifier].append(entry)
        by_entry_pair[(entry.owning_work_package, entry.business_activity_reference)].append(entry)
    for identifier, group in by_entry_id.items():
        if identifier and len(group) > 1:
            add(EvidenceFindingCode.DUPLICATE_IDENTIFIER, identifier, f"index rows at lines {[e.line for e in group]}")
    for pair, group in by_entry_pair.items():
        if all(pair) and len(group) > 1:
            add(EvidenceFindingCode.DUPLICATE_REFERENCE, f"{pair[0]} / {pair[1]}", f"index rows at lines {[e.line for e in group]}")

    # index -> acts
    for entry in evidence.index_entries:
        problems = index_entry_problems(entry)
        if problems:
            add(EvidenceFindingCode.MALFORMED_INDEX_ENTRY, entry.subject, "; ".join(problems))
            continue
        cited = by_act_id.get(entry.registering_act, [])
        if not cited:
            failed = [f for f in evidence.act_failures if failure_names_act(f, entry.registering_act)]
            if not failed:  # a failed record is already reported as malformed above
                add(EvidenceFindingCode.MISSING_ACT, entry.subject, f"registering act '{entry.registering_act}' is not a governed act in the repository")
            continue
        if len(cited) > 1:
            continue  # DUPLICATE_ACT already reported
        act = cited[0].act
        if act.execution is None:
            add(EvidenceFindingCode.INCOMPLETE_ACT, entry.subject, f"'{cited[0].path}' has no execution addendum")
            continue
        if act.execution.bar_business_activity_identifier != entry.identifier:
            add(
                EvidenceFindingCode.IDENTIFIER_MISMATCH,
                entry.subject,
                f"'{cited[0].path}' records {act.execution.bar_business_activity_identifier}, the index records {entry.identifier}",
            )
            continue
        for name, expected, actual in _entry_vs_act(entry, act):
            add(EvidenceFindingCode.FIELD_MISMATCH, entry.subject, f"'{name}': index '{actual}', act '{expected}'")
        if entry_date(entry) != act.execution.executed_on:
            add(EvidenceFindingCode.STALE_INDEX_ENTRY, entry.subject, f"registration date {entry.registration_date} != executed_on {act.execution.executed_on}")

    # acts -> index
    cited_ids = {entry.registering_act for entry in evidence.index_entries}
    for discovered in evidence.acts:
        act = discovered.act
        act_id = act.authorization.governing_act_id
        if act.execution is None:
            if act_id not in cited_ids:
                add(EvidenceFindingCode.AUTHORIZATION_PENDING_EXECUTION, discovered.path, "authorization without an execution addendum (not yet executed)")
            continue
        issued = act.execution.bar_business_activity_identifier
        entries = by_entry_id.get(issued, [])
        if not entries:
            add(EvidenceFindingCode.MISSING_INDEX_ENTRY, discovered.path, f"{issued} has no BAR-INDEX.md §3 row")
        elif all(entry.registering_act != act_id for entry in entries):
            add(
                EvidenceFindingCode.IDENTIFIER_MISMATCH,
                discovered.path,
                f"{issued} is indexed under registering act(s) {sorted({e.registering_act for e in entries})}, not {act_id}",
            )
    return findings


def _entry_vs_act(entry: IndexEntry, act: GovernedAct) -> list[tuple[str, str, str]]:
    authorization = act.authorization
    pairs = [
        ("business_activity_reference", authorization.business_activity_reference, entry.business_activity_reference),
        ("owning_capability", authorization.owning_capability, entry.owning_capability),
        ("owning_work_package", authorization.owning_work_package, entry.owning_work_package),
        ("retroactive", "Yes" if authorization.retroactive else "No", entry.retroactive),
    ]
    return [(name, expected, actual) for name, expected, actual in pairs if expected != actual]


def check_repository(repository_root: Path) -> list[EvidenceFinding]:
    """Load and check. Raises `BarIndexUnreadable` / `OSError` if the evidence cannot be read."""
    return check_repository_evidence(load_governance_evidence(repository_root))
