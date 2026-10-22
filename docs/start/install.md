# Install a qualified environment

YIDL requires **CPython 3.12 or newer (3.12+)**. For the demonstrated first-use
route, build YIDL **0.1.0 from this documentation candidate**, install Astichi
**1.1.3** explicitly, and select `ASTICHI_LOWER_ENGINE=python`.

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
  build/wheels/yidl-0.1.0-py3-none-any.whl 'astichi==1.1.3'
```

The example selects the CPython 3.12 series; you can select another installed
CPython 3.12+ interpreter with `--python`.

On Windows the interpreter is `build/example-env/Scripts/python.exe`; use that
path in place of `build/example-env/bin/python`. Native Windows and other Python
minors have not been qualified for these new documentation examples.

**Astichi must be explicit:** current YIDL metadata lists Lark and omits Astichi,
even though the concept compiler imports it. An old local `dist/` wheel may also
lack `yidl.concept_parser`. Rebuild from the intended checkout; do not diagnose
that stale artifact as failure of the current compiler.

## Check imports and backend

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python -c \
 'import sys,yidl,astichi; from importlib.metadata import version; from yidl.concept_parser import compile_yidl_files; from astichi.lower_engine.native import select_effective_lower_engine; print(sys.version); print(yidl.__file__); print(astichi.__file__); print(version("yidl"),version("astichi")); print(select_effective_lower_engine().snapshot())'
```

Both imports should point inside the chosen environment. Expected requested and
selected engines are `python`, with no fallback reason. In PowerShell first set
`$env:ASTICHI_LOWER_ENGINE = "python"`; then run the Python command. The Unix
inline environment assignment syntax is not a PowerShell command.

## Run outside the checkout

Copy `example/documentation/` to an otherwise empty directory. From that copy,
run its `generate.py` with the **same installed interpreter**, setting the engine
to Python. The script resolves `classes.yidl` relative to itself and writes only
the chosen output directory. No Astichi, consumer or GWZ checkout is needed.

```sh
ASTICHI_LOWER_ENGINE=python build/example-env/bin/python \
  example/documentation/generate.py --out build/first
```

Expected observations: `Point: [3, 4]`, `parameters: ["x", "y"]`, and an engine
snapshot selecting Python. Continue with the [tutorial](first-generator.md).

Use [compatibility](../reference/compatibility.md) to separate this installed
route from workspace native/cross-platform results. Source and templates are
executable inputs; use the same trust boundary as for Python modules.
