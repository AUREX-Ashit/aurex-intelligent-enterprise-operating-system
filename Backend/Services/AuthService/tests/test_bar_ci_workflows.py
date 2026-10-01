"""
TD-171 remediation tranche (WP-23 Charter §21a), slice 3: static validation of
the BAR CI workflows (`.github/workflows/bar-governance-ci.yml`,
`.github/workflows/bar-postgres-ci.yml`).

Proves that the trigger paths cover the BAR evidence (BAR-INDEX.md, governed
acts anywhere under architecture/, the evidence code) and that the
PostgreSQL job cannot report a skip as a pass. It parses configuration only;
it does not prove that GitHub ran anything.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from services.bar_governance_evidence import BAR_INDEX_RELATIVE_PATH, DEFAULT_REPOSITORY_ROOT

WORKFLOWS = DEFAULT_REPOSITORY_ROOT / ".github" / "workflows"
GOVERNANCE_WORKFLOW = WORKFLOWS / "bar-governance-ci.yml"
POSTGRES_WORKFLOW = WORKFLOWS / "bar-postgres-ci.yml"
AUTHSERVICE = "Backend/Services/AuthService"


def _load(path: Path) -> dict:
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    workflow["on"] = workflow.pop("on", None) or workflow.pop(True)  # YAML 1.1 reads `on` as True
    return workflow


def _glob_regex(pattern: str) -> re.Pattern[str]:
    """GitHub Actions path-filter glob: `**` crosses directories, `*` and `?` do not."""
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pattern[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pattern[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pattern[i]), i + 1
    return re.compile(f"^{out}$")


def _triggers(workflow: dict, path: str) -> bool:
    return any(_glob_regex(p).match(path) for p in workflow["on"]["push"]["paths"])


@pytest.fixture(scope="module", params=[GOVERNANCE_WORKFLOW, POSTGRES_WORKFLOW], ids=["governance", "postgres"])
def workflow(request) -> dict:
    return _load(request.param)


def test_push_and_pull_request_filters_are_identical(workflow):
    assert workflow["on"]["push"]["paths"] == workflow["on"]["pull_request"]["paths"]
    assert workflow["on"]["push"]["branches"] == ["main", "master"]


def test_every_literal_trigger_path_exists(workflow):
    for pattern in workflow["on"]["push"]["paths"]:
        if not any(ch in pattern for ch in "*?["):
            assert (DEFAULT_REPOSITORY_ROOT / pattern).is_file(), f"stale trigger path {pattern}"


def test_glob_translation():
    assert _glob_regex("architecture/**/*.md").match("architecture/BAR.md")
    assert _glob_regex("architecture/**/*.md").match("architecture/a/b/c.md")
    assert not _glob_regex("architecture/**/*.md").match("architecture/a/b.txt")
    assert not _glob_regex("a/*.py").match("a/b/c.py")


# ------------------------------------------------- governance evidence check


@pytest.mark.parametrize(
    "path",
    [
        BAR_INDEX_RELATIVE_PATH.as_posix(),
        "architecture/07-Decisions/ADR-0999_Registering_Act.md",
        "architecture/06-Reviews/ROD-TEST-Registering-Act.md",
        "architecture/99-Archive/old/ADR-0001_Act.md",
        f"{AUTHSERVICE}/services/bar_governance_evidence.py",
        f"{AUTHSERVICE}/services/bar_governed_act.py",
        f"{AUTHSERVICE}/scripts/bar_index_check.py",
        ".github/workflows/bar-governance-ci.yml",
    ],
)
def test_governance_check_triggers_on_bar_evidence(path):
    assert _triggers(_load(GOVERNANCE_WORKFLOW), path)


@pytest.mark.parametrize(
    "path",
    [f"{AUTHSERVICE}/main.py", "source/frontend/app/page.tsx", "Infrastructure/Docker/docker-compose.yml", "README.md"],
)
def test_governance_check_does_not_trigger_on_unrelated_paths(path):
    assert not _triggers(_load(GOVERNANCE_WORKFLOW), path)


def test_governance_job_runs_the_checker_from_the_service_directory():
    workflow = _load(GOVERNANCE_WORKFLOW)
    assert workflow["defaults"]["run"]["working-directory"] == AUTHSERVICE
    (job,) = workflow["jobs"].values()
    runs = [step.get("run", "") for step in job["steps"]]
    assert "python -m scripts.bar_index_check" in runs
    assert "services" not in job  # repository-only: no database


# --------------------------------------------------------- PostgreSQL job


@pytest.mark.parametrize(
    "path",
    [
        f"{AUTHSERVICE}/services/bar_registration_service.py",
        f"{AUTHSERVICE}/services/bar_identifier_service.py",
        f"{AUTHSERVICE}/services/bar_governed_registration.py",
        f"{AUTHSERVICE}/services/bar_reconciliation.py",
        f"{AUTHSERVICE}/repositories/bar_identifier_repository.py",
        f"{AUTHSERVICE}/models/bar_registration.py",
        f"{AUTHSERVICE}/tests/test_bar_postgres.py",
        f"{AUTHSERVICE}/tests/bar_governance_fixtures.py",
        f"{AUTHSERVICE}/alembic/versions/2026_09_22_1000-b8c9d0e1f2a3_bar_registration.py",
        f"{AUTHSERVICE}/requirements.txt",
        f"{AUTHSERVICE}/alembic/versions/2026_08_01_0900-a1b2c3d4e5f6_any_migration.py",
        f"{AUTHSERVICE}/alembic/env.py",
        f"{AUTHSERVICE}/alembic.ini",
    ],
)
def test_postgres_job_triggers_on_bar_code(path):
    assert _triggers(_load(POSTGRES_WORKFLOW), path)


def test_postgres_job_does_not_trigger_on_unrelated_paths():
    workflow = _load(POSTGRES_WORKFLOW)
    assert not _triggers(workflow, f"{AUTHSERVICE}/main.py")
    assert not _triggers(workflow, BAR_INDEX_RELATIVE_PATH.as_posix())


def test_postgres_job_uses_a_disposable_service_and_cannot_skip():
    workflow = _load(POSTGRES_WORKFLOW)
    (job,) = workflow["jobs"].values()
    assert job["services"]["postgres"]["image"] == "postgres:16"
    assert "volumes" not in job["services"]["postgres"]  # nothing persists between runs
    assert job["env"]["BAR_POSTGRES_REQUIRED"] == "1"
    assert job["env"]["BAR_POSTGRES_TEST_DATABASE_URL"].startswith("postgresql+asyncpg://")
    assert "BAR_POSTGRES_RUNTIME_ROLE_URL" not in job["env"]  # role separation is EP-02, not this job
    runs = " ".join(step.get("run", "") for step in job["steps"])
    assert "tests/test_bar_postgres.py" in runs


def test_postgres_job_migrates_a_separate_database_with_the_real_alembic_chain_before_testing():
    workflow = _load(POSTGRES_WORKFLOW)
    (job,) = workflow["jobs"].values()
    steps = job["steps"]
    models_url = job["env"]["BAR_POSTGRES_TEST_DATABASE_URL"]
    migrated_url = job["env"]["BAR_POSTGRES_MIGRATED_DATABASE_URL"]
    assert migrated_url.rsplit("/", 1)[0] == models_url.rsplit("/", 1)[0]  # same disposable service
    assert migrated_url != models_url  # but its own database
    migrated_db = migrated_url.rsplit("/", 1)[1]

    def index(predicate) -> int:
        return next(i for i, step in enumerate(steps) if predicate(step))

    create = index(lambda st: f"CREATE DATABASE {migrated_db}" in st.get("run", ""))
    migrate = index(lambda st: st.get("run", "").strip() == "alembic upgrade head")
    test = index(lambda st: "tests/test_bar_postgres.py" in st.get("run", ""))
    assert create < migrate < test
    assert steps[migrate]["env"]["DATABASE_URL"] == migrated_url  # alembic/env.py reads DATABASE_URL


def test_postgres_module_fails_instead_of_skipping_when_required(tmp_path):
    """What the CI job relies on: BAR_POSTGRES_REQUIRED=1 without a database is a failure, never a skip."""
    import os
    import subprocess
    import sys

    env = {k: v for k, v in os.environ.items() if not k.startswith("BAR_POSTGRES_")}
    env["BAR_POSTGRES_REQUIRED"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_bar_postgres.py", "-q", "-p", "no:cacheprovider"],
        cwd=DEFAULT_REPOSITORY_ROOT / AUTHSERVICE, env=env, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode != 0
    assert "BAR_POSTGRES_TEST_DATABASE_URL, BAR_POSTGRES_MIGRATED_DATABASE_URL is unset" in result.stdout


def test_postgres_module_requires_the_migrated_database_too():
    """A model-created database alone does not satisfy BAR_POSTGRES_REQUIRED=1."""
    import os
    import subprocess
    import sys

    env = {k: v for k, v in os.environ.items() if not k.startswith("BAR_POSTGRES_")}
    env["BAR_POSTGRES_REQUIRED"] = "1"
    env["BAR_POSTGRES_TEST_DATABASE_URL"] = "postgresql+asyncpg://unused@localhost:1/unused"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_bar_postgres.py", "-q", "-p", "no:cacheprovider"],
        cwd=DEFAULT_REPOSITORY_ROOT / AUTHSERVICE, env=env, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode != 0
    assert "BAR_POSTGRES_MIGRATED_DATABASE_URL is unset" in result.stdout
