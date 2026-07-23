from __future__ import annotations

from pathlib import Path
from typing import Sequence

from tools.docsctl.model import ParsedDocument, ReferenceEntry
from tools.docsctl.render import json_text, reference_sort_key, relative_path


def build_registry(documents: Sequence[ParsedDocument]) -> tuple[ReferenceEntry, ...]:
    return tuple(
        sorted(
            (entry for document in documents for entry in document.references),
            key=lambda item: reference_sort_key(item.code),
        )
    )


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
        lines.append(
            f"| {entry.code} | {entry.title} | {entry.repository} | `{document}#{entry.anchor}` | "
            f"{entry.status.value} | {entry.authority} | {entry.effective_date} | {entry.canonical_version or ''} |"
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
