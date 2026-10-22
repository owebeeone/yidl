"""Execute public catalog entries in fresh processes with installed packages."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from astichi.lower_engine.native import select_effective_lower_engine
import astichi
import yidl


@dataclass(frozen=True)
class Case:
    path: str
    arguments: tuple[str, ...]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, default=Path("build/documentation-evidence.json")
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cases = [
        Case("example/documentation/generate.py", ()),
        Case("example/documentation/generate.py", ("--extended",)),
        Case("example/documentation/generate.py", ("--empty",)),
        Case("example/documentation/generate.py", ("--disabled",)),
        Case("example/documentation/captures.py", ()),
        Case("example/documentation/control_flow.py", ()),
        Case("example/documentation/comparison.py", ()),
    ]
    fixtures = [
        "yidl_imported_concepts",
        "yidl_update_a_multi_source_from",
        "dds_composite_identity_lookup",
        "dds_matcher_productions",
        "dds_lifecycle_callable_facts",
        "yidl_lark_v2_vertical",
    ]
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)
    environment["ASTICHI_LOWER_ENGINE"] = "python"
    observations: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="yidl-documentation-") as temporary:
        temporary_root = Path(temporary)
        authority = temporary_root / "tutorial"
        shutil.copytree(root / "example/documentation", authority)
        for index, case in enumerate(cases):
            script = authority / Path(case.path).name
            command = [sys.executable, str(script), *case.arguments]
            if script.name == "generate.py":
                command.extend(["--out", str(temporary_root / str(index))])
            completed = subprocess.run(
                command,
                cwd=temporary_root,
                env=environment,
                capture_output=True,
                text=True,
                check=True,
            )
            observations.append(
                {
                    "source": case.path,
                    "arguments": case.arguments,
                    "cwd": "outside-checkout",
                    "exit": completed.returncode,
                    "stdout": completed.stdout,
                }
            )
        for name in fixtures:
            relative = f"tests/data/gold_src/{name}.py"
            completed = subprocess.run(
                [sys.executable, str(root / relative), str(temporary_root / name)],
                cwd=root,
                env=environment,
                capture_output=True,
                text=True,
                check=True,
            )
            observations.append(
                {"source": relative, "cwd": "repository", "exit": completed.returncode}
            )
    for module in (yidl, astichi):
        if "site-packages" not in str(Path(module.__file__).resolve()):
            raise ValueError(
                "qualification requires installed packages, not source imports"
            )
    evidence = {
        "python": sys.version.split()[0],
        "yidl": importlib.metadata.version("yidl"),
        "astichi": importlib.metadata.version("astichi"),
        "engine": select_effective_lower_engine().snapshot(),
        "origins": "both installed site-packages; no PYTHONPATH in child processes",
        "cases": observations,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"{len(observations)} installed-package examples passed")


if __name__ == "__main__":
    main()
