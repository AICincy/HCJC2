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
