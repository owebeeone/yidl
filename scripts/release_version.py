"""Synchronize or verify YIDL's public version during GEARU preparation."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import re
import tomllib


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("sync", "verify"))
    parser.add_argument("version")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    if project["version"] != args.version:
        raise SystemExit("Requested version does not match pyproject.toml")
    path = root / "src/yidl/__init__.py"
    source = path.read_text()
    assignments = [
        node
        for node in ast.parse(source).body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "__version__" for t in node.targets)
    ]
    if len(assignments) != 1:
        raise SystemExit("Expected one top-level __version__ assignment")
    if ast.literal_eval(assignments[0].value) == args.version:
        return
    if args.mode == "verify":
        raise SystemExit("yidl.__version__ does not match pyproject.toml")
    updated, count = re.subn(
        r'^__version__ = "[^"\n]+"$',
        f'__version__ = "{args.version}"',
        source,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise SystemExit("Expected the owned version assignment format")
    path.write_text(updated)


if __name__ == "__main__":
    main()
