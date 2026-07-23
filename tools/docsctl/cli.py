from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from tools.docsctl.parser import parse_document
from tools.docsctl.registry import build_registry, render_registry_json, render_registry_markdown
from tools.docsctl.snapshot import SnapshotMetadata, render_v1_snapshot
from tools.docsctl.traceability import build_traceability, render_traceability_json, render_traceability_markdown
from tools.docsctl.validate import discover_controlled_documents, validate_documents


COMMANDS = ("validate", "registry", "traceability", "snapshot-v1", "check")


def _add_repository_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--repository", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="docsctl")
    subparsers = parser.add_subparsers(dest="command", metavar="{" + ",".join(COMMANDS) + "}")
    for command in COMMANDS:
        command_parser = subparsers.add_parser(command)
        _add_repository_arguments(command_parser)
        if command == "registry":
            command_parser.add_argument("--markdown-output", type=Path, default=Path("docs/reference/REFERENCE-REGISTRY.md"))
            command_parser.add_argument("--json-output", type=Path, default=Path("docs/reference/REFERENCE-REGISTRY.json"))
        elif command == "traceability":
            command_parser.add_argument("--markdown-output", type=Path, default=Path("docs/reference/TRACEABILITY-MATRIX.md"))
            command_parser.add_argument("--json-output", type=Path, default=Path("docs/reference/TRACEABILITY-MATRIX.json"))
        elif command == "snapshot-v1":
            command_parser.add_argument("--output", type=Path, required=True)
            command_parser.add_argument("--canonical-version", required=True)
            command_parser.add_argument("--canonical-tag", required=True)
            command_parser.add_argument("--canonical-commit", required=True)
            command_parser.add_argument("--v1-commit", required=True)
            command_parser.add_argument("--generated-date", required=True)
    return parser


def _repository_roots(repo_root: Path, repository: str) -> dict[str, Path]:
    resolved = repo_root.resolve()
    roots = {repository: resolved}
    sibling_name = "HCJC" if repository == "AICincy/HCJC2" else "HCJC2" if repository == "AICincy/HCJC" else None
    sibling_repository = "AICincy/HCJC" if repository == "AICincy/HCJC2" else "AICincy/HCJC2" if repository == "AICincy/HCJC" else None
    if sibling_name and sibling_repository:
        sibling = resolved.parent / sibling_name
        if sibling.is_dir():
            roots[sibling_repository] = sibling
    return roots


def _load_documents(repo_root: Path, repository: str):
    documents = []
    for owner, root in _repository_roots(repo_root, repository).items():
        documents.extend(parse_document(path, owner) for path in discover_controlled_documents(root))
    return documents


def _validated_documents(repo_root: Path, repository: str):
    documents = _load_documents(repo_root, repository)
    issues = validate_documents(documents, repo_root, repository_roots=_repository_roots(repo_root, repository))
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        for issue in issues:
            print(f"{issue.severity}: {issue.path}: {issue.code}: {issue.message}")
        return None
    return documents


def _run_validate(repo_root: Path, repository: str) -> int:
    documents = _load_documents(repo_root, repository)
    issues = validate_documents(documents, repo_root, repository_roots=_repository_roots(repo_root, repository))
    for issue in issues:
        print(f"{issue.severity}: {issue.path}: {issue.code}: {issue.message}")
    return 1 if any(issue.severity == "error" for issue in issues) else 0


def _write_output(repo_root: Path, output: Path, text: str) -> Path:
    destination = output if output.is_absolute() else repo_root / output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    print(destination)
    return destination


def _run_registry(args: argparse.Namespace) -> int:
    documents = _validated_documents(args.repo_root, args.repository)
    if documents is None:
        return 1
    entries = build_registry(documents)
    _write_output(args.repo_root, args.markdown_output, render_registry_markdown(entries, args.repo_root))
    _write_output(args.repo_root, args.json_output, render_registry_json(entries, args.repo_root))
    return 0


def _run_traceability(args: argparse.Namespace) -> int:
    documents = _validated_documents(args.repo_root, args.repository)
    if documents is None:
        return 1
    rows = build_traceability(documents)
    _write_output(args.repo_root, args.markdown_output, render_traceability_markdown(rows))
    _write_output(args.repo_root, args.json_output, render_traceability_json(rows))
    return 0


def _run_snapshot(args: argparse.Namespace) -> int:
    documents = _validated_documents(args.repo_root, args.repository)
    if documents is None:
        return 1
    rows = tuple(
        row
        for row in build_traceability(documents)
        if row.source.startswith("V1-") or row.target.startswith("V1-")
    )
    text = render_v1_snapshot(
        rows,
        SnapshotMetadata(
            canonical_version=args.canonical_version,
            canonical_tag=args.canonical_tag,
            canonical_commit=args.canonical_commit,
            v1_commit=args.v1_commit,
            generated_date=args.generated_date,
            generator_version="0.1.0",
        ),
    )
    _write_output(args.repo_root, args.output, text)
    return 0



def _run_check(args: argparse.Namespace) -> int:
    documents = _validated_documents(args.repo_root, args.repository)
    if documents is None:
        return 1
    registry_entries = build_registry(documents)
    traceability_rows = build_traceability(documents)
    expected = {
        Path("docs/reference/REFERENCE-REGISTRY.md"): render_registry_markdown(
            registry_entries, args.repo_root
        ),
        Path("docs/reference/REFERENCE-REGISTRY.json"): render_registry_json(
            registry_entries, args.repo_root
        ),
        Path("docs/reference/TRACEABILITY-MATRIX.md"): render_traceability_markdown(
            traceability_rows
        ),
        Path("docs/reference/TRACEABILITY-MATRIX.json"): render_traceability_json(
            traceability_rows
        ),
    }
    stale: list[Path] = []
    for relative, rendered in expected.items():
        path = args.repo_root / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
            stale.append(relative)
    if stale:
        for path in stale:
            print(f"stale generated documentation: {path.as_posix()}")
        return 1
    print("controlled documentation and generated indexes are current")
    return 0

def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "validate":
        return _run_validate(args.repo_root, args.repository)
    if args.command == "registry":
        return _run_registry(args)
    if args.command == "traceability":
        return _run_traceability(args)
    if args.command == "snapshot-v1":
        return _run_snapshot(args)
    if args.command == "check":
        return _run_check(args)
    return 0
