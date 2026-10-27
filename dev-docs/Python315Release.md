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
