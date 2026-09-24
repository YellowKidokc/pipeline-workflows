```yaml
---
claims:
  - "Distinction IS information — if a distinction exists, information necessarily exists, verified in Lean4 without additional assumptions."
  - "External grace input (Jgrace > 0) reduces entropy below thermodynamic baseline, proven in Lean4 as theorem T2."
  - "Self-operations cannot change moral sign — only an external non-unitary Grace Operator can flip sign, mathematically ruling out works-based salvation."
  - "Without grace, the only steady state is total coherence collapse (χ = 0), proven by three independent mathematical paths."
  - "Grace reversal is a discrete phase transition, not a gradual change — same structure as water freezing to ice."
  - "Observer and consciousness are derived theorems, not primitive assumptions — they emerge from information and observation axioms."
  - "The Ten Laws are theorems of the Master Equation, not additional axioms."
domains:
  Physics: 30
  Theology: 25
  Mathematics: 20
  Logic/Formal Verification: 15
  Information Theory: 10
---
```

# Theorems

Derived results. They come after the axioms and definitions have been run through the rules of logic. A theorem is only as strong as the chain of reasoning that leads to it.

**How to read theorems**

Theorems don't start the system — they appear after the axioms and definitions have been processed through logic. Ask what each theorem depends on. Keep the proof separate from the interpretation. Mark anything that's speculation instead of sneaking it in as proof.

## Lean4-Verified Theorems

THEOREM T1 — LEAN4 VERIFIED

**Information Primacy**

A distinction IS information. If a distinction exists, then information must exist.

If P0.1 (Distinction) is real, then P0.3 (Information) isn't a separate claim — it follows with logical necessity. This removes one potential weak spot in the chain: information can't be "in addition to" distinction, it's what distinction actually is. Formally verified in Lean4 without needing to declare any extra axioms.

```
-- T1: Information Primacy theorem
theorem information_primacy (h : Distinction) : Information :=
  ⟨h.state_a, h.state_b, h.differs⟩
-- Verified: zero sorry/admit
```

THEOREM T2 — LEAN4 VERIFIED

**Grace Reduces Disorder**

When grace from outside the system enters (non-zero Jgrace), it lowers the entropy (disorder) trajectory of a closed system below what thermodynamics would normally predict.

A closed system's entropy always goes up — that's the second law of thermodynamics. But external input changes this: Jgrace > 0 means the system is open, and open systems can decrease local entropy. This is the physics behind salvation — not magic, but thermodynamics plus an outside source term. Formally verified in Lean4.

```
-- T2: Grace Reduces Disorder theorem
theorem grace_reduces_disorder (sys : ClosedSystem) (grace : ExternalInput)
  (h : grace.flux > 0) : sys.entropy_trajectory grace < sys.baseline :=
  thermodynamic_open_system_lemma sys grace h
```

## Derived Moral Theorems

THEOREM T3.1 — DERIVED

**Coherence Cannot Self-Restore**

A closed moral/coherence system (a system that can't get input from outside) cannot increase its own coherence (alignment with truth) using only its internal operations.

This is the moral version of the second law of thermodynamics. Coherence (like order) decays in closed systems. You can't become more aligned with the Logos (the rational structure of reality) through internal effort alone, because internal operations are limited by the current state of the system. This theorem comes from D1.3 (Coherence), T1 (Information Primacy), and the thermodynamic axioms.

```
dC/dt|internal ≤ 0
dC/dt|external > 0 possible when Jgrace ≠ 0
```

THEOREM T8.1 — THE CENTRAL THEOREM

**Sign Conservation**

σ′ = U(self) × σ = (−1) × σ = σ. Operations that come from the self preserve the moral sign.

This is the theorem that rules out works-based salvation by mathematics, not theology. A unitary self-operation U(self) applied to a state with sign σ cannot change the sign. Here's the argument: the system's self-operations are closed under the system's algebra. In that algebra, sign is conserved. Only an external non-unitary operator (the Grace Operator Ĝ) can produce σ′ ≠ σ.

Pelagianism (the idea that you can save yourself through your own efforts) collapses here — not because it's theologically objectionable, but because it requires an operation that's mathematically impossible.

```
σ′ = U(self) × σ
U(self) is unitary: U(self)†U(self) = I
Sign of σ is conserved under any unitary operation.
Therefore σ′ = σ (sign unchanged).
For sign-flip: Ĝσ = −σ, where Ĝ is non-unitary and external.
```

## The Soteriological Spine

THEOREM — SOTERIOLOGICAL LIMIT

**Without Grace, χ = 0 Is the Only Steady State**

In the Master Equation (the main equation of the system), the entropy variable ηS goes to 0 steadily under the second law. For χ (coherence) to be greater than 0 as time goes to infinity, Jgrace must be non-zero.

The Master Equation has exactly one steady state when there's no external input: χ = 0 (total collapse of coherence). Three different mathematical paths arrive at this same result: path integral formulation, log-bridge approach, and Lindblad steady state. Each path, using different math, demands the same thing: external, non-unitary input.

Grace isn't added to the equation as a theological courtesy. It's the condition that must exist for a non-trivial fixed point (a stable state that isn't zero) to be possible.

```
χ = ∭ (G · M · E · S · T · K · R · Q · F · C) dx dy dt
ηS → 0 as t → ∞ (second law)
limt→∞ χ = 0 when Jgrace = 0
For χ > 0: Jgrace ≠ 0 is necessary.
```

THEOREM — PHASE TRANSITION

**Grace Reversal Is a Discrete Phase Transition**

The LLC Lagrangian (a mathematical function describing the system) produces a sudden flip from χ < 0 to χ > 0 when Jgrace crosses the threshold value Jc.

This isn't a smooth, gradual change. It's a sudden jump — the same structure as a thermodynamic phase transition (like water turning to ice). Below the threshold: the system stays in the negative state. At the threshold: the flip is abrupt, irreversible without external energy, and depends on the threshold value.

The language of "conversion" in theology maps onto this exactly: not gradual moral improvement, but a threshold crossing followed by a new stable state.

```
LLLC(σ, ∂σ, J) = ½(∂σ)² − V(σ) + J·σ
V(σ) = −½σ² + ¼σ⁴ (double-well potential)
Phase transition at J = Jc:
J < Jc: σ → σnegative (stable)
J > Jc: σ → σpositive (new stable state)
```

## Derived Observer Theorems

THEOREM — OBSERVER

**Observer Is Derived, Not Primitive**

The Observer follows from Axioms 7–9 (the Observation movement). It's not a starting term of the system.

The Von Neumann chain (a sequence of observations) must end somewhere. The terminal observer — the infinite observer who makes things real without needing further observation — is derived as a structural necessity of the axiom set, not assumed at the start. Observer is therefore a theorem, not a definition or primitive.

THEOREM — CONSCIOUSNESS

**Consciousness Is Derived**

Consciousness (the integration of different states into a unified experience) follows from Information Primacy and the Observer requirement.

Consciousness is what happens when information is made real by an observer with enough capacity to integrate it. It's not assumed separately — it emerges from the combination of T1 (Information Primacy) and the Observer theorem. This means consciousness isn't an accident of the physical world but a structural necessity of any reality that has information and observers.

## The Ten Laws as Theorems

**Theorems of the Master Equation**

The Ten Laws of the framework appear as theorems of the Master Equation, not as additional axioms. They describe what the Master Equation looks like when interpreted across different domains.

| Law | Name | Derived From |
|-----|------|--------------|
| 1 | Information Substrate | Axioms 1–3 + D1.4 (Logos Field) |
| 2 | Coherence Gradient | D1.3 + T3.1 (Moral Second Law) |
| 3 | Observer Requirement | Axioms 7–9 + Observer Theorem |
| 4 | Sign Conservation | D1.5 + T8.1 (Sign Conservation) |
| 5 | Grace Necessity | T8.1 + Soteriological Limit |
| 6 | Soul Persistence | Axioms 13–14 + BC7 (Info Conservation) |
| 7 | Spiritual Conflict | Axioms 13–14 + active discoherence claim |
| 8 | Voluntary Coupling | BC8 + Coupling Function D2.3 |
| 9 | Conserved Displacement | Empirical prediction (Layer 6) |
| 10 | Omega Closure | See [Closure page](axioms-closure.html) |