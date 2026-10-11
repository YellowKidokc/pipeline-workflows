# The MDA Coherence Diagnostic: An Information-Theoretic Framework for Societal Coherence

## Abstract

This article presents the MDA Coherence Diagnostic, a formal measurement framework that applies information-theoretic divergence measures to the assessment of societal coherence. The diagnostic decomposes societal stability into ten channels, each structurally isomorphic to a fundamental law of physics, and quantifies the ratio of constructive to destructive regime dominance through a log-ratio measure. The framework yields an aggregate coherence statistic, χ\_MDA, and a dynamical equation describing the rate of change of societal coherence. This paper provides the formal derivation, methodological justification, and proposed empirical validation protocol, including five explicit falsification criteria. The framework is presented as a testable hypothesis: that the ten-law channel decomposition carries statistically significant structural information beyond arbitrary categorization of the same proxy variables.

---

## 1. Introduction: The Measurement Isomorphism

The MDA Coherence Diagnostic constitutes not an ad hoc scoring system but a formal application of established information-theoretic divergence measures to the problem of quantifying societal coherence. The diagnostic's central claim is that the mathematical structures governing information transmission, thermodynamic disequilibrium, and signal-to-noise ratio in physical systems are isomorphic to the structures governing constructive versus destructive societal dynamics.

This isomorphism was identified through structural comparison of the log-ratio measure employed in stochastic thermodynamics and Shannon information theory with the problem of measuring relative dominance of constructive over destructive social forces. The framework does not assert metaphorical correspondence but mathematical identity across measurement domains.

---

## 2. Formal Definition of the Coherence Diagnostic

### 2.1 Channel Score

For each of ten channels indexed by \(i\), the channel score \(L_i\) is defined as:

\[
L_i = \log\left(\frac{C_i + \varepsilon}{D_i + \varepsilon}\right)
\]

where:
- \(C_i\) represents the constructive proxy variable for channel \(i\) (dimensionless, normalized)
- \(D_i\) represents the destructive proxy variable for channel \(i\) (dimensionless, normalized)
- \(\varepsilon\) is a regularization constant (\(0 < \varepsilon \ll 1\)) to prevent logarithmic divergence when either variable approaches zero
- The logarithm is natural (base \(e\)) unless otherwise specified

### 2.2 Aggregate Coherence Statistic

The aggregate coherence statistic \(\chi_{\text{MDA}}\) is defined as:

\[
\chi_{\text{MDA}} = \frac{1}{N} \sum_{i=1}^{N} w_i \cdot L_i
\]

where:
- \(N = 10\) (the number of channels)
- \(w_i\) is the weight assigned to channel \(i\)
- In the current implementation, \(w_i = 1\) for all \(i\) (equal weighting)

### 2.3 Structural Isomorphism to Known Information-Theoretic Quantities

The channel score \(L_i\) is structurally identical to the log-likelihood ratio in the Kullback-Leibler divergence:

\[
D_{\text{KL}}(P \parallel Q) = \sum_x P(x) \log\left(\frac{P(x)}{Q(x)}\right)
\]

where \(P(x)\) corresponds to the normalized constructive regime distribution and \(Q(x)\) to the normalized destructive regime distribution across the measurement domain.

The aggregate statistic \(\chi_{\text{MDA}}\) is isomorphic to the Shannon channel capacity:

\[
C = B \cdot \log_2\left(1 + \frac{S}{N}\right)
\]

where the constructive signal \(C_i\) corresponds to signal power \(S\), the destructive signal \(D_i\) corresponds to noise power \(N\), and the bandwidth \(B\) corresponds to the number of channels \(N\). This is not metaphorical correspondence but mathematical identity: the log-ratio of signal to noise is the fundamental measure of information transmission fidelity in both domains.

---

## 3. Justification of the Log-Ratio Measure

The choice of log-ratio over linear difference \((C - D)\) is justified on both mathematical and physical grounds. A linear difference would assign identical scores to the pairs \((C=100, D=90)\) and \((C=10, D=0)\), despite the former representing a 10% destructive contamination and the latter representing a 100% constructive signal with zero destructive component. The log-ratio captures the *proportion* of constructive to destructive dominance, not the absolute magnitude of the gap.

This choice is consistent with information theory, where the signal-to-noise ratio (SNR) is defined as:

\[
\text{SNR} = \frac{P_{\text{signal}}}{P_{\text{noise}}}
\]

and is expressed in decibels as \(10 \log_{10}(\text{SNR})\). The relevant quantity is the ratio, not the absolute difference, because information transmission fidelity depends on the relative strength of signal to noise, not on their absolute magnitudes.

A corollary of this choice: a society with modest institutions that are internally coherent (low \(C\), lower \(D\)) scores higher than a society with massive institutions that are deeply corrupted (high \(C\), higher \(D\)). This is physically correct: a low-noise, low-signal system transmits information more faithfully than a high-noise, high-signal system.

---

## 4. The Ten-Law Channel Decomposition

The diagnostic decomposes societal coherence into ten channels, each corresponding to a fundamental law or principle of physics. This constitutes the framework's distinctive structural claim: that the ten fundamental forces and principles of physics each generate a distinct dimension of societal coherence, and that this decomposition is not arbitrary but reflects an underlying structural isomorphism between physical and social domains.

**Table 1: Ten-Law Channel Decomposition**

| Channel | Physics Domain | Societal Channel | Constructive Proxy | Destructive Proxy |
|---------|----------------|------------------|-------------------|-------------------|
| 01 | Gravitation | Community binding vs. isolation | Civic organization membership, community participation rates | Social isolation indices, loneliness prevalence |
| 02 | Motion (\(F=ma\)) | Behavioral momentum and change | Recovery program participation, behavioral health access | Addiction rates, recidivism |
| 03 | Electromagnetism | Signal integrity in discourse | Media trust indices, press freedom indices | Misinformation prevalence, propaganda saturation |
| 04 | Strong Force | Close-bond binding strength | Marriage rates, family stability indices | Divorce rates, single-parent household prevalence |
| 05 | Thermodynamics | Consequence functioning | Rule of law index, legal coherence | Recidivism rates, debt-to-income ratios, bankruptcy rates |
| 06 | Information (Shannon) | Knowledge transmission fidelity | Functional literacy rates, educational attainment | Information overload metrics, media consumption hours |
| 07 | Quantum | Commitment under uncertainty | Religious attendance rates, charitable giving | Religious disaffiliation rates |
| 08 | Relativity | Perspective-taking across difference | Cross-group trust indices, social mobility | Political polarization indices |
| 09 | Weak Force | Moral conservation (directional) | Intergenerational household stability | Family structure dissolution rates |
| 10 | Coherence | Overall systemic integration | Social cohesion indices, well-being scores | Fragmentation composites (Gini coefficient + distrust + isolation) |

*Note: Proxy variables are selected from publicly available sociological and economic datasets. Source attribution and confidence intervals for each proxy are provided in Appendix A (forthcoming).*

---

## 5. The Weight Problem: Methodological Honesty

The current implementation employs equal weights (\(w_i = 1\) for all \(i\)). This is a deliberate methodological choice, not an oversight. The framework predicts that the weights should be non-arbitrary—that the ten laws are not interchangeable and that some channels should carry greater diagnostic weight than others. However, until the weights are either:

1. Derived from the mathematical structure of the physical laws themselves (e.g., relative coupling constants), or
2. Empirically fitted to historical data and shown to be unique and stable across validation samples,

equal weighting represents the most conservative assumption. Any deviation from equal weighting introduces additional degrees of freedom that must be justified, not assumed. The burden of proof lies with any proposal for non-uniform weights.

---

## 6. The Dynamics Equation

The channel scores \(L_i\) describe the *state* of a society—its current position on the coherence spectrum. The dynamics equation describes the *motion*—the rate at which a society is moving toward coherence or collapse:

\[
\frac{dS_m}{dt} = \sigma - \frac{W}{T}
\]

where:
- \(S_m\) is the societal coherence measure (dimensionless, related to \(\chi_{\text{MDA}}\))
- \(\sigma\) is the rate of entropy production (damage accumulation, units of inverse time)
- \(W\) is restorative work (grace, reform, renewal, units of energy or equivalent)
- \(T\) is institutional resistance (bureaucratic friction, cultural inertia, system mass, units of energy·time or equivalent)

This equation is inherited from irreversible thermodynamics, specifically the Onsager reciprocal relations (Onsager, 1931) and Prigogine's formulation of entropy production in non-equilibrium systems (Prigogine, 1967). It is not original to this framework.

### 6.1 Critical Prediction

When \(T\) is large, even significant restorative work \(W\) is divided down to near-zero effectiveness (\(W/T \to 0\)). This yields the prediction that large, heavily institutionalized societies can experience internal decay while surface statistics remain stable, and that restoration in such societies requires disproportionate force—either spiritual renewal or existential threat—to overcome institutional inertia.

---

## 7. Proposed Empirical Validation: The Permutation Test

The decisive empirical test for this framework is whether the ten-law channel decomposition outperforms arbitrary groupings of the same proxy variables. The proposed protocol is as follows:

**Table 2: Permutation Test Protocol**

| Step | Procedure |
|------|-----------|
| 1 | Gather all proxy variables across all ten channels |
| 2 | Score \(\chi_{\text{MDA}}\) using the ten-law channel assignments |
| 3 | Randomly shuffle the same variables into ten arbitrary buckets |
| 4 | Score using the same procedure; record predictions for collapse/recovery/instability |
| 5 | Repeat step 3–4 for 1,000 iterations to build a null distribution |
| 6 | Compare: if the ten-law grouping sits outside the 95th percentile of the null distribution, the channel decomposition is doing statistically significant structural work |

This test has not yet been conducted. The framework makes an explicit prediction: the ten-law grouping will outperform random groupings. If it does not, the framework fails its own test and the channel decomposition should be abandoned.

---

## 8. Five Falsification Criteria

The following criteria were specified *before* empirical testing, not after. The framework is falsified if any of the following conditions obtain:

**F1:** The ten-law grouping does not outperform random groupings in the permutation test (Section 7). *Interpretation:* The channel decomposition adds no structural information beyond arbitrary categorization.

**F2:** Historical reversal cases (Josiah's reforms, the Great Awakening, the Meiji Restoration) do not score below threshold before reversal and above threshold after. *Interpretation:* The threshold concept has no historical validity.

**F3:** The 2024 United States prediction (\(\chi \approx 0.27\), below threshold) is falsified by measurable self-correction through administrative reform alone within 10 years. *Interpretation:* The framework's central prediction about the nature of recovery is incorrect.

**F4:** Channel scores show no temporal correlation—past values do not predict future values within the same channel. *Interpretation:* The channels are not measuring persistent structural features.

**F5:** A society is identified that self-corrected from below \(\chi = 0.35\) through purely administrative or political means without metaphysical renewal or existential threat. *Interpretation:* The threshold is not a boundary requiring the mechanism the framework claims.

---

## 9. Methodological Honesty: Scope and Limitations

This framework measures constructive-regime versus destructive-regime dominance across observable proxies. It does not measure sin, grace, the Holy Spirit, or any spiritual state directly. The channel labels reference physics and theology because the framework claims structural isomorphism between these domains—but the *measurements* are sociological and economic, not spiritual.

A high score does not imply that a society is righteous. A low score does not imply that a society is damned. The framework measures that observable proxies for constructive coordination are being outpaced by observable proxies for destructive dissolution. The explanation for *why* this is happening constitutes a separate inquiry from the measurement *that* it is happening.

---

## 10. Invitation to Critical Engagement

The framework is designed to be falsifiable. The permutation test (Section 7) constitutes the primary kill switch. Challenges that identify miscalibrated proxy variables, incorrect channel assignments, misscored historical cases, or structural inadequacy in the ten-law decomposition are welcomed. A challenge that holds up improves the system; a challenge that does not hold up strengthens the result.

Correspondence should include: the channel in question, the proxy variable under dispute, the proposed alternative, supporting reasoning, and source citations.

---

## References

Onsager, L. (1931). Reciprocal relations in irreversible processes. I. *Physical Review*, 37(4), 405–426.

Prigogine, I. (1967). *Introduction to thermodynamics of irreversible processes* (3rd ed.). Interscience Publishers.

Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379–423.

---

**MDA Coherence Diagnostic v1.0**
David Lowe (POF 2828)
June 2026
Theophysics Research Initiative
faiththruphysics.com
Contact: david@faiththruphysics.com