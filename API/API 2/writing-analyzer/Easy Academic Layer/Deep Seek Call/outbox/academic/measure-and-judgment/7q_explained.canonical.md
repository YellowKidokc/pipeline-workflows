# The 7Q Framework: A Formal Methodology for Cross-Domain Claim Analysis

## Abstract

This article presents the 7Q Framework, a systematic methodology for the structural analysis of truth claims across disciplinary boundaries, with particular application to theophysics—the interdisciplinary study of structural isomorphisms between physical and theological propositions. The framework is demonstrated through a worked example drawn from general relativity: the proposition that mass-energy curves spacetime and that free-falling objects follow geodesics through that curvature. Each of seven sequential analytical lenses—Identity, Domain, Assertion, Evidence, Dependencies, Consequences, and Falsification—is applied to this single claim, revealing hidden assumptions, cross-domain dependencies, and unresolved kill conditions that have driven theoretical physics for over a century. The framework is preceded by a precondition (Q0) establishing epistemic posture. Results indicate that the framework successfully decomposes complex claims into independently testable components, exposes structural isomorphisms across domains, and identifies the smooth manifold assumption as the primary unresolved dependency preventing unification with quantum mechanics.

---

## Q0: The Precondition—Epistemic Posture

### Function

Before any analytical framework can be applied, the inquirer must establish a posture of epistemic humility. Q0 is not a question but a precondition: the recognition that the ground of inquiry cannot be identical with the inquirer's prior commitments.

### Formal Statement

Let \( \mathcal{I} \) denote the inquirer and \( \mathcal{G} \) denote the ground of inquiry. The precondition asserts:

\[
\mathcal{I} \not\equiv \mathcal{G}
\]

That is, the inquirer cannot serve as the foundation for the inquiry itself. Historical failures of this precondition include logical positivism, which presupposed empirical verifiability as the criterion of meaning prior to any investigation of meaning, and behaviorism, which presupposed the irrelevance of mental states prior to any investigation of cognition. In both cases, the soil was poisoned before the seed was planted.

### Physics Example: Einstein (1905)

Einstein's development of special relativity did not commence with the assertion "Newton is wrong." Rather, it began with a genuine epistemic puzzlement: *What are the consequences if the speed of light is invariant across all inertial reference frames?* The theory that ultimately displaced Newtonian absolute space emerged from holding this question open, not from a predetermined conclusion.

---

## Q1: Identity—Definition and Classification

### Function

Q1 establishes the identity of the claim under examination. Every claim must be named, classified by type, and situated within a hierarchy of theoretical tiers. Failure to establish identity produces category confusion that propagates through all subsequent analysis.

### Formal Definition

Let \( C \) denote a claim. Q1 assigns:

\[
C \mapsto \{\text{Type}, \text{Tier}, \text{Prior Names}\}
\]

### Sub-Questions

1. What type of claim is this? (descriptive, causal, ontological, mathematical, mechanistic, predictive, normative)
2. What tier does it occupy? (foundational axiom, derived theorem, testable hypothesis, boundary condition)
3. Has this claim been named before, and does that name carry unverified assumptions?

### Classification—Worked Example

| Parameter | Value |
|-----------|-------|
| **Label** | Mass-energy curves spacetime |
| **Type** | Causal—mass-energy *causes* curvature |
| **Tier** | Foundational—the Einstein Field Equations are not derived from deeper principles within general relativity |
| **Prior Names** | General Relativity, Einstein Field Equations—carries the implicit domain constraint that "relativity" refers exclusively to physics |

### Analytical Yield

The classification as *causal* rather than *descriptive* is epistemically significant. Einstein's proposition asserts that mass-energy *causes* spacetime curvature, not merely that curvature and mass-energy are correlated. This is a stronger claim than is commonly recognized: matter tells spacetime how to bend, and spacetime tells matter how to move.

---

## Q2: Domain—Situating the Claim

### Function

Q2 anchors the claim within its domain of operation, identifies cross-domain presence, and distinguishes between surface analogy and structural isomorphism.

### Formal Definition

Let \( \mathcal{D} \) denote the set of all domains. Q2 assigns:

\[
C \mapsto \{\text{Primary Domain}, \text{Secondary Domains}, \text{Scale}, \text{Isomorphism Status}\}
\]

### Sub-Questions

1. Which domain owns this claim? (physics, mathematics, theology, consciousness, information, moral)
2. Does it appear in more than one domain? If so, is the relationship surface analogy or structural isomorphism?
3. At what scale does it operate? (quantum, molecular, neural, individual, social, cosmic, universal)

### Classification—Worked Example

| Parameter | Value |
|-----------|-------|
| **Primary Domain** | Physics |
| **Secondary Domains** | Mathematics (differential geometry, Riemannian manifolds) |
| **Scale** | Cosmic → Universal—applies from planetary orbits to cosmological expansion |
| **Isomorphism Status** | ISO-confirmed—the mathematical structure (Riemannian geometry) is independently valid across domains |

### Analytical Yield

The claim resides in physics but exhibits a structural dependency on mathematics. Riemannian geometry existed as a formal mathematical structure prior to its physical application by Einstein. The mathematics does not require the physics, but the physics cannot be formulated without the mathematics. This constitutes a genuine cross-domain dependency. Notably, Riemannian geometry also appears in machine learning (manifold learning), economics (curved utility surfaces), and information geometry (statistical manifolds), suggesting that the mathematical soil is more universal than the physical seed initially recognized.

---

## Q3: Assertion—Precision and Negation

### Function

Q3 forces the claim into precise, unambiguous formulation. A claim that cannot be restated accurately by an opponent is insufficiently precise. The claim must generate its own negation, which becomes the seed for subsequent falsification analysis.

### Formal Definition

Let \( C \) be a claim. Q3 produces:

\[
C \mapsto \{\text{Assertion}, \text{Negation}\}
\]

where the negation \( \neg C \) is the logical complement of \( C \).

### Sub-Questions

1. State the claim in one sentence with zero hedging.
2. Can a serious opponent restate it accurately?
3. Generate the negation—this becomes the seed for Q7's kill conditions.

### Classification—Worked Example

| Parameter | Value |
|-----------|-------|
| **Assertion** | "The distribution of mass-energy determines the curvature of spacetime, and free-falling objects follow geodesics through that curvature." |
| **Precision** | Mathematical—fully expressible in tensor calculus |
| **Certainty** | Proven—confirmed to extraordinary precision across multiple independent methods |
| **Scope** | Universal—applies everywhere gravity operates |
| **Negation** | "Mass-energy does NOT determine spacetime curvature, OR objects do NOT follow geodesics." |

### Analytical Yield

The negation reveals that the original claim bundles two distinct propositions: (1) mass-energy causes curvature, and (2) objects follow geodesics. Either could fail independently. Newtonian gravity posits mass causing attraction without curvature. Modified gravity theories (e.g., MOND, \( f(R) \) gravity) may retain curvature while adding extra forces such that objects do not follow pure geodesics. Q3's decomposition splits the claim into two independently killable components.

### Mathematical Formulation

The Einstein Field Equations:

\[
G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}
\]

where:
- \( G_{\mu\nu} \) = Einstein tensor (spacetime curvature)
- \( \Lambda \) = cosmological constant
- \( g_{\mu\nu} \) = metric tensor
- \( G \) = Newton's gravitational constant (\( 6.674 \times 10^{-11} \, \text{m}^3 \text{kg}^{-1} \text{s}^{-2} \))
- \( c \) = speed of light in vacuum (\( 2.998 \times 10^8 \, \text{m/s} \))
- \( T_{\mu\nu} \) = stress-energy tensor (mass-energy distribution)

The geodesic equation:

\[
\frac{d^2 x^\mu}{d\tau^2} + \Gamma^\mu_{\nu\rho} \frac{dx^\nu}{d\tau} \frac{dx^\rho}{d\tau} = 0
\]

where \( \tau \) is proper time and \( \Gamma^\mu_{\nu\rho} \) are the Christoffel symbols (connection coefficients).

---

## Q4: Evidence—External Justification

### Function

Q4 attaches external justification to the claim. Evidence must be classified by type, assessed for replication status, and evaluated for its ability to discriminate between competing models.

### Formal Definition

Let \( E \) denote the evidence set. Q4 assigns:

\[
E \mapsto \{\text{Type}, \text{Tier}, \text{Replication Status}, \text{Discriminatory Power}\}
\]

### Sub-Questions

1. Is this evidence empirical, experimental, mathematical, logical, or inferential?
2. Has it been replicated? By whom? Under what conditions?
3. Could the same evidence equally support a competing model?

### Classification—Worked Example

| Parameter | Value |
|-----------|-------|
| **Type** | Experimental, mathematical, observational |
| **Tier** | Tier 1—direct experimental, massively replicated |
| **Replication** | Replicated across 100+ years, multiple independent teams, multiple methods |
| **Competing Models** | No—specific predictions (e.g., exact Mercury precession value) are unique to GR |

### The Evidence—Four Independent Confirmations

**1. Mercury's Perihelion Precession (1915)**
Newtonian prediction: 5,557 arcseconds per century
Observed value: 5,600 arcseconds per century
GR residual: 43 arcseconds per century (exactly accounted for by GR)
No competing theory predicted this value prior to GR.

**2. Gravitational Lensing (1919)**
Eddington's solar eclipse expedition measured starlight deflection at \( 1.75 \pm 0.30 \) arcseconds at the solar limb, consistent with GR's prediction of twice the Newtonian value. Subsequent measurements have confirmed this to within 0.1%.

**3. Gravitational Waves (2015)**
LIGO detected GW150914, a gravitational wave signal from a binary black hole merger. The waveform matched GR predictions to within 1% across the inspiral, merger, and ringdown phases (Abbott et al., 2016, *Physical Review Letters*, 116, 061102).

**4. GPS Time Dilation (operational daily)**
GPS satellites at approximately 20,200 km altitude experience both special relativistic time dilation (due to orbital velocity) and general relativistic gravitational time dilation (due to reduced gravitational potential). The net correction is approximately 38 microseconds per day. Without this correction, GPS positional accuracy degrades by approximately 10 km per day.

---

## Q5: Dependencies—Hidden Foundations

### Function

Q5 exposes the dependency chain upon which the claim rests. Every claim depends on prior propositions, some of which may be axioms, brute facts, or circularities. The dependency chain must be traced to its terminus.

### Formal Definition

Let \( D(C) \) denote the set of propositions upon which \( C \) depends. Q5 produces:

\[
D(C) \mapsto \{\text{Explicit Dependencies}, \text{Chain Terminus}, \text{Fragility Profile}, \text{Hidden Dependencies}\}
\]

### Sub-Questions

1. What must already be true for this claim to stand?
2. Trace the dependency chain to its terminus: axiom, brute fact, or circularity?
3. If a dependency fails, does the entire claim collapse or only a branch?

### Classification—Worked Example

| Parameter | Value |
|-----------|-------|
| **Explicit Dependencies** | Equivalence Principle, Riemannian geometry, constancy of \( c \), conservation of energy-momentum, smooth spacetime manifold |
| **Chain Terminus** | Axiom—the Equivalence Principle is foundational, not derived from deeper physics |
| **Fragility Profile** | Degrade gracefully—if smooth manifold assumption fails at Planck scale, GR still applies everywhere else |
| **Hidden Dependency** | Smooth spacetime—GR assumes spacetime is a continuous differentiable manifold. Quantum gravity theories challenge this at \( 10^{-35} \) m |

### Analytical Yield—The Hidden Root

General relativity depends on spacetime being a smooth, continuous manifold. This is an assumption, not a proven fact. At the Planck scale (\( \ell_P = \sqrt{\hbar G / c^3} \approx 1.616 \times 10^{-35} \) m), spacetime may be discrete, foamy, or governed by non-commutative geometry. This hidden dependency is the fundamental obstacle to unification with quantum mechanics: the two theories disagree about the nature of the ground upon which they stand. Q5 identifies the crack that has driven theoretical physics for a century.

---

## Q6: Consequences—Generative Force

### Function

Q6 examines what the claim forces to be true downstream. A claim that generates no testable consequences is explanatorily inert. Consequences may include predictions within the original domain or forced implications in other domains (isomorphisms).

### Formal Definition

Let \( \mathcal{F}(C) \) denote the set of forced consequences. Q6 produces:

\[
\mathcal{F}(C) \mapsto \{\text{Direct Implications}, \text{Testable Predictions}, \text{Cross-Domain Consequences}\}
\]

### Sub-Questions

1. If true, what else MUST follow that has not yet been checked?
2. Does it generate testable predictions?
3. Does it force consequences in a different domain?

### Classification—Worked Example

| Parameter | Value |
|-----------|-------|
| **Direct Implications** | Black holes must exist (BH), gravitational waves must propagate (GW), time runs slower near mass (TD), light bends around massive objects (LB) |
| **Testable Predictions** | Exact Mercury precession value, exact LIGO waveform shape, exact GPS correction factor |
| **Cross-Domain Consequences** | Cosmology (expansion), astrophysics (neutron stars), technology (GPS), information theory (holographic principle) |

### Analytical Yield—Unforeseen Fruit

Einstein published the field equations in 1915. Schwarzschild derived the first exact solution—predicting black holes—within months. Gravitational waves fell out of the mathematics in 1916 and were detected 99 years later. GPS time dilation was forced by the equations long before satellite technology existed. The claim generated consequences its own author had not anticipated. This is the generative function of Q6: the tree bore fruit Einstein did not plant.

---

## Q7: Falsification—Death Conditions

### Function

Q7 attaches explicit death conditions to the claim. Every scientific claim must carry its own falsification criteria. Five death types are recognized: self-refutation, infinite regress, empirical contradiction, logical incoherence, and explanatory failure.

### Formal Definition

Let \( K(C) \) denote the set of kill conditions. Q7 produces:

\[
K(C) \mapsto \{\text{Death Type}, \text{Downstream Breaks}, \text{Adversarial Status}\}
\]

### Sub-Questions

1. Name the death condition—which of the five types?
2. What breaks downstream if this fails? (link to Q6 consequences)
3. Has anyone actually attempted to kill it, or has it only survived friendly examination?

### Classification—Worked Example

| Parameter | Value |
|-----------|-------|
| **Death #1** | Empirical—if light does not bend around massive objects (tested: Eddington 1919, confirmed thousands of times since) |
| **Death #2** | Empirical—if gravitational waves are not detected (tested: LIGO 2015) |
| **Death #3** | Empirical—if GPS does not require relativistic correction (tested: operational daily) |
| **Death #4** | Explanatory—if GR cannot handle singularities or quantum scales (LIVE—GR breaks at black hole centers and the Big Bang) |
| **Status** | Alive—survived 100+ years of adversarial testing. Q5's hidden root (smooth manifold assumption) is the open wound |
| **Adversarial Status** | Survived expert attack—every major physicist for a century has attempted to break it. No one has succeeded |

### Analytical Yield—The Living Kill Condition

Three of the four death conditions have been tested, and GR has survived each. However, Death #4 remains live. GR produces mathematical singularities (infinities) at black hole centers and cannot describe the first instant of the Big Bang. This is not a hypothetical objection but a mathematical fact internal to the theory. The smooth manifold assumption identified by Q5 is the axe wound. The theory is standing, but the crack has been present since 1915. The unification of gravity with quantum mechanics will either kill GR or heal this wound.

---

## Summary: The Complete Analytical Object

One claim, seven lenses, nothing hidden. The application of the 7Q Framework to the proposition "mass-energy curves spacetime" yields the following analytical results:

| Question | Finding |
|----------|---------|
| **Q1 Identity** | The claim is causal, not descriptive—a stronger claim than commonly recognized |
| **Q2 Domain** | The claim structurally depends on mathematics that exists independently in other domains |
| **Q3 Assertion** | The negation splits into two independently killable components |
| **Q4 Evidence** | Four independent confirmations, tier-1 replication, no competing model matches all four |
| **Q5 Dependencies** | A hidden root—the smooth manifold assumption—has driven unsolved physics for 100 years |
| **Q6 Consequences** | Forced predictions its own author did not foresee: black holes, gravitational waves, GPS corrections |
| **Q7 Kill Conditions** | Three death conditions survived, one still live—the singularity problem is the open wound |

---

## Conclusion

The 7Q Framework provides a systematic methodology for the analysis of truth claims across disciplinary boundaries. Applied forward, it classifies any claim. Applied in reverse, it proves any claim. The precondition Q0 ensures that the inquirer arrives with epistemic humility or not at all.

The framework is designed to be domain-independent: any AI, any student, any scientist can apply these seven questions without the presence of the framework's author. If it works without us in the room, it is real.

---

## References

Abbott, B. P., et al. (2016). Observation of gravitational waves from a binary black hole merger. *Physical Review Letters*, 116(6), 061102.

Eddington, A. S. (1919). The deflection of light during the solar eclipse. *Nature*, 104, 372–373.

Einstein, A. (1915). Die Feldgleichungen der Gravitation. *Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften*, 844–847.

Einstein, A. (1916). Die Grundlage der allgemeinen Relativitätstheorie. *Annalen der Physik*, 49(7), 769–822.

Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). *Gravitation*. W. H. Freeman.

Schwarzschild, K. (1916). Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie. *Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften*, 189–196.

Will, C. M. (2014). The confrontation between general relativity and experiment. *Living Reviews in Relativity*, 17(1), 4.