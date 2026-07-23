from __future__ import annotations

import json
from pathlib import Path
from typing import Any


NAMESPACE_ORDER = {"A": 0, "V1": 1, "V2": 2, "D": 3, "S": 4, "T": 5, "E": 6}


def reference_sort_key(code: str) -> tuple[int, int]:
    namespace, number = code.split("-", 1)
    return NAMESPACE_ORDER[namespace], int(number)


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
