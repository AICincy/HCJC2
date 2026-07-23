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


def test_cross_repository_relationship_and_links_validate_with_repository_roots(tmp_path):
    hcjc2 = tmp_path / "HCJC2"
    hcjc = tmp_path / "HCJC"
    (hcjc2 / "docs").mkdir(parents=True)
    (hcjc / "docs-reference").mkdir(parents=True)
    v2_path = hcjc2 / "docs" / "MASTER-SPEC.md"
    v1_path = hcjc / "docs-reference" / "MASTER-SPEC.md"
    v2_path.write_text(
        """---
title: V2
reference_namespace: V2
status: approved
authority: v2-master
owner_repository: AICincy/HCJC2
document_family: master
effective_date: 2026-07-23
supersedes: []
superseded_by: null
relationships:
  - from: V1-1
    relation: maps-to
    to: V2-1
---

# V2

## V2-1 Successor Rule
""",
        encoding="utf-8",
    )
    v1_path.write_text(
        """---
title: V1
reference_namespace: V1
status: approved
authority: v1-master
owner_repository: AICincy/HCJC
document_family: master
effective_date: 2026-07-23
supersedes: []
superseded_by: null
relationships: []
---

# V1

## V1-1 Implemented Behavior
""",
        encoding="utf-8",
    )
    documents = [parse_document(v2_path, "AICincy/HCJC2"), parse_document(v1_path, "AICincy/HCJC")]

    issues = validate_documents(
        documents,
        hcjc2,
        repository_roots={"AICincy/HCJC2": hcjc2, "AICincy/HCJC": hcjc},
    )

    assert not issues
