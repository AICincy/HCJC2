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
