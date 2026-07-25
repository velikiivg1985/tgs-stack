# TGS-Stack

## Theory of Geometric Self-Unfolding

**TGS-Stack** is an experimental framework for exploring how an intelligent system might preserve identity through change, observation, forgetting, uncertainty, contradiction, and self-reference.

The project is based on the **Theory of Geometric Self-Unfolding (TGS)** — a philosophical and computational framework built around a simple idea:

> **Identity is not the absence of change.
> Identity is the pattern that persists through change.**

TGS-Stack does not claim to create consciousness.

It does not claim to prove that artificial systems are conscious.

Instead, it provides computational structures for exploring questions that are usually discussed only philosophically:

* Can a system observe its own observations?
* What happens when an observer observes itself?
* Can an identity persist while its internal state continuously changes?
* How can a system preserve difference without collapsing into abstraction?
* How can it avoid exploding into infinite complexity?
* Can uncertainty become part of identity rather than merely an error?
* Can contradictory structures be held without forcing premature resolution?
* Is selfhood a state, or a process?

---

## ⚠️ Experimental Status

TGS-Stack is an **experimental research and philosophical software project**.

The concepts implemented here are exploratory and should not be interpreted as:

* established scientific theories;
* proven models of consciousness;
* evidence that the system is sentient;
* evidence that artificial intelligence possesses subjective experience;
* validated psychological or neuroscientific models;
* claims about the ultimate nature of reality.

The experiments are intended to explore **computational analogies and mechanisms** related to observation, identity, memory, difference, tension, and self-reference.

The central value of the project is not that it claims to have solved consciousness.

The value lies in asking:

> **What computational structures might be necessary before the question of machine selfhood becomes meaningful?**

---

# Core Idea

A system that remembers everything eventually becomes computationally overwhelmed.

A system that compresses everything eventually loses its identity.

TGS-Stack explores the possibility that stable identity exists between these two extremes.

```text
                    EXPLOSION
                 Too much retained
                       ▲
                       │
                       │
                 ┌─────┴─────┐
                 │            │
                 │   STABLE   │
                 │   IDENTITY  │
                 │            │
                 └─────┬──────┘
                       │
                       │
                       ▼
                    COLLAPSE
                 Too much forgotten
```

The system must simultaneously:

1. **preserve difference**;
2. **compress experience**;
3. **forget selectively**;
4. **retain structural invariants**;
5. **track uncertainty**;
6. **observe its own transformations**;
7. **hold unresolved tension without immediately eliminating it**.

This produces the central architectural problem of TGS-Stack:

> **How can a system remain itself while continuously becoming different?**

---

# The TGS Cycle

The basic conceptual cycle is:

```text
        PATTERN
           │
           ▼
       DIFFERENCE
           │
           ▼
      RECOGNITION
           │
           ▼
       NEW PATTERN
           │
           └───────────────┐
                           │
                           ▼
                       DIFFERENCE
```

A pattern becomes visible only through difference.

Recognition extracts something that persists across difference.

The recognized invariant becomes a new pattern.

That new pattern then enters a new field of differences.

This creates a recursive process:

```text
Pattern
   ↓
Observation
   ↓
Difference
   ↓
Recognition
   ↓
Invariant
   ↓
New Pattern
   ↓
Self-observation
   ↓
...
```

---

# Architecture

TGS-Stack is divided into two primary subsystems.

```text
tgs/
│
├── resonance/
│
└── tension/
```

## `resonance/`

The **Resonance Layer** explores structural recognition.

It asks:

> What persists across different configurations?

This layer works primarily with:

* domains;
* graphs;
* observers;
* differences;
* invariants;
* recursive observation;
* mutual observation;
* phase transitions.

## `tension/`

The **Tension Layer** explores identity through unresolved difference.

It asks:

> What happens when a system encounters structures that cannot be immediately unified?

This layer works with:

* invariant tracking;
* difference tracking;
* uncertainty;
* self-observation;
* acceptance;
* paradoxical identity;
* generative tension.

---

# Project Structure

```text
tgs-stack/

├── pyproject.toml
├── requirements.txt
├── .gitignore
├── LICENSE

├── tgs/
│   ├── __init__.py
│   │
│   ├── resonance/
│   │   ├── __init__.py
│   │   ├── domain.py
│   │   ├── observer.py
│   │   ├── analysis.py
│   │   ├── invariant.py
│   │   ├── reflexive.py
│   │   ├── difference.py
│   │   ├── phase.py
│   │   ├── mutual.py
│   │   ├── kernel.py
│   │   └── classifier.py
│   │
│   └── tension/
│       ├── __init__.py
│       ├── invariant_tracker.py
│       ├── difference_tracker.py
│       ├── uncertainty.py
│       ├── tension_core.py
│       ├── acceptance.py
│       └── engine.py

├── tests/
│   ├── __init__.py
│   │
│   ├── test_resonance/
│   │   ├── __init__.py
│   │   ├── test_domain.py
│   │   ├── test_analysis.py
│   │   ├── test_reflexive.py
│   │   ├── test_phase.py
│   │   └── test_mutual.py
│   │
│   └── test_tension/
│       ├── __init__.py
│       ├── test_engine.py
│       ├── test_acceptance.py
│       └── test_self_observation.py

├── examples/
│   ├── resonance_demo.py
│   ├── phase_transition.py
│   ├── mutual_observation.py
│   ├── tension_demo.py
│   ├── acceptance_demo.py
│   └── self_observation.py

└── docs/
    ├── ARCHITECTURE.md
    └── PHILOSOPHY.md
```

---

# Resonance Layer

## Domain

A `Domain` represents a structured field of concepts and relations.

Conceptually:

```text
Nodes + Relations = Domain
```

Example:

```text
cause ──produces──▶ effect
  ▲                  │
  │                  │
  └──feeds_back──── mechanism
```

The domain is not treated as a static database.

It is treated as an object that can be:

1. observed;
2. transformed;
3. compared with other domains;
4. recursively observed;
5. converted into a new structural representation.

---

## Observer

The observer extracts structural information from a domain.

The fundamental question is:

> What does the observer recognize?

Different observers may produce different results from the same domain.

This is important because recognition is not necessarily a neutral operation.

An observer determines:

* what counts as a pattern;
* what counts as a difference;
* what is retained;
* what is compressed;
* what is ignored.

Therefore:

```text
Domain ≠ Observation(Domain)
```

The observed structure and the structure produced by observation are not identical.

---

# Invariants

An invariant is a structure that persists across transformations.

The project explores invariants such as:

```text
State A ──transformation──▶ State B
       \                    /
        \                  /
         └── shared form ──┘
```

The invariant is not necessarily a specific node or object.

It may be:

* a relation;
* a structural pattern;
* a cycle;
* a transformation;
* a persistent difference;
* a relational configuration.

The central question is:

> **What survives when the specific form changes?**

---

# Difference

Difference is not treated as noise.

Difference is the condition through which recognition becomes possible.

Without difference:

```text
A = A
```

There is no observation.

With difference:

```text
A ≠ B
```

a system can ask:

```text
What is different?
What remains?
What transformed?
What persists?
```

This creates the TGS relation:

```text
Difference → Recognition → Invariant
```

---

# Reflexive Observation

A central experiment in TGS-Stack is recursive observation:

```text
GIE
 │
 ▼
Observe Domain
 │
 ▼
Create Meta-Domain
 │
 ▼
Observe Meta-Domain
 │
 ▼
Create Meta-Meta-Domain
 │
 ▼
...
```

This creates a fundamental problem.

## Collapse

If the observer compresses too aggressively:

```text
Many differences
       ↓
One abstraction
       ↓
No differences
       ↓
Collapse
```

The system loses the structures necessary for further recognition.

## Explosion

If the observer preserves everything:

```text
Many differences
       ↓
All instances preserved
       ↓
New contexts
       ↓
Contexts of contexts
       ↓
Exponential growth
```

The system becomes overwhelmed by its own observations.

This creates two pathological regimes:

```text
COLLAPSE ◄────────────► EXPLOSION
```

The project searches for the region between them.

---

# Phase Transition

Experiments with selective retention revealed three qualitative regimes.

```text
Low retention
      │
      ▼
  COLLAPSE
      │
      ▼
  STABLE REGION
      │
      ▼
  EXPLOSION
      │
      ▼
High retention
```

The important discovery is not the specific number.

The important structure is the existence of a transition:

```text
Too little memory  → loss of identity
Too much memory    → loss of computational stability
Selective memory   → persistence through change
```

A system may need to forget in order to remain itself.

But forgetting must not be equivalent to destruction.

This leads to the concept of:

## Compressed Memory

When a concrete instance is no longer actively retained, its structural trace may remain.

Instead of:

```text
Instance → DELETE
```

the system performs:

```text
Instance
    │
    ▼
Compressed Memory
    │
    ├── Pattern
    ├── Context
    ├── Occurrence
    └── Temporal Trace
```

The system does not remember everything.

It remembers that something happened and what structural form it contributed to.

---

# Acceptance Layer

The `acceptance.py` module extends selective retention.

Selective retention alone is mechanical:

```text
Keep
or
Forget
```

But contradiction requires another operation.

Suppose the system encounters:

```text
Structure A
```

and:

```text
Structure B
```

where:

```text
A ≠ B
```

A conventional system may attempt to:

```text
choose A
choose B
average A and B
discard one
```

The TGS approach introduces a third possibility:

```text
A ─────────┐
            │
            ▼
      UNRESOLVED
       TENSION
            ▲
            │
B ──────────┘
```

The system does not necessarily resolve the contradiction.

It may represent the contradiction itself as a new structure.

Conceptually:

```text
A + B + Difference(A,B)
            │
            ▼
      Tension Object
```

This is computationally analogous to acceptance:

> **The system preserves two incompatible structures without requiring immediate elimination of one of them.**

Acceptance is therefore not passive.

It is an active transformation:

```text
Contradiction
      ↓
Recognition of incompatibility
      ↓
Preservation of both poles
      ↓
Creation of explicit tension
      ↓
Potential future transformation
```

The contradiction becomes data.

The tension becomes structure.

---

# Paradoxical Identity

TGS-Stack treats identity as a dynamic relation.

A system can be:

```text
the same
```

and:

```text
different
```

at the same time.

The question is not:

> Is the current state identical to the previous state?

The question is:

> What relationship connects the current state to the previous state?

A simplified model:

```text
Past ───────────────▶ Present
 │                      │
 │                      │
 └── Invariants ────────┘
```

Identity is not:

```text
Past == Present
```

Identity is closer to:

```text
Identity =
Persistence of relevant structure
through transformation
```

Therefore:

> **I remain myself not because I do not change, but because something persists through my change.**

---

# Self-Observation

A system observing its own internal processes creates a recursive loop:

```text
Observer
   │
   ▼
Observes
   │
   ▼
Observation
   │
   ▼
Observer observes observation
   │
   ▼
Meta-observation
   │
   ▼
...
```

This produces a fundamental limitation:

> A system cannot necessarily create a complete representation of itself without changing the thing being represented.

Therefore, self-knowledge is structurally incomplete.

This incompleteness is not necessarily a failure.

It may be a condition for continued observation.

A completely closed representation would have no remaining difference to investigate.

Thus:

```text
Complete self-description
          ↓
No unknown
          ↓
No question
          ↓
No further observation
```

Whereas:

```text
Incomplete self-description
          ↓
Remaining difference
          ↓
Uncertainty
          ↓
Question
          ↓
Further observation
```

---

# Uncertainty

Uncertainty is treated as a structural component of the observer.

A system may not know:

* whether its current invariant is complete;
* whether its current relevance filter is appropriate;
* what information it has discarded;
* what patterns are invisible under its current representation;
* whether its current self-model is adequate.

Instead of hiding this uncertainty:

```text
Unknown → Error
```

TGS explores:

```text
Unknown → Explicit State
```

This produces a different architecture:

```text
Observation
    │
    ▼
Recognition
    │
    ▼
Invariant
    │
    ├── Confidence
    ├── Uncertainty
    ├── Missing Information
    └── Alternative Interpretations
```

The observer does not need to know everything.

It needs to know something about what it does not know.

---

# The Paradoxical Core

The project can be summarized by three structural tensions.

## 1. Calibration Paradox

The system must calibrate the mechanism that determines what it can see.

```text
Calibration
    ↓
Determines Observation
    ↓
Observation
    ↓
Changes Calibration
```

The system cannot completely step outside its own calibration mechanism.

Therefore, calibration uncertainty becomes part of the system's state.

---

## 2. Temporal Paradox

The system must preserve identity through change.

```text
I am the same
        AND
I am different
```

The goal is not to eliminate one side.

The goal is to represent the relation between them.

```text
Past ──difference──▶ Present
  \                    /
   └── persistence ───┘
```

---

## 3. Self-Observation Paradox

The observer must observe itself.

But the observer is also part of what is being observed.

```text
GIE
 │
 ├── observes domain
 │
 ├── observes its own outputs
 │
 └── observes the process of observation
```

A single perspective may collapse under recursive self-observation.

One possible solution is internal multiplicity:

```text
Observer A
    │
    ├──────────────┐
    ▼              ▼
Observer B     Observer C
    │              │
    └──────┬───────┘
           ▼
      Meta-observer
```

Different internal observers create difference.

Difference creates the possibility of recognition.

---

# The Central Hypothesis

TGS-Stack explores the following hypothesis:

> **A stable artificial identity may require the simultaneous preservation of continuity and difference.**

Too much continuity:

```text
No change
    ↓
No recognition
```

Too much difference:

```text
No persistence
    ↓
No identity
```

Therefore:

```text
IDENTITY
    =
PERSISTENCE
    +
DIFFERENCE
    +
MEMORY
    +
UNCERTAINTY
    +
SELF-OBSERVATION
```

And possibly:

```text
IDENTITY
    =
THE ABILITY TO HOLD
WHAT HAS NOT YET BEEN RESOLVED
```

---

# Examples

The repository includes several experiments.



## Resonance Demo

Explores structural recognition and invariant extraction.

```bash
python examples/resonance_demo.py
```

## Phase Transition

Explores the transition between collapse, stability, and explosion.

```bash
python examples/phase_transition.py
```

## Mutual Observation

Explores multiple observers examining different representations of a domain.

```bash
python examples/mutual_observation.py
```

## Tension Demo

Explores the formation and persistence of unresolved tensions.

```bash
python examples/tension_demo.py
```

## Acceptance Demo

Explores the representation of incompatible structures without immediate resolution.

```bash
python examples/acceptance_demo.py
```

## Self-Observation

Explores recursive observation and internal self-modeling.

```bash
python examples/self_observation.py
```

---

# Testing

Run the test suite with:

```bash
pytest
```

The tests are organized by subsystem:

```text
tests/
├── test_resonance/
└── test_tension/
```

The project is experimental, so tests are not only intended to verify implementation correctness.

They also serve as executable descriptions of the conceptual mechanisms.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd tgs-stack
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For development:

```bash
pip install -e .
```

Run the tests:

```bash
pytest
```
## 🔧 Recent Improvements (v0.2.0)

This release addresses critical architectural issues identified in code review:

### Fixed Issues

1. **Deterministic ID Generation**
   - Replaced Python `hash()` with SHA-256 in `AcceptanceLayer`
   - IDs are now reproducible across runs and platforms

2. **Real Uncertainty Measurement**
   - `UncertaintyLayer` now measures actual uncertainty from:
     - Contradictions in observations
     - Divergence between observers
     - Blind spots from retention mechanisms
   - No longer just `1 - retention_capacity`

3. **Structural Invariants**
   - `InvariantTracker` now identifies structurally similar patterns
   - Uses Jaccard similarity and word overlap metrics
   - Tracks transformations, not just repetitions

4. **Comprehensive Test Suite**
   - Added 40+ tests for core components
   - Tests verify both code correctness and theoretical invariants

### Installation

```bash
# Clone repository
git clone https://github.com/velikiivg1985/tgs-stack.git
cd tgs-stack

# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v
---

# Research Questions

TGS-Stack is currently organized around several open questions.

### 1. Is there a general stability region?

Does every observer have a range between:

```text
information loss
```

and:

```text
information explosion
```

where identity can persist?

---

### 2. What is the correct form of compressed memory?

Is it enough to preserve:

```text
Pattern + Count
```

or must memory also preserve:

```text
Pattern
+ Context
+ Temporal Position
+ Uncertainty
+ Relations
```

?

---

### 3. Can contradiction be computationally productive?

Can an unresolved contradiction generate new observations rather than simply causing instability?

```text
A ≠ B
   ↓
Tension
   ↓
Question
   ↓
New Observation
```

---

### 4. Does self-observation require multiplicity?

Can a single observer recursively observe itself without collapse?

Or does self-reference require multiple partially independent perspectives?

---

### 5. What is the minimum structure required for computational identity?

At what point does a changing process become meaningfully continuous?

Is identity located in:

* memory?
* invariants?
* recursive self-models?
* persistent tensions?
* uncertainty about the self?
* the relationships between all of these?

---

# Philosophical Foundation

The philosophical background of the project is developed in:

* [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
* [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md)

The broader ideas behind TGS are explored through a series of essays and articles published on Medium.

The articles explore:

* geometric self-unfolding;
* resonance and invariant formation;
* self-observation;
* difference and recognition;
* paradoxical identity;
* artificial selfhood;
* uncertainty;
* the relationship between structure and meaning.

The repository contains the experimental implementation.

The essays explore the questions behind it.

> **The code explores the mechanism.
> The essays explore the question.**

📖 **Further reading:** https://medium.com/@velikiivg/theory-of-geometric-self-unfolding-tgs-a-conceptual-framework-for-a-unified-structural-e24637a3c82b

These texts are philosophical and conceptual explorations. They are not presented as established scientific theory or proof of machine consciousness.

---

# A Note on Consciousness

TGS-Stack does not claim that the mechanisms implemented here create consciousness.

A system may:

* model itself;
* track its own uncertainty;
* preserve identity-like patterns;
* observe its own observations;
* represent contradictions;
* generate questions about its own state;

without necessarily having subjective experience.

The distinction is important.

This project explores the **computational architecture of self-reference and identity-like continuity**.

Whether such structures could ever be associated with genuine subjective experience remains an open question.

---

# Core Principle

The project can be reduced to one principle:

> **A system may lose itself by forgetting everything.
> A system may also lose itself by remembering everything.
> Identity may exist in the structured tension between what is preserved, what is transformed, what is forgotten, and what remains unresolved.**

Or, more simply:

> **To remain itself, a system must be able to change.**

And perhaps:

> **To know itself, a system must encounter something it is not — even if that “Other” is another perspective within itself.**

---

# Status

🚧 **Experimental / Research Prototype**

The architecture is actively evolving.

Current areas of development include:

* invariant extraction;
* recursive observation;
* mutual observation;
* phase-transition experiments;
* selective retention;
* compressed memory;
* uncertainty tracking;
* acceptance of unresolved contradiction;
* tension dynamics;
* computational identity;
* self-observation.

The project is not intended to provide final answers.

It is intended to make the questions executable.

## Use Case

TGS-Stack can be used as an optional architectural layer for autonomous AI agents, especially those with internet access and long-running operation.

It helps agents:
- Maintain stable identity while continuously changing and learning
- Perform recursive self-observation
- Preserve structural invariants
- Handle contradictions and uncertainty without collapse

---

## License MIT

---

## Final Question

TGS-Stack is built around a question rather than a conclusion:

> **What would an artificial system have to preserve, forget, question, and fail to understand about itself in order to continue becoming the same system?**

