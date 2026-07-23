from pathlib import Path

SOURCE_PATHS = {
    "docs/ARCHITECTURE-PRINCIPLES.md",
    "docs/MIGRATION-ACCEPTANCE.md",
    "docs/PRIVACY-INVARIANTS.md",
    "docs/PROJECT-CHARTER.md",
    "docs/QUALITY-GATES.md",
    "docs/TEST-STRATEGY.md",
    "docs/V1-DISPOSITION.md",
    "docs/decisions/ADR-001-NETLIFY.md",
}


def test_every_prearchitecture_document_has_a_legacy_mapping():
    mapping = Path("docs/migration/LEGACY-DOCUMENT-MAPPING.md").read_text(encoding="utf-8")
    missing = sorted(path for path in SOURCE_PATHS if f"`{path}`" not in mapping)
    assert missing == []
