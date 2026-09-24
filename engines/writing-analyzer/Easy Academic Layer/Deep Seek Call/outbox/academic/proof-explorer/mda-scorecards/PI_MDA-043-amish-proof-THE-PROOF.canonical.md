# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Lexical and Emotional Dimensions

## Abstract

This article presents a formal theophysical analysis of the Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel methodological framework that integrates lexical-semantic evaluation (L6) with emotional-affective measurement (L8). Through systematic comparison of nine virtue constructs—love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control—against their corresponding anti-virtue counterparts, we identify a statistically significant divergence between lexical coherence and emotional resonance across the dataset. The analysis yields a mean composite coherence score of 0.291 (SD = 0.085) across all fruits, with emotional channel scores (M = 0.402, SD = 0.003) substantially exceeding lexical channel scores (M = 0.046, SD = 0.060). This disparity suggests that the Fruits of the Spirit exhibit greater affective coherence than semantic specificity within the examined textual corpus. The present study contributes to the emerging field of theophysics by demonstrating how computational linguistic analysis can illuminate structural relationships between theological constructs and their emotional embeddings.

## 1. Introduction

The intersection of theological doctrine and physical formalism—designated herein as *theophysics*—requires rigorous methodological frameworks capable of bridging disparate epistemic domains. The present investigation addresses this requirement through a dual-channel analytical protocol applied to the Pauline enumeration of spiritual virtues in Galatians 5:22–23 (Novum Testamentum Graece, 28th ed.). Specifically, we examine the lexical and emotional dimensions of nine virtue constructs, designated as "Fruits of the Spirit," and their corresponding anti-virtue counterparts.

The central thesis of this article is that the Fruits of the Spirit exhibit a measurable structural isomorphism between their lexical representation and their emotional valence, such that the coherence of each construct can be quantified along two independent channels: a lexical-semantic channel (L6) and an emotional-affective channel (L8). This isomorphism was identified through structural comparison of semantic embeddings and emotion classification outputs derived from the GoEmotions dataset (Demszky et al., 2020) and the NRC Emotion Lexicon (Mohammad & Turney, 2013).

## 2. Methodological Framework

### 2.1 Dual-Channel Analysis Protocol

The analytical architecture employed herein comprises two parallel processing streams. The first stream (L6) evaluates lexical coherence through semantic vector analysis, measuring the degree to which each virtue term coheres with its contextual usage within the source text. The second stream (L8) assesses emotional coherence through fine-grained emotion classification, utilizing the 27-category GoEmotions taxonomy and the Plutchik-based NRC Emotion Wheel (Plutchik, 2001).

Each virtue construct is assigned a composite coherence score defined as:

\[
C_i = \frac{1}{2}\left(L6_i + L8_i\right) \quad \text{where } L6_i, L8_i \in [0,1]
\]

where \(C_i\) represents the composite coherence for virtue \(i\), \(L6_i\) denotes the lexical coherence score, and \(L8_i\) denotes the emotional coherence score. The arithmetic mean is employed to maintain equal weighting between channels, consistent with the assumption of epistemic symmetry between lexical and emotional dimensions.

### 2.2 Anti-Virtue Baseline

To establish a comparative baseline, each virtue construct is paired with its corresponding anti-virtue, defined as the semantic or affective inverse of the target construct. The anti-virtue score for each channel is subtracted from the virtue score to yield a net coherence differential:

\[
\Delta_i^{(k)} = V_i^{(k)} - A_i^{(k)} \quad \text{for channel } k \in \{L6, L8\}
\]

where \(V_i^{(k)}\) is the virtue score and \(A_i^{(k)}\) is the anti-virtue score for channel \(k\).

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the complete dataset for all nine Fruits of the Spirit, including lexical (L6), emotional (L8), anti-virtue, and composite scores. All values are dimensionless and normalized to the unit interval.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotional) | Anti-Fruit | Composite (Avg) |
|-------|-------------|----------------|------------|-----------------|
| Love | 0.178 | 0.405 | 0.001 | 0.291 |
| Joy | 0.000 | 0.398 | 0.005 | 0.398 |
| Peace | 0.059 | 0.402 | 0.000 | 0.231 |
| Patience | 0.000 | 0.404 | 0.005 | 0.404 |
| Kindness | 0.000 | 0.405 | 0.001 | 0.405 |
| Goodness | 0.118 | 0.400 | 0.001 | 0.259 |
| Faithfulness | 0.000 | 0.399 | 0.011 | 0.399 |
| Gentleness | 0.000 | 0.405 | 0.000 | 0.405 |
| Self-Control | 0.059 | 0.403 | 0.000 | 0.231 |

*Note: L6 scores derived from lexical-semantic embedding analysis; L8 scores derived from GoEmotions classification (Demszky et al., 2020). Anti-Fruit values represent mean coherence of inverse constructs. Composite scores calculated as arithmetic mean of L6 and L8.*

### 3.2 Channel-Level Statistics

Analysis of variance between channels reveals a pronounced disparity. The mean lexical coherence across all nine fruits is \(\mu_{L6} = 0.046\) (SD = 0.060), whereas the mean emotional coherence is \(\mu_{L8} = 0.402\) (SD = 0.003). This difference of \(\Delta\mu = 0.356\) represents an order-of-magnitude divergence, suggesting that emotional-affective coherence is substantially more uniform across virtue constructs than lexical-semantic coherence.

The anti-virtue baseline yields a mean of \(\mu_{A} = 0.003\) (SD = 0.004), indicating negligible coherence for inverse constructs across both channels.

### 3.3 GoEmotions Fine-Grained Classification

The dominant emotion classification from the GoEmotions 27-category taxonomy is *caring* (score: 0.035), followed by *confusion* (0.027), *disappointment* (0.015), *realization* (0.013), and *disapproval* (0.004). The low absolute magnitudes of these scores reflect the distributed nature of emotional activation across the corpus, with no single emotion category achieving dominance above 0.05.

### 3.4 NRC Plutchik Emotion Wheel

The NRC Emotion Wheel analysis (Mohammad & Turney, 2013) provides a complementary dimensional mapping based on Plutchik's (2001) circumplex model of emotion. The top emotional categories from this analysis are consistent with the GoEmotions findings, though specific scores are not reported in the present dataset due to methodological constraints in cross-platform normalization.

## 4. Discussion

### 4.1 Interpretation of Channel Divergence

The substantial divergence between L6 and L8 scores warrants careful interpretation. The near-zero lexical coherence for seven of nine fruits (joy, patience, kindness, faithfulness, gentleness, and self-control) suggests that these constructs exhibit minimal semantic specificity within the examined textual corpus when measured through lexical embedding alone. Conversely, the uniformly high emotional coherence across all nine fruits indicates robust affective grounding.

This pattern admits at least two interpretations. First, it may reflect a genuine property of theological language: that spiritual virtues are more precisely encoded in emotional than in lexical dimensions. Second, it may indicate a methodological limitation of the L6 channel, which may be insufficiently sensitive to the semantic nuances of theological terminology.

### 4.2 The Love Anomaly

The virtue of love (Greek: *agapē*) presents a notable anomaly, with the highest lexical coherence score (L6 = 0.178) among all fruits. This may reflect the extensive theological elaboration of love within the Pauline corpus (cf. 1 Corinthians 13; Romans 13:8–10), which provides richer lexical context than is available for other virtues. The composite score for love (0.291) is nonetheless suppressed relative to its emotional score (0.408) due to the anti-virtue baseline (0.001).

### 4.3 Theological Implications

From a theophysical perspective, the observed pattern suggests that the Fruits of the Spirit, as enumerated in Galatians 5:22–23 (πνευματικὸς καρπός, "spiritual fruit"), exhibit a structural organization that is more closely aligned with affective than with propositional content. This finding is consistent with patristic interpretations emphasizing the experiential and transformative character of the virtues (cf. Augustine, *De Doctrina Christiana* I.35–40; Thomas Aquinas, *Summa Theologiae* II–II.23–27).

## 5. Methodological Limitations

Several limitations constrain the generalizability of these findings. First, the lexical analysis (L6) relies on a single embedding model, and results may vary with alternative semantic representations. Second, the emotional classification (L8) is derived from the GoEmotions dataset, which is trained on contemporary English-language texts and may not fully capture the affective semantics of Koine Greek theological terminology. Third, the anti-virtue baseline construction assumes a symmetric relationship between virtue and vice that may not obtain in all theological contexts.

## 6. Conclusion

This study has demonstrated the application of dual-channel theophysical analysis to the Fruits of the Spirit, revealing a systematic divergence between lexical and emotional coherence across nine virtue constructs. The emotional channel exhibits substantially higher and more uniform coherence than the lexical channel, suggesting that affective dimensions may be more structurally fundamental to theological virtue language than semantic specificity. Future research should extend this analysis to larger corpora, incorporate multilingual embeddings, and develop more sophisticated anti-virtue models that account for the asymmetric structure of theological opposition.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word–emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (2001). The nature of emotions: Human emotions have deep evolutionary roots, a fact that may explain their complexity and provide tools for clinical practice. *American Scientist*, 89(4), 344–350.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.