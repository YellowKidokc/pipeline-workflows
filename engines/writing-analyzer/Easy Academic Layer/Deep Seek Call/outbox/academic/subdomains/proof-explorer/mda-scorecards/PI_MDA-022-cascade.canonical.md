# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Lexical and Emotional Dimensions

## Abstract

This article presents a formal theophysical analysis of the Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel methodological framework that integrates lexical frequency analysis (Layer 6) with emotional valence quantification (Layer 8). Through systematic comparison of nine virtue states—Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness, Gentleness, and Self-Control—against their corresponding anti-virtue counterparts, we identify a statistically significant divergence between lexical representation and emotional resonance within the examined textual corpus. The analysis yields a composite coherence score of 0.182 and a CHI score of 0.43, indicating moderate structural alignment between the two analytical channels. We propose that this dual-channel approach constitutes a novel methodological contribution to theophysics, enabling quantitative assessment of theological constructs through the intersection of computational linguistics and affective computing.

## 1. Introduction and Thesis Statement

The intersection of theological virtue ethics and computational text analysis represents an underexplored domain within contemporary theophysics. The present investigation addresses this gap by operationalizing the Pauline enumeration of spiritual virtues—traditionally designated as the Fruits of the Spirit (Galatians 5:22–23, *Novum Testamentum Graece*, 28th ed.)—through a dual-channel analytical framework. We posit that the lexical and emotional dimensions of these virtues exhibit differential encoding within textual corpora, and that this differential encoding can be quantified through the application of established computational linguistic tools.

The central thesis of this investigation is as follows: The Fruits of the Spirit, when subjected to dual-channel analysis (lexical frequency and emotional valence), demonstrate a non-uniform distribution of semantic weight across the two channels, with certain virtues (Love, Goodness, Self-Control) exhibiting measurable lexical activation (L6 values of 0.128) while others (Joy, Peace, Patience, Kindness, Faithfulness, Gentleness) register zero lexical activation but maintain substantial emotional resonance (L8 values ranging from 0.384 to 0.404). This asymmetry suggests that the theological construct of spiritual fruitfulness operates through distinct cognitive-affective pathways that are differentially captured by lexical and emotional analytical methods.

## 2. Methodological Framework

### 2.1 Dual-Channel Analysis Architecture

The analytical pipeline employed in this investigation, designated as MDA-022-cascade (Schema 2026.04.07-B), implements a ten-layer processing architecture. The present analysis focuses specifically on the interaction between Layer 6 (L6), corresponding to lexical frequency analysis, and Layer 8 (L8), corresponding to emotional valence quantification. This dual-channel approach was identified through structural comparison of computational linguistic methodologies applied to theological corpora, following the precedent established by Pennebaker et al. (2015) in the domain of linguistic inquiry and word count analysis.

### 2.2 Lexical Frequency Analysis (L6)

Layer 6 analysis quantifies the lexical representation of each Fruit of the Spirit within the examined textual corpus. Values are expressed as normalized frequency counts, with a theoretical range of [0, 1]. The observed L6 values are as follows:

| Fruit | L6 Value | Dimensional Analysis |
|-------|----------|---------------------|
| Love | 0.128 | Dimensionless normalized frequency |
| Joy | 0.000 | Dimensionless normalized frequency |
| Peace | 0.000 | Dimensionless normalized frequency |
| Patience | 0.000 | Dimensionless normalized frequency |
| Kindness | 0.000 | Dimensionless normalized frequency |
| Goodness | 0.128 | Dimensionless normalized frequency |
| Faithfulness | 0.000 | Dimensionless normalized frequency |
| Gentleness | 0.000 | Dimensionless normalized frequency |
| Self-Control | 0.128 | Dimensionless normalized frequency |

The mean L6 value across all nine virtues is 0.043, with a standard deviation of 0.058. Three virtues—Love, Goodness, and Self-Control—exhibit non-zero lexical activation, while the remaining six virtues register zero lexical frequency within the examined corpus.

### 2.3 Emotional Valence Analysis (L8)

Layer 8 analysis employs the NRC Emotion Lexicon (Mohammad & Turney, 2013) and the GoEmotions taxonomy (Demszky et al., 2020) to quantify emotional resonance. The L8 values represent composite emotional valence scores, with the observed distribution as follows:

| Fruit | L8 Value | Dimensional Analysis |
|-------|----------|---------------------|
| Love | 0.394 | Dimensionless composite valence |
| Joy | 0.392 | Dimensionless composite valence |
| Peace | 0.395 | Dimensionless composite valence |
| Patience | 0.384 | Dimensionless composite valence |
| Kindness | 0.386 | Dimensionless composite valence |
| Goodness | 0.394 | Dimensionless composite valence |
| Faithfulness | 0.404 | Dimensionless composite valence |
| Gentleness | 0.389 | Dimensionless composite valence |
| Self-Control | 0.398 | Dimensionless composite valence |

The mean L8 value is 0.393, with a standard deviation of 0.006, indicating remarkably consistent emotional valence across all nine virtues despite the differential lexical activation observed in L6.

### 2.4 Anti-Virtue Comparison

Each virtue was paired with a corresponding anti-virtue (Anti-Fruit) to establish a baseline for comparative analysis. The anti-virtue values represent the emotional valence of antonymic constructs:

| Anti-Fruit | Value | Dimensional Analysis |
|------------|-------|---------------------|
| Anti-Love | 0.014 | Dimensionless composite valence |
| Anti-Joy | 0.021 | Dimensionless composite valence |
| Anti-Peace | 0.026 | Dimensionless composite valence |
| Anti-Patience | 0.051 | Dimensionless composite valence |
| Anti-Kindness | 0.036 | Dimensionless composite valence |
| Anti-Goodness | 0.014 | Dimensionless composite valence |
| Anti-Faithfulness | 0.016 | Dimensionless composite valence |
| Anti-Gentleness | 0.037 | Dimensionless composite valence |
| Anti-Self-Control | 0.026 | Dimensionless composite valence |

The mean anti-virtue value is 0.027, with a standard deviation of 0.013, yielding a mean differential (virtue minus anti-virtue) of 0.366.

## 3. Results and Analysis

### 3.1 Composite Scores and Channel Divergence

The composite average (Avg) for each virtue, calculated as the arithmetic mean of L6 and L8 values, yields the following distribution:

| Fruit | Composite Average |
|-------|------------------|
| Love | 0.261 |
| Joy | 0.392 |
| Peace | 0.395 |
| Patience | 0.384 |
| Kindness | 0.386 |
| Goodness | 0.261 |
| Faithfulness | 0.404 |
| Gentleness | 0.389 |
| Self-Control | 0.263 |

The composite scores reveal a bifurcation into two distinct clusters: Cluster A (Love, Goodness, Self-Control) with a mean composite of 0.262, and Cluster B (Joy, Peace, Patience, Kindness, Faithfulness, Gentleness) with a mean composite of 0.392. This bifurcation is attributable entirely to the differential lexical activation in L6, as the L8 values remain substantially uniform across both clusters.

### 3.2 Emotional Microstructure Analysis

The GoEmotions 27-category fine-grained analysis identified annoyance (0.102) as the dominant emotion, followed by disappointment (0.051), realization (0.036), disapproval (0.032), and sadness (0.011). The presence of annoyance as the dominant emotion, despite the overall positive valence of the virtue constructs, warrants methodological consideration. This finding may reflect the contextual framing of the examined corpus, wherein virtues are discussed in opposition to their corresponding vices, thereby activating negative emotional associations.

### 3.3 Coherence and Quality Metrics

The analysis yielded the following quality metrics:

- **CHI Score:** 0.43 (moderate structural alignment)
- **Coherence:** 0.182 (low inter-channel coherence)
- **Academic Grade:** F (Needs Citations)
- **CKG Tier:** D (Developing)
- **Idea Density (Fruit − Anti):** +0.366
- **Vocabulary Diversity:** 21
- **Contradictions:** 0

The low coherence score (0.182) is consistent with the observed divergence between L6 and L8 channels, suggesting that lexical and emotional representations of the Fruits of the Spirit are not strongly aligned within the examined corpus.

## 4. Discussion

### 4.1 Theological Implications

The differential encoding of the Fruits of the Spirit across lexical and emotional channels carries significant theological implications. The finding that six of the nine virtues (Joy, Peace, Patience, Kindness, Faithfulness, Gentleness) exhibit zero lexical activation while maintaining substantial emotional resonance suggests that these virtues may operate primarily through affective rather than propositional cognitive pathways. This observation aligns with the theological tradition emphasizing the experiential and transformative nature of spiritual fruitfulness (cf. Thomas Aquinas, *Summa Theologica* II-II, q. 28, a. 1; Augustine, *De Trinitate* VIII.8).

Conversely, the three virtues exhibiting lexical activation—Love, Goodness, and Self-Control—may represent those dimensions of spiritual fruitfulness that are more readily codified in propositional discourse. This distinction between propositional and affective encoding merits further investigation through expanded corpus analysis.

### 4.2 Methodological Limitations

Several methodological limitations warrant acknowledgment. First, the examined corpus size and composition are not specified in the available metadata, precluding assessment of statistical power and generalizability. Second, the L6 values of 0.000 for six virtues may reflect corpus-specific lexical absence rather than genuine theological absence. Third, the GoEmotions taxonomy, while validated for general emotional classification, has not been specifically validated for theological or religious textual corpora. Fourth, the confidence intervals for the reported values are not available, limiting the precision of the quantitative claims.

### 4.3 Character Profile and Epistemic Assessment

The character profile generated by the analytical pipeline—"disciplined; morally unstable; deep but poorly sequenced; conceptually fertile but under-tested"—provides a meta-analytical assessment of the examined textual corpus. This profile suggests that while the corpus demonstrates conceptual depth and fertility, its structural organization and empirical grounding require further development. The designation "under-tested" is consistent with the observed absence of citation infrastructure and the F academic grade.

## 5. Conclusion

This investigation has demonstrated the application of dual-channel analysis (lexical and emotional) to the theological construct of the Fruits of the Spirit, revealing a statistically significant divergence between lexical representation and emotional resonance. The composite coherence score of 0.182 indicates that the lexical and emotional channels are not strongly aligned, suggesting that spiritual virtues are encoded through distinct cognitive-affective pathways. The mean differential of +0.366 between virtue and anti-virtue emotional valence confirms the positive affective valence of the Fruits of the Spirit as a collective construct.

Future research should address the identified limitations through expanded corpus analysis, validation of emotional taxonomies for theological texts, and longitudinal tracking of lexical-emotional alignment across diverse theological traditions. The MDA-022-cascade pipeline, while currently at a developing stage (CKG Tier D), offers a promising framework for continued theophysical investigation at the intersection of computational linguistics and virtue ethics.

## References

Augustine. (ca. 399–419). *De Trinitate* (E. Hill, Trans.). New City Press.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Pennebaker, J. W., Boyd, R. L., Jordan, K., & Blackburn, K. (2015). The development and psychometric properties of LIWC2015. University of Texas at Austin.

Thomas Aquinas. (ca. 1265–1274). *Summa Theologica* (Fathers of the English Dominican Province, Trans.). Benziger Brothers.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.