from tools.docsctl.cli import main


def test_help_lists_all_commands(capsys):
    result = main(["--help"])
    captured = capsys.readouterr()

    assert result == 0
    assert "validate" in captured.out
    assert "registry" in captured.out
    assert "traceability" in captured.out
    assert "snapshot-v1" in captured.out
    assert "check" in captured.out


def test_load_documents_includes_sibling_repository(tmp_path):
    from pathlib import Path
    from tools.docsctl.cli import _load_documents

    hcjc2 = tmp_path / "HCJC2"
    hcjc = tmp_path / "HCJC"
    (hcjc2 / "docs").mkdir(parents=True)
    (hcjc / "docs-reference").mkdir(parents=True)
    common = """---
title: {title}
reference_namespace: {namespace}
status: approved
authority: {authority}
owner_repository: {owner}
document_family: master
effective_date: 2026-07-23
supersedes: []
superseded_by: null
relationships: []
---

# {title}

## {code} Entry
"""
    (hcjc2 / "docs" / "MASTER-SPEC.md").write_text(
        common.format(title="V2", namespace="V2", authority="v2-master", owner="AICincy/HCJC2", code="V2-1"),
        encoding="utf-8",
    )
    (hcjc / "docs-reference" / "MASTER-SPEC.md").write_text(
        common.format(title="V1", namespace="V1", authority="v1-master", owner="AICincy/HCJC", code="V1-1"),
        encoding="utf-8",
    )

    documents = _load_documents(hcjc2, "AICincy/HCJC2")

    assert {document.metadata.owner_repository for document in documents} == {"AICincy/HCJC2", "AICincy/HCJC"}
