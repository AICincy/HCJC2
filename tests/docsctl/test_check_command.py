from tools.docsctl.cli import main


def test_check_fails_when_generated_registry_is_stale(tmp_path, capsys):
    docs = tmp_path / "docs" / "reference"
    docs.mkdir(parents=True)
    (docs / "REFERENCE-REGISTRY.md").write_text("stale\n", encoding="utf-8")

    result = main(["check", "--repo-root", str(tmp_path), "--repository", "AICincy/HCJC2"])
    captured = capsys.readouterr()

    assert result == 1
    assert "stale generated documentation" in captured.out
    assert "REFERENCE-REGISTRY.md" in captured.out
