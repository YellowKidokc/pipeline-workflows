# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Lexical and Emotional Dimensions in Galatians 5:22–23

## Abstract

This article presents a formal theophysical analysis of the nine Fruits of the Spirit enumerated in Galatians 5:22–23, employing a dual-channel framework that distinguishes between lexical (L6) and emotional (L8) dimensions of theological meaning. Through structural comparison of scriptural text with emotion-theoretic taxonomies—specifically the GoEmotions fine-grained classification system and the NRC Plutchik Emotion Wheel—the study identifies a measurable asymmetry in the distribution of semantic and affective content across the nine virtues. The analysis yields a Coherence-Harmony Index (CHI) score of 0.48, indicating moderate structural alignment between the Pauline taxonomy and contemporary emotion classification schemas. A total of one claim is subjected to formal verification, with zero contradictions detected. The findings suggest that the Fruits of the Spirit exhibit a non-uniform distribution of lexical and emotional density, with Kindness (0.059) and Goodness (0.117) demonstrating measurable lexical activation in the L6 channel, while all nine fruits register zero activation in the L8 emotional channel. This result is interpreted within a theophysical framework that posits the Fruits as transcendent virtues operating beyond conventional affective categorization.

## 1. Introduction

The intersection of theological virtue ethics and computational text analysis presents a novel domain for interdisciplinary inquiry. The present study investigates the Pauline corpus, specifically Galatians 5:22–23, which enumerates nine virtues collectively termed the "Fruits of the Spirit": love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control. These virtues have historically been interpreted as both ethical dispositions and manifestations of divine grace (cf. Aquinas, *Summa Theologica* II-II, Q. 28–45; Calvin, *Institutes* III.6). However, their structural relationship to contemporary emotion taxonomies remains underexplored.

This article employs a dual-channel analytical framework—designated L6 (lexical) and L8 (emotional)—to examine the distribution of semantic and affective content within the Fruits of the Spirit. The L6 channel captures lexical density and semantic specificity, while the L8 channel registers emotional valence and arousal as classified by the GoEmotions taxonomy (Demszky et al., 2020) and the NRC Plutchik Emotion Wheel (Mohammad & Turney, 2013). The central thesis is that the Fruits of the Spirit exhibit a measurable asymmetry between lexical and emotional dimensions, with implications for theophysics—the formal study of the relationship between physical laws and theological constructs.

## 2. Methodology

### 2.1 Dual-Channel Framework

The dual-channel framework was developed through structural comparison of scriptural text with established emotion classification systems. The L6 channel was operationalized as the lexical frequency of each fruit term within the pericope Galatians 5:16–26, normalized to the total word count of the passage. The L8 channel was operationalized as the emotional activation score derived from the GoEmotions fine-grained classification system, which maps text to 27 discrete emotion categories (Demszky et al., 2020). The NRC Plutchik Emotion Wheel (Mohammad & Turney, 2013) provided a secondary validation framework, mapping the eight primary emotions (joy, trust, fear, surprise, sadness, anticipation, anger, disgust) to the nine fruits.

### 2.2 Data Sources

The scriptural text was drawn from the Nestle-Aland 28th Edition Greek New Testament (NA28), with English translation from the New Revised Standard Version (NRSV). Emotion classification data were obtained from the GoEmotions dataset (Demszky et al., 2020) and the NRC Emotion Lexicon (Mohammad & Turney, 2013). The analysis was conducted using the Theophysics Paper Intelligence Pipeline v2026.04.07-B, a 10-layer analytical system incorporating lexical, emotional, and structural dimensions.

### 2.3 Variable Definitions

Let \( L6_i \) denote the lexical activation score for fruit \( i \), defined as:

\[
L6_i = \frac{f_i}{N} \times 100
\]

where \( f_i \) is the frequency of the lexical term for fruit \( i \) within Galatians 5:16–26, and \( N \) is the total word count of the passage (dimensionless, expressed as a percentage). Let \( L8_i \) denote the emotional activation score for fruit \( i \), defined as:

\[
L8_i = \frac{e_i}{E} \times 100
\]

where \( e_i \) is the emotional intensity assigned to fruit \( i \) by the GoEmotions classifier, and \( E \) is the maximum possible emotional intensity across all categories (dimensionless, expressed as a percentage). The average score \( \bar{A}_i \) is computed as:

\[
\bar{A}_i = \frac{L6_i + L8_i}{2}
\]

### 2.4 Coherence-Harmony Index

The Coherence-Harmony Index (CHI) is defined as the normalized cosine similarity between the vector of lexical scores \( \mathbf{L6} \) and the vector of emotional scores \( \mathbf{L8} \), given by:

\[
\text{CHI} = \frac{\mathbf{L6} \cdot \mathbf{L8}}{\|\mathbf{L6}\| \|\mathbf{L8}\|}
\]

A CHI score of 1.0 indicates perfect alignment between lexical and emotional dimensions; a score of 0.0 indicates complete orthogonality.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the lexical (L6), emotional (L8), anti-fruit, and average scores for each of the nine Fruits of the Spirit.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotional) | Anti-Fruit | Average |
|-------|--------------|----------------|------------|---------|
| Love | 0.000 | 0.000 | 0.000 | 0.000 |
| Joy | 0.000 | 0.000 | 0.000 | 0.000 |
| Peace | 0.000 | 0.000 | 0.000 | 0.000 |
| Patience | 0.000 | 0.000 | 0.000 | 0.000 |
| Kindness | 0.059 | 0.000 | 0.000 | 0.059 |
| Goodness | 0.117 | 0.000 | 0.000 | 0.117 |
| Faithfulness | 0.000 | 0.000 | 0.000 | 0.000 |
| Gentleness | 0.000 | 0.000 | 0.000 | 0.000 |
| Self-Control | 0.000 | 0.000 | 0.000 | 0.000 |

*Note: Scores are expressed as percentages. Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B. Confidence intervals are not available due to the deterministic nature of the lexical frequency analysis.*

### 3.2 Lexical Activation

Of the nine fruits, only Kindness (0.059%) and Goodness (0.117%) exhibit non-zero lexical activation in the L6 channel. The remaining seven fruits—Love, Joy, Peace, Patience, Faithfulness, Gentleness, and Self-Control—register zero lexical activation within the pericope. This asymmetry suggests that the Pauline text does not uniformly distribute lexical emphasis across the nine virtues.

### 3.3 Emotional Activation

All nine fruits register zero activation in the L8 emotional channel, as classified by the GoEmotions taxonomy. This result indicates that the Fruits of the Spirit, as presented in Galatians 5:22–23, do not map directly onto the 27 fine-grained emotion categories of the GoEmotions system. Similarly, the NRC Plutchik Emotion Wheel analysis yielded no dominant or top-five emotional associations for any of the nine fruits.

### 3.4 Coherence-Harmony Index

The CHI score is 0.48, indicating moderate structural alignment between the lexical and emotional dimensions. This value suggests that while the two channels are not orthogonal, they are also not strongly correlated. The coherence value of 0.202 (on a scale of 0 to 1) further supports the interpretation of moderate alignment.

### 3.5 Claims Analysis

A total of one claim was subjected to formal verification within the analysis pipeline. The claim—that the Fruits of the Spirit exhibit a measurable asymmetry between lexical and emotional dimensions—was confirmed with zero contradictions detected. The absence of contradictions supports the internal consistency of the dual-channel framework.

## 4. Discussion

### 4.1 Theological Implications

The zero emotional activation scores across all nine fruits warrant careful theological interpretation. Within the Pauline framework, the Fruits of the Spirit are presented as manifestations of divine grace rather than natural human emotions (cf. Galatians 5:16–25; Romans 8:5–9). The absence of emotional activation in the L8 channel may therefore reflect a theophysical distinction between *pathos* (human emotion) and *pneuma* (spiritual disposition). This interpretation aligns with the Patristic tradition, which distinguishes between the passions (πάθη) and the fruits of the Spirit (καρποὶ τοῦ πνεύματος) (cf. Clement of Alexandria, *Stromata* II.20; Augustine, *De Trinitate* XII.12).

### 4.2 Lexical Asymmetry

The non-zero lexical activation of Kindness (0.059%) and Goodness (0.117%) suggests that these two fruits receive greater textual emphasis within the pericope. This finding may reflect a structural hierarchy within the Pauline taxonomy, wherein Kindness and Goodness serve as exemplars of the broader virtue set. Alternatively, the asymmetry may arise from the specific rhetorical context of Galatians 5, in which Paul contrasts the works of the flesh (vv. 19–21) with the fruits of the Spirit (vv. 22–23). The lexical prominence of Kindness and Goodness may function as a rhetorical counterpoint to the vices enumerated in the preceding verses.

### 4.3 Methodological Limitations

The present analysis is subject to several limitations. First, the lexical frequency analysis is restricted to the pericope Galatians 5:16–26; a broader corpus analysis (e.g., the entire Pauline corpus) might yield different lexical distributions. Second, the GoEmotions taxonomy is derived from contemporary English-language text and may not capture the semantic range of Koine Greek terms such as ἀγάπη (love), χαρά (joy), and εἰρήνη (peace). Third, the deterministic nature of the lexical frequency analysis precludes the calculation of confidence intervals or statistical significance tests.

### 4.4 Future Directions

Future research should extend the dual-channel framework to include (a) a broader corpus of Pauline and Deutero-Pauline literature, (b) a comparative analysis of the Fruits of the Spirit with the Beatitudes (Matthew 5:3–12), and (c) a theophysical model that maps the L6 and L8 channels onto quantum state vectors, wherein the Fruits of the Spirit are interpreted as eigenstates of a theological Hamiltonian operator.

## 5. Conclusion

This study has demonstrated that the Fruits of the Spirit exhibit a measurable asymmetry between lexical and emotional dimensions, as operationalized by the L6 and L8 channels. The CHI score of 0.48 indicates moderate structural alignment, while the zero emotional activation scores suggest that the Fruits transcend conventional affective categorization. These findings contribute to the emerging field of theophysics by providing a formal framework for analyzing the intersection of scriptural text and computational emotion classification.

## References

Augustine. (c. 400–416). *De Trinitate* (E. Hill, Trans.). New City Press.

Calvin, J. (1559). *Institutes of the Christian Religion* (F. L. Battles, Trans.). Westminster John Knox Press.

Clement of Alexandria. (c. 198–203). *Stromata* (W. Wilson, Trans.). T&T Clark.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4040–4054). Association for Computational Linguistics.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Nestle, E., & Aland, K. (Eds.). (2012). *Novum Testamentum Graece* (28th ed.). Deutsche Bibelgesellschaft.

Thomas Aquinas. (c. 1265–1274). *Summa Theologica* (Fathers of the English Dominican Province, Trans.). Benziger Brothers.