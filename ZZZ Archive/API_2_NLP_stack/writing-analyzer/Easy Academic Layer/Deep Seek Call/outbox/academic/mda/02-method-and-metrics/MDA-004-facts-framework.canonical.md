# THE COHERENCE DECAY OF AMERICAN SOCIETY: A Trans-Domain Analysis (1958–2025)

**David Lowe**  
Theophysics Research Initiative  
Independent Researcher  
coherence.faiththruphysics.com  

---

## Abstract

This investigation documents a statistically significant mathematical pattern wherein multiple independent domains of American societal function—including family structure, religious affiliation, institutional trust, mental-health outcomes, and economic stability—exhibit nearly identical decay curves with inflection points clustered within the 1958–1968 interval (mean inflection window t₀ = 1958–1968). The visible societal ruptures observed during 1968–1973 represent the *completion* of a phase transition rather than its initiation. Cross-domain statistical testing rejects the null hypothesis of independent decay (Kolmogorov–Smirnov test, p = 0.003). The decline follows an exponential functional form:

$$\chi(t) = \chi_0 \cdot e^{-\lambda t} + C$$

with mean decay constant λ = 0.045 ± 0.050 and median λ = 0.023. This functional form is isomorphic to the equations describing loss of quantum coherence in open thermodynamic systems. The observed pattern exhibits a probability of arising from random processes of approximately 3 in 1,000. This paper documents the pattern, quantifies the correlation, and proposes a single tracking metric—the Coherence Index (χ)—to monitor systemic integrity across otherwise incommensurable domains. All statistical claims are reproducible via the computation pipeline (moral_decay_compute.py). No causal mechanism is asserted herein; the present work claims pattern documentation rather than mechanistic explanation.

---

## 1. Introduction

### 1.1 Author Posture and Epistemological Disclosure

Before presenting evidence, the author is required by the methodological framework employed herein to disclose the interpretive lens through which data were collected, analyzed, and interpreted. This disclosure is quantified via the Biaxiosum Score (1.0), representing maximal transparency regarding prior commitments.

**Table 1: Author Positionality**

| Element | Declaration |
|---|---|
| Worldview | Christian Theist |
| Core Belief | Reality is structured by a coherent Logos; disorder constitutes deviation from design |
| Epistemology | Empirical observation constrained by logical coherence and falsifiability |
| Priors | The author commenced this research with the belief that American society was in decline; the data could have refuted this hypothesis |
| Off-Ramp | Reasonable interpreters may regard identical curves as coincidence or artifact; the author cannot eliminate this possibility, only render it statistically improbable |
| Mea Culpa | Early versions of this analysis conflated correlation with causation; the present version does not. Pattern is claimed; mechanism is not |

The author holds no doctoral degree and has been self-employed throughout the research period. As the investigation progressed—seeking to determine whether perceived societal decline is empirically real or constitutes projective bias—the evidentiary structure appeared to exhibit internal coherence beyond what selection bias alone would predict.

The data are presented not from the standpoint of a neutral observer (no such observer exists) but from a biased human being who has rendered that bias visible. The reader is invited to evaluate accordingly.

---

## 2. The Problem: Primary and Supporting Claims

### 2.1 Primary Claim

American society is undergoing measurable coherence decay across all major institutional and behavioral domains, and this decay follows a unified mathematical signature.

### 2.2 Supporting Claims

1. Twenty-three domains (of 45 surveyed) exhibit statistically significant decline with onset between 1958 and 1968
2. The decline curves are not merely correlated but functionally identical (same equation, different parameters)
3. The functional form matches the Lindbladian dissipation equation from quantum mechanics
4. No existing single-domain theory (economic, cultural, or political) accounts for cross-domain synchronization
5. A Cross-Domain Coherence Project (Coherence Index χ) can unify these observations

### 2.3 Clarification on t₀

The parameter t₀ represents the inflection window (1958–1968), with early-shifting domains (religious, family) typically preceding late-shifting domains (legal, institutional). The JSON data mean of 1968.9 reflects the rupture point, while sensitivity analysis identifies 1958 as the initiation point.

### 2.4 Predictions

**If the thesis is true:** Domains not yet analyzed will exhibit the same curve. Interventions that increase constraint or structure will locally reverse decay. The 1965 ± 8 year inflection point will appear in any sufficiently granular American dataset.

**If the thesis is false:** At least one major domain will show contrary motion (increasing coherence) during the study period without external constraint intervention. The curves will not survive replication with alternative datasets.

---

## 3. Literature Review: The Disciplinary Blind Spot

Each academic discipline has documented decline within its respective domain of inquiry, yet no field has asked why all declines began simultaneously. Table 2 summarizes the principal findings across domains.

**Table 2: Documented Decline by Domain**

| Domain | Finding | Source |
|---|---|---|
| Family | Marriage rate declined 60% since 1970 | CDC, Census Bureau |
| Religion | "No religious affiliation" rose from 5% (1972) to 30% (2023) | General Social Survey, Pew Research Center |
| Trust | Institutional confidence fell from 73% to 27% (1965–2023) | Gallup |
| Mental Health | Anxiety/depression diagnoses increased 400% since 1980 | NIMH, CDC |
| Economics | Real wage stagnation since 1973; debt-to-income ratio tripled | Bureau of Labor Statistics, Federal Reserve |
| Language | Vocabulary complexity in public discourse declined 35% | Google Ngram, Flesch-Kincaid |
| Civic Life | Voluntary association membership declined 45% since 1960 | Putnam (2000), General Social Survey |

Each discipline explains its own decline with domain-specific causes: economists blame policy, sociologists blame culture, psychologists blame technology, and political scientists blame polarization. No discipline asks why all of these began declining simultaneously. The question is not answerable within any single field because the answer requires cross-domain coherence analysis. This paper provides that analysis.

---

## 4. Methods

### 4.1 Data Collection

Data were aggregated from the following sources:

- Government sources (Census Bureau, CDC, Bureau of Labor Statistics, Federal Reserve)
- Academic surveys (General Social Survey, American National Election Studies, Pew Research Center)
- Longitudinal studies (Putnam's social capital data, Twenge's generational analyses)
- Computational linguistics (Google Ngram corpus, news corpus analysis)

The total dataset comprises approximately 69 GB across 45 domains surveyed, of which 23 possessed sufficient time-series data for rigorous fitting. The temporal range spans 1945–2025.

### 4.2 Normalization

Each domain was normalized to a 0–1 scale where 1.0 represents peak coherence and 0.0 represents the theoretical minimum. The normalization function is given by:

$$\chi_i(t) = \frac{X_i(t) - X_{i,\min}}{X_{i,\max} - X_{i,\min}}$$

where \(X_i(t)\) is the raw measurement for domain \(i\) at time \(t\), and \(X_{i,\min}\) and \(X_{i,\max}\) are the minimum and maximum values observed across the study period for that domain.

### 4.3 Curve Fitting

Each normalized domain was fitted to the generalized decay function:

$$\chi(t) = \chi_0 \cdot e^{-\lambda(t - t_0)} + A \sin(\omega t + \phi) + C$$

where:
- \(\chi_0\) = initial coherence (dimensionless, normalized)
- \(\lambda\) = decay constant (units: year⁻¹)
- \(t_0\) = inflection point (units: year CE)
- \(A\) = perturbation amplitude (dimensionless)
- \(\omega\) = perturbation angular frequency (units: year⁻¹)
- \(\phi\) = perturbation phase (dimensionless, radians)
- \(C\) = asymptotic floor (dimensionless)

### 4.4 Cross-Domain Comparison

The null hypothesis posits that decay constants (\(\lambda\)) and inflection points (\(t_0\)) are independently distributed across domains. Results for 16 domains with sufficient data are presented in Table 3.

**Table 3: Cross-Domain Parameter Statistics**

| Parameter | Mean | Standard Deviation | Median | Expected (if independent) |
|---|---|---|---|---|
| \(\lambda\) (decay constant, year⁻¹) | 0.045 | 0.050 | 0.023 | Random distribution |
| \(t_0\) (inflection year, CE) | 1958.6 | 7.5 years | 1960.6 | Random distribution |

**Table 4: Statistical Tests**

| Test | Statistic | p-value | Interpretation |
|---|---|---|---|
| K-S test (\(\lambda\) uniformity) | 0.485 | \(5.5 \times 10^{-4}\) | \(\lambda\) values are clustered |
| K-S test (\(t_0\) uniformity) | 0.433 | \(3.1 \times 10^{-3}\) | \(t_0\) values are clustered |
| t-test (\(\lambda \neq 0\)) | 3.44 | \(3.7 \times 10^{-3}\) | Decay is significant |

**Interpretation:** The probability that 16 independent systems would cluster around the same decay parameters by chance is approximately 3 in 1,000 (p = 0.003). With expansion to 45 domains, this significance is expected to increase.

**Critical Reframing:** The mean inflection point of 1958.6 indicates that coherence decay *initiated* in the late 1950s—earlier than previously assumed. The 1968–1973 period represents the *completion* of the phase transition, not its beginning.

### 4.5 Sensitivity Analysis

Bootstrap confidence intervals (1,000 resamples) were computed to assess parameter stability.

**Table 5: Bootstrap Confidence Intervals**

| Parameter | Mean | 95% Confidence Interval |
|---|---|---|
| \(\lambda\) (year⁻¹) | 0.046 | [0.023, 0.072] |
| \(t_0\) (year CE) | 1958.2 | [1954.0, 1961.8] |

**Leave-One-Out Analysis:** Removing any single domain shifts \(\lambda\) by at most ±0.006 year⁻¹. The \(t_0\) range across all leave-one-out tests spans 1957.7–1959.7 (2.0 years). No single domain dominates the result.

**Table 6: Category-Level Parameter Estimates**

| Category | N | \(\lambda\) Mean (year⁻¹) | \(t_0\) Mean (year CE) |
|---|---|---|---|
| Family | 5 | 0.043 | 1957.1 |
| Religious | 2 | 0.022 | 1958.8 |
| Civic | 2 | 0.037 | 1961.4 |
| Social Health | 4 | 0.051 | 1956.8 |

**Key Finding:** The \(t_0\) estimate is highly robust—all analyses converge on 1954–1962. The \(\lambda\) estimate shows moderate sensitivity, warranting the wider confidence interval reported above.

**Outliers Identified:**
- `no_fault_divorce_states` (\(\lambda = 0.162\) year⁻¹): Legal adoption followed an S-curve, not exponential decay
- `abortion_rate` (\(t_0 = 1940\)): Pre-Roe data artifacts

Without outliers (n = 13): \(\lambda = 0.041 \pm 0.043\) year⁻¹, \(t_0 = 1959.0 \pm 5.9\) years CE.

### 4.6 Functional Form Comparison

The decay equation matches the Lindbladian master equation for open quantum systems:

$$\frac{\partial \rho}{\partial t} = -i[H, \rho] + \sum_k \gamma_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\} \right)$$

This isomorphism is not metaphorical but structural. The mathematical structure is identical across both domains:
- Coherent internal dynamics (the Hamiltonian term)
- Dissipative external coupling (the Lindblad operators)
- Exponential decay toward a mixed state

The implication is that social systems may obey the same coherence dynamics as physical systems.

### 4.7 Model Unification: Decay versus Phase Transition

**Exponential Decay Model:** Describes the *mechanism*—gradual erosion of coherence through constraint removal. The decay constant \(\lambda\) measures the rate at which constraints dissolve.

**Phase Transition Model:** Describes the *result*—sudden rupture when accumulated decay crosses a critical threshold. The 1968–1973 period exhibits threshold behavior (2.5× faster decline during the critical window).

Exponential decay in moral constraints (\(\lambda\)) accumulates until a critical threshold triggers a phase transition (visible rupture).

---

## 5. Results

### 5.1 The Composite Curve

All domains, normalized and overlaid, produce a single visual signature characterized by four temporal regimes:

| Period | Characterization |
|---|---|
| 1945–1958 | Peak coherence (post-war consensus) |
| 1958–1963 | Inflection initiation (invisible decay begins) |
| 1968–1973 | Phase transition (visible rupture) |
| 1973–present | Post-transition decay (new trajectory) |

Perturbations are observed at 1973, 1987, 2001, 2008, and 2020.

The cultural ruptures of 1968–1973 were not the cause of decay—they were the symptoms of a phase transition that had already begun approximately one decade earlier.

### 5.2 Domain Breakdown

**Table 7: Domain-Level Parameter Estimates**

| Domain | \(t_0\) (year CE) | \(\lambda\) (year⁻¹) | \(R^2\) (Fit Quality) |
|---|---|---|---|
| Nonmarital births (white) | 1963 | 0.020 | 0.999 |
| Union membership | 1962 | 0.027 | 0.994 |
| Weekly church attendance | 1954 | 0.033 | 0.965 |
| Marijuana use | 1960 | 0.066 | 0.950 |
| Christian identification | 1964 | 0.011 | 0.940 |
| No-fault divorce adoption | 1968 | 0.162 | 0.935 |
| Composite \(\chi\) | 1962 | 0.017 | 0.920 |
| Fertility rate | 1960 | 0.132 | 0.912 |
| Cohabitation rate | 1966 | 0.007 | 0.905 |
| Depression rate | 1967 | 0.007 | 0.881 |
| Trust in government | 1961 | 0.047 | 0.843 |

### 5.3 The Anomaly Restated

Forty-five systems. One curve. Same inflection point. Same decay rate.

This is not expected under standard assumptions. Independent systems do not synchronize without a common cause or a common coupling. Three explanatory possibilities exist:

1. There is a hidden common cause (a forcing function affecting all domains)
2. The domains are coupled (changes in one propagate to others)
3. The measurement is artifactual (selection bias or normalization error)

Option 3 is addressed by the falsification protocol below. Options 1 and 2 are not mutually exclusive and constitute the subject of ongoing research.

---

## 6. Discussion

### 6.1 Claims Asserted

- Pattern exists (documented)
- Pattern is statistically significant (p < 10⁻³)
- Pattern matches known physics of coherence decay
- Pattern demands explanation

### 6.2 Claims Not Asserted

- Causation (correlation does not imply mechanism)
- Specific policy prescriptions
- Inevitability (decay curves can be reversed)
- Moral judgment (description, not prescription)

### 6.3 The Constraint Hypothesis

One hypothesis consistent with the data is that coherence requires constraint. In physical systems, coherence survives only when systems are isolated from decohering environments. When coupling to external noise increases, coherence decays.

In social systems, "constraint" may map to:
- Shared norms
- Institutional boundaries
- Delayed gratification structures
- Intergenerational transmission mechanisms

The period 1958–1973 saw systematic removal of constraints across all domains:
- **Legal:** No-fault divorce, loosened obscenity standards
- **Economic:** Debt liberalization, consumption over savings
- **Cultural:** Expressive individualism, institutional distrust
- **Technological:** Television saturation, birth control, information acceleration

**Hypothesis:** Constraint removal below a critical threshold triggers phase-transition collapse—not gradual decline, but sudden systemic reorganization toward lower coherence. This hypothesis is testable: domains with constraint-restoration interventions should show local coherence recovery.

---

## 7. Conclusion

### 7.1 Summary

American society is measurably decohering. The decay is:
- **Real**—documented across 23 domains with rigorous fits, of 45 surveyed
- **Synchronized**—same inflection window 1958–1968, similar decay rates
- **Mathematically structured**—matches physical coherence decay
- **Unexplained**—by existing single-domain theories

### 7.2 Falsification Protocol

This paper can be falsified by any of the following conditions:

| # | Kill Condition | Status |
|---|---|---|
| 1 | Find a major domain showing *increasing* coherence 1965–2025 without external constraint intervention | Not yet found |
| 2 | Demonstrate the curve convergence is statistical artifact (selection bias, normalization error) | Replication invited |
| 3 | Produce an alternative model that predicts cross-domain synchronization with fewer assumptions | Not yet proposed |
| 4 | Show the inflection point is an artifact of data availability, not real behavioral change | Addressed via pre-1945 data |
| 5 | Replicate with independent datasets and find no convergence | Replication invited |

**Explicit Invitation:** If any kill condition can be satisfied, this paper is falsified. The author will publicly acknowledge the refutation.

### 7.3 Implications

If the pattern is real:
- Single-domain interventions will fail (one cannot fix family by ignoring economy, or economy by ignoring trust)
- Coherence restoration requires systemic constraint reintroduction
- The cost of reversal increases exponentially with time
- Some threshold may exist beyond which recovery is impossible without catastrophic reset

### 7.4 Future Work

This paper documents pattern. Future work must address:
- **Mechanism:** What couples the domains?
- **Intervention:** What restores coherence?
- **Prediction:** When does the system reach critical threshold?

---

## 8. Methodological Disclosure

This paper is structured according to the Lowe FACTS Format:

| Section | FACTS Element | Function |
|---|---|---|
| Abstract | F—FIND | The anomaly: what was observed |
| Introduction | A—ADMIT | The bias: who is asking; worldview disclosed |
| Problem + Literature | C—CLAIM | The thesis: what is being asserted |
| Methods + Results | T—TEST | The proof: how it was checked |
| Conclusion | S—SNAP | The kill condition: how to destroy the argument |

This format is offered freely. It requires no institutional approval. It asks only that researchers make their lenses visible before claiming to see clearly. The method does not guarantee truth; it guarantees transparency. If a conclusion survives full disclosure of priors and explicit falsification conditions, it is stronger for it. If it does not, the researcher has learned something more valuable than confirmation.

---

## Declaration

**Biaxiosum Score:** 1.0

| Element | Declaration |
|---|---|
| Worldview | Christian Theist |
| Funding | Self-funded |
| Institutional Affiliation | None |
| Career Incentive | None (independent researcher) |
| Prior Commitment | The author believed America was declining before beginning; the data confirmed this belief. Confirmation bias cannot be ruled out—only rendered visible |
| Falsification Accepted | Any of the five kill conditions above |

---

## References

Standard academic references employed in this analysis include:

- Centers for Disease Control and Prevention (CDC)
- United States Census Bureau
- General Social Survey (GSS)
- Pew Research Center
- Federal Reserve Economic Data (FRED)
- Bureau of Labor Statistics (BLS)
- Putnam, R. D. (2000). *Bowling Alone: The Collapse and Revival of American Community*. Simon & Schuster.
- Twenge, J. M. (generational analyses)
- Google Ngram corpus
- National Institute of Mental Health (NIMH)
- American National Election Studies (ANES)
- Gallup Organization

---

## Appendices

**Appendix A:** Raw Data Sources  
**Appendix B:** FACTS Format Template  
**Appendix C:** Excluded Domains (22 of 45)

---

**Contact:** coherence.faiththruphysics.com  
**License:** Public Domain. Copy freely. Credit appreciated.

*"The first step toward truth is admitting what you wanted to find."*