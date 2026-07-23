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
    return tuple(
        sorted(
            rows,
            key=lambda row: (reference_sort_key(row.source), row.relation, reference_sort_key(row.target)),
        )
    )


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
