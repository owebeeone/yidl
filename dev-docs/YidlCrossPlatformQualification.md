# Original-candidate cross-platform qualification

October 23, 2026. This record concerns the published candidate below. It does not
include the separately authorized constructor-annotation fix, whose edits were
released to start only after the Mac qualification finished.

## Authorized boundary and publication

The operational task covered inventory, GWZ commits/pushes, safe remote updates,
normal dependency setup/native builds, and explicit Python/Rust qualification on
the MacBook, ZT-RPI and DABEEST. Compiler, consumer, infrastructure and golden
repairs were outside this task. Dependencies were exercised as existing source
or candidate wheels, with no implementation edits to cure failures.

The documentation/review/archive work was committed only after the review-filing
checkpoint and the paper worker's terminal completion. Twelve archived documents
were recognized as byte-preserving Git renames; archive references were not repaired.

- YIDL candidate: `ee5ded0854aa5b1fc0ddfa7213b765009b63bb95`, pushed.
- Initial workspace checkpoint: `fb44c9cf2be6d28f5b14701a60b8743a39b2b220`.
- Published workspace after authorized Pyrocat detachment:
  `e5ac6a77ca1dadcfde4afe7554b55fad3835b4a6`.
- Pyrocat first commit: `ae28d69ae02768b53f80924cd006580ea81b96d2`, retained
  locally with its files/history. Its GWZ designation is inactive; no hosted
  repository was created and it was not pushed. Reattachment uses its retained
  `mem_pyrocat` designation through GWZ.
- Glade's remote was ahead of the local `a393ecb` commit. Its attempted push was
  refused; the successful workspace push excluded that member, preserved its
  remote history, and passed root dependency proof. No force operation was used.

## Exact source tuple

| Component | Candidate commit |
| --- | --- |
| Astichi | `ce47c629973d8e5a6340ceaa89b0bc3e8788d5fe` |
| YIDL | `ee5ded0854aa5b1fc0ddfa7213b765009b63bb95` |
| Lifecycle | `ee5ba633efdeac9fbdd74cfe67ecd975eab8a26d` |
| Dataclass | `202b01c879eb0ffb724158efe783b379fe522031` |
| Undoable | `ca68b8271841931506297db316911fe0ed3ad332` |
| Cache | `a4ae595e0f9835a86dadec3bedebd383ebf9ae2f` |

All compiler and consumer results below refer to these revisions. The Mac
root advanced from its initial checkpoint through detachment while this source
tuple stayed unchanged. The later
operational evidence commit is documentation-only; it does not redefine the
candidate or establish acceptance of the subsequent annotation fix or other concurrent work.

Pyrolyze was an unmodified reference dependency, not a repair target. Its
checkout was `092d055294df97666bee473126708c2868379c2d` on the Mac/Pi and
`0ae2e710eafe4a9b7729e2e40f83a2a19540911d` on Windows. The compiler/consumer
candidate table does not claim identical unrelated workspace/reference trees.

## Host/setup record

| Host | Interpreter and architecture | Workspace state used |
| --- | --- | --- |
| MacBook | CPython 3.12.12, macOS 26.6.2, arm64 | Existing canonical workspace; published root `e5ac6a7` after detachment |
| ZT-RPI (`weftpi`, Raspberry Pi 5 Model B Rev 1.0) | CPython 3.13.5, Debian/Linux 6.12.62, aarch64, glibc 2.41 | New canonical checkout on external XFS drive; published root `e5ac6a7` |
| DABEEST | CPython 3.13.5, Windows 11 build 26200, AMD64 | Existing clean `lcm-resume` root `f5f318a798b75a6a8bcd45bd4ee7ae54064052f2`; relevant existing members updated through GWZ |

The Pi had no canonical checkout in the bounded external-drive/home locations.
Existing benchmark/snapshot trees were preserved. After checking ownership,
absence of the destination, and 171 GiB free space, GWZ cloned the existing
canonical remote. Its symbolic HEAD selected `lcm-resume`; a new local `main`
branch was selected from the existing `origin/main` through GWZ. Generated root
lock staging was preserved in coordinated stash
`stash_unix_ms_1792704683434` before the root fast-forward. No stash was dropped,
no branch was replaced, and managed configuration was not edited by hand.
Subsequent materialization left generated root-lock staging uncommitted; source
checkouts retained the verified candidate revisions.

The existing RSA SSH identity supplied access to the private root through a
dedicated forwarded agent. No private key was copied. The original agent state
was restored. The dedicated agent was used only for this operation.

Windows' root update was blocked by unavailable HTTPS credentials after its
configured SSH-to-HTTPS rewrite. Its existing branch was preserved. The existing
Astichi/YIDL/Lifecycle members were fetched/pulled through GWZ and their exact
commits verified before testing. Its old membership lacked Cache, Dataclass and
Undoable source checkouts; current candidate wheels supplied those dependencies
and the installed-consumer checks below. This is not an assertion that Windows'
root or full workspace tuple matched the Mac/Pi root.

Build/test tools: Black 26.3.1 and Lark 1.3.1 on all hosts; pytest 9.0.3 on
the Mac shared environment and 9.1.1 on Pi/Windows and isolated Cache runs.
Hatchling 1.32.4 was available for prepared packaging tests. Rust toolchains
satisfied the native source's Rust 1.85 minimum; exact binary identity remains
the build qualification boundary.

## Results

P/S/F mean passed/skipped/failed. A failing suite remains a failure.

| Host/scope | Explicit Python | Explicit native Rust |
| --- | --- | --- |
| MacBook / yidl | 299 P / 2 S | 299 P / 2 S |
| MacBook / yidl-lifecycle | 433 P / 46 S / 1 F | 434 P / 46 S |
| MacBook / yidl-dataclass | 259 P / 3 S | 259 P / 3 S |
| MacBook / yidl_undoable | 350 P | 350 P |
| ZT-RPI / yidl | 299 P / 2 S | 299 P / 2 S |
| ZT-RPI / yidl-lifecycle | 432 P / 47 S / 1 F | 433 P / 47 S |
| ZT-RPI / yidl-dataclass | 260 P / 2 S | 260 P / 2 S |
| ZT-RPI / yidl_undoable | 350 P | 350 P |
| DABEEST / yidl | 299 P / 2 S | 299 P / 2 S |
| DABEEST / yidl-lifecycle | 423 P / 55 S / 2 F | 424 P / 55 S / 1 F |
| DABEEST / installed-consumers | 4 P | 4 P |

Standalone Cache service: MacBook **57 passed** in the clean environment;
ZT-RPI **55 passed, 2 skipped** under each requested environment. The two Pi
skips are explicitly macOS-only ACL regression/backend tests. These are
backend-independent service results. Windows did not run this standalone suite.

The four Windows installed-consumer checks were the packaged Dataclass first-use
example, Undoable first-use example, fresh Dataclass base regeneration, and fresh
Undoable base regeneration compared with packaged generated source. All four
passed under each explicit backend. These do not substitute for the absent full
Windows Dataclass/Undoable source suites. Their candidate wheel SHA-256 values, verified again on the receiving Windows host:

| Wheel | SHA-256 |
| --- | --- |
| Cache 0.1.0 | `cd59c988bb4f62cf4ef324330e60b71db3301ff33f919b91f6b42760f19c7e95` |
| Dataclass 0.1.0.dev0 | `812cebc67e2f28708cbf6abf32b23576e40bdcaa7b6cce466231bf0712f2b443` |
| Undoable 0.1.0 | `3504ebf11449d7a74368c37980a707d5e5c372b256679ace57d4838620a77c58` |

Cache is a backend-independent standard-library service. Its own cache-hit tests
exercise persistence intentionally; they are not evidence that a compiler ran.
Windows did not run the standalone Cache source suite.

## Backend and cache qualification

The Rust rows qualify Astichi's native Rust lower engine within YIDL's existing
compiler/generation path.

Each compiler/consumer suite ran in a new process with:

```text
ASTICHI_LOWER_ENGINE=python OR native-rust
YIDL_LIFECYCLE_CACHE=off
PYTHONDONTWRITEBYTECODE=1
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
python -m pytest -q -p no:cacheprovider -p yidl_qual_plugin
```

The temporary observation plugin checked
`select_effective_lower_engine().snapshot()` against the explicitly requested
engine before collection. It recorded interpreter/platform, native binary
SHA-256/capabilities and native extension C-call samples. Sampling stopped after
500 matching native calls to bound observation overhead. Native runs selected
`native-rust` with no engine fallback and recorded actual
`compile_validate_source`, `register_template_package_v2_source`, and
`lower_template_package_v2_from_registered_template` calls. This establishes
Rust compiler dispatch beyond importability or a requested environment value.
Individual tests may deliberately change selectors for gate/fallback assertions.

Automatic Lifecycle builder caching was disabled for backend qualification.
Canonical fixture subprocesses regenerated output into ignored actual-result
artifacts. Cache-specific tests deliberately install their own cache instances
or override configuration; their passing hits are separate cache coverage.

| Host | Native binary, relative to this YIDL repository | SHA-256 |
| --- | --- | --- |
| MacBook | `../astichi/native_engine/_astichi_native_engine.cpython-312-darwin.so` | `8266d234e9de1767b04c7a8291727b70164d3e6376f2562651252fa363f895c5` |
| ZT-RPI | `../astichi/native_engine/_astichi_native_engine.cpython-313-aarch64-linux-gnu.so` | `0332446883d2d9ecd68a8d5e23049db28aad99947cf5b189920cb43aaa0dc783` |
| DABEEST | `../astichi/native_engine/_astichi_native_engine.cp313-win_amd64.pyd` | `db81f125ed30c3b39eea2160c2f296493b2aee59ff712f187e9aa540d3572da6` |

All three were rebuilt using Astichi's documented `../astichi/native_engine/build.py`
route, not accepted as pre-existing binaries. Capabilities report
`rust-pyo3-core`, `cargo release`, ABI schema 1, RustPython parser 0.4.0, the full
lower-engine feature, and all required self-native production features including
`native.self_native.current_surfaces.v1`. The native capability version string
is `1.0.7`, matching the checked-in capability constant; Astichi distribution
metadata is `1.1.3`. The binary hash and exact source commit identify this tuple;
the native label alone is not a package-version qualification.

The [machine-readable companion](qualification/2026-10-23/results.json) records the observed selection, capabilities,
binary identity, sampled calls, result summaries and original-log digests.
Host-specific absolute paths are omitted from committed evidence.

## Failures, setup findings and follow-ups

1. **Confirmed Python owned-field source difference.** Lifecycle's
   `test_fixture_outputs_match_goldens[yidl_transactional_phase_h_owned.py]`
   produces `value__astichi_scoped_1` where the native golden uses `value`.
   The fixture subprocess succeeds; exact source comparison fails. The owning
   Lifecycle record `../yidl-lifecycle/dev-docs/L0CompletionVerification.md` already documents
   this difference. It was not normalized or counted as a pass. Suggested
   follow-up: an explicit owning decision on backend source equality versus
   separate canonical output. It blocks a clean Python Lifecycle suite, not
   the independently passing core compiler checks.

2. **Confirmed Windows cache diagnostic expectation mismatch.**
   `test_public_diagnostics_expose_failed_publication_and_exhausted_routes`
   expects `CacheHit` after fallback publication, but receives `CacheBypass`
   with `CacheLocationError("no usable cache location")`, under both backends.
   Cache storage explicitly bypasses persistence when `os.name != "posix"`
   or `O_NOFOLLOW` is unavailable. Suggested follow-up: reconcile this test's
   platform expectation with the declared persistence capability. This run
   does not establish an additional storage implementation defect. It blocks
   a clean Windows Lifecycle suite; core and four installed-consumer checks
   pass independently.

3. **Resolved Mac test-environment gaps.** Initial Dataclass/Undoable packaging
   tests lacked Hatchling. Installing that declared build dependency made the
   focused failed packaging checks pass, followed by clean full Python consumer
   reruns. Initial standalone Cache isolation assertions saw pre-imported
   `pyrolyze` in the shared environment before test code ran. A clean environment
   containing pytest and the candidate Cache package passed all 57 tests.
   These initial failures remain in the machine-readable record; no source was
   patched. Suggested follow-up: use isolated package environments for packaging
   and import-boundary qualification.

4. **Remaining coverage limits.** One interpreter was tested per host; this is
   not the complete declared Python-version matrix or an all-workspace test.
   Windows lacks full source consumer/cache-suite coverage in this run. The
   annotation defect and its incoming fix are a separate task, with separate
   candidate/acceptance requirements. No annotation fix, golden change,
   dependency repair, tag, registry upload or release publication was performed
   by this operational task.

5. **Remote default-branch drift (confirmed setup limitation).** The canonical
   remote's symbolic HEAD still selects `lcm-resume`, so a fresh ordinary clone
   starts with the older root composition. Selecting the already published
   `main` through GWZ resolved Pi setup without replacing either branch.
   Suggested separate administrative follow-up: confirm the intended default
   branch and align it if appropriate. No remote default was changed; this did
   not block the qualified Pi source tuple.

6. **Standalone YIDL distribution remains unqualified.** This matrix explicitly
   installed the candidate Astichi dependency. The candidate YIDL `pyproject.toml`
   declares Lark, but not Astichi, as a runtime dependency. That metadata omission
   is confirmed; this task did not rerun or certify a bare YIDL-only installation.
   Suggested follow-up: audit distribution dependencies and perform clean pinned
   installation before standalone package acceptance. This does not block the
   existing explicit workspace/dependency route exercised here, and no package
   metadata was repaired to make the tests run.

## Reproduction notes

From the YIDL repository, create/use the sibling workspace environment and
install the exact source tuple's editable packages. Install normal test/build
dependencies including pytest, Black 26.3.1, Hatchling and wheel. Astichi's
Python-only installation switch avoids accepting an implicit build; then run its
explicit documented native build with the selected interpreter:

```sh
uv venv --python 3.13 ../.venv
ASTICHI_SKIP_NATIVE_BUILD=1 uv pip install --python ../.venv/bin/python \
  -e ../astichi -e . -e ../yidl-lifecycle -e ../yidl-dataclass \
  -e ../yidl_undoable -e ../yidl-cache pytest black==26.3.1 hatchling wheel
../.venv/bin/python ../astichi/native_engine/build.py
```

Use the Windows environment's `Scripts/python.exe` spelling on Windows. Select
3.12 for the Mac run. In each owning repository, run its full configured pytest
scope under each explicit engine and the environment settings above. The
observation plugin is external test instrumentation; ordinary reproduction may
omit that plugin while using the same environment and checking the native gate:

```python
import os
from astichi.lower_engine.native import select_effective_lower_engine
selection = select_effective_lower_engine().snapshot()
assert selection["selected_engine"] == os.environ["ASTICHI_LOWER_ENGINE"]
assert selection["fallback_scope"] is None
print(selection)
```

For standalone Cache import-boundary coverage, use an isolated environment
without producer packages or startup hooks. Do not infer compiler execution
from Cache's intentionally persistent fixture hits. Preserve failed golden
output for comparison; do not rewrite expectations merely to get a green run.
