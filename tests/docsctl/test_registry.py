import json
from pathlib import Path

from tools.docsctl.parser import parse_document
from tools.docsctl.registry import build_registry, render_registry_json, render_registry_markdown

FIXTURE = Path(__file__).parent / "fixtures" / "valid-controlled.md"


def test_registry_is_sorted_and_renders_stable_outputs(tmp_path):
    document = parse_document(FIXTURE, "AICincy/HCJC2")
    entries = build_registry([document])

    markdown = render_registry_markdown(entries, tmp_path)
    payload = json.loads(render_registry_json(entries, tmp_path))

    assert "| V2-57 | Correlation Assessments |" in markdown
    assert payload[0]["reference"] == "V2-57"
