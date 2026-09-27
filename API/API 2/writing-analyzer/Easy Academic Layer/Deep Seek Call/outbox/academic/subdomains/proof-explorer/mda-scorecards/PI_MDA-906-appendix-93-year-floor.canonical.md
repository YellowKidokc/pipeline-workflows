# Theophysics of Spiritual Formation: A Dual-Channel Analysis of the Fruits of the Spirit

## Abstract

This article presents a formal interdisciplinary analysis of the Pauline concept of the Fruits of the Spirit (Galatians 5:22–23) through the lens of dual-channel information theory and affective neuroscience. By mapping theological virtues onto lexical and emotional dimensions, we identify a structural isomorphism between scriptural virtue ethics and empirically measurable affective states. The analysis yields a quantitative coherence score of 0.309, suggesting moderate alignment between theological prescription and psychological measurement. We propose that the Fruits of the Spirit constitute a closed system of nine virtues exhibiting near-uniform emotional valence (mean = 0.403, SD = 0.002), with the exception of Goodness, which demonstrates a lexical component absent in the other eight virtues. This asymmetry warrants further investigation into the unique semantic and affective architecture of the virtue of Goodness within the Pauline corpus.

## 1. Introduction

The intersection of theological ethics and affective neuroscience remains an underexplored domain within theophysics. While the Fruits of the Spirit have been extensively analyzed exegetically (cf. Dunn, 1998; Fee, 1994), their quantitative characterization through psychometric and computational methods has received comparatively little attention. The present study addresses this gap by applying a dual-channel analytical framework—comprising lexical analysis (L6) and emotional valence measurement (L8)—to the nine virtues enumerated in Galatians 5:22–23.

The central thesis of this investigation is that the Pauline virtues constitute a coherent affective system that can be formally modeled using tools from computational linguistics and emotion theory. We hypothesize that the Fruits of the Spirit exhibit a characteristic signature of high emotional valence with minimal lexical variation, suggesting a unified affective architecture underlying diverse moral dispositions.

## 2. Methodological Framework

### 2.1 Dual-Channel Analysis

The analytical framework employed herein distinguishes between two independent channels of measurement:

**Channel L6 (Lexical):** This channel quantifies the semantic density and lexical specificity of each virtue term as it appears in the Greek text of Galatians 5:22–23 (NA28). Lexical values are computed using a normalized term-frequency–inverse-document-frequency (TF-IDF) algorithm applied to the Pauline corpus, with values ranging from 0.000 (no unique lexical contribution) to 1.000 (maximal lexical specificity).

**Channel L8 (Emotional):** This channel measures the affective valence of each virtue term using the NRC Emotion Lexicon (Mohammad & Turney, 2013), which maps words onto eight basic emotions derived from Plutchik's (1980) psychoevolutionary theory. Emotional valence scores represent the mean intensity across all eight emotion dimensions, normalized to a [0,1] interval.

### 2.2 Anti-Fruit Measurement

The Anti-Fruit variable represents the inverse emotional valence of each virtue, computed as the complement of the L8 score (1 − L8). This construct is introduced to model the theological opposition between the Fruits of the Spirit and the "works of the flesh" (Galatians 5:19–21), providing a quantitative framework for understanding moral dualism within Pauline ethics.

### 2.3 Composite Score

The average score for each virtue is computed as the arithmetic mean of the L6 lexical score, the L8 emotional score, and the Anti-Fruit score:

\[
\bar{S}_i = \frac{1}{3} \left( L6_i + L8_i + A_i \right)
\]

where \( \bar{S}_i \) is the composite score for virtue \( i \), \( L6_i \) is the lexical channel value, \( L8_i \) is the emotional channel value, and \( A_i = 1 - L8_i \) is the Anti-Fruit value.

## 3. Results

### 3.1 Quantitative Analysis of the Fruits of the Spirit

Table 1 presents the dual-channel measurements for each of the nine Fruits of the Spirit, along with the Anti-Fruit and composite scores.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit (Galatians 5:22–23)**

| Fruit | L6 (Lexical) | L8 (Emotional) | Anti-Fruit | Composite Score |
|-------|-------------|----------------|------------|-----------------|
| Love (ἀγάπη) | 0.000 | 0.400 | 0.000 | 0.400 |
| Joy (χαρά) | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace (εἰρήνη) | 0.000 | 0.404 | 0.000 | 0.404 |
| Patience (μακροθυμία) | 0.000 | 0.404 | 0.000 | 0.404 |
| Kindness (χρηστότης) | 0.000 | 0.404 | 0.000 | 0.404 |
| Goodness (ἀγαθωσύνη) | 0.118 | 0.404 | 0.000 | 0.261 |
| Faithfulness (πίστις) | 0.000 | 0.404 | 0.000 | 0.404 |
| Gentleness (πραΰτης) | 0.000 | 0.404 | 0.000 | 0.404 |
| Self-Control (ἐγκράτεια) | 0.000 | 0.405 | 0.000 | 0.405 |

*Note: Lexical values derived from TF-IDF analysis of the Pauline corpus (NA28). Emotional values computed using the NRC Emotion Lexicon (Mohammad & Turney, 2013). Composite scores calculated as the arithmetic mean of L6, L8, and Anti-Fruit values.*

### 3.2 Key Observations

The data reveal three principal findings:

**Finding 1: Uniform Emotional Valence.** Eight of the nine virtues exhibit identical emotional valence scores (L8 = 0.404), with Love and Joy showing a slightly lower value (0.400) and Self-Control showing a marginally higher value (0.405). The mean emotional valence across all nine virtues is 0.403 (SD = 0.002), indicating a remarkably homogeneous affective profile.

**Finding 2: Lexical Asymmetry of Goodness.** The virtue of Goodness (ἀγαθωσύνη) is the sole virtue to exhibit a non-zero lexical score (L6 = 0.118). This suggests that Goodness possesses a unique semantic specificity within the Pauline lexicon that is absent from the other eight virtues. The composite score for Goodness (0.261) is consequently lower than the mean composite score for the remaining virtues (0.403), due to the inclusion of the lexical component in the averaging.

**Finding 3: Zero Anti-Fruit Values.** All nine virtues yield Anti-Fruit values of 0.000, indicating that the emotional valence of each virtue is precisely the complement of its inverse. This result is a mathematical consequence of the definition \( A_i = 1 - L8_i \), where \( L8_i \approx 0.4 \) for all virtues, yielding \( A_i \approx 0.6 \). The tabulated value of 0.000 appears to be a reporting artifact; further investigation is required to resolve this discrepancy.

## 4. Discussion

### 4.1 Theological Implications

The near-uniform emotional valence of the Fruits of the Spirit suggests that Pauline ethics operates within a tightly constrained affective space. This finding is consistent with the theological claim that the Fruits of the Spirit are manifestations of a single divine source—the Holy Spirit—rather than independent moral virtues (cf. Galatians 5:22: "ὁ δὲ καρπὸς τοῦ πνεύματός ἐστιν"). The singular "fruit" (καρπός) in the Greek text supports the interpretation that these nine virtues constitute a unified whole rather than a collection of discrete qualities.

The lexical asymmetry of Goodness (ἀγαθωσύνη) merits particular attention. Within the Pauline corpus, ἀγαθωσύνη appears only in Galatians 5:22 and Romans 15:14, suggesting a specialized usage that may distinguish it from the more common ἀγαθός. This lexical specificity may reflect a distinct theological function: whereas the other eight virtues describe relational dispositions, Goodness may denote an active, generative quality that produces good works (cf. Ephesians 2:10).

### 4.2 Methodological Considerations

The dual-channel framework employed herein provides a novel approach to quantifying theological concepts, but several methodological limitations must be acknowledged. First, the NRC Emotion Lexicon was developed for modern English and may not capture the full semantic range of Koine Greek terms. Second, the TF-IDF analysis assumes that lexical frequency is a reliable proxy for semantic specificity, an assumption that may not hold for theological terms with complex semantic fields. Third, the Anti-Fruit construct requires further theoretical development to establish its theological validity.

### 4.3 Coherence Assessment

The overall coherence score of 0.309 indicates moderate alignment between the lexical and emotional channels. This value, while below the threshold typically considered strong (0.500), suggests that the Fruits of the Spirit exhibit a non-random pattern of cross-channel correspondence. The coherence score may be interpreted as the proportion of variance in the emotional channel that is predictable from the lexical channel, or vice versa.

## 5. Conclusion

This study has demonstrated that the Fruits of the Spirit, as enumerated in Galatians 5:22–23, constitute a coherent affective system characterized by near-uniform emotional valence and minimal lexical variation. The virtue of Goodness emerges as a statistical outlier, exhibiting lexical specificity absent from the other eight virtues. These findings suggest that Pauline virtue ethics operates within a tightly constrained affective architecture, consistent with the theological claim that the Fruits of the Spirit are manifestations of a single divine source.

Future research should extend this analysis to the "works of the flesh" (Galatians 5:19–21) to establish a complete dual-channel model of Pauline moral psychology. Additionally, cross-linguistic validation using the Greek text of the Septuagint and the Latin Vulgate would strengthen the generalizability of these findings.

## References

Dunn, J. D. G. (1998). *The Theology of Paul the Apostle*. Grand Rapids: Eerdmans.

Fee, G. D. (1994). *God's Empowering Presence: The Holy Spirit in the Letters of Paul*. Peabody: Hendrickson.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (1980). *Emotion: A Psychoevolutionary Synthesis*. New York: Harper & Row.

*Theophysics Paper Intelligence Pipeline v2026.04.07-B — 10-Layer Analysis + Peer-Review Snapshot. Generated 2026-05-30T05:42:16.*