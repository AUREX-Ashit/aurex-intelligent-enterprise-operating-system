"""
Enterprise BAR — TD-171 remediation tranche (WP-23 Charter §21a), R-05/R-07:
environment reconciliation and the OD-5 deployment-level block.

Compares the persisted `bar_registration` rows of one environment with the
repository governance evidence (`BAR-INDEX.md` §3 and the governed acts,
`services.bar_governance_evidence`) and classifies every row, and every
piece of evidence with no row, into exactly the seven OD-5 states of
TDS §7 ("OD-5 state set", RO decision 2026-09-30):

  valid registered row · missing governing act · malformed governing act ·
  mismatched governing act · duplicate/conflicting evidence ·
  ungoverned row · reconciliation failure

Every state except *valid registered row* is a deployment integrity failure
(OD-5): the report is blocking and the process result is non-zero. A
reconciliation that cannot complete is *reconciliation failure*, never
"clean". Reconciliation is read-only: it never adopts, deletes, rewrites or
reinterprets a row (TDS §9), and the `bar_registration` lifecycle is
unchanged (no new status). BAE/M2 does not consume this result.

`[IMPLEMENTATION DESIGN]` mapping of the pre-OD-5 §7 table onto the
decided state set, disclosed rather than assumed:
  * a row with a complete, matching act but no `BAR-INDEX.md` row, and an
    index row or execution addendum with no persisted row ("index-only"),
    are *mismatched governing act*: row, index and act disagree. The
    "index-only" case blocks in every environment, because the canonical
    environment is not designated (OD-4, external);
  * *ungoverned row* is a row that no index row, no act and no failed act
    record relates to at all; a row with some evidence that does not
    resolve to a complete act is *missing governing act* (TDS §11 S);
  * an act that fails validation and relates to no row is reported as
    *malformed governing act*.

Read-only database access is a repository-side contract only: the loader
issues SELECT statements and rolls back. Provisioning a read-only
reconciliation principal is an external prerequisite (EP-03); nothing
here proves the connection cannot write.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bar_registration import REGISTRATION_STATUS_REGISTERED, BarRegistration
from services.bar_governance_evidence import (
    INDEX_RETROACTIVE_VALUES,
    BarIndexUnreadable,
    DiscoveredAct,
    GovernanceEvidence,
    IndexEntry,
    entry_date,
    failure_names_act,
    index_entry_problems,
    load_governance_evidence,
)


class ReconciliationState(str, Enum):
    VALID_REGISTERED_ROW = "valid registered row"
    MISSING_GOVERNING_ACT = "missing governing act"
    MALFORMED_GOVERNING_ACT = "malformed governing act"
    MISMATCHED_GOVERNING_ACT = "mismatched governing act"
    DUPLICATE_CONFLICTING_EVIDENCE = "duplicate/conflicting evidence"
    UNGOVERNED_ROW = "ungoverned row"
    RECONCILIATION_FAILURE = "reconciliation failure"


EXIT_VALID = 0
EXIT_INTEGRITY_FAILURE = 1
EXIT_RECONCILIATION_FAILURE = 2


@dataclass(frozen=True)
class RegistrationSnapshot:
    """A persisted `bar_registration` row, as read. Never written back."""

    identifier: str
    business_activity_reference: str
    owning_capability: str
    owning_work_package: str
    registration_status: str
    registering_act: str
    registered_at: datetime
    is_retroactive: bool

    @property
    def registered_on(self) -> date:
        registered_at = self.registered_at
        if registered_at.tzinfo is None:  # SQLite returns the stored UTC value naive
            registered_at = registered_at.replace(tzinfo=timezone.utc)
        return registered_at.astimezone(timezone.utc).date()


@dataclass(frozen=True)
class ReconciliationResult:
    state: ReconciliationState
    subject: str
    detail: str

    @property
    def blocking(self) -> bool:
        return self.state is not ReconciliationState.VALID_REGISTERED_ROW


@dataclass(frozen=True)
class ReconciliationReport:
    results: tuple[ReconciliationResult, ...]

    @property
    def blocking(self) -> bool:
        return any(result.blocking for result in self.results)

    @property
    def exit_code(self) -> int:
        if any(r.state is ReconciliationState.RECONCILIATION_FAILURE for r in self.results):
            return EXIT_RECONCILIATION_FAILURE
        return EXIT_INTEGRITY_FAILURE if self.blocking else EXIT_VALID

    def render(self) -> str:
        if not self.results:
            return "BAR reconciliation: no registrations and no registration evidence. Not blocked."
        lines = [f"[{r.state.value}] {r.subject}: {r.detail}" for r in self.results]
        verdict = "BLOCKED (OD-5 deployment-level block)" if self.blocking else "Not blocked."
        return "\n".join([*lines, f"BAR reconciliation: {verdict}"])


def failure_report(detail: str) -> ReconciliationReport:
    """The check could not complete; never read as clean."""
    return ReconciliationReport((ReconciliationResult(ReconciliationState.RECONCILIATION_FAILURE, "reconciliation", detail),))


async def load_registration_snapshots(session: AsyncSession) -> list[RegistrationSnapshot]:
    """Read every `bar_registration` row (SELECT only) and roll back."""
    try:
        rows = (await session.execute(select(BarRegistration).order_by(BarRegistration.identifier))).scalars().all()
        return [
            RegistrationSnapshot(
                identifier=row.identifier,
                business_activity_reference=row.business_activity_reference,
                owning_capability=row.owning_capability,
                owning_work_package=row.owning_work_package,
                registration_status=row.registration_status,
                registering_act=row.registering_act,
                registered_at=row.registered_at,
                is_retroactive=row.is_retroactive,
            )
            for row in rows
        ]
    finally:
        await session.rollback()


# ---------------------------------------------------------------- classifier


def reconcile(rows: list[RegistrationSnapshot], evidence: GovernanceEvidence) -> ReconciliationReport:
    """Classify every row and every unmatched piece of evidence. Pure."""
    entries_by_id: dict[str, list[IndexEntry]] = defaultdict(list)
    entries_by_pair: dict[tuple[str, str], list[IndexEntry]] = defaultdict(list)
    for entry in evidence.index_entries:
        entries_by_id[entry.identifier].append(entry)
        entries_by_pair[(entry.owning_work_package, entry.business_activity_reference)].append(entry)
    acts_by_id: dict[str, list[DiscoveredAct]] = defaultdict(list)
    acts_by_issued: dict[str, list[DiscoveredAct]] = defaultdict(list)
    acts_by_pair: dict[tuple[str, str], list[DiscoveredAct]] = defaultdict(list)
    for discovered in evidence.acts:
        authorization = discovered.act.authorization
        acts_by_id[authorization.governing_act_id].append(discovered)
        acts_by_pair[(authorization.owning_work_package, authorization.business_activity_reference)].append(discovered)
        if discovered.act.execution is not None:
            acts_by_issued[discovered.act.execution.bar_business_activity_identifier].append(discovered)

    results: list[ReconciliationResult] = []
    rows_by_id: dict[str, list[RegistrationSnapshot]] = defaultdict(list)
    rows_by_pair: dict[tuple[str, str], list[RegistrationSnapshot]] = defaultdict(list)
    for row in rows:
        rows_by_id[row.identifier].append(row)
        rows_by_pair[(row.owning_work_package, row.business_activity_reference)].append(row)

    related_failures: set[str] = set()
    for row in rows:
        pair = (row.owning_work_package, row.business_activity_reference)
        failures = [f for f in evidence.act_failures if failure_names_act(f, row.registering_act)]
        related_failures.update(f.path for f in failures)
        results.append(
            _classify_row(
                row,
                entries_by_id=entries_by_id.get(row.identifier, []),
                entries_by_pair=entries_by_pair.get(pair, []),
                acts_by_id=acts_by_id.get(row.registering_act, []),
                acts_by_issued=acts_by_issued.get(row.identifier, []),
                acts_by_pair=acts_by_pair.get(pair, []),
                failures=[f.path for f in failures],
                row_duplicates=len(rows_by_id[row.identifier]) + len(rows_by_pair[pair]) - 2,
            )
        )

    # Duplicate evidence that no persisted row carries (a row carrying it is
    # already classified duplicate/conflicting above). Its members are not
    # also reported as unpersisted evidence, so each condition has one state.
    row_act_ids = {row.registering_act for row in rows}
    duplicated: set[int] = set()
    groups = [
        ("index identifier", key, members, key in rows_by_id)
        for key, members in entries_by_id.items() if key and len(members) > 1
    ] + [
        ("index (WP, reference)", f"{key[0]} / {key[1]}", members, key in rows_by_pair)
        for key, members in entries_by_pair.items() if all(key) and len(members) > 1
    ] + [
        ("governing act id", key, members, key in row_act_ids)
        for key, members in acts_by_id.items() if len(members) > 1
    ] + [
        ("issued identifier", key, members, key in rows_by_id)
        for key, members in acts_by_issued.items() if len(members) > 1
    ] + [
        ("authorized (WP, reference)", f"{key[0]} / {key[1]}", members, key in rows_by_pair)
        for key, members in acts_by_pair.items() if len(members) > 1
    ]
    for kind, key, members, carried_by_row in groups:
        duplicated.update(id(member) for member in members)
        if not carried_by_row:
            subjects = [m.subject if isinstance(m, IndexEntry) else m.path for m in members]
            results.append(
                ReconciliationResult(
                    ReconciliationState.DUPLICATE_CONFLICTING_EVIDENCE, f"{kind} {key}", f"claimed by {subjects}"
                )
            )

    # Evidence that claims a registration this environment does not hold.
    for entry in evidence.index_entries:
        if entry.identifier not in rows_by_id and id(entry) not in duplicated:
            problems = index_entry_problems(entry)
            detail = "index row with no persisted registration in this environment"
            results.append(
                ReconciliationResult(
                    ReconciliationState.MISMATCHED_GOVERNING_ACT,
                    entry.subject,
                    f"{detail} (malformed: {'; '.join(problems)})" if problems else detail,
                )
            )
    for discovered in evidence.acts:
        execution = discovered.act.execution
        if id(discovered) in duplicated:
            continue
        if execution is not None and execution.bar_business_activity_identifier not in rows_by_id:
            results.append(
                ReconciliationResult(
                    ReconciliationState.MISMATCHED_GOVERNING_ACT,
                    discovered.path,
                    f"execution addendum records {execution.bar_business_activity_identifier}, which is not persisted in this environment",
                )
            )
    for failure in evidence.act_failures:
        if failure.path not in related_failures:
            results.append(ReconciliationResult(ReconciliationState.MALFORMED_GOVERNING_ACT, failure.path, str(failure.error)))
    return ReconciliationReport(tuple(results))


def _classify_row(
    row: RegistrationSnapshot,
    *,
    entries_by_id: list[IndexEntry],
    entries_by_pair: list[IndexEntry],
    acts_by_id: list[DiscoveredAct],
    acts_by_issued: list[DiscoveredAct],
    acts_by_pair: list[DiscoveredAct],
    failures: list[str],
    row_duplicates: int,
) -> ReconciliationResult:
    subject = f"bar_registration {row.identifier}"
    S = ReconciliationState

    def result(state: ReconciliationState, detail: str) -> ReconciliationResult:
        return ReconciliationResult(state, subject, detail)

    if not (entries_by_id or entries_by_pair or acts_by_id or acts_by_issued or acts_by_pair or failures):
        return result(S.UNGOVERNED_ROW, f"no index row and no governed act relates to this row (registering_act '{row.registering_act}')")

    conflicts = []
    if row_duplicates > 0:
        conflicts.append("more than one persisted row shares this identifier or (WP, reference)")
    if len(entries_by_id) > 1 or len(entries_by_pair) > 1:
        conflicts.append("more than one index row for this identifier or (WP, reference)")
    if len(acts_by_id) > 1 or len(acts_by_issued) > 1 or len(acts_by_pair) > 1:
        conflicts.append("more than one act for this registering act, identifier or (WP, reference)")
    if conflicts:
        return result(S.DUPLICATE_CONFLICTING_EVIDENCE, "; ".join(conflicts))

    if failures:
        return result(S.MALFORMED_GOVERNING_ACT, f"registering act record(s) {failures} fail validation")
    if not acts_by_id:
        if acts_by_issued:
            return result(
                S.MISMATCHED_GOVERNING_ACT,
                f"identifier issued by '{acts_by_issued[0].path}' "
                f"({acts_by_issued[0].act.authorization.governing_act_id}), but the row cites '{row.registering_act}'",
            )
        return result(S.MISSING_GOVERNING_ACT, f"registering act '{row.registering_act}' is not a governed act in the repository")
    discovered = acts_by_id[0]
    act = discovered.act
    if act.execution is None:
        return result(S.MISSING_GOVERNING_ACT, f"'{discovered.path}' has no committed execution addendum")

    mismatches = _row_vs_act(row, discovered)
    entry = entries_by_id[0] if entries_by_id else None
    if entry is None:
        mismatches.append("no BAR-INDEX.md §3 row for this identifier")
    else:
        mismatches.extend(_row_vs_entry(row, entry))
    if mismatches:
        return result(S.MISMATCHED_GOVERNING_ACT, "; ".join(mismatches))
    return result(S.VALID_REGISTERED_ROW, f"row = index (line {entry.line}) = act '{discovered.path}'")


def _row_vs_act(row: RegistrationSnapshot, discovered: DiscoveredAct) -> list[str]:
    authorization, execution = discovered.act.authorization, discovered.act.execution
    assert execution is not None
    pairs = [
        ("identifier", row.identifier, execution.bar_business_activity_identifier),
        ("business_activity_reference", row.business_activity_reference, authorization.business_activity_reference),
        ("owning_capability", row.owning_capability, authorization.owning_capability),
        ("owning_work_package", row.owning_work_package, authorization.owning_work_package),
        ("is_retroactive", row.is_retroactive, authorization.retroactive),
        ("registered_on", row.registered_on, execution.executed_on),
        ("registration_status", row.registration_status, REGISTRATION_STATUS_REGISTERED),
    ]
    return [f"{name}: row {mine!r}, act {theirs!r}" for name, mine, theirs in pairs if mine != theirs]


def _row_vs_entry(row: RegistrationSnapshot, entry: IndexEntry) -> list[str]:
    problems = [f"index row malformed: {p}" for p in index_entry_problems(entry)]
    if problems:
        return problems
    pairs = [
        ("business_activity_reference", row.business_activity_reference, entry.business_activity_reference),
        ("owning_capability", row.owning_capability, entry.owning_capability),
        ("owning_work_package", row.owning_work_package, entry.owning_work_package),
        ("registering_act", row.registering_act, entry.registering_act),
        ("is_retroactive", row.is_retroactive, INDEX_RETROACTIVE_VALUES[entry.retroactive]),
        ("registered_on", row.registered_on, entry_date(entry)),
    ]
    return [f"{name}: row {mine!r}, index {theirs!r}" for name, mine, theirs in pairs if mine != theirs]


async def reconcile_environment(session: AsyncSession, repository_root: Path) -> ReconciliationReport:
    """Load evidence and rows, then classify. Any failure to read either is *reconciliation failure*."""
    try:
        evidence = load_governance_evidence(repository_root)
    except (BarIndexUnreadable, OSError, UnicodeDecodeError) as exc:
        return failure_report(f"repository governance evidence unreadable: {exc}")
    try:
        rows = await load_registration_snapshots(session)
    except Exception as exc:  # noqa: BLE001 — any store failure means the check did not complete
        return failure_report(f"registration store unreadable: {type(exc).__name__}: {exc}")
    return reconcile(rows, evidence)
