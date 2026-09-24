# The Universal Signal Persistence Framework: A Formal Isomorphism with Shannon Channel Capacity Theory

## Abstract

This article presents the Universal Signal Persistence Framework (USPF), a formal mathematical structure for quantifying the robustness of signal transmission across historical and cross-domain channels. The framework establishes a direct isomorphism with Claude Shannon's Channel Capacity Theorem (Shannon, 1948), mapping signal integrity and mechanism strength to signal power, and survival pressure to the signal-to-noise ratio. The resulting multiplicative formulation—Strength = S · M · ln(1 + P)—preserves the logarithmic structure of Shannon's original equation while extending its domain of application from telecommunications to the persistence of written, oral, mathematical, physical, legal, biological, and artistic signals over extended temporal scales. The framework incorporates pre-registration requirements, category-locked baseline normalization, and explicit methodological limitations to maintain scientific rigor.

---

## 1. Introduction

The problem of quantifying how information persists across temporal, cultural, and material transitions has received limited formal treatment within information theory. While Shannon's (1948) mathematical theory of communication provides a rigorous foundation for analyzing signal transmission through engineered channels, its application to historical and cultural signal transmission has remained largely metaphorical. The present work argues that this relationship is not merely analogical but constitutes a formal isomorphism—a structural identity between the mathematical frameworks governing telecommunications and historical signal persistence.

The thesis advanced herein is that the persistence of any signal through a hostile transmission channel can be modeled using a three-variable multiplicative framework isomorphic to Shannon's channel capacity equation. This framework, designated the Universal Signal Persistence Framework (USPF), yields quantifiable anomaly scores that identify signals whose survival characteristics deviate significantly from category-expected baselines.

---

## 2. Theoretical Foundations: The Shannon Isomorphism

### 2.1 Shannon's Channel Capacity Theorem

Claude Shannon's (1948) fundamental theorem for a discrete channel with noise establishes the maximum rate at which information can be transmitted through a channel with arbitrarily low error probability. The channel capacity \( C \) is given by:

\[
C = B \cdot \log_2(1 + S/N)
\]

where:
- \( C \) = channel capacity (bits per second)
- \( B \) = bandwidth of the channel (Hz)
- \( S \) = average received signal power (watts)
- \( N \) = average noise power (watts)
- \( S/N \) = signal-to-noise ratio (dimensionless)

### 2.2 The USPF Isomorphism

The USPF defines signal persistence strength \( \Sigma \) as:

\[
\Sigma = S \cdot M \cdot \ln(1 + P)
\]

where:
- \( S \) = signal integrity (dimensionless, range [0,1])
- \( M \) = mechanism strength (dimensionless, range [0,1])
- \( P \) = survival pressure (dimensionless, range [0,∞))

The mapping between Shannon's formulation and the USPF is established through the following structural correspondences:

| Shannon Variable | USPF Variable | Correspondence Rationale |
|---|---|---|
| Signal power \( S \) | \( S \cdot M \) | The product of integrity and mechanism represents the effective "power" of the signal available for transmission |
| Signal-to-noise ratio \( S/N \) | \( P \) | Survival pressure functions as the noise load against which the signal must be transmitted |
| Logarithmic capacity term \( \log_2(1 + S/N) \) | \( \ln(1 + P) \) | The natural logarithm preserves the monotonic, concave relationship between noise load and capacity |

This isomorphism was identified through structural comparison of the respective mathematical formulations, revealing that both equations employ a multiplicative relationship between a signal strength term and a logarithmic noise-load term. The substitution of the natural logarithm for the base-2 logarithm is a scaling choice that preserves the functional form while accommodating the different units of analysis.

---

## 3. Variable Definitions and Operationalization

### 3.1 Signal Integrity (\( S \))

Signal integrity quantifies the proportion of the original signal that survives in usable, interpretable form. It is decomposed into three subcomponents:

- **Fidelity to original** (weight 0.50): The degree to which the received signal matches the transmitted signal
- **Fragmentation (inverted)** (weight 0.50): The complement of the proportion of the signal that has been lost or rendered discontinuous
- **Semantic stability** (weight 0.50): The extent to which the meaning of the signal remains interpretable across temporal and cultural distance

The composite integrity score is the arithmetic mean of these subcomponents, each normalized to [0,1].

### 3.2 Mechanism Strength (\( M \))

Mechanism strength captures how the signal protected and replicated itself through structural features:

- **Redundant copies** (weight 0.50): The number and distribution of independent copies of the signal
- **Independence of paths** (weight 0.50): The degree to which transmission pathways are uncorrelated
- **Reconstruction ability** (weight 0.50): The capacity to reconstruct the signal from partial or degraded copies

### 3.3 Survival Pressure (\( P \))

Survival pressure represents the total entropy load the signal has survived, operationalized as:

- **Deliberate suppression** (weight 0.20): Active attempts to destroy or censor the signal
- **Catastrophic events** (weight 0.20): Natural or human-caused disasters affecting transmission media
- **Cultural discontinuity** (weight 0.20): Ruptures in the interpretive community maintaining the signal
- **Medium transitions** (weight 0.20): Changes in the physical or technological substrate of the signal

---

## 4. Mathematical Properties of the Multiplicative Formulation

The multiplicative structure of the USPF equation is theoretically motivated rather than arbitrary. If any single dimension collapses to zero, the entire persistence score collapses to zero:

\[
\lim_{S \to 0} \Sigma = 0, \quad \lim_{M \to 0} \Sigma = 0, \quad \lim_{P \to 0} \Sigma = 0
\]

This property prevents any single variable from compensating for complete failure in another. A signal that persisted indefinitely but lost all integrity yields a zero score; a signal perfectly preserved but never subjected to any survival pressure also yields a zero score. This reflects the theoretical position that persistence requires simultaneous satisfaction of all three conditions: integrity without mechanism is fragile, mechanism without integrity is empty, and pressure without either is irrelevant.

---

## 5. Anomaly Scoring and Normalization

### 5.1 Category-Locked Baseline Computation

Raw persistence scores are converted to Z-scores against a category-locked baseline. For a given signal category \( k \), the Z-score is:

\[
Z_{i,k} = \frac{\Sigma_{i,k} - \mu_k}{\sigma_k}
\]

where:
- \( \Sigma_{i,k} \) = raw persistence score for signal \( i \) in category \( k \)
- \( \mu_k \) = mean persistence score for all signals in category \( k \)
- \( \sigma_k \) = standard deviation of persistence scores for category \( k \)

Baselines are computed from the existing registry prior to the entry of any new signal, preventing the comparison class from being tailored to favor a predetermined result.

### 5.2 Anomaly Classification Thresholds

| Classification | Z-Score Range |
|---|---|
| Extreme Anomaly | \( Z > 4.0\sigma \) |
| Highly Anomalous | \( 2.5\sigma < Z \leq 4.0\sigma \) |
| Notable | \( 1.5\sigma < Z \leq 2.5\sigma \) |
| Normal | \( -1.5\sigma \leq Z \leq 1.5\sigma \) |
| Rapid Decay | \( Z < -1.5\sigma \) |

---

## 6. Methodological Limitations and Epistemic Honesty

The USPF measures signal robustness—the capacity of a signal to survive transmission through a hostile channel. It does not directly measure truth, correspondence with reality, or normative value. Persistence is not proof of veridicality; a signal may persist because it is true, because it is useful, because it is institutionally enforced, or because it is structurally resistant to degradation for reasons unrelated to its truth content.

The framework identifies structurally non-arbitrary signals that demand explanation. The anomaly score constitutes the beginning of an inquiry, not its conclusion. What form that explanation takes—historical, theological, sociological, or otherwise—remains a separate investigative domain.

---

## 7. Pre-Registration and Reproducibility Requirements

To maintain scientific defensibility, all variable definitions, baseline categories, and anomaly thresholds must be locked prior to the entry of any signal of interest into the system. The registry enforces this requirement by computing baselines from existing data before any new addition is processed. This pre-registration protocol prevents post-hoc rationalization of variable weights or comparison classes.

---

## 8. Conclusion

The Universal Signal Persistence Framework provides a formally rigorous, mathematically grounded method for quantifying signal persistence across diverse domains. By establishing a direct isomorphism with Shannon's Channel Capacity Theorem, the framework extends information-theoretic analysis to historical and cross-cultural signal transmission while preserving the mathematical structure that makes Shannon's formulation powerful. The multiplicative formulation, category-locked normalization, and pre-registration requirements collectively ensure that the framework produces reproducible, falsifiable results. The anomaly scores generated by this framework identify signals whose persistence characteristics demand further explanation, without prejudging the nature of that explanation.

---

## References

Shannon, C. E. (1948). A mathematical theory of communication. *The Bell System Technical Journal*, 27(3), 379–423. https://doi.org/10.1002/j.1538-7305.1948.tb01338.x

---

*USPF v1.0 · David Lowe (POF 2828) · March 2026*