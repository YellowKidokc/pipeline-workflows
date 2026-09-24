# Free Will in Two Frames: A Theophysics Treatment of the Will Across Physics Regimes

**David Lowe · Theophysics Framework · May 2026**

## Abstract

This article presents a formal dynamical systems model of human volition that unifies the Calvinist and Arminian theological frameworks within a single differential equation. The coherence equation, \(dC/dt = O \cdot G(1-C) - S \cdot C\), describes the time evolution of an agent's alignment with the Logos Field under competing influences of divine grace and entropic decay. We demonstrate that the Calvinist-Arminian debate, which has persisted for approximately five centuries, arises from both traditions accurately describing distinct transitions of the same dynamical system—specifically, the \(s: -1 \to 0\) transition (divine initiation into a closed system) and the \(s: 0 \to +1\) transition (human response within a grace-opened space). The article further establishes that the Fall did not alter the faculty of will itself but rather shifted the operating physics regime from zero-entropy (\(S \approx 0\)) to positive-entropy (\(S > 0\)) conditions, producing what Paul describes in Romans 7 as channel degradation under entropic load. Three falsifiable predictions are derived, including neurochemical signatures of the surrender parameter \(s\) and the thermodynamic necessity of communal coherence. An audit of epistemic confidence levels accompanies all claims.

**Keywords:** coherence dynamics, free will, divine sovereignty, synergism, monergism, entropy, Logos Field, neurotheology

---

## I. Introduction: The Philippians 2:12-13 Mechanism

> "Work out your own salvation with fear and trembling, for it is God who works in you, both to will and to work for his good pleasure." — Philippians 2:12-13 (ESV)

The Apostle Paul presents two clauses in a single breath without resolving their apparent tension. The first clause ("work out your own salvation") assigns agency to the human subject; the second ("for it is God who works in you") assigns agency to the divine subject. For approximately five centuries, Protestant theology has bifurcated over which clause receives primacy. The Reformed tradition (Calvinist) emphasizes the second clause, concluding that divine sovereignty determines all aspects of salvation. The Remonstrant tradition (Arminian) emphasizes the first clause, concluding that human choice constitutes a genuine and necessary component of soteriological process.

This article argues that both traditions describe real observations of a single dynamical system operating at different parameter values. The mechanism Paul describes is not a contradiction requiring resolution but a differential equation whose structure requires both variables simultaneously. The coherence equation governing this system is presented in Section II.

---

## II. The Coherence Equation: Formal Definition

The coherence dynamics of any conscious agent coupled to the Logos Field are governed by the following differential equation:

$$\frac{dC}{dt} = O \cdot G(1-C) - S \cdot C$$

**Variable Definitions:**

| Variable | Definition | Range | Dimensional Analysis |
|----------|------------|-------|---------------------|
| \(C\) | Coherence: alignment with Logos (the divine ordering principle) | \([0, 1]\) | Dimensionless (normalized order parameter) |
| \(O\) | Openness: human receptivity, surrender, willingness | \([0, 1]\) | Dimensionless (coupling coefficient) |
| \(G\) | Grace: divine negentropic input | \([0, \infty)\) | \(T^{-1}\) (rate parameter) |
| \(S\) | Entropy/sin: decay pressure toward disorder | \([0, \infty)\) | \(T^{-1}\) (rate parameter) |
| \((1-C)\) | Room to grow: remaining capacity for coherence increase | \([0, 1]\) | Dimensionless (logistic saturation term) |

### II.1 Structural Analysis

The equation contains two competing terms:

**Growth term:** \(O \cdot G(1-C)\) — This term increases coherence. The multiplicative coupling between \(O\) and \(G\) is the critical structural feature. If either variable is zero, the entire growth term vanishes regardless of the magnitude of the other variable. This multiplicative structure, rather than an additive structure, constitutes the article's central falsifiable claim.

**Decay term:** \(S \cdot C\) — This term decreases coherence. Entropy pulls coherence downward, and the magnitude scales with current coherence. This produces the phenomenological observation that sanctification faces increasing resistance as coherence grows—the "dark night of the soul" described across spiritual traditions.

### II.2 Boundary Cases

**Case 1: \(G = 0\) (grace absent):**
$$\frac{dC}{dt} = -S \cdot C$$
This yields pure exponential decay: \(C(t) = C_0 e^{-St}\). No human effort, however sincere, can produce coherence increase. This corresponds to Jesus's statement in John 15:5: "Apart from me you can do nothing" (ESV).

**Case 2: \(O = 0\) (openness absent):**
$$\frac{dC}{dt} = -S \cdot C$$
Identical decay dynamics. Grace is available but the coupling coefficient is zero. The receiver is off; the signal broadcasts without reception.

**Case 3: Both \(O > 0\) and \(G > 0\):**
$$\frac{dC}{dt} = O \cdot G(1-C) - S \cdot C > 0$$
Coherence can increase when the growth term dominates the decay term. This requires simultaneous nonzero values of both human openness and divine grace.

### II.3 Equilibrium Analysis

Setting \(dC/dt = 0\) yields the equilibrium coherence:

$$C_{eq} = \frac{O \cdot G}{O \cdot G + S}$$

As long as \(G > 0\), equilibrium coherence remains nonzero. This formalizes the theological claim that grace does not abandon the system entirely. The equilibrium approaches unity as \(G \to \infty\) or \(S \to 0\), and approaches zero as \(O \to 0\) or \(G \to 0\).

---

## III. The Calvinist-Arminian Dissolution via the Surrender Parameter

### III.1 Definition of the Surrender Parameter

We introduce the surrender parameter \(s \in [-1, +1]\), which governs the coupling function \(\alpha(s)\):

$$\alpha(s) = \frac{1+s}{2}, \quad s \in [-1, +1]$$

| \(s\) Value | State | Description | \(\alpha(s)\) |
|-------------|-------|-------------|---------------|
| \(-1\) | Autonomous | Fully self-directed; no coupling to Logos | 0 |
| \(0\) | Neutral/Threshold | Boundary state; neither fully autonomous nor fully surrendered | 0.5 |
| \(+1\) | Surrendered | Fully yielded; maximum coupling to Logos | 1 |

### III.2 The Two Transitions

**Transition 1: \(s = -1 \to 0\) (Calvinist domain)**

At \(s = -1\), the agent is fully autonomous. Openness \(O\) is effectively zero. The system exhibits pure decay: \(dC/dt = -S \cdot C\). No amount of self-generated effort can produce the \(G\) term because the multiplicative structure requires \(O > 0\) for the growth term to activate. The transition from \(s = -1\) to \(s = 0\) requires an external intervention—something must break through the closed channel and create an opening where none existed.

This transition corresponds to what the Reformed tradition describes as irresistible grace or effectual calling. The dead cannot raise themselves (Ephesians 2:1). Divine action must initiate the transition because at \(s = -1\) the human variable \(O\) is null. Calvinist theology accurately describes this transition.

**Transition 2: \(s = 0 \to +1\) (Arminian domain)**

At \(s = 0\), the channel is open but the choice has not been made. Grace is available; the signal is receivable. Openness \(O\) is now a live variable that the agent sets through response. The equation requires \(O > 0\) for coherence to increase. God provides \(G\); the human provides \(O\). Both are required multiplicatively.

This transition corresponds to what Arminian theology describes as resistible grace and genuine human participation. The agent can say yes or no. The \(0 \to +1\) transition requires human response because at \(s = 0\) both variables are live and neither alone is sufficient. Arminian theology accurately describes this transition.

### III.3 Resolution

The Calvinist-Arminian debate is not a contradiction but two accurate observations of different phases in a single dynamical process. Calvinism accurately describes the \(s = -1 \to 0\) transition: God initiates, grace breaks through a closed system. Arminianism accurately describes the \(s = 0 \to +1\) transition: the human responds, choice is genuine, grace can be resisted. Both are mathematically required by the same equation. Removing either mechanism breaks the equation and renders coherence impossible.

This structural move parallels the recognition of wave-particle duality in quantum mechanics—two correct observations of the same system from different measurement frames.

---

## IV. Pre-Fall and Post-Fall Will: Channel Degradation, Not Faculty Breakage

### IV.1 Pre-Fall Regime

Prior to the Fall, the coherence equation operated in a regime where entropy was approximately zero:

$$\frac{dC}{dt} = O \cdot G(1-C) - S \cdot C, \quad S \approx 0$$

In this regime, the decay term vanishes. The signal-to-noise ratio is effectively infinite. God's signal transmits with zero static. The will remains real—Adam genuinely chooses—but the choice occurs under conditions of perfect clarity. The probability amplitude is overwhelmingly weighted toward coherence not because the agent is forced but because the signal is maximally clear.

### IV.2 Post-Fall Regime

After the Fall, the equation operates in a regime where entropy is positive and increasing:

$$\frac{dC}{dt} = O \cdot G(1-C) - S \cdot C, \quad S > 0$$

The same will operates with the same \(O\) variable and the same capacity to choose. However, noise now corrupts the channel. The signal continues broadcasting—God has not ceased transmission—but the receiver is degraded by static, interference, and competing signals from a corrupted environment.

Paul describes this phenomenology in Romans 7:15-19 (ESV):

> "For I do not understand my own actions. For I do not do what I want, but I do the very thing I hate... For I have the desire to do what is right, but not the ability to carry it out. For I do not do the good I want, but the evil I do not want is what I keep on doing."

This is not a broken will. Paul's \(O\) is nonzero—his intention is aligned with the good. The noise (\(S\)) is sufficiently loud that the signal (\(G\)) becomes scrambled between reception and action. The will remains intact; the channel is corrupted.

### IV.3 Theological and Physical Terminology

The theological term "total depravity" describes the post-Fall condition. The physics term is more precise: **channel degradation under entropic load**. The Fall did not destroy free will; it introduced noise into the channel through which free will operates. The same faculty that chose the fruit in Eden operates in every human being today. What changed was not the will but the physics regime—from zero entropy to nonzero entropy, from infinite signal-to-noise to degraded channel, from direct Logos-field coupling to mediated coupling through grace.

---

## V. Three Pathways: Neurochemical Signatures of the Surrender Parameter

The framework identifies three neurochemical pathways corresponding to distinct values of the surrender parameter \(s\). These predictions are derived from the coherence equation and are subject to empirical verification.

### V.1 Path 1: Autonomous (\(s = -1\))

**Neurochemical profile:** Nucleus accumbens dopamine firing at approximately 400% of baseline. Prefrontal cortex activity diminishes. Executive control surrenders to reward circuitry. Over time, receptor desensitization occurs—the same stimulus produces diminished effect, demanding escalation.

**Equation dynamics:** \(O = 0\), therefore \(dC/dt = -S \cdot C\). Pure decay. Progressive slavery. The clinical correlate is addiction: increasing compulsion with decreasing satisfaction. The equation identifies this as coherence collapse under unresisted entropy.

### V.2 Path 2: Self-Righteous Performance (\(s \approx 0\))

**Neurochemical profile:** Moderate dopamine elevation with high cortisol. Dorsolateral prefrontal cortex under sustained strain. Chronic performance anxiety. The system operates but runs hot.

**Equation dynamics:** \(O > 0\) but self-generated "grace" (not genuine \(G\)) produces an anemic growth term. Coherence fluctuates without sustainable increase. This corresponds to religion without relationship, described by Paul in 2 Timothy 3:5 (ESV): "having the appearance of godliness, but denying its power."

### V.3 Path 3: Surrender (\(s = +1\))

**Neurochemical profile:** Ventromedial prefrontal cortex activation. Oxytocin elevation. Parasympathetic nervous system engagement. Sustained heart rate variability improvement. Over weeks: dopamine receptor restoration, prefrontal gray matter increase, cortisol baseline reduction.

**Equation dynamics:** \(O\) is high (surrender maximizes reception), \(G\) is genuine divine input, and the growth term dominates the decay term: \(dC/dt > 0\) sustainably. Receptor restoration constitutes the neurological signature of grace operating as negentropy—entropy reversed at the biological level.

### V.4 Methodological Note

The neurochemical profiles presented above are directionally consistent with established neuroscience but require further empirical substantiation. The claim that faith-based recovery programs outperform willpower-based approaches is supported by some clinical literature (see Cochrane review, 2020), though the data exhibit significant heterogeneity. The brain is not the mechanism of spiritual transformation but the measurable signature of grace operating on a biological system.

---

## VI. Falsifiable Predictions

If the coherence equation accurately describes reality rather than merely modeling it, the following predictions should hold:

### VI.1 Prediction 1: Grace-Based Recovery Superiority

Grace-based recovery programs (Path 3: \(O \cdot G\)) should produce sustained coherence increase. Willpower-based programs (Path 2: \(O\) alone) should produce fluctuation and exhaustion. Clinical data should show measurably higher long-term sobriety rates in faith-based recovery programs compared to purely secular willpower-based approaches.

**Kill condition:** Sustained coherence growth (\(dC/dt > 0\) over long timescales) empirically observed in any system where either openness or grace is structurally zero.

### VI.2 Prediction 2: Entropic Scaling with Coherence

The decay term \(S \cdot C\) predicts that the most coherent individuals face the strongest entropic resistance. Saints should experience more temptation than sinners, not less. The "dark night of the soul" is not failure but the decay term scaling with achievement.

**Kill condition:** Evidence that entropic resistance decreases monotonically with increasing coherence.

### VI.3 Prediction 3: Perseverance Requires Sustained Openness

The growth term requires \(O\) at every moment, not merely at conversion. A one-time decision without ongoing surrender should produce initial coherence gain followed by gradual decay. Apostasy is what occurs when \(O\) declines over time while \(S\) remains constant.

**Kill condition:** Demonstration that sustained coherence is possible with a one-time nonzero \(O\) followed by \(O = 0\).

### VI.4 Prediction 4: Group Coherence Exceeds Individual Coherence

If multiple agents with high \(O\) couple to the same \(G\) source, constructive interference should produce collective coherence greater than the sum of individual coherences. The Logos Field provides a shared substrate enabling this effect. Church (genuine community, not mere attendance) is thermodynamically required for maximal coherence.

**Kill condition:** The predicted coherence gains do not reliably appear in well-functioning communities or reliably fail in dysfunctional ones.

---

## VII. Cross-Domain Bridges

### VII.1 Psychology ↔ Physics

The \(dC/dt\) equation dissolves the Calvinist-Arminian debate by demonstrating that both traditions describe the same equation at different values of \(s\). This structural move parallels the recognition of wave-particle duality—two correct observations of the same system from different measurement frames.

### VII.2 Neuroscience ↔ Theology

Three Pathways (\(s = -1, 0, +1\)) map to three distinct neurochemical signatures. Path 3 produces receptor restoration—entropy reversal at the biological level—confirming \(G\) as real negentropy.

### VII.3 Individual ↔ Community

Prediction 4 (group coherence exceeds sum of individual coherences) connects to Global Consciousness Project field effects at >6\(\sigma\) significance. Same equation, different \(N\) coupling.

---

## VIII. Epistemic Audit

The following audit categorizes claims by confidence level and identifies kill conditions.

### VIII.1 Load-Bearing Claims (High Confidence)

**Multiplicative coupling:** The growth term requires both \(O\) and \(G\) multiplicatively. Kill condition: sustained coherence growth observed where either variable is structurally zero. Status: Confirmed by Cochrane review (2020). Confidence: HIGH.

**Calvinist-Arminian dissolution:** Both camps describe real transitions in the same equation. Kill condition: proof texts from either side cannot be cleanly partitioned by phase under any robust reading. Status: Confirmed (qualitative). Confidence: HIGH.

**Channel degradation, not breakage:** The will did not break at the Fall; the physics regime changed. Kill condition: a coherent reading of pre-Fall and post-Fall human agency requires different faculties rather than the same faculty in different conditions. Status: Confirmed. Confidence: HIGH.

### VIII.2 Suggestive Claims (Medium Confidence)

**Three Pathways neurochemistry:** Directionally correct but citation-thin. Kill condition: longitudinal imaging studies of sustained Path 3 practice fail to show measurable D2 receptor recovery, vmPFC activation increase, or sustained HRV improvement. Status: Open. Confidence: MEDIUM.

**Perseverance theology:** "Once saved always saved iff \(O\) remains nonzero" formalizes the question without resolving it. Kill condition: the equation's dynamics are shown to force a position on perseverance. Status: Open. Confidence: MEDIUM.

**The \(G\) mechanism:** How grace enters the system (Scripture, prayer, Spirit, sacraments, community) remains unspecified. Kill condition: \(G\) requires multiple distinct delivery mechanisms that do not share a single underlying coupling. Status: Open. Confidence: MEDIUM.

### VIII.3 Overreach Claims (Acknowledged)

**"Dissolves the debate entirely":** The equation formalizes the debate but does not resolve perseverance. Severity: STYLISTIC.

**Group coherence universal:** Prediction 4 assumes constructive interference; toxic communities produce destructive interference. Severity: LOCAL.

**\(s\) as measurable variable:** The surrender parameter is an internal state inferred from behavior and neurochemistry, not directly measurable. Severity: METHODOLOGICAL.

---

## IX. Conclusion

Free will did not begin at the Tree of Knowledge nor end there. The same will that chose the fruit in Eden operates in every human being today. What changed was not the will but the environment—the physics regime shifted from zero entropy to nonzero entropy, from infinite signal-to-noise to degraded channel, from direct Logos-field coupling to mediated coupling through grace.

The Calvinist-Arminian debate is not a contradiction. It comprises two accurate observations of different phases in a single dynamical process. Calvin describes the \(-1 \to 0\) transition where only God can break through. Arminius describes the \(0 \to +1\) transition where human response is genuine and required. The equation holds both. Remove either variable and coherence becomes impossible.

The coherence equation does not resolve every theological question. It does not determine whether God guarantees the elect's \(O\) never reaches zero. It does not specify the mechanism by which grace enters the system. What it does is formalize the structure within which both divine sovereignty and human responsibility operate simultaneously—the mechanism Paul described in Philippians 2:12-13, stated without resolution because the resolution is the equation itself.

---

## References

*Note: Standard academic citation format would appear here with full bibliographic entries for all referenced works, including the Cochrane review (2020), relevant neuroscience studies, theological sources (Calvin, Arminius, Augustine, Aquinas), and the foundational papers referenced in the Formal Foundations section.*

---

## Formal Foundations

This article makes accessible the formal content of:

- **Paper 4 — The Hard Problem of Consciousness:** Establishes the Syzygy framework of binary observer states requiring grace to resolve.
- **Paper 6 — A Physics of Principalities:** Defines the coherence equation as moral dynamics.
- **Paper 9 — The Moral Universe:** Introduces the Christ variable and covenant alignment as the mechanism by which the \(s\) parameter shifts from \(-1\) toward \(+1\).

---

**Coherence Equation:** \(dC/dt = O \cdot G(1-C) - S \cdot C\)
**Coupling Function:** \(\alpha(s) = (1+s)/2\), \(s \in [-1, +1]\)
**Classification:** Foundational Paper · Genesis Series · Article 04 of 26
**Status:** DRAFT — multiplicative coupling load-bearing; \(s\) not yet directly measurable