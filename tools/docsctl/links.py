from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from tools.docsctl.parser import github_anchor


MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\((?P<target>[^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6} (?P<title>.+)$")


@dataclass(frozen=True)
class LinkProblem:
    target: str
    message: str


def _anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if match:
            anchors.add(github_anchor(match.group("title")))
    return anchors


def validate_local_links(path: Path, root: Path) -> list[LinkProblem]:
    problems: list[LinkProblem] = []
    text = path.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group("target").strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        location, _, fragment = target.partition("#")
        destination = path if location == "" else (path.parent / unquote(location)).resolve()
        try:
            destination.relative_to(root.resolve())
        except ValueError:
            problems.append(LinkProblem(target, "link escapes the repository root"))
            continue
        if not destination.exists():
            problems.append(LinkProblem(target, "linked file does not exist"))
            continue
        if fragment and destination.suffix.lower() == ".md" and fragment not in _anchors(destination):
            problems.append(LinkProblem(target, f"anchor #{fragment} does not exist"))
    return problems
