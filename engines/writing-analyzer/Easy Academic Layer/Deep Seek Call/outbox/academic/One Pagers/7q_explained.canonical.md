# The 7Q Framework: A Formal Methodology for Cross-Domain Claim Analysis

## Abstract

This article presents the 7Q Framework, a systematic methodology for the structural analysis, classification, and evaluation of knowledge claims across disciplinary boundaries. The framework is demonstrated through a worked example drawn from general relativity: the proposition that mass-energy curves spacetime and that free-falling objects follow geodesics through that curvature. Each of seven sequential interrogative stages—Identity, Domain, Assertion, Evidence, Dependencies, Consequences, and Falsification—is applied to this single claim, revealing its causal structure, cross-domain dependencies, hidden axiomatic assumptions, forced predictions, and surviving kill conditions. A preliminary precondition (Q0) establishes the epistemic posture required for genuine inquiry. The framework is designed to be domain-agnostic, reproducible, and amenable to both human and automated implementation.

---

## Q0: The Precondition of Inquiry

### Function

To establish the epistemic posture of the inquirer prior to claim analysis. Q0 is not a question but a precondition: the recognition that the inquirer cannot serve as the ground of inquiry.

### Rationale

The history of failed epistemological frameworks reveals a recurring pattern: the imposition of methodological constraints before the object of inquiry has been examined. Logical positivism, for instance, stipulated that meaning must be empirically verifiable before examining whether such a criterion could itself be verified. Behaviorism excluded introspective data before investigating whether consciousness could be studied without it. In both cases, the soil of inquiry was poisoned before the seed of investigation was planted.

### Physics Example: General Relativity

Albert Einstein did not commence his 1905 investigations with the conclusion that Newtonian gravity was incorrect. Rather, he began with a genuine puzzlement: what follows if the speed of light is invariant across all inertial reference frames? The theory that ultimately displaced Newtonian absolute space emerged from sustained engagement with an open question, not from a predetermined answer.

---

## Q1: Identity — The Seed

### Function

To define, name, and classify the claim under investigation, thereby preventing category confusion.

### Sub-Questions

1. What type of claim is this? (descriptive, causal, ontological, mathematical, mechanistic, predictive, normative)
2. What tier does it occupy? (foundational axiom, derived theorem, testable hypothesis, boundary condition)
3. Has this claim been named previously, and does that name carry unverified assumptions?

### Classification: Mass-Energy Curves Spacetime

| Parameter | Classification |
|-----------|----------------|
| Label | Mass-energy curves spacetime |
| Type | Causal — mass-energy *causes* curvature |
| Tier | Foundational — the Einstein field equations are not derived from deeper principles within general relativity |
| Prior Names | General Relativity, Einstein Field Equations — the term "relativity" carries a domain constraint (physics) that is itself worth noting |

### Analytical Yield

Forcing the claim type reveals that this is a causal proposition, not merely a descriptive one. Einstein asserts that mass-energy *causes* spacetime curvature, not that spacetime happens to be curved. This is a substantially stronger claim than a descriptive correlation: matter actively instructs spacetime how to bend. Classifying this as "descriptive" would obscure half the potential kill conditions.

---

## Q2: Domain — The Soil

### Function

To anchor the claim within its domain(s) of operation, identify scale, and detect cross-domain presence.

### Sub-Questions

1. Which domain owns this claim? (physics, mathematics, theology, consciousness, information, moral)
2. Does it appear in more than one domain? If so, is this a surface analogy or a structural isomorphism?
3. At what scale does it operate? (quantum, molecular, neural, individual, social, cosmic, universal)

### Classification

| Parameter | Classification |
|-----------|----------------|
| Primary Domain | Physics |
| Additional Domains | Mathematics (differential geometry, Riemannian manifolds) |
| Scale | Cosmic → Universal — applies from planetary orbits to cosmological expansion |
| Isomorphism Status | Confirmed — the mathematical structure (Riemannian geometry) is independently valid across domains |

### Analytical Yield

The claim resides in physics but structurally depends on mathematics. Riemannian geometry existed as a formal mathematical structure prior to Einstein's appropriation of it. The mathematics does not require the physics for its validity, but the physics cannot be formulated without the mathematics. This constitutes a genuine cross-domain dependency. Notably, Riemannian geometry also appears in machine learning (manifold learning), economics (curved utility surfaces), and information geometry (statistical manifolds). The soil is more universal than the seed initially recognized.

---

## Q3: Assertion — The Sprout

### Function

To force precision in the claim's formulation, committing it to a specific direction and generating its own negation.

### Sub-Questions

1. State the claim in one sentence with zero hedging.
2. Can a serious opponent restate the claim accurately? If not, it is not precise enough.
3. Generate the negation — this becomes the seed for Q7's kill conditions.

### Classification

| Parameter | Classification |
|-----------|----------------|
| Assertion | "The distribution of mass-energy determines the curvature of spacetime, and free-falling objects follow geodesics through that curvature." |
| Precision | Mathematical |
| Certainty | Proven — confirmed to extraordinary precision |
| Scope | Universal — applies wherever gravity operates |
| Negation | "Mass-energy does NOT determine spacetime curvature, OR objects do NOT follow geodesics." |

### Analytical Yield

The negation reveals that the claim actually contains two independently killable propositions: (1) mass-energy causes curvature, and (2) objects follow geodesics. Either could fail independently. Newtonian gravity posits mass causing attraction but no curvature whatsoever. Certain modified gravity theories retain curvature while introducing additional forces such that objects do not follow pure geodesics. Q3's negation splits the claim into two independently falsifiable components.

### Mathematical Formulation

The Einstein field equations are expressed as:

$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$

where:
- $G_{\mu\nu}$ is the Einstein tensor, encoding spacetime curvature
- $\Lambda$ is the cosmological constant (dimension: $\text{L}^{-2}$)
- $g_{\mu\nu}$ is the metric tensor (dimensionless)
- $G$ is Newton's gravitational constant (dimension: $\text{M}^{-1}\text{L}^3\text{T}^{-2}$)
- $c$ is the speed of light in vacuum (dimension: $\text{L}\text{T}^{-1}$)
- $T_{\mu\nu}$ is the stress-energy tensor (dimension: $\text{M}\text{L}^{-1}\text{T}^{-2}$)
- The factor $\frac{8\pi G}{c^4}$ ensures dimensional consistency (dimension: $\text{M}^{-1}\text{L}^{-1}\text{T}^2$)

---

## Q4: Evidence — The Rain

### Function

To attach external justification, demonstrating that the claim does not support itself.

### Sub-Questions

1. Is this evidence empirical, experimental, mathematical, logical, or inferential?
2. Has it been replicated? By whom? Under what conditions?
3. Could the same evidence equally support a competing model?

### Classification

| Parameter | Classification |
|-----------|----------------|
| Type | Experimental, mathematical, observational |
| Tier | Tier 1 — direct experimental, massively replicated |
| Replication | Replicated across 100+ years, multiple independent teams, multiple methods |
| Competing Models | No — the specific predictions (e.g., exact Mercury precession value) are unique to general relativity |

### The Evidence: Four Independent Confirmations

**1. Mercury's Perihelion Precession (1915)**
Newtonian mechanics predicted 5,557 arcseconds per century. The observed value was 5,600 arcseconds per century. The 43-arcsecond discrepancy was explained exactly by general relativity. No competing theory predicted this value.

**2. Gravitational Lensing (1919)**
Eddington's solar eclipse expedition demonstrated that starlight bends around the Sun by precisely the amount predicted by general relativity — twice the Newtonian value.

**3. Gravitational Waves (2015)**
The Laser Interferometer Gravitational-Wave Observatory (LIGO) detected spacetime ripples from merging black holes. The waveform matched general relativistic predictions to extraordinary precision (Abbott et al., 2016).

**4. GPS Time Dilation (Ongoing)**
Global Positioning System satellites must correct for relativistic time dilation every second. Removal of these corrections renders GPS inoperable within hours (Ashby, 2003).

---

## Q5: Dependencies — The Roots

### Function

To expose hidden foundations by tracing the dependency chain to its terminus.

### Sub-Questions

1. What must already be true for this claim to stand?
2. Trace the dependency chain all the way down — where does it end? (Axiom, brute fact, or circularity?)
3. If a root fails, does the whole tree fall immediately or only one branch?

### Classification

| Parameter | Classification |
|-----------|----------------|
| Depends On | Equivalence Principle, Riemannian geometry, constancy of $c$, conservation of energy-momentum, smooth spacetime manifold |
| Chain Terminus | Axiom — the equivalence principle is foundational, not derived from deeper physics |
| Fragility | Degrades gracefully — if the smooth manifold assumption fails at the Planck scale, general relativity still applies everywhere else |
| Hidden Dependency | Smooth spacetime — general relativity assumes spacetime is a continuous manifold. Quantum gravity theories challenge this at $10^{-35}$ meters |

### Analytical Yield

General relativity depends on spacetime being a smooth, continuous manifold. This is an assumption, not a proven fact. At the Planck scale ($\ell_P = \sqrt{\hbar G/c^3} \approx 1.616 \times 10^{-35}$ m), spacetime may be discrete, foamy, or governed by an entirely different ontology. This hidden root is the fundamental reason general relativity and quantum mechanics resist unification: they disagree about the nature of the ground on which they stand. Q5 identifies the crack that has driven theoretical physics for a century.

---

## Q6: Consequences — The Canopy

### Function

To determine what else must be true if the claim is true, generating predictions and identifying cross-domain implications.

### Sub-Questions

1. If true, what else MUST follow that nobody has checked?
2. Does it generate testable predictions?
3. Does it force consequences in a different domain? (This is where isomorphisms reside.)

### Classification

| Parameter | Classification |
|-----------|----------------|
| Implies | Black holes must exist (BH); gravitational waves must propagate (GW); time runs slower near mass (TD); light bends around massive objects (LB) |
| Predicts | Exact Mercury precession value; exact LIGO waveform shape; exact GPS correction factor |
| Cross-Domain | Forces consequences in cosmology (expansion), astrophysics (neutron stars), technology (GPS), and potentially information theory (holographic principle) |

### Analytical Yield

Einstein published the field equations in 1915. He did not predict black holes — Schwarzschild derived them as a forced consequence within months (Schwarzschild, 1916). Einstein did not predict gravitational waves either; they fell out of the mathematics in 1916 and were detected 99 years later. GPS time dilation was not predicted by Einstein but was forced by the equations long before satellites existed. The tree bore fruit its own author had not planted. This is Q6 functioning: the claim forced consequences its originator had not imagined.

---

## Q7: Falsification — The Axe

### Function

To attach death conditions to the claim, identifying the specific conditions under which it would be invalidated.

### Sub-Questions

1. Name the death condition — which of the five types? (self-refutation, infinite regress, empirical contradiction, logical incoherence, explanatory failure)
2. What breaks DOWNSTREAM if this fails? (Link to Q6 consequences.)
3. Has anyone actually TRIED to kill it, or has it only survived friendly examination?

### Classification

| Parameter | Classification |
|-----------|----------------|
| Death #1 | Empirical — if light does not bend around massive objects (tested: Eddington 1919, confirmed thousands of times since) |
| Death #2 | Empirical — if gravitational waves are not detected (tested: LIGO 2015) |
| Death #3 | Empirical — if GPS does not require relativistic correction (tested: every day) |
| Death #4 | Explanatory — if general relativity cannot handle singularities or quantum scales (LIVE — GR breaks at black hole centers and the Big Bang) |
| Status | Alive — survived 100+ years of adversarial testing. Q5's hidden root (smooth manifold assumption) remains the open wound. |
| Adversarial Testing | Survived expert attack — every major physicist for a century has attempted to break it. None have succeeded. |

### Analytical Yield

Three of the four death conditions have been tested, and general relativity has survived each. However, Death #4 remains live. General relativity produces infinities at black hole singularities and cannot describe the first instant of the Big Bang. This is not a hypothetical objection but a mathematical fact internal to the theory itself. The smooth manifold assumption identified in Q5 constitutes the axe wound. The tree stands, but the crack has been present since 1915. Whoever unifies gravity and quantum mechanics will either swing the axe that kills general relativity or heal the wound.

---

## Summary: The Complete Object

One claim, examined through seven lenses, reveals the following:

| Question | Finding |
|----------|---------|
| Q1 Identity | Causal, not descriptive — a stronger claim than most recognize |
| Q2 Domain | Structurally depends on mathematics that exists in other domains |
| Q3 Assertion | Negation splits into two independently killable parts |
| Q4 Evidence | Four independent confirmations, tier-1, no competing model matches all four |
| Q5 Dependencies | Hidden root (smooth manifold assumption) driving unsolved physics for 100 years |
| Q6 Consequences | Forced predictions its own author did not foresee: black holes, gravitational waves, GPS corrections |
| Q7 Falsification | Three death conditions survived, one still live — the singularity problem is the open wound |

Seven questions forward: classify anything.
Seven questions reversed: prove anything.
Q0: arrive humble or do not arrive at all.

---

## References

Abbott, B. P., et al. (LIGO Scientific Collaboration and Virgo Collaboration). (2016). Observation of Gravitational Waves from a Binary Black Hole Merger. *Physical Review Letters*, 116(6), 061102.

Ashby, N. (2003). Relativity in the Global Positioning System. *Living Reviews in Relativity*, 6(1), 1.

Eddington, A. S. (1919). The Deflection of Light during a Solar Eclipse. *Philosophical Transactions of the Royal Society A*, 220, 291–333.

Einstein, A. (1915). Die Feldgleichungen der Gravitation. *Sitzungsberichte der Preussischen Akademie der Wissenschaften*, 844–847.

Schwarzschild, K. (1916). Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie. *Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften*, 189–196.