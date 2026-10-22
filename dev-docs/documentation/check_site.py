"""Check active built HTML links, anchors, assets, search, and public exclusions."""

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


@dataclass
class Page(HTMLParser):
    anchors: set[str] = field(default_factory=set)
    links: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        HTMLParser.__init__(self, convert_charrefs=True)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("id", "name"):
            if values.get(key):
                self.anchors.add(values[key])
        for key in ("href", "src"):
            if values.get(key):
                self.links.append(values[key])


def check(root: Path) -> dict[str, int]:
    root = root.resolve()
    pages: dict[Path, Page] = {}
    for path in root.rglob("*.html"):
        source = path.read_text()
        if re.search(r"/(?:Users|Volumes)/|[A-Za-z]:\\\\", source):
            raise ValueError(f"machine path leaked into {path.relative_to(root)}")
        if "{{source:" in source or "{{consumer:" in source:
            raise ValueError(f"unresolved inclusion in {path.relative_to(root)}")
        parser = Page()
        parser.feed(source)
        pages[path] = parser
    failures: list[str] = []
    checked = 0
    for path, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            raw = unquote(url.path)
            if raw.startswith("/yidl/"):
                target = root / raw.removeprefix("/yidl/")
            elif raw.startswith("/"):
                failures.append(f"{path.relative_to(root)}: base-path-unsafe {href}")
                continue
            else:
                target = path.parent / raw if raw else path
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(root) or not target.exists():
                failures.append(f"{path.relative_to(root)}: missing {href}")
            elif (
                url.fragment
                and target in pages
                and unquote(url.fragment) not in pages[target].anchors
            ):
                failures.append(f"{path.relative_to(root)}: missing anchor {href}")
            checked += 1
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(
            part in {"validation", "dev-docs", "history", "_snippets"}
            for part in relative.parts
        ):
            failures.append(f"excluded content leaked: {relative}")
        if path.suffix in {".py", ".log", ".md"}:
            failures.append(f"unexpected source/evidence asset: {relative}")
    search = json.loads((root / "search/search_index.json").read_text())
    entries = search["docs"]
    if not any("FieldName" in entry["text"] for entry in entries):
        failures.append("search corpus lacks FieldName")
    if not any(
        entry["location"].startswith("start/first-generator/") for entry in entries
    ):
        failures.append("quick start missing from search")
    if not any(
        "search" in name.name and name.suffix == ".js" for name in root.rglob("*.js")
    ):
        failures.append("search JavaScript missing")
    if failures:
        raise ValueError("\n".join(failures))
    return {
        "html_pages": len(pages),
        "local_links_assets": checked,
        "search_entries": len(entries),
    }


if __name__ == "__main__":
    print(json.dumps(check(Path(sys.argv[1])), sort_keys=True))
