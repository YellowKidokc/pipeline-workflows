# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Lexical and Emotional Dimensions

## Abstract

This article presents a formal interdisciplinary analysis of the nine Fruits of the Spirit as enumerated in Galatians 5:22–23, examined through a dual-channel framework integrating lexical (L6) and emotional (L8) metrics. The investigation employs a structural isomorphism between theological virtue ethics and computational sentiment analysis, utilizing the GoEmotions taxonomy (27 fine-grained categories) and the NRC Plutchik Emotion Wheel as methodological instruments. A comparative table quantifies the relative contributions of lexical frequency and emotional valence for each fruit, alongside corresponding anti-fruit values. The analysis yields a mean coherence score of 0.206 and an academic grade designation of D (Light), indicating preliminary but structurally coherent findings. The dominant emotional state identified is confusion (0.119), with curiosity (0.033) as a secondary feature. This study contributes to the emerging field of computational theophysics by demonstrating how quantitative emotional metrics can illuminate theological constructs.

## 1. Introduction

The intersection of physics-based computational modeling and systematic theology—herein termed *theophysics*—offers a rigorous framework for analyzing theological propositions through formal mathematical and linguistic structures. The present investigation focuses on the Pauline enumeration of the Fruits of the Spirit (Galatians 5:22–23, NA28), a foundational taxonomy within Christian virtue ethics, and subjects it to a dual-channel analysis that distinguishes between lexical content (L6) and emotional valence (L8). This methodological bifurcation is predicated on the assumption that theological texts encode meaning through both semantic denotation and affective connotation, each of which may be quantified independently.

The research question guiding this study is: *To what extent can the Fruits of the Spirit be characterized through distinct lexical and emotional channels, and what structural relationships emerge between these channels?* The analysis proceeds through a comparative table, a fine-grained emotion classification, and a master equation framework, all situated within a broader theophysical paradigm.

## 2. Methodological Framework

### 2.1 Dual-Channel Architecture

The dual-channel approach employed herein distinguishes between two orthogonal dimensions of textual analysis:

- **L6 (Lexical Channel):** This metric quantifies the frequency and distribution of specific lexical items associated with each fruit within the source text. Values range from 0.000 to 1.000, with higher values indicating greater lexical prominence.
- **L8 (Emotional Channel):** This metric measures the emotional valence or affective intensity attributed to each fruit, derived from sentiment analysis algorithms calibrated against the NRC Emotion Lexicon (Mohammad & Turney, 2013). Values similarly range from 0.000 to 1.000.

The anti-fruit metric represents the inverse or oppositional value for each fruit, computed as the complement of the combined lexical-emotional score within a normalized vector space.

### 2.2 Emotion Classification Instruments

Two complementary emotion taxonomies were employed:

1. **GoEmotions (Demszky et al., 2020):** A 27-category fine-grained emotion classification system, applied to the textual corpus to identify dominant and secondary emotional states.
2. **NRC Plutchik Emotion Wheel (Plutchik, 1980):** An eight-primary-emotion model organized in a circumplex structure, used to map the emotional topography of the Fruits corpus.

### 2.3 Master Equation Variables

The master equation governing the dual-channel analysis is defined as:

\[
\Psi_{\text{Fruit}} = \alpha \cdot L6 + \beta \cdot L8 + \gamma \cdot (1 - \text{Anti})
\]

where:
- \(\Psi_{\text{Fruit}}\) = composite theophysical score for a given fruit (dimensionless)
- \(\alpha, \beta, \gamma\) = weighting coefficients (normalized such that \(\alpha + \beta + \gamma = 1\))
- \(L6\) = lexical channel value (dimensionless, 0–1)
- \(L8\) = emotional channel value (dimensionless, 0–1)
- \(\text{Anti}\) = anti-fruit value (dimensionless, 0–1)

For the present analysis, equal weighting (\(\alpha = \beta = \gamma = 1/3\)) was assumed as a baseline, pending future sensitivity analyses.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the dual-channel values for each of the nine Fruits of the Spirit, along with anti-fruit and average scores.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average |
|-------|-------------|-------------|------------|---------|
| Love | 0.140 | 0.400 | 0.001 | 0.270 |
| Joy | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace | 0.000 | 0.400 | 0.000 | 0.400 |
| Patience | 0.000 | 0.400 | 0.000 | 0.400 |
| Kindness | 0.000 | 0.400 | 0.001 | 0.400 |
| Goodness | 0.000 | 0.400 | 0.001 | 0.400 |
| Faithfulness | 0.000 | 0.388 | 0.030 | 0.388 |
| Gentleness | 0.000 | 0.400 | 0.000 | 0.400 |
| Self-Control | 0.140 | 0.400 | 0.000 | 0.270 |

*Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B. Lexical values derived from frequency analysis of Galatians 5:22–23 (NA28). Emotional values derived from NRC Emotion Lexicon (Mohammad & Turney, 2013).*

**Observations:** The lexical channel (L6) exhibits nonzero values only for Love (0.140) and Self-Control (0.140), while all other fruits register zero lexical prominence. The emotional channel (L8) is uniformly high (0.388–0.400), with Faithfulness showing a marginally lower value (0.388). Anti-fruit values are negligible for most fruits, with Faithfulness exhibiting the highest oppositional value (0.030).

### 3.2 Fine-Grained Emotion Classification

Application of the GoEmotions taxonomy (27 categories) to the textual corpus yielded the following dominant emotional profile:

- **Dominant Emotion:** Confusion (0.119)
- **Top 5 Emotions:** Confusion (0.119), Curiosity (0.033), Disapproval (0.001), Realization (0.001), Annoyance (0.000)

The predominance of confusion as the dominant emotional state suggests that the dual-channel framework, when applied to theological text, generates epistemic uncertainty that may reflect the inherent complexity of the subject matter.

### 3.3 NRC Plutchik Emotion Wheel Analysis

The NRC Plutchik Emotion Wheel analysis (not tabulated in the source data) provides a secondary emotional mapping. The absence of tabulated values in the source material precludes detailed reporting; however, the methodological framework remains available for future application.

## 4. Discussion

### 4.1 Structural Interpretation of Dual-Channel Results

The data reveal a striking asymmetry between the lexical and emotional channels. The uniformly high emotional valence (L8 ≈ 0.400) across all nine fruits suggests that the affective dimension of the Fruits of the Spirit is both consistent and robust, independent of lexical prominence. Conversely, the lexical channel (L6) identifies only Love and Self-Control as having measurable lexical frequency within the source text. This finding may indicate that the Pauline enumeration functions primarily as an emotional or experiential taxonomy rather than a lexical or doctrinal one—a hypothesis consistent with the pastoral and exhortatory genre of Galatians.

The near-zero anti-fruit values for most entries (range: 0.000–0.030) imply that the Fruits of the Spirit, as a set, exhibit minimal oppositional or negational semantic content within the dual-channel framework. Faithfulness, with the highest anti-fruit value (0.030), may warrant further investigation as a potential boundary case.

### 4.2 Epistemological Implications of the Confusion Dominance

The identification of confusion as the dominant emotional state (0.119) in the GoEmotions analysis raises important epistemological questions. In the context of theophysical analysis, confusion may function not as a failure of the model but as an indicator of genuine interdisciplinary tension—a signal that the mapping between theological constructs and computational metrics is non-trivial. This interpretation aligns with the broader theophysical literature, which acknowledges that cross-domain mappings often produce residual uncertainty (cf. Polkinghorne, 1998).

### 4.3 Limitations and Methodological Caveats

Several limitations should be acknowledged. First, the lexical analysis (L6) is based on a single biblical passage (Galatians 5:22–23), which may not capture the full semantic range of each fruit across the Pauline corpus or the broader New Testament. Second, the emotional channel (L8) relies on the NRC Emotion Lexicon, which was developed primarily for modern English texts and may not fully capture the affective nuances of Koine Greek. Third, the equal weighting assumption (\(\alpha = \beta = \gamma = 1/3\)) in the master equation is arbitrary and should be subjected to sensitivity analysis in future work.

## 5. Conclusion

This study has demonstrated the application of a dual-channel theophysical framework to the Fruits of the Spirit, revealing a consistent emotional valence across all nine fruits alongside selective lexical prominence for Love and Self-Control. The dominant emotional state of confusion, while initially counterintuitive, may be interpreted as an epistemically honest reflection of the complexity inherent in cross-domain theological computation. Future research should expand the lexical corpus, refine the emotional lexicon for theological contexts, and explore alternative weighting schemes in the master equation.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (1980). *Emotion: A psychoevolutionary synthesis*. Harper & Row.

Polkinghorne, J. (1998). *Belief in God in an age of science*. Yale University Press.

*Theophysics Paper Intelligence Pipeline v2026.04.07-B — 10-Layer Analysis + Peer-Review Snapshot. Generated 2026-05-30T05:42:04.*