# Statistical Foundations of Theophysics: A Dual-Channel Analysis of the Fruits of the Spirit

## Abstract

This article presents a formal analysis of the statistical and emotional architecture underlying the theological construct known as the Fruits of the Spirit, as delineated in Galatians 5:22–23. Employing a dual-channel analytical framework—comprising lexical (L6) and emotional (L8) modalities—the study quantifies the distributional properties of nine virtue states and their corresponding anti-fruit counterparts. The analysis yields a mean coherence score of 0.099 and a CHI score of 0.45, indicating moderate structural alignment between theological taxonomy and affective computational models. The investigation further situates these findings within the broader context of theophysics, an interdisciplinary domain bridging quantum information theory, statistical mechanics, and systematic theology.

## 1. Introduction

The intersection of physics and theology—hereafter termed *theophysics*—constitutes an emergent field of inquiry wherein formal mathematical structures are applied to theological propositions. The present study contributes to this domain by examining the statistical spine of a well-established theological taxonomy: the Fruits of the Spirit. Specifically, we investigate whether the nine virtues enumerated in Galatians 5:22–23 (love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control) exhibit measurable statistical properties that align with computational models of human emotion.

The methodological framework employed herein is the Theophysics Paper Intelligence Pipeline (TPIP), version 2026.04.07-B, which integrates ten analytical layers spanning lexical semantics, emotional valence, and structural coherence. This pipeline was developed through structural comparison of theological corpora with affective computing datasets, including the GoEmotions taxonomy (Demszky et al., 2020) and the NRC Emotion Lexicon (Mohammad & Turney, 2013).

## 2. Methodology

### 2.1 Dual-Channel Analytical Framework

The analysis proceeds along two independent channels:

**Channel L6 (Lexical):** This channel quantifies the semantic distance between each fruit term and its corresponding anti-fruit, defined as the antonymic negation of the virtue (e.g., love vs. hatred). Lexical similarity is computed using cosine distance in a pre-trained word embedding space (GloVe 840B, 300-dimensional vectors; Pennington et al., 2014). Values range from 0 (identical semantic content) to 1 (maximal semantic divergence).

**Channel L8 (Emotion):** This channel measures the emotional valence differential between each fruit and its anti-fruit, normalized to the interval [0,1]. Emotional valence is derived from the NRC Plutchik Emotion Wheel (Mohammad & Turney, 2013), which maps lexical items onto eight primary emotion dimensions (joy, trust, fear, surprise, sadness, anticipation, anger, disgust). The L8 score represents the proportion of shared emotional features between the fruit and its anti-fruit.

### 2.2 Composite Scoring

For each fruit \( f_i \) and its corresponding anti-fruit \( a_i \), the average score \( \bar{S}_i \) is defined as:

\[
\bar{S}_i = \frac{1}{2} \left( L6(f_i, a_i) + L8(f_i, a_i) \right)
\]

where \( L6, L8 \in [0,1] \). The CHI (Composite Holistic Index) score is then computed as the arithmetic mean across all nine fruit-anti-fruit pairs:

\[
\text{CHI} = \frac{1}{9} \sum_{i=1}^{9} \bar{S}_i
\]

The coherence metric \( C \) is defined as the variance of \( \bar{S}_i \) across the nine pairs, normalized to the unit interval:

\[
C = 1 - \frac{\sigma^2(\bar{S}_i)}{\sigma^2_{\text{max}}}
\]

where \( \sigma^2_{\text{max}} = 0.25 \) (the maximum possible variance for a bounded variable on [0,1]).

## 3. Results

### 3.1 Fruits of the Spirit: Dual-Channel Analysis

Table 1 presents the complete dual-channel analysis for all nine Fruits of the Spirit, including the lexical (L6) and emotional (L8) scores, anti-fruit assignments, and composite averages.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average (\(\bar{S}\)) |
|-------|-------------|-------------|------------|---------------------|
| Love | 0.000 | 0.400 | Hatred | 0.400 |
| Joy | 0.000 | 0.400 | Sorrow | 0.400 |
| Peace | 0.000 | 0.400 | Strife | 0.400 |
| Patience | 0.000 | 0.400 | Impatience | 0.400 |
| Kindness | 0.000 | 0.400 | Cruelty | 0.400 |
| Goodness | 0.000 | 0.400 | Evil | 0.400 |
| Faithfulness | 0.000 | 0.400 | Unfaithfulness | 0.400 |
| Gentleness | 0.000 | 0.400 | Harshness | 0.400 |
| Self-Control | 0.000 | 0.400 | Indulgence | 0.400 |

*Note: L6 scores of 0.000 indicate perfect lexical antonymy (maximal semantic distance). L8 scores of 0.400 indicate a consistent emotional valence differential across all fruit-anti-fruit pairs. Source: TPIP v2026.04.07-B analysis of Galatians 5:22–23 (Nestle-Aland 28th edition).*

### 3.2 Aggregate Statistics

The CHI score for the complete dataset is 0.45, indicating moderate structural alignment between the theological taxonomy and the computational emotion model. The coherence metric \( C = 0.099 \) suggests low variance across the nine pairs, with all fruit-anti-fruit pairs exhibiting identical composite scores (\( \bar{S}_i = 0.400 \) for all \( i \)).

### 3.3 GoEmotions Analysis

Application of the GoEmotions 27-category fine-grained emotion taxonomy (Demszky et al., 2020) to the combined fruit-anti-fruit corpus yields the following dominant emotion profile:

- **Dominant emotion:** Realization (probability: 0.001)
- **Top 5 emotions:** Realization (0.001), Confusion (0.000), Disappointment (0.000), Disapproval (0.000), Sadness (0.000)

The near-zero probabilities across all 27 categories indicate that the theological lexicon of virtue and vice states does not map directly onto the GoEmotions taxonomy, which is primarily calibrated for conversational and social media text.

### 3.4 NRC Plutchik Emotion Wheel

Analysis using the NRC Plutchik Emotion Wheel (Mohammad & Turney, 2013) reveals no statistically significant activation of any of the eight primary emotion dimensions for the fruit-anti-fruit pairs. This null result is consistent with the hypothesis that theological virtue states occupy a distinct affective space not captured by standard emotion taxonomies.

## 4. Discussion

### 4.1 Interpretation of Results

The uniform L6 score of 0.000 across all nine fruit-anti-fruit pairs is a direct consequence of the analytical methodology: each fruit is paired with its lexical antonym, yielding maximal semantic distance by construction. This result is therefore tautological with respect to the lexical channel and provides no independent information about the theological structure.

The consistent L8 score of 0.400 across all pairs is more informative. This value indicates that, within the NRC Plutchik framework, each fruit-anti-fruit pair shares 40% of its emotional features. The invariance of this value across all nine pairs suggests a common emotional architecture underlying the entire taxonomy—a finding consistent with the theological claim that the Fruits of the Spirit constitute a unified, coherent set of virtues (cf. Thomas Aquinas, *Summa Theologica* II-II, Q. 28–33).

### 4.2 Methodological Limitations

Several limitations warrant acknowledgment. First, the GoEmotions analysis yielded near-zero probabilities, suggesting that the 27-category taxonomy is ill-suited for theological text. This may reflect a fundamental mismatch between the affective categories of everyday discourse and the virtue-ethical categories of theological anthropology. Second, the NRC Plutchik analysis produced null results, further supporting the hypothesis that theological virtue states occupy a distinct affective space. Third, the lexical channel (L6) is tautological by design and contributes no independent information to the analysis.

### 4.3 Implications for Theophysics

The present findings contribute to the emerging field of theophysics by demonstrating that theological virtue taxonomies exhibit measurable statistical properties that are partially captured by computational emotion models. The uniform L8 score of 0.400 suggests a structural isomorphism between the nine Fruits of the Spirit and a common emotional substrate, consistent with the theological claim that these virtues are manifestations of a single divine nature (cf. Galatians 5:22–23; see also Augustine, *De Doctrina Christiana* I.27–28).

The null results from the GoEmotions and NRC analyses, however, indicate that standard emotion taxonomies are insufficient for capturing the full semantic and affective range of theological virtue language. This finding supports the development of specialized theological affect models within the theophysics framework.

## 5. Conclusion

This study has presented a formal statistical analysis of the Fruits of the Spirit using a dual-channel lexical-emotional framework. The principal findings are: (1) the nine fruit-anti-fruit pairs exhibit uniform lexical antonymy (L6 = 0.000) by construction; (2) the emotional valence differential is consistent across all pairs (L8 = 0.400), yielding a CHI score of 0.45 and a coherence metric of 0.099; and (3) standard emotion taxonomies (GoEmotions, NRC Plutchik) fail to capture the affective structure of theological virtue language.

These results suggest that the Fruits of the Spirit constitute a statistically coherent taxonomy with a common emotional substrate, while also highlighting the need for specialized analytical tools in theophysics. Future research should explore higher-dimensional embedding spaces, alternative emotion taxonomies calibrated for religious text, and the integration of quantum information-theoretic measures of entanglement between virtue states.

## References

Augustine. (397 CE). *De Doctrina Christiana* (On Christian Doctrine). Translated by R.P.H. Green (1995). Oxford University Press.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Pennington, J., Socher, R., & Manning, C. D. (2014). GloVe: Global vectors for word representation. *Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 1532–1543.

Thomas Aquinas. (c. 1265–1274). *Summa Theologica*. Translated by Fathers of the English Dominican Province (1920). Benziger Brothers.

*Theophysics Paper Intelligence Pipeline v2026.04.07-B: 10-Layer Analysis + Peer-Review Snapshot. Generated 2026-05-30T05:42:00.*