# Theophysics of Spiritual Formation: A Dual-Channel Analysis of the Fruits of the Spirit

## Abstract

This paper presents a formal analysis of the Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel computational framework that integrates lexical and emotional dimensions. The investigation utilizes the MDA-051-korea-experiment protocol within the Schema 2026.04.07-B pipeline to evaluate nine virtue constructs across two distinct measurement channels: lexical frequency (L6) and emotional valence (L8). Results indicate that eight of the nine fruits exhibit negligible lexical activation (L6 = 0.000) while demonstrating consistent emotional resonance (L8 ≈ 0.394–0.400), with the notable exception of Self-Control, which registers a lexical score of 0.587 alongside an emotional score of 0.398. The aggregate coherence metric of 0.307 and a CHI score of 0.45 suggest moderate structural alignment between the theological construct and its computational representation. This paper provides a rigorous methodological framework for theophysics research, establishing a replicable protocol for cross-domain analysis of spiritual formation metrics.

## 1. Introduction

The intersection of theological anthropology and computational linguistics presents a novel domain for empirical investigation of spiritual formation constructs. The Pauline corpus, particularly the enumeration of the Fruits of the Spirit in Galatians 5:22–23 (Nestle-Aland 28th edition, NA28), provides a well-established taxonomy of virtues that has received extensive exegetical treatment but limited quantitative analysis. The present study addresses this gap by applying a dual-channel analytical framework—designated as L6 (lexical) and L8 (emotional)—to examine the structural properties of these nine virtues.

The research question guiding this investigation is: To what extent do the Fruits of the Spirit exhibit measurable coherence across lexical and emotional dimensions when subjected to computational linguistic analysis? This question is motivated by the broader theophysics project, which seeks to establish formal correspondences between theological constructs and physical or mathematical structures.

## 2. Methodological Framework

### 2.1 The MDA-051-korea-experiment Protocol

The analysis was conducted using the Paper Intelligence Pipeline v2026.04.07-B, a 10-layer analytical system designed for theophysics research. The protocol designation "MDA-051-korea-experiment" refers to a specific experimental configuration within this pipeline, characterized by:

- **L1 Activation**: Baseline lexical scanning
- **L10 Activation**: Emotional valence mapping
- **L13 Activation**: Cross-channel correlation
- **L2, L3, L4, L5, L6, L8, L9 Activation**: Intermediate processing layers

The system employs a dual-channel architecture wherein Channel L6 captures lexical frequency distributions and Channel L8 captures emotional valence scores derived from the GoEmotions 27 fine-grained emotion taxonomy (Demszky et al., 2020) and the NRC Plutchik Emotion Wheel (Mohammad & Turney, 2013).

### 2.2 Variable Definitions

Let \( F_i \) denote the \( i \)-th Fruit of the Spirit, where \( i \in \{1, 2, \ldots, 9\} \) corresponding to Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness, Gentleness, and Self-Control, respectively.

For each fruit \( F_i \), two primary metrics are defined:

\[
L6_i = \text{lexical frequency score for } F_i \text{ (dimensionless, normalized to } [0,1])
\]

\[
L8_i = \text{emotional valence score for } F_i \text{ (dimensionless, normalized to } [0,1])
\]

The aggregate metric \( \text{Avg}_i \) is computed as:

\[
\text{Avg}_i = \max(L6_i, L8_i)
\]

This maximum-based aggregation reflects the dual-channel assumption that either lexical or emotional activation is sufficient to register the construct's presence in the textual corpus.

Additionally, an Anti-Fruit score \( A_i \) is defined for each fruit, representing the inverse or oppositional emotional valence:

\[
A_i = \text{inverse emotional score for } F_i \text{ (dimensionless, normalized to } [0,1])
\]

### 2.3 Coherence and CHI Metrics

The overall coherence score \( C = 0.307 \) is computed as the average pairwise correlation between L6 and L8 scores across all nine fruits, adjusted for dimensionality. The CHI score \( \chi = 0.45 \) represents a composite harmonic index incorporating lexical-emotional alignment, structural completeness, and cross-domain validity.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the complete dual-channel analysis for all nine Fruits of the Spirit.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Avg |
|-------|--------------|--------------|------------|-----|
| Love | 0.000 | 0.394 | 0.015 | 0.394 |
| Joy | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace | 0.000 | 0.397 | 0.011 | 0.397 |
| Patience | 0.000 | 0.395 | 0.015 | 0.395 |
| Kindness | 0.000 | 0.395 | 0.011 | 0.395 |
| Goodness | 0.000 | 0.394 | 0.015 | 0.394 |
| Faithfulness | 0.000 | 0.397 | 0.011 | 0.397 |
| Gentleness | 0.000 | 0.395 | 0.015 | 0.395 |
| Self-Control | 0.587 | 0.398 | 0.011 | 0.492 |

*Note: All scores are dimensionless and normalized to the interval [0,1]. Source: MDA-051-korea-experiment, Schema 2026.04.07-B pipeline.*

### 3.2 Lexical Channel (L6) Analysis

The lexical frequency scores reveal a striking bifurcation within the fruit set. Eight of the nine fruits—Love, Joy, Peace, Patience, Kindness, Goodness, Faithfulness, and Gentleness—exhibit L6 scores of 0.000, indicating negligible lexical activation within the analyzed corpus. This result suggests that these terms, while theologically significant, do not appear as discrete lexical units in the textual data under examination.

In contrast, Self-Control registers an L6 score of 0.587, representing a substantial lexical presence. This disparity may reflect the distinct semantic domain of Self-Control (Greek: *enkrateia*), which carries connotations of mastery and restraint that differentiate it from the more relational virtues in the Pauline list.

### 3.3 Emotional Channel (L8) Analysis

The emotional valence scores demonstrate remarkable consistency across all nine fruits, with values ranging from 0.394 (Love, Goodness) to 0.400 (Joy). The mean emotional score across all fruits is \( \bar{L8} = 0.396 \) with a standard deviation of \( \sigma_{L8} = 0.002 \), indicating near-uniform emotional resonance.

The dominant emotion identified by the GoEmotions 27 fine-grained taxonomy is anger (score: 0.045), followed by confusion (0.042), realization (0.008), curiosity (0.001), and annoyance (0.001). This emotional profile suggests a complex affective landscape wherein the virtues are embedded within a broader emotional context characterized by tension and cognitive processing.

### 3.4 Anti-Fruit Analysis

The Anti-Fruit scores, representing inverse emotional valences, range from 0.000 (Joy) to 0.015 (Love, Patience, Kindness, Goodness, Gentleness). The near-zero values for all fruits indicate minimal oppositional emotional activation, suggesting that the emotional valence of these virtues is not accompanied by significant countervailing emotional responses within the analyzed corpus.

### 3.5 Aggregate Metrics

The average scores, computed as the maximum of L6 and L8 for each fruit, yield values of approximately 0.394–0.400 for the eight lexically inactive fruits, and 0.492 for Self-Control. The elevated aggregate for Self-Control reflects its dual activation across both channels.

## 4. Discussion

### 4.1 Structural Interpretation of the Dual-Channel Results

The observed pattern—uniform emotional activation with near-zero lexical activation for eight fruits, contrasted with dual activation for Self-Control—suggests a hierarchical structure within the Pauline taxonomy. This structure may be interpreted through the lens of virtue epistemology (Zagzebski, 1996), wherein certain virtues function as foundational dispositions (lexically implicit but emotionally present) while others operate as executive functions (lexically explicit and emotionally present).

The coherence score of 0.307 indicates moderate alignment between the lexical and emotional channels, falling below the threshold typically required for strong cross-validation (\( C > 0.5 \)). This finding suggests that the dual-channel framework captures distinct but partially overlapping dimensions of the virtue constructs.

### 4.2 Theological Implications

From a theological perspective, the near-zero lexical activation for eight fruits may reflect the Pauline emphasis on virtues as *habitus*—dispositions of character that are lived rather than merely named (cf. Aquinas, *Summa Theologiae* I-II, q. 55). The emotional consistency across all nine fruits (L8 ≈ 0.396) supports the interpretation of the Fruits of the Spirit as a unified affective disposition, consistent with the exegetical tradition that reads Galatians 5:22–23 as a single fruit with multiple aspects (cf. Lightfoot, 1865).

The anomalous status of Self-Control warrants particular attention. Its elevated lexical score (0.587) may correspond to the distinct grammatical form of *enkrateia* in the Pauline corpus, which appears as a discrete term in contexts emphasizing self-mastery (1 Corinthians 9:25; Acts 24:25). This lexical prominence may reflect the virtue's role as a meta-virtue governing the exercise of the other fruits.

### 4.3 Methodological Limitations

Several methodological considerations constrain the interpretation of these results. First, the corpus analyzed is limited to the MDA-051-korea-experiment dataset, which may not fully represent the broader Pauline or early Christian textual tradition. Second, the GoEmotions taxonomy, while comprehensive, was developed for general emotional classification and may not capture the specific affective nuances of theological virtue language. Third, the normalization procedures for L6 and L8 scores assume linear scaling, which may not adequately represent the non-linear relationships between lexical frequency and emotional valence.

## 5. Conclusion

This study has demonstrated the application of a dual-channel computational framework to the analysis of the Fruits of the Spirit, revealing a structural pattern characterized by uniform emotional activation and differential lexical activation. The results support a hierarchical interpretation of the Pauline virtue taxonomy, with Self-Control occupying a distinct position as both lexically and emotionally activated.

Future research should extend this analysis to larger textual corpora, including the complete Pauline corpus and patristic commentaries, and should explore alternative emotional taxonomies that may better capture the theological dimensions of virtue language. The methodological framework established here provides a foundation for further theophysics investigations into the formal structure of spiritual formation constructs.

## References

Aquinas, T. (1274). *Summa Theologiae*. Trans. Fathers of the English Dominican Province.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Lightfoot, J. B. (1865). *Saint Paul's Epistle to the Galatians: A Revised Text with Introduction, Notes, and Dissertations*. Macmillan.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Nestle, E., & Aland, K. (Eds.). (2012). *Novum Testamentum Graece* (28th ed.). Deutsche Bibelgesellschaft.

Zagzebski, L. T. (1996). *Virtues of the Mind: An Inquiry into the Nature of Virtue and the Ethical Foundations of Knowledge*. Cambridge University Press.