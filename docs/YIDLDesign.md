# **V2 YIDL Compiler Design: Historical Reference**

> Historical reference only.
>
> This document is preserved as the original monolithic design note. It is no
> longer the normative source of truth.
>
> Current normative design is split across:
>
> - `docs/YIDLFrontendDesign.md`
> - `docs/YIDLCodegenDesign.md`
> - `docs/YIDLRuntimeClassModel.md`
>
> Keep this file for history and context, but prefer the split design docs for
> active design, coverage review, and follow-on edits.

## **1\. Executive Summary**

The Pyrolyze Lifecycle V2 engine transitions from runtime metaprogramming (descriptors, metaclasses, dynamic \_\_dict\_\_ manipulation) to a purely declarative, **Ahead-of-Time (AOT) Metacompiler** model.

The core of this system is the **YIDL compiler**. It reads a strict schema of field behaviors (Transducers) and dynamically generates raw, slotted, highly optimized Python code for multi-state object tracking.

This document serves as the architectural blueprint for building the compiler, detailing the pipeline, the memory model, and the generation strategies required to emit the final exec() strings.

## **2\. The Compilation Pipeline**

The system operates in five distinct phases, moving from user-facing Python down to raw AST manipulation, and back up to executable Python.

### **Phase 1: The Harvester (Python \-\> Dict)**

Triggered by the @managed\_context decorator.

* Scans the UserBaseClass for lifecycle field declarations (e.g., a: int \= managed()).  
* Extracts explicit arguments (default, freeze, thaw, etc.).  
* Resolves class MRO to inherit configurations from parent classes.  
* **Output:** An unbound dictionary of field specifications.

### **Phase 2: The Lexer & Parser (YIDL \-\> Typed AST)**

Instead of relying on third-party frameworks like textX or Lark, the system uses a bespoke, zero-dependency parser to read the `.yidl` specification.

* **The Lexer:** An indentation-aware line scanner. It uses %% fences to explicitly identify and "swallow" raw Python code blocks, perfectly preserving their internal whitespace while stripping YIDL comments.  
* **The Parser:** A pure Python recursive descent parser that converts the lexer's token stream into strongly-typed dataclass nodes (TransducerNode, BehaviorNode, CodeNode).  
* **Output:** A strict, hierarchical Abstract Syntax Tree (AST) representing the YIDL rules engine.

### **Phase 3: The AST Transformer (Code Snippet \-\> Contextual Python)**

The compiler bridges the gap between the abstract YIDL spec and the physical memory layout using Python's native ast module.

* It parses the isolated CODE\_SNIPPET blocks from the spec (e.g., store.write(val)) into native Python ASTs.  
* A custom ast.NodeTransformer intercepts abstract calls (.read(), .write(), .has()) and rewrites them into direct physical memory accesses based on context aliases (e.g., converting store.write(val) to self.\_lc\_working\['field\_name'\] \= val).  
* It unparses the modified AST back into raw Python strings.  
* **Output:** Context-aware, highly optimized Python strings ready for injection.

### **Phase 4: The String Builder (Transducer Nodes \-\> Python Factory)**

The compiler iterates over the Transducer Nodes and pieces together the final Python source code string.

* Translates logical **Surfaces** (Current, Working, Proxy) into class definitions.  
* Translates logical **Stores** (Published, Working, Instance) into slotted memory classes.  
* Unrolls transformed behavior snippets into the specific generated methods (\_\_init\_\_, @property, \_lc\_commit).  
* **Output:** A single string representing a Python factory function (e.g., build\_class).

### **Phase 5: Closure Capture & Execution (String \-\> Executable Class)**

* The generated string is executed via Python's built-in exec().  
* The factory function is invoked, receiving a spec\_dict containing the user's UserBaseClass, lambdas, and factory functions.  
* The functions are unpacked into local variables, securely captured by the generated classes as highly optimized Python closures (LOAD\_DEREF).  
* **Output:** The final, executable Proxy class returned to the user.

## **3\. The Multi-Store / Multi-Facade System**

To achieve deterministic "Method Contexts" (allowing a user's method to seamlessly target the current or working state), the compiler implements a **Multi-Facade MRO Architecture**.

### **3.1. Physical Stores (Memory)**

Stores hold the actual data. The compiler guarantees that stores contain NO logic, only \_\_slots\_\_ and initial MISSING sentinels.

* **PublishedStore (\_lc\_published):** Holds the authoritative, committed state.  
* **WorkingStore (\_lc\_working):** Holds speculative, uncommitted transactional state.  
* **InstanceStore (self):** The primary proxy object itself. Used for "Homed" fields (like LocalStore) to achieve raw Python performance without interception overhead.  
* **HiddenStore:** Ephemeral storage strictly bounded to the \_\_init\_\_ execution stack (used for InitVar).

### **3.2. Logical Facades (Surfaces)**

Facades provide the viewing lenses. The compiler generates three distinct classes that all inherit from the user's UserBaseClass, guaranteeing correct MRO for user-defined methods.

* **CurrentView:** A slotted class that exclusively reads from the PublishedStore. Mutating managed fields here throws an error.  
* **WorkingView:** A slotted class that implements "Copy-on-Read" (Thaw-on-Read) logic. It checks the WorkingStore, falls back to the PublishedStore, and routes mutations safely to the WorkingStore.  
* **Proxy (Main):** The class instantiated by the user. It evaluates the global transaction manager (tx\_active()) and dynamically routes self.field access to either self.working or self.current.

## **4\. Code Generation Strategies & Guardrails**

The compiler must guarantee absolute safety during initialization and transactions. It achieves this through strict sequence generation.

### **4.1. The 3-Phase Initialization Rule**

To handle default\_factory dependencies safely (e.g., field b relies on field a being initialized), the compiler must generate the \_\_init\_\_ method in three unbreakable phases:

1. **Store Allocation:** Instantiate \_PublishedStore and \_WorkingStore. (All memory exists, holding MISSING).  
2. **View Wiring:** Instantiate CurrentView and WorkingView, passing in the stores. Setup circular fallbacks (e.g., self.working.current \= self.current). *At this point, routing infrastructure is fully live.*  
3. **Sequential Unrolling:** Iterate through the AST in top-to-bottom declaration order, injecting the behavior Init code blocks. If a factory relies on self.current.a, it will succeed because phase 2 established the routing.

### **4.2. Safe Pointer Eviction (The "Evict Last" Pattern)**

For reference-counted or resource-bound fields (defined in BindingField), the generated code must prevent Zombie pointers or cascading garbage-collection side effects during mutation or commit phases.

The compiler's generation templates must sequence operations identically to this pattern:

1. **Stage:** Increment references for new inbound values.  
2. **Update Structures:** Update physical memory (WorkingStore or PublishedStore) and set MISSING markers where appropriate. The data tree is now consistent.  
3. **Evict LAST:** Trigger dec\_ref() or \_close() on the orphaned value.

### **4.3. Native Homing Optimization**

When the compiler encounters a home: InstanceStore parameter (e.g., in LocalStoreField), it bypasses the Published and Working memory architectures entirely.

* It injects the field name directly into the Proxy class \_\_slots\_\_.  
* It generates native @property lookups on the Views that reach up to self.\_main\_instance.\<field\>.  
* It emits get: native and set: native inside the Proxy, meaning NO @property is generated, allowing the Python interpreter to interact with it as a raw, slotted attribute at maximum C-level speed.

## **5\. Two-Phase Integration: FieldSpec Helpers and the Generated Factory**

Author-facing code stays familiar (`@managed_context`, `managed()`, `binding()`, …), but implementation splits into **two cooperating artifacts**:

### **5.1. What the YIDL compiler emits (static, per transducer kind)**

From the `.yidl` transducer definitions, the compiler generates **FieldSpec / LCKind-style helpers** — the small dataclass constructors and `managed(...)`, `binding(...)`, etc. callables that the harvester recognizes. That is the **schema layer**: it encodes *which* inputs exist and *which* surfaces apply, without embedding the full memory layout.

Today’s `yidl-compile` pipeline only implements a narrow slice of this (API stub generation); the full compiler will grow to match every transducer and behavior in the spec.

### **5.2. What the generated decorator emits (per user class)**

The **`@managed_context`** (or successor) decorator **harvests** the user class: field names, annotations, and the return values of those helpers. It then **binds** that information into a **`spec` dict** and passes it into a **generated factory function** produced by Phase 4–5:

```text
def build_<UserClass>_<...>(<user>_spec):
    # Unpack spec into locals for closure capture (MISSING, UserBaseClass, thaw/freeze, factories, …)
    # 1. Slotted PublishedStore / WorkingStore (and any other stores)
    # 2. CurrentView / WorkingView facades (inherit UserBaseClass)
    # 3. Proxy class: __init__ (3-phase init), routed @properties, _lc_commit / rollback per group
    return <ProxyClass>
```

The factory is **`exec`’d once per managed class** (or loaded from a cached string). Invoking `build_…(spec)` returns the concrete **proxy type** the user instantiates. Nested classes close over the unpacked locals so per-field `freeze` / `thaw` / `default_factory` run as **native closures** (`LOAD_DEREF`) instead of living in per-instance dicts or generic descriptor tables.

### **5.3. Skeleton reference in the repo**

The intended shape of the emitted factory (stores, views, proxy, commit unrolling, binding “evict last”) is spelled out concretely in:

* `example/generated_factory_sample.py` — illustrative `build_bar_class(bar_spec)` for a tiny field set.

That file is **not** produced by the current CLI; it is the **target** for the string builder until the generator lands.
