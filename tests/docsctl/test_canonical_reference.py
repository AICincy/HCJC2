from pathlib import Path

from tools.docsctl.parser import parse_document

EXPECTED = {f"A-{number}" for number in range(1, 47)}


def test_initial_canonical_identity_and_record_entries_exist():
    document = parse_document(Path("docs/reference/HCJC-CANONICAL-REFERENCE.md"), "AICincy/HCJC2")
    assert EXPECTED <= {entry.code for entry in document.references}
