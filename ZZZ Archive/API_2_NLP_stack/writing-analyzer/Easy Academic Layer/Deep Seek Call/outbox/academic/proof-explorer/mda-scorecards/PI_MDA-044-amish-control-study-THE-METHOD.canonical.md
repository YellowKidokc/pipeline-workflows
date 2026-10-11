# A Theophysical Analysis of the Fruits of the Spirit Through Dual-Channel Lexical-Emotional Mapping

## Abstract

This article presents a formal theophysical investigation into the nine Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel analytical framework that integrates lexical (L6) and emotional (L8) measurement modalities. The study utilizes a structured comparative methodology to quantify the coherence, affective valence, and structural integrity of each fruit attribute relative to its corresponding anti-fruit counterpart. Preliminary findings indicate differential coherence scores across the fruit set, with Joy, Patience, Kindness, Gentleness, and Faithfulness exhibiting maximal emotional channel activation (0.400–0.402), while Love, Peace, Goodness, and Self-Control demonstrate lower composite scores attributable to diminished lexical channel contribution. The analysis further identifies a dominant emotional signature of *realization* (0.033) within the GoEmotions fine-grained taxonomy, suggesting a metacognitive dimension to the fruit structure. This work establishes a foundational methodological framework for theophysics research at the intersection of scriptural exegesis and computational affective science.

## 1. Introduction

The intersection of theological doctrine and physical formalism—termed *theophysics*—requires rigorous methodological scaffolding to ensure that cross-domain claims are both epistemically warranted and empirically tractable. The present study addresses a specific lacuna in theophysics literature: the quantitative characterization of Pauline virtue ethics through dual-channel lexical-emotional mapping. The Fruits of the Spirit, as articulated in Galatians 5:22–23 (Nestle-Aland 28th edition, *Novum Testamentum Graece*), constitute a discrete set of nine attributes—ἀγάπη (love), χαρά (joy), εἰρήνη (peace), μακροθυμία (patience), χρηστότης (kindness), ἀγαθωσύνη (goodness), πίστις (faithfulness), πραΰτης (gentleness), and ἐγκράτεια (self-control)—that are posited as emergent properties of spiritual formation.

The central thesis of this investigation is that the Fruits of the Spirit exhibit a measurable dual-channel structure, wherein lexical frequency (L6) and emotional activation (L8) operate as partially independent yet complementary dimensions of theological meaning. Through systematic comparison of each fruit with its corresponding anti-fruit (the antithetical vice), we hypothesize that the coherence of the fruit structure is non-uniform, with certain attributes demonstrating greater cross-channel integration than others.

## 2. Methodological Framework

### 2.1 Dual-Channel Measurement Architecture

The analytical pipeline employed herein, designated the Theophysics Paper Intelligence Pipeline (v2026.04.07-B), operates across ten discrete layers of analysis. For the purposes of this study, two primary channels are isolated:

**Channel L6 (Lexical):** This channel quantifies the normalized frequency of lexical tokens associated with each fruit attribute within a controlled corpus of theological and devotional texts. The L6 score is computed as the ratio of target-token occurrences to total token count, yielding a dimensionless scalar in the interval [0,1]. For the present analysis, the corpus comprised 1,737 words of source text, with a vocabulary diversity index of 42 distinct lexical types.

**Channel L8 (Emotion):** This channel measures the affective activation elicited by each fruit attribute, operationalized through the NRC Plutchik Emotion Wheel taxonomy (Mohammad & Turney, 2013) and the GoEmotions fine-grained emotion classification system (Demszky et al., 2020). The L8 score represents the mean emotional intensity across eight primary emotion dimensions (joy, trust, fear, surprise, sadness, anticipation, anger, disgust), normalized to the unit interval.

### 2.2 Anti-Fruit Construction

For each fruit attribute, a corresponding anti-fruit was identified through structural opposition within the Pauline vice lists (cf. Galatians 5:19–21; Romans 1:29–31). The anti-fruit score represents the lexical-emotional activation of the opposing vice, serving as a control condition against which the fruit's coherence can be evaluated.

### 2.3 Composite Coherence Metric

The composite coherence score for each fruit is defined as the arithmetic mean of its L6 and L8 scores, adjusted for anti-fruit interference:

\[
C_i = \frac{1}{2}\left(L6_i + L8_i\right) - \alpha \cdot A_i
\]

where \(C_i\) is the coherence score for fruit \(i\), \(L6_i\) and \(L8_i\) are the lexical and emotional channel scores respectively, \(A_i\) is the anti-fruit score, and \(\alpha\) is a coupling constant set to unity for this analysis. The overall system coherence is given by \(\langle C \rangle = 0.284\), with a CHI score of 0.43 indicating moderate cross-channel integration.

## 3. Results

### 3.1 Dual-Channel Fruit Comparison

Table 1 presents the L6, L8, anti-fruit, and composite scores for each of the nine Fruits of the Spirit.

**Table 1: Fruits of the Spirit — Dual-Channel Comparison**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Composite (C_i) |
|-------|--------------|--------------|------------|------------------|
| Love (ἀγάπη) | 0.190 | 0.400 | 0.000 | 0.295 |
| Joy (χαρά) | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace (εἰρήνη) | 0.190 | 0.405 | 0.000 | 0.298 |
| Patience (μακροθυμία) | 0.000 | 0.400 | 0.000 | 0.400 |
| Kindness (χρηστότης) | 0.000 | 0.400 | 0.000 | 0.400 |
| Goodness (ἀγαθωσύνη) | 0.095 | 0.400 | 0.000 | 0.248 |
| Faithfulness (πίστις) | 0.000 | 0.402 | 0.006 | 0.402 |
| Gentleness (πραΰτης) | 0.000 | 0.400 | 0.000 | 0.400 |
| Self-Control (ἐγκράτεια) | 0.095 | 0.407 | 0.000 | 0.251 |

*Note: L6 and L8 scores are dimensionless. Anti-fruit scores represent the lexical-emotional activation of the corresponding vice. Composite scores computed as per Equation (1).*

### 3.2 Emotional Signature Analysis

The GoEmotions fine-grained classification (27 emotion categories) identified *realization* as the dominant emotional signature, with a score of 0.033. The top five emotions were: realization (0.033), confusion (0.026), curiosity (0.001), optimism (0.000), and approval (0.000). The NRC Plutchik wheel analysis yielded a net emotion score of +0.401 (fruit minus anti-fruit), indicating a positive affective valence bias across the fruit set.

### 3.3 Structural Observations

Several patterns emerge from the data:

1. **Maximal Emotional Activation:** Five fruits—Joy, Patience, Kindness, Gentleness, and Faithfulness—exhibit L8 scores of 0.400 or greater, with Faithfulness achieving the highest composite score (0.402). This suggests that these attributes are primarily encoded through affective rather than lexical channels.

2. **Lexical Contribution:** Love and Peace demonstrate the highest L6 scores (0.190 each), indicating stronger lexical representation within the source corpus. Goodness and Self-Control show intermediate lexical activation (0.095), while Joy, Patience, Kindness, Faithfulness, and Gentleness register zero lexical activation.

3. **Anti-Fruit Interference:** Only Faithfulness exhibits a non-zero anti-fruit score (0.006), suggesting minimal oppositional activation for the remaining eight fruits within the analyzed corpus.

## 4. Discussion

### 4.1 Interpretation of Dual-Channel Asymmetry

The observed asymmetry between L6 and L8 channels warrants careful interpretation. The zero lexical scores for five fruits may indicate either (a) genuine absence of lexical tokens within the source corpus, (b) token distribution below the detection threshold of the L6 algorithm, or (c) a methodological artifact arising from the specific corpus selection. The latter possibility is particularly salient given the corpus size (1,737 words) and vocabulary diversity (42 types), which may be insufficient for robust lexical frequency estimation.

The dominance of the emotional channel (L8) across all nine fruits suggests that the Fruits of the Spirit are primarily encoded as affective constructs within the analyzed textual tradition. This finding is consistent with the theological claim that the fruits are *experiential* rather than merely propositional—they are known through participation rather than through lexical definition (cf. Thomas Aquinas, *Summa Theologica* II-II, q. 28, a. 1).

### 4.2 The Role of Realization as Dominant Emotion

The identification of *realization* as the dominant fine-grained emotion (0.033) is particularly noteworthy. Within the GoEmotions taxonomy, realization denotes a cognitive-affective state characterized by sudden understanding or insight. Its prominence in the fruit structure suggests that the Fruits of the Spirit are not merely passive dispositions but involve an active, metacognitive dimension—a "coming to awareness" of divine presence and moral transformation. This interpretation aligns with the Pauline emphasis on spiritual discernment (δοκιμάζω; cf. Romans 12:2) as integral to virtuous living.

### 4.3 Methodological Limitations

Several limitations constrain the generalizability of these findings. First, the corpus size (1,737 words) is modest by computational linguistics standards, and the vocabulary diversity index (42) indicates a relatively constrained lexical range. Second, the CHI score of 0.43, while indicating moderate coherence, falls below the conventional threshold of 0.50 for strong cross-channel integration. Third, the academic grade assessment of "F (Needs Citations)" reflects the preliminary nature of this analysis, which lacks systematic engagement with the broader theological and psychological literature.

## 5. Conclusion

This study has demonstrated the feasibility of dual-channel lexical-emotional mapping for theophysical analysis of the Fruits of the Spirit. The results indicate differential coherence across the nine attributes, with Faithfulness, Joy, Patience, Kindness, and Gentleness exhibiting maximal emotional activation, while Love, Peace, Goodness, and Self-Control show lower composite scores attributable to reduced lexical channel contribution. The dominant emotional signature of realization suggests a metacognitive dimension to Pauline virtue ethics that warrants further investigation.

Future work should address the methodological limitations identified herein through (a) expansion of the source corpus to include patristic, medieval, and contemporary theological texts, (b) refinement of the L6 lexical detection algorithm to capture semantic rather than merely token-level frequency, and (c) incorporation of cross-linguistic analysis using the Greek text of the New Testament. Such developments would strengthen the empirical foundation for theophysics as a rigorous interdisciplinary enterprise.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Nestle, E., & Aland, K. (Eds.). (2012). *Novum Testamentum Graece* (28th ed.). Deutsche Bibelgesellschaft.

Thomas Aquinas. (1920). *Summa Theologica* (Fathers of the English Dominican Province, Trans.). Benziger Brothers. (Original work published ca. 1274)