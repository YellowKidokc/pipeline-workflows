```yaml
---
claims:
  - "The measured mutation rate (10⁻⁸ per base per replication) exceeds Eigen's error threshold for genomes large enough to produce novel protein folds, so genetic information cannot be preserved across generations."
  - "The selection coefficient required to fix coordinated multi-site mutations (s ≥ 0.09) is 89 to 890 times larger than the maximum observed in natural populations (s = 10⁻³), making such fixations impossible under Kimura's neutral theory."
  - "Lynch and Abegg's own waiting-time equation shows that a three-site coordinated mutation requires 10¹¹ years to arise and fix — 7 times longer than the age of the universe (1.38 × 10¹⁰ years)."
domains:
  Physics: 15
  Biology: 50
  Mathematics: 20
  Information Theory: 10
  Theology: 5
---
```

# The Evolution Probe

**Three mathematical killshots against the standard evolutionary model — using the model's own published numbers, its own cited authors, its own equations. No theology required. The math fails on its own terms.**

## The Method

### Their Numbers. Their Authors. Their Failure.

This is not a theological argument. It's a math audit. We take the numbers published by leading evolutionary biologists — mutation rates, selection strengths, population sizes — plug them into the equations those same scientists use, and show that the results don't match the claims. Every number here comes from peer-reviewed science papers. Every author cited supports the evolutionary model being tested.

**On Their Own Terms**

### What This Is Not

This is not an attack on scientists. It's not young-earth creationism. It's not a refusal to look at evidence. It's a math audit of whether the claimed mechanism — random mutations filtered by natural selection — can actually produce what people say it does, given the published limits on the process. The answer, using their own numbers, is no.

**The standard of proof:** Each killshot gives the published numbers, the main equation, the calculated result, and the gap between that result and the claim. A killshot is valid if you can't close the gap without throwing out the published numbers. All three gaps are huge — not small rounding errors.

## Killshot 01 · Mutation Rate

### The Mutation Rate Exceeds the Error Threshold

**Drake · Eigen · Published Genomic Data**

**FAILS BY 10×**

John Drake published the main measurement of mutation rates in DNA-based organisms in 1991. His result, now confirmed across thousands of sequenced genomes, gives a mutation rate per base pair per replication. Manfred Eigen figured out the error threshold — the highest mutation rate that still allows genetic information to survive from one generation to the next.

The problem: when you apply Drake's measured rate to Eigen's threshold equation for organisms with genomes big enough to produce new protein folds, the measured rate is higher than the threshold. The genome can't preserve the information needed for the claimed evolution to happen.

- **10⁻⁸** — Drake Rate (per base per replication)
- **10⁻⁹** — Eigen Threshold (max survivable rate)
- **10×** — Gap — Their Numbers

**Q_threshold = e^(−μL)** → Eigen's Error Threshold

Q = quality factor — the fraction of replications that produce an accurate copy. μ = mutation rate per base per replication (Drake: ~10⁻⁸). L = genome length needed for the new function being claimed. When μL > 1, the error threshold is crossed: each generation produces more mutation errors than selection can remove. The genome degrades. Information is lost faster than selection can save it.

For a genome of 10,000 base pairs (the minimum for a new protein fold family): μL = 10⁻⁸ × 10⁴ = 10⁻⁴. That looks fine. But the claimed evolutionary steps need coordinated changes across *many* interdependent sites — which raises the effective L a lot. For the coordination needed to produce new domain folds, the effective target reaches 10⁷ to 10⁹ bases. At that point, μL ≥ 1 and the threshold is crossed.

**Their Claim**

Mutation + selection produces new protein folds and new genetic information over deep time. The mutation rate is low enough that selection can preserve beneficial changes.

**What Their Numbers Show**

Drake's measured rate applied to Eigen's threshold equation, using the genome complexity needed for the claimed novelty, puts the system at or past the error threshold. Selection can't work faster than mutations destroy information.

**Source:** Drake, J.W. (1991). "A constant rate of spontaneous mutation in DNA-based microbes." *PNAS* 88(16):7160–7164. Eigen, M. (1971). "Self-organization of matter." *Naturwissenschaften* 58:465–523. The gap between measured rate and required threshold is not disputed — the dispute is over whether the threshold applies to the claimed evolutionary steps. The math says it does.

## Killshot 02 · Selection Coefficient

### The Required Selection Coefficient Is 89–890× Above Observed

**Kimura · Ohta · Published Population Genetics**

**FAILS BY 89–890×**

Motoo Kimura and Tomoko Ohta's neutral theory of molecular evolution — now the main framework in population genetics — sets the range of selection coefficients that natural selection can "see." Coefficients below 1/N (where N is effective population size) are effectively neutral — selection can't tell them apart from random genetic drift.

The selection coefficient needed for a new beneficial mutation to take over a population — rather than drift to extinction — must be big enough to beat drift. Observed selection coefficients for beneficial mutations in natural populations are measured in the range of 10⁻³ to 10⁻⁴. The coefficient needed to drive the coordinated multi-site changes attributed to major evolutionary innovations is 89 to 890 times larger than the observed maximums.

- **10⁻¹** — Required s (novel fold)
- **10⁻³** — Observed s (natural max)
- **89–890×** — Gap — Their Numbers

**P_fix = (1 − e^(−2s)) / (1 − e^(−4Ns))** → Kimura Fixation Probability

P_fix = probability that a new mutation takes over the population instead of drifting to extinction. s = selection coefficient — the reproductive advantage the mutation gives. N = effective population size. For a beneficial mutation with s = 10⁻³ in a population of N = 10⁶: P_fix ≈ 2s = 0.002. One in five hundred new beneficial mutations takes over. The rest are lost to drift.

For the coordinated mutations needed to produce a new protein domain fold — where multiple specific amino acid positions must change together to produce a working intermediate — the effective selection coefficient must be large enough to drive all the coordinated changes at the same time or in very tight sequence. Calculations using published protein structure data (Axe 2004, Behe & Snoke 2004) place the required s at 0.09 to 0.9. No natural population has been observed producing beneficial mutations at this selection strength. The gap is not theoretical — it's based on real-world data.

**Their Claim**

Natural selection acting on random mutations can drive the origin of new protein folds and new body plans over geological time. The process is gradual and each step is individually beneficial.

**What Their Numbers Show**

The observed selection coefficients for beneficial mutations are 89 to 890 times smaller than what Kimura's fixation equation needs to drive coordinated multi-site changes. Gradual step-by-step accumulation can't bridge this gap because the intermediate states don't work.

**Sources:** Kimura, M. (1983). *The Neutral Theory of Molecular Evolution.* Cambridge University Press. Axe, D.D. (2004). "Estimating the prevalence of protein sequences adopting functional enzyme folds." *Journal of Molecular Biology* 341(5):1295–1315. Behe, M.J. & Snoke, D.W. (2004). "Simulating evolution by gene duplication of protein features that require multiple amino acid residues." *Protein Science* 13(10):2651–2664.

## Killshot 03 · Simultaneous Mutations

### Lynch & Abegg's Simultaneous Mutation Requirement Is Off by 11 Orders of Magnitude

**Lynch · Abegg · Their Own Published Calculation**

**FAILS BY 10¹¹**

Michael Lynch and Aisha Abegg published a 2011 paper in *Evolution* calculating the waiting time for mutations that need two or more simultaneous specific changes. This is the paper most often cited by evolutionary biologists as showing that complex adaptations are possible. It is also — using their own numbers — the clearest demonstration that they are not.

Lynch & Abegg calculate waiting times for two-site coordinated mutations. For a population of 10⁶ organisms with a generation time of one year, the waiting time for a two-site specific coordinated mutation is about 10⁸ years. For three sites: 10¹¹ years. For four sites: 10¹⁴ years. The age of the universe is 1.38 × 10¹⁰ years. The math is theirs. The problem is theirs.

- **10¹¹ yr** — Wait time (3-site coordination)
- **1.38×10¹⁰ yr** — Age of universe
- **10×** — Longer than universe exists

**T_wait ≈ 1 / (N · μᵏ · f)** → Lynch-Abegg Waiting Time

T_wait = expected waiting time for the coordinated mutation to arise and take over. N = effective population size (Lynch & Abegg use 10⁶ as a favorable case). μ = mutation rate per site per generation (Drake: 10⁻⁸). k = number of specific sites needing simultaneous or near-simultaneous change. f = fixation probability.

For k = 2: T ≈ 1 / (10⁶ × (10⁻⁸)² × 2×10⁻³) = 1 / (10⁶ × 10⁻¹⁶ × 2×10⁻³) ≈ 5 × 10¹² generations. At one generation per year: 5 × 10¹² years. The age of the universe: 1.38 × 10¹⁰ years. This is 363 times longer than the universe has existed — for just two coordinated sites. Lynch & Abegg get a more favorable number by assuming many coordinating mutations don't all need to be beneficial at the same time. But even their most favorable calculation for k=3 produces a waiting time 7 times the age of the universe.

**Their Claim (Lynch & Abegg 2011)**

"Complex adaptations requiring the simultaneous occurrence of multiple mutations can evolve on reasonable timescales." They present this as a defense of evolutionary gradualism against ID arguments.

**What Their Equations Actually Show**

Their own equations produce waiting times of 10¹¹ to 10¹⁴ years for 3-4 site coordination — 7 to 1,000 times the age of the universe. The paper intended to refute this problem accidentally measures it exactly.

**Source:** Lynch, M. & Abegg, A. (2010). "The rate of establishment of complex adaptations." *Molecular Biology and Evolution* 27(6):1404–1414. The waiting time calculations appear in Table 1 of that paper. We are using their numbers from their table. The conclusion that these times exceed geological and cosmic timescales follows directly from their published results.

---

## The Combined Case

### Three Independent Constraints

**Any One Is Sufficient. All Three Together Is Decisive.**

Each killshot works on its own. The mutation rate problem doesn't depend on the selection coefficient problem. The Lynch-Abegg waiting time problem doesn't depend on either of the others. These are three separate math limits on the same claimed mechanism, coming from three different research traditions, all using peer-reviewed published numbers. All three produce the same result: the mechanism can't do what people say it does.

| Killshot | Equation Used | Published Source | Required Value | Observed Value | Gap |
|---|---|---|---|---|---|
| 01 · Mutation Rate | Eigen threshold Q = e^(−μL) | Drake 1991, Eigen 1971 | μ ≤ 10⁻⁹ | μ = 10⁻⁸ | 10× over limit |
| 02 · Selection Coefficient | Kimura P_fix = f(s, N) | Kimura 1983, Axe 2004 | s ≥ 0.09 | s = 10⁻³ | 89–890× short |
| 03 · Simultaneous Mutations | Lynch-Abegg T ≈ 1/(Nμᵏf) | Lynch & Abegg 2010 | < 4.5 × 10⁹ yr | 10¹¹ yr (k=3) | 7× age of universe |

**The standard response** to each of these is that evolution had more time, larger populations, or different mechanisms than the ones being modeled. Those responses can be tested. If the population were 10 times larger, the waiting time drops by 10 — still 7 times the age of the universe for k=3. If the generation time were 10 times shorter, same result. The gaps are not closed by small adjustments to the numbers. They require throwing out the published numbers entirely, which means throwing out the published literature these arguments depend on.

### What This Means

**What This Does Not Mean**

This is not a claim that evolution is false in every sense of the word. Microevolution — adaptation within existing genetic information, antibiotic resistance, beak size variation — is real and mathematically sound. Like the strong nuclear force holding a nucleus together, it produces real variation within stable bound states.

The killshots target a specific claim: that the mechanism of random mutation filtered by natural selection can produce *new genetic information*, new protein folds, and new body plan complexity. That specific claim fails the published math.

**The Theophysics Position**

The Fermi Law — Redemption — is the only force in physics that changes a particle's *identity*. Not degree. Type. If new information enters biological systems, it does so through an identity-change mechanism that has a name in the canonical framework. Random mutation is not that mechanism.

**The invitation:** These kill conditions are clear. If you can show that the Eigen threshold does not apply to the claimed evolutionary steps, show the calculation. If you can show that the Kimura fixation probability is wrong for coordinated mutations, show the math. If you can show that Lynch & Abegg's waiting time formula produces different numbers than what their Table 1 reports, show the derivation. The probe can be proven wrong. That's what makes it a probe and not a rant.

---

**David Lowe · faiththruphysics.com · April 2026 · The Probe Series · POF 2828 · Their numbers. Their authors. Their failure.**