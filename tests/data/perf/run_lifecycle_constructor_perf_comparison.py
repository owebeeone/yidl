from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    env = dict(os.environ)
    env["YIDL_PERF_TESTS"] = "1"
    command = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_lifecycle_decorator.py::"
        "test_lifecycle_generated_class_constructor_throughput_comparison",
        "-q",
        "-s",
    ]
    return subprocess.run(command, cwd=repo_root, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
