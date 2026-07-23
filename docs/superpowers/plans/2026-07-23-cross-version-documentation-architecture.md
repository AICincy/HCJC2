# Cross-Version Documentation Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and migrate a controlled, human-readable documentation system spanning `AICincy/HCJC` and `AICincy/HCJC2`, with one HCJC2-owned canonical reference, mirrored version modules, stable reference identifiers, deterministic validation, and auditable V1-to-V2 traceability.

**Architecture:** HCJC2 owns the canonical concepts, registry, traceability generator, and current cross-version matrix. V1 stores its descriptive reference under `docs-reference/` so the generated GitHub Pages `docs/` tree remains untouched. Controlled Markdown files are authoritative; Python tooling parses YAML front matter and numbered headings to validate metadata, links, lifecycle, supersession, and relationships, then generates human-readable Markdown and JSON indexes.

**Tech Stack:** Python 3.13+, PyYAML 6.0.2, Pytest 9.1.1, Ruff 0.15.22, Markdown, JSON, Git, GitHub Actions.

## Global Constraints

- HCJC2 owns `docs/reference/HCJC-CANONICAL-REFERENCE.md` and the current reference registry and traceability matrix.
- V1 remains authoritative for implemented V1 behavior; V2 remains authoritative for V2 requirements and planned behavior.
- V1 controlled documentation lives under `docs-reference/`; never repurpose or rewrite the generated V1 `docs/` publication directory.
- Use the mirrored ten-family structure approved in the design specification.
- Use continuous human-readable namespaces: `A-`, `V1-`, `V2-`, `D-`, `S-`, `T-`, and `E-`.
- Only controlled sections and independently traceable critical rules receive numbered headings.
- Never renumber a published identifier, reuse a retired identifier, or infer identifiers automatically.
- Define shared meaning once in the canonical reference; version modules contain concise summaries and version-specific behavior.
- Every controlled document uses YAML front matter followed by a visible authority statement.
- Supporting research, audits, evidence, and historical files remain visibly non-authoritative.
- Canonical-reference releases use semantic versions and release dates.
- V1 pins the canonical-reference release and commit used for interpretation.
- Preserve legacy documents until every substantive section has an explicit migration disposition.
- Keep generated Markdown readable to humans; JSON sidecars support automation.
- Do not change V1 runtime behavior, production workflows, public data, booking photos, or generated site output as part of this documentation migration.
- Use test-first development for documentation tooling and validation rules.
- Commit after every independently reviewable task.

---

## File Structure Locked by This Plan

### HCJC2 files created or modified

```text
pyproject.toml
tools/__init__.py
tools/docsctl/__init__.py
tools/docsctl/__main__.py
tools/docsctl/cli.py
tools/docsctl/model.py
tools/docsctl/parser.py
tools/docsctl/links.py
tools/docsctl/validate.py
tools/docsctl/registry.py
tools/docsctl/traceability.py
tools/docsctl/snapshot.py
tools/docsctl/render.py

tests/docsctl/test_cli.py
tests/docsctl/test_parser.py
tests/docsctl/test_validate.py
tests/docsctl/test_registry.py
tests/docsctl/test_traceability.py
tests/docsctl/test_snapshot.py
tests/docsctl/fixtures/**

docs/MASTER-SPEC.md
docs/reference/HCJC-CANONICAL-REFERENCE.md
docs/reference/REFERENCE-REGISTRY.md
docs/reference/REFERENCE-REGISTRY.json
docs/reference/TRACEABILITY-MATRIX.md
docs/reference/TRACEABILITY-MATRIX.json
docs/reference/REFERENCE-RELEASES.md
docs/reference/reference-lock.json

docs/architecture/SYSTEM-ARCHITECTURE.md
docs/data/DATA-AND-SCHEMAS.md
docs/pipeline/ACQUISITION-AND-PUBLICATION.md
docs/correlations/CORRELATIONS.md
docs/taxonomy/OFFENSE-TAXONOMY.md
docs/product/PRODUCT-AND-UI-UX.md
docs/governance/PRIVACY-AND-LEGAL.md
docs/operations/OPERATIONS-AND-SECURITY.md
docs/quality/TESTING-AND-QUALITY.md
docs/migration/MIGRATION-AND-TRACEABILITY.md
docs/migration/LEGACY-DOCUMENT-MAPPING.md

docs/supporting/research/**
docs/supporting/evidence/**
docs/supporting/audits/**
docs/supporting/historical/**

.github/workflows/docs.yml
README
```

### V1 files created or modified

```text
docs-reference/MASTER-SPEC.md
docs-reference/architecture/SYSTEM-ARCHITECTURE.md
docs-reference/data/DATA-AND-SCHEMAS.md
docs-reference/pipeline/ACQUISITION-AND-PUBLICATION.md
docs-reference/correlations/CORRELATIONS.md
docs-reference/taxonomy/OFFENSE-TAXONOMY.md
docs-reference/product/PRODUCT-AND-UI-UX.md
docs-reference/governance/PRIVACY-AND-LEGAL.md
docs-reference/operations/OPERATIONS-AND-SECURITY.md
docs-reference/quality/TESTING-AND-QUALITY.md
docs-reference/migration/MIGRATION-AND-TRACEABILITY.md
docs-reference/migration/LEGACY-DOCUMENT-MAPPING.md
docs-reference/reference/TRACEABILITY-MATRIX-SNAPSHOT.md
docs-reference/reference/canonical-lock.json
docs-reference/supporting/research/**
docs-reference/supporting/evidence/**
docs-reference/supporting/audits/**
docs-reference/supporting/historical/**

.github/workflows/ci.yml
README.md
```

---

### Task 1: Bootstrap the HCJC2 Documentation Tooling Package

**Files:**
- Create: `pyproject.toml`
- Create: `tools/__init__.py`
- Create: `tools/docsctl/__init__.py`
- Create: `tools/docsctl/__main__.py`
- Create: `tools/docsctl/cli.py`
- Create: `tests/docsctl/test_cli.py`

**Interfaces:**
- Produces: `tools.docsctl.cli.main(argv: Sequence[str] | None = None) -> int`
- Produces CLI commands: `validate`, `registry`, `traceability`, `snapshot-v1`, `check`
- Later tasks may import `main` and invoke `python -m tools.docsctl`

- [ ] **Step 1: Write the failing CLI test**

```python
# tests/docsctl/test_cli.py
from tools.docsctl.cli import main


def test_help_lists_all_commands(capsys):
    result = main(["--help"])
    captured = capsys.readouterr()

    assert result == 0
    assert "validate" in captured.out
    assert "registry" in captured.out
    assert "traceability" in captured.out
    assert "snapshot-v1" in captured.out
    assert "check" in captured.out
```

- [ ] **Step 2: Run the test and verify the package is absent**

Run:

```bash
python -m pytest tests/docsctl/test_cli.py -v
```

Expected: collection fails with `ModuleNotFoundError: No module named 'tools'`.

- [ ] **Step 3: Create the packaging configuration**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "hcjc2-docs-tools"
version = "0.1.0"
description = "Validation and traceability tooling for HCJC and HCJC2 controlled documentation"
requires-python = ">=3.13"
dependencies = ["PyYAML==6.0.2"]

[project.optional-dependencies]
dev = ["pytest==9.1.1", "ruff==0.15.22"]

[project.scripts]
docsctl = "tools.docsctl.cli:main"

[tool.setuptools.packages.find]
include = ["tools*"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
target-version = "py313"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "B"]
ignore = ["E501"]
```

Create empty package files:

```python
# tools/__init__.py
```

```python
# tools/docsctl/__init__.py
"""Controlled documentation validation and generation tools."""
```

- [ ] **Step 4: Implement the CLI surface**

```python
# tools/docsctl/cli.py
from __future__ import annotations

import argparse
from collections.abc import Sequence


COMMANDS = ("validate", "registry", "traceability", "snapshot-v1", "check")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docsctl")
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    for command in COMMANDS:
        subparsers.add_parser(command)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    if args.command is None:
        parser.print_help()
    return 0
```

```python
# tools/docsctl/__main__.py
from tools.docsctl.cli import main

raise SystemExit(main())
```

- [ ] **Step 5: Run the focused test**

Run:

```bash
python -m pip install -e '.[dev]'
python -m pytest tests/docsctl/test_cli.py -v
```

Expected: `1 passed`.

- [ ] **Step 6: Run linting**

Run:

```bash
ruff check pyproject.toml tools tests/docsctl/test_cli.py
```

Expected: `All checks passed!`

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml tools tests/docsctl/test_cli.py
git commit -m "feat(docs): bootstrap documentation tooling"
```

---

### Task 2: Parse Controlled Metadata and Numbered Headings

**Files:**
- Create: `tools/docsctl/model.py`
- Create: `tools/docsctl/parser.py`
- Create: `tests/docsctl/test_parser.py`
- Create: `tests/docsctl/fixtures/valid-controlled.md`
- Create: `tests/docsctl/fixtures/invalid-frontmatter.md`

**Interfaces:**
- Produces: `parse_document(path: Path, repository: str) -> ParsedDocument`
- Produces: `github_anchor(value: str) -> str`
- Produces immutable models: `DocumentMetadata`, `ReferenceEntry`, `Relationship`, `ParsedDocument`
- Consumed by all validation and generation tasks

- [ ] **Step 1: Create the valid fixture**

```markdown
---
title: Correlations
reference_namespace: V2
status: approved
authority: v2-correlations
owner_repository: AICincy/HCJC2
document_family: correlations
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
  - from: V2-57
    relation: refines
    to: A-12
---

# Correlations

> **Authority:** Approved V2 correlation requirements.

## V2-57 Correlation Assessments

Supporting prose.

### Evidence classes
```

Save as `tests/docsctl/fixtures/valid-controlled.md`.

- [ ] **Step 2: Write parser tests**

```python
# tests/docsctl/test_parser.py
from pathlib import Path

import pytest

from tools.docsctl.model import DocumentStatus
from tools.docsctl.parser import FrontMatterError, github_anchor, parse_document


FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_document_returns_metadata_references_and_relationships():
    parsed = parse_document(FIXTURES / "valid-controlled.md", "AICincy/HCJC2")

    assert parsed.metadata.title == "Correlations"
    assert parsed.metadata.status is DocumentStatus.APPROVED
    assert parsed.metadata.owner_repository == "AICincy/HCJC2"
    assert [entry.code for entry in parsed.references] == ["V2-57"]
    assert parsed.references[0].anchor == "v2-57-correlation-assessments"
    assert parsed.relationships[0].source == "V2-57"
    assert parsed.relationships[0].relation == "refines"
    assert parsed.relationships[0].target == "A-12"


def test_github_anchor_is_stable_for_controlled_heading():
    assert github_anchor("V2-57 Correlation Assessments") == "v2-57-correlation-assessments"


def test_missing_closing_frontmatter_delimiter_fails(tmp_path):
    path = tmp_path / "broken.md"
    path.write_text("---\ntitle: Broken\n", encoding="utf-8")

    with pytest.raises(FrontMatterError, match="closing front matter delimiter"):
        parse_document(path, "AICincy/HCJC2")
```

- [ ] **Step 3: Run the tests and verify missing modules**

Run:

```bash
python -m pytest tests/docsctl/test_parser.py -v
```

Expected: collection fails because `tools.docsctl.model` and `tools.docsctl.parser` do not exist.

- [ ] **Step 4: Implement immutable models**

```python
# tools/docsctl/model.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class DocumentStatus(StrEnum):
    PROPOSED = "proposed"
    DRAFT = "draft"
    IN_REVIEW = "in-review"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    RETIRED = "retired"
    WITHDRAWN = "withdrawn"


@dataclass(frozen=True)
class CanonicalReference:
    version: str
    tag: str
    commit: str | None = None


@dataclass(frozen=True)
class DocumentMetadata:
    title: str
    reference_namespace: str
    status: DocumentStatus
    authority: str
    owner_repository: str
    document_family: str
    effective_date: str
    canonical_reference: CanonicalReference | None
    supersedes: tuple[str, ...] = ()
    superseded_by: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReferenceEntry:
    code: str
    title: str
    repository: str
    path: Path
    anchor: str
    status: DocumentStatus
    authority: str
    effective_date: str
    canonical_version: str | None


@dataclass(frozen=True)
class Relationship:
    source: str
    relation: str
    target: str


@dataclass(frozen=True)
class ParsedDocument:
    path: Path
    metadata: DocumentMetadata
    references: tuple[ReferenceEntry, ...]
    relationships: tuple[Relationship, ...]
    markdown: str
```

- [ ] **Step 5: Implement the parser**

```python
# tools/docsctl/parser.py
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from tools.docsctl.model import (
    CanonicalReference,
    DocumentMetadata,
    DocumentStatus,
    ParsedDocument,
    ReferenceEntry,
    Relationship,
)


CONTROLLED_HEADING_RE = re.compile(
    r"^(?P<marks>#{2,6}) (?P<code>(?:A|V1|V2|D|S|T|E)-[1-9][0-9]*) (?P<title>\S.*)$"
)


class FrontMatterError(ValueError):
    pass


def github_anchor(value: str) -> str:
    lowered = value.strip().lower()
    without_punctuation = re.sub(r"[^a-z0-9\s-]", "", lowered)
    return re.sub(r"[\s-]+", "-", without_punctuation).strip("-")


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise FrontMatterError("document must begin with YAML front matter")
    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError as exc:
        raise FrontMatterError("document is missing the closing front matter delimiter") from exc
    metadata = yaml.safe_load("\n".join(lines[1:closing_index])) or {}
    if not isinstance(metadata, dict):
        raise FrontMatterError("front matter must decode to a mapping")
    markdown = "\n".join(lines[closing_index + 1 :]) + "\n"
    return metadata, markdown


def _canonical_reference(raw: object) -> CanonicalReference | None:
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise FrontMatterError("canonical_reference must be a mapping")
    return CanonicalReference(
        version=str(raw["version"]),
        tag=str(raw["tag"]),
        commit=str(raw["commit"]) if raw.get("commit") else None,
    )


def parse_document(path: Path, repository: str) -> ParsedDocument:
    raw_metadata, markdown = _split_front_matter(path.read_text(encoding="utf-8"))
    metadata = DocumentMetadata(
        title=str(raw_metadata["title"]),
        reference_namespace=str(raw_metadata["reference_namespace"]),
        status=DocumentStatus(str(raw_metadata["status"])),
        authority=str(raw_metadata["authority"]),
        owner_repository=str(raw_metadata["owner_repository"]),
        document_family=str(raw_metadata["document_family"]),
        effective_date=str(raw_metadata["effective_date"]),
        canonical_reference=_canonical_reference(raw_metadata.get("canonical_reference")),
        supersedes=tuple(str(item) for item in raw_metadata.get("supersedes", [])),
        superseded_by=(str(raw_metadata["superseded_by"]) if raw_metadata.get("superseded_by") else None),
        raw=raw_metadata,
    )

    references: list[ReferenceEntry] = []
    for line in markdown.splitlines():
        match = CONTROLLED_HEADING_RE.match(line)
        if match is None:
            continue
        code = match.group("code")
        title = match.group("title").strip()
        references.append(
            ReferenceEntry(
                code=code,
                title=title,
                repository=repository,
                path=path,
                anchor=github_anchor(f"{code} {title}"),
                status=metadata.status,
                authority=metadata.authority,
                effective_date=metadata.effective_date,
                canonical_version=(metadata.canonical_reference.version if metadata.canonical_reference else None),
            )
        )

    relationships = tuple(
        Relationship(source=str(item["from"]), relation=str(item["relation"]), target=str(item["to"]))
        for item in raw_metadata.get("relationships", [])
    )
    return ParsedDocument(
        path=path,
        metadata=metadata,
        references=tuple(references),
        relationships=relationships,
        markdown=markdown,
    )
```

- [ ] **Step 6: Run parser tests**

Run:

```bash
python -m pytest tests/docsctl/test_parser.py -v
```

Expected: `3 passed`.

- [ ] **Step 7: Commit**

```bash
git add tools/docsctl/model.py tools/docsctl/parser.py tests/docsctl/test_parser.py tests/docsctl/fixtures
git commit -m "feat(docs): parse controlled documentation"
```

---

### Task 3: Validate Metadata, Identifiers, Links, and Supersession

**Files:**
- Create: `tools/docsctl/links.py`
- Create: `tools/docsctl/validate.py`
- Modify: `tools/docsctl/cli.py`
- Create: `tests/docsctl/test_validate.py`
- Create fixtures under: `tests/docsctl/fixtures/validation/`

**Interfaces:**
- Consumes: `parse_document()`
- Produces: `ValidationIssue(code: str, message: str, path: Path, severity: Severity)`
- Produces: `validate_documents(documents: Sequence[ParsedDocument], root: Path) -> list[ValidationIssue]`
- Produces: `discover_controlled_documents(root: Path) -> tuple[Path, ...]`

- [ ] **Step 1: Write failing validation tests**

```python
# tests/docsctl/test_validate.py
from pathlib import Path

from tools.docsctl.model import ParsedDocument
from tools.docsctl.parser import parse_document
from tools.docsctl.validate import validate_documents


FIXTURES = Path(__file__).parent / "fixtures" / "validation"


def _parse(name: str) -> ParsedDocument:
    return parse_document(FIXTURES / name, "AICincy/HCJC2")


def test_duplicate_reference_codes_fail():
    issues = validate_documents([_parse("duplicate-a.md"), _parse("duplicate-b.md")], FIXTURES)

    assert any(issue.code == "duplicate-reference" and issue.severity == "error" for issue in issues)


def test_superseded_document_requires_replacement():
    issues = validate_documents([_parse("superseded-without-replacement.md")], FIXTURES)

    assert any(issue.code == "missing-superseded-by" for issue in issues)


def test_unknown_relationship_target_fails():
    issues = validate_documents([_parse("unknown-target.md")], FIXTURES)

    assert any(issue.code == "unknown-reference" and "A-999" in issue.message for issue in issues)
```

Create the three fixtures with valid front matter and the exact fault named by each test. Use `V2-1` in both duplicate fixtures, `status: superseded` with `superseded_by: null` in the second fixture, and a relationship to `A-999` in the third fixture.

- [ ] **Step 2: Run tests and verify missing validator modules**

Run:

```bash
python -m pytest tests/docsctl/test_validate.py -v
```

Expected: collection fails because `tools.docsctl.validate` does not exist.

- [ ] **Step 3: Implement link extraction and local-link validation**

```python
# tools/docsctl/links.py
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from tools.docsctl.parser import github_anchor


MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\((?P<target>[^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6} (?P<title>.+)$")


@dataclass(frozen=True)
class LinkProblem:
    target: str
    message: str


def _anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if match:
            anchors.add(github_anchor(match.group("title")))
    return anchors


def validate_local_links(path: Path, root: Path) -> list[LinkProblem]:
    problems: list[LinkProblem] = []
    text = path.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group("target").strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        location, _, fragment = target.partition("#")
        destination = path if location == "" else (path.parent / unquote(location)).resolve()
        try:
            destination.relative_to(root.resolve())
        except ValueError:
            problems.append(LinkProblem(target, "link escapes the repository root"))
            continue
        if not destination.exists():
            problems.append(LinkProblem(target, "linked file does not exist"))
            continue
        if fragment and destination.suffix.lower() == ".md" and fragment not in _anchors(destination):
            problems.append(LinkProblem(target, f"anchor #{fragment} does not exist"))
    return problems
```

- [ ] **Step 4: Implement validation rules**

```python
# tools/docsctl/validate.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Sequence

from tools.docsctl.links import validate_local_links
from tools.docsctl.model import DocumentStatus, ParsedDocument


Severity = Literal["warning", "error"]
ALLOWED_RELATIONS = {
    "defines",
    "implements",
    "requires",
    "refines",
    "replaces",
    "preserves",
    "verifies",
    "produces-evidence-for",
    "supersedes",
    "maps-to",
    "accepted-difference-from",
    "depends-on",
    "constrained-by",
    "historical-reference",
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    path: Path
    severity: Severity


def discover_controlled_documents(root: Path) -> tuple[Path, ...]:
    candidates = [
        *root.glob("docs/**/*.md"),
        *root.glob("docs-reference/**/*.md"),
    ]
    return tuple(sorted(path for path in candidates if "/supporting/" not in path.as_posix()))


def _supersession_cycles(documents: Sequence[ParsedDocument]) -> set[str]:
    edges = {
        entry.code: document.metadata.superseded_by
        for document in documents
        for entry in document.references
        if document.metadata.superseded_by
    }
    cyclic: set[str] = set()
    for start in edges:
        seen: set[str] = set()
        current: str | None = start
        while current in edges:
            if current in seen:
                cyclic.update(seen)
                break
            seen.add(current)
            current = edges[current]
    return cyclic


def validate_documents(documents: Sequence[ParsedDocument], root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    by_code: dict[str, list[tuple[ParsedDocument, object]]] = {}
    for document in documents:
        if document.metadata.owner_repository not in {"AICincy/HCJC", "AICincy/HCJC2"}:
            issues.append(
                ValidationIssue(
                    "invalid-owner",
                    f"unsupported owner_repository: {document.metadata.owner_repository}",
                    document.path,
                    "error",
                )
            )
        if document.metadata.status is DocumentStatus.SUPERSEDED and not document.metadata.superseded_by:
            issues.append(
                ValidationIssue(
                    "missing-superseded-by",
                    "superseded documents require superseded_by",
                    document.path,
                    "error",
                )
            )
        for entry in document.references:
            by_code.setdefault(entry.code, []).append((document, entry))
        for problem in validate_local_links(document.path, root):
            issues.append(ValidationIssue("broken-link", f"{problem.target}: {problem.message}", document.path, "error"))

    for code, occurrences in by_code.items():
        if len(occurrences) > 1:
            for document, _entry in occurrences:
                issues.append(ValidationIssue("duplicate-reference", f"duplicate reference code: {code}", document.path, "error"))

    known = set(by_code)
    for document in documents:
        for relationship in document.relationships:
            if relationship.relation not in ALLOWED_RELATIONS:
                issues.append(
                    ValidationIssue(
                        "invalid-relation",
                        f"unsupported relationship: {relationship.relation}",
                        document.path,
                        "error",
                    )
                )
            for code in (relationship.source, relationship.target):
                if code not in known:
                    issues.append(ValidationIssue("unknown-reference", f"unknown reference: {code}", document.path, "error"))

    for code in _supersession_cycles(documents):
        document, _entry = by_code[code][0]
        issues.append(ValidationIssue("supersession-cycle", f"supersession cycle includes {code}", document.path, "error"))
    return sorted(issues, key=lambda item: (item.path.as_posix(), item.code, item.message))
```

- [ ] **Step 5: Wire the `validate` command**

Update `tools/docsctl/cli.py` so every command accepts `--repo-root` and `--repository`, then implement validation:

```python
from pathlib import Path

from tools.docsctl.parser import parse_document
from tools.docsctl.validate import discover_controlled_documents, validate_documents


def _add_repository_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository", required=True)


def _run_validate(repo_root: Path, repository: str) -> int:
    documents = [parse_document(path, repository) for path in discover_controlled_documents(repo_root)]
    issues = validate_documents(documents, repo_root)
    for issue in issues:
        print(f"{issue.severity}: {issue.path}: {issue.code}: {issue.message}")
    return 1 if any(issue.severity == "error" for issue in issues) else 0
```

Dispatch `validate` to `_run_validate()`.

- [ ] **Step 6: Run validation tests**

Run:

```bash
python -m pytest tests/docsctl/test_validate.py -v
```

Expected: `3 passed`.

- [ ] **Step 7: Commit**

```bash
git add tools/docsctl/links.py tools/docsctl/validate.py tools/docsctl/cli.py tests/docsctl/test_validate.py tests/docsctl/fixtures/validation
git commit -m "feat(docs): validate controlled references"
```

---

### Task 4: Generate the Reference Registry and Detailed Traceability Matrix

**Files:**
- Create: `tools/docsctl/render.py`
- Create: `tools/docsctl/registry.py`
- Create: `tools/docsctl/traceability.py`
- Modify: `tools/docsctl/cli.py`
- Create: `tests/docsctl/test_registry.py`
- Create: `tests/docsctl/test_traceability.py`

**Interfaces:**
- Produces: `build_registry(documents) -> tuple[ReferenceEntry, ...]`
- Produces: `render_registry_markdown(entries, root) -> str`
- Produces: `render_registry_json(entries, root) -> str`
- Produces: `build_traceability(documents) -> tuple[TraceabilityRow, ...]`
- Produces deterministic Markdown and JSON outputs

- [ ] **Step 1: Write failing deterministic-output tests**

```python
# tests/docsctl/test_registry.py
import json
from pathlib import Path

from tools.docsctl.parser import parse_document
from tools.docsctl.registry import build_registry, render_registry_json, render_registry_markdown


FIXTURE = Path(__file__).parent / "fixtures" / "valid-controlled.md"


def test_registry_is_sorted_and_renders_stable_outputs(tmp_path):
    document = parse_document(FIXTURE, "AICincy/HCJC2")
    entries = build_registry([document])

    markdown = render_registry_markdown(entries, tmp_path)
    payload = json.loads(render_registry_json(entries, tmp_path))

    assert "| V2-57 | Correlation Assessments |" in markdown
    assert payload[0]["reference"] == "V2-57"
```

```python
# tests/docsctl/test_traceability.py
from pathlib import Path

from tools.docsctl.parser import parse_document
from tools.docsctl.traceability import build_traceability, render_traceability_markdown


FIXTURE = Path(__file__).parent / "fixtures" / "valid-controlled.md"


def test_traceability_preserves_explicit_relationship_meaning():
    document = parse_document(FIXTURE, "AICincy/HCJC2")
    rows = build_traceability([document])

    assert rows[0].source == "V2-57"
    assert rows[0].relation == "refines"
    assert rows[0].target == "A-12"
    assert "| V2-57 | refines | A-12 |" in render_traceability_markdown(rows)
```

- [ ] **Step 2: Run tests and verify missing generator modules**

Run:

```bash
python -m pytest tests/docsctl/test_registry.py tests/docsctl/test_traceability.py -v
```

Expected: collection fails because registry and traceability modules do not exist.

- [ ] **Step 3: Implement deterministic sorting and rendering**

```python
# tools/docsctl/render.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


NAMESPACE_ORDER = {"A": 0, "V1": 1, "V2": 2, "D": 3, "S": 4, "T": 5, "E": 6}


def reference_sort_key(code: str) -> tuple[int, int]:
    namespace, number = code.split("-", 1)
    return NAMESPACE_ORDER[namespace], int(number)


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
```

```python
# tools/docsctl/registry.py
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from tools.docsctl.model import ParsedDocument, ReferenceEntry
from tools.docsctl.render import json_text, reference_sort_key, relative_path


def build_registry(documents: Sequence[ParsedDocument]) -> tuple[ReferenceEntry, ...]:
    return tuple(sorted((entry for document in documents for entry in document.references), key=lambda item: reference_sort_key(item.code)))


def render_registry_markdown(entries: Sequence[ReferenceEntry], root: Path) -> str:
    lines = [
        "# Reference Registry",
        "",
        "> Generated from controlled Markdown. Do not edit manually.",
        "",
        "| Reference | Title | Repository | Document | Status | Authority | Effective date | Canonical version |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for entry in entries:
        document = relative_path(entry.path, root)
        link = f"[{entry.code}](../{document}#{entry.anchor})"
        lines.append(
            f"| {link} | {entry.title} | {entry.repository} | `{document}` | {entry.status.value} | {entry.authority} | {entry.effective_date} | {entry.canonical_version or ''} |"
        )
    return "\n".join(lines) + "\n"


def render_registry_json(entries: Sequence[ReferenceEntry], root: Path) -> str:
    return json_text(
        [
            {
                "reference": entry.code,
                "title": entry.title,
                "repository": entry.repository,
                "document": relative_path(entry.path, root),
                "anchor": entry.anchor,
                "status": entry.status.value,
                "authority": entry.authority,
                "effective_date": entry.effective_date,
                "canonical_version": entry.canonical_version,
            }
            for entry in entries
        ]
    )
```

```python
# tools/docsctl/traceability.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from tools.docsctl.model import ParsedDocument
from tools.docsctl.render import json_text, reference_sort_key


@dataclass(frozen=True)
class TraceabilityRow:
    source: str
    relation: str
    target: str


def build_traceability(documents: Sequence[ParsedDocument]) -> tuple[TraceabilityRow, ...]:
    rows = {
        TraceabilityRow(relationship.source, relationship.relation, relationship.target)
        for document in documents
        for relationship in document.relationships
    }
    return tuple(sorted(rows, key=lambda row: (reference_sort_key(row.source), row.relation, reference_sort_key(row.target))))


def render_traceability_markdown(rows: Sequence[TraceabilityRow]) -> str:
    lines = [
        "# Traceability Matrix",
        "",
        "> Generated from controlled Markdown relationships. Do not edit manually.",
        "",
        "| Source | Relationship | Target |",
        "|---|---|---|",
    ]
    lines.extend(f"| {row.source} | {row.relation} | {row.target} |" for row in rows)
    return "\n".join(lines) + "\n"


def render_traceability_json(rows: Sequence[TraceabilityRow]) -> str:
    return json_text([{"source": row.source, "relationship": row.relation, "target": row.target} for row in rows])
```

- [ ] **Step 4: Add generator commands**

Implement `registry` and `traceability` in `tools/docsctl/cli.py` with these exact defaults:

```text
registry Markdown: docs/reference/REFERENCE-REGISTRY.md
registry JSON:     docs/reference/REFERENCE-REGISTRY.json
matrix Markdown:   docs/reference/TRACEABILITY-MATRIX.md
matrix JSON:       docs/reference/TRACEABILITY-MATRIX.json
```

Each command parses controlled documents, fails on validation errors, writes both outputs, and prints the written paths.

- [ ] **Step 5: Run tests**

Run:

```bash
python -m pytest tests/docsctl/test_registry.py tests/docsctl/test_traceability.py -v
```

Expected: `2 passed`.

- [ ] **Step 6: Commit**

```bash
git add tools/docsctl/render.py tools/docsctl/registry.py tools/docsctl/traceability.py tools/docsctl/cli.py tests/docsctl/test_registry.py tests/docsctl/test_traceability.py
git commit -m "feat(docs): generate registry and traceability"
```

---

### Task 5: Generate a Pinned V1 Traceability Snapshot

**Files:**
- Create: `tools/docsctl/snapshot.py`
- Modify: `tools/docsctl/cli.py`
- Create: `tests/docsctl/test_snapshot.py`

**Interfaces:**
- Produces: `render_v1_snapshot(rows, metadata: SnapshotMetadata) -> str`
- CLI command requires exact canonical version, tag, canonical commit, V1 commit, and output path

- [ ] **Step 1: Write the failing snapshot test**

```python
# tests/docsctl/test_snapshot.py
from tools.docsctl.snapshot import SnapshotMetadata, render_v1_snapshot
from tools.docsctl.traceability import TraceabilityRow


def test_v1_snapshot_records_exact_pins():
    text = render_v1_snapshot(
        [TraceabilityRow("V1-1", "implements", "A-1")],
        SnapshotMetadata(
            canonical_version="1.0.0",
            canonical_tag="reference-v1.0.0",
            canonical_commit="abc123",
            v1_commit="def456",
            generated_date="2026-07-23",
            generator_version="0.1.0",
        ),
    )

    assert "canonical_commit: abc123" in text
    assert "v1_commit: def456" in text
    assert "| V1-1 | implements | A-1 |" in text
```

- [ ] **Step 2: Run the test and verify the module is absent**

Run:

```bash
python -m pytest tests/docsctl/test_snapshot.py -v
```

Expected: collection fails because `tools.docsctl.snapshot` does not exist.

- [ ] **Step 3: Implement snapshot rendering**

```python
# tools/docsctl/snapshot.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from tools.docsctl.traceability import TraceabilityRow, render_traceability_markdown


@dataclass(frozen=True)
class SnapshotMetadata:
    canonical_version: str
    canonical_tag: str
    canonical_commit: str
    v1_commit: str
    generated_date: str
    generator_version: str


def render_v1_snapshot(rows: Sequence[TraceabilityRow], metadata: SnapshotMetadata) -> str:
    body = render_traceability_markdown(rows).replace("# Traceability Matrix", "# V1 Traceability Matrix Snapshot", 1)
    front_matter = "\n".join(
        [
            "---",
            "title: V1 Traceability Matrix Snapshot",
            "status: approved",
            "authority: v1-traceability-snapshot",
            "owner_repository: AICincy/HCJC",
            "document_family: reference",
            f"effective_date: {metadata.generated_date}",
            "canonical_reference:",
            f"  version: {metadata.canonical_version}",
            f"  tag: {metadata.canonical_tag}",
            f"  commit: {metadata.canonical_commit}",
            f"v1_commit: {metadata.v1_commit}",
            f"generator_version: {metadata.generator_version}",
            "supersedes: []",
            "superseded_by: null",
            "---",
            "",
        ]
    )
    return front_matter + body
```

- [ ] **Step 4: Implement the CLI command**

Add required `snapshot-v1` arguments:

```text
--repo-root
--repository
--output
--canonical-version
--canonical-tag
--canonical-commit
--v1-commit
--generated-date
```

Filter the generated rows to relationships containing at least one `V1-` endpoint, then write the snapshot.

- [ ] **Step 5: Run the focused test**

Run:

```bash
python -m pytest tests/docsctl/test_snapshot.py -v
```

Expected: `1 passed`.

- [ ] **Step 6: Commit**

```bash
git add tools/docsctl/snapshot.py tools/docsctl/cli.py tests/docsctl/test_snapshot.py
git commit -m "feat(docs): generate pinned V1 traceability snapshots"
```

---

### Task 6: Create the HCJC2 Controlled Documentation Skeleton

**Files:**
- Create the ten controlled modules and reference files listed in the locked file structure
- Create: `tests/docsctl/test_hcjc2_layout.py`
- Modify: `README`

**Interfaces:**
- Produces the authoritative HCJC2 documentation entry points expected by tooling and later migration tasks
- Every new controlled document begins in `draft` except the already approved design specification

- [ ] **Step 1: Write the failing layout test**

```python
# tests/docsctl/test_hcjc2_layout.py
from pathlib import Path


EXPECTED = {
    "docs/MASTER-SPEC.md",
    "docs/reference/HCJC-CANONICAL-REFERENCE.md",
    "docs/reference/REFERENCE-RELEASES.md",
    "docs/architecture/SYSTEM-ARCHITECTURE.md",
    "docs/data/DATA-AND-SCHEMAS.md",
    "docs/pipeline/ACQUISITION-AND-PUBLICATION.md",
    "docs/correlations/CORRELATIONS.md",
    "docs/taxonomy/OFFENSE-TAXONOMY.md",
    "docs/product/PRODUCT-AND-UI-UX.md",
    "docs/governance/PRIVACY-AND-LEGAL.md",
    "docs/operations/OPERATIONS-AND-SECURITY.md",
    "docs/quality/TESTING-AND-QUALITY.md",
    "docs/migration/MIGRATION-AND-TRACEABILITY.md",
    "docs/migration/LEGACY-DOCUMENT-MAPPING.md",
}


def test_hcjc2_controlled_document_layout_exists():
    missing = sorted(path for path in EXPECTED if not Path(path).is_file())
    assert missing == []
```

- [ ] **Step 2: Run the test and verify the files are missing**

Run:

```bash
python -m pytest tests/docsctl/test_hcjc2_layout.py -v
```

Expected: failure listing all missing controlled files.

- [ ] **Step 3: Create every directory**

Run:

```bash
mkdir -p \
  docs/reference \
  docs/architecture \
  docs/data \
  docs/pipeline \
  docs/correlations \
  docs/taxonomy \
  docs/product \
  docs/governance \
  docs/operations \
  docs/quality \
  docs/migration \
  docs/supporting/{research,evidence,audits,historical}
```

- [ ] **Step 4: Create `docs/MASTER-SPEC.md` with exact initial content**

```markdown
---
title: HCJC2 Master Specification
reference_namespace: V2
status: draft
authority: v2-master
owner_repository: AICincy/HCJC2
document_family: master
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

# HCJC2 Master Specification

> **Authority:** Draft controlling entry point for HCJC2 scope, critical invariants, document ownership, and production-readiness boundaries. Detailed requirements belong to the linked controlled modules.

## System identity

HCJC2 is the greenfield successor to JCStream. V1 remains the production and behavioral reference during migration.

## Critical invariants

- Correlations remain required and must be materially enhanced.
- Missing legal facts remain unresolved.
- Failed or partial acquisition does not advance.
- Application deployment and data publication remain separate.
- Accessibility, privacy, provenance, correction, rollback, and verification are release gates.

## Controlled modules

1. [System Architecture](architecture/SYSTEM-ARCHITECTURE.md)
2. [Data and Schemas](data/DATA-AND-SCHEMAS.md)
3. [Acquisition and Publication](pipeline/ACQUISITION-AND-PUBLICATION.md)
4. [Correlations](correlations/CORRELATIONS.md)
5. [Offense Taxonomy](taxonomy/OFFENSE-TAXONOMY.md)
6. [Product and UI/UX](product/PRODUCT-AND-UI-UX.md)
7. [Privacy and Legal](governance/PRIVACY-AND-LEGAL.md)
8. [Operations and Security](operations/OPERATIONS-AND-SECURITY.md)
9. [Testing and Quality](quality/TESTING-AND-QUALITY.md)
10. [Migration and Traceability](migration/MIGRATION-AND-TRACEABILITY.md)

## Shared reference

See [HCJC Canonical Reference](reference/HCJC-CANONICAL-REFERENCE.md).
```

- [ ] **Step 5: Create the ten module files from an exact manifest**

Run this script from the HCJC2 repository root:

```bash
python - <<'PY_MODULES'
from pathlib import Path

modules = {
    "docs/architecture/SYSTEM-ARCHITECTURE.md": (
        "System Architecture",
        "v2-architecture",
        "architecture",
        "Controls V2 system boundaries, components, dependencies, runtime topology, and architectural invariants.",
    ),
    "docs/data/DATA-AND-SCHEMAS.md": (
        "Data and Schemas",
        "v2-data",
        "data",
        "Controls V2 entities, identifiers, fields, schema families, serialization, and compatibility.",
    ),
    "docs/pipeline/ACQUISITION-AND-PUBLICATION.md": (
        "Acquisition and Publication",
        "v2-pipeline",
        "pipeline",
        "Controls V2 acquisition, validation, candidate releases, publication, promotion, and rollback.",
    ),
    "docs/correlations/CORRELATIONS.md": (
        "Correlations",
        "v2-correlations",
        "correlations",
        "Controls V2 relationship families, evidence, scoring, competition, review, publication, and disputes.",
    ),
    "docs/taxonomy/OFFENSE-TAXONOMY.md": (
        "Offense Taxonomy",
        "v2-taxonomy",
        "taxonomy",
        "Controls V2 charge observations, authority records, concepts, assessments, and unresolved classifications.",
    ),
    "docs/product/PRODUCT-AND-UI-UX.md": (
        "Product and UI/UX",
        "v2-product",
        "product",
        "Controls V2 product behavior, routes, information architecture, visual design, interaction design, and accessibility.",
    ),
    "docs/governance/PRIVACY-AND-LEGAL.md": (
        "Privacy and Legal",
        "v2-governance",
        "governance",
        "Controls V2 privacy boundaries, legal language, correction, removal, dispute, and public-use restrictions.",
    ),
    "docs/operations/OPERATIONS-AND-SECURITY.md": (
        "Operations and Security",
        "v2-operations",
        "operations",
        "Controls V2 credentials, automation, observability, deployment operations, incident response, and security.",
    ),
    "docs/quality/TESTING-AND-QUALITY.md": (
        "Testing and Quality",
        "v2-quality",
        "quality",
        "Controls V2 test layers, quality gates, accessibility, security, privacy, resilience, and reproducibility.",
    ),
    "docs/migration/MIGRATION-AND-TRACEABILITY.md": (
        "Migration and Traceability",
        "v2-migration",
        "migration",
        "Controls V2 parity, accepted differences, shadow operation, cutover, rollback, stabilization, and V1 retirement.",
    ),
}

for raw_path, (title, authority, family, authority_statement) in modules.items():
    path = Path(raw_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
title: {title}
reference_namespace: V2
status: draft
authority: {authority}
owner_repository: AICincy/HCJC2
document_family: {family}
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

# {title}

> **Authority:** {authority_statement}

## Scope

## Controlled rules

## Related decisions, schemas, tests, and evidence

## Supporting material
""",
        encoding="utf-8",
    )
PY_MODULES
```

- [ ] **Step 6: Create reference release and migration ledgers**

Create `docs/reference/REFERENCE-RELEASES.md` and `docs/migration/LEGACY-DOCUMENT-MAPPING.md` with valid front matter, visible authority statements, and empty approved tables that later tasks will populate.

- [ ] **Step 7: Update the HCJC2 README**

Replace the contradictory correlation restriction with this compact orientation:

```markdown
# HCJC2

HCJC2 is the greenfield successor to JCStream, the public Hamilton County, Ohio Justice Center custody-data system.

## Status

- Phase: documentation architecture and contract migration
- Production reference: `AICincy/HCJC`
- V2 repository: `AICincy/HCJC2`
- V1 change policy: emergency fixes only

## Documentation authority

- [Master Specification](docs/MASTER-SPEC.md)
- [Canonical Cross-Version Reference](docs/reference/HCJC-CANONICAL-REFERENCE.md)
- [Reference Registry](docs/reference/REFERENCE-REGISTRY.md)
- [Traceability Matrix](docs/reference/TRACEABILITY-MATRIX.md)

## Controlled modules

1. [System Architecture](docs/architecture/SYSTEM-ARCHITECTURE.md)
2. [Data and Schemas](docs/data/DATA-AND-SCHEMAS.md)
3. [Acquisition and Publication](docs/pipeline/ACQUISITION-AND-PUBLICATION.md)
4. [Correlations](docs/correlations/CORRELATIONS.md)
5. [Offense Taxonomy](docs/taxonomy/OFFENSE-TAXONOMY.md)
6. [Product and UI/UX](docs/product/PRODUCT-AND-UI-UX.md)
7. [Privacy and Legal](docs/governance/PRIVACY-AND-LEGAL.md)
8. [Operations and Security](docs/operations/OPERATIONS-AND-SECURITY.md)
9. [Testing and Quality](docs/quality/TESTING-AND-QUALITY.md)
10. [Migration and Traceability](docs/migration/MIGRATION-AND-TRACEABILITY.md)
```

- [ ] **Step 8: Run the layout and validator tests**

Run:

```bash
python -m pytest tests/docsctl/test_hcjc2_layout.py -v
python -m tools.docsctl validate --repo-root . --repository AICincy/HCJC2
```

Expected: layout passes. Validation returns zero errors for the new controlled files.

- [ ] **Step 9: Commit**

```bash
git add README docs tests/docsctl/test_hcjc2_layout.py
git commit -m "docs: establish HCJC2 controlled documentation structure"
```

---

### Task 7: Publish Canonical Entries A-1 Through A-12

**Files:**
- Modify: `docs/reference/HCJC-CANONICAL-REFERENCE.md`
- Create: `tests/docsctl/test_canonical_reference.py`

**Interfaces:**
- Produces the first shared concepts used by both V1 and V2 modules
- Later tasks may cite these identifiers without redefining them

- [ ] **Step 1: Write the failing canonical-entry test**

```python
# tests/docsctl/test_canonical_reference.py
from pathlib import Path

from tools.docsctl.parser import parse_document


EXPECTED = {
    "A-1",
    "A-2",
    "A-3",
    "A-4",
    "A-5",
    "A-6",
    "A-7",
    "A-8",
    "A-9",
    "A-10",
    "A-11",
    "A-12",
}


def test_initial_canonical_identity_and_record_entries_exist():
    document = parse_document(Path("docs/reference/HCJC-CANONICAL-REFERENCE.md"), "AICincy/HCJC2")
    assert EXPECTED <= {entry.code for entry in document.references}
```

- [ ] **Step 2: Run the test and verify the entries are absent**

Run:

```bash
python -m pytest tests/docsctl/test_canonical_reference.py -v
```

Expected: failure because the canonical reference has no numbered entries.

- [ ] **Step 3: Add exact entries A-1 through A-12**

Use these titles and definitions:

| Code | Title | Definition |
|---|---|---|
| A-1 | Source System | A public or approved private system from which HCJC or HCJC2 obtains an observation, reference, or operational signal. |
| A-2 | Source Observation | An immutable representation of what a source reported at a specific observation time, before project interpretation changes its meaning. |
| A-3 | Canonical Record | A normalized project record derived from one or more source observations under a versioned transformation contract. |
| A-4 | Current Roster | The latest approved collection of custody records representing individuals listed by the authoritative roster source at its observation time. |
| A-5 | Person Reference | A project-scoped reference used to associate records with a person without asserting that a source identifier is universally unique. |
| A-6 | Custody Record | A record describing a source-reported state of custody, booking, charge, court, bond, holder, or release information. |
| A-7 | Custody Episode | A continuous period of custody associated with one person reference and one or more source observations. |
| A-8 | Booking Event | A dated event representing entry into a custody episode or the first approved observation of that entry. |
| A-9 | Release Event | A dated event representing departure from a custody episode or the first approved observation of that departure. |
| A-10 | Material Change Event | A dated event representing a significant approved change to a custody record that is neither a booking nor a release. |
| A-11 | Source Identifier | An identifier assigned by a source system and interpreted only within the scope documented for that source. |
| A-12 | Project Identifier | A versioned identifier assigned by the project for a defined record type, lifecycle, and collision domain. |

Each entry must use this exact structure:

```markdown
## A-1 Source System

**Definition:** A public or approved private system from which HCJC or HCJC2 obtains an observation, reference, or operational signal.

**V1 interpretation:** V1 acquires the HCSO roster and approved public feeds through implemented source-specific clients.

**V2 interpretation:** V2 requires every source system to be registered with an explicit owner, contract, freshness policy, and public-data classification.

**Related references:** Version-specific links are added when their controlled entries are assigned.
```

Apply the same four-paragraph structure to A-2 through A-12 with concise V1 and V2 interpretation sentences grounded in the approved V1 and V2 specifications.

- [ ] **Step 4: Run tests and validation**

Run:

```bash
python -m pytest tests/docsctl/test_canonical_reference.py -v
python -m tools.docsctl validate --repo-root . --repository AICincy/HCJC2
```

Expected: both pass.

- [ ] **Step 5: Commit**

```bash
git add docs/reference/HCJC-CANONICAL-REFERENCE.md tests/docsctl/test_canonical_reference.py
git commit -m "docs: define canonical identity and record concepts"
```

---

### Task 8: Publish Canonical Entries A-13 Through A-24

**Files:**
- Modify: `docs/reference/HCJC-CANONICAL-REFERENCE.md`
- Modify: `tests/docsctl/test_canonical_reference.py`

**Interfaces:**
- Adds shared release, status, provenance, and artifact vocabulary

- [ ] **Step 1: Extend the test with A-13 through A-24**

Add these identifiers to `EXPECTED`:

```python
{
    "A-13", "A-14", "A-15", "A-16", "A-17", "A-18",
    "A-19", "A-20", "A-21", "A-22", "A-23", "A-24",
}
```

- [ ] **Step 2: Run the test and verify the new entries are absent**

Run:

```bash
python -m pytest tests/docsctl/test_canonical_reference.py -v
```

Expected: failure listing missing A-13 through A-24.

- [ ] **Step 3: Add exact entries**

| Code | Title | Definition |
|---|---|---|
| A-13 | Public Artifact | A file or route intentionally approved for public access under a documented schema, retention rule, and release. |
| A-14 | Candidate Release | An immutable collection of generated artifacts that has not yet received publication approval. |
| A-15 | Approved Release | A candidate release that passed required validation and became the publicly selected release. |
| A-16 | Last-Known-Good Release | The most recent approved release retained as the public fallback when a later run fails or is withheld. |
| A-17 | Release Manifest | A versioned record listing a release's artifacts, hashes, schemas, provenance, and verification state. |
| A-18 | Source Status | A controlled statement describing a source's current availability, freshness, delay, degradation, pause, or retirement. |
| A-19 | Completeness | A controlled statement describing whether an artifact contains all records expected under its source and selection contract. |
| A-20 | Truncation | An explicit condition in which a bounded artifact returns fewer records than are known or potentially available. |
| A-21 | Provenance | The recorded origin, observation time, transformation path, software version, and release context of a record or artifact. |
| A-22 | Public Field Allowlist | The explicit set of fields approved for publication from a record or feed. |
| A-23 | Retained Evidence | A preserved result, review, approval, incident record, or operational proof used to demonstrate compliance or behavior. |
| A-24 | Supporting Material | Research, audit, history, or analysis that informs controlled documentation but does not itself define authority. |

Use the same four-paragraph entry structure as Task 7.

- [ ] **Step 4: Run tests and validation**

Run:

```bash
python -m pytest tests/docsctl/test_canonical_reference.py -v
python -m tools.docsctl validate --repo-root . --repository AICincy/HCJC2
```

Expected: both pass.

- [ ] **Step 5: Commit**

```bash
git add docs/reference/HCJC-CANONICAL-REFERENCE.md tests/docsctl/test_canonical_reference.py
git commit -m "docs: define canonical release and provenance concepts"
```

---

### Task 9: Publish Canonical Entries A-25 Through A-36

**Files:**
- Modify: `docs/reference/HCJC-CANONICAL-REFERENCE.md`
- Modify: `tests/docsctl/test_canonical_reference.py`

**Interfaces:**
- Adds shared correlation and offense vocabulary

- [ ] **Step 1: Extend the test with A-25 through A-36**

```python
{
    "A-25", "A-26", "A-27", "A-28", "A-29", "A-30",
    "A-31", "A-32", "A-33", "A-34", "A-35", "A-36",
}
```

- [ ] **Step 2: Run the test and verify the entries are absent**

Run:

```bash
python -m pytest tests/docsctl/test_canonical_reference.py -v
```

Expected: failure listing missing A-25 through A-36.

- [ ] **Step 3: Add exact entries**

| Code | Title | Definition |
|---|---|---|
| A-25 | Correlation | A documented relationship, association, or candidate association between two or more records. |
| A-26 | Candidate Relationship | A possible relationship retained for assessment because it satisfies a relationship family's candidate-generation rules. |
| A-27 | Supporting Evidence | A signal that increases support for a candidate relationship or assessment under a documented ruleset. |
| A-28 | Conflicting Evidence | A signal that decreases support or creates ambiguity without automatically disqualifying a candidate. |
| A-29 | Missing Evidence | An expected signal that is unavailable, omitted, unresolved, or not observable. |
| A-30 | Disqualifying Evidence | A signal that makes a candidate relationship or assessment ineligible under a documented rule. |
| A-31 | Evidence Score | A deterministic or statistical summary of evidence that is not a probability unless separately calibrated and validated. |
| A-32 | Confidence Band | A controlled qualitative interpretation of an assessment's evidence and uncertainty. |
| A-33 | Charge Observation | A source observation preserving raw charge text, code, degree, jurisdiction, and source context. |
| A-34 | Authority Record | A reviewed statute, ordinance, rule, or legal reference with currency, jurisdiction, and source provenance. |
| A-35 | Offense Concept | An analytical category used to group related charge observations without replacing legal authority. |
| A-36 | Charge Assessment | A versioned interpretation connecting a charge observation to possible authority records, concepts, classifications, and unresolved facts. |

Use the same four-paragraph entry structure as Task 7.

- [ ] **Step 4: Run tests and validation**

Run:

```bash
python -m pytest tests/docsctl/test_canonical_reference.py -v
python -m tools.docsctl validate --repo-root . --repository AICincy/HCJC2
```

Expected: both pass.

- [ ] **Step 5: Commit**

```bash
git add docs/reference/HCJC-CANONICAL-REFERENCE.md tests/docsctl/test_canonical_reference.py
git commit -m "docs: define canonical correlation and offense concepts"
```

---

### Task 10: Publish Canonical Entries A-37 Through A-46 and Release 1.0.0

**Files:**
- Modify: `docs/reference/HCJC-CANONICAL-REFERENCE.md`
- Modify: `docs/reference/REFERENCE-RELEASES.md`
- Create: `docs/reference/reference-lock.json`
- Modify: `tests/docsctl/test_canonical_reference.py`

**Interfaces:**
- Completes the initial shared product, correction, evidence, and document-governance vocabulary
- Establishes the exact canonical release metadata used by V1 pinning

- [ ] **Step 1: Extend the test with A-37 through A-46**

```python
{
    "A-37", "A-38", "A-39", "A-40", "A-41",
    "A-42", "A-43", "A-44", "A-45", "A-46",
}
```

- [ ] **Step 2: Add exact entries**

| Code | Title | Definition |
|---|---|---|
| A-37 | Correction | A documented process and resulting record used to amend inaccurate, incomplete, or misleading published information. |
| A-38 | Removal | A documented process and resulting state used to stop public availability of an eligible record or artifact. |
| A-39 | Dispute | A documented challenge to a correlation, assessment, or publication decision that requires review and disposition. |
| A-40 | Progressive Enhancement | A presentation model in which essential content and actions remain available without required client-side JavaScript. |
| A-41 | Current Custody Status | A presentation statement identifying whether the latest approved roster lists a person as currently in custody. |
| A-42 | Controlled Document | A document with declared authority, lifecycle, ownership, effective date, and stable references. |
| A-43 | Supersession | The formal replacement of one controlled document or entry by another approved authority. |
| A-44 | Verification Procedure | An executable test, check, or review method identified by a `T-` reference. |
| A-45 | Evidence Record | A dated and attributable result, approval, review, or incident record identified by an `E-` reference. |
| A-46 | Accepted Difference | A reviewed V1-to-V2 difference that is intentional, documented, and not a migration defect. |

- [ ] **Step 3: Record the first canonical release**

Add to `docs/reference/REFERENCE-RELEASES.md`:

```markdown
## Reference release 1.0.0

| Property | Value |
|---|---|
| Tag | `reference-v1.0.0` |
| Release date | 2026-07-23 |
| Change class | Major, initial controlled release |
| Approval | Repository owner with explicit V1 and V2 impact review |
| Entries | A-1 through A-46 |
```

- [ ] **Step 4: Create the release lock**

Before writing the file, capture the current commit:

```bash
CANONICAL_COMMIT=$(git rev-parse HEAD)
printf '%s\n' "$CANONICAL_COMMIT"
```

Create `docs/reference/reference-lock.json` directly from the captured SHA:

```bash
cat > docs/reference/reference-lock.json <<EOF
{
  "canonical_repository": "AICincy/HCJC2",
  "canonical_version": "1.0.0",
  "canonical_tag": "reference-v1.0.0",
  "canonical_commit": "$CANONICAL_COMMIT",
  "released": "2026-07-23"
}
EOF
python -m json.tool docs/reference/reference-lock.json >/dev/null
```

The JSON validation command must exit successfully.

- [ ] **Step 5: Run the full documentation-tool test suite**

Run:

```bash
python -m pytest tests/docsctl -v
python -m tools.docsctl validate --repo-root . --repository AICincy/HCJC2
```

Expected: all tests pass and validation returns zero errors.

- [ ] **Step 6: Commit the release content**

```bash
git add docs/reference tests/docsctl/test_canonical_reference.py
git commit -m "docs: publish canonical reference 1.0.0"
```

Do not create the Git tag until both V1 and V2 migrations pass final verification in Task 17.

---

### Task 11: Import and Classify the Existing HCJC2 Documentation Corpus

**Files:**
- Move or copy existing HCJC2 documents into the controlled structure
- Populate: `docs/migration/LEGACY-DOCUMENT-MAPPING.md`
- Populate supporting directories
- Modify all ten V2 modules

**Interfaces:**
- Converts the approved pre-architecture corpus into controlled modules or explicitly non-authoritative supporting material
- Preserves all source documents and records every migration action

- [ ] **Step 1: Create a failing migration-completeness test**

```python
# tests/docsctl/test_legacy_mapping.py
from pathlib import Path

import yaml


SOURCE_PATHS = {
    "docs/ARCHITECTURE-PRINCIPLES.md",
    "docs/MIGRATION-ACCEPTANCE.md",
    "docs/PRIVACY-INVARIANTS.md",
    "docs/PROJECT-CHARTER.md",
    "docs/QUALITY-GATES.md",
    "docs/TEST-STRATEGY.md",
    "docs/V1-DISPOSITION.md",
    "docs/decisions/ADR-001-NETLIFY.md",
}


def test_every_prearchitecture_document_has_a_legacy_mapping():
    mapping = Path("docs/migration/LEGACY-DOCUMENT-MAPPING.md").read_text(encoding="utf-8")
    missing = sorted(path for path in SOURCE_PATHS if f"`{path}`" not in mapping)
    assert missing == []
```

- [ ] **Step 2: Run the test and verify mappings are absent**

Run:

```bash
python -m pytest tests/docsctl/test_legacy_mapping.py -v
```

Expected: failure listing unmapped source paths.

- [ ] **Step 3: Import the approved consolidated source corpus**

In the implementation environment, extract the approved artifact:

```bash
rm -rf /tmp/hcjc2-doc-source
mkdir -p /tmp/hcjc2-doc-source
unzip -q /mnt/data/HCJC2-consolidated-workspace.zip -d /tmp/hcjc2-doc-source
SOURCE=/tmp/hcjc2-doc-source/HCJC2-workspace
```

Copy source material according to this exact classification:

| Source | Destination | Classification |
|---|---|---|
| `docs/audits/*` | `docs/supporting/audits/` | non-authoritative audit |
| `docs/research/*` | `docs/supporting/research/` | non-authoritative research |
| `docs/tracks/*` | `docs/supporting/historical/tracks/` | historical planning |
| `docs/CONSOLIDATION-RECORD.md` | `docs/supporting/historical/CONSOLIDATION-RECORD.md` | historical record |
| `docs/PROJECT-RECORD.md` | `docs/supporting/historical/PROJECT-RECORD.md` | historical record |
| `docs/costs/*` | `docs/operations/costs/` | controlled operations extension |
| `docs/runbooks/*` | `docs/operations/runbooks/` | controlled operations extension |
| `docs/security/*` | `docs/operations/security/` | controlled operations extension |
| `schemas/*` | `schemas/` | machine-readable contracts |
| `examples/*` | `examples/` | schema examples |

- [ ] **Step 4: Place existing contracts under their controlling families**

Use this exact mapping:

| Existing contract | Controlled destination |
|---|---|
| `CORRELATION-SYSTEM.md` | `docs/correlations/CORRELATION-SYSTEM.md` |
| `LABELED-CORRELATION-FIXTURES.md` | `docs/correlations/LABELED-CORRELATION-FIXTURES.md` |
| `OFFENSE-TAXONOMY.md` | `docs/taxonomy/OFFENSE-TAXONOMY-CONTRACT.md` |
| `PIPELINE-STATE-MACHINE.md` | `docs/pipeline/PIPELINE-STATE-MACHINE.md` |
| `PUBLIC-DATA-PLANE.md` | `docs/pipeline/PUBLIC-DATA-PLANE.md` |
| `CANONICAL-PUBLIC-DATA-MODEL.md` | `docs/data/CANONICAL-PUBLIC-DATA-MODEL.md` |
| `FEED-REGISTRY.md` | `docs/data/FEED-REGISTRY.md` |
| `ARTIFACT-CLASSIFICATION-RETENTION.md` | `docs/data/ARTIFACT-CLASSIFICATION-RETENTION.md` |

Add valid controlled metadata and visible authority statements to each moved contract. Use `status: approved` for contracts and ADRs already approved in the project record.

- [ ] **Step 5: Assign decision references D-1 through D-6**

Preserve ADR filenames and add these references to front matter and headings:

| Decision code | Existing file |
|---|---|
| D-1 | `docs/decisions/ADR-001-NETLIFY.md` |
| D-2 | `docs/decisions/ADR-002-CORRELATION-ENGINE.md` |
| D-3 | `docs/decisions/ADR-003-OFFENSE-TAXONOMY.md` |
| D-4 | `docs/decisions/ADR-004-NETLIFY-AND-DATA-PUBLICATION.md` |
| D-5 | `docs/decisions/ADR-005-R2-WORKER-DATA-PLANE.md` |
| D-6 | `docs/decisions/ADR-006-CANONICAL-DATA-CONTRACTS.md` |

The first heading of each file becomes:

```markdown
# D-1 Netlify Application Hosting
```

Use the corresponding title for D-2 through D-6.

- [ ] **Step 6: Populate the ten core modules as authoritative maps**

Each core module must:

1. summarize the controlled subject in no more than two introductory paragraphs
2. add numbered `V2-` headings for critical requirements
3. link to family extensions and applicable ADRs
4. cite canonical `A-` definitions rather than restating them
5. link supporting audits and research under a clearly labeled non-authoritative section

Assign V2 references continuously in this exact initial sequence:

| Range | Module |
|---|---|
| V2-1 to V2-10 | Master and architecture |
| V2-11 to V2-24 | Data and schemas |
| V2-25 to V2-38 | Acquisition and publication |
| V2-39 to V2-54 | Correlations |
| V2-55 to V2-66 | Offense taxonomy |
| V2-67 to V2-84 | Product and UI/UX |
| V2-85 to V2-96 | Privacy and legal |
| V2-97 to V2-108 | Operations and security |
| V2-109 to V2-120 | Testing and quality |
| V2-121 to V2-136 | Migration and traceability |

Use the approved V2 master specification and imported contracts as the source for titles and rule text. Preserve these mandatory critical rules as independent numbered headings:

- correlations are required and must be materially enhanced
- correlation scores are not probabilities without calibration
- missing legal facts remain unresolved
- missing degree never defaults to `MM`
- partial acquisition never advances
- application deployment and data publication remain separate
- Netlify serves the application plane
- private R2 behind a Worker serves the planned data plane
- the product is a civic-data interface, not a mugshot gallery
- the approved red, navy, white, and near-black visual system is controlling
- WCAG 2.2 AA and progressive enhancement are release requirements
- production cutover requires documented acceptance evidence

- [ ] **Step 7: Populate `LEGACY-DOCUMENT-MAPPING.md`**

Add one row for every existing root document, imported contract, audit, research note, runbook, decision, schema, and example. Use columns:

```markdown
| Legacy path | Section | Classification | Destination | Action | State | Verification |
|---|---|---|---|---|---|---|
```

No row may use an empty action or state.

- [ ] **Step 8: Run validation and legacy mapping tests**

Run:

```bash
python -m pytest tests/docsctl/test_legacy_mapping.py -v
python -m tools.docsctl validate --repo-root . --repository AICincy/HCJC2
python -m tools.docsctl registry --repo-root . --repository AICincy/HCJC2
python -m tools.docsctl traceability --repo-root . --repository AICincy/HCJC2
```

Expected: all commands succeed and generate deterministic registry and matrix outputs.

- [ ] **Step 9: Commit**

```bash
git add docs schemas examples tests/docsctl/test_legacy_mapping.py
git commit -m "docs: migrate HCJC2 documentation into controlled modules"
```

---

### Task 12: Create the V1 Controlled Reference Structure

**Files:**
- Create all V1 `docs-reference/` paths in the locked structure
- Create: `docs-reference/reference/canonical-lock.json`
- Modify: `README.md`

**Interfaces:**
- Produces the V1 descriptive documentation entry points
- Uses the canonical release pinned by HCJC2
- Must not modify `docs/`

- [ ] **Step 1: Record exact repository commits**

From sibling worktrees:

```bash
HCJC2_COMMIT=$(git -C ../HCJC2 rev-parse HEAD)
V1_COMMIT=$(git -C ../HCJC rev-parse HEAD)
printf 'HCJC2=%s\nV1=%s\n' "$HCJC2_COMMIT" "$V1_COMMIT"
```

- [ ] **Step 2: Create the V1 directory structure**

```bash
mkdir -p \
  ../HCJC/docs-reference/architecture \
  ../HCJC/docs-reference/data \
  ../HCJC/docs-reference/pipeline \
  ../HCJC/docs-reference/correlations \
  ../HCJC/docs-reference/taxonomy \
  ../HCJC/docs-reference/product \
  ../HCJC/docs-reference/governance \
  ../HCJC/docs-reference/operations \
  ../HCJC/docs-reference/quality \
  ../HCJC/docs-reference/migration \
  ../HCJC/docs-reference/reference \
  ../HCJC/docs-reference/supporting/{research,evidence,audits,historical}
```

- [ ] **Step 3: Create `canonical-lock.json` from the recorded commits**

```bash
cat > ../HCJC/docs-reference/reference/canonical-lock.json <<EOF
{
  "canonical_repository": "AICincy/HCJC2",
  "canonical_version": "1.0.0",
  "canonical_tag": "reference-v1.0.0",
  "canonical_commit": "$HCJC2_COMMIT",
  "v1_repository": "AICincy/HCJC",
  "reviewed_v1_commit": "$V1_COMMIT",
  "snapshot_generated": "2026-07-23"
}
EOF
python -m json.tool ../HCJC/docs-reference/reference/canonical-lock.json >/dev/null
```

Expected: JSON validation succeeds.

- [ ] **Step 4: Create the V1 master specification**

Run:

```bash
cat > ../HCJC/docs-reference/MASTER-SPEC.md <<EOF
---
title: JCStream V1 Master Specification
reference_namespace: V1
status: draft
authority: v1-master
owner_repository: AICincy/HCJC
document_family: master
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
  commit: $HCJC2_COMMIT
supersedes: []
superseded_by: null
relationships: []
---

# JCStream V1 Master Specification

> **Authority:** Draft controlling entry point for implemented JCStream V1 behavior, reference ownership, preservation, and cross-version interpretation.

## System identity

JCStream V1 is the implemented static public-records system in \`AICincy/HCJC\`. This document describes behavior and does not create new runtime requirements.

## Preservation rule

The V1 reference preserves implemented behavior, operating context, public interfaces, tests, and evidence without presenting V2 plans as V1 capabilities.

## Controlled modules

1. [System Architecture](architecture/SYSTEM-ARCHITECTURE.md)
2. [Data and Schemas](data/DATA-AND-SCHEMAS.md)
3. [Acquisition and Publication](pipeline/ACQUISITION-AND-PUBLICATION.md)
4. [Correlations](correlations/CORRELATIONS.md)
5. [Offense Taxonomy](taxonomy/OFFENSE-TAXONOMY.md)
6. [Product and UI/UX](product/PRODUCT-AND-UI-UX.md)
7. [Privacy and Legal](governance/PRIVACY-AND-LEGAL.md)
8. [Operations and Security](operations/OPERATIONS-AND-SECURITY.md)
9. [Testing and Quality](quality/TESTING-AND-QUALITY.md)
10. [Migration and Traceability](migration/MIGRATION-AND-TRACEABILITY.md)
EOF
```

- [ ] **Step 5: Create the ten V1 module files from the HCJC2 manifest**

Reuse the exact module manifest from Task 6, changing only these values before writing each file:

```python
reference_namespace = "V1"
status = "draft"
owner_repository = "AICincy/HCJC"
canonical_commit = HCJC2_COMMIT
path_prefix = Path("../HCJC/docs-reference")
```

The script must write the same ten titles and families, use authority names beginning with `v1-`, and include the actual `$HCJC2_COMMIT` value in `canonical_reference.commit`. Run the script in the same shell that set `HCJC2_COMMIT`, then verify:

```bash
grep -R "commit: $HCJC2_COMMIT" ../HCJC/docs-reference/{architecture,data,pipeline,correlations,taxonomy,product,governance,operations,quality,migration}
```

Expected: one match in each of the ten module files.

- [ ] **Step 6: Update the V1 README as a compact orientation**

Preserve the public identity and quick-start material, but replace the encyclopedic body with:

```markdown
## Controlled reference documentation

- [V1 Master Specification](docs-reference/MASTER-SPEC.md)
- [Pinned Canonical Reference](https://github.com/AICincy/HCJC2/blob/reference-v1.0.0/docs/reference/HCJC-CANONICAL-REFERENCE.md)
- [V1 Traceability Snapshot](docs-reference/reference/TRACEABILITY-MATRIX-SNAPSHOT.md)

The generated public website remains in `docs/`. Controlled technical reference documentation is maintained separately in `docs-reference/`.
```

Retain essential local setup and operator commands below this section.

- [ ] **Step 7: Verify that the generated site directory is unchanged**

Run before and after the task:

```bash
git -C ../HCJC status --short docs/
```

Expected: no changes under `docs/`.

- [ ] **Step 8: Validate V1 controlled files with HCJC2 tooling**

Run from HCJC2:

```bash
python -m tools.docsctl validate --repo-root ../HCJC --repository AICincy/HCJC
```

Expected: zero errors.

- [ ] **Step 9: Commit in V1**

```bash
git -C ../HCJC add README.md docs-reference
git -C ../HCJC commit -m "docs: establish V1 controlled reference structure"
```

---

### Task 13: Populate and Verify the Ten V1 Modules

**Files:**
- Modify all ten V1 controlled modules
- Create: `docs-reference/migration/LEGACY-DOCUMENT-MAPPING.md`
- Populate V1 supporting directories

**Interfaces:**
- Produces authoritative descriptive V1 entries `V1-1` through `V1-120`
- Provides source paths, tests, and evidence for each controlled behavior

- [ ] **Step 1: Inventory the V1 documentation and implementation sources**

Use these exact source groups:

| Module | Primary sources |
|---|---|
| Architecture | `README.md`, `wiki/Architecture.md`, `pyproject.toml`, repository tree |
| Data | `wiki/Data.md`, `scraper/models.py`, `scraper/store.py`, `data/*.json` shape samples |
| Pipeline | `wiki/Operations.md`, `scraper/sweep.py`, `scraper/client.py`, `scraper/store.py`, `.github/workflows/sweep.yml` |
| Correlations | `scraper/match.py`, `scraper/correlate.py`, `tests/test_match.py`, `tests/test_correlate.py` |
| Taxonomy | `scraper/orc.py`, `web/classify.py`, `data/orc_offenses.json`, ORC tests |
| Product | `web/templates/**`, `web/static/site.css`, `web/static/site.js`, route-building code, accessibility audits |
| Governance | `wiki/Legal.md`, `SECURITY.md`, legal copy in templates, correction issue forms |
| Operations | `.github/workflows/**`, alert modules, evidence verifiers, `wiki/Operations.md` |
| Quality | `pyproject.toml`, `.github/workflows/ci.yml`, `tests/**`, CodeQL workflow |
| Migration | all above, V2 controlled modules, canonical reference, reviewed V1 commit |

- [ ] **Step 2: Copy non-authoritative material into V1 supporting areas without deleting originals**

Use:

```text
audit/*.md                  -> docs-reference/supporting/audits/
audit/sessions/**           -> docs-reference/supporting/historical/sessions/
wiki/Roadmap.md             -> docs-reference/supporting/historical/ROADMAP.md
selected test baselines     -> docs-reference/supporting/evidence/
```

Do not copy runtime data, photos, caches, session JSONL containing sensitive material, or generated `docs/` output into controlled documentation.

- [ ] **Step 3: Assign V1 reference ranges**

Use this exact continuous allocation:

| Range | Module |
|---|---|
| V1-1 to V1-10 | Master and architecture |
| V1-11 to V1-24 | Data and schemas |
| V1-25 to V1-40 | Acquisition and publication |
| V1-41 to V1-52 | Correlations |
| V1-53 to V1-64 | Offense taxonomy |
| V1-65 to V1-82 | Product and UI/UX |
| V1-83 to V1-94 | Privacy and legal |
| V1-95 to V1-106 | Operations and security |
| V1-107 to V1-114 | Testing and quality |
| V1-115 to V1-120 | Migration and traceability |

Every entry must cite at least one implementation path or test path.

- [ ] **Step 4: Populate System Architecture, Data, and Pipeline modules**

Required controlled headings include:

```text
V1-1 Static Site and Flat-File Architecture
V1-2 Repository and Publication Topology
V1-3 Major Runtime Components
V1-4 GitHub Pages Application Surface
V1-5 Version-Controlled Operational State
V1-11 Current Roster Snapshot
V1-12 Inmate and Charge Models
V1-13 Change Events
V1-14 Anonymized Activity History
V1-15 Booking Photo Records
V1-16 Supplemental Feed Artifacts
V1-25 Alphabetic Surname Sweep
V1-26 List and Detail Acquisition
V1-27 Concurrency and Crawl Delay
V1-28 Source Health Evaluation
V1-29 Atomic File Persistence
V1-30 Booking, Release, and Update Diffing
V1-31 Static Site Build
V1-32 Repository Commit and GitHub Pages Publication
```

Cite the canonical A entries for shared concepts, then describe only implemented V1 behavior.

- [ ] **Step 5: Populate Correlations and Offense Taxonomy modules**

Required headings include:

```text
V1-41 Public Candidate Dispatch Matching
V1-42 Research Correlation Output
V1-43 Public Correlation Presentation
V1-44 Correlation Input Signals
V1-45 Correlation Output Fields
V1-53 ORC Reference Catalog
V1-54 ORC Code Normalization
V1-55 Severity Ladder
V1-56 Offense Category Grouping
V1-57 Statute Pages
V1-58 Charge-Tier Presentation
```

Describe both correlation paths neutrally and separately. Preserve the exact V1 naming `Candidate dispatch calls` where it appears in the UI.

- [ ] **Step 6: Populate Product and UI/UX and Privacy and Legal modules**

Required headings include:

```text
V1-65 Public Route Hierarchy
V1-66 Shared Page Shell and Navigation
V1-67 Roster Search and Filtering
V1-68 Roster Card and Table Views
V1-69 Individual Custody Page
V1-70 Statistics and Context Pages
V1-71 Public Sans and IBM Plex Mono Typography
V1-72 Warm Neutral Civic-Modern Palette
V1-73 Severity and Category Color Systems
V1-74 Progressive Enhancement
V1-75 Booking Photo Lightbox
V1-76 Tooltips and Disclosure Navigation
V1-77 Responsive Behavior
V1-78 Accessibility Behavior
V1-83 Public Records and Independent Status
V1-84 Presumption of Innocence
V1-85 Consumer Reporting Restriction
V1-86 No-Index and No-Archive Controls
V1-87 Generic Social Metadata
V1-88 Current Photo Removal
V1-89 Correction and Removal Assistance
```

Use the actual CSS tokens and implemented JavaScript behaviors documented in V1 source.

- [ ] **Step 7: Populate Operations, Quality, and Migration modules**

Required headings include:

```text
V1-95 Scheduled Sweep Workflow
V1-96 Source Freeze Monitoring
V1-97 Deployment Staleness Monitoring
V1-98 WAF Access Evidence Ledger
V1-99 PRA Evidence Ledger
V1-100 Security and Dependency Checks
V1-107 Pytest Verification Suite
V1-108 Ruff Linting
V1-109 Mypy Type Checking
V1-110 Empty-Data Build Smoke Test
V1-111 Evidence Chain Verification
V1-112 Custom Domain Verification
V1-115 V1 Preservation Scope
V1-116 V1-to-V2 Behavioral Mapping
V1-117 Reviewed V1 Commit
V1-118 Pinned Canonical Reference
V1-119 Accepted Differences
V1-120 V1 Traceability Snapshot
```

- [ ] **Step 8: Populate the V1 legacy mapping ledger**

Inventory:

- root `README.md`
- all `wiki/*.md`
- all `audit/*.md`
- relevant `.github` issue and workflow documentation
- existing `CLAUDE.md` documentation sections

For every substantive section, record whether it was migrated, consolidated, preserved as supporting, retained as historical, or intentionally excluded because it is generated output or runtime data.

- [ ] **Step 9: Validate V1 against its implementation**

Run:

```bash
python -m tools.docsctl validate --repo-root ../HCJC --repository AICincy/HCJC
python -m pytest ../HCJC/tests/test_match.py ../HCJC/tests/test_correlate.py -v
python -m pytest ../HCJC/tests/test_build.py ../HCJC/tests/test_outputs.py -v
```

Expected: documentation validation passes and the cited behavioral tests pass.

- [ ] **Step 10: Commit in V1**

```bash
git -C ../HCJC add docs-reference
git -C ../HCJC commit -m "docs: document implemented JCStream V1 behavior"
```

---

### Task 14: Add Cross-Version Relationships and Generate the V1 Snapshot

**Files:**
- Modify HCJC2 controlled front matter relationships
- Modify V1 controlled front matter relationships
- Generate HCJC2 registry and matrix
- Generate V1 snapshot

**Interfaces:**
- Produces explicit `defines`, `implements`, `refines`, `replaces`, `preserves`, `verifies`, and `accepted-difference-from` relationships

- [ ] **Step 1: Add canonical-to-version relationships**

At minimum, create these explicit relationships:

```yaml
- from: V1-13
  relation: implements
  to: A-10
- from: V2-14
  relation: refines
  to: A-7
- from: V1-41
  relation: implements
  to: A-26
- from: V2-39
  relation: refines
  to: A-25
- from: V1-53
  relation: implements
  to: A-34
- from: V2-55
  relation: refines
  to: A-33
- from: V1-74
  relation: implements
  to: A-40
- from: V2-78
  relation: requires
  to: A-40
- from: V1-116
  relation: maps-to
  to: V2-121
```

Add the remaining relationships needed to connect every canonical entry to at least one V1 or V2 entry where applicable.

- [ ] **Step 2: Add decision constraints**

Create explicit relationships such as:

```yaml
- from: V2-39
  relation: constrained-by
  to: D-2
- from: V2-55
  relation: constrained-by
  to: D-3
- from: V2-25
  relation: constrained-by
  to: D-4
- from: V2-30
  relation: constrained-by
  to: D-5
- from: V2-11
  relation: constrained-by
  to: D-6
```

Each relationship is authored from the controlled requirement to the governing decision, so `constrained-by` is the exact relationship term.

- [ ] **Step 3: Generate current HCJC2 outputs**

Run:

```bash
python -m tools.docsctl registry --repo-root . --repository AICincy/HCJC2
python -m tools.docsctl traceability --repo-root . --repository AICincy/HCJC2
```

Expected: Markdown and JSON files are written under `docs/reference/`.

- [ ] **Step 4: Generate the V1 snapshot using actual commits**

Run:

```bash
CANONICAL_COMMIT=$(git rev-parse HEAD)
V1_COMMIT=$(git -C ../HCJC rev-parse HEAD)
python -m tools.docsctl snapshot-v1 \
  --repo-root . \
  --repository AICincy/HCJC2 \
  --output ../HCJC/docs-reference/reference/TRACEABILITY-MATRIX-SNAPSHOT.md \
  --canonical-version 1.0.0 \
  --canonical-tag reference-v1.0.0 \
  --canonical-commit "$CANONICAL_COMMIT" \
  --v1-commit "$V1_COMMIT" \
  --generated-date 2026-07-23
```

Expected: the snapshot contains actual 40-character commit SHAs and only relationships involving V1.

- [ ] **Step 5: Validate both repositories**

Run:

```bash
python -m tools.docsctl validate --repo-root . --repository AICincy/HCJC2
python -m tools.docsctl validate --repo-root ../HCJC --repository AICincy/HCJC
```

Expected: zero errors in both repositories.

- [ ] **Step 6: Commit in both repositories**

```bash
git add docs/reference docs/**/*.md
git commit -m "docs: generate cross-version traceability"

git -C ../HCJC add docs-reference
git -C ../HCJC commit -m "docs: pin V1 traceability snapshot"
```

---

### Task 15: Integrate Documentation Validation into HCJC2 CI

**Files:**
- Create: `.github/workflows/docs.yml`
- Modify: `tools/docsctl/cli.py`
- Create: `tests/docsctl/test_check_command.py`

**Interfaces:**
- `docsctl check` validates controlled documents, regenerates outputs in memory, and fails when committed outputs differ

- [ ] **Step 1: Write the failing `check` command test**

```python
# tests/docsctl/test_check_command.py
from pathlib import Path

from tools.docsctl.cli import main


def test_check_fails_when_generated_registry_is_stale(tmp_path):
    docs = tmp_path / "docs" / "reference"
    docs.mkdir(parents=True)
    (docs / "REFERENCE-REGISTRY.md").write_text("stale\n", encoding="utf-8")

    result = main(["check", "--repo-root", str(tmp_path), "--repository", "AICincy/HCJC2"])

    assert result == 1
```

- [ ] **Step 2: Implement `check`**

`check` must:

1. discover and parse controlled documents
2. fail on validation errors
3. render registry and traceability outputs in memory
4. compare them byte-for-byte with committed Markdown and JSON outputs
5. print a precise stale-file message
6. return `1` when any output differs

- [ ] **Step 3: Create the HCJC2 workflow**

```yaml
# .github/workflows/docs.yml
name: documentation

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
          cache: pip
      - run: python -m pip install -e '.[dev]'
      - run: ruff check tools tests
      - run: python -m pytest tests/docsctl -v
      - run: python -m tools.docsctl check --repo-root . --repository AICincy/HCJC2
```

Pin action SHAs according to the repository's workflow policy before merging. Do not leave floating tags in the committed workflow.

- [ ] **Step 4: Run local verification**

Run:

```bash
python -m pytest tests/docsctl/test_check_command.py -v
python -m tools.docsctl check --repo-root . --repository AICincy/HCJC2
```

Expected: tests pass and current generated outputs are reported as current.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/docs.yml tools/docsctl/cli.py tests/docsctl/test_check_command.py
git commit -m "ci: validate controlled documentation"
```

---

### Task 16: Integrate Pinned Cross-Repository Validation into V1 CI

**Files:**
- Modify: `../HCJC/.github/workflows/ci.yml`
- Modify: `../HCJC/docs-reference/reference/canonical-lock.json`

**Interfaces:**
- V1 CI checks out the exact canonical HCJC2 reference commit and runs the canonical validator against V1

- [ ] **Step 1: Add a separate V1 documentation job**

Append this job to the V1 CI workflow:

```yaml
  documentation:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Check out V1
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          path: HCJC
      - name: Read the pinned HCJC2 commit
        id: canonical-lock
        working-directory: HCJC
        shell: bash
        run: |
          commit=$(python -c 'import json; print(json.load(open("docs-reference/reference/canonical-lock.json"))["canonical_commit"])')
          echo "commit=$commit" >> "$GITHUB_OUTPUT"
      - name: Check out pinned HCJC2 documentation tooling
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          repository: AICincy/HCJC2
          ref: ${{ steps.canonical-lock.outputs.commit }}
          path: HCJC2
      - name: Set up Python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97
        with:
          python-version: '3.13'
          cache: pip
          cache-dependency-path: HCJC2/pyproject.toml
      - name: Install documentation tooling
        working-directory: HCJC2
        run: python -m pip install -e '.[dev]'
      - name: Validate V1 controlled documentation
        working-directory: HCJC2
        run: python -m tools.docsctl validate --repo-root ../HCJC --repository AICincy/HCJC
```

- [ ] **Step 2: Preserve the existing V1 runtime CI job unchanged**

Confirm the existing test matrix, Ruff, Mypy, dependency audit, evidence-chain verification, empty-data build, and CNAME checks remain byte-equivalent except for YAML indentation required to add the new sibling job.

- [ ] **Step 3: Run local V1 validation**

Run from HCJC2:

```bash
python -m tools.docsctl validate --repo-root ../HCJC --repository AICincy/HCJC
```

Expected: zero errors.

- [ ] **Step 4: Commit in V1**

```bash
git -C ../HCJC add .github/workflows/ci.yml docs-reference/reference/canonical-lock.json
git -C ../HCJC commit -m "ci: validate pinned V1 reference documentation"
```

---

### Task 17: Final Cross-Repository Verification and Canonical Release Tag

**Files:**
- Modify generated registries and snapshots if commit pins changed
- Modify: `docs/reference/REFERENCE-RELEASES.md`
- Modify both legacy mapping ledgers to `verified` or `archived`

**Interfaces:**
- Produces the reviewed release state required before documentation entry points become authoritative

- [ ] **Step 1: Run complete HCJC2 verification**

Run:

```bash
python -m pip install -e '.[dev]'
ruff check tools tests
python -m pytest tests/docsctl -v
python -m tools.docsctl check --repo-root . --repository AICincy/HCJC2
```

Expected: all checks pass.

- [ ] **Step 2: Run complete V1 verification**

Run:

```bash
python -m tools.docsctl validate --repo-root ../HCJC --repository AICincy/HCJC
python -m pytest ../HCJC/tests -v
```

Expected: documentation validation and the complete V1 test suite pass.

- [ ] **Step 3: Verify legacy mapping completeness**

Run:

```bash
python - <<'PY'
from pathlib import Path

for path in (
    Path("docs/migration/LEGACY-DOCUMENT-MAPPING.md"),
    Path("../HCJC/docs-reference/migration/LEGACY-DOCUMENT-MAPPING.md"),
):
    text = path.read_text(encoding="utf-8")
    forbidden = ("|  |", "pending classification", "unresolved marker")
    failures = [value for value in forbidden if value in text]
    if failures:
        raise SystemExit(f"{path}: unresolved migration markers: {failures}")
print("legacy mappings complete")
PY
```

Expected: `legacy mappings complete`.

- [ ] **Step 4: Regenerate outputs using final commits**

Because the canonical and V1 commits changed during migration, regenerate:

```bash
python -m tools.docsctl registry --repo-root . --repository AICincy/HCJC2
python -m tools.docsctl traceability --repo-root . --repository AICincy/HCJC2
CANONICAL_COMMIT=$(git rev-parse HEAD)
V1_COMMIT=$(git -C ../HCJC rev-parse HEAD)
python -m tools.docsctl snapshot-v1 \
  --repo-root . \
  --repository AICincy/HCJC2 \
  --output ../HCJC/docs-reference/reference/TRACEABILITY-MATRIX-SNAPSHOT.md \
  --canonical-version 1.0.0 \
  --canonical-tag reference-v1.0.0 \
  --canonical-commit "$CANONICAL_COMMIT" \
  --v1-commit "$V1_COMMIT" \
  --generated-date 2026-07-23
```

Commit regenerated outputs in each repository.

- [ ] **Step 5: Mark approved controlled documents**

Change `status: draft` to `status: approved` only for documents that passed subject review. Leave any incomplete document as `draft`; do not issue the release tag until all master specifications and ten core modules are approved.

- [ ] **Step 6: Create the canonical release tag**

After final approvals:

```bash
git tag -a reference-v1.0.0 -m "Canonical cross-version reference 1.0.0"
git show --stat reference-v1.0.0
```

Expected: the tag points to the commit containing A-1 through A-46, the current registry, the current traceability matrix, approved modules, and final release metadata.

- [ ] **Step 7: Push branches and tag through the approved repository workflow**

```bash
git push origin HEAD
git push origin reference-v1.0.0
git -C ../HCJC push origin HEAD
```

Expected: all pushes succeed and both repositories' documentation CI checks pass.

- [ ] **Step 8: Record release evidence**

Create an `E-` entry for the completed release review containing:

- HCJC2 commit
- V1 commit
- canonical tag
- CI run links
- test counts
- validator result
- approving reviewers
- release date

Link that evidence entry from `REFERENCE-RELEASES.md` and the migration modules.

- [ ] **Step 9: Final commit if evidence was added after tagging**

If the evidence record is added after the tag, release it as canonical patch version `1.0.1` only when it changes the canonical reference itself. An external evidence record that does not change canonical meaning does not require retagging `1.0.0`.

---

## Self-Review

### Spec coverage

- Repository ownership and authority: Tasks 6, 12, 17
- Mirrored ten-family structure: Tasks 6, 12, 13
- Canonical reference: Tasks 7 through 10
- Human-readable identifiers: Tasks 2, 7 through 14
- YAML metadata and visible authority: Tasks 2, 6, 12
- Registry and matrix generation: Tasks 4, 14
- V1 pinned snapshot: Tasks 5, 14
- Legacy preservation and mapping: Tasks 11, 13, 17
- Validation rules and CI: Tasks 3, 15, 16
- Semantic release and approval: Tasks 10, 17
- V1 generated `docs/` protection: Tasks 12 and 13
- README compaction: Tasks 6 and 12
- Supporting-material separation: Tasks 11 and 13
- Human usability: enforced by the controlled templates, linked code-and-title citations, and final acceptance review

### Completeness scan

Every runtime-derived commit value is produced by an exact command and written through shell interpolation. Workflow actions use immutable commit SHAs. No unresolved implementation marker or unspecified change step remains.

### Type and interface consistency

- `parse_document()` returns `ParsedDocument` throughout.
- `validate_documents()` consumes parsed documents and returns `ValidationIssue` values.
- Registry and traceability generation consume the same parsed-document model.
- Snapshot generation consumes `TraceabilityRow` values and explicit pin metadata.
- CLI command names and default output paths remain consistent across tasks.

