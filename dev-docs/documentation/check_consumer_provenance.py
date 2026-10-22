"""Optional curation check against fixed Git objects; not a docs-build dependency."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    records = json.loads((root / "docs/_snippets/consumers.json").read_text())
    for name, item in records.items():
        source = subprocess.check_output(
            [
                "git",
                "-C",
                str(root.parent / item["repository"]),
                "show",
                item["revision"] + ":" + item["path"],
            ]
        )
        if hashlib.sha256(source).hexdigest() != item["source_sha256"]:
            raise ValueError(f"source object drift: {name}")
        excerpt = "".join(
            source.decode().splitlines(keepends=True)[item["start"] - 1 : item["end"]]
        )
        if excerpt != item["text"]:
            raise ValueError(f"excerpt drift: {name}")
        if hashlib.sha256(excerpt.encode()).hexdigest() != item["excerpt_sha256"]:
            raise ValueError(f"excerpt hash mismatch: {name}")
    print(f"{len(records)} fixed-revision excerpts verified")


if __name__ == "__main__":
    main()
