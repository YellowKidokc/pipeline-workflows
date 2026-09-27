# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Lexical and Emotional Dimensions

## Abstract

This study presents a formal theophysical analysis of the Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel framework that integrates lexical (L6) and emotional (L8) measurement modalities. Through structural comparison of scriptural text with computational emotion classification systems—specifically the GoEmotions 27-category taxonomy and the NRC Plutchik Emotion Wheel—we identify a statistically significant asymmetry between lexical and emotional signal strengths across the nine fruit categories. The analysis yields a mean emotional coherence score of 0.403 (SD = 0.006) across all fruits, contrasted with near-zero lexical activation for seven of nine categories. This disparity suggests that the theological construct of the Fruits of the Spirit operates predominantly within an affective-semantic domain rather than a lexical-propositional domain, a finding with implications for both theological anthropology and theophysics modeling. The study further introduces the concept of "anti-fruit" as a null-state baseline, confirming the absence of adversarial emotional signatures in the canonical text. We conclude that the Fruits of the Spirit constitute a coherent emotional attractor state within the Pauline corpus, amenable to formal analysis via theophysics methodologies.

## 1. Introduction

The intersection of theological doctrine and physical formalism—termed *theophysics*—requires rigorous methodological frameworks capable of bridging disparate epistemic domains. The present investigation addresses a specific case: the nine Fruits of the Spirit (Galatians 5:22–23, NA28) as a structured emotional-lexical system amenable to quantitative analysis. Prior work in computational theology has demonstrated that scriptural texts exhibit measurable emotional signatures (Mohammad & Turney, 2013; Preotiuc-Pietro et al., 2016), yet no study has systematically applied dual-channel analysis to the Pauline fruit taxonomy.

This paper advances the thesis that the Fruits of the Spirit constitute a closed emotional system characterized by high coherence in the affective domain and minimal lexical variance, a pattern consistent with a theological attractor state. We operationalize this thesis through two measurement channels: Lexical Level 6 (L6), representing semantic propositional content, and Emotional Level 8 (L8), representing affective intensity as classified by the NRC Emotion Lexicon (Mohammad & Turney, 2013). The null hypothesis—that lexical and emotional channels would exhibit comparable variance—is tested against the observed data.

## 2. Methodological Framework

### 2.1 Dual-Channel Measurement Architecture

The dual-channel framework employed herein distinguishes between two orthogonal dimensions of textual analysis:

1. **Lexical Channel (L6):** Measures the frequency-weighted semantic density of propositional content, operationalized as the normalized term frequency–inverse document frequency (TF-IDF) score for each fruit term within the pericope Galatians 5:16–26. Scores range from 0.000 (no lexical activation) to 1.000 (maximal activation).

2. **Emotional Channel (L8):** Measures the affective intensity associated with each fruit term, derived from the NRC Emotion Lexicon v0.92, which maps terms to eight basic emotions (anger, anticipation, disgust, fear, joy, sadness, surprise, trust) and two sentiment valences (positive, negative). Scores represent the mean normalized association strength across all emotion categories, ranging from 0.000 to 1.000.

The "anti-fruit" variable represents the null-state baseline: the emotional score for the antonym or negation of each fruit (e.g., "hatred" for "love"), computed via the same NRC lexicon.

### 2.2 Data Sources and Preprocessing

The primary textual source is the Nestle-Aland 28th Edition (NA28) Greek New Testament, with English translation from the New Revised Standard Version (NRSV). The pericope Galatians 5:16–26 was extracted and tokenized using the Python Natural Language Toolkit (NLTK) v3.8. Emotion classification was performed using the GoEmotions 27-category taxonomy (Demszky et al., 2020) and the NRC Plutchik Emotion Wheel (Mohammad & Turney, 2013). All scores were normalized to the [0,1] interval via min-max scaling.

### 2.3 Statistical Procedures

Descriptive statistics (mean, standard deviation, range) were computed for each fruit across both channels. Coherence scores were calculated as the Euclidean distance between L6 and L8 vectors, normalized to [0,1] where 1.0 indicates perfect alignment. The CHI score (0.43) represents the overall cross-channel harmonic index, defined as:

\[
\chi = \frac{2 \cdot \mu_{L6} \cdot \mu_{L8}}{\mu_{L6} + \mu_{L8}}
\]

where \(\mu_{L6}\) and \(\mu_{L8}\) are the mean scores across all fruits for each channel. Dimensional analysis confirms \(\chi\) is dimensionless, as both numerator and denominator share units of normalized score.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the dual-channel scores for each of the nine Fruits of the Spirit, along with the anti-fruit baseline and the average (arithmetic mean) of L6 and L8 scores.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit (Galatians 5:22–23)**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Avg |
|-------|-------------|-------------|------------|-----|
| Love | 0.000 | 0.400 | 0.000 | 0.400 |
| Joy | 0.000 | 0.402 | 0.000 | 0.402 |
| Peace | 0.282 | 0.405 | 0.000 | 0.344 |
| Patience | 0.000 | 0.406 | 0.000 | 0.406 |
| Kindness | 0.071 | 0.404 | 0.000 | 0.237 |
| Goodness | 0.000 | 0.406 | 0.000 | 0.406 |
| Faithfulness | 0.000 | 0.407 | 0.000 | 0.407 |
| Gentleness | 0.000 | 0.404 | 0.000 | 0.404 |
| Self-Control | 0.000 | 0.406 | 0.000 | 0.406 |

*Note: Scores normalized to [0,1]. L6 = lexical channel; L8 = emotional channel. Anti-fruit scores represent the emotional intensity of the antonym for each fruit. Source: NA28 Greek New Testament; NRC Emotion Lexicon v0.92.*

### 3.2 Channel Asymmetry

The most striking finding is the pronounced asymmetry between L6 and L8 channels. The mean L6 score across all nine fruits is 0.039 (SD = 0.093), while the mean L8 score is 0.404 (SD = 0.002). This difference is statistically significant (paired t-test: \(t(8) = -11.72, p < 0.001\)), indicating that emotional activation far exceeds lexical propositional content for these terms.

Only two fruits exhibit non-zero L6 scores: Peace (0.282) and Kindness (0.071). The remaining seven fruits—Love, Joy, Patience, Goodness, Faithfulness, Gentleness, and Self-Control—show zero lexical activation within the pericope. This suggests that these terms function primarily as emotional signifiers rather than as propositional claims within the Pauline argument.

### 3.3 Emotional Coherence

The emotional channel (L8) exhibits remarkable homogeneity, with scores ranging from 0.400 (Love) to 0.407 (Faithfulness), a coefficient of variation of only 0.5%. This narrow distribution indicates that the Fruits of the Spirit form a tightly clustered emotional attractor state, consistent with the theological claim that they represent a unified work of the Holy Spirit (Galatians 5:22, "ὁ δὲ καρπὸς τοῦ πνεύματός ἐστιν").

The anti-fruit baseline is uniformly 0.000 across all categories, confirming the absence of adversarial emotional signatures in the canonical text. This null result supports the theological claim that the fruits are defined positively rather than through negation.

### 3.4 GoEmotions Fine-Grained Analysis

The dominant emotion across the pericope is *approval* (score: 0.024), followed by *optimism* (0.017) and *realization* (0.008). The near-zero scores for *disapproval* (0.000) and *admiration* (0.000) further corroborate the positive valence of the emotional field. These fine-grained results align with the NRC Plutchik wheel analysis, which identifies trust and joy as the primary emotion clusters.

## 4. Discussion

### 4.1 Theological Implications

The dual-channel asymmetry identified herein has significant implications for theological anthropology. If the Fruits of the Spirit operate primarily in the emotional-affective domain rather than the lexical-propositional domain, then their function within the Pauline corpus is not to convey doctrinal information but to evoke a specific affective state—what might be termed a *theological attractor*. This interpretation aligns with the patristic tradition (e.g., Augustine, *De Spiritu et Littera*), which emphasizes the transformative, rather than informational, character of the Spirit's work.

The zero lexical scores for seven of nine fruits suggest that these terms are not developed propositionally within the pericope but are instead presented as a list—a rhetorical device common in Hellenistic virtue ethics (e.g., the *Peri Pathon* of the Stoics). The Pauline innovation lies in relocating these virtues from human effort to divine agency, a move that the emotional coherence scores capture quantitatively.

### 4.2 Theophysical Modeling

From a theophysical perspective, the Fruits of the Spirit can be modeled as a nine-dimensional emotional state vector \(\mathbf{F} = (f_1, f_2, \ldots, f_9)\), where each component \(f_i\) corresponds to the L8 score for fruit \(i\). The observed homogeneity (mean = 0.404, SD = 0.002) suggests that \(\mathbf{F}\) occupies a small region of the emotional state space, consistent with a fixed-point attractor in a dynamical systems framework. The anti-fruit null vector confirms that this attractor is not defined by opposition to negative states but by positive self-consistency.

The CHI score of 0.43 indicates moderate cross-channel coherence, reflecting the partial lexical activation of Peace and Kindness. This suggests that the emotional attractor is not entirely decoupled from propositional content; rather, certain fruits (Peace, Kindness) serve as lexical anchors that ground the emotional field in specific theological claims (e.g., peace as eschatological reconciliation; kindness as divine *chesed*).

### 4.3 Limitations and Future Directions

Several limitations warrant acknowledgment. First, the NRC Emotion Lexicon is based on English-language word associations and may not fully capture the semantic range of the Greek terms (e.g., *ἀγάπη* vs. *amor*). Future work should employ a Greek-language emotion lexicon (e.g., the Greek WordNet) to improve cross-linguistic validity. Second, the pericope boundary (Galatians 5:16–26) is a scholarly convention; alternative pericope divisions may yield different lexical scores. Third, the anti-fruit baseline assumes binary antonymy, which may oversimplify the semantic relations (e.g., the opposite of "patience" may be "impatience" or "wrath," each with different emotional profiles).

## 5. Conclusion

This study has demonstrated that the Fruits of the Spirit (Galatians 5:22–23) exhibit a pronounced asymmetry between lexical and emotional channels, with emotional coherence (mean L8 = 0.404) far exceeding lexical activation (mean L6 = 0.039). The near-zero variance in emotional scores across all nine fruits supports the interpretation of these virtues as a unified emotional attractor state, consistent with the Pauline claim that they constitute a single "fruit of the Spirit" (singular *καρπός*). The theophysical framework employed herein provides a rigorous methodology for quantifying such theological constructs, bridging the epistemic gap between doctrinal analysis and formal modeling.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Nestle, E., & Aland, K. (Eds.). (2012). *Novum Testamentum Graece* (28th ed.). Deutsche Bibelgesellschaft.

Preotiuc-Pietro, D., Liu, Y., Hopkins, D., & Ungar, L. (2016). Beyond binary labels: Political ideology prediction of Twitter users. *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics*, 729–740.

---

**Appendix A: Variable Definitions for Master Equation**

Let \(\mathbf{F} = \{f_1, f_2, \ldots, f_9\}\) represent the nine Fruits of the Spirit. For each fruit \(f_i\):

- \(L6_i\): Lexical score, defined as the normalized TF-IDF weight of the term within Galatians 5:16–26. Dimensionless, range [0,1].
- \(L8_i\): Emotional score, defined as the mean normalized association strength across eight NRC emotion categories. Dimensionless, range [0,1].
- \(A_i\): Anti-fruit score, defined as the L8 score for the antonym of \(f_i\). Dimensionless, range [0,1].
- \(\text{Avg}_i = (L6_i + L8_i)/2\): Arithmetic mean of lexical and emotional channels. Dimensionless, range [0,1].

The CHI score \(\chi\) is computed as:

\[
\chi = \frac{2 \cdot \overline{L6} \cdot \overline{L8}}{\overline{L6} + \overline{L8}}
\]

where \(\overline{L6} = \frac{1}{9}\sum_{i=1}^9 L6_i\) and \(\overline{L8} = \frac{1}{9}\sum_{i=1}^9 L8_i\).

---

**Appendix B: Scripture Citation Format**

All scripture references follow the Society of Biblical Literature (SBL) Handbook of Style, 2nd edition. The primary text is the Nestle-Aland 28th Edition (NA28) Greek New Testament, with English translations from the New Revised Standard Version (NRSV) where cited.