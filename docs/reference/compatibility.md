# Qualified versions and limitations

YIDL's declared Python requirement is **CPython 3.12 or newer (3.12+)**, matching
`requires-python >=3.12`. The exact CPython 3.12.12 version below records the
environment used to reproduce these examples. The table describes executed
qualification; it does not restrict installation to that patch version or qualify
every Python/backend/platform combination.

**Documentation candidate:** YIDL revision `ee5ded0854aa5b1fc0ddfa7213b765009b63bb95`
for compiler/runtime bytes, package version 0.1.0; documentation changes are local
and uncommitted. Version metadata does not establish registry release readiness.

| Route | Python / SDK / backend | Evidence boundary |
| --- | --- | --- |
| New class/capture/control-flow/comparison recipes | CPython 3.12.12, installed current YIDL wheel, published Astichi 1.1.3, explicit Python | Fresh installed standalone runs plus canonical snapshots/behavior assertions |
| Generation and canonical golden suite | Same interpreter/Astichi, YIDL repository source | 239 passing checks; source path configured by pytest, not an installed-package claim |
| Existing original-candidate native/cross-host checks | Separately recorded Mac/Windows/Pi matrix | Do not transfer those results to these later documentation examples |
| Python 3.13 / 3.14 tutorial | Unqualified in this documentation run | Listed package classifiers are not evidence for this example |
| Native Rust tutorial | Unqualified until explicitly run with actual dispatch evidence | A request or auto-selection alone is insufficient |
| Consumer excerpts | Fixed owning revisions below; local accepted checkpoint evidence | Read-only explanatory excerpts, not reproduced package acceptance here |

## Known boundaries

| Case | Classification / usable disposition |
| --- | --- |
| Astichi omitted from YIDL dependency metadata | Confirmed packaging gap; explicit install documented |
| Old local dist artifact missing concept API | Confirmed stale-artifact hazard; build intended candidate |
| `yidl-compile` | Legacy transducer helper generator; Python concept API is current route |
| `yidl.embed` | Designed bootstrap, unavailable current public route |
| Live Lifecycle type annotations | Known failing arrangement; separate fix in progress, not accepted here; use qualified explicit string/Python route |
| Nested indexed scalar-expression chain (D17) | Unresolved mechanism; flat consumer alternative has bounded evidence |
| Static scalar carrier / bare references (D19) | Backend-sensitive observed boundary; no universal recipe or no-overhead claim |
| Mandatory empty holes | Explicit fillers required; demonstrated by zero-field and disabled-init tutorial |
| Mutable captures/template reuse | Separate ownership contracts; no general thread-safety or native failure-isolation proof |
| Callable providers/cycles | Consumer policy; no generic DDS resolver/reachability claim |
| Complex compound Python insertions | control_flow.py qualifies its exact interacting constructs; other positions/minors deferred |
| Nested two-record template edge environment | Not a general API claim; explicit generic evaluated fields are distinct |
| Two-consumer packaging reproduction | Consumer-specific evidence; not made a standalone tutorial prerequisite |

Existing original-candidate testing includes known Python Lifecycle source-hygiene
golden drift and Windows cache diagnostics failure. Neither is described as
universal success or silently fixed here. Consumer package checkpoints are not
proof of unrelated-domain generality.

The [example catalog](../examples/index.md) gives commands and ownership. The
[troubleshooting index](../troubleshooting/index.md) gives remedies without
promoting unresolved hypotheses into compiler defects.
