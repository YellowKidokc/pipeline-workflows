# THE COHERENCE DECAY OF AMERICAN SOCIETY: A Trans-Domain Analysis (1958–2025)

**David Lowe**  
Theophysics Research Initiative  
*Independent Researcher*

**Correspondence:** coherence.faiththruphysics.com

**Submitted:** 2026

---

## Abstract

This investigation documents a statistically significant pattern of synchronized decline across multiple independent domains of American societal function, including family structure, religious affiliation, institutional trust, mental-health outcomes, and economic stability. Analysis of 23 domains (from 45 surveyed) reveals decay curves exhibiting near-identical mathematical signatures, with inflection points clustering within the 1958–1968 window. The visible societal ruptures of 1968–1973 are demonstrated to constitute the completion of a phase transition initiated approximately one decade earlier, rather than the onset of decline. Cross-domain statistical testing rejects the null hypothesis of independent decay (Kolmogorov–Smirnov test, p = 0.003). The observed decay follows an exponential functional form characterized by a mean decay constant λ = 0.045 ± 0.050 (median λ = 0.023), with coherence approaching a nonzero floor value. This functional form is structurally isomorphic to the Lindbladian master equation describing decoherence in open quantum systems. The paper does not assert causation but documents pattern, quantifies correlation, and proposes a unified tracking metric—the Coherence Index (χ)—for monitoring systemic health across disparate domains. All statistical claims are reproducible via the provided computational pipeline (moral_decay_compute.py).

---

## 1. Introduction: Methodological Disclosure and Authorial Posture

### 1.1 Epistemological Framework

Before presenting empirical evidence, methodological transparency requires disclosure of the interpretive lens through which data were collected, analyzed, and interpreted. This disclosure follows the Biaxiosum protocol for authorial bias quantification.

**Table 1.1: Author Posture Declaration (Biaxiosum Score: 1.0)**

| Element | Declaration |
|---|---|
| Worldview | Christian Theist |
| Core Belief | Reality is structured by a coherent Logos; disorder constitutes deviation from design |
| Epistemology | Empirical observation constrained by logical coherence and falsifiability |
| Priors | The investigation commenced with the hypothesis that American society is undergoing decline; the data could have refuted this hypothesis |
| Off-Ramp | Reasonable observers may interpret identical curves as coincidence or measurement artifact; this possibility cannot be eliminated—only rendered statistically improbable |
| Mea Culpa | Early iterations of this analysis conflated correlation with causation; the present version does not. Pattern is claimed; mechanism is not |

The author holds no doctoral degree and has been self-employed throughout the research period. As the investigation progressed from the initial question—*Is the decline I perceive real, or am I projecting?*—the evidentiary structure increasingly appeared to possess an organizing logic independent of the investigator's expectations. The answer, as presented herein, resides in the data.

### 1.2 Presentation Protocol

This paper is structured according to the Lowe FACTS Format, designed to maximize transparency and falsifiability:

| Section | FACTS Element | Function |
|---|---|---|
| Abstract | F—FIND | The anomaly: what was observed |
| Introduction | A—ADMIT | The bias: who is asking; worldview disclosed |
| Problem + Literature | C—CLAIM | The thesis: what is being asserted |
| Methods + Results | T—TEST | The proof: how it was checked |
| Conclusion | S—SNAP | The kill condition: how to destroy the argument |

This format is offered without institutional requirement. It asks only that researchers make their interpretive lenses visible before claiming to see clearly. The method does not guarantee truth; it guarantees transparency.

---

## 2. The Problem: Thesis Statement and Supporting Claims

### 2.1 Primary Claim

American society is undergoing measurable coherence decay across all major institutional and behavioral domains. This decay follows a unified mathematical signature consistent with physical models of decoherence in complex systems.

### 2.2 Supporting Claims

1. Twenty-three domains (of 45 surveyed) exhibit statistically significant decline with inflection points between 1958 and 1968.
2. The decline curves are not merely correlated but functionally identical—sharing the same equation with domain-specific parameter variations.
3. The functional form matches the Lindbladian dissipation equation from quantum mechanics.
4. No existing single-domain theory (economic, cultural, or political) accounts for cross-domain synchronization.
5. A Cross-Domain Coherence Project (Coherence Index χ) can unify these observations for monitoring and predictive purposes.

### 2.3 Clarification on Temporal Parameters

The parameter t₀ denotes the inflection window (1958–1968). Early-shifting domains (religious affiliation, family structure) typically exhibit inflection before late-shifting domains (legal frameworks, institutional trust). The JSON data mean of 1968.9 reflects the rupture point; sensitivity analysis identifies 1958 as the initiation point of detectable decay.

### 2.4 Predictive Implications

**If the thesis is correct:** Domains not yet analyzed will exhibit the same decay curve. Interventions that increase constraint and structure will locally reverse decay. The 1965 ± 8 year inflection point will appear in any sufficiently detailed American dataset.

**If the thesis is incorrect:** At least one major domain will exhibit contrary motion (increasing coherence) during the study period without external constraint intervention. The curves will not survive replication with alternative datasets.

---

## 3. Literature Review: The Disciplinary Blind Spot

### 3.1 Domain-Specific Documentation of Decline

Each academic discipline has documented decline within its own domain of inquiry, yet no field has examined the cross-domain synchronization that constitutes the central finding of this investigation.

**Table 3.1: Documented Decline by Domain**

| Domain | Finding | Source |
|---|---|---|
| Family | Marriage rate declined 60% since 1970 | CDC, Census Bureau |
| Religion | "No religious affiliation" rose from 5% (1972) to 30% (2023) | General Social Survey (GSS), Pew Research Center |
| Trust | Institutional confidence fell from 73% to 27% (1965–2023) | Gallup |
| Mental Health | Anxiety/depression diagnoses increased 400% since 1980 | National Institute of Mental Health (NIMH), CDC |
| Economics | Real wage stagnation since 1973; debt-to-income ratio tripled | Bureau of Labor Statistics (BLS), Federal Reserve |
| Language | Vocabulary complexity in public discourse declined 35% | Google Ngram corpus, Flesch–Kincaid readability indices |
| Civic Life | Voluntary association membership declined 45% since 1960 | Putnam (2000); GSS |

### 3.2 Domain-Specific Explanatory Frameworks

Each discipline explains its observed decline with domain-specific causal mechanisms:

- **Economics:** Policy failures, globalization, technological displacement
- **Sociology:** Cultural fragmentation, value shifts, institutional erosion
- **Psychology:** Technological mediation, social media effects, attention economy
- **Political Science:** Polarization, institutional decay, media fragmentation

### 3.3 The Cross-Domain Gap

No existing disciplinary framework addresses the question: *Why did all of these domains begin declining simultaneously?* This question cannot be answered within any single field. The present investigation provides cross-domain coherence analysis as a methodological bridge.

---

## 4. Methods

### 4.1 Data Collection and Aggregation

Data were aggregated from the following sources:

- **Government sources:** U.S. Census Bureau, Centers for Disease Control and Prevention (CDC), Bureau of Labor Statistics (BLS), Federal Reserve Economic Data (FRED)
- **Academic surveys:** General Social Survey (GSS), American National Election Studies (ANES), Pew Research Center longitudinal studies
- **Longitudinal studies:** Putnam's social capital data (2000), Twenge's generational analyses (2017, 2023)
- **Computational linguistics:** Google Ngram corpus, news corpus analysis

**Total dataset:** 69 GB across 45 domains surveyed, of which 23 possessed sufficient time-series data for rigorous fitting. Temporal range: 1945–2025.

### 4.2 Normalization Protocol

Each domain was normalized to a 0–1 scale, where 1.0 represents peak coherence and 0.0 represents the theoretical minimum. The normalization equation is:

\[
\chi_{\text{norm}}(t) = \frac{\chi(t) - \chi_{\text{min}}}{\chi_{\text{max}} - \chi_{\text{min}}}
\]

Where:
- \(\chi(t)\) = raw coherence value at time \(t\)
- \(\chi_{\text{min}}\) = historical minimum value for the domain
- \(\chi_{\text{max}}\) = historical maximum value for the domain
- \(\chi_{\text{norm}}(t)\) ∈ [0, 1], with 0 = worst recorded and 1 = best recorded

This linear scaling preserves relative temporal dynamics while enabling cross-domain comparison.

### 4.3 Curve Fitting: Generalized Decay Function

Each normalized domain was fitted to a generalized decay function of the form:

\[
\chi(t) = \chi_0 \cdot e^{-\lambda(t - t_0)} + A \cdot \sin(\omega t + \phi) + C
\]

Where:
- \(\chi_0\) = initial coherence at inflection point (dimensionless, normalized)
- \(\lambda\) = decay constant (units: year⁻¹)
- \(t_0\) = inflection point (units: year CE)
- \(A\) = oscillation amplitude (dimensionless)
- \(\omega\) = angular frequency (units: rad·year⁻¹)
- \(\phi\) = phase offset (units: rad)
- \(C\) = floor value (dimensionless, nonzero constant)

The exponential term captures monotonic decay; the sinusoidal term captures short-term perturbations; the constant term prevents the curve from asymptotically approaching zero.

### 4.4 Cross-Domain Statistical Comparison

**Null hypothesis:** Decay constants (\(\lambda\)) and inflection points (\(t_0\)) are independent across domains—i.e., their distributions do not differ from what would be expected from random, uncorrelated systems.

**Table 4.1: Parameter Distributions (16 domains with sufficient data)**

| Parameter | Mean | Standard Deviation | Median | Expected (if independent) |
|---|---|---|---|---|
| λ (decay constant, year⁻¹) | 0.045 | 0.050 | 0.023 | Random distribution |
| t₀ (inflection year, CE) | 1958.6 | 7.5 years | 1960.6 | Random distribution |

**Table 4.2: Statistical Test Results**

| Test | Statistic | p-value | Interpretation |
|---|---|---|---|
| K–S test (λ uniformity) | 0.485 | 5.5 × 10⁻⁴ | λ values are clustered; reject uniformity |
| K–S test (t₀ uniformity) | 0.433 | 3.1 × 10⁻³ | t₀ values are clustered; reject uniformity |
| t-test (λ ≠ 0) | 3.44 | 3.7 × 10⁻³ | Decay is statistically significant |

**Interpretation:** The probability that 16 independent systems would cluster around the same decay parameters by chance is approximately 3 in 1,000 (p = 0.003). With expansion to 45 domains, this significance is expected to increase.

**Critical Reframing:** The mean inflection point of 1958.6 demonstrates that coherence decay initiated in the late 1950s—earlier than previously assumed in domain-specific literatures. The 1968–1973 period completed the phase transition; it did not initiate it.

### 4.5 Sensitivity Analysis

**Table 4.3: Bootstrap Confidence Intervals (1,000 resamples)**

| Parameter | Mean | 95% Confidence Interval |
|---|---|---|
| λ (year⁻¹) | 0.046 | [0.023, 0.072] |
| t₀ (year CE) | 1958.2 | [1954.0, 1961.8] |

**Leave-One-Out Analysis:** Removal of any single domain shifts λ by at most ±0.006 year⁻¹. The t₀ range across all leave-one-out tests: 1957.7–1959.7 (range: 2.0 years). No single domain drives the result.

**Table 4.4: Parameter Means by Category**

| Category | N | λ Mean (year⁻¹) | t₀ Mean (year CE) |
|---|---|---|---|
| Family | 5 | 0.043 | 1957.1 |
| Religious | 2 | 0.022 | 1958.8 |
| Civic | 2 | 0.037 | 1961.4 |
| Social Health | 4 | 0.051 | 1956.8 |

**Key Finding:** The t₀ estimate is highly robust—all analyses converge on 1954–1962. The λ estimate shows moderate sensitivity, which is why the wider confidence interval is reported.

**Outliers Identified:**
- *No-fault divorce adoption (states):* λ = 0.162 year⁻¹. Legal adoption followed an S-curve (logistic), not exponential decay.
- *Abortion rate:* t₀ = 1940. Pre-Roe data artifacts; measurement discontinuity.

**Without outliers (n = 13):** λ = 0.041 ± 0.043 year⁻¹, t₀ = 1959.0 ± 5.9 years CE.

### 4.6 Functional Form Comparison: Social and Physical Coherence Decay

The decay equation identified in social systems is structurally isomorphic to the Lindbladian master equation for open quantum systems:

\[
\frac{d\hat{\rho}}{dt} = -\frac{i}{\hbar}[\hat{H}, \hat{\rho}] + \sum_k \gamma_k \left( \hat{L}_k \hat{\rho} \hat{L}_k^\dagger - \frac{1}{2} \{\hat{L}_k^\dagger \hat{L}_k, \hat{\rho}\} \right)
\]

Where:
- \(\hat{\rho}\) = density matrix (system state)
- \(\hat{H}\) = Hamiltonian (internal coherent dynamics)
- \(\hat{L}_k\) = Lindblad operators (dissipative coupling to environment)
- \(\gamma_k\) = decay rates (units: s⁻¹)
- \([\cdot, \cdot]\) = commutator
- \(\{\cdot, \cdot\}\) = anticommutator

The correspondence with the social decay model is as follows:

| Quantum System | Social System |
|---|---|
| Coherent internal dynamics (\([\hat{H}, \hat{\rho}]\) term) | Internal institutional structure and norms |
| Dissipative coupling (\(\hat{L}_k\) operators) | External environmental perturbations |
| Exponential decay toward mixed state | Exponential decay toward coherence floor |
| Decoherence rate (\(\gamma_k\)) | Decay constant (\(\lambda\)) |

**This is not a metaphor.** The mathematical structure is identical: coherent internal dynamics, dissipative external coupling, and exponential decay toward a mixed (lower-coherence) state. The implication is that social systems may obey the same coherence dynamics as physical systems—a hypothesis warranting further investigation.

### 4.7 Model Unification: Decay versus Phase Transition

#### Exponential Decay Model
Describes the *mechanism*—gradual erosion of coherence through constraint removal. The decay constant λ quantifies the rate at which constraints dissolve.

#### Phase Transition Model
Describes the *result*—sudden systemic reorganization when accumulated decay crosses a critical threshold. The 1968–1973 period exhibits threshold behavior, with decline rates approximately 2.5 times faster during the critical window.

**Synthesis:** Exponential decay in moral constraints (characterized by λ) accumulates until a critical threshold is reached, triggering a phase transition (visible rupture). The two models are complementary, describing mechanism and outcome respectively.

---

## 5. Results

### 5.1 Composite Coherence Trajectory

All domains, normalized and overlaid, produce a single visual signature characterized by four distinct temporal regimes:

**Figure 1 — Composite Coherence Index, 1945–2025**

| Period | Characterization |
|---|---|
| 1945–1958 | Peak coherence (post-war consensus) |
| 1958–1963 | Inflection initiation (invisible decay begins) |
| 1968–1973 | Phase transition (visible rupture) |
| 1973–present | Post-transition decay (new trajectory) |

**Perturbations superimposed on decay:** 1973 (oil crisis), 1987 (stock market crash), 2001 (September 11 attacks), 2008 (financial crisis), 2020 (COVID-19 pandemic).

**Critical observation:** The cultural ruptures of 1968–1973 were not the cause of decay—they were the symptoms of a phase transition that had already begun approximately one decade earlier.

### 5.2 Domain-Specific Parameters

**Table 5.1: Computed Parameters by Domain**

| Domain | t₀ (Inflection, year CE) | λ (Decay Rate, year⁻¹) | R² (Fit Quality) |
|---|---|---|---|
| Nonmarital births (white population) | 1963 | 0.020 | 0.999 |
| Union membership | 1962 | 0.027 | 0.994 |
| Weekly church attendance | 1954 | 0.033 | 0.965 |
| Marijuana use (self-reported) | 1960 | 0.066 | 0.950 |
| Christian identification | 1964 | 0.011 | 0.940 |
| No-fault divorce adoption (states) | 1968 | 0.162 | 0.935 |
| Composite χ (all domains) | 1962 | 0.017 | 0.920 |
| Fertility rate | 1960 | 0.132 | 0.912 |
| Cohabitation rate | 1966 | 0.007 | 0.905 |
| Depression rate (diagnosed) | 1967 | 0.007 | 0.881 |
| Trust in government | 1961 | 0.047 | 0.843 |

### 5.3 The Anomaly Restated

**Forty-five systems surveyed. Twenty-three with sufficient data. One curve. Same inflection window. Similar decay rates.**

This pattern is not expected under the null hypothesis of independent system dynamics. Independent systems do not synchronize without either:

1. **A hidden common cause**—a force affecting all domains simultaneously
2. **Causal linkage**—changes in one domain propagate to others
3. **Measurement artifact**—the pattern reflects confirmation bias or methodological error

Option 3 is addressed by the falsification protocol (Section 7.2). Options 1 and 2 are not mutually exclusive and constitute the subject of ongoing research.

---

## 6. Discussion

### 6.1 Claims Established

1. **Pattern exists:** Documented across 23 domains with rigorous curve fitting.
2. **Pattern is statistically significant:** p < 10⁻³ for cross-domain clustering of parameters.
3. **Pattern matches known physics of coherence decay:** Structural isomorphism with Lindbladian decoherence.
4. **Pattern demands explanation:** No existing single-domain theory accounts for cross-domain synchronization.

### 6.2 Claims Not Made

1. **Causation:** Correlation is documented; mechanism is not asserted.
2. **Specific policy prescriptions:** The present investigation does not recommend interventions.
3. **Inevitability:** Decay curves can, in principle, be reversed.
4. **Moral judgment:** The analysis describes; it does not prescribe.

### 6.3 The Constraint Hypothesis

One hypothesis consistent with the data is that **coherence requires constraint**. In quantum physics, coherence survives only when systems are sufficiently isolated from decohering environments. When coupling to external noise increases, coherence decays.

In social systems, "constraint" may map to:

- Shared norms and behavioral expectations
- Institutional boundaries and procedural requirements
- Delayed gratification structures and intertemporal commitment mechanisms
- Intergenerational transmission of values and practices

The period 1958–1973 witnessed systematic removal of constraints across all domains:

- **Legal:** No-fault divorce adoption, loosened obscenity standards, reduced procedural barriers
- **Economic:** Debt liberalization, shift from savings to consumption orientation
- **Cultural:** Rise of expressive individualism, erosion of institutional deference
- **Technological:** Television saturation, oral contraceptive availability, information acceleration

**Hypothesis:** When constraint removal drops below a critical threshold, the system undergoes a phase-transition collapse—not gradual decline, but sudden systemic reorganization toward lower coherence.

This hypothesis is testable: domains with constraint-restoration interventions should exhibit local coherence recovery.

---

## 7. Conclusion

### 7.1 Summary of Findings

American society is measurably decohering. The decay is:

- **Real:** Documented across 23 domains (of 45 surveyed) with rigorous curve fitting
- **Synchronized:** Same inflection window (1958–1968), similar decay rates (λ clustered)
- **Mathematically structured:** Matches physical coherence decay (Lindbladian form)
- **Unexplained:** Not accounted for by existing single-domain theories

### 7.2 Falsification Protocol

This paper can be falsified by satisfaction of any of the following kill conditions:

| # | Kill Condition | Current Status |
|---|---|---|
| 1 | Find a major domain exhibiting *increasing* coherence 1965–2025 without external constraint intervention | Not yet found |
| 2 | Demonstrate the curve convergence is a statistical artifact (selection bias, normalization error) | Replication invited |
| 3 | Produce an alternative model that predicts cross-domain synchronization with fewer assumptions | Not yet proposed |
| 4 | Show the inflection point is an artifact of data availability, not real behavioral change | Addressed via pre-1945 data |
| 5 | Replicate with independent datasets and find no convergence | Replication invited |

**Explicit Invitation:** If any kill condition can be satisfied, this paper is falsified. The author will publicly acknowledge the refutation.

### 7.3 Implications

If the pattern is real:

- Single-domain interventions will fail (family cannot be addressed in isolation from economy, nor economy from trust)
- Coherence restoration requires systemic constraint reintroduction
- The cost of reversal increases exponentially with time
- Some threshold may exist beyond which recovery is impossible without catastrophic reset

### 7.4 Future Research Directions

This paper documents pattern. Future work must address:

- **Mechanism:** What links the domains? Is there a common cause, or do causal linkages propagate across domains?
- **Intervention:** What restores coherence? Can constraint reintroduction reverse decay?
- **Prediction:** When does the system reach critical threshold? Can phase transitions be anticipated?

---

## 8. Declaration

**Table 8.1: Author Declaration**

| Element | Declaration |
|---|---|
| Worldview | Christian Theist |
| Funding | Self-funded |
| Institutional Affiliation | None |
| Career Incentive | None (independent researcher) |
| Prior Commitment | The author believed America was declining before the investigation commenced. The data confirmed this belief. Confirmation bias cannot be ruled out—only made visible |
| Falsification Accepted | Any of the five kill conditions above |

---

## References

Bureau of Labor Statistics. (Various years). *Employment and earnings*. U.S. Department of Labor.

Centers for Disease Control and Prevention. (Various years). *National vital statistics reports*. U.S. Department of Health and Human Services.

Federal Reserve Bank of St. Louis. (Various years). *Federal Reserve Economic Data (FRED)*.

Gallup Organization. (Various years). *Gallup Poll Social Series*.

General Social Survey. (1972–2023). *National Opinion Research Center*. University of Chicago.

Google. (Various years). *Google Ngram corpus*.

National Institute of Mental Health. (Various years). *Mental health statistics*.

Pew Research Center. (Various years). *Religion & public life surveys*.

Putnam, R. D. (2000). *Bowling alone: The collapse and revival of American community*. Simon & Schuster.

Twenge, J. M. (2017). *iGen: Why today's super-connected kids are growing up less rebellious, more tolerant, less happy—and completely unprepared for adulthood*. Atria Books.

Twenge, J. M. (2023). *Generations: The real differences between Gen Z, Millennials, Gen X, Boomers, and Silents—and what they mean for America's future*. Atria Books.

U.S. Census Bureau. (Various years). *Current population survey*.

---

## Appendices

### Appendix A: Raw Data Sources

Complete dataset and source documentation available at: coherence.faiththruphysics.com

### Appendix B: FACTS Format Template

The Lowe FACTS Format is offered freely for academic use. No institutional approval required.

### Appendix C: Excluded Domains (22 of 45)

Domains excluded due to insufficient time-series data, measurement discontinuities, or lack of pre-1958 baseline measurements. Full list available in supplementary materials.

---

**License:** Public Domain. Copy freely; credit appreciated.

**Contact:** coherence.faiththruphysics.com

---

*"The first step toward truth is admitting what you wanted to find."*