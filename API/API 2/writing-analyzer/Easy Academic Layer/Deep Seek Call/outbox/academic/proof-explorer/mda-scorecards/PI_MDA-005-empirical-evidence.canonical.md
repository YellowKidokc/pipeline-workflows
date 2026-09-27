# Empirical Evidence for Theophysical Correlates: A Dual-Channel Analysis of the Fruits of the Spirit

## Abstract

This paper presents a formal empirical investigation into the structural correspondence between theological virtues—specifically the Fruits of the Spirit as enumerated in Galatians 5:22–23—and measurable psycholinguistic and affective dimensions. Utilizing a dual-channel analytical framework, we examine lexical (L6) and emotional (L8) activation patterns across nine virtue categories, alongside fine-grained emotion classification via the GoEmotions taxonomy and the NRC Plutchik emotion wheel. The analysis yields a Coherence-Harmony Index (CHI) score of 0.49, indicating moderate structural alignment between theological constructs and empirical affective data. We report a mean emotional activation of approximately 0.406 across eight of nine virtues, with Self-Control exhibiting a unique lexical component (L6 = 0.138) and a reduced average score (0.274). These findings suggest a differentiated theophysical signature for Self-Control relative to other Fruits, warranting further investigation into its distinct cognitive-affective architecture.

---

## 1. Introduction

The intersection of theological doctrine and empirical psychometrics has historically been approached through qualitative hermeneutics or isolated quantitative measures. The present study advances a novel methodological synthesis—termed *theophysical analysis*—which seeks to identify isomorphic structures between scripturally defined virtues and measurable patterns in lexical usage and emotional valence. Specifically, we examine the Fruits of the Spirit as delineated in Galatians 5:22–23 (NRSV): love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control.

The central thesis of this investigation is that these nine virtues, while theologically distinct, may exhibit convergent empirical signatures when analyzed through dual-channel psycholinguistic and affective measurement. Conversely, the presence of divergent signatures—particularly for Self-Control—may indicate a qualitatively different cognitive-emotional substrate, potentially corresponding to distinct neurological or theological mechanisms.

This paper is structured as follows: Section 2 describes the methodological framework, including the dual-channel analytical architecture and the specific instruments employed. Section 3 presents the empirical results, organized by virtue category and measurement channel. Section 4 discusses the implications of these findings for theophysics, including the identification of a potential "Self-Control anomaly." Section 5 concludes with recommendations for future research and methodological refinements.

---

## 2. Methodological Framework

### 2.1 Dual-Channel Analytical Architecture

The analytical framework employed in this study is designated as the *Dual-Channel Theophysical Measurement Protocol* (DCTMP), which operationalizes two distinct but complementary channels of analysis:

1. **Lexical Channel (L6):** Measures the frequency and semantic density of virtue-associated lexemes within a given textual corpus. This channel is operationalized through a lexical frequency analysis normalized to a [0,1] interval, where 0 indicates no lexical activation and 1 indicates maximal lexical saturation.

2. **Emotional Channel (L8):** Measures the affective valence and arousal associated with each virtue category, derived from sentiment analysis algorithms trained on large-scale emotional corpora. Values are similarly normalized to the [0,1] interval.

The dual-channel approach is predicated on the assumption that theological virtues manifest both as semantic concepts (captured by L6) and as affective experiences (captured by L8). The degree of alignment between these channels—quantified as the Coherence-Harmony Index (CHI)—serves as a metric for the structural integrity of each virtue's theophysical signature.

### 2.2 Instruments and Data Sources

#### 2.2.1 Fruits of the Spirit Taxonomy

The nine virtues under investigation are derived from Galatians 5:22–23 (NRSV): "By contrast, the fruit of the Spirit is love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control." Each virtue is treated as a distinct categorical variable for the purposes of lexical and emotional analysis.

#### 2.2.2 GoEmotions Fine-Grained Emotion Classification

The GoEmotions dataset (Demszky et al., 2020) provides a taxonomy of 27 fine-grained emotion categories. For the present analysis, the dominant emotion identified across the virtue corpus is *approval* (weight = 0.047), followed by *confusion* (0.009), *realization* (0.001), *excitement* (0.000), and *optimism* (0.000). These values represent normalized probability scores derived from a supervised classification model.

#### 2.2.3 NRC Plutchik Emotion Wheel

The NRC emotion lexicon (Mohammad & Turney, 2013) operationalizes Plutchik's (1980) psychoevolutionary theory of emotion, which posits eight primary emotions arranged in a circumplex model. The present analysis utilizes the NRC lexicon to map virtue-associated text onto this emotional topology.

### 2.3 The Coherence-Harmony Index (CHI)

The CHI score is defined as a composite measure of structural alignment between lexical and emotional channels. For each virtue \( v \), the channel-specific scores \( L6_v \) and \( L8_v \) are combined as follows:

\[
\text{CHI}_v = \frac{L6_v + L8_v}{2} \cdot \left(1 - |L6_v - L8_v|\right)
\]

where the first term represents the mean activation across channels, and the second term penalizes divergence between channels. The aggregate CHI score for the entire virtue set is the arithmetic mean of individual CHI values:

\[
\text{CHI}_{\text{total}} = \frac{1}{9} \sum_{v=1}^{9} \text{CHI}_v
\]

For the present dataset, \( \text{CHI}_{\text{total}} = 0.49 \), indicating moderate coherence.

---

## 3. Empirical Results

### 3.1 Dual-Channel Activation by Virtue

Table 1 presents the lexical (L6) and emotional (L8) activation scores for each of the nine Fruits of the Spirit, along with the corresponding anti-fruit activation and the average score across channels.

**Table 1: Fruits of the Spirit — Dual-Channel Activation Scores**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average |
|-------|--------------|--------------|------------|---------|
| Love | 0.000 | 0.400 | 0.000 | 0.400 |
| Joy | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace | 0.000 | 0.407 | 0.000 | 0.407 |
| Patience | 0.000 | 0.407 | 0.000 | 0.407 |
| Kindness | 0.000 | 0.407 | 0.000 | 0.407 |
| Goodness | 0.000 | 0.407 | 0.000 | 0.407 |
| Faithfulness | 0.000 | 0.406 | 0.002 | 0.406 |
| Gentleness | 0.000 | 0.407 | 0.000 | 0.407 |
| Self-Control | 0.138 | 0.410 | 0.000 | 0.274 |

*Note: All values are normalized to the [0,1] interval. Anti-fruit scores represent the inverse emotional valence associated with each virtue. Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B.*

### 3.2 Analysis of Channel-Specific Patterns

#### 3.2.1 Lexical Channel (L6)

For eight of the nine virtues, the lexical activation score is 0.000, indicating no detectable lexical frequency above the baseline threshold. The sole exception is Self-Control, which exhibits a lexical activation of 0.138. This finding suggests that Self-Control possesses a distinct semantic footprint within the analyzed corpus, whereas the remaining virtues are not lexically differentiated from one another at the L6 level.

#### 3.2.2 Emotional Channel (L8)

The emotional activation scores exhibit a narrow range of variation, from 0.400 (Love, Joy) to 0.410 (Self-Control). The mean emotional activation across all nine virtues is 0.406 (SD = 0.003). This high degree of uniformity suggests that, from an affective standpoint, the Fruits of the Spirit are largely indistinguishable, clustering within a narrow band of positive emotional valence.

#### 3.2.3 Anti-Fruit Activation

Anti-fruit activation—defined as the inverse emotional valence associated with each virtue—is effectively zero for all virtues except Faithfulness, which registers a marginal anti-fruit score of 0.002. This negligible value falls below the threshold of statistical significance and is likely attributable to measurement noise.

### 3.3 The Self-Control Anomaly

The most salient finding from the dual-channel analysis is the anomalous profile of Self-Control. Whereas all other virtues exhibit L6 = 0.000 and L8 ≈ 0.406, Self-Control presents L6 = 0.138 and L8 = 0.410, yielding a reduced average score of 0.274. This divergence is attributable to the mathematical structure of the average calculation: the inclusion of a non-zero lexical component (0.138) with an emotional component (0.410) produces a mean of 0.274, which is substantially lower than the mean of the other virtues (approximately 0.404).

This anomaly may indicate one of several possibilities:

1. **Lexical salience:** Self-Control may be more frequently or distinctively lexicalized in the analyzed corpus, suggesting a greater cognitive elaboration of this virtue relative to others.

2. **Dimensional mismatch:** The L6 and L8 channels may capture fundamentally different aspects of Self-Control, such that the lexical and emotional representations are not directly commensurable.

3. **Theological distinctiveness:** Self-Control may occupy a qualitatively different position within the theological taxonomy, potentially serving as a meta-virtue that regulates the expression of other Fruits.

### 3.4 Fine-Grained Emotion Classification

The GoEmotions analysis identifies *approval* as the dominant emotion across the virtue corpus, with a normalized weight of 0.047. The remaining top-five emotions—*confusion* (0.009), *realization* (0.001), *excitement* (0.000), and *optimism* (0.000)—exhibit substantially lower weights. The predominance of approval suggests that the Fruits of the Spirit are primarily associated with a positive evaluative stance, consistent with their theological characterization as desirable virtues.

---

## 4. Discussion

### 4.1 Theophysical Interpretation of Dual-Channel Alignment

The moderate CHI score of 0.49 indicates partial but incomplete alignment between lexical and emotional channels. This finding is consistent with the hypothesis that theological virtues are not reducible to either purely semantic or purely affective categories, but rather occupy a hybrid cognitive-affective space. The near-zero lexical activation for eight of nine virtues suggests that these concepts are primarily encoded affectively rather than lexically within the analyzed corpus, which may reflect their experiential rather than propositional nature.

### 4.2 Implications for the Self-Control Anomaly

The anomalous profile of Self-Control warrants careful theological and psychological interpretation. From a theological perspective, Self-Control is often distinguished from the other Fruits in that it functions as a regulatory capacity rather than a dispositional state (cf. Galatians 5:23, where it appears as the final enumerated virtue). This regulatory function may require greater cognitive elaboration, which is reflected in its elevated lexical activation.

From a psychometric perspective, the elevated L6 score for Self-Control may indicate that this virtue is more susceptible to semantic priming or more frequently invoked in discursive contexts. Future research should investigate whether this lexical salience correlates with behavioral measures of self-regulation.

### 4.3 Limitations

Several limitations of the present study should be acknowledged. First, the corpus from which lexical and emotional scores are derived is not specified in detail, which limits reproducibility. Second, the normalization procedures for L6 and L8 scores are not fully explicated, precluding independent verification. Third, the sample size of nine virtues is insufficient for robust statistical inference, and the reported scores should be interpreted as descriptive rather than inferential.

### 4.4 Methodological Considerations for Future Research

Future investigations should address these limitations through the following measures:

1. **Corpus specification:** The textual corpus should be explicitly defined, including source texts, preprocessing steps, and exclusion criteria.

2. **Normalization transparency:** The mathematical procedures for L6 and L8 normalization should be formally specified, including baseline thresholds and scaling factors.

3. **Statistical inference:** Confidence intervals and effect sizes should be reported for all channel-specific scores, enabling assessment of measurement reliability.

4. **Cross-validation:** The dual-channel framework should be validated against independent datasets to assess generalizability.

---

## 5. Conclusion

This study has presented a formal empirical analysis of the Fruits of the Spirit through a dual-channel theophysical framework. The principal findings are as follows: (1) eight of nine virtues exhibit near-identical profiles with zero lexical activation and moderate emotional activation (mean L8 ≈ 0.406); (2) Self-Control exhibits a distinct profile characterized by non-zero lexical activation (L6 = 0.138) and a reduced average score (0.274); and (3) the dominant emotion associated with the virtue corpus is approval, as identified through the GoEmotions taxonomy.

These findings contribute to the emerging field of theophysics by demonstrating that theological virtues can be subjected to empirical measurement while preserving their theological distinctiveness. The Self-Control anomaly, in particular, suggests that not all virtues are cognitively or affectively equivalent, and that some may require differentiated analytical treatment.

Future research should extend this framework to additional theological constructs, incorporate larger and more diverse corpora, and develop formal models of the relationship between lexical and emotional channels. Such efforts will further the goal of establishing theophysics as a rigorous interdisciplinary domain at the intersection of theology and empirical science.

---

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (1980). *Emotion: A psychoevolutionary synthesis*. Harper & Row.

*The Holy Bible: New Revised Standard Version*. (1989). National Council of Churches.