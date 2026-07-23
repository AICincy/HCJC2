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
    r"^(?P<marks>#{1,6}) (?P<code>(?:A|V1|V2|D|S|T|E)-[1-9][0-9]*) (?P<title>\S.*)$"
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
