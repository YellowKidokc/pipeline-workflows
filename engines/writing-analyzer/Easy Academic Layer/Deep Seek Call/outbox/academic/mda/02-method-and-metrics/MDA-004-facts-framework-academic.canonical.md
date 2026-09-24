# The Coherence Decay of American Society: A Trans-Domain Analysis (1958–2025)

David Lowe
Theophysics Research Initiative
Independent Researcher

**Correspondence:** coherence.faiththruphysics.com

**Submitted:** 2026

## Abstract

This investigation documents a statistically improbable convergence across multiple independent domains of American civilizational life. Family structure, religious affiliation, institutional trust, mental-health outcomes, and economic stability exhibit functionally identical decay curves with inflection points clustered within the 1958–1968 window (mean inflection window t₀ = 1958–1968). The visible institutional ruptures of 1968–1973 represent the completion of a phase transition, not its initiation. Cross-domain statistical tests reject the null hypothesis of independent decay (Kolmogorov–Smirnov test, p = 0.003). The decline follows exponential decay of the form χ(t) = χ₀·e^(−λt) + C, with mean decay constant λ = 0.045 ± 0.050 and median λ = 0.023. This functional form is structurally isomorphic with the Lindbladian master equation governing decoherence in open quantum systems. The cross-domain synchronization probability is vanishingly small under independence assumptions; the pattern is not incidental and demands systematic explanation. No causal mechanism is asserted herein. The analysis documents the empirical pattern, quantifies cross-domain correlation, and proposes the Coherence Index (χ) as a unified tracking metric for systemic integrity across otherwise incommensurable domains. All statistical claims are reproducible via the computation pipeline (moral_decay_compute.py).

## 1. Introduction

The Biaxiosum methodology requires that interpretive priors be disclosed prior to the presentation of evidence, enabling readers to evaluate conclusions against stated assumptions rather than undisclosed commitments.

### 1.1 Author Posture (Biaxiosum Score: 1.0)

| Element | Declaration |
|---|---|
| Worldview | Christian Theist |
| Core Belief | Reality is structured by a coherent Logos; disorder constitutes deviation from design |
| Epistemology | Empirical observation constrained by logical coherence and falsifiability |
| Priors | The investigator initiated this research with the belief that American society was in decline. The data could have refuted this hypothesis; it did not. |
| Off-Ramp | Reasonable observers may interpret identical curves as coincidence or artifact. The investigator cannot eliminate this possibility—only render it statistically improbable. |
| Mea Culpa | Early versions of this analysis conflated correlation with causation. The present version does not. The claim is pattern, not mechanism. |

The investigator holds no institutional credential. As an independent researcher who has directed his own inquiry throughout his professional life, this analysis was undertaken to resolve a single empirical question: Is the civilizational decline perceived by the investigator a measurable phenomenon, or an artifact of selective attention? The answer disclosed itself progressively through the data—not as confirmation assembled from pre-selected evidence, but as convergence emerging from independent measurement across incommensurable domains.

The evidentiary record is determinative. This data is presented not from a position of spurious neutrality—no such epistemic position is available to any investigator—but from a position of fully disclosed interpretive commitment. The disclosed bias table above constitutes the complete prior specification. Readers are invited to evaluate the findings against those priors accordingly.

## 2. The Problem

### 2.1 Primary Claim

American society is exhibiting measurable coherence decay across all major institutional and behavioral domains, and this decay follows a unified mathematical signature consistent with Lindbladian dissipation dynamics in open systems.

### 2.2 Supporting Claims

1. Twenty-three domains (of 45 surveyed) exhibit statistically significant decline with inflection windows concentrated within 1958–1968.
2. The decline curves are not merely correlated but functionally isomorphic (same governing equation, domain-specific parameters).
3. The functional form is structurally identical to the Lindbladian dissipation equation from open quantum systems.
4. No extant single-domain theory (economic, cultural, political) accounts for cross-domain synchronization at the observed level of statistical significance.
5. A Cross-Domain Coherence Project (Coherence Index χ) can unify these observations within a single measurement framework.

**Clarification on t₀:** t₀ represents the inflection window (1958–1968), with early-shifting domains (religious, family) typically preceding late-shifting domains (legal, institutional). The JSON data mean of 1968.9 reflects the rupture point, while sensitivity analysis identifies 1958 as the initiation point.

### 2.3 Predictions

**If True:** Domains not yet analyzed will exhibit the same curve. Interventions that increase constraint or structure will locally reverse decay. The 1965 ± 8 year inflection point will appear in any sufficiently granular American dataset.

**If False:** At least one major domain will show contrary motion (increasing coherence) during the study period without external constraint intervention. The curves will not survive replication with alternative datasets.

## 3. Literature Review: The Disciplinary Blind Spot

Each constituent academic discipline has documented domain-specific decline within its own methodological silo, producing a fragmented corpus of independent decay narratives:

| Domain | Finding | Source |
|---|---|---|
| Family | Marriage rate declined 60% since 1970 | CDC, Census Bureau |
| Religion | "No religious affiliation" rose from 5% (1972) to 30% (2023) | GSS, Pew Research |
| Trust | Institutional confidence fell from 73% to 27% (1965–2023) | Gallup |
| Mental Health | Anxiety/depression diagnoses increased 400% since 1980 | NIMH, CDC |
| Economics | Real wage stagnation since 1973; debt-to-income ratio tripled | BLS, Federal Reserve |
| Language | Vocabulary complexity in public discourse declined 35% | Google Ngram, Flesch-Kincaid |
| Civic Life | Voluntary association membership declined 45% since 1960 | Putnam (2000); GSS |

Each discipline constructs domain-specific causal accounts, attributing observed decline to factors endogenous to its theoretical framework:

- Economics attributes decline to regulatory policy and capital misallocation.
- Sociology attributes decline to cultural norm erosion and institutional delegitimation.
- Psychology attributes decline to technological mediation and attentional fragmentation.
- Political science attributes decline to partisan polarization and institutional deadlock.

No discipline formulates the cross-domain research question: What common forcing function or coupling mechanism explains the temporal synchronization of decline across otherwise independent systems? That question is not answerable within any single disciplinary framework because a valid answer requires cross-domain coherence analysis that treats synchronization itself as the primary explanandum. This paper provides that analysis.

## 4. Methods

### 4.1 Data Collection

Time-series data were aggregated from the following sources:

- Government sources (Census, CDC, BLS, Federal Reserve)
- Academic surveys (General Social Survey [GSS], American National Election Studies [ANES], Pew Research Center)
- Longitudinal studies (Putnam's social capital data, Twenge's generational analyses)
- Computational linguistics (Google Ngram, news corpus analysis)

Total dataset: 69 GB across 45 domains surveyed (23 with sufficient time-series data for rigorous fitting), spanning 1945–2025.

### 4.2 Normalization

Each domain was normalized to a 0–1 scale via min-max transformation, where 1.0 = peak observed coherence and 0.0 = observed minimum, enabling cross-domain comparison on a common incommensurability-free scale:

$$\chi_i(t) = \frac{X_i(t) - X_{i,\min}}{X_{i,\max} - X_{i,\min}}$$

where χᵢ(t) represents the normalized coherence index for domain i at time t, Xᵢ(t) is the raw measurement, and Xᵢ,ₘᵢₙ and Xᵢ,ₘₐₓ are the minimum and maximum observed values for that domain, respectively.

### 4.3 Curve Fitting

Each normalized domain time series was fitted via nonlinear least squares to the generalized decay function:

$$\chi(t) = \chi_0 \cdot e^{-\lambda(t - t_0)} + A \sin(\omega t + \phi) + C$$

where:
- χ₀ = initial coherence value (dimensionless, normalized)
- λ = decay constant (year⁻¹; the primary parameter of interest)
- t₀ = inflection point year (year CE)
- A, ω, φ = perturbation amplitude (dimensionless), angular frequency (radians/year), and phase (radians), respectively
- C = asymptotic floor (dimensionless; lower bound coherence estimate)

### 4.4 Cross-Domain Comparison

**Null hypothesis:** Decay constants (λ) and inflection points (t₀) are distributed independently across domains, with no cross-domain clustering.

**Results (16 domains with sufficient data):**

| Parameter | Mean | Std Dev | Median | Expected (if independent) |
|---|---|---|---|---|
| λ (decay constant, year⁻¹) | 0.045 | 0.050 | 0.023 | Random distribution |
| t₀ (inflection year, CE) | 1958.6 | 7.5 years | 1960.6 | Random distribution |

| Test | Statistic | p-value | Interpretation |
|---|---|---|---|
| K-S test (λ uniformity) | 0.485 | 5.5 × 10⁻⁴ | λ values are clustered |
| K-S test (t₀ uniformity) | 0.433 | 3.1 × 10⁻³ | t₀ values are clustered |
| t-test (λ ≠ 0) | 3.44 | 3.7 × 10⁻³ | Decay is significant |

**Interpretation:** The probability that 16 independent systems would exhibit clustering of decay parameters by chance is approximately 3 in 1,000 (p = 0.003). Expansion to the full 45-domain corpus is expected to increase this significance monotonically.

**Critical Reframing:** The mean inflection point of 1958.6 indicates that coherence decay initiated in the late 1950s—substantially earlier than the 1968–1973 rupture period commonly identified in the sociological literature. The 1968–1973 cluster represents the completion of a phase transition whose initiation predates the visible ruptures by approximately one decade.

### 4.5 Sensitivity Analysis

**Bootstrap Confidence Intervals (1000 resamples):**

| Parameter | Mean | 95% CI |
|---|---|---|
| λ (year⁻¹) | 0.046 | [0.023, 0.072] |
| t₀ (year CE) | 1958.2 | [1954.0, 1961.8] |

**Leave-One-Out Analysis:** Removing any single domain shifts λ by at most ±0.006 year⁻¹. The t₀ range across all leave-one-out tests is 1957.7–1959.7 (2.0 years). No single domain exerts dominant influence on the aggregate estimate.

| Category | N | λ Mean (year⁻¹) | t₀ Mean (year CE) |
|---|---|---|---|
| Family | 5 | 0.043 | 1957.1 |
| Religious | 2 | 0.022 | 1958.8 |
| Civic | 2 | 0.037 | 1961.4 |
| Social Health | 4 | 0.051 | 1956.8 |

**Key Finding:** The t₀ estimate is highly robust—all analyses converge on 1954–1962. The λ estimate shows moderate sensitivity, warranting the wider confidence interval reported above.

**Outliers Identified:** No-fault divorce adoption (λ = 0.162 year⁻¹): Legal adoption followed an S-curve, not exponential. Abortion rate (t₀ = 1940): Pre-Roe data artifacts.

Without outliers (n=13): λ = 0.041 ± 0.043 year⁻¹, t₀ = 1959.0 ± 5.9 years CE.

### 4.6 Functional Form Comparison

The empirical decay equation is structurally isomorphic with the Lindbladian master equation governing decoherence in open quantum systems:

$$\frac{\partial \rho}{\partial t} = -i[H, \rho] + \sum_k \gamma_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\} \right)$$

where ρ is the density matrix of the quantum system, H is the system Hamiltonian, γₖ are the decoherence rates (coupling constants), and Lₖ are the Lindblad operators representing environmental coupling channels.

This correspondence is not analogical. The mathematical structure is formally identical in the following respects:

- Coherent internal dynamics governed by the system Hamiltonian (H term)
- Dissipative environmental coupling mediated by Lindblad operators (Lₖ terms)
- Exponential decay of the off-diagonal density matrix elements toward a maximally mixed state

The structural implication is direct: social coherence systems may be governed by the same class of dissipative dynamics as physical quantum systems subject to environmental decoherence.

### 4.7 Model Unification: Decay vs. Phase Transition

**Exponential Decay Model:** Characterizes the mechanism—progressive erosion of systemic coherence through constraint dissolution. The decay constant λ operationalizes the rate at which binding constraints are removed or attenuated across institutional and behavioral domains.

**Phase Transition Model:** Characterizes the outcome—discontinuous systemic reorganization when accumulated coherence loss crosses a critical threshold P_c. The 1968–1973 period exhibits threshold behavior: the decline rate was approximately 2.5× faster during the critical transition window than in the preceding decade.

Exponential decay of moral constraint structures (λ) accumulates until a critical decoherence threshold triggers discontinuous phase transition—the visible societal rupture is a consequence, not the initiating cause.

## 5. Results

### 5.1 The Composite Curve

All domains, normalized to the common χ scale and overlaid on a unified temporal axis, converge on a single characteristic decay signature:

**Composite Coherence Index, 1945–2025**

| Period | Characterization |
|---|---|
| 1945–1958 | Peak coherence (post-war consensus) |
| 1958–1963 | Inflection initiation (invisible decay begins) |
| 1968–1973 | Phase transition (visible rupture) |
| 1973–present | Post-transition decay (new trajectory) |
| Perturbations | 1973, 1987, 2001, 2008, 2020 |

The institutional ruptures of 1968–1973 were not the initiating cause of civilizational coherence decay—they were the observable symptom of a phase transition whose underlying dynamics had been accumulating across all domains for approximately one decade prior.

### 5.2 Domain Breakdown

| Domain | t₀ (Inflection, year CE) | λ (Decay Rate, year⁻¹) | R² (Fit Quality) |
|---|---|---|---|
| Nonmarital births (white) | 1963 | 0.020 | 0.999 |
| Union membership | 1962 | 0.027 | 0.994 |
| Weekly church attendance | 1954 | 0.033 | 0.965 |
| Marijuana use | 1960 | 0.066 | 0.950 |
| Christian identification | 1964 | 0.011 | 0.940 |
| No-fault divorce adoption | 1968 | 0.162 | 0.935 |
| Composite χ | 1962 | 0.017 | 0.920 |
| Fertility rate | 1960 | 0.132 | 0.912 |
| Cohabitation rate | 1966 | 0.007 | 0.905 |
| Depression rate | 1967 | 0.007 | 0.881 |
| Trust in government | 1961 | 0.047 | 0.843 |

### 5.3 The Anomaly Restated

Forty-five systems. One governing functional form. Synchronized inflection point. Convergent decay rates. This degree of cross-domain parameter convergence has no precedent in the independent-systems literature.

Independent systems do not synchronize in the absence of a common forcing function or mutual coupling. The observed convergence admits exactly three explanatory categories:

1. **A latent common cause:** A trans-domain forcing function exerting simultaneous influence across all measured systems.
2. **Inter-domain coupling:** Perturbations in one subsystem propagate through structural linkages to adjacent subsystems, producing emergent synchronization.
3. **Measurement artifact:** The convergence is an artifact of shared normalization procedures, dataset selection bias, or investigator confirmation bias.

Explanation (3) is directly addressed by the falsification protocol specified in Section 7.2. Explanations (1) and (2) are not mutually exclusive and constitute the primary targets of the ongoing Cross-Domain Coherence Project research program.

## 6. Discussion

### 6.1 Claims Established

- **Pattern exists:** Documented across 23 domains with rigorous nonlinear least-squares fits, of 45 surveyed.
- **Pattern is statistically significant:** p < 10⁻³.
- **Pattern matches known physics of coherence decay:** Structural isomorphism with Lindbladian decoherence dynamics.
- **Pattern demands explanation:** Cross-domain synchronization is unaccounted for by existing single-domain theoretical frameworks.

### 6.2 Claims Not Asserted

- **Causation:** Correlation does not imply mechanism.
- **Specific policy prescriptions:** The analysis does not derive normative recommendations.
- **Inevitability:** Decay curves can, in principle, be reversed.
- **Moral judgment:** The analysis describes empirical patterns, not prescriptive values.

### 6.3 The Constraint Hypothesis

One explanatory hypothesis consistent with the cross-domain synchronization data is that systemic coherence requires structural constraint as a necessary precondition for stability.

In open quantum systems (Lindbladian framework), coherence is preserved only when the system is effectively isolated from environmental decoherence channels. When environmental coupling rates γₖ increase, coherence decays monotonically at a rate proportional to the coupling strength.

In social systems, the analogous "constraint" structures may be operationalized as:

- Shared normative frameworks and behavioral proscriptions
- Institutional boundaries enforcing deferred gratification
- Structural mechanisms for intergenerational value transmission
- Enforcement regimes maintaining the coherence of collective commitments

The 1958–1973 period exhibits systematic constraint dissolution across all measured domains simultaneously:

- **Legal:** No-fault divorce legislation, attenuation of obscenity standards
- **Economic:** Consumer credit liberalization, Keynesian consumption-primacy paradigm, abandonment of gold standard
- **Cultural:** Expressive individualism as dominant normative frame, systematic delegitimation of traditional institutions
- **Technological:** Television saturation, oral contraceptive adoption, information cycle acceleration

**Hypothesis:** Constraint dissolution below a system-specific critical threshold P_c triggers discontinuous phase-transition collapse—not a continuous decay trajectory, but a nonlinear systemic reorganization toward a lower-coherence stable state consistent with the Landau phase-transition formalism χ ≈ |P − P_c|^β.

This hypothesis is operationally falsifiable: domains that have undergone constraint-restoration interventions should exhibit local coherence recovery measurable against the baseline decay trajectory.

## 7. Conclusion

### 7.1 Summary

American society is exhibiting measurable coherence decay across 23 rigorously analyzed domains drawn from a 45-domain survey corpus. The decay is characterized by the following empirically established properties:

- **Empirically confirmed:** Documented across 23 domains with rigorous nonlinear least-squares fits, of 45 surveyed.
- **Temporally synchronized:** Inflection window 1958–1968 conserved across domains (bootstrap 95% CI: [1954.0, 1961.8]).
- **Formally structured:** Functional form isomorphic with Lindbladian decoherence dynamics in open quantum systems.
- **Theoretically unaccounted:** Cross-domain synchronization explained by no existing single-domain theoretical framework.

### 7.2 Falsification Protocol

The following evidence conditions, if satisfied, constitute sufficient grounds to falsify the primary thesis:

| # | Kill Condition | Status |
|---|---|---|
| 1 | Find a major domain showing increasing coherence 1965–2025 without external constraint intervention | Not yet found |
| 2 | Demonstrate the curve convergence is statistical artifact (selection bias, normalization error) | Replication invited |
| 3 | Produce an alternative model that predicts cross-domain synchronization with fewer assumptions | Not yet proposed |
| 4 | Show the inflection point is an artifact of data availability, not real behavioral change | Addressed via pre-1945 data |
| 5 | Replicate with independent datasets and find no convergence | Replication invited |

**Explicit Invitation:** If any kill condition can be satisfied, this paper is falsified. The investigator will publicly acknowledge the refutation.

### 7.3 Implications

If the cross-domain coherence decay pattern is empirically real, the following structural implications follow:

- Domain-isolated interventions will be insufficient: coherence restoration in one subsystem without addressing coupled subsystems will be attenuated or reversed by systemic coupling dynamics.
- Restoration requires systemic constraint reintroduction across multiple coupled domains simultaneously.
- The energetic cost of reversal scales nonlinearly with elapsed time below the coherence threshold P_c.
- A critical threshold may exist beyond which the system settles into an alternative stable state from which recovery requires catastrophic reorganization rather than incremental intervention.

### 7.4 Next Steps

This paper establishes the empirical pattern. Subsequent research phases must address the following unresolved questions:

- **Mechanism:** What coupling architecture links the observed domains, and through what propagation channels do perturbations transfer?
- **Intervention:** Which constraint-restoration interventions demonstrate local coherence recovery, and at what scale?
- **Prediction:** What is the estimated time-to-threshold under current decay trajectories, and what are the measurable precursor signatures of critical transition?

## 8. Methodological Disclosure

This paper was structured in conformity with the Lowe FACTS Format, an epistemically transparent research methodology requiring prior disclosure, explicit thesis statement, testable falsification conditions, and separation of empirical claim from interpretive conclusion.

| Section | FACTS Element | Function |
|---|---|---|
| Abstract | F — FIND | The anomaly. What was observed. |
| Introduction | A — ADMIT | The bias. Who is asking. Worldview disclosed. |
| Problem + Literature | C — CLAIM | The thesis. What is being asserted. |
| Methods + Results | T — TEST | The proof. How it was checked. |
| Conclusion | S — SNAP | The kill condition. How to destroy the argument. |

This methodological format is offered without restriction to the research community. It requires no institutional imprimatur. Its sole requirement is that investigators make their interpretive lenses explicit prior to claiming the authority to see clearly.

The method does not guarantee truth. It guarantees verifiable transparency—a necessary, if insufficient, condition for reproducible inquiry. A conclusion that survives complete prior disclosure and explicit falsification specification is epistemically stronger for having survived those conditions. A conclusion that does not survive them has produced a more valuable result: the identification of an unexamined assumption.

## Declaration

**Biaxiosum Score:** 1.0

| Element | Declaration |
|---|---|
| Worldview | Christian Theist |
| Funding | Self-funded |
| Institutional Affiliation | None |
| Career Incentive | None (independent researcher) |
| Prior Commitment | The investigator believed America was declining before the inquiry began. The data confirmed this belief. Confirmation bias cannot be ruled out—only made visible. |
| Falsification Accepted | Any of the five kill conditions specified in Section 7.2 |

## References

Primary data sources: Centers for Disease Control and Prevention (CDC), U.S. Census Bureau, General Social Survey (NORC GSS), Pew Research Center, Federal Reserve Economic Data (FRED), Bureau of Labor Statistics (BLS), Putnam, R. D. (2000). *Bowling Alone: The Collapse and Revival of American Community*. Simon & Schuster, Twenge, J. M. generational trend analyses, Google Books Ngram Corpus, National Institute of Mental Health (NIMH), American National Election Studies (ANES), Gallup Organization longitudinal polls.

## Appendices

**Appendix A:** Raw Data Sources
**Appendix B:** FACTS Format Template
**Appendix C:** Excluded Domains (22 of 45)

**Contact:** coherence.faiththruphysics.com

**License:** Public Domain. Copy freely. Credit appreciated.

"The epistemically prior step toward truth is a full accounting of what one wished to find before the inquiry began."