# Observations on Concept Composition and Specialization

This note records an exploratory discussion about a possible general technique for modeling interrelated problems. It is not a design contract or a claim that the technique has been proven. The examples are YIDL and YIDL Lifecycle, with C++ and GARNs as comparisons. The scope is this note only; those systems are reference material.

## Motivation

In the development of YIDL Lifecycle, attempts to divide the problem into independently solvable pieces encountered interdependencies across the pieces. The resulting question was how to model the problem as a whole while still expressing its parts in manageable units. The user reports that presenting the interrelated problem to an LLM led to a workable YIDL Lifecycle solution. This is an account of the development experience, not a controlled experiment.

## Observations

1. **Encapsulation.** A concept can provide a boundary for a related body of information and behavior. A YIDL concept packages declarations and rules; C++ classes and GARNs modules provide different examples of boundaries. The mechanisms are analogous in role, not identical.

2. **Composition.** Concepts can be combined to form a more specific or larger concept. Their relationships describe how their contributions fit together. Composition allows the overall model to span concerns that cannot be solved independently.

3. **Selection and specialization.** General behavior can be refined for particular combinations. YIDL matchers select contributions based on facts; C++ full and partial template specializations, and the corresponding GARNs direction, offer analogous ways to select more specific behavior. The exact matching and precedence semantics differ. General behavior may carry forward unless an applicable rule changes it; whether and how this happens is specific to each system.

4. **Shared properties and facts.** Concepts need a shared vocabulary of properties and relationships so that information supplied or derived in one part can be used elsewhere. This is closely connected to composition but is fundamental enough to identify separately. In Lifecycle, field kind and other properties can influence contributions to storage, facade methods, and transaction operations.

5. **Derivation.** Rules can produce additional facts from known facts, making the consequences of a combination available to other rules. Whether derivation is a distinct primitive or a form of composition remains open.

6. **Coordination and ordering.** Contributions must be assembled into a coherent result. Interactions may require shared ordering, conflict resolution, or a common operation pipeline. Lifecycle's historical field matrix identified cross-field and hook interactions that could not be settled by examining field kinds alone.

7. **Stages in time.** The model can describe multiple stages: YIDL definitions contribute to generation of a decorator; that decorator generates a class; instances then operate at runtime. Facts and rules need their stage and dependencies preserved to avoid confusing the generator with its output. Staging is an observation about systems such as YIDL, not necessarily a universal requirement.

8. **Constraints and validation.** A model can state which combinations are valid and identify ambiguous or incompatible selections. Validation and tests also help check whether the assembled result behaves as intended.

## Hypothesis and open questions

One hypothesis is that these mechanisms let an LLM work with an explicitly represented, interconnected problem while expressing individual contributions locally. YIDL's matching and assembly turn those contributions into an inspectable, testable result. This is a hypothesis about a useful process, not a claim that an LLM internally stores an explicit concept graph or that YIDL alone caused the outcome.

An exploratory black-box model maps YIDL constructs and their relationships into a concept space, preserving their information and stage; the discussion provisionally assumes a one-to-one mapping. That is a thought experiment, not an established property of an LLM or an implemented transformation.

Open questions include which mechanisms are essential, how shared properties relate to composition, how to describe precedence and cross-concept interactions, and whether the approach succeeds on other interrelated problems. C++ and GARNs suggest independently recognizable patterns, but their existence does not by itself establish that the LLM-assisted technique generalizes.

## Historical references

- `dev-docs/history/FieldSpecYIDLDesignMatrix.md` records the historical interaction or “third dimension” problem.
- `dev-docs/history/YidlTransducerCompositionModelReq.md` discusses why local AST substitution can require changes to surrounding control flow.
- `dev-docs/history/YidlArchitecturePosition.md` describes the fact-oriented generation architecture and Lifecycle as its forcing use case.
- `dev-docs/history/YidlBetterMergeProposals.md` records the later pressure to let features contribute to shared production phases.
