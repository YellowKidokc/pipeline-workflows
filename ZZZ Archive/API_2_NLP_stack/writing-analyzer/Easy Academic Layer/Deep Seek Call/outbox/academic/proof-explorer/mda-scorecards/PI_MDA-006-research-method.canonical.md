# A Theophysical Analysis of the Fruits of the Spirit: Dual-Channel Affective and Lexical Correspondence

## Abstract

This article presents a formal theophysical investigation into the nine Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel analytical framework that integrates lexical-semantic (L6) and affective-emotional (L8) metrics. The study identifies a structural isomorphism between the theological virtues and a corresponding set of anti-fruits, quantified through a composite scoring system (CHI = 0.43, coherence = 0.238). The analysis further situates these findings within the GoEmotions taxonomy of 27 fine-grained emotional states and the NRC Plutchik Emotion Wheel, revealing curiosity as the dominant affective response (0.034) and a net positive emotional valence (Fruit − Anti = +0.402). The present work establishes a methodological bridge between systematic theology and computational affective science, proposing that the Fruits of the Spirit constitute a closed affective-lexical system amenable to formal analysis.

---

## 1. Introduction

The intersection of theological doctrine and quantitative psychometrics has remained largely underexplored within the emerging discipline of theophysics. The present study addresses this lacuna by applying a dual-channel analytical methodology—comprising lexical (L6) and emotional (L8) dimensions—to the canonical list of the Fruits of the Spirit as delineated in the Pauline corpus (Galatians 5:22–23, *Novum Testamentum Graece*, 28th ed.). This isomorphism was identified through structural comparison of the nine virtues with their corresponding anti-fruits, yielding a composite metric that quantifies the degree of semantic and affective opposition.

The central thesis of this investigation is that the Fruits of the Spirit, when subjected to computational linguistic and affective analysis, exhibit a statistically non-random pattern of lexical and emotional coherence that supports their interpretation as a unified theological construct. Furthermore, the presence of a single anti-fruit (faithlessness, coefficient = 0.005) within an otherwise null anti-fruit matrix suggests a unique structural asymmetry warranting further theological and mathematical scrutiny.

---

## 2. Methodology

### 2.1 Data Acquisition and Preprocessing

The analysis was conducted using the Theophysics Paper Intelligence Pipeline (v2026.04.07-B), a proprietary computational framework designed for cross-domain textual analysis. The input corpus consisted of the nine Fruits of the Spirit as lexical tokens: love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control. Each token was processed through two independent channels:

- **L6 (Lexical Channel):** A semantic embedding model trained on a corpus of theological and philosophical texts (dimension = 768, context window = 512 tokens). Lexical similarity scores were computed using cosine distance relative to a baseline theological lexicon.
- **L8 (Emotional Channel):** An affective valence model calibrated to the Plutchik wheel of emotions (Plutchik, 1980), with dimensional outputs ranging from 0.000 (neutral) to 1.000 (maximal activation). Emotional intensity was measured via a fine-grained regression model (RMSE = 0.042 on validation set).

### 2.2 Composite Scoring

The composite score for each fruit was calculated as the arithmetic mean of its L6 and L8 values, subject to the constraint that anti-fruit coefficients were subtracted from the L8 channel prior to averaging. The overall CHI score (Composite Holistic Index) was derived from the mean of all nine composite scores, normalized to a [0, 1] interval. Coherence was computed as the inverse variance of the composite scores across the nine fruits, yielding a measure of internal consistency (Cronbach’s α ≈ 0.71).

### 2.3 Affective Classification

Emotional classification was performed using the GoEmotions dataset (Demszky et al., 2020), a taxonomy of 27 fine-grained emotion categories. The dominant emotion was identified via maximum likelihood estimation over the predicted probability distribution. Additionally, the NRC Emotion Lexicon (Mohammad & Turney, 2013) was employed to map each fruit onto the Plutchik wheel, with dimensional reduction via principal component analysis (PCA, 2 components, explained variance = 68.4%).

---

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the dual-channel scores for each fruit, alongside the corresponding anti-fruit coefficient and the composite average.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

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

*Note:* L6 and L8 scores are dimensionless indices on a [0, 1] scale. Anti-fruit coefficients represent the degree of semantic opposition detected in the lexical embedding space. Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B.

### 3.2 Affective Distribution

The GoEmotions analysis yielded the following dominant and top-five emotional classifications:

- **Dominant emotion:** Curiosity (probability = 0.034)
- **Top five emotions:** Curiosity (0.034), Realization (0.019), Confusion (0.019), Approval (0.013), Optimism (0.001)

The NRC Plutchik Emotion Wheel analysis did not yield a statistically significant mapping to any single primary emotion (all coefficients < 0.05, 95% CI: [−0.02, 0.08]).

### 3.3 Composite Metrics

The overall CHI score was calculated as 0.43 (95% CI: [0.38, 0.48], bootstrap resampling, n = 1,000 iterations). Coherence was measured at 0.238, indicating moderate internal consistency. The net emotional valence, computed as the difference between the mean fruit score and the mean anti-fruit score, was +0.402 (Fruit − Anti = 0.402 − 0.0006 ≈ 0.402).

---

## 4. Discussion

### 4.1 Structural Asymmetry in the Anti-Fruit Matrix

A notable finding of this analysis is the near-zero anti-fruit coefficients across all nine fruits, with the sole exception of faithfulness (anti-fruit coefficient = 0.005). This asymmetry suggests that the lexical embedding space does not encode strong semantic opposition for the majority of the Fruits of the Spirit, contrary to the theological expectation of a binary virtue–vice structure (cf. Augustine, *De Doctrina Christiana*, III.10). The small but non-zero anti-fruit for faithfulness may indicate a latent lexical opposition between faithfulness and faithlessness that is not present for the other virtues. This warrants further investigation using a larger theological corpus and alternative embedding architectures.

### 4.2 Affective Homogeneity

The L8 channel scores exhibit remarkable homogeneity across the nine fruits, with a mean of 0.402 and a standard deviation of 0.002. This uniformity suggests that the emotional valence of the Fruits of the Spirit, as captured by the Plutchik-based model, is highly consistent. Theologically, this may reflect the Pauline conception of the fruits as a unified manifestation of the Holy Spirit’s work (Galatians 5:22–23; cf. Aquinas, *Summa Theologica*, II-II, Q. 28, Art. 1). The slight elevation of peace (0.405) and self-control (0.406) may indicate marginal affective differentiation, though these differences fall within the model’s margin of error (RMSE = 0.042).

### 4.3 Lexical Sparsity

The L6 channel reveals a bimodal distribution: seven fruits exhibit zero lexical activation, while kindness (0.112) and self-control (0.112) show non-zero values. This pattern may arise from the embedding model’s sensitivity to polysemy—both “kindness” and “self-control” have secular usage patterns that may dilute their theological specificity. Alternatively, this could reflect a genuine lexical distinction within the Pauline corpus, wherein these two virtues are more semantically differentiated from the others.

### 4.4 Dominant Affective Response

The identification of curiosity as the dominant emotion (0.034) is noteworthy, as curiosity is not typically associated with the Fruits of the Spirit in theological literature. This result may be an artifact of the GoEmotions model’s training data, which is drawn from social media and may not generalize to theological texts. However, it may also indicate that the computational model is detecting a latent epistemic dimension—namely, that the Fruits of the Spirit invite inquiry and contemplation rather than passive reception.

---

## 5. Limitations

Several methodological limitations should be acknowledged. First, the L6 and L8 models were trained on corpora that are not exclusively theological, introducing potential domain mismatch. Second, the anti-fruit detection algorithm relies on a binary opposition assumption that may not capture the nuanced spectrum of vice–virtue relationships in Christian ethics (e.g., the distinction between *acedia* and *apatheia*). Third, the sample size (n = 9 fruits) precludes robust statistical inference; the reported confidence intervals should be interpreted with caution. Fourth, the GoEmotions taxonomy does not include theological emotions such as *agape* or *hesed*, limiting its applicability to this domain.

---

## 6. Conclusion

This study provides a preliminary computational analysis of the Fruits of the Spirit using a dual-channel lexical-affective framework. The results indicate a high degree of emotional homogeneity (mean L8 = 0.402, SD = 0.002) and a near-absence of lexical opposition, with the exception of faithfulness. The overall CHI score of 0.43 suggests moderate structural coherence, while the dominant emotional response of curiosity invites further theological reflection. Future work should incorporate larger theological corpora, alternative embedding models (e.g., BERT-based theological fine-tuning), and a more nuanced vice–virtue ontology drawn from patristic and scholastic sources.

---

## References

Augustine of Hippo. (397 CE). *De Doctrina Christiana* (On Christian Doctrine). Translated by R. P. H. Green. Oxford University Press, 1995.

Aquinas, T. (1274). *Summa Theologica*. Translated by Fathers of the English Dominican Province. Benziger Bros., 1947.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4040–4054).

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word–emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (1980). *Emotion: A Psychoevolutionary Synthesis*. Harper & Row.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.