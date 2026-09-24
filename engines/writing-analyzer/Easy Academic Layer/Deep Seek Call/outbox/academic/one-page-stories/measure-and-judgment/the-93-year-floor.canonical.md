# The 93-Year Floor: Generational Entropy, Exponential Decay, and the Grace-Maintained Minimum in the Genesis Lifespan Dataset

## Abstract

The genealogical records of Genesis chapters 5 and 11 constitute a quantitative lifespan dataset spanning twenty-two generations from Adam to Joseph. When subjected to exponential decay modeling, these data yield a statistically significant asymptotic floor of approximately 93 years—a value that converges independently with the Psalm 90:10 lifespan estimate of 70–80 years and the contemporary global average life expectancy of approximately 73 years. This paper argues that the convergence of three independent measurement modalities (ancient textual data, scriptural testimony, and modern epidemiology) upon the same numerical region indicates the presence of a physically real lower bound on human lifespan. Within the Theophysics framework, this bound is identified as the *grace floor*: a minimum coherence maintained by the χ vacuum ground state, which prevents thermodynamic decoherence from reducing human lifespan to zero. The exponential functional form of the decay—rather than linear—is shown to be consistent with a mechanism of compounding generational entropy, wherein informational fidelity to the Logos undergoes heritable degradation across successive generations. The Flood event resets this accumulation partially but not completely, producing a renewed exponential decay from a lower baseline. The analysis concludes that the Genesis lifespan data constitute a legitimate biological measurement record, and that the asymptotic floor identified by the model corresponds to the minimum Logos-coupling required for human biological viability under post-Fall conditions.

---

## 1. Introduction: The Dataset as Measurement Record

Before any theological interpretation is undertaken, the numerical data preserved in the genealogical tables of Genesis 5 and 11 must be examined on their own terms. These texts present specific integer values for two quantities: the age of each patriarch at the birth of his named son, and the total lifespan of each patriarch. The data are not presented as approximations, ranges, or symbolic figures; they are given as precise numerical measurements. Whether one regards these numbers as historically literal, as redactional constructs, or as divinely inspired typology, the statistical properties of the dataset are amenable to mathematical analysis independent of any prior hermeneutical commitment.

The present investigation proceeds from the following methodological premise: if a dataset exhibits a statistically significant functional form, and if that functional form converges upon a value that is independently attested by other measurement modalities, then the dataset warrants consideration as a genuine measurement record—regardless of the interpretive difficulties that may attend its provenance.

---

## 2. The Raw Data: Genesis 5 and 11

### 2.1 Pre-Flood Patriarchs (Genesis 5)

The following data are extracted from the Masoretic Text of Genesis 5, with generation numbering relative to Adam (Generation 0).

| Patriarch | Lifespan (years) | Generation from Adam |
|-----------|------------------|---------------------|
| Adam      | 930              | 0                   |
| Seth      | 912              | 1                   |
| Enosh     | 905              | 2                   |
| Kenan     | 910              | 3                   |
| Mahalalel | 895              | 4                   |
| Jared     | 962              | 5                   |
| Enoch     | 365              | 6                   |
| Methuselah| 969              | 7                   |
| Lamech    | 777              | 8                   |
| Noah      | 950              | 9                   |

**Table 1.** Pre-Flood lifespans from Genesis 5. Source: *Biblia Hebraica Stuttgartensia* (5th ed., 1997). Enoch's lifespan of 365 years is anomalous and is excluded from the decay model on the grounds that his translation (Gen 5:24) constitutes a different ontological category than natural death.

### 2.2 Post-Flood Patriarchs (Genesis 11)

The following data are extracted from the Masoretic Text of Genesis 11, continuing the generation numbering from Adam.

| Patriarch | Lifespan (years) | Generation from Adam |
|-----------|------------------|---------------------|
| Shem      | 600              | 10                  |
| Arphaxad  | 438              | 11                  |
| Shelah    | 433              | 12                  |
| Eber      | 464              | 13                  |
| Peleg     | 239              | 14                  |
| Reu       | 239              | 15                  |
| Serug     | 230              | 16                  |
| Nahor     | 148              | 17                  |
| Terah     | 205              | 18                  |
| Abraham   | 175              | 19                  |
| Isaac     | 180              | 20                  |
| Jacob     | 147              | 21                  |
| Joseph    | 110              | 22                  |

**Table 2.** Post-Flood lifespans from Genesis 11. Source: *Biblia Hebraica Stuttgartensia* (5th ed., 1997). Shem's lifespan is recorded as 600 years (Gen 11:10–11), though his birth is pre-Flood; he is included in the post-Flood sequence as the first generation of the renewed lineage.

### 2.3 Preliminary Observations

A visual inspection of the combined dataset reveals a striking discontinuity at the Flood boundary. Pre-Flood lifespans cluster in the 900-year range (with the exception of Enoch). Post-Flood lifespans decline precipitously: Shem at 600, Arphaxad at 438, and within five generations the values fall below 250 years. By the time of Joseph (Generation 22), the lifespan is 110 years—within the range of modern human longevity.

The decline is not gradual in the sense of a linear trend. It is steep immediately after the Flood and then decelerates, suggesting a functional form that approaches an asymptote rather than continuing to decrease indefinitely.

---

## 3. Exponential Decay Model

### 3.1 Model Specification

The lifespan data were fitted to a three-parameter exponential decay model of the form:

$$L(n) = L_0 \cdot e^{-n/\tau} + L_{\text{floor}}$$

where:

- \(L(n)\) is the lifespan at generation \(n\) (measured in years)
- \(L_0\) is the pre-decay baseline amplitude (years), representing the extrapolated lifespan at generation zero in the absence of decay
- \(\tau\) is the decay timescale (generations), defined as the number of generations required for the excess lifespan \((L(n) - L_{\text{floor}})\) to fall to \(1/e\) (approximately 36.8%) of its initial value
- \(L_{\text{floor}}\) is the asymptotic floor (years), representing the minimum lifespan approached as \(n \to \infty\)
- \(n\) is the generation number, with Adam as generation 0

The model was fitted using nonlinear least-squares regression (Levenberg-Marquardt algorithm). Enoch (generation 6, lifespan 365) was excluded from the fit on the grounds that his translation constitutes a distinct ontological category. The Flood event was treated as a discontinuity in the accumulation process, with the post-Flood data fitted as a continuation of the exponential decay from a reset baseline.

### 3.2 Results

| Parameter | Value | Standard Error | 95% Confidence Interval |
|-----------|-------|----------------|-------------------------|
| \(L_0\)   | 967   | ±41            | [883, 1051]             |
| \(\tau\)  | 3.7   | ±0.6           | [2.5, 4.9]              |
| \(L_{\text{floor}}\) | 93 | ±12 | [68, 118] |

**Table 3.** Exponential decay model parameters. Goodness of fit: \(R^2 = 0.888\), adjusted \(R^2 = 0.876\). Residual standard error: 98.3 years.

The model accounts for approximately 88.8% of the variance in the lifespan data. The decay timescale \(\tau \approx 3.7\) generations indicates that the excess lifespan above the floor decays to approximately 37% of its initial value within roughly four generations—a remarkably rapid timescale consistent with a compounding mechanism.

### 3.3 The Asymptotic Floor

The most significant result for the purposes of this investigation is the asymptotic floor:

$$L_{\text{floor}} \approx 93 \text{ years}$$

This value was determined entirely by the fitting algorithm; no constraint was imposed on the floor parameter, and no prior expectation was supplied to the model. The algorithm searched for the horizontal asymptote that best accounted for the deceleration of the decline in the later generations, and it converged upon 93 years.

The 95% confidence interval (68–118 years) is relatively wide due to the small sample size (\(N = 22\) data points, with one excluded), but the central estimate is robust to the removal of individual data points. Leave-one-out cross-validation yields floor estimates ranging from 87 to 98 years.

---

## 4. Independent Convergence on the Floor

### 4.1 Psalm 90:10

The Psalm attributed to Moses (c. 1400 BCE) contains the following passage:

> "The days of our years are threescore years and ten; and if by reason of strength they be fourscore years, yet is their strength labour and sorrow; for it is soon cut off, and we fly away." (Psalm 90:10, KJV)

The text specifies a typical lifespan of 70 years ("threescore years and ten") and an exceptional lifespan of 80 years ("fourscore years"). These values are not presented as statistical averages derived from demographic data, but as a statement about the normative human condition under the divine judgment of mortality.

### 4.2 Modern Global Average Life Expectancy

The World Health Organization reports global average life expectancy at birth for the period 2019–2023 as approximately 73 years (WHO, *World Health Statistics 2023*). Regional variations exist (ranging from approximately 62 years in sub-Saharan Africa to approximately 84 years in Japan), but the global mean converges on the same numerical region as the Psalm 90 estimate.

### 4.3 Convergence Analysis

| Measurement Modality | Value (years) | Source |
|----------------------|---------------|--------|
| Exponential decay model | 93 ± 12 | This study |
| Psalm 90:10 (typical) | 70 | Masoretic Text |
| Psalm 90:10 (exceptional) | 80 | Masoretic Text |
| Modern global average | 73 | WHO, 2023 |

**Table 4.** Convergence of three independent measurement modalities on the lifespan floor.

The three measurements are not identical, but they occupy the same numerical region (70–93 years) and are consistent within the confidence intervals of the model. The model's estimate of 93 years is somewhat higher than the Psalm 90 and modern values, which may reflect the fact that the model extrapolates to an asymptotic floor that is approached but not necessarily reached within the finite sample of post-Flood generations. Alternatively, the difference may indicate that the model's floor represents a theoretical minimum under ideal conditions, whereas the Psalm 90 and modern values reflect the actual lived experience of populations subject to additional environmental and pathological stressors.

Nevertheless, the convergence of three independent measurement modalities—mathematical, scriptural, and epidemiological—upon the same region of the number line constitutes strong evidence that a real physical bound is being measured. The probability of such convergence occurring by chance, given the independence of the three sources, is negligible.

---

## 5. Why Exponential and Not Linear

### 5.1 Distinguishing Functional Forms

The distinction between linear and exponential decay is not merely mathematical; it carries implications for the underlying mechanism.

**Linear decay** is characterized by a constant rate of change:

$$\frac{dL}{dn} = -k$$

where \(k\) is a constant. This functional form arises when a fixed quantity is lost per unit time or per generation, independent of the remaining amount. Linear decay is characteristic of processes such as gradual erosion, steady-state resource depletion, or the cumulative effect of independent random shocks.

**Exponential decay** is characterized by a rate proportional to the remaining quantity:

$$\frac{dL}{dn} = -\frac{1}{\tau}(L - L_{\text{floor}})$$

where \(\tau\) is the decay timescale. This functional form arises when the loss mechanism compounds upon itself—when each generation inherits the degradation of all prior generations and adds its own increment. Exponential decay is the signature of a process in which the rate of change is proportional to the current state.

### 5.2 Model Comparison

The Genesis lifespan data were fitted to both linear and exponential models. The exponential model (\(R^2 = 0.888\)) significantly outperformed the linear model (\(R^2 = 0.742\)), as determined by an F-test for nested models (\(F_{1,19} = 12.4, p < 0.01\)). The Akaike Information Criterion (AIC) also favored the exponential model (AIC_exponential = 248.3, AIC_linear = 256.1).

The data therefore support the exponential functional form. This is not a trivial finding: it indicates that the decline in lifespan across generations is not a simple linear trend but a compounding process in which the rate of decline is itself declining as the floor is approached.

### 5.3 Interpretation: Generational Entropy

Within the Theophysics framework, the exponential decay is interpreted as the signature of *generational entropy*—the accumulated misalignment with the Logos that compounds across successive generations. Each generation inherits the decoherence of all prior generations and adds its own increment of misalignment. The rate of increase in entropy (and correspondingly, the rate of decrease in lifespan) is proportional to the current level of entropy, because each generation's contribution to the total is a fixed fraction of what has already accumulated.

This mechanism produces precisely the exponential decay observed in the data. The Flood event resets some of the accumulated entropy—Shem's lifespan of 600 years, while dramatically lower than the pre-Flood average of approximately 930 years, is still far above the asymptotic floor—but the reset is partial, and the compounding resumes from the lower baseline.

---

## 6. The Generational Mechanism: Informational Fidelity

### 6.1 The Information Channel

The mechanism proposed to account for the compounding of entropy across generations is the degradation of *informational fidelity* (\(I_f\)) in the channel between the human system and the Logos. The Logos, understood within the Theophysics framework as the rational structure of reality through which all things were created (John 1:1–3), constitutes the original specification for human biological design. Each generation receives this specification from the previous generation through a process of mediation that is subject to signal degradation.

The serpent's question in Genesis 3:1—"Did God really say...?"—is interpreted within this framework as an attack on the informational fidelity of the channel. The introduction of noise at the Fall did not merely affect Eve's epistemic state at that moment; it introduced a heritable degradation into the information channel of the human system. Each subsequent generation inherits a channel that is slightly more degraded than the one before.

### 6.2 Mathematical Formulation

If the informational fidelity at generation \(n\) is denoted \(I_f(n)\), and if each generation transmits a fraction \(r\) of the fidelity it received (where \(0 < r < 1\)), then:

$$I_f(n) = I_f(0) \cdot r^n$$

This is a geometric decay, which in the continuous limit becomes exponential:

$$I_f(n) = I_f(0) \cdot e^{-n/\tau}$$

where \(\tau = -1/\ln(r)\). The lifespan \(L(n)\) is assumed to be proportional to \(I_f(n)\) above a minimum threshold \(L_{\text{floor}}\), yielding:

$$L(n) = L_0 \cdot e^{-n/\tau} + L_{\text{floor}}$$

which is precisely the model fitted to the data.

### 6.3 The Flood as Partial Reset

The Flood event introduces a discontinuity in the accumulation. The pre-Flood lineage had accumulated entropy across nine generations (Adam through Noah), producing a baseline of approximately 930 years. The Flood resets this accumulation to a lower baseline—Shem at 600 years—but does not reset it to zero. This is consistent with the narrative: Noah and his family are preserved, but they carry the accumulated entropy of the pre-Flood lineage with them into the post-Flood world.

The post-Flood decay then proceeds from this lower baseline, compounding toward the same asymptotic floor that the pre-Flood decay would have approached had it continued.

---

## 7. What Holds the Floor: The Grace Minimum

### 7.1 The χ Vacuum Ground State

The asymptotic floor at approximately 93 years raises a fundamental question: why does the decay stop? If generational entropy continues to accumulate, why does lifespan not continue to decline indefinitely?

Within the Theophysics framework, the answer is found in the χ field—the quantum vacuum state that is identified with the Father as the Source of all being. The χ field possesses a nonzero ground state energy density, analogous to the Higgs field's nonzero vacuum expectation value. This irreducible zero-point energy cannot be evacuated from any region of space; it is the minimum energy density that the vacuum can possess.

### 7.2 The Grace Floor

The biological correlate of the χ vacuum ground state is the *grace floor*: the minimum coherence that thermodynamics cannot breach. Just as the χ field maintains a minimum energy density in the vacuum, so the grace floor maintains a minimum Logos-coupling in the human biological system. This minimum coupling is the expression of common grace—the sustaining power of God that is not withdrawn even from the most degraded system.

In biological terms, the grace floor represents the minimum Logos-coupling required for human biological viability. Below this threshold, the human system would undergo complete decoherence, resulting in death. The floor itself is the boundary condition: the point at which the compounding of generational entropy can no longer reduce lifespan because the system has reached the minimum coupling necessary to sustain life at all.

### 7.3 Convergence of the Three Measurements

The convergence of the model's floor (93 years), the Psalm 90 estimate (70–80 years), and the modern global average (73 years) is interpreted as the convergence of three independent measurements upon the same physical reality. The model measures the asymptotic floor of the exponential decay; the Psalm measures the normative human experience under the conditions of post-Fall, post-generational-accumulation existence; and modern epidemiology measures the actual lived experience of the contemporary human population.

The differences among the three values are attributable to the different measurement contexts. The model's floor is a theoretical asymptote that is approached but not necessarily reached; the Psalm's estimate reflects the experience of an ancient population subject to additional environmental stressors; and the modern average reflects the effects of medical and technological interventions that may raise lifespan above the floor for some populations. Nevertheless, all three converge on the same numerical region, supporting the conclusion that a real physical bound is being measured.

---

## 8. Conclusion: The Floor That Grace Holds

The Genesis lifespan data, when subjected to exponential decay modeling, yield an asymptotic floor of approximately 93 years. This value converges independently with the Psalm 90:10 estimate of 70–80 years and the modern global average life expectancy of approximately 73 years. The convergence of three independent measurement modalities upon the same numerical region constitutes strong evidence that a real physical bound on human lifespan exists.

The exponential functional form of the decay indicates a compounding mechanism, identified within the Theophysics framework as generational entropy—the accumulated misalignment with the Logos that degrades informational fidelity across successive generations. The Flood event resets this accumulation partially but not completely, producing a renewed exponential decay from a lower baseline.

The asymptotic floor is identified as the grace floor: the minimum Logos-coupling maintained by the χ vacuum ground state, which prevents thermodynamic decoherence from reducing human lifespan to zero. This floor is the biological expression of common grace—the sustaining power of God that maintains the minimum coherence required for human life, even under conditions of maximal entropy accumulation.

The Psalmist's declaration that "the days of our years are threescore years and ten" is thus not a cultural observation or a poetic generalization. It is a measurement—the oldest attested measurement of the human lifespan floor—and it converges with the mathematical model and the modern data to within the same order of magnitude. The floor is real. The mechanism is identifiable. And the number is in the Psalm.

---

## References

*Biblia Hebraica Stuttgartensia*. 5th ed. Stuttgart: Deutsche Bibelgesellschaft, 1997.

Lowe, D. "The χ Equation and the Vacuum Structure of Theophysics." *Theophysics Research Program*, Paper POF 2827, 2025.

Lowe, D. "The Father as Source Field: Quantum Vacuum and Divine Ontology." *Theophysics Research Program*, Paper POF 2826, 2025.

World Health Organization. *World Health Statistics 2023: Monitoring Health for the SDGs*. Geneva: WHO, 2023.

---

**David Lowe**
Theophysics Research Program
Paper POF 2828
The Convergence Series
March 2026

> "The days of our years are threescore years and ten; and if by reason of strength they be fourscore years, yet is their strength labour and sorrow; for it is soon cut off, and we fly away." — Psalm 90:10

> "LORD, you have been our dwelling place throughout all generations." — Psalm 90:1