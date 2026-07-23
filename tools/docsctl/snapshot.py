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
    body = render_traceability_markdown(rows).replace(
        "# Traceability Matrix", "# V1 Traceability Matrix Snapshot", 1
    )
    front_matter = "\n".join(
        [
            "---",
            "title: V1 Traceability Matrix Snapshot",
            "reference_namespace: V1",
            "status: approved",
            "authority: v1-traceability-snapshot",
            "owner_repository: AICincy/HCJC",
            "document_family: reference",
            f"effective_date: {metadata.generated_date}",
            "canonical_reference:",
            f"  version: {metadata.canonical_version}",
            f"  tag: {metadata.canonical_tag}",
            f"  commit: {metadata.canonical_commit}",
            f"canonical_commit: {metadata.canonical_commit}",
            f"v1_commit: {metadata.v1_commit}",
            f"generator_version: {metadata.generator_version}",
            "supersedes: []",
            "superseded_by: null",
            "---",
            "",
            "> **Authority:** Generated historical snapshot of V1 relationships against the pinned canonical reference.",
            "",
        ]
    )
    return front_matter + body
