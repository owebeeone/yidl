# Install a qualified environment

**Learning path · Step 3 of 4.** Build and install below, then check imports and
the backend. After those checks, continue to [Generate your first class](first-generator.md).
The external-directory exercise and cleanup sections are optional follow-up.

For a first visit, read [How YIDL works](../concepts/model.md) and
[generation stages](../concepts/generation-pipeline.md) before installing. The
next tutorial uses their distinction between a generator library and generated
application code.

YIDL requires **CPython 3.12 or newer (3.12+)**. For the demonstrated first-use
route, build YIDL **0.1.0 from this documentation candidate**, use its declared
Astichi **1.1.3** dependency, and select `ASTICHI_LOWER_ENGINE=python`.

The recorded reproduction environment used CPython **3.12.12** and installed
wheels without sibling imports. That exact patch version identifies the test
environment; installation requires 3.12+. Qualification of other Python, backend
and platform combinations is recorded separately in
[compatibility](../reference/compatibility.md). This development route does not
claim that `pip install yidl` fetches this compiler from a registry.

## Build and install explicitly

From a clone of this YIDL repository, with [uv](https://docs.astral.sh/uv/)
installed:

```sh
uv build --wheel --out-dir build/wheels
uv venv build/example-env --python 3.12
uv pip install --python build/example-env/bin/python \
  build/wheels/yidl-0.1.0-py3-none-any.whl
```

The example selects the CPython 3.12 series; you can select another installed
CPython 3.12+ interpreter with `--python`.

On Windows the interpreter is `build/example-env/Scripts/python.exe`; use that
path in place of `build/example-env/bin/python`. Native Windows and other Python
minors have not been qualified for these new documentation examples.

**Use a freshly built artifact:** current metadata installs Astichi 1.1.3
automatically. Older wheels can omit that dependency or lack
`yidl.concept_parser`. Rebuild from the intended checkout rather than diagnosing
a stale artifact as failure of the current compiler.

## Check imports and backend

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python -c \
 'import sys,yidl,astichi; from importlib.metadata import version; from yidl.concept_parser import compile_yidl_files; from astichi.lower_engine.native import select_effective_lower_engine; print(sys.version); print(yidl.__file__); print(astichi.__file__); print(version("yidl"),version("astichi")); print(select_effective_lower_engine().snapshot())'
```

Both imports should point inside the chosen environment. Expected requested and
selected engines are `python`, with no fallback reason. In PowerShell first set
`$env:ASTICHI_LOWER_ENGINE = "python"`; then run the Python command. The Unix
inline environment assignment syntax is not a PowerShell command.

## Optional: check an external copy { #run-outside-the-checkout }

**Optional installation check.** You can go straight to the
[tutorial](first-generator.md) after checking imports and the backend above.
Use this additional exercise to verify the installed packages also work from a
copied example outside the repository. It is not required before the tutorial.

The following commands are for a POSIX shell on macOS/Linux. Start in the YIDL
repository root, after creating the installed environment above. Capture that
interpreter's location **before** changing directory; resolving the environment
from the external directory would fail. The variables hold locations discovered
on your machine, so no machine-specific paths need to be edited into the example.

```sh
yidl_project_dir="$PWD"
yidl_python="$(build/example-env/bin/python -c 'import sys; print(sys.executable)')"
yidl_example_dir="$(mktemp -d)"
cp -R example/documentation "$yidl_example_dir/tutorial"
cd "$yidl_example_dir/tutorial"
env -u PYTHONPATH -u PYTHONHOME ASTICHI_LOWER_ENGINE=python \
  "$yidl_python" generate.py --out generated
```

You are now in the copied tutorial directory, so the script is `generate.py`,
not `example/documentation/generate.py`. The `.yidl` authority is found beside
that copied script. Its installed interpreter remains in the checkout's example
environment, reached through `yidl_python`; no sibling source imports are used.
The command clears ambient Python path overrides and selects the Python backend.

Expected observations include `Point: [3, 4]`, `parameters: ["x", "y"]` and an
engine snapshot selecting Python without fallback. The two files are
`generated/runtime.py` and `generated/model.py` **inside this external copy**.
The script's optional output default is `build/documentation` relative to the
current directory; the explicit `--out generated` above replaces that default.

This shell sequence is the qualified external-directory procedure; it is not a
PowerShell sequence or a new Windows/native qualification. Return to the checkout
before following [Generate your first class](first-generator.md):

```sh
cd "$yidl_project_dir"
```

Keep the installed environment for that tutorial. The copied example and its
generated output can remain in the temporary directory until you finish experimenting.

## Clean up after experimenting { #clean-up-the-walkthrough }

Keep the environment while following the tutorial; clean up when you have
finished experimenting.

First inspect the generated files you want to keep. These commands assume the
listed directories were created exclusively for this walkthrough; retain shared
or pre-existing environments, wheels and outputs. Remove only the destinations
you actually used.

If you followed the external-copy sequence, run this while still in its copied
tutorial directory. It removes only the generated output, retains the copied
`.yidl` and Python source, and returns to the original checkout:

```sh
rm -rf -- generated
cd "$yidl_project_dir"
```

From the repository root, these are disposable when created by this walkthrough:

```sh
rm -rf -- build/first build/example-env build/wheels
```

`build/first` is the first-generator tutorial's explicit output destination; it
may not exist if you only ran the external example. If you ran the script without
`--out`, remove its `build/documentation/` destination separately after checking
your current directory. Removing the environment also removes the packages
installed into it; no YIDL-specific uninstall command is needed.

Keep the original `example/documentation/` authored files. The external temporary
directory also still contains its copied sources; you may retain them for edits.
Do not remove the whole repository or a shared build directory as cleanup.

Use [compatibility](../reference/compatibility.md) to separate this installed
route from workspace native/cross-platform results. Source and templates are
executable inputs; use the same trust boundary as for Python modules.
