# Generated code cache plan remediation 1

Baseline: YIDL `a3222bb44e2a5709dde9a680bca1ff6ab62eba96`, Lifecycle
`c2502f1a7a565624f20cf930fde92f581b123e9f`.

Consistency reported GO with no findings. Safety reported NO-GO with one
bounded blocking finding, P2-1. No blind convergence occurred.

## Disposition and closure

Safety P2-1: amend the existing invalidation contract to require a verified
immutable producer epoch. Initial editable/source and uncertain-provenance
cases bypass persistent reads and writes. Installed dependencies need coherent
provenance for both loaded modules and deferred imports; package versions and
disk rehashes alone are insufficient. Lost guarantees invalidate the epoch and
forbid publishing under the old request identity.

Closure: Safety must retrace its fingerprint-then-replacement counterexample
and the already-loaded-old-module/new-disk reverse case against the amended
policy. Both become explicit future acceptance tests. Consistency rechecks
compatibility with the existing plan and the narrowed initial cache coverage.
Neither report closes the finding without the reviewers' revised verdicts.

Scope: one documentation patch, no runtime implementation or activation.
