"""Read authoritative examples into public prose without publishing internal files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
TOKEN = re.compile(r"\{\{(source|consumer):([^|}]+)\|([a-z]+)\}\}")


def on_page_markdown(markdown: str, **kwargs: object) -> str:
    consumers = json.loads((ROOT / "docs/_snippets/consumers.json").read_text())

    def include(match: re.Match[str]) -> str:
        kind, identifier, language = match.groups()
        if kind == "consumer":
            item = consumers[identifier]
            source = item["text"]
            digest = hashlib.sha256(source.encode()).hexdigest()
            if digest != item["excerpt_sha256"]:
                raise ValueError(f"consumer excerpt drift: {identifier}")
            provenance = (
                f'\n[Source: {item["repository"]}, {item["revision"][:12]}, '
                f'{item["path"]}:{item["start"]}]({item["url"]})\n'
            )
        else:
            path_text, _, selection = identifier.partition("@")
            relative = Path(path_text)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"invalid source path: {identifier}")
            if relative.parts[0] not in {"example", "tests", "src"}:
                raise ValueError(f"non-public source inclusion: {identifier}")
            source = (ROOT / relative).read_text()
            if selection:
                first, last = (int(value) for value in selection.split(":"))
                source = "".join(source.splitlines(keepends=True)[first - 1 : last])
            provenance = f"\nSource authority: `{relative.as_posix()}`.\n"
        fence = "`" * max(
            3, max((len(run) + 1 for run in re.findall(r"`+", source)), default=0)
        )
        return f"{provenance}\n{fence}{language}\n{source.rstrip()}\n{fence}\n"

    return TOKEN.sub(include, markdown)
