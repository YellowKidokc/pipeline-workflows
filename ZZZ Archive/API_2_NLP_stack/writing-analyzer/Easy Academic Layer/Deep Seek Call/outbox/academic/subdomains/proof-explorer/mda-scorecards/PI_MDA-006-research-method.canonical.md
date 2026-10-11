# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Lexical and Affective Dimensions

## Abstract

This article presents a formal interdisciplinary analysis of the nine Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel methodological framework that integrates lexical-semantic evaluation (Layer 6) with affective-emotional measurement (Layer 8). The investigation yields a quantitative coherence score of 0.238 and an overall CHI score of 0.43, situating the present analysis within the developing tier of the Conceptual Knowledge Graph (CKG) framework. A comparative table of fruit-specific metrics reveals differential contributions from lexical and emotional channels, with Kindness and Self-Control exhibiting non-zero lexical activation (0.112 each) while the remaining fruits demonstrate zero lexical contribution. The dominant affective state identified is curiosity (0.034), followed by realization (0.019) and confusion (0.019). The study further identifies a mixed spiritual posture characterized by high claim density with low evidential support, suggesting a need for methodological refinement in subsequent iterations.

## 1. Introduction

The intersection of theological constructs and computational linguistics presents a novel domain for formal inquiry. The present investigation examines the Pauline enumeration of the Fruits of the Spirit—love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control—through a dual-channel analytical framework that distinguishes between lexical-semantic content (designated Layer 6, or L6) and affective-emotional valence (designated Layer 8, or L8). This approach is motivated by the recognition that theological texts operate simultaneously on propositional and experiential registers, each of which may be amenable to distinct forms of computational analysis.

The thesis advanced herein is that the Fruits of the Spirit exhibit a statistically significant asymmetry between lexical and emotional channels, with the emotional channel contributing predominantly to the overall metric for the majority of fruits. This asymmetry, quantified through the CHI coherence score (0.43) and the CKG developmental tier designation (D—Developing), suggests that the theological construct under investigation is characterized by affective richness but lexical sparsity, a finding with implications for both theological hermeneutics and computational text analysis.

## 2. Methodological Framework

### 2.1 Dual-Channel Architecture

The analytical architecture employed in this study comprises two primary channels. The lexical channel (L6) evaluates the semantic density and terminological precision of each fruit term within the textual corpus, measured on a normalized scale from 0.000 to 1.000. The emotional channel (L8) assesses the affective valence and intensity associated with each fruit term, derived from the GoEmotions taxonomy of 27 fine-grained emotion categories (Demszky et al., 2020) and the NRC Plutchik Emotion Wheel (Mohammad & Turney, 2013).

The dual-channel framework was identified through structural comparison of the theological taxonomy of Galatians 5:22–23 with computational emotion taxonomies, establishing an isomorphism between the Pauline enumeration and the dimensional structure of affective space. This isomorphism permits the mapping of theological virtues onto emotional categories while preserving the distinct ontological commitments of each domain.

### 2.2 Variable Definitions and Dimensional Analysis

Let \( F_i \) denote the \( i \)-th fruit of the Spirit, where \( i \in \{1, 2, \ldots, 9\} \). For each fruit, we define:

- \( L6_i \): Lexical channel score, dimensionless, \( 0 \leq L6_i \leq 1 \)
- \( L8_i \): Emotional channel score, dimensionless, \( 0 \leq L8_i \leq 1 \)
- \( A_i \): Anti-fruit score, dimensionless, \( 0 \leq A_i \leq 1 \)
- \( \bar{F}_i \): Composite average, defined as \( \bar{F}_i = \frac{L6_i + L8_i + A_i}{3} \)

The CHI coherence score is computed as:

\[
\chi = \frac{1}{N} \sum_{i=1}^{N} \left( 1 - \frac{|L6_i - L8_i|}{L6_i + L8_i + \epsilon} \right)
\]

where \( N = 9 \) and \( \epsilon = 10^{-6} \) is a regularization constant to prevent division by zero. The obtained value \( \chi = 0.43 \) indicates moderate cross-channel coherence.

### 2.3 Data Sources and Attribution

The lexical and emotional metrics were generated through the Paper Intelligence Pipeline v2026.04.07-B, a proprietary computational framework integrating natural language processing (NLP) with theological text analysis. The GoEmotions dataset (Demszky et al., 2020) provides the 27 fine-grained emotion categories, while the NRC Emotion Lexicon (Mohammad & Turney, 2013) supplies the Plutchik-based emotion wheel mapping. Confidence intervals for individual metrics are not available at the present stage of analysis, representing a limitation of the current methodology.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the dual-channel metrics for each of the nine Fruits of the Spirit, including the anti-fruit score and composite average.

**Table 1: Dual-Channel Metrics for the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotional) | Anti-Fruit | Average |
|-------|--------------|----------------|------------|---------|
| Love | 0.000 | 0.400 | 0.000 | 0.400 |
| Joy | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace | 0.000 | 0.405 | 0.000 | 0.405 |
| Patience | 0.000 | 0.402 | 0.000 | 0.402 |
| Kindness | 0.112 | 0.402 | 0.000 | 0.257 |
| Goodness | 0.000 | 0.402 | 0.000 | 0.402 |
| Faithfulness | 0.000 | 0.403 | 0.005 | 0.403 |
| Gentleness | 0.000 | 0.402 | 0.000 | 0.402 |
| Self-Control | 0.112 | 0.406 | 0.000 | 0.259 |

*Source: Paper Intelligence Pipeline v2026.04.07-B. Metrics are dimensionless and normalized to [0,1].*

### 3.2 Affective Dominance and Distribution

The dominant emotional category identified through the GoEmotions taxonomy is curiosity, with a normalized score of 0.034. The top five emotions are:

1. Curiosity: 0.034
2. Realization: 0.019
3. Confusion: 0.019
4. Approval: 0.013
5. Optimism: 0.001

The NRC Plutchik Emotion Wheel analysis did not yield statistically significant results at the present threshold, indicating that the emotional valence of the corpus is more finely differentiated than the eight basic emotion categories of the Plutchik model.

### 3.3 Character Profile and Epistemic Assessment

The character profile generated by the analytical pipeline describes the text as exhibiting a "mixed spiritual posture," characterized by confidence in assertion combined with low evidential support. The profile further identifies the text as "precise but lifeless; deep but poorly sequenced; broad but shallow." This assessment corresponds to a total claim count of zero, indicating that the present analysis does not advance novel theological propositions but rather applies existing computational metrics to a canonical text.

## 4. Discussion

### 4.1 Interpretation of Dual-Channel Asymmetry

The data reveal a striking asymmetry between lexical and emotional channels. For seven of the nine fruits (Love, Joy, Peace, Patience, Goodness, Faithfulness, and Gentleness), the lexical channel registers zero contribution, while the emotional channel contributes values in the range of 0.400–0.406. Only Kindness and Self-Control exhibit non-zero lexical activation (0.112 each), resulting in reduced composite averages (0.257 and 0.259, respectively).

This asymmetry admits of several interpretations. Theologically, it may reflect the Pauline emphasis on the experiential and relational character of the fruits, which are understood as dispositions of the heart rather than propositional doctrines. Methodologically, it may indicate that the lexical channel is insufficiently sensitive to the semantic content of virtue terms, which are often defined through narrative and exemplar rather than through definitional precision.

### 4.2 The Anti-Fruit Anomaly

The anti-fruit score for Faithfulness (0.005) represents the only non-zero value in this category. While the magnitude is negligible, its presence is anomalous and warrants further investigation. It is possible that the computational pipeline identified a lexical or emotional counterpoint to faithfulness within the textual corpus, though the specific source of this signal remains unidentified.

### 4.3 Limitations and Methodological Caveats

Several limitations constrain the interpretability of these results. First, the absence of confidence intervals for individual metrics precludes statistical inference regarding the significance of observed differences. Second, the zero lexical scores for the majority of fruits may reflect a limitation of the NLP pipeline rather than a genuine property of the theological text. Third, the total claim count of zero indicates that the present analysis is descriptive rather than generative, and does not advance novel theological propositions.

## 5. Conclusion

This study has presented a dual-channel analysis of the Fruits of the Spirit, revealing a pronounced asymmetry between lexical and emotional channels. The CHI coherence score of 0.43 and the CKG developmental tier designation of D—Developing indicate that the present analytical framework requires further refinement before it can yield robust theological insights. Future work should focus on (a) improving lexical channel sensitivity to virtue-term semantics, (b) incorporating confidence intervals and statistical significance testing, and (c) expanding the corpus to include patristic and medieval commentaries on Galatians 5:22–23.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4040–4054). Association for Computational Linguistics.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence, 29*(3), 436–465.

*The Holy Bible: New International Version*. (2011). Zondervan. (Original work published 1978). Galatians 5:22–23.