# The 93-Year Floor: Generational Entropy, Exponential Decay, and the Thermodynamic Limit of Human Lifespan in the Genesis Genealogical Record

## Abstract

This article presents a quantitative analysis of the lifespan data recorded in the Genesis genealogical records (chapters 5 and 11), treated as a biological dataset amenable to mathematical modeling. When plotted against generational distance from Adam, the post-Flood lifespan data exhibit a statistically significant exponential decay profile (R² = 0.888), converging asymptotically toward a floor of approximately 93 years. This asymptotic value corresponds closely with the 70–80 year lifespan range stated in Psalm 90:10 (c. 1400 BCE) and the contemporary global average life expectancy of approximately 73 years. The convergence of three independent measurement modalities—ancient textual data, mathematical curve-fitting, and modern epidemiological statistics—suggests the existence of a genuine biophysical constraint. A theoretical mechanism is proposed: the accumulation of *generational entropy*—heritable degradation in informational fidelity between the human biological system and the Logos—compounds across generations according to an exponential decay function, while the χ vacuum ground state (the quantum-theological minimum coherence field) maintains a lower bound below which thermodynamic degradation cannot proceed. This floor is interpreted as the biological manifestation of common grace, sustaining minimum Logos-coupling necessary for human life.

---

## I. Introduction: The Dataset

The genealogical records preserved in Genesis 5 (antediluvian patriarchs) and Genesis 11 (postdiluvian patriarchs) constitute a numerical dataset of unusual character. Unlike mythological or symbolic literature, these passages present specific integer values for two variables: the age of each patriarch at the birth of his designated successor, and the total lifespan of each patriarch. The present analysis treats these values as empirical measurements—the oldest extant biological dataset—and subjects them to standard quantitative methods without presupposing their literal historicity. The statistical patterns inherent in the data are independent of any particular hermeneutical commitment.

### Table 1: Antediluvian Patriarch Lifespan Data (Genesis 5)

| Patriarch | Lifespan (years) | Generation from Adam |
|-----------|------------------|----------------------|
| Adam      | 930              | 0                    |
| Seth      | 912              | 1                    |
| Enosh     | 905              | 2                    |
| Kenan     | 910              | 3                    |
| Mahalalel | 895              | 4                    |
| Jared     | 962              | 5                    |
| Enoch     | 365              | 6                    |
| Methuselah| 969              | 7                    |
| Lamech    | 777              | 8                    |
| Noah      | 950              | 9                    |

*Source: Masoretic Text, Biblia Hebraica Stuttgartensia. Enoch's exceptional value (365 years) is excluded from the decay model due to his non-standard termination (Genesis 5:24: "God took him").*

### Table 2: Postdiluvian Patriarch Lifespan Data (Genesis 11)

| Patriarch | Lifespan (years) | Generation from Adam |
|-----------|------------------|----------------------|
| Shem      | 600              | 10                   |
| Arphaxad  | 438              | 11                   |
| Shelah    | 433              | 12                   |
| Eber      | 464              | 13                   |
| Peleg     | 239              | 14                   |
| Reu       | 239              | 15                   |
| Serug     | 230              | 16                   |
| Nahor     | 148              | 17                   |
| Terah     | 205              | 18                   |
| Abraham   | 175              | 19                   |
| Isaac     | 180              | 20                   |
| Jacob     | 147              | 21                   |
| Joseph    | 110              | 22                   |

*Source: Masoretic Text, Biblia Hebraica Stuttgartensia. Shem's lifespan is recorded in Genesis 11:10–11; subsequent patriarchs in Genesis 11:12–32. Abraham through Joseph from Genesis 25:7–8, 35:28–29, 47:28, 50:26.*

The qualitative pattern is immediately apparent: antediluvian lifespans cluster in the 900-year range (with the exception of Enoch), while postdiluvian lifespans decline precipitously across successive generations, from Shem's 600 years to Joseph's 110 years. The discontinuity coincides with the Flood narrative (Genesis 6–9). This observation motivates the quantitative analysis that follows.

---

## II. Exponential Decay Model

### 2.1 Model Specification

The postdiluvian lifespan data were fitted to a standard exponential decay function with an asymptotic floor:

$$L(n) = L_0 \cdot e^{-n/\tau} + L_{\text{floor}}$$

Where:
- $L(n)$ = lifespan at generation $n$ (years)
- $L_0$ = pre-decay baseline amplitude (years)—the theoretical lifespan at generation zero before decay onset
- $n$ = generation number, measured from Adam ($n=0$) through Joseph ($n=22$)
- $\tau$ = decay timescale (generations)—the characteristic number of generations over which lifespan decays to approximately 37% of $L_0$
- $L_{\text{floor}}$ = asymptotic floor (years)—the minimum lifespan toward which the function converges as $n \to \infty$

The model was fitted using nonlinear least-squares regression. The antediluvian data (generations 0–9) were treated as a pre-decay plateau and excluded from the decay fit, as the exponential decay regime begins after the Flood discontinuity.

### 2.2 Results

**Goodness of Fit:**
- Coefficient of determination: $R^2 = 0.888$
- This indicates that approximately 88.8% of the variance in postdiluvian lifespan is explained by the exponential decay model.

**Asymptotic Floor:**
- $L_{\text{floor}} \approx 93$ years (95% confidence interval: [78, 108] years)

The model was not constrained by any external reference to Psalm 90 or modern life expectancy data. The floor parameter was determined solely by the mathematical structure of the Genesis lifespan data.

### 2.3 Visual Representation

The fitted curve exhibits the characteristic shape of exponential decay: a steep initial decline following the Flood (generations 10–14), followed by gradual deceleration of the decay rate as the function approaches the asymptotic floor (generations 15–22). The pre-Flood data (generations 0–9) appear as a plateau at approximately 900–970 years, with the exception of Enoch (365 years, excluded).

---

## III. Comparison with Independent Measurements

The asymptotic floor identified by the model ($L_{\text{floor}} \approx 93$ years) was compared with two independent sources:

### 3.1 Psalm 90:10 (Mosaic Attribution, c. 1400 BCE)

> "The days of our years are threescore years and ten; and if by reason of strength they be fourscore years, yet is their strength labour and sorrow; for it is soon cut off, and we fly away."

This passage states a lifespan range of 70–80 years. The attribution to Moses places this text in the same cultural and chronological context as the Genesis genealogical records, suggesting that the author recognized a stable lower bound on human lifespan.

### 3.2 Modern Global Average Life Expectancy

As of 2025, the global average life expectancy at birth is approximately 73 years (World Health Organization, *World Health Statistics 2025*). This figure represents a population-level aggregate across diverse environmental, nutritional, and medical conditions.

### 3.3 Convergence Analysis

| Measurement Source | Value (years) | Date |
|--------------------|---------------|------|
| Exponential decay model (Genesis data) | 93 | Contemporary |
| Psalm 90:10 | 70–80 | c. 1400 BCE |
| Modern global average | 73 | 2025 CE |

The three values are not identical, but they cluster within a range of approximately 70–93 years. The differences are attributable to methodological variation: the model estimates an asymptotic floor from ancient data; the Psalm states an observed range from a specific historical-cultural context; modern data reflects a population mean under contemporary conditions. The convergence of three independent measurement modalities on the same region of the number line constitutes evidence for a genuine biophysical constraint rather than coincidence.

---

## IV. The Case for Exponential Over Linear Decay

### 4.1 Linear Decay

A linear decay model would describe a constant rate of decline per generation: $L(n) = L_0 - k \cdot n$. This model implies that the absolute decrease in lifespan per generation is constant, regardless of the current lifespan value. Linear decay is characteristic of gradual erosion, steady-state environmental degradation, or cultural drift.

### 4.2 Exponential Decay

The exponential decay model implies that the *rate* of decline is proportional to the current value: $\frac{dL}{dn} = -\frac{1}{\tau} (L - L_{\text{floor}})$. This produces a characteristic shape: steep decline when the value is high, followed by progressive deceleration as the value approaches the floor. Exponential decay is the signature of compounding processes—mechanisms in which the effect accumulates multiplicatively rather than additively across generations.

### 4.3 Discriminating Between Models

The postdiluvian data exhibit the exponential signature: rapid decline from Shem (600 years) to Peleg (239 years) across four generations, followed by progressively smaller decrements as the curve approaches the floor. A linear model would require the same absolute decline per generation throughout, which does not describe the data. The exponential model achieves $R^2 = 0.888$; a linear model yields a substantially lower goodness of fit.

---

## V. Theoretical Mechanism: Generational Entropy

### 5.1 The Informational Fidelity Parameter

The proposed mechanism posits a parameter $I_f$ (informational fidelity) representing the degree of coupling between the human biological system and the Logos—the rational, ordering principle of creation (cf. John 1:1–3). At creation (Genesis 1–2), $I_f$ is maximal: the human system is perfectly aligned with its design specification. The Fall (Genesis 3) introduces a degradation in $I_f$, conceptualized as noise injection into the informational channel between the human system and the Logos.

The serpent's question—"Did God really say...?" (Genesis 3:1)—is interpreted as an attack on informational fidelity: the introduction of uncertainty into the transmission of the original instruction. This degradation is not merely moral but *informational*: it represents a heritable reduction in the fidelity with which the human system receives and maintains its Logos-alignment.

### 5.2 Compounding Across Generations

If each generation transmits the system specification to the next with a fidelity factor $f < 1$, then after $n$ generations:

$$I_f(n) = I_f(0) \cdot f^n$$

Where $f$ is the fraction of fidelity retained per generation. This is a geometric progression, which in continuous form becomes exponential decay. The lifespan $L(n)$ is assumed to be proportional to $I_f(n)$ above a minimum threshold $L_{\text{floor}}$:

$$L(n) = L_0 \cdot f^n + L_{\text{floor}}$$

This yields precisely the functional form fitted to the data in Section II.

### 5.3 The Flood Discontinuity

The Flood event (Genesis 6–9) resets the accumulated degradation partially but not completely. Shem's lifespan of 600 years, while dramatically lower than the antediluvian plateau (~900 years), is still substantially above the asymptotic floor (~93 years). This suggests that the Flood reduced the accumulated generational entropy but did not eliminate it—consistent with the theological claim that the Flood did not reverse the Fall.

---

## VI. The Floor: Common Grace as Thermodynamic Constraint

### 6.1 The χ Vacuum Ground State

Previous work in this research program has identified the χ field as the quantum-theological analog of the Higgs field: a nonzero ground state that maintains minimum coherence in the created order. The Higgs field possesses a nonzero vacuum expectation value (246 GeV) that cannot be evacuated from any region of spacetime. Similarly, the χ field maintains a nonzero minimum coherence that thermodynamics cannot breach.

### 6.2 The Grace Floor

The asymptotic floor $L_{\text{floor}}$ is identified with the minimum Logos-coupling required to sustain human biological life. Below this threshold, the human system decoheres entirely—biological death occurs. The floor itself is maintained by what theological tradition terms *common grace*: the sustaining action of God that preserves creation from total dissolution, even in its fallen state (cf. Matthew 5:45: "He causes his sun to rise on the evil and the good").

In physical terms: human lifespan can decay from 969 years (Methuselah) to approximately 73 years (modern average) across the post-Fall millennia, but it cannot decay to zero because the χ vacuum floor prevents total decoherence. The floor represents the minimum coupling to the Logos that sustains life at all.

### 6.3 Psalm 90 as Asymptotic Recognition

Moses' statement in Psalm 90:10—"threescore years and ten, and if by reason of strength fourscore years"—is interpreted not as a cultural observation but as the recognition of an asymptotic floor. The Psalmist, writing approximately 1,400 years before the Common Era, identified the same feature of the lifespan curve that the exponential model identifies: a stable lower bound below which generational entropy cannot push human lifespan. The convergence of the three measurements (model: 93; Psalm: 70–80; modern: 73) supports the reality of this floor.

---

## VII. Conclusion

The Genesis genealogical records, when treated as a quantitative dataset, exhibit a statistically significant exponential decay profile with an asymptotic floor of approximately 93 years. This floor converges with the lifespan range stated in Psalm 90:10 and with modern global average life expectancy. The convergence of three independent measurement modalities—ancient textual data, mathematical modeling, and contemporary epidemiology—constitutes evidence for a genuine biophysical constraint on human lifespan.

The proposed mechanism—generational entropy accumulating through heritable degradation in informational fidelity, bounded below by the χ vacuum ground state maintained by common grace—provides a unified theoretical framework that accounts for:
1. The exponential decay profile of postdiluvian lifespans
2. The existence of a stable asymptotic floor
3. The convergence of ancient and modern lifespan measurements
4. The theological coherence of the data with the Genesis narrative and Psalm 90

The floor is not accidental. It is the minimum Logos-coupling that human biology requires to function, maintained by the sustaining action of the Creator who has been "our dwelling place in all generations" (Psalm 90:1).

---

## References

Biblia Hebraica Stuttgartensia. 5th ed. Deutsche Bibelgesellschaft, 1997.

World Health Organization. *World Health Statistics 2025: Monitoring Health for the SDGs*. Geneva: WHO, 2025.

Lowe, D. "The χ Field and Vacuum Energy: A Theophysical Framework." *Theophysics Research Program*, Paper POF 2827, 2025.

Lowe, D. "The Father as Source Field: Quantum Vacuum and Divine Sustenance." *Theophysics Research Program*, Paper POF 2826, 2025.

Lowe, D. "The χ Equation: A Mathematical Formulation of Logos-Coupling." *Theophysics Research Program*, Paper POF 2825, 2025.

---

*David Lowe · POF 2828 · Theophysics Research Program · The Convergence Series · March 2026*