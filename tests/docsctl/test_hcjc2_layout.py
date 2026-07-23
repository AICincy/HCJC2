from pathlib import Path


EXPECTED = {
    "docs/MASTER-SPEC.md",
    "docs/reference/HCJC-CANONICAL-REFERENCE.md",
    "docs/reference/REFERENCE-RELEASES.md",
    "docs/architecture/SYSTEM-ARCHITECTURE.md",
    "docs/data/DATA-AND-SCHEMAS.md",
    "docs/pipeline/ACQUISITION-AND-PUBLICATION.md",
    "docs/correlations/CORRELATIONS.md",
    "docs/taxonomy/OFFENSE-TAXONOMY.md",
    "docs/product/PRODUCT-AND-UI-UX.md",
    "docs/governance/PRIVACY-AND-LEGAL.md",
    "docs/operations/OPERATIONS-AND-SECURITY.md",
    "docs/quality/TESTING-AND-QUALITY.md",
    "docs/migration/MIGRATION-AND-TRACEABILITY.md",
    "docs/migration/LEGACY-DOCUMENT-MAPPING.md",
}


def test_hcjc2_controlled_document_layout_exists():
    missing = sorted(path for path in EXPECTED if not Path(path).is_file())
    assert missing == []
