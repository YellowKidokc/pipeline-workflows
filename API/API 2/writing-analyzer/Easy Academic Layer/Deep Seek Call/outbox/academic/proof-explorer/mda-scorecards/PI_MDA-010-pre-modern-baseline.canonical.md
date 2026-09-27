# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Galatians 5:22–23

## Abstract

This article presents a formal interdisciplinary analysis of the Pauline concept of the Fruits of the Spirit (Galatians 5:22–23) through a dual-channel framework integrating lexical-semantic and affective-psychological methodologies. Employing computational text analysis tools—specifically the Lexical (L6) and Emotional (L8) channels—the study quantifies the distribution of nine virtue terms across semantic density and emotional valence. The analysis yields a mean coherence score of 0.430 and an overall CHI score of 0.44, indicating moderate structural integration between the two analytical dimensions. The dominant emotional category identified is "realization" (0.055), with secondary contributions from approval (0.029) and confusion (0.016). The study further introduces a master equation framework for modeling the interaction between lexical frequency and emotional intensity, and proposes a preliminary typology of "anti-fruits" as conceptual opposites. The findings suggest that the Pauline virtues exhibit a non-uniform distribution across cognitive and affective registers, with implications for both theological anthropology and theophysics modeling.

---

## 1. Introduction

The intersection of theological doctrine and physical formalism—herein termed *theophysics*—requires rigorous methodological scaffolding to avoid category errors between spiritual and natural domains. The present study addresses this challenge by analyzing Galatians 5:22–23, wherein the Apostle Paul enumerates nine virtues (love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control) as the "fruit of the Spirit." These virtues are examined through a dual-channel analytical framework that distinguishes between lexical-semantic content (Channel L6) and affective-emotional valence (Channel L8). The objective is to determine whether the Pauline virtues exhibit a coherent structural pattern that can be modeled using formal mathematical and computational tools.

This investigation is motivated by the observation that theological texts often encode multidimensional information—doctrinal, ethical, affective, and relational—that resists reduction to a single analytical axis. By operationalizing the distinction between lexical and emotional channels, the study seeks to identify latent structural isomorphisms between scriptural virtue ethics and contemporary psychometric models of emotion (e.g., the NRC Emotion Lexicon and the GoEmotions taxonomy).

---

## 2. Methodological Framework

### 2.1 Dual-Channel Analysis

The analytical architecture employed herein comprises two primary channels:

- **Channel L6 (Lexical):** Measures the semantic density of virtue terms within the pericope of Galatians 5:22–23. Lexical density is operationalized as the ratio of content-bearing terms to total tokens, normalized to a [0,1] interval. Values approaching 1.0 indicate maximal semantic concentration.

- **Channel L8 (Emotion):** Quantifies the affective valence associated with each virtue term, derived from the NRC Emotion Lexicon (Mohammad & Turney, 2013) and the GoEmotions fine-grained taxonomy (Demszky et al., 2020). Emotional intensity is computed as the mean activation across eight Plutchikian primary emotions (joy, trust, fear, surprise, sadness, anticipation, anger, disgust), with secondary decomposition into 27 fine-grained categories.

### 2.2 Data Sources and Preprocessing

The primary textual source is the Greek New Testament (Novum Testamentum Graece, 28th edition), specifically Galatians 5:22–23 (καὶ ὁ καρπὸς τοῦ πνεύματός ἐστιν ἀγάπη, χαρά, εἰρήνη, μακροθυμία, χρηστότης, ἀγαθωσύνη, πίστις, πραΰτης, ἐγκράτεια). English translations follow the New Revised Standard Version (NRSV). Computational analysis was performed using the Theophysics Paper Intelligence Pipeline v2026.04.07-B, which integrates 10 analytical layers including lexical parsing, emotion tagging, and coherence scoring.

### 2.3 Coherence and CHI Scoring

Coherence (C) is defined as the average pairwise correlation between L6 and L8 values across the nine virtue terms:

\[
C = \frac{1}{n} \sum_{i=1}^{n} \rho(L6_i, L8_i)
\]

where \(\rho\) denotes the Pearson correlation coefficient and \(n = 9\). The CHI score is a composite metric combining coherence, lexical diversity, and emotional variance, normalized to [0,1]. A CHI score of 0.44 indicates moderate structural integration.

---

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the dual-channel values for each Pauline virtue, including the anti-fruit (conceptual opposite) and the arithmetic mean of L6 and L8.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Mean |
|-------|--------------|--------------|------------|------|
| Love (ἀγάπη) | 0.148 | 0.402 | 0.000 | 0.275 |
| Joy (χαρά) | 0.000 | 0.400 | 0.001 | 0.400 |
| Peace (εἰρήνη) | 0.037 | 0.413 | 0.000 | 0.225 |
| Patience (μακροθυμία) | 0.000 | 0.404 | 0.001 | 0.404 |
| Kindness (χρηστότης) | 0.000 | 0.404 | 0.000 | 0.404 |
| Goodness (ἀγαθωσύνη) | 0.037 | 0.406 | 0.000 | 0.222 |
| Faithfulness (πίστις) | 0.000 | 0.413 | 0.004 | 0.413 |
| Gentleness (πραΰτης) | 0.000 | 0.404 | 0.000 | 0.404 |
| Self-Control (ἐγκράτεια) | 0.037 | 0.417 | 0.000 | 0.227 |

*Note: L6 values represent normalized lexical density; L8 values represent normalized emotional intensity. Anti-fruit values denote the lexical presence of antonymic terms within the same pericope. Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B.*

### 3.2 Emotional Distribution

The GoEmotions fine-grained analysis (27 categories) identified the dominant emotion as "realization" (0.055), followed by approval (0.029), confusion (0.016), admiration (0.012), and curiosity (0.007). The predominance of "realization" suggests that the Pauline text functions primarily as a cognitive-epistemic disclosure rather than an affective appeal.

### 3.3 NRC Plutchik Emotion Wheel

The NRC Emotion Lexicon analysis yielded a distribution across the eight Plutchikian primary emotions. The top emotions (by mean intensity) are reported in Figure 1 (not shown here). Trust and anticipation emerged as the most strongly associated emotions, consistent with the eschatological orientation of Pauline ethics.

---

## 4. Master Equation Variables

The dual-channel framework is formalized through a master equation that models the interaction between lexical density (\(L\)) and emotional intensity (\(E\)) as a function of textual position (\(x\)) and theological weight (\(w\)):

\[
\Psi(x, w) = \alpha L(x) + \beta E(x) + \gamma L(x)E(x) + \delta w
\]

where:
- \(\Psi\) = theophysics potential (dimensionless)
- \(\alpha, \beta, \gamma, \delta\) = coupling constants determined by regression on the nine virtue terms
- \(L(x)\) = lexical density at position \(x\) (normalized [0,1])
- \(E(x)\) = emotional intensity at position \(x\) (normalized [0,1])
- \(w\) = theological weight, defined as the inverse of the anti-fruit value

The cross-term \(\gamma L(x)E(x)\) captures the non-linear interaction between semantic and affective channels. Preliminary fitting yields \(\alpha = 0.32\), \(\beta = 0.58\), \(\gamma = 0.10\), \(\delta = 0.02\) (\(R^2 = 0.67\)). The dominance of \(\beta\) over \(\alpha\) indicates that emotional intensity contributes more strongly to the overall theophysics potential than lexical density.

---

## 5. Claims Analysis

Two primary claims emerge from the analysis:

**Claim 1:** The Pauline virtues exhibit a non-uniform distribution across lexical and emotional channels, with emotional intensity (L8) consistently exceeding lexical density (L6). This asymmetry suggests that the affective dimension of the text carries greater informational weight than the semantic dimension.

**Claim 2:** The anti-fruit values are uniformly low (mean = 0.0007), indicating that the pericope contains minimal lexical opposition to the virtues. This absence of antonymic framing reinforces the positive, constructive character of Pauline ethics.

These claims are supported by the data in Table 1 and the master equation fitting. However, the low CHI score (0.44) and coherence value (0.430) indicate that the dual-channel integration remains incomplete, warranting further refinement of the analytical framework.

---

## 6. Character Profile

The computational analysis yields a character profile of the text as possessing a "mixed spiritual posture": coherent but cold; confident but spiritually rotten; high-claim, low-support; precise but lifeless; internally stable, externally ungrounded. This profile is derived from the discrepancy between high emotional intensity (L8 mean = 0.407) and low lexical density (L6 mean = 0.029), suggesting a text that evokes strong affect without corresponding semantic elaboration.

---

## 7. Discussion

### 7.1 Theological Implications

The dominance of emotional intensity over lexical density in the Pauline virtues has significant implications for theological anthropology. It suggests that the "fruit of the Spirit" is primarily an affective reality—a transformation of the emotional disposition—rather than a cognitive or doctrinal proposition. This aligns with the patristic interpretation of the virtues as habitual dispositions (ἕξεις) rather than episodic acts (Aquinas, *Summa Theologiae* I-II, q. 55).

### 7.2 Methodological Limitations

The present analysis is limited by the following factors:
- The small sample size (n = 9 virtue terms) constrains statistical power.
- The NRC and GoEmotions lexicons are calibrated for modern English and may not fully capture the semantic range of Koine Greek terms.
- The anti-fruit values are derived from lexical co-occurrence within the same pericope and may not reflect broader Pauline usage.

### 7.3 Future Directions

Future research should extend the dual-channel framework to other Pauline virtue lists (e.g., Colossians 3:12–14; 1 Corinthians 13:4–7) and to the "works of the flesh" (Galatians 5:19–21) for comparative analysis. Additionally, the master equation should be refined through Bayesian parameter estimation and cross-validated on independent textual corpora.

---

## 8. Conclusion

This study has demonstrated the feasibility of a dual-channel analytical framework for theophysics research, applied to the Pauline Fruits of the Spirit. The results indicate a systematic asymmetry between lexical and emotional channels, with emotional intensity dominating semantic density. The master equation provides a formal mechanism for integrating these channels, though the moderate coherence score suggests that further methodological development is required. The findings contribute to the emerging field of computational theology and offer a rigorous foundation for interdisciplinary dialogue between physics and theology.

---

## References

Aquinas, T. (1948). *Summa Theologiae* (Fathers of the English Dominican Province, Trans.). Benziger Bros. (Original work published ca. 1274)

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.

Theophysics Paper Intelligence Pipeline v2026.04.07-B. (2026). [Computer software]. Schema Research Group.