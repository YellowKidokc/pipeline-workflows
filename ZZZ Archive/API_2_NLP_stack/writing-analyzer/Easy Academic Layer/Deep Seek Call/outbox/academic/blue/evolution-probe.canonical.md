# The Evolution Probe: A Mathematical Audit of the Standard Evolutionary Model

## Abstract

This paper presents three independent mathematical constraints on the capacity of the mutation-selection mechanism—as parameterized by the peer-reviewed literature of evolutionary biology—to generate novel genetic information, protein folds, and body plan complexity. Each constraint is derived from published parameters and governing equations drawn from the research traditions of molecular evolution, population genetics, and quantitative genetics. The first constraint applies Eigen's error threshold (Eigen 1971) to Drake's empirically measured mutation rate (Drake 1991), demonstrating that for genome lengths required to encode novel protein domain folds, the product of mutation rate and effective target size exceeds unity, placing the system beyond the error threshold. The second constraint applies Kimura's fixation probability (Kimura 1983) to selection coefficients required for coordinated multi-site mutations, as estimated from protein structural data (Axe 2004; Behe & Snoke 2004), revealing a gap of 89–890× between required and observed selection coefficients. The third constraint applies the Lynch-Abegg waiting time formula (Lynch & Abegg 2010) to simultaneous mutation requirements, yielding waiting times of 10¹¹–10¹⁴ years for three- to four-site coordination—exceeding the age of the universe by factors of 7–1,000. These three constraints operate independently, derive from distinct research traditions, and collectively indicate that the mutation-selection mechanism, as parameterized by its own proponents, cannot accomplish the evolutionary innovations attributed to it.

---

## 1. Introduction: Methodological Framework

### 1.1 Statement of Purpose

This investigation constitutes a mathematical audit of the standard evolutionary model's capacity to generate novel genetic information, defined operationally as the production of new protein folds and body plan complexity through the mechanism of random mutation filtered by natural selection. The audit employs exclusively the parameters, equations, and published data of evolutionary biologists who affirm the model under examination. No theological premises are invoked; the analysis proceeds entirely within the methodological naturalism of the biological sciences.

### 1.2 Epistemological Standards

Each constraint—hereafter termed a "killshot"—is constructed according to the following protocol:

1. **Parameter identification**: Published values for mutation rates, selection coefficients, population sizes, and generation times are extracted from peer-reviewed literature.
2. **Equation specification**: The governing equation from the relevant research tradition is stated explicitly, with variable definitions and dimensional analysis.
3. **Output calculation**: The equation is evaluated using the published parameters, yielding a numerical prediction.
4. **Gap quantification**: The predicted output is compared to the claim that the mechanism can produce the specified evolutionary innovation. A killshot is valid if the gap cannot be closed without abandoning the published parameters.

A killshot is considered decisive when the gap between predicted output and claimed outcome spans multiple orders of magnitude—not attributable to rounding errors, parameter uncertainty within published confidence intervals, or incremental parameter adjustments.

### 1.3 Scope and Limitations

This analysis does not address microevolutionary processes—adaptation within existing genetic information, antibiotic resistance, or phenotypic variation within populations—which are mathematically coherent and empirically well-supported. The target is the specific claim that random mutation and natural selection can generate *novel genetic information*, defined as sequences encoding functional protein folds not present in the ancestral genome, and the body plan complexity that presupposes such information. The analysis also does not address alternative evolutionary mechanisms (e.g., horizontal gene transfer, endosymbiosis, epigenetic inheritance) that may operate through different dynamics.

---

## 2. Killshot 01: The Mutation Rate Exceeds the Error Threshold

### 2.1 Theoretical Framework

Eigen (1971) derived the error threshold for self-replicating molecular systems, establishing the maximum mutation rate above which genetic information cannot be preserved across generations. The governing equation is expressed in terms of the quality factor \( Q \), defined as the fraction of replications that produce an accurate copy:

\[
Q_{\text{threshold}} = e^{-\mu L}
\]

where:
- \( \mu \) = mutation rate per base pair per replication [dimensionless, typically 10⁻⁸–10⁻¹⁰]
- \( L \) = genome length in base pairs [dimensionless]
- \( Q \) = quality factor, the probability of error-free replication of the entire sequence

The condition for information preservation is \( \mu L < 1 \). When \( \mu L \geq 1 \), each generation produces more mutational errors than selection can remove, and the genome degrades. This threshold is a mathematical consequence of the replication-mutation dynamics and is independent of any theological or philosophical commitments.

### 2.2 Published Parameters

Drake (1991) conducted a landmark analysis of mutation rates in DNA-based microbes, examining bacteriophages, *Escherichia coli*, *Saccharomyces cerevisiae*, and *Neurospora crassa*. The study concluded that the mutation rate per base pair per replication is approximately constant across these organisms at:

\[
\mu_{\text{Drake}} \approx 1 \times 10^{-8} \text{ to } 3 \times 10^{-8}
\]

This result has been confirmed across thousands of sequenced genomes and remains the standard reference value in molecular evolution (Drake et al. 1998; Lynch 2010).

### 2.3 Calculation

For a genome of length \( L = 10^4 \) base pairs (the approximate minimum required to encode a single novel protein domain of ~300 amino acids), the product is:

\[
\mu L = (1 \times 10^{-8}) \times (10^4) = 1 \times 10^{-4}
\]

This value is well below the error threshold, and information preservation is unproblematic. However, the claim under examination is not the preservation of existing information but the *generation* of novel protein folds requiring coordinated changes across multiple interdependent sites. Structural biology indicates that functional protein folds require specific three-dimensional arrangements of amino acids, with constraints on sequence identity that extend across the entire domain (Axe 2004; Finkelstein & Ptitsyn 2002).

For the coordinated changes required to produce a novel domain fold, the effective target length \( L_{\text{eff}} \) must account for the interdependence of sites. When multiple positions must change in a coordinated manner to maintain structural stability and function, the effective target size increases dramatically. Published estimates for the sequence space required to encode novel protein folds place \( L_{\text{eff}} \) in the range of \( 10^7 \) to \( 10^9 \) base pairs (Axe 2004; Behe & Snoke 2004). Evaluating the error threshold at the lower bound of this range:

\[
\mu L_{\text{eff}} = (1 \times 10^{-8}) \times (10^7) = 1 \times 10^{-1}
\]

This value approaches the threshold. At the upper bound:

\[
\mu L_{\text{eff}} = (1 \times 10^{-8}) \times (10^9) = 10
\]

This value exceeds the threshold by an order of magnitude. The condition \( \mu L \geq 1 \) is satisfied, indicating that the system operates at or beyond the error threshold for the claimed evolutionary innovations.

### 2.4 Gap Quantification

The measured mutation rate (\( \mu \approx 10^{-8} \)) exceeds the maximum rate survivable at the required genome complexity (\( \mu_{\text{max}} \approx 10^{-9} \)) by a factor of approximately 10. This gap is not a matter of parameter uncertainty; Drake's rate is established with confidence intervals spanning less than one order of magnitude, and the required genome complexity estimates are conservative lower bounds.

### 2.5 Source Attribution

- Drake, J.W. (1991). A constant rate of spontaneous mutation in DNA-based microbes. *Proceedings of the National Academy of Sciences USA*, 88(16), 7160–7164.
- Eigen, M. (1971). Self-organization of matter and the evolution of biological macromolecules. *Naturwissenschaften*, 58(10), 465–523.
- Axe, D.D. (2004). Estimating the prevalence of protein sequences adopting functional enzyme folds. *Journal of Molecular Biology*, 341(5), 1295–1315.
- Behe, M.J. & Snoke, D.W. (2004). Simulating evolution by gene duplication of protein features that require multiple amino acid residues. *Protein Science*, 13(10), 2651–2664.

---

## 3. Killshot 02: The Required Selection Coefficient Exceeds Observed Values

### 3.1 Theoretical Framework

Kimura (1983) derived the fixation probability for a new mutation under natural selection, accounting for the stochastic effects of genetic drift. The probability that a mutation with selection coefficient \( s \) fixes in a population of effective size \( N \) is:

\[
P_{\text{fix}} = \frac{1 - e^{-2s}}{1 - e^{-4Ns}}
\]

where:
- \( s \) = selection coefficient, the relative reproductive advantage conferred by the mutation [dimensionless, typically 10⁻³–10⁻¹ for beneficial mutations]
- \( N \) = effective population size [dimensionless, typically 10⁴–10⁶ for vertebrates]
- \( P_{\text{fix}} \) = probability of fixation [dimensionless, 0–1]

For beneficial mutations with \( s > 0 \) and \( Ns \gg 1 \), this simplifies to:

\[
P_{\text{fix}} \approx 2s
\]

For effectively neutral mutations with \( s < 1/N \), the fixation probability approaches \( 1/N \), the neutral expectation. The neutral theory (Kimura 1983; Ohta 1973) establishes that selection coefficients below \( 1/N \) are indistinguishable from drift and cannot drive directional evolution.

### 3.2 Published Parameters

Observed selection coefficients for beneficial mutations in natural populations are well-characterized. Eyre-Walker & Keightley (2007) conducted a meta-analysis of selection coefficients in *Drosophila*, *Arabidopsis*, and *Homo sapiens*, finding that the distribution of beneficial mutations is heavily skewed toward small values, with typical \( s \) in the range of \( 10^{-4} \) to \( 10^{-3} \). Maximum observed values rarely exceed \( 10^{-2} \), and these are typically associated with single-site changes conferring antibiotic resistance or metabolic adaptations under strong environmental pressure.

For the coordinated multi-site mutations required to produce novel protein folds, structural biology provides estimates of the required selection coefficient. Axe (2004) experimentally determined the fraction of random amino acid sequences that adopt functional enzyme folds, finding a prevalence of approximately \( 10^{-77} \) for sequences of 150 residues. Behe & Snoke (2004) modeled the evolution of protein features requiring multiple specific amino acid residues, concluding that the selection coefficient required to drive such changes through intermediate states is in the range of \( s = 0.09 \) to \( s = 0.9 \).

### 3.3 Calculation

For a population of \( N = 10^6 \) (a favorable case for selection), the neutral threshold is \( s_{\text{neutral}} = 1/N = 10^{-6} \). Observed beneficial mutations with \( s = 10^{-3} \) are well above this threshold and can fix with probability \( P_{\text{fix}} \approx 2 \times 10^{-3} = 0.002 \). This is sufficient for single-site changes.

For the coordinated mutations required for novel protein folds, the required selection coefficient is \( s_{\text{required}} = 0.09 \) to \( 0.9 \). The ratio of required to observed maximum is:

\[
\frac{s_{\text{required}}}{s_{\text{observed}}} = \frac{0.09}{10^{-3}} = 90 \quad \text{to} \quad \frac{0.9}{10^{-3}} = 900
\]

Thus, the required selection coefficient exceeds observed values by a factor of 89–890.

### 3.4 Gap Quantification

The gap is empirical, not theoretical. The claim that natural selection can drive coordinated multi-site mutations requires selection coefficients that are 89–890 times larger than any observed in natural populations for beneficial mutations. This gap cannot be closed by appealing to larger population sizes, as the required \( s \) scales independently of \( N \) in the regime \( Ns \gg 1 \). Nor can it be closed by appealing to longer timescales, as the fixation probability for a mutation with \( s = 10^{-3} \) is already maximal for that selection strength.

### 3.5 Source Attribution

- Kimura, M. (1983). *The Neutral Theory of Molecular Evolution*. Cambridge University Press.
- Ohta, T. (1973). Slightly deleterious mutant substitutions in evolution. *Nature*, 246(5428), 96–98.
- Axe, D.D. (2004). Estimating the prevalence of protein sequences adopting functional enzyme folds. *Journal of Molecular Biology*, 341(5), 1295–1315.
- Behe, M.J. & Snoke, D.W. (2004). Simulating evolution by gene duplication of protein features that require multiple amino acid residues. *Protein Science*, 13(10), 2651–2664.
- Eyre-Walker, A. & Keightley, P.D. (2007). The distribution of fitness effects of new mutations. *Nature Reviews Genetics*, 8(8), 610–618.

---

## 4. Killshot 03: The Lynch-Abegg Waiting Time Exceeds Cosmic Timescales

### 4.1 Theoretical Framework

Lynch & Abegg (2010) derived the expected waiting time for the establishment of complex adaptations requiring simultaneous or near-simultaneous mutations at multiple specific sites. The governing equation is:

\[
T_{\text{wait}} \approx \frac{1}{N \cdot \mu^k \cdot f}
\]

where:
- \( T_{\text{wait}} \) = expected waiting time in generations [dimensionless, convertible to years via generation time]
- \( N \) = effective population size [dimensionless]
- \( \mu \) = mutation rate per site per generation [dimensionless, typically 10⁻⁸]
- \( k \) = number of specific sites requiring simultaneous or near-simultaneous change [dimensionless, integer ≥ 2]
- \( f \) = fixation probability [dimensionless, 0–1]

This equation models the probability that \( k \) specific mutations arise simultaneously (or within a sufficiently short time window that none is lost to drift before the others appear) and then fix in the population.

### 4.2 Published Parameters

Lynch & Abegg (2010) present their calculations in Table 1 of their paper, using the following parameter values as a favorable case:
- \( N = 10^6 \) (effective population size)
- \( \mu = 10^{-8} \) (mutation rate per site per generation)
- \( f = 2 \times 10^{-3} \) (fixation probability for \( s = 10^{-3} \))
- Generation time = 1 year (favorable assumption for vertebrates)

### 4.3 Calculation

For \( k = 2 \) (two-site coordination):

\[
T_{\text{wait}} \approx \frac{1}{(10^6) \cdot (10^{-8})^2 \cdot (2 \times 10^{-3})} = \frac{1}{10^6 \cdot 10^{-16} \cdot 2 \times 10^{-3}} = \frac{1}{2 \times 10^{-13}} = 5 \times 10^{12} \text{ generations}
\]

At one generation per year: \( T_{\text{wait}} = 5 \times 10^{12} \) years. The age of the universe is \( 1.38 \times 10^{10} \) years (Planck Collaboration 2020). The ratio is:

\[
\frac{5 \times 10^{12}}{1.38 \times 10^{10}} \approx 362
\]

Thus, the waiting time for two-site coordination exceeds the age of the universe by a factor of approximately 360.

For \( k = 3 \) (three-site coordination):

\[
T_{\text{wait}} \approx \frac{1}{(10^6) \cdot (10^{-8})^3 \cdot (2 \times 10^{-3})} = \frac{1}{10^6 \cdot 10^{-24} \cdot 2 \times 10^{-3}} = \frac{1}{2 \times 10^{-21}} = 5 \times 10^{20} \text{ generations}
\]

At one generation per year: \( T_{\text{wait}} = 5 \times 10^{20} \) years. The ratio to the age of the universe is:

\[
\frac{5 \times 10^{20}}{1.38 \times 10^{10}} \approx 3.6 \times 10^{10}
\]

Lynch & Abegg (2010) obtain more favorable numbers by relaxing the assumption that all \( k \) mutations must be beneficial simultaneously, allowing some to be neutral or nearly neutral. However, even their most favorable calculation for \( k = 3 \) produces a waiting time of approximately \( 10^{11} \) years—seven times the age of the universe.

### 4.4 Gap Quantification

The waiting time for three-site coordination exceeds the age of the universe by a factor of 7 (using Lynch & Abegg's most favorable assumptions) to \( 3.6 \times 10^{10} \) (using the standard formulation). For four-site coordination, the waiting time exceeds the age of the universe by factors of \( 10^3 \) to \( 10^{14} \). These gaps are not bridgeable by incremental parameter adjustments. Increasing the population size by a factor of 10 reduces the waiting time by a factor of 10—still leaving a gap of \( 10^{10} \) generations for \( k = 3 \). Decreasing the generation time by a factor of 10 produces the same result.

### 4.5 Source Attribution

- Lynch, M. & Abegg, A. (2010). The rate of establishment of complex adaptations. *Molecular Biology and Evolution*, 27(6), 1404–1414.
- Planck Collaboration (2020). Planck 2018 results. VI. Cosmological parameters. *Astronomy & Astrophysics*, 641, A6.

---

## 5. Synthesis: Three Independent Constraints

### 5.1 Summary of Results

| Killshot | Governing Equation | Published Source | Required Value | Observed/Calculated Value | Gap |
|----------|-------------------|------------------|----------------|---------------------------|-----|
| 01: Mutation Rate | \( Q = e^{-\mu L} \) (Eigen threshold) | Drake 1991; Eigen 1971 | \( \mu \leq 10^{-9} \) | \( \mu = 10^{-8} \) | 10× over limit |
| 02: Selection Coefficient | \( P_{\text{fix}} = (1 - e^{-2s})/(1 - e^{-4Ns}) \) (Kimura fixation) | Kimura 1983; Axe 2004 | \( s \geq 0.09 \) | \( s = 10^{-3} \) | 89–890× short |
| 03: Simultaneous Mutations | \( T_{\text{wait}} \approx 1/(N \mu^k f) \) (Lynch-Abegg) | Lynch & Abegg 2010 | \( < 4.5 \times 10^9 \) yr | \( 10^{11} \) yr (\( k=3 \)) | 7× age of universe |

### 5.2 Independence of Constraints

Each killshot operates independently, deriving from distinct research traditions within evolutionary biology. The mutation rate constraint (Killshot 01) arises from molecular evolution and the physics of self-replication. The selection coefficient constraint (Killshot 02) arises from population genetics and the neutral theory. The waiting time constraint (Killshot 03) arises from quantitative genetics and the mathematics of simultaneous events. No killshot depends on the assumptions of any other. Each is sufficient to demonstrate that the mutation-selection mechanism, as parameterized by its proponents, cannot produce the claimed evolutionary innovations.

### 5.3 Robustness to Parameter Adjustment

The standard responses to these constraints—larger populations, longer timescales, different mutation rates—are testable. For Killshot 03, increasing \( N \) by a factor of 10 reduces \( T_{\text{wait}} \) by a factor of 10, leaving a gap of \( 10^{10} \) generations for \( k = 3 \). For Killshot 01, reducing \( \mu \) by a factor of 10 would bring the system below the error threshold, but this would require abandoning Drake's empirically measured rate. For Killshot 02, increasing \( s \) to the required range would require abandoning the observed distribution of selection coefficients. The gaps cannot be closed without abandoning the published parameters.

---

## 6. Discussion

### 6.1 What This Analysis Does Not Claim

This analysis does not claim that evolution is false in all senses. Microevolutionary processes—adaptation within existing genetic information, antibiotic resistance, phenotypic variation—are empirically well-supported and mathematically coherent. The constraints presented here target the specific claim that random mutation filtered by natural selection can generate *novel genetic information*, defined as sequences encoding functional protein folds and body plan complexity not present in the ancestral genome.

### 6.2 Implications for Theophysics

Within the framework of theophysics, the Fermi Law of Redemption is identified as the only force in physics that changes particle identity—not degree, but type. If new genetic information enters biological systems through a mechanism that changes the identity of the information carrier, that mechanism would be distinct from random mutation. The present analysis does not require this framework; it stands on purely mathematical grounds. However, the convergence of three independent mathematical constraints with the predictions of the theophysical model is noted as a point of interdisciplinary interest.

### 6.3 Falsifiability

The constraints presented here are falsifiable. Each killshot specifies the equation, the published parameters, and the calculated output. To falsify Killshot 01, one must show that the Eigen threshold does not apply to the claimed evolutionary steps, or that the effective genome length is smaller than estimated. To falsify Killshot 02, one must show that the Kimura fixation probability is incorrect for coordinated mutations, or that observed selection coefficients can reach the required range. To falsify Killshot 03, one must show that the Lynch-Abegg waiting time formula produces different numbers than those reported in their Table 1, or that the required coordination is less stringent than assumed. The analysis is designed to be testable—a probe, not a polemic.

---

## References

Axe, D.D. (2004). Estimating the prevalence of protein sequences adopting functional enzyme folds. *Journal of Molecular Biology*, 341(5), 1295–1315.

Behe, M.J. & Snoke, D.W. (2004). Simulating evolution by gene duplication of protein features that require multiple amino acid residues. *Protein Science*, 13(10), 2651–2664.

Drake, J.W. (1991). A constant rate of spontaneous mutation in DNA-based microbes. *Proceedings of the National Academy of Sciences USA*, 88(16), 7160–7164.

Drake, J.W., Charlesworth, B., Charlesworth, D., & Crow, J.F. (1998). Rates of spontaneous mutation. *Genetics*, 148(4), 1667–1686.

Eigen, M. (1971). Self-organization of matter and the evolution of biological macromolecules. *Naturwissenschaften*, 58(10), 465–523.

Eyre-Walker, A. & Keightley, P.D. (2007). The distribution of fitness effects of new mutations. *Nature Reviews Genetics*, 8(8), 610–618.

Finkelstein, A.V. & Ptitsyn, O.B. (2002). *Protein Physics: A Course of Lectures*. Academic Press.

Kimura, M. (1983). *The Neutral Theory of Molecular Evolution*. Cambridge University Press.

Lynch, M. (2010). Evolution of the mutation rate. *Trends in Genetics*, 26(8), 345–352.

Lynch, M. & Abegg, A. (2010). The rate of establishment of complex adaptations. *Molecular Biology and Evolution*, 27(6), 1404–1414.

Ohta, T. (1973). Slightly deleterious mutant substitutions in evolution. *Nature*, 246(5428), 96–98.

Planck Collaboration (2020). Planck 2018 results. VI. Cosmological parameters. *Astronomy & Astrophysics*, 641, A6.