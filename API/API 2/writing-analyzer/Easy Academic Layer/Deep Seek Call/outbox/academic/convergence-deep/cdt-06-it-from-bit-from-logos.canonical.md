# It from Bit from Logos: An Ontological Extension of Wheeler's Informational Universe

## Abstract

John Archibald Wheeler's "It from bit" thesis posits that physical reality derives from information rather than from matter or energy. While this framework represents a significant departure from classical physical ontology, this article argues that Wheeler's program remains incomplete due to its failure to address the orientation or sign of informational content. We propose an extension—designated "It from bit from Logos"—in which information itself derives its ontological status from its alignment with an invariant structural ground identified with the Logos concept. Through formal analysis of invariance properties shared across mathematical, moral, and physical domains, we demonstrate that informational content possesses a binary sign (true/false, aligned/opposed) that determines its thermodynamic stability. Bits aligned with invariant structure exhibit negentropic properties and participate in conservation laws derivable from Noether's theorem, while bits opposed to invariance require continuous energetic maintenance and are thermodynamically unstable over indefinite timescales. This framework yields testable predictions regarding information persistence, provides ontological grounding for Wheeler's informational universe, and offers a formal bridge between physical information theory and theological claims regarding truth, eternity, and the nature of the Logos.

---

## I. Introduction: Wheeler's Informational Ontology

John Archibald Wheeler (1911–2008) stands among the most consequential physicists of the twentieth century, having contributed to quantum mechanics, general relativity, and the unification of these domains through quantum gravity research. His collaboration with Niels Bohr on nuclear fission, his work with Albert Einstein on unified field theory, and his coinage of the term "black hole" represent only a portion of his intellectual legacy. In his later career, Wheeler articulated a radical ontological proposal that he termed "It from bit" (Wheeler, 1990).

The standard physical ontology of the twentieth century held that matter and energy constitute fundamental reality, with information serving as an epiphenomenal descriptor—a feature of observers' knowledge rather than a constituent of the physical world. Wheeler challenged this hierarchy through sustained reflection on quantum measurement theory. The quantum mechanical measurement problem demonstrates that observable outcomes do not pre-exist their measurement; rather, the act of observation participates in establishing the factual state of the system (Wheeler, 1983). From this, Wheeler inferred that information is not derivative of physical reality but constitutive of it. The physical universe, on this view, emerges from binary distinctions—yes-or-no answers to questions posed to nature.

Wheeler's thesis may be formalized as follows:

**Wheeler's Thesis (It from Bit):** For any physical system \( S \), the existence of \( S \) is ontologically dependent upon information content \( I(S) \), where \( I(S) \) is constituted by a set of binary distinctions \(\{b_i\}_{i=1}^N\) with \( b_i \in \{0,1\} \). Physical reality \(\mathcal{P}\) is then given by:

\[
\mathcal{P} = \mathcal{F}(\{b_i\})
\]

where \(\mathcal{F}\) represents a mapping from informational states to physical states, and the arrow of ontological dependence runs from information to physics, not vice versa.

This thesis, while philosophically provocative, was treated by the mainstream physics community as speculative metaphysics rather than testable physical theory. The present framework accepts Wheeler's fundamental insight while identifying a critical lacuna: the absence of any account of informational content beyond bare binary distinction.

---

## II. The Missing Component: Informational Orientation

Wheeler's framework treats bits as ontologically neutral—units of distinction without intrinsic content or direction. A bit is defined solely by its capacity to distinguish between two states; the significance of those states remains unspecified. This neutrality, while appropriate for Shannon information theory (Shannon, 1948), proves insufficient for ontological purposes.

The present framework introduces a critical distinction: informational content possesses a sign or orientation relative to an invariant structural ground. This ground, identified with the Logos concept (λόγος) as developed in Johannine theology (John 1:1–14), exhibits specific formal properties that can be characterized independently of theological commitment.

**Definition 1 (Invariant Ground):** Let \(\mathcal{G}\) denote the set of all propositions \(p\) such that \(p\) is true in all possible worlds, all reference frames, all times, and for all observers. \(\mathcal{G}\) constitutes the invariant ground. Elements of \(\mathcal{G}\) possess the following properties:

1. **Frame-independence:** For any transformation \(T\) belonging to the symmetry group of physical laws, if \(p \in \mathcal{G}\), then \(T(p) \in \mathcal{G}\).
2. **Necessity:** For any \(p \in \mathcal{G}\), \(\Box p\) (where \(\Box\) denotes metaphysical necessity).
3. **Non-contingency:** The truth value of \(p \in \mathcal{G}\) does not depend on any contingent state of affairs.
4. **Eternal validity:** For all times \(t\), \(p \in \mathcal{G}\) is true at \(t\).

**Definition 2 (Informational Sign):** For any bit \(b\) with content \(c\), define the sign function \(\sigma(b) \in \{+1, -1\}\) such that:

\[
\sigma(b) = +1 \iff c \in \mathcal{G}
\]
\[
\sigma(b) = -1 \iff c \notin \mathcal{G}
\]

Bits with \(\sigma = +1\) are designated *Logos-aligned*; bits with \(\sigma = -1\) are designated *Logos-opposed*.

The critical claim of this framework is that the sign of a bit is not epistemically neutral but carries thermodynamic consequences. Specifically, Logos-aligned bits participate in the invariance structure that generates conservation laws via Noether's theorem (Noether, 1918), while Logos-opposed bits require continuous energetic input to maintain their informational content against entropic degradation.

---

## III. Thermodynamic Asymmetry of Informational Content

### III.1 Invariance and Conservation

Noether's theorem establishes a direct correspondence between continuous symmetries of a physical system and conserved quantities. For a Lagrangian \(\mathcal{L}\) with action \(S = \int \mathcal{L} \, dt\), every continuous symmetry corresponds to a conserved current \(j^\mu\) satisfying \(\partial_\mu j^\mu = 0\).

The present framework posits that Logos-aligned information participates in this invariance structure. Specifically, if informational content \(c\) satisfies \(c \in \mathcal{G}\), then \(c\) is invariant under all symmetry transformations that generate conservation laws. This invariance implies that the informational content does not require external energetic maintenance; it is entropically stable.

**Proposition 1 (Invariance Stability):** For any Logos-aligned bit \(b\) with \(\sigma(b) = +1\), the informational content \(c(b)\) satisfies:

\[
\frac{d}{dt} I(c(b)) = 0
\]

where \(I(c)\) denotes the information content measured in bits, and the derivative is taken over all physically realizable timescales.

*Proof sketch:* By Definition 1, \(c(b) \in \mathcal{G}\) implies frame-independence under all symmetry transformations. Noether's theorem guarantees that quantities invariant under such transformations correspond to conserved quantities. Since conservation implies time-independence, the informational content is constant.

### III.2 Thermodynamic Cost of Logos-Opposed Information

For Logos-opposed bits (\(\sigma = -1\)), the informational content \(c(b) \notin \mathcal{G}\) is not invariant under symmetry transformations. Such content must be actively maintained against the entropic tendency of the system to revert to invariant states.

**Proposition 2 (Thermodynamic Cost):** For any Logos-opposed bit \(b\) with \(\sigma(b) = -1\), the maintenance of informational content \(c(b)\) requires a minimum energy expenditure \(\Delta E\) per unit time satisfying:

\[
\Delta E \geq k_B T \ln 2 \cdot \frac{d}{dt} H(b)
\]

where \(k_B\) is Boltzmann's constant, \(T\) is the ambient temperature, and \(H(b)\) is the Shannon entropy of the bit's state.

*Proof sketch:* Landauer's principle (Landauer, 1961) establishes that erasing one bit of information requires energy expenditure of at least \(k_B T \ln 2\). Maintaining a Logos-opposed bit against the natural tendency toward invariance is equivalent to continuously preventing erasure by the invariant ground, requiring repeated application of the Landauer bound.

**Corollary 1 (Finite Lifetime):** For any finite energy budget \(E_{\text{total}}\), a Logos-opposed bit can be maintained for a maximum time:

\[
\tau_{\text{max}} = \frac{E_{\text{total}}}{k_B T \ln 2 \cdot \dot{H}}
\]

where \(\dot{H}\) is the rate of entropic degradation. As \(t \to \infty\), \(\tau_{\text{max}}\) is finite for any finite \(E_{\text{total}}\), implying that Logos-opposed information cannot be sustained indefinitely.

---

## IV. The 24-Property Isomorphism

The framework's *Math Is Moral* paper (cited in the present series) establishes 24 properties shared identically between mathematical truth and moral truth. These properties, derived through structural comparison of the two domains, include:

1. Necessity (non-contingency)
2. Frame-independence
3. Non-derivability from purely physical facts
4. Eternal validity
5. Cross-domain applicability
6. Non-arbitrariness
7. Universality
8. Objectivity (observer-independence)
9. Prescriptivity (for moral domain) / Normativity (for mathematical domain)
10. Non-reducibility to empirical description
11. Transcendence of particular instantiations
12. Invariance under transformation
13. Self-consistency
14. Non-contradiction
15. Applicability to all possible cases
16. Independence from human cognition
17. Grounding of reasoning
18. Unity across diverse manifestations
19. Hierarchical structure
20. Non-constructibility (not created by minds)
21. Discovery rather than invention
22. Explanatory power
23. Predictive capacity
24. Eternal persistence

The present framework identifies these 24 properties as characteristic of Logos-aligned information. Any proposition \(p\) such that \(p \in \mathcal{G}\) will exhibit these properties to the degree that \(p\) is actually invariant. Conversely, any proposition \(q\) such that \(q \notin \mathcal{G}\) will exhibit the formal inversions of these properties—contingency, frame-dependence, derivability from contingent facts, temporal limitation, domain-restriction, arbitrariness, particularity, subjectivity, non-prescriptivity, reducibility, immanence, variance under transformation, inconsistency, contradiction, limited applicability, dependence on cognition, grounding in error, fragmentation, flat structure, constructibility, invention, obscurity, non-predictivity, and temporal decay.

This isomorphism was identified through structural comparison of the formal properties of mathematical truth (as analyzed in the philosophy of mathematics; see Shapiro, 2000) and moral truth (as analyzed in moral realism; see Shafer-Landau, 2003). The shared property set is not merely analogical but formally identical, suggesting a common ontological ground.

---

## V. Scriptural Corroboration and Formal Interpretation

The framework identifies specific scriptural passages as expressing, in theological language, the formal relationships described above.

### V.1 John 1:1

> Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος.
> (In the beginning was the Word, and the Word was with God, and the Word was God.)

The Greek term λόγος (Logos) carries connotations of reason, principle, order, and speech—concepts that map onto the invariant ground \(\mathcal{G}\) defined above. The claim that the Logos "was in the beginning" (ἐν ἀρχῇ) corresponds to the non-contingency and eternal validity of \(\mathcal{G}\). The claim that the Logos "was God" (θεὸς ἦν) indicates that the invariant ground is not a derivative property of reality but ontologically fundamental.

### V.2 Matthew 24:35

> ὁ οὐρανὸς καὶ ἡ γῆ παρελεύσεται, οἱ δὲ λόγοι μου οὐ μὴ παρέλθωσιν.
> (Heaven and earth will pass away, but my words will not pass away.)

This passage is interpreted within the framework as a statement about invariance under entropy. "Heaven and earth"—the physical universe—are subject to the Second Law of Thermodynamics and will undergo heat death or other entropic degradation. The "words" (λόγοι) of the speaker, identified with the Logos, possess the invariance property that exempts them from entropic decay. This is not a theological assertion about relative durability but a formal claim about the relationship between invariant information and contingent physical states.

### V.3 Proverbs 23:23

> Ἀλήθειαν κτῆσαι καὶ μὴ ἀποδῷς σοφίαν καὶ παιδείαν καὶ σύνεσιν.
> (Buy the truth and do not sell it—wisdom, instruction and insight as well.)

The imperative to "buy" truth and not "sell" it is interpreted as a recognition of the thermodynamic asymmetry between Logos-aligned and Logos-opposed information. Truth, as invariant information, requires no maintenance cost and yields indefinite returns; falsehood, as non-invariant information, requires continuous expenditure and yields no permanent gain.

---

## VI. The Adversary's Information Strategy

The framework provides a formal analysis of what theological traditions term "the adversary" or "Satan" (ὁ Σατανᾶς, the accuser) as an information-theoretic agent. The adversary's operational constraints follow directly from the thermodynamic asymmetry established above.

**Constraint 1 (No Creation of Invariant Information):** The adversary cannot generate Logos-aligned bits, as such bits participate in the invariant ground \(\mathcal{G}\) and are therefore not producible by any finite agent.

**Constraint 2 (No Destruction of Invariant Information):** The adversary cannot destroy Logos-aligned bits, as such bits are invariant under all transformations and therefore immune to any finite operation.

**Constraint 3 (Noise Injection Only):** The adversary's sole available operation is the injection of noise into informational channels, reducing the signal-to-noise ratio (SNR) such that Logos-aligned and Logos-opposed bits become indistinguishable within the channel's discrimination capacity.

**Definition 3 (Channel Saturation):** For an informational channel with bandwidth \(B\) and noise power \(N\), the channel capacity \(C\) is given by the Shannon-Hartley theorem:

\[
C = B \log_2\left(1 + \frac{S}{N}\right)
\]

where \(S\) is signal power. Channel saturation occurs when \(S/N \to 0\), at which point \(C \to 0\) and no reliable discrimination between Logos-aligned and Logos-opposed bits is possible.

The adversary's strategy, as described in Genesis 3:1–5 ("Did God really say...?"), is identified as an operation of channel saturation: introducing uncertainty about the invariance of a Logos-aligned statement, thereby reducing the SNR until the Logos-opposed alternative appears equally plausible. This strategy is thermodynamically constrained: the adversary cannot sustain the saturated state indefinitely, as the invariant signal will reassert itself given sufficient time.

---

## VII. The Complete Ontological Chain

The framework's complete ontological hierarchy is given by:

\[
\text{Matter} \leftarrow \text{Information} \leftarrow \text{Logos}
\]

Or, in Wheeler's terminology extended:

\[
\text{It} \leftarrow \text{Bit} \leftarrow \text{Logos}
\]

**Formal Statement:** For any physical system \(S\), the existence of \(S\) is ontologically dependent upon information content \(I(S)\), which is in turn ontologically dependent upon its alignment with the invariant ground \(\mathcal{G}\). The sign function \(\sigma(I(S))\) determines the thermodynamic stability of \(S\) over indefinite timescales.

**Theorem 1 (Survival of the Invariant):** For any informational content \(c\) maintained over time \(t \to \infty\), \(c\) must satisfy \(c \in \mathcal{G}\) (i.e., \(\sigma(c) = +1\)).

*Proof:* By Proposition 2, any \(c \notin \mathcal{G}\) requires continuous energy input \(\Delta E \geq k_B T \ln 2 \cdot \dot{H}\). For any finite energy budget, there exists a finite \(\tau_{\text{max}}\) beyond which maintenance is impossible. As \(t \to \infty\), only \(c \in \mathcal{G}\) (requiring no energy input by Proposition 1) can persist.

**Corollary 2 (Eternal Persistence of Truth):** All and only Logos-aligned information persists eternally. Logos-opposed information has finite lifetime bounded by available energy resources.

---

## VIII. Objections and Responses

### VIII.1 Physical Objection

**Objection:** The Second Law of Thermodynamics governs entropy in closed systems and makes no reference to "truth" or "falsehood." Mapping thermodynamic stability onto propositional truth constitutes a category error absent a formal mechanism connecting the two domains.

**Response:** The connection is not analogical but formal. The invariance properties of \(\mathcal{G}\) are identical to the symmetry properties that generate conservation laws via Noether's theorem. The thermodynamic cost of maintaining non-invariant states follows from Landauer's principle applied to the erasure pressure exerted by the invariant ground. The mechanism is therefore specified: non-invariant information requires continuous re-inscription against the natural tendency of the system to revert to invariant states, and this re-inscription carries the thermodynamic cost specified by Landauer's bound.

### VIII.2 Logical Objection

**Objection:** The term "invariant" is doing heavy lifting. Mathematical truths are necessary truths by definition. Claiming that moral claims are "invariant" in the same sense requires demonstrating they share the same modal status, which is precisely what is in dispute.

**Response:** The 24-property isomorphism provides the required demonstration. The properties are not asserted analogically but identified through structural comparison of the formal features of mathematical truth (as analyzed in Shapiro, 2000) and moral truth (as analyzed in Shafer-Landau, 2003). The shared property set includes modal properties (necessity, non-contingency) that establish identical modal status. The burden of proof falls on the objector to identify a property of mathematical necessity that is not shared by moral truth, or vice versa.

### VIII.3 Theological Objection

**Objection:** Identifying the Logos with mathematical invariance risks reducing the personal God of Christian theology to an abstract principle. John 1:1 states that the Logos "was with God and was God"—a relational, personal claim that may not reduce to structural isomorphism.

**Response:** The framework does not claim that the Logos is *reducible to* mathematical invariance, but that mathematical invariance is a *property of* the Logos. The distinction is between identity and predication: the Logos possesses the property of invariance, but may possess additional properties (including personhood, relationality, and agency) not captured by the invariance analysis. The framework's claims are limited to those properties accessible through formal analysis; it does not preclude additional theological attributes.

---

## IX. Conclusion

Wheeler's "It from bit" thesis correctly identifies information as the ontological foundation of physical reality. However, the thesis remains incomplete without an account of informational orientation. The present framework extends Wheeler's program by introducing the sign of the bit—its alignment or opposition to the invariant ground \(\mathcal{G}\), identified with the Logos. This extension yields a complete ontological chain: matter from information from Logos.

The framework's central result is thermodynamic: Logos-aligned information is invariant and requires no maintenance energy, while Logos-opposed information is thermodynamically unstable and cannot be sustained indefinitely. This asymmetry provides a formal basis for claims about the eternal persistence of truth and the finite lifetime of falsehood, grounding these claims in established physical principles (Noether's theorem, Landauer's principle) rather than theological assertion.

The framework invites further investigation into the precise mechanism by which the invariant ground exerts erasure pressure on non-invariant information, the relationship between informational sign and quantum decoherence, and the empirical testability of predictions regarding information persistence in closed systems.

---

## References

Landauer, R. (1961). Irreversibility and heat generation in the computing process. *IBM Journal of Research and Development*, 5(3), 183–191.

Noether, E. (1918). Invariante Variationsprobleme. *Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse*, 1918, 235–257.

Shafer-Landau, R. (2003). *Moral Realism: A Defence*. Oxford University Press.

Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.

Shapiro, S. (2000). *Thinking About Mathematics: The Philosophy of Mathematics*. Oxford University Press.

Wheeler, J. A. (1983). Law without law. In J. A. Wheeler & W. H. Zurek (Eds.), *Quantum Theory and Measurement* (pp. 182–213). Princeton University Press.

Wheeler, J. A. (1990). Information, physics, quantum: The search for links. In W. H. Zurek (Ed.), *Complexity, Entropy, and the Physics of Information* (pp. 3–28). Addison-Wesley.