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
