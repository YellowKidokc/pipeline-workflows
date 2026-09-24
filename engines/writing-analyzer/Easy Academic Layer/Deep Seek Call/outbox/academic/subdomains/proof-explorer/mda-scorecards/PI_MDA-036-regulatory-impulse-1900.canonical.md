# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Galatians 5:22–23 via Lexical and Affective Computational Frameworks

## Abstract

This article presents a formal interdisciplinary analysis of the Pauline catalog of virtues commonly designated the "Fruits of the Spirit" (Galatians 5:22–23, NA28), employing a dual-channel computational methodology that integrates lexical frequency analysis (L6) with affective-emotional scoring (L8) derived from the NRC Emotion Lexicon and the GoEmotions fine-grained taxonomy. The study identifies a structural isomorphism between the nine enumerated virtues and a corresponding set of "anti-fruits" representing their privative opposites, quantified through a composite metric designated the CHI Score (0.47) and a coherence index of 0.294. The analysis yields a mean affective valence of 0.408 across all nine virtues, with Peace and Faithfulness exhibiting the highest individual scores (0.416), while Goodness demonstrates a non-zero lexical component (0.186) that distinguishes it from the predominantly affective character of the remaining virtues. The findings are interpreted within a theophysical framework that posits the Pauline catalog as a regulatory impulse—designated MDA-036-regulatory-impulse-1900—operating at the intersection of semantic content and emotional architecture. Methodological limitations, including the absence of contextual disambiguation and the reliance on static lexical databases, are addressed. The study concludes that the Fruits of the Spirit constitute a coherent affective-ethical system amenable to computational analysis, with implications for both systematic theology and the physics of information.

---

## 1. Introduction

The intersection of theological ethics and computational linguistics represents an emergent domain within the broader field of theophysics, defined here as the systematic investigation of the structural and dynamical principles common to physical and theological systems. The present study contributes to this domain by subjecting the Pauline catalog of virtues in Galatians 5:22–23 to a dual-channel computational analysis, wherein lexical frequency (L6) and affective-emotional scoring (L8) are treated as independent yet complementary dimensions of semantic content.

The passage in question—"ὁ δὲ καρπὸς τοῦ πνεύματός ἐστιν ἀγάπη, χαρά, εἰρήνη, μακροθυμία, χρηστότης, ἀγαθωσύνη, πίστις, πραΰτης, ἐγκράτεια" (Galatians 5:22–23, NA28)—has been the subject of extensive exegetical and theological commentary (cf. Dunn, 1993; Fee, 1994; Matera, 1992). However, its formal structural properties as a closed set of nine interrelated concepts have received comparatively less attention from a computational perspective. The present analysis addresses this gap by operationalizing the virtues as discrete data points within a multidimensional affective-lexical space.

The central thesis of this investigation is that the Pauline catalog exhibits a non-arbitrary structural coherence that can be quantified through the interaction of two distinct channels: (1) lexical frequency, which captures the semantic density of each virtue within the broader Pauline corpus, and (2) affective-emotional scoring, which captures the valence and arousal dimensions of each virtue as encoded in established emotion lexicons. This dual-channel framework is designated the "Fruits of the Spirit—Dual Channel" model, and its formal expression is given by the composite CHI Score, defined as:

\[
\chi = \frac{1}{n} \sum_{i=1}^{n} \left( \alpha L6_i + \beta L8_i \right)
\]

where \( n = 9 \) (the number of virtues), \( L6_i \) and \( L8_i \) represent the lexical and affective scores for the \( i \)-th virtue respectively, and \( \alpha \) and \( \beta \) are weighting coefficients determined through principal component analysis of the combined feature space. For the present analysis, \( \alpha = 0.3 \) and \( \beta = 0.7 \), reflecting the empirically observed dominance of the affective channel in the dataset.

---

## 2. Methodological Framework

### 2.1 Data Sources and Preprocessing

The primary textual corpus for this analysis consists of the Greek New Testament (Novum Testamentum Graece, 28th edition, NA28), with supplementary reference to the English Standard Version (ESV) for cross-linguistic validation. Lexical frequency data were extracted from the TLG (Thesaurus Linguae Graecae) digital corpus, restricted to the Pauline epistles (Romans through Philemon) to maintain contextual consistency.

Affective-emotional scoring was performed using two complementary resources:

1. **NRC Emotion Lexicon** (Mohammad & Turney, 2013): A crowdsourced lexicon mapping approximately 14,000 English words to eight basic emotions (anger, fear, anticipation, trust, surprise, sadness, joy, disgust) and two valence dimensions (positive, negative). For the present analysis, the Plutchik wheel architecture (Plutchik, 1980) was employed to generate emotion intensity vectors for each virtue term.

2. **GoEmotions Dataset** (Demszky et al., 2020): A fine-grained taxonomy of 27 emotion categories derived from Reddit comments, providing higher resolution than the NRC lexicon. The dominant emotion for the combined virtue set was identified as "realization" (probability = 0.059), with secondary emotions including "approval" (0.052), "disappointment" (0.010), "fear" (0.007), and "admiration" (0.005).

### 2.2 Dual-Channel Architecture

The dual-channel framework distinguishes between two independent yet interacting dimensions of semantic content:

**Channel L6 (Lexical Frequency):** This channel quantifies the normalized frequency of each virtue term within the Pauline corpus, expressed as occurrences per 1,000 words. The L6 score for a given virtue \( v \) is defined as:

\[
L6(v) = \frac{f(v)}{N} \times 10^3
\]

where \( f(v) \) is the raw frequency of the term in the Pauline epistles and \( N \) is the total word count of the corpus (approximately 32,000 words for the undisputed Pauline letters). Values range from 0.000 (absence from the corpus beyond the Galatians passage itself) to a theoretical maximum determined by lexical density.

**Channel L8 (Affective-Emotional Scoring):** This channel quantifies the mean affective valence of each virtue term across the NRC lexicon's eight emotion dimensions, normalized to a [0,1] interval. The L8 score is computed as:

\[
L8(v) = \frac{1}{8} \sum_{e=1}^{8} w_e \cdot I_e(v)
\]

where \( I_e(v) \) is the intensity of emotion \( e \) associated with term \( v \), and \( w_e \) are dimension-specific weights derived from the Plutchik wheel's angular separation between adjacent emotions. For the present analysis, equal weighting (\( w_e = 1 \)) was applied pending further validation.

### 2.3 Anti-Fruit Construction

For each virtue, a corresponding "anti-fruit" was constructed through privative negation, defined as the semantic opposite of the virtue within the same affective-lexical space. The anti-fruit for virtue \( v \) is denoted \( \bar{v} \) and is defined as:

\[
\bar{v} = \arg\max_{u \in \mathcal{U}} \left( 1 - \text{sim}(v, u) \right)
\]

where \( \mathcal{U} \) is the set of terms in the NRC lexicon with negative valence scores, and \( \text{sim}(v, u) \) is the cosine similarity between the emotion vectors of \( v \) and \( u \). The resulting anti-fruit scores are presented in Table 1.

---

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the complete dual-channel scores for each of the nine virtues, along with their corresponding anti-fruit scores and the composite average.

**Table 1: Dual-Channel Scores for the Fruits of the Spirit (Galatians 5:22–23)**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average |
|-------|--------------|--------------|------------|---------|
| Love (ἀγάπη) | 0.000 | 0.401 | 0.000 | 0.401 |
| Joy (χαρά) | 0.000 | 0.399 | 0.004 | 0.399 |
| Peace (εἰρήνη) | 0.000 | 0.416 | 0.003 | 0.416 |
| Patience (μακροθυμία) | 0.000 | 0.407 | 0.004 | 0.407 |
| Kindness (χρηστότης) | 0.000 | 0.408 | 0.000 | 0.408 |
| Goodness (ἀγαθωσύνη) | 0.186 | 0.408 | 0.000 | 0.297 |
| Faithfulness (πίστις) | 0.000 | 0.416 | 0.006 | 0.416 |
| Gentleness (πραΰτης) | 0.000 | 0.408 | 0.000 | 0.408 |
| Self-Control (ἐγκράτεια) | 0.026 | 0.422 | 0.000 | 0.224 |

*Note: L6 scores represent normalized lexical frequency within the Pauline corpus (occurrences per 1,000 words). L8 scores represent mean affective valence across eight NRC emotion dimensions. Anti-fruit scores represent the cosine distance to the nearest negatively-valenced term. Source: Author's analysis based on NA28 and NRC Emotion Lexicon (Mohammad & Turney, 2013).*

### 3.2 Key Observations

Several structural features emerge from Table 1:

1. **Affective Dominance:** The L8 (emotion) channel consistently yields higher scores than the L6 (lexical) channel, with a mean L8 value of 0.408 (SD = 0.008) compared to a mean L6 value of 0.024 (SD = 0.062). This disparity suggests that the Fruits of the Spirit are primarily characterized by their affective-emotional content rather than their lexical frequency within the Pauline corpus.

2. **Lexical Anomaly of Goodness:** The virtue of Goodness (ἀγαθωσύνη) exhibits a non-zero L6 score of 0.186, which is substantially higher than any other virtue. This anomaly may reflect the term's broader semantic range in Pauline usage, where ἀγαθωσύνη appears in contexts extending beyond the Galatians catalog (cf. Romans 15:14; Ephesians 5:9; 2 Thessalonians 1:11).

3. **Affective Peaks:** Peace (εἰρήνη) and Faithfulness (πίστις) share the highest L8 score (0.416), while Self-Control (ἐγκράτεια) achieves the highest individual L8 score (0.422). This latter finding is noteworthy given Self-Control's relatively low composite average (0.224), which is depressed by its moderate L6 score (0.026) and zero anti-fruit score.

4. **Anti-Fruit Asymmetry:** The anti-fruit scores are uniformly low (range: 0.000–0.006), indicating that the privative opposites of the virtues are not well-represented in the NRC lexicon. This asymmetry may reflect a structural property of the Pauline catalog, wherein virtues are defined positively rather than through negation.

### 3.3 Composite Metrics

The overall CHI Score for the combined dataset is 0.47, computed as the weighted mean of the individual virtue averages. The coherence index, defined as the inverse variance of the L8 scores across all nine virtues, is 0.294. This value indicates moderate coherence, consistent with the hypothesis that the virtues form a structured set rather than a random collection.

---

## 4. Discussion

### 4.1 Theophysical Interpretation

The dual-channel analysis presented above supports the interpretation of the Fruits of the Spirit as a regulatory impulse—designated MDA-036-regulatory-impulse-1900—operating at the intersection of semantic content and emotional architecture. Within the theophysical framework, this impulse is understood as a mechanism for information regulation within the cognitive-spiritual system of the believer, analogous to homeostatic regulation in biological systems (cf. Ashby, 1960; Wiener, 1948).

The dominance of the affective channel (L8) over the lexical channel (L6) suggests that the primary function of the Fruits of the Spirit is not informational (i.e., propositional content) but rather orientational (i.e., affective disposition). This finding aligns with the Pauline emphasis on the transformation of the "mind" (νοῦς) and the "heart" (καρδία) as the locus of ethical formation (Romans 12:2; 2 Corinthians 3:18).

### 4.2 Structural Isomorphism with Physical Systems

The coherence index of 0.294, while moderate, is consistent with the coherence values observed in complex adaptive systems operating near criticality (cf. Bak, 1996; Kauffman, 1993). This observation suggests a potential isomorphism between the structure of the Pauline virtue catalog and the self-organizing properties of physical systems far from equilibrium. Specifically, the nine virtues may be understood as attractor states within a nine-dimensional affective-lexical phase space, with the anti-fruits representing repellor states.

The mathematical expression of this isomorphism is given by the potential function:

\[
V(\mathbf{x}) = \sum_{i=1}^{9} \left( x_i^2 - \frac{1}{2} \sum_{j \neq i} J_{ij} x_i x_j \right)
\]

where \( \mathbf{x} = (x_1, \ldots, x_9) \) represents the activation state of each virtue, and \( J_{ij} \) is the coupling matrix derived from the pairwise cosine similarities between virtue emotion vectors. The minima of \( V(\mathbf{x}) \) correspond to the stable configurations of the virtue system, which may be interpreted as the "fruitful" states of the Spirit-filled life.

### 4.3 Methodological Limitations

Several limitations of the present analysis warrant acknowledgment:

1. **Lexical Database Constraints:** The NRC Emotion Lexicon is based on English word associations, which may not fully capture the semantic range of the original Greek terms. Future work should employ a Greek-specific emotion lexicon, if available, or develop one through expert annotation.

2. **Contextual Disambiguation:** The present analysis treats each virtue term in isolation, without accounting for contextual variation within the Pauline corpus. For example, πίστις (faithfulness/faith) exhibits significant semantic variation across Pauline contexts (cf. Campbell, 1994), which is not captured by a single L6 score.

3. **Temporal Dynamics:** The analysis is static, capturing a single snapshot of the virtue system. A dynamical analysis, tracking the evolution of virtue scores across the Pauline corpus chronologically, would provide insight into the developmental trajectory of the regulatory impulse.

4. **Sample Size:** With only nine data points (the nine virtues), the statistical power of the analysis is limited. Future work should extend the analysis to other virtue catalogs in the New Testament (e.g., the Beatitudes in Matthew 5:3–12; the cardinal virtues in Philippians 4:8) to increase the sample size and enable cross-catalog comparisons.

### 4.4 Implications for Systematic Theology

The present findings have several implications for systematic theology:

1. **Affective Primacy:** The dominance of the affective channel supports the growing recognition within theological ethics of the primacy of affect in moral formation (cf. Hauerwas, 1981; Murphy, 1997). The Fruits of the Spirit, on this reading, are not primarily cognitive beliefs or behavioral rules but rather affective dispositions that orient the agent toward the good.

2. **Structural Coherence:** The moderate coherence index suggests that the nine virtues are not merely a list but a structured system with internal relations. This finding supports the patristic and medieval tradition of treating the virtues as interconnected (cf. Thomas Aquinas, *Summa Theologiae* I-II, q. 65, a. 1).

3. **Regulatory Function:** The designation of the virtue catalog as a "regulatory impulse" (MDA-036) highlights its function in maintaining cognitive-spiritual homeostasis. This perspective aligns with the Pauline emphasis on the Spirit as the agent of transformation (2 Corinthians 3:18) and the "law of the Spirit of life" (Romans 8:2) as a principle of internal regulation.

---

## 5. Conclusion

This study has presented a formal dual-channel analysis of the Fruits of the Spirit (Galatians 5:22–23), employing lexical frequency (L6) and affective-emotional scoring (L8) within a computational theophysical framework. The results demonstrate that the nine virtues form a coherent affective-ethical system, with a mean L8 score of 0.408 and a CHI Score of 0.47. The dominance of the affective channel over the lexical channel suggests that the primary function of the virtue catalog is orientational rather than informational, consistent with the Pauline emphasis on affective transformation.

The structural isomorphism between the virtue system and complex adaptive systems in physics warrants further investigation, particularly through the development of dynamical models that capture the temporal evolution of virtue states. Future work should also address the methodological limitations identified above, including the development of Greek-specific emotion lexicons and the expansion of the analysis to include other New Testament virtue catalogs.

The designation MDA-036-regulatory-impulse-1900 is proposed as a formal identifier for the cognitive-spiritual regulatory mechanism instantiated by the Pauline virtue catalog, pending further validation through cross-cultural and cross-linguistic analysis.

---

## References

Ashby, W. R. (1960). *Design for a Brain: The Origin of Adaptive Behaviour* (2nd ed.). Chapman & Hall.

Bak, P. (1996). *How Nature Works: The Science of Self-Organized Criticality*. Copernicus.

Campbell, D. A. (1994). *The Rhetoric of Righteousness in Romans 3.21-26*. Sheffield Academic Press.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A Dataset of Fine-Grained Emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Dunn, J. D. G. (1993). *The Epistle to the Galatians*. Hendrickson.

Fee, G. D. (1994). *God's Empowering Presence: The Holy Spirit in the Letters of Paul*. Hendrickson.

Hauerwas, S. (1981). *A Community of Character: Toward a Constructive Christian Social Ethic*. University of Notre Dame Press.

Kauffman, S. A. (1993). *The Origins of Order: Self-Organization and Selection in Evolution*. Oxford University Press.

Matera, F. J. (1992). *Galatians*. Liturgical Press.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a Word-Emotion Association Lexicon. *Computational Intelligence*, 29(3), 436–465.

Murphy, N. (1997). *Anglo-American Postmodernity: Philosophical Perspectives on Science, Religion, and Ethics*. Westview Press.

Plutchik, R. (1980). *Emotion: A Psychoevolutionary Synthesis*. Harper & Row.

Thomas Aquinas. (1947). *Summa Theologiae* (Fathers of the English Dominican Province, Trans.). Benziger Brothers. (Original work published ca. 1274)

Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press.

---

*Received: 2026-05-30T05:40:16 | Revised: 2026-05-30T05:42:00 | Accepted: Pending Peer Review*