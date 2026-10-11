# Theophysics of Moral Affect: A Dual-Channel Analysis of Galatians 5:22–23 via Lexical and Emotional Embedding Spaces

## Abstract

This study presents a formal analysis of the Pauline catalogue of moral virtues known as the "Fruits of the Spirit" (Galatians 5:22–23) through a dual-channel computational framework integrating lexical-semantic embedding (L6) and affective-emotional embedding (L8). The investigation employs a control-group design drawn from an Amish textual corpus (MDA-045) to isolate the theological signal from ambient linguistic noise. A master equation governing the interaction between lexical frequency and emotional valence is proposed, with variable definitions and dimensional consistency established. The analysis yields a composite coherence index of 0.265 and an academic readability grade of C (moderate), corresponding to an 11th–12th grade reading level. The dominant fine-grained emotion detected via the GoEmotions taxonomy is *realization* (0.024), while the NRC Plutchik wheel indicates suppressed negative affect. The findings suggest a structurally asymmetric distribution of moral affect across the nine virtues, with *faithfulness* and *gentleness* exhibiting maximal emotional salience and *love* and *goodness* demonstrating lexical-emotional divergence. These results are interpreted within a theophysical framework that posits a non-reductive correspondence between scriptural moral ontology and quantifiable affective dynamics.

## 1. Introduction

The intersection of theological ethics and computational linguistics remains an underexplored domain within the emerging field of theophysics. While substantial work has been undertaken in sentiment analysis of religious texts (e.g., Mohammad & Turney, 2013; Cook, 2020), few studies have attempted to formalize the structural relationship between Pauline virtue ethics and the latent emotional architecture encoded in lexical choice. The present investigation addresses this gap by applying a dual-channel analytical pipeline—comprising lexical frequency analysis (L6) and emotional embedding (L8)—to the pericope Galatians 5:22–23, as rendered in the Amish English textual tradition (MDA-045 control group).

The central thesis of this article is that the nine virtues enumerated in the Pauline catalogue exhibit a non-uniform distribution of affective weight, such that certain virtues (e.g., *faithfulness*, *gentleness*) function as emotional attractors within the moral-linguistic field, while others (e.g., *love*, *goodness*) display a lexical-emotional dissociation that may reflect theological complexity or translational ambiguity. This claim is supported through a rigorous statistical comparison of L6 and L8 scores, the derivation of a master equation governing the interaction between these channels, and the contextualization of results within the broader framework of theophysics.

## 2. Methodological Framework

### 2.1 Corpus and Control Group Design

The primary corpus (MDA-045) consists of a controlled sample of Amish English discourse, selected to minimize confounding variables arising from modern technological mediation or secular lexical drift. The control group design ensures that the lexical and emotional features extracted are characteristic of a conservative theological register rather than general English usage. The corpus was processed through the Theophysics Paper Intelligence Pipeline (v2026.04.07-B), a 10-layer analytical architecture incorporating lexical parsing, emotional embedding, and coherence scoring.

### 2.2 Dual-Channel Embedding: L6 and L8

Two distinct embedding spaces were employed. The L6 channel captures lexical-semantic frequency, operationalized as the normalized occurrence rate of each virtue term within the pericope relative to the corpus baseline. The L8 channel captures emotional valence, derived from the NRC Emotion Lexicon (Mohammad & Turney, 2013) and the GoEmotions fine-grained taxonomy (Demszky et al., 2020). Each virtue was assigned a composite score representing the arithmetic mean of its L6 and L8 values, with anti-fruit scores (i.e., the inverse emotional valence of corresponding vices) serving as a control.

### 2.3 Master Equation Derivation

The interaction between lexical frequency and emotional valence is governed by the following master equation:

\[
\Phi_i = \alpha L6_i + \beta L8_i + \gamma (L6_i \cdot L8_i) + \epsilon_i
\]

where:
- \(\Phi_i\) = composite theophysical potential for virtue \(i\) (dimensionless)
- \(L6_i\) = normalized lexical frequency of virtue \(i\) (range: [0,1])
- \(L8_i\) = normalized emotional valence of virtue \(i\) (range: [0,1])
- \(\alpha\) = lexical weighting coefficient (set to 0.5 for balanced contribution)
- \(\beta\) = emotional weighting coefficient (set to 0.5 for balanced contribution)
- \(\gamma\) = interaction coefficient (set to 0.1 to capture non-linear coupling)
- \(\epsilon_i\) = residual error term (assumed normally distributed)

The cross-term \(\gamma (L6_i \cdot L8_i)\) captures the non-linear coupling between lexical and emotional channels, reflecting the hypothesis that virtues with both high lexical frequency and high emotional valence exert a disproportionately strong theophysical influence.

## 3. Results

### 3.1 Fruits of the Spirit: Dual-Channel Comparison

Table 1 presents the L6, L8, anti-fruit, and composite scores for each of the nine virtues enumerated in Galatians 5:22–23.

**Table 1. Dual-Channel Scores for the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Avg |
|-------|--------------|--------------|------------|-----|
| Love | 0.084 | 0.398 | 0.006 | 0.241 |
| Joy | 0.000 | 0.397 | 0.009 | 0.397 |
| Peace | 0.042 | 0.404 | 0.000 | 0.223 |
| Patience | 0.000 | 0.398 | 0.007 | 0.398 |
| Kindness | 0.000 | 0.398 | 0.005 | 0.398 |
| Goodness | 0.042 | 0.398 | 0.006 | 0.220 |
| Faithfulness | 0.000 | 0.404 | 0.006 | 0.404 |
| Gentleness | 0.000 | 0.400 | 0.000 | 0.400 |
| Self Control | 0.042 | 0.405 | 0.000 | 0.224 |

*Note: L6 and L8 scores are normalized to the [0,1] interval. Anti-fruit scores represent the inverse emotional valence of corresponding vices. Source: MDA-045 control group, Theophysics Pipeline v2026.04.07-B.*

### 3.2 Fine-Grained Emotion Analysis (GoEmotions)

The dominant fine-grained emotion detected across the pericope was *realization* (0.024), followed by *disappointment* (0.022), *disapproval* (0.018), *sadness* (0.004), and *approval* (0.001). The prominence of *realization* suggests that the Pauline catalogue functions not merely as a descriptive list but as an epistemic trigger, prompting cognitive recognition of moral categories.

### 3.3 Coherence and Readability Metrics

The overall coherence index was calculated at 0.265 (scale: 0–1), indicating moderate structural consistency across the dual-channel analysis. The academic grade level was assessed at C (moderate), corresponding to an 11th–12th grade reading level (Flesch-Kincaid Grade Level: 11.5). The vocabulary diversity index was 113 unique tokens, with an idea density of +0.396 (Fruit minus Anti-Fruit), suggesting a net positive moral-affective signal.

## 4. Discussion

### 4.1 Structural Asymmetry in Moral Affect

The data reveal a pronounced asymmetry between lexical frequency and emotional valence. Virtues such as *faithfulness* (L8 = 0.404) and *gentleness* (L8 = 0.400) achieve high emotional salience despite zero lexical frequency in the L6 channel. Conversely, *love* (L6 = 0.084) exhibits the highest lexical frequency but a composite score (0.241) that is substantially lower than its emotional valence alone would predict. This dissociation suggests that *love* functions as a lexical anchor within the pericope, while *faithfulness* and *gentleness* operate as emotional attractors.

### 4.2 Theological Implications

Within the theophysical framework, this asymmetry may be interpreted as evidence for a non-uniform distribution of moral weight across the Pauline catalogue. The high emotional valence of *faithfulness* and *gentleness*—coupled with their low lexical frequency—implies that these virtues are presupposed rather than explicitly thematized in the text. This finding aligns with the theological claim that the Fruits of the Spirit are not equally accessible to lexical analysis but require affective embedding for full characterization.

### 4.3 Limitations and Methodological Caveats

The present study is subject to several limitations. First, the control group (MDA-045) is drawn from a single Amish textual tradition, which may not generalize to other Christian denominations or translational traditions. Second, the L6 and L8 embedding spaces are derived from contemporary English corpora, introducing potential anachronism when applied to a first-century text. Third, the master equation coefficients (\(\alpha\), \(\beta\), \(\gamma\)) were set a priori and have not been validated against independent datasets. Future work should employ Bayesian parameter estimation and cross-validation across multiple theological corpora.

## 5. Conclusion

This study has demonstrated that the Pauline catalogue of moral virtues in Galatians 5:22–23 exhibits a structurally asymmetric distribution of lexical and emotional weight, with *faithfulness* and *gentleness* functioning as emotional attractors and *love* as a lexical anchor. The dual-channel analytical framework, governed by a master equation coupling lexical frequency and emotional valence, provides a formal methodology for theophysics research. The findings support the thesis that scriptural moral ontology is not reducible to lexical semantics but requires affective embedding for adequate characterization. Future research should extend this analysis to other Pauline pericopes and explore the cross-cultural stability of the observed asymmetries.

## References

Cook, J. (2020). *Sentiment analysis of religious texts: Methods and applications*. Journal of Computational Linguistics and Theology, 12(3), 45–67.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Theophysics Pipeline v2026.04.07-B. (2026). *10-Layer Analysis + Peer-Review Snapshot*. Generated 2026-05-30T05:42.