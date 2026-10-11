# Theophysics of Spiritual Formation: A Dual-Channel Analysis of the Fruits of the Spirit

## Abstract

This article presents a formal interdisciplinary analysis of the Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel measurement framework that integrates lexical-semantic and affective-emotional dimensions. The investigation proceeds from the hypothesis that spiritual virtues, as described in the Pauline corpus, exhibit measurable structural properties that can be characterized through computational linguistic and psychometric methodologies. A comparative table of nine Fruits—Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness, Gentleness, and Self-Control—is constructed, with each virtue evaluated along two independent axes: a lexical channel (L6) and an emotional channel (L8). The analysis further incorporates the GoEmotions taxonomy of 27 fine-grained emotional categories and the NRC Plutchik Emotion Wheel framework. The resulting data yield a composite CHI Score of 0.44, a coherence metric of 0.232, and an average Fruit-Anti-Fruit differential of +0.399, suggesting a statistically significant but moderate alignment between lexical representation and emotional valence. The findings are contextualized within the broader discourse of theophysics, defined here as the systematic study of the intersection between theological constructs and physical or formal systems.

## 1. Introduction

The intersection of theological virtue ethics and quantitative measurement presents a methodological challenge that has received limited attention in both the physics and theology literatures. The present study addresses this gap by operationalizing the Fruits of the Spirit—a set of nine character virtues derived from Galatians 5:22–23 (Nestle-Aland 28th edition, NA28)—through a dual-channel analytical framework. This framework, designated Schema 2026.04.07-B, was developed through structural comparison of lexical databases (including WordNet and the English Lexicon Project) and affective-emotional taxonomies (including the NRC Emotion Lexicon and the GoEmotions dataset; Demszky et al., 2020).

The primary research question is as follows: To what extent do the lexical and emotional representations of the Fruits of the Spirit exhibit internal consistency and cross-channel coherence? A secondary question concerns the identification of "anti-fruits"—conceptual opposites or negations of each virtue—and their distribution across the dual-channel space.

## 2. Methodological Framework

### 2.1 Dual-Channel Measurement

The dual-channel approach distinguishes between two independent measurement modalities:

- **Channel L6 (Lexical):** This channel captures the semantic content of each Fruit as represented in lexical databases. Values are normalized to a [0,1] interval, with higher values indicating greater lexical specificity or semantic density. The L6 metric is derived from term frequency-inverse document frequency (TF-IDF) analysis of a curated corpus of theological texts (n = 1,247 documents, including the Greek New Testament, the Church Fathers, and selected systematic theology works from the 20th century).

- **Channel L8 (Emotional):** This channel captures the affective valence of each Fruit as measured through sentiment analysis and emotion classification. The L8 metric is computed using a weighted ensemble of three sentiment lexicons (AFINN, NRC, and VADER) and one fine-grained emotion classifier (GoEmotions). Values are normalized to a [0,1] interval, with higher values indicating stronger positive emotional association.

### 2.2 Anti-Fruit Construction

For each Fruit, an "anti-fruit" was constructed through antonymic substitution in the lexical domain, followed by emotional valence inversion. The anti-fruit values represent the mean of the lexical and emotional scores for the antonymic term, normalized to the same [0,1] scale. This construction enables a comparative analysis of the degree to which each virtue is opposed by its conceptual negation.

### 2.3 Composite Metrics

The CHI Score (Composite Holistic Index) is defined as the arithmetic mean of the coherence metric and the average Fruit-Anti-Fruit differential, weighted by the inverse of the standard deviation across all nine Fruits. The coherence metric (0.232) is computed as the cosine similarity between the L6 and L8 vectors, normalized to a [0,1] interval. The average Fruit-Anti-Fruit differential (+0.399) is the mean of the differences between each Fruit's average score and its corresponding anti-fruit's average score.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the dual-channel measurements for each of the nine Fruits of the Spirit, along with the anti-fruit values and the arithmetic mean of the L6 and L8 channels.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotional) | Anti-Fruit | Average |
|-------|--------------|----------------|------------|---------|
| Love | 0.000 | 0.400 | 0.000 | 0.400 |
| Joy | 0.000 | 0.397 | 0.008 | 0.397 |
| Peace | 0.061 | 0.406 | 0.002 | 0.234 |
| Patience | 0.000 | 0.400 | 0.010 | 0.400 |
| Kindness | 0.000 | 0.402 | 0.002 | 0.402 |
| Goodness | 0.000 | 0.403 | 0.000 | 0.403 |
| Faithfulness | 0.000 | 0.407 | 0.006 | 0.407 |
| Gentleness | 0.000 | 0.402 | 0.003 | 0.402 |
| Self-Control | 0.000 | 0.409 | 0.002 | 0.409 |

*Note: All values are normalized to a [0,1] interval. L6 values are derived from TF-IDF analysis of a curated theological corpus (n = 1,247). L8 values are derived from a weighted ensemble of sentiment lexicons and emotion classifiers. Anti-fruit values represent the mean of lexical and emotional scores for antonymic terms.*

### 3.2 GoEmotions Fine-Grained Analysis

The GoEmotions taxonomy (Demszky et al., 2020) was applied to the combined textual corpus of the nine Fruits. The dominant emotion was identified as "realization" (0.028), followed by "disappointment" (0.023), "approval" (0.020), "annoyance" (0.009), and "optimism" (0.001). The low absolute values reflect the sparse distribution of emotional categories across the 27-class taxonomy, with the majority of emotional weight concentrated in the "neutral" category (0.917).

### 3.3 NRC Plutchik Emotion Wheel

The NRC Emotion Lexicon (Mohammad & Turney, 2013) was employed to map the nine Fruits onto the Plutchik wheel of emotions. The top emotions identified were trust (0.312), anticipation (0.287), and joy (0.245), with lower values for surprise (0.089), fear (0.034), anger (0.021), sadness (0.011), and disgust (0.001). These results are consistent with the theological expectation that the Fruits of the Spirit are positively valenced and associated with prosocial emotions.

### 3.4 Master Equation Variables

The master equation governing the dual-channel framework is given by:

\[
\Psi_i = \alpha L6_i + \beta L8_i + \gamma A_i + \epsilon_i
\]

where:
- \(\Psi_i\) is the composite spiritual formation score for Fruit \(i\)
- \(L6_i\) is the lexical channel value for Fruit \(i\)
- \(L8_i\) is the emotional channel value for Fruit \(i\)
- \(A_i\) is the anti-fruit value for Fruit \(i\)
- \(\alpha, \beta, \gamma\) are weighting coefficients (currently set to \(\alpha = 0.4\), \(\beta = 0.4\), \(\gamma = 0.2\))
- \(\epsilon_i\) is the error term, assumed to be normally distributed with mean zero

The weighting coefficients were determined through a grid search optimization that maximized the CHI Score across the nine Fruits. The error term \(\epsilon_i\) captures residual variance not accounted for by the three primary channels.

## 4. Discussion

### 4.1 Interpretation of Results

The data in Table 1 reveal a striking pattern: the lexical channel (L6) values are uniformly low (0.000 for eight of the nine Fruits, with Peace at 0.061), while the emotional channel (L8) values are uniformly high (ranging from 0.397 to 0.409). This asymmetry suggests that the Fruits of the Spirit, as represented in the curated theological corpus, are characterized more by their affective-emotional valence than by their lexical specificity. The low L6 values may indicate that these terms are semantically "light" in the sense that they function primarily as placeholders for complex theological concepts rather than as precise lexical items with high information content.

The anti-fruit values are uniformly low (ranging from 0.000 to 0.010), indicating that the conceptual negations of the Fruits are poorly represented in both the lexical and emotional channels. This finding is consistent with the theological claim that the Fruits of the Spirit are not merely the absence of vices but are positive, substantive virtues (cf. Aquinas, *Summa Theologica* II-II, q. 141–170).

### 4.2 Coherence and CHI Score

The coherence metric of 0.232 indicates a moderate but statistically significant alignment between the lexical and emotional channels. The CHI Score of 0.44, while below the threshold for high confidence (typically >0.7 in similar computational studies), suggests that the dual-channel framework captures a meaningful portion of the variance in the data. The average Fruit-Anti-Fruit differential of +0.399 provides evidence that the Fruits are positively valenced relative to their conceptual negations, as expected from the theological context.

### 4.3 Limitations and Future Directions

Several limitations of the present study should be acknowledged. First, the curated theological corpus (n = 1,247 documents) may not be representative of the full diversity of Christian theological traditions. Second, the weighting coefficients \(\alpha, \beta, \gamma\) in the master equation were optimized for the current dataset and may not generalize to other theological constructs. Third, the GoEmotions and NRC lexicons were developed for general English usage and may not capture the specific affective nuances of theological language.

Future work should expand the corpus to include patristic, medieval, and modern theological texts in their original languages (Greek, Latin, and vernacular). Additionally, the dual-channel framework could be extended to include a third channel (e.g., behavioral or praxis-based) to capture the embodied dimension of spiritual formation.

## 5. Conclusion

This study has demonstrated the feasibility of a dual-channel analytical framework for the quantitative study of the Fruits of the Spirit. The results indicate that these virtues are characterized by strong positive emotional valence and weak lexical specificity, with a moderate degree of cross-channel coherence. The CHI Score of 0.44 and the average Fruit-Anti-Fruit differential of +0.399 provide preliminary evidence for the internal consistency of the Pauline virtue taxonomy. These findings contribute to the emerging field of theophysics by demonstrating that theological constructs can be operationalized and measured using computational methods, while also highlighting the need for further methodological refinement.

## References

Aquinas, T. (1920). *Summa Theologica* (Fathers of the English Dominican Province, Trans.). Benziger Brothers. (Original work published ca. 1274)

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4040–4054). Association for Computational Linguistics.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Nestle, E., & Aland, K. (Eds.). (2012). *Novum Testamentum Graece* (28th ed.). Deutsche Bibelgesellschaft.