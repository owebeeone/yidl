# FieldSpec helpers × YIDL design features

This document maps each **pyrolyze.lifecycle-style field helper** (schema /
FieldSpec surface) to **features described in the split YIDL design docs**:

- `docs/YIDLFrontendDesign.md`
- `docs/YIDLCodegenDesign.md`
- `docs/YIDLRuntimeClassModel.md`

It supports PRE_IMPL **Phase 1a** (audit sample vs design) and closure checks
that lifecycle needs are not silently absent from the design.

**Row source:** `dev-docs/lifecycle_field_catalog.py` (`FIELD_HELPERS` keys), same
order as `IMPLEMENTATION_ORDER` where the helper name matches a slice.

**Column source:** the split YIDL design docs (see glossary below). Cells are a
**first-pass** classification; they are intentionally conservative. Prefer `◐`
over `●` when the design only weakly implies ownership or the generated sample
has not yet confirmed the mapping. **TBD** marks where the design is silent or
the mapping needs lifecycle + sample verification during 1a.

### Cell legend (matrix cells)

| Symbol | Meaning |
|--------|---------|
| **●** | Design text clearly assigns this area primary responsibility for the helper’s runtime/codegen shape. |
| **◐** | Partial / shared: helper touches this area but design is thin, illustrative-only in `example/generated_factory_sample.py`, or split across areas. |
| **—** | Not applicable for typical semantics of this helper. |
| **?** | **TBD:** design gap, undefined split between harvester vs factory, or needs explicit § addition. |

### Coverage legend (row-level, before Notes)

**Coverage** summarizes how well **design + hand-crafted sample** currently
explain the lifecycle semantics for that row (Phase 1a fills this in; initial
values are a starting guess).

Coverage is not derived from the helper row alone. Ambient rows below are part
of the real coverage story and must be considered when evaluating whether a
helper is actually “covered.”

| Code | Meaning |
|------|---------|
| **B** | **Both:** `YIDLDesign.md` and `example/generated_factory_sample.py` align for the slice they claim (after 1a audit). |
| **D** | **Design-first:** design documents the shape; sample silent or out of scope for this helper (acceptable if recorded). |
| **S** | **Sample-first:** sample illustrates a pattern; design text is thin—close gap in design or demote sample claims. |
| **P** | **Partial:** known mismatch, thin §, or **◐** / **?** cells dominate—1a must produce explicit gap list. |
| **G** | **Gap:** lifecycle behavior not clearly owned in design (and usually not in sample)—high priority for 1b target-shape decision. |

Practical derivation rule:

- use **G** when a required responsibility is still `?` or clearly unowned
- use **P** when important responsibilities remain `◐` or ambient coverage is still thin
- use **D** when the design is explicit enough but the sample is intentionally silent
- use **S** when the sample implies a shape the design has not yet made explicit
- use **B** only when both design and sample are aligned for the claimed scope

---

### Column glossary (YIDL design features)

| ID | Design feature | Split design anchor |
|----|----------------|---------------------|
| **H** | Harvester → unbound field spec / binding into `spec` dict | `YIDLFrontendDesign.md` §2 |
| **S5** | Static helper / FieldSpec emission (schema layer per transducer) | `YIDLCodegenDesign.md` §3 |
| **PS** | **PublishedStore** — committed authoritative state | `YIDLRuntimeClassModel.md` §2 |
| **WS** | **WorkingStore** — transactional speculative state | `YIDLRuntimeClassModel.md` §2 |
| **IS** | **InstanceStore** / native homing on proxy (`__slots__`, no facade interception) | `YIDLRuntimeClassModel.md` §2, §7 |
| **HD** | **HiddenStore** / init-only ephemeral (InitVar-style) | `YIDLRuntimeClassModel.md` §2, §4 |
| **CV** | **CurrentView** — read published; managed immutability rules | `YIDLRuntimeClassModel.md` §3 |
| **WV** | **WorkingView** — copy-on-read / thaw-on-read, write to working | `YIDLRuntimeClassModel.md` §3 |
| **PX** | **Proxy** — routing between current vs working | `YIDLRuntimeClassModel.md` §3 |
| **I3** | **3-phase `__init__`** — allocate stores → wire views → sequential field init | `YIDLRuntimeClassModel.md` §4 |
| **CM** | **Commit / rollback** emission (`_lc_commit`, group roll-up, dirty tracking) | `YIDLRuntimeClassModel.md` §5, `YIDLCodegenDesign.md` §4 |
| **EL** | **Evict-last** staging (refcount / binding teardown order) | `YIDLRuntimeClassModel.md` §6 |
| **CL** | **Closure capture** — `exec` factory, `LOAD_DEREF`, spec locals | `YIDLCodegenDesign.md` §5 |
| **TR** | **AST transform** — behavior snippets → physical store access | `YIDLCodegenDesign.md` §2 |
| **TG** | **Named transaction groups** — multi-group begin/commit isolation | Runtime-class-model open issue; not yet first-class (**TBD** in split design) |

---

## Matrix (helpers × design areas)

| Helper | H | S5 | PS | WS | IS | HD | CV | WV | PX | I3 | CM | EL | CL | TR | TG | Cov | Notes |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|-------|
| **managed** | ◐ | ◐ | ● | ● | — | — | ● | ● | ● | ● | ● | — | ◐ | ◐ | ◐ | P | `TG`; [GAP-TG](./FieldSpecYIDLDesignMatrixGaps.md#gap-tg). |
| **const** | ◐ | ◐ | ● | ◐ | — | — | ● | — | ◐ | ◐ | — | — | ◐ | ◐ | — | P | working/current split; [GAP-COMBINATORIAL-PRECEDENCE](./FieldSpecYIDLDesignMatrixGaps.md#gap-combinatorial-precedence). |
| **static** | ◐ | ◐ | ◐ | ◐ | — | — | ◐ | ◐ | ◐ | ◐ | ◐ | — | ◐ | ◐ | — | G | class surface; [GAP-STATIC-CLASS-SURFACE](./FieldSpecYIDLDesignMatrixGaps.md#gap-static-class-surface). |
| **binding** | ◐ | ◐ | ● | ● | — | — | ● | ● | ● | ● | ● | ● | ◐ | ◐ | ◐ | P | evict-last + ownership; [GAP-BINDING-OWNED-MERGE](./FieldSpecYIDLDesignMatrixGaps.md#gap-binding-owned-merge). |
| **owned** | ◐ | ◐ | ● | ● | — | — | ● | ● | ● | ● | ● | ● | ◐ | ◐ | ◐ | P | ownership merge; [GAP-BINDING-OWNED-MERGE](./FieldSpecYIDLDesignMatrixGaps.md#gap-binding-owned-merge). |
| **transient** | ◐ | ◐ | ◐ | ● | — | — | ◐ | ● | ● | ● | ● | — | ◐ | ◐ | ◐ | P | ordering + runtime pressure; [GAP-INIT-ORDERING](./FieldSpecYIDLDesignMatrixGaps.md#gap-init-ordering), [GAP-TG](./FieldSpecYIDLDesignMatrixGaps.md#gap-tg). |
| **local_store** | ◐ | ◐ | ◐ | ◐ | ● | — | ◐ | ◐ | ● | ● | ◐ | — | ◐ | ◐ | — | P | native homing composition; [GAP-COMBINATORIAL-PRECEDENCE](./FieldSpecYIDLDesignMatrixGaps.md#gap-combinatorial-precedence). |
| **derived** | ◐ | ◐ | ◐ | ◐ | — | — | ◐ | ◐ | ● | ● | ◐ | — | ◐ | ◐ | — | P | ordering interactions; [GAP-INIT-ORDERING](./FieldSpecYIDLDesignMatrixGaps.md#gap-init-ordering), [GAP-COMBINATORIAL-PRECEDENCE](./FieldSpecYIDLDesignMatrixGaps.md#gap-combinatorial-precedence). |
| **initvar** | ◐ | ◐ | — | — | — | ● | — | — | ◐ | ● | — | — | ◐ | ◐ | — | G | hidden/init ordering + injectables; [GAP-INIT-ORDERING](./FieldSpecYIDLDesignMatrixGaps.md#gap-init-ordering), [GAP-INJECTABLE-REGISTRY](./FieldSpecYIDLDesignMatrixGaps.md#gap-injectable-registry). |
| **classvar** | ◐ | ◐ | ? | ? | — | — | ? | ? | ? | ? | ? | — | ◐ | ? | — | G | class surface gap; [GAP-STATIC-CLASS-SURFACE](./FieldSpecYIDLDesignMatrixGaps.md#gap-static-class-surface). |
| **commit_order_key** | ◐ | ◐ | ◐ | ◐ | — | — | — | — | ◐ | — | ● | — | ◐ | ◐ | ● | P | commit ordering + groups; [GAP-COMMIT-PIPELINE](./FieldSpecYIDLDesignMatrixGaps.md#gap-commit-pipeline), [GAP-TG](./FieldSpecYIDLDesignMatrixGaps.md#gap-tg). |
| **commit_validator** | ◐ | ◐ | ◐ | ◐ | — | — | ◐ | ◐ | ◐ | — | ● | — | ◐ | ◐ | ◐ | P | commit ordering; [GAP-COMMIT-PIPELINE](./FieldSpecYIDLDesignMatrixGaps.md#gap-commit-pipeline). |
| **on_before_commit** | ◐ | ◐ | — | — | — | — | — | — | ◐ | — | ● | — | ◐ | ◐ | ◐ | P | hook ordering; [GAP-COMMIT-PIPELINE](./FieldSpecYIDLDesignMatrixGaps.md#gap-commit-pipeline). |
| **on_after_commit** | ◐ | ◐ | — | — | — | — | — | — | ◐ | — | ● | — | ◐ | ◐ | ◐ | P | hook ordering; [GAP-COMMIT-PIPELINE](./FieldSpecYIDLDesignMatrixGaps.md#gap-commit-pipeline). |
| **on_after_rollback** | ◐ | ◐ | — | — | — | — | — | — | ◐ | — | ● | — | ◐ | ◐ | ◐ | P | rollback ordering; [GAP-COMMIT-PIPELINE](./FieldSpecYIDLDesignMatrixGaps.md#gap-commit-pipeline). |

---

## FieldSpec parameters × design areas

Each **keyword parameter** that appears on one or more helpers (`FIELD_HELPERS` in
`lifecycle_field_catalog.py`). Same columns as above; **Cov** as in legend.

| Parameter | H | S5 | PS | WS | IS | HD | CV | WV | PX | I3 | CM | EL | CL | TR | TG | Cov | Notes |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|-------|
| **compare** | ◐ | ● | ◐ | ◐ | — | — | — | — | — | — | ● | — | — | ● | — | P | Affects commit equality / dirty detection; annotation/tuple forms in lifecycle are **ambient** (see table below). |
| **tx_group** | ◐ | ◐ | — | — | — | — | — | — | ◐ | — | ● | — | — | ◐ | ● | G | multi-group semantics gap; [GAP-TG](./FieldSpecYIDLDesignMatrixGaps.md#gap-tg). |
| **default** | ◐ | ● | ◐ | ◐ | ◐ | ◐ | — | — | — | ● | ◐ | — | ● | ● | — | P | Static default vs factory; participates in **I3** ordering with other fields. |
| **default_factory** | ◐ | ● | ◐ | ◐ | ◐ | ◐ | — | — | — | ● | ◐ | — | ● | ● | — | P | Injectable names (`self`, `current`, `working`, initvars)—**TR** + harvester contract; `init=True` on **initvar** changes who runs first (**I3** / **HD**). |
| **initial_working** | ◐ | ● | — | ● | — | — | — | ◐ | ◐ | ● | ◐ | — | ● | ● | — | P | Seeds **WS** before user code; interaction with **transient** / **derived** order **?**. |
| **freeze** | ◐ | ● | ◐ | ◐ | — | — | ◐ | ◐ | ◐ | ◐ | ● | ◐ | ● | ● | — | P | Per-value freeze at commit (lifecycle); not whole-object **freezable** (see ambient). |
| **thaw** | ◐ | ● | ◐ | ● | — | — | ◐ | ● | ◐ | ◐ | ◐ | — | ● | ● | — | P | Managed thaw-on-read / working promotion; aligns with **WV** §3.2 narrative. |
| **state_factory** | ◐ | ● | — | ● | — | — | — | ● | ◐ | ● | ● | — | ● | ● | — | P | Advanced managed state shape; **WS** + **CM** coupling. |
| **state_copy** | ◐ | ● | — | ● | — | — | — | ● | ◐ | — | ● | — | ● | ● | — | P | Copy semantics into working; **CM** participation. |
| **working_default_factory** | ◐ | ● | — | ● | — | — | — | ● | ◐ | ● | ◐ | — | ● | ● | — | P | **transient** only; **WV** + **I3** must define ordering vs `default_factory`. |
| **init** (initvar) | ◐ | ◐ | — | — | — | ● | — | — | — | ● | — | — | ◐ | ◐ | — | G | init ordering gap; [GAP-INIT-ORDERING](./FieldSpecYIDLDesignMatrixGaps.md#gap-init-ordering). |

### Injectable / signature ambient (parameters)

| Concern | H | S5 | PS | WS | IS | HD | CV | WV | PX | I3 | CM | EL | CL | TR | TG | Cov | Notes |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|-------|
| **Factory/hook params** (`self`, `current`, `working`, `tx_group`, `previous`, initvar names per `COMMON_PARAM_NOTES` in catalog) | ◐ | ◐ | — | — | — | ◐ | — | — | — | ● | ● | — | ◐ | ◐ | ◐ | G | injectable registry gap; [GAP-INJECTABLE-REGISTRY](./FieldSpecYIDLDesignMatrixGaps.md#gap-injectable-registry). |

---

## Ambient features (non–helper-entrypoint)

Behavior that **lifecycle** applies without a dedicated `managed()`-style helper name,
or that spans **all** fields. Same column IDs + **Cov**.

These rows are part of coverage, not an appendix. A helper row should not be
treated as complete if the corresponding ambient behavior remains partial or
undefined.

| Ambient feature | H | S5 | PS | WS | IS | HD | CV | WV | PX | I3 | CM | EL | CL | TR | TG | Cov | Notes |
|-----------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|-------|
| **Field-spec MRO merge** (subclass overrides / inherits helper params) | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | — | ◐ | ◐ | ◐ | P | MRO merge gap; [GAP-MRO-MERGE](./FieldSpecYIDLDesignMatrixGaps.md#gap-mro-merge). |
| **Transaction enlistment** (only contexts that promote to working; DEFAULT group) | ◐ | — | ◐ | ● | — | — | — | — | ● | ◐ | ● | — | — | — | ◐ | P | **RuntimeExtractionPlan**; design sample shows `TransactionManager` usage. |
| **Annotation-driven compare** (e.g. tuple / identity hints resolved at compile time) | ◐ | ◐ | — | — | — | — | — | — | — | — | ● | — | — | ◐ | — | G | ambient annotation gap; [GAP-ANNOTATION-DRIVEN-BEHAVIOR](./FieldSpecYIDLDesignMatrixGaps.md#gap-annotation-driven-behavior). |
| **Per-field `freeze` / `thaw` callables** (value-level, not whole-object) | ◐ | ● | ◐ | ◐ | — | — | ◐ | ● | ◐ | ◐ | ● | ◐ | ● | ● | — | P | `lifecycle.py` states it does **not** use `pyrolyze.freezable` whole-object clones; design §3.2 / managed params should say the same to avoid confusion with a different “freezable” product. |
| **Whole-object frozen/thawed graph** (explicit non-goal in current lifecycle) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | D | Document as **out of scope** for this matrix unless YIDL chooses to revive it. |
| **Copy-on-read / thaw-on-read default path** (managed without explicit `thaw`) | — | — | ◐ | ● | — | — | ◐ | ● | ● | ◐ | ◐ | — | — | ● | — | P | **WV** behavior when `thaw` omitted—must match lifecycle descriptor tables. |

---

## Combinatorial complexity (“third dimension”)

Some correctness is not **one transducer = one column**, but **interaction** between
two (or more) field kinds, parameters, or commit-phase hooks. If the design only
lists transducers in isolation, codegen may be **ambiguous** about which rule wins
or which **order** runs.

**Hypothesis / risk note (for 1a to confirm against lifecycle):** YIDL may need
**composed transducers** or an explicit **precedence / ordering layer** in the
spec so the compiler emits a single deterministic pipeline per class—not N
independent snippets.

| Interaction (examples) | Risk | Design mitigation direction |
|--------------------------|------|------------------------------|
| **derived** reads **managed** / **transient** / **local_store** while those fields still in **I3** | Wrong default visible; wrong store | Fix **global declaration order** in spec; **I3** unrolling order = total order over all fields; derived slots after dependencies (explicit `depends_on` or topo-sort). |
| **binding** + **owned** (or multiple bindings) on overlapping value graph | Double free / refcount / **EL** order | **§4.2** evict-last must be **global** per commit step, not per-field in isolation; may need graph merge in IR. |
| **commit_order_key** + **commit_validator** + **on_before_commit** | Relative order undefined | Single **commit pipeline** table in design: order keys → validators → hooks → store writes → **EL**. |
| **multi-group `tx_group`** + field A in group G1 reading field B in G2 mid-transaction | Stale / inconsistent reads | **TG** § must define visibility rules (or forbid); may require composable “read barrier” transducer. |
| **local_store** + **derived** reading peer field | Routing: instance vs facade | **IS** + **PX** interaction; view delegation rules must be composed, not per-kind ad hoc. |
| **initvar** + **default_factory** on another field referencing initvar | Injection and **I3** phase boundaries | **HD** teardown vs **I3** phase 3: lifecycle rules must become explicit **phases × field kind** matrix. |
| **transient** `working_default_factory` + **initial_working** + **managed** default | Multiple writers to **WS** at init | Precedence: which factory wins and when—**?** until specified. |

**Exit for this section in Phase 1a:** either (1) each row is **falsified** (“lifecycle forbids combo” / “order is defined in code at …”), or (2) a **gap** is filed and **1b** chooses: new **YIDLDesign** §, composed transducer syntax, or runtime restriction.

---

## Using this doc in Phase 1a

1. **Enumerate gaps:** any **?** cell, **G** coverage, or combinatorial row without
   lifecycle disposition → design or sample follow-up.
2. **Sample pass:** for each **●** / **◐**, check `example/generated_factory_sample.py`
   for the **Bar** field set; update **Cov** to **B** / **D** / **P** honestly.
3. **Regenerate** when `lifecycle_field_catalog.FIELD_HELPERS` changes; add **ambient**
   rows when new cross-cutting lifecycle behavior is discovered.
4. **Combinatorial** table: link each confirmed issue to a
   **CodegenRequirements.md**, **YIDLFrontendDesign.md**, **YIDLCodegenDesign.md**,
   or **YIDLRuntimeClassModel.md** edit or explicit “forbidden combination” in
   spec.

---

## Related docs

- `dev-docs/lifecycle_field_catalog.py` — helper names and kwargs.
- `docs/YIDLFrontendDesign.md` — frontend design.
- `docs/YIDLCodegenDesign.md` — generator/codegen design.
- `docs/YIDLRuntimeClassModel.md` — runtime/class model.
- `docs/YIDLDesign.md` — historical reference only.
- `dev-docs/RuntimeExtractionPlan.md` — runtime vs decoration-time split in lifecycle.
- `dev-docs/PRE_IMPL_STUDY_IMPL_PLAN.md` — Phase 1a audit expectations.
- `dev-docs/CodegenRequirements.md` — generator / IR implications.
