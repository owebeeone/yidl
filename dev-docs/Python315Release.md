# Python 3.15 release qualification

The operator requested Python 3.15 in the matrices and patch releases for YIDL,
Lifecycle, Dataclass and Undoable on 27 October 2026. Editable scope is those
four members, their consumer compatibility changes, tests, packaging and release
automation. Astichi, Cache and other dependencies remain reference-only unless a
concrete failure requires a separate scope decision. Releases use Gearu and each
repository's trusted publication workflow.

YIDL's unchanged baseline passed on final CPython 3.15.2 with the explicit Python
backend: **297 passed, 4 skipped**. The documented downstream Lifecycle smoke
remained excluded from this compiler-only run, as in existing release gates; it
will be checked with the combined downstream tuple. No compiler implementation
change was needed by this baseline. This patch adds the classifier and matrix
entry and updates the package/runtime version through Gearu.

Target release: **0.1.2**. This is separate from the earlier 0.1.1 README patch.
Publication and fresh registry installation must be confirmed before downstream
members adopt the exact new YIDL pin. Current local evidence is not new independent
review or proof of all backend/platform combinations.

## Completed publication

Published **0.1.2** using Gearu 0.1.1. Release commit:
`ff76068d4c312b9cc92979ac285d9112951400e0`.

- GitHub release: https://github.com/owebeeone/yidl/releases/tag/v0.1.2
- Successful trusted publication: https://github.com/owebeeone/yidl/actions/runs/40494655031
- PyPI wheel and source distribution: https://pypi.org/project/yidl/0.1.2/

Candidate and exact-commit checks passed for every declared Python minor.
Local and Ubuntu source matrices include 3.12, 3.13, 3.14 and 3.15.
This member's release gate uses the explicit Python lowering backend.

A fresh registry-only installation of all four released packages passed the
combined integration probe on CPython 3.15.2 with each explicit backend. It
verified freezing, Lifecycle fields/annotations, transactions, rollback, history
navigation/branching, shared comparisons and installed Dataclass/Undoable
regeneration. The previously excluded YIDL downstream Lifecycle smoke separately
passed against the published pair on 3.15.2.

The cross-package evidence, per-cell counts, workflow/tag checks and PyPI artifact
SHA256s are recorded at:
https://github.com/owebeeone/yidl-dataclass/blob/main/docs/validation/releases/python315.json

These are qualification results, not new independent reviews or new performance/
cost measurements. Windows 3.15 remains outside this pass: Astichi 1.1.3 has no
cp315 Windows wheel. No Astichi implementation change was made.
