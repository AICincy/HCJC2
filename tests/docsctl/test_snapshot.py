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
