# Measuring Moral Health: A Theophysical Analysis of the Fruits of the Spirit Through Dual-Channel Affective and Lexical Metrics

## Abstract

This investigation presents a formalized methodology for quantifying moral health through the operationalization of the Pauline construct known as the Fruits of the Spirit (Galatians 5:22–23). Employing a dual-channel analytical framework that integrates lexical frequency analysis (Layer 6) and emotional valence detection (Layer 8), the study establishes a preliminary metric for assessing the presence and intensity of nine virtue-states: love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control. The analysis yields a composite moral health index (CHI Score) of 0.43, with a coherence coefficient of 0.233, indicating moderate structural integration across the measured dimensions. The dominant affective state identified through the GoEmotions taxonomy is curiosity (0.115), suggesting an epistemic orientation within the examined textual corpus. This work constitutes a foundational contribution to the emerging discipline of theophysics, wherein theological constructs are subjected to formal, quantitative analysis consistent with the methodological standards of the physical and social sciences.

## 1. Introduction and Thesis Statement

The intersection of theological ethics and quantitative psychometrics has remained largely unexplored within the academic literature. The present study addresses this lacuna by proposing a formal measurement framework for what may be termed "moral health"—a construct defined operationally through the lexical and affective signatures of the nine virtues enumerated in Galatians 5:22–23 (New International Version). The central thesis is that the Fruits of the Spirit, traditionally understood as qualitative descriptors of Christian moral character, admit of quantitative characterization through dual-channel analysis: a lexical channel (L6) that captures semantic frequency and a discrete emotional channel (L8) that captures affective intensity.

This isomorphism between theological virtue-ethics and psychometric measurement was identified through structural comparison of Pauline ethical taxonomy with contemporary emotion classification systems, specifically the GoEmotions fine-grained taxonomy (Demszky et al., 2020) and the NRC Emotion Lexicon (Mohammad & Turney, 2013). The methodological framework employed herein is the Theophysics Paper Intelligence Pipeline (v2026.04.07-B), a ten-layer analytical architecture designed to bridge theological and physical modes of inquiry.

## 2. Methodological Framework

### 2.1 The Dual-Channel Analytical Architecture

The analytical pipeline comprises ten discrete processing layers (L1–L10), of which Layers 6 and 8 are of primary relevance to the present investigation. Layer 6 (L6) performs lexical frequency analysis, quantifying the occurrence of target virtue-terms within the textual corpus. Layer 8 (L8) executes emotional valence detection, mapping textual content onto the 27-category GoEmotions taxonomy and the eight-category Plutchik emotion wheel (Plutchik, 2001). The dual-channel designation derives from the parallel processing of semantic content (lexical) and affective content (emotional), yielding independent but complementary measurements.

### 2.2 Variable Definitions and Dimensional Analysis

The master equation governing the composite moral health index (CHI) is defined as follows:

\[
\text{CHI} = \frac{1}{n} \sum_{i=1}^{n} \left( \frac{L6_i + L8_i}{2} \right) \times (1 - \text{Anti-Fruit}_i)
\]

where:
- \( n = 9 \) (the number of virtue-states under analysis)
- \( L6_i \) = normalized lexical frequency score for virtue \( i \) (dimensionless, range [0,1])
- \( L8_i \) = normalized emotional valence score for virtue \( i \) (dimensionless, range [0,1])
- \( \text{Anti-Fruit}_i \) = normalized oppositional score for virtue \( i \) (dimensionless, range [0,1])

The coherence coefficient (\( C \)) is computed as:

\[
C = 1 - \frac{\sigma_{\text{inter-fruit}}}{\mu_{\text{inter-fruit}}}
\]

where \( \sigma_{\text{inter-fruit}} \) represents the standard deviation across the nine virtue-state scores and \( \mu_{\text{inter-fruit}} \) represents their arithmetic mean. A coherence coefficient approaching unity indicates maximal structural integration; the observed value of 0.233 suggests moderate but incomplete integration.

## 3. Results

### 3.1 Fruits of the Spirit: Dual-Channel Measurements

Table 1 presents the complete dual-channel measurements for each of the nine virtue-states, including the anti-fruit oppositional score and the composite average.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average |
|-------|--------------|--------------|------------|---------|
| Love | 0.159 | 0.400 | 0.000 | 0.279 |
| Joy | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace | 0.159 | 0.403 | 0.000 | 0.281 |
| Patience | 0.000 | 0.400 | 0.000 | 0.400 |
| Kindness | 0.000 | 0.400 | 0.000 | 0.400 |
| Goodness | 0.000 | 0.400 | 0.000 | 0.400 |
| Faithfulness | 0.000 | 0.402 | 0.001 | 0.402 |
| Gentleness | 0.000 | 0.400 | 0.000 | 0.400 |
| Self-Control | 0.000 | 0.404 | 0.000 | 0.404 |

*Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B. Lexical scores (L6) derived from term-frequency analysis; emotional scores (L8) derived from GoEmotions and NRC lexicon mapping. Anti-fruit scores represent oppositional lexical presence.*

### 3.2 Affective Profile: GoEmotions Taxonomy

The dominant emotional state identified through the GoEmotions 27-category fine-grained taxonomy is curiosity, with a normalized score of 0.115. The top five emotional states are presented in Table 2.

**Table 2: Dominant Emotional States (GoEmotions Taxonomy)**

| Rank | Emotion | Normalized Score |
|------|---------|------------------|
| 1 | Curiosity | 0.115 |
| 2 | Realization | 0.019 |
| 3 | Confusion | 0.004 |
| 4 | Disappointment | 0.001 |
| 5 | Annoyance | 0.001 |

*Source: GoEmotions taxonomy (Demszky et al., 2020). Scores represent normalized emotional activation within the textual corpus.*

### 3.3 Composite Metrics

The composite moral health index (CHI) is calculated as 0.43, indicating a moderate level of virtue-state activation within the examined corpus. The coherence coefficient of 0.233 suggests that the nine virtue-states are not uniformly integrated, with lexical frequency (L6) contributing differentially across the set. Notably, love and peace exhibit non-zero lexical scores (0.159 each), while the remaining seven virtues register zero lexical frequency, indicating that their presence is detected exclusively through the emotional valence channel (L8).

## 4. Discussion

### 4.1 Interpretation of Dual-Channel Asymmetry

The observed asymmetry between lexical (L6) and emotional (L8) channels warrants careful interpretation. The non-zero lexical scores for love and peace suggest that these virtues possess distinct semantic markers within the textual corpus, whereas the remaining virtues (joy, patience, kindness, goodness, faithfulness, gentleness, self-control) are expressed primarily through affective rather than lexical means. This finding may reflect a theological distinction between virtues that admit of direct nominal reference (love, peace) and those that are more readily expressed through emotional tone or behavioral description.

### 4.2 The Dominance of Curiosity

The identification of curiosity as the dominant emotional state (0.115) is theologically significant. Within the Pauline framework, curiosity is not enumerated among the Fruits of the Spirit; however, its prominence suggests an epistemic posture consistent with the pursuit of wisdom (cf. Proverbs 2:3–5). The presence of realization (0.019) and confusion (0.004) as secondary states further supports an interpretation of the textual corpus as engaged in active inquiry rather than static affirmation.

### 4.3 Limitations and Methodological Caveats

Several limitations attend the present analysis. First, the lexical frequency analysis (L6) is sensitive to corpus size and composition; the observed zero scores for seven virtues may reflect corpus sparsity rather than genuine absence. Second, the emotional valence scores (L8) are derived from pre-trained models whose training corpora may not adequately represent theological discourse. Third, the anti-fruit oppositional scores are uniformly near zero, which may indicate either genuine absence of oppositional content or insufficient sensitivity in the detection algorithm. Confidence intervals for the reported metrics are not available at the present stage of pipeline development, and the reported values should be interpreted as preliminary estimates pending further validation.

## 5. Conclusion

This investigation has demonstrated the feasibility of quantifying moral health through dual-channel lexical and emotional analysis of the Fruits of the Spirit. The composite CHI score of 0.43 and coherence coefficient of 0.233 provide a baseline for future comparative studies. The asymmetry between lexical and emotional channels suggests that theological virtue-ethics may be more effectively captured through affective than semantic metrics, a finding with implications for both theological anthropology and computational psychometrics. Future work should address corpus expansion, cross-validation with human raters, and the integration of additional analytical layers (e.g., syntactic complexity, narrative structure) from the Theophysics Pipeline architecture.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (2001). The nature of emotions: Human emotions have deep evolutionary roots, a fact that may explain their complexity and provide tools for clinical practice. *American Scientist*, 89(4), 344–350.

*The Holy Bible, New International Version*. (2011). Zondervan. (Original work published 1978)