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
    controlled_paths = [
        root / "docs/MASTER-SPEC.md",
        *root.glob("docs/architecture/*.md"),
        *root.glob("docs/data/*.md"),
        *root.glob("docs/pipeline/*.md"),
        *root.glob("docs/correlations/*.md"),
        *root.glob("docs/taxonomy/*.md"),
        *root.glob("docs/product/*.md"),
        *root.glob("docs/governance/*.md"),
        *root.glob("docs/operations/*.md"),
        *root.glob("docs/quality/*.md"),
        *root.glob("docs/migration/*.md"),
        *root.glob("docs/reference/*.md"),
        root / "docs-reference/MASTER-SPEC.md",
        *root.glob("docs-reference/architecture/*.md"),
        *root.glob("docs-reference/data/*.md"),
        *root.glob("docs-reference/pipeline/*.md"),
        *root.glob("docs-reference/correlations/*.md"),
        *root.glob("docs-reference/taxonomy/*.md"),
        *root.glob("docs-reference/product/*.md"),
        *root.glob("docs-reference/governance/*.md"),
        *root.glob("docs-reference/operations/*.md"),
        *root.glob("docs-reference/quality/*.md"),
        *root.glob("docs-reference/migration/*.md"),
        *root.glob("docs-reference/reference/*.md"),
        *root.glob("docs/decisions/*.md"),
    ]
    return tuple(
        sorted(
            {
                path
                for path in controlled_paths
                if path.is_file() and path.read_text(encoding="utf-8").startswith("---\n")
            }
        )
    )


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


def validate_documents(
    documents: Sequence[ParsedDocument],
    root: Path,
    repository_roots: dict[str, Path] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    roots = repository_roots or {}
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
        document_root = roots.get(document.metadata.owner_repository, root)
        for problem in validate_local_links(document.path, document_root):
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
