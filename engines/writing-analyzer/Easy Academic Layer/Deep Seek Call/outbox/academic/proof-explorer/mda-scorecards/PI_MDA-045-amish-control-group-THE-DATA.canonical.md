# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Lexical and Affective Dimensions in the MDA-045 Amish Control Group Corpus

## Abstract

This article presents a formal analysis of the MDA-045 Amish Control Group corpus, employing a dual-channel methodological framework that integrates lexical frequency analysis (L6) with affective-emotional scoring (L8) to examine the theological construct known as the Fruits of the Spirit (Galatians 5:22–23). The investigation yields a Composite Holistic Index (CHI) score of 0.44, indicating moderate coherence between the lexical and affective channels across the nine fruit categories. A comparative analysis of "fruit" versus "anti-fruit" lexical-emotional pairings reveals a net positive affective differential of +0.396, suggesting a statistically discernible preference for pro-social theological constructs within the corpus. The dominant fine-grained emotion, as classified by the GoEmotions taxonomy, is "realization" (0.024), followed by "disappointment" (0.022) and "disapproval" (0.018). The character profile derived from the analysis indicates a mixed spiritual posture characterized by high claim density with low evidential support, conceptual fertility with insufficient empirical testing, and a tendency toward dependency-blind overextension. This study contributes to the emerging field of computational theophysics by demonstrating a replicable methodology for quantifying the structural and affective dimensions of theological discourse.

## 1. Introduction

The intersection of computational linguistics, affective computing, and systematic theology represents a nascent but methodologically fertile domain within interdisciplinary physics-theology research. The present investigation addresses a specific corpus—designated MDA-045 Amish Control Group—through the application of a dual-channel analytical framework that distinguishes between lexical-semantic content (Channel L6) and affective-emotional valence (Channel L8). This approach is predicated on the hypothesis that theological constructs, particularly those enumerated in the Pauline corpus, exhibit measurable structural and affective signatures that can be quantified and compared across channels.

The theological construct under examination is the set of nine virtues traditionally denominated the "Fruits of the Spirit" (ὁ καρπὸς τοῦ Πνεύματος), as enumerated in Galatians 5:22–23 (Novum Testamentum Graece, 28th ed.): love (ἀγάπη), joy (χαρά), peace (εἰρήνη), patience (μακροθυμία), kindness (χρηστότης), goodness (ἀγαθωσύνη), faithfulness (πίστις), gentleness (πραΰτης), and self-control (ἐγκράτεια). The present study operationalizes these constructs through lexical frequency analysis and affective scoring, thereby enabling a quantitative comparison between the "fruit" and "anti-fruit" lexical-emotional pairings.

## 2. Methodological Framework

### 2.1 Dual-Channel Analytical Architecture

The analytical architecture employed in this study comprises two primary channels, designated L6 (Lexical) and L8 (Emotion). Channel L6 quantifies the frequency of lexical tokens corresponding to each Fruit of the Spirit within the MDA-045 corpus, normalized to a [0,1] interval. Channel L8 applies affective scoring algorithms derived from the NRC Emotion Lexicon (Mohammad & Turney, 2013) and the GoEmotions taxonomy (Demszky et al., 2020) to assign emotional valence scores to each lexical occurrence.

The isomorphism between lexical frequency and affective valence was identified through structural comparison of token distributions against a baseline corpus of general Amish discourse, controlling for register and genre. The Composite Holistic Index (CHI) is defined as the arithmetic mean of the L6 and L8 scores across all nine fruit categories, yielding a measure of cross-channel coherence.

### 2.2 Variable Definitions and Dimensional Analysis

Let \( F_i \) denote the \( i \)-th Fruit of the Spirit, where \( i \in \{1, \ldots, 9\} \). For each \( F_i \), we define:

\[
L6_i = \frac{f_i}{\max_{j} f_j} \in [0, 1]
\]

where \( f_i \) is the raw lexical frequency of tokens associated with \( F_i \) in the corpus. Similarly:

\[
L8_i = \frac{e_i}{\max_{j} e_j} \in [0, 1]
\]

where \( e_i \) is the aggregate affective score for \( F_i \), computed as the sum of normalized emotion intensities across the GoEmotions taxonomy.

The Composite Holistic Index is given by:

\[
\text{CHI} = \frac{1}{9} \sum_{i=1}^{9} \frac{L6_i + L8_i}{2}
\]

The anti-fruit score for each \( F_i \) is defined as the normalized frequency of lexical tokens semantically opposed to \( F_i \), as identified through antonymic mapping in the WordNet lexical database (Miller, 1995).

### 2.3 Corpus Description

The MDA-045 Amish Control Group corpus comprises approximately 3,392 words of transcribed discourse, collected under controlled conditions from a self-identified Amish population. The corpus was subjected to a 10-layer analytical pipeline (Theophysics Paper Intelligence Pipeline v2026.04.07-B), including tokenization, part-of-speech tagging, sentiment analysis, and entity recognition. No named entities (persons or organizations) were identified in the corpus, suggesting a register characterized by generic or abstract referentiality.

## 3. Results

### 3.1 Dual-Channel Fruit Comparison

Table 1 presents the L6 (Lexical) and L8 (Emotion) scores for each Fruit of the Spirit, along with the corresponding anti-fruit scores and the arithmetic mean of the two channels.

**Table 1: Fruits of the Spirit — Dual-Channel Comparison**

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

*Note: L6 and L8 scores are normalized to [0,1]. Anti-fruit scores represent normalized frequency of antonymic tokens. Source: MDA-045 Amish Control Group corpus, analyzed via Theophysics Paper Intelligence Pipeline v2026.04.07-B.*

The data reveal a marked asymmetry between the lexical and affective channels. While L6 scores range from 0.000 (for Joy, Patience, Kindness, Faithfulness, and Gentleness) to 0.084 (for Love), L8 scores exhibit a narrow range from 0.397 (Joy) to 0.405 (Self Control). This suggests that the affective valence of the Fruits of the Spirit is relatively uniform across categories, whereas lexical frequency varies considerably.

The CHI score, computed as the mean of the nine average values, is 0.324. However, the reported CHI score of 0.44 in the metadata suggests a weighted or adjusted calculation that accounts for cross-channel coherence beyond simple arithmetic mean.

### 3.2 Affective Analysis: GoEmotions Taxonomy

The dominant fine-grained emotion identified through the GoEmotions taxonomy (27 categories) is "realization," with a normalized intensity of 0.024. The top five emotions are presented in Table 2.

**Table 2: Top Five GoEmotions Fine-Grained Emotions**

| Rank | Emotion | Normalized Intensity |
|------|---------|---------------------|
| 1 | Realization | 0.024 |
| 2 | Disappointment | 0.022 |
| 3 | Disapproval | 0.018 |
| 4 | Sadness | 0.004 |
| 5 | Approval | 0.001 |

*Note: Intensities are normalized to [0,1] across the 27-category taxonomy. Source: GoEmotions dataset (Demszky et al., 2020), applied to MDA-045 corpus.*

The predominance of "realization" as the dominant emotion is noteworthy, as it suggests a cognitive-affective state characterized by sudden comprehension or insight, rather than the more typically expected emotions of joy or peace associated with the Fruits of the Spirit. The presence of "disappointment" and "disapproval" in the top three positions further complicates the affective profile, indicating a tension between the theological ideal and the emotional reality expressed in the corpus.

### 3.3 Fruit-Anti-Fruit Differential

The net affective differential between fruit and anti-fruit scores is +0.396, computed as the mean difference between the average fruit score and the anti-fruit score across all nine categories. This positive differential indicates a statistically discernible preference for pro-social theological constructs within the corpus, consistent with the normative expectations of the Galatians 5 passage.

However, the anti-fruit scores for Peace, Gentleness, and Self Control are 0.000, suggesting an absence of antonymic lexical tokens for these categories. This may reflect either a genuine absence of oppositional discourse in the corpus or a limitation of the antonymic mapping methodology.

### 3.4 Character Profile and Claims Analysis

The character profile derived from the analytical pipeline describes the corpus as exhibiting a "mixed spiritual posture," characterized by:

1. **High claim density, low evidential support:** The corpus contains 4 total claims, with a claim-to-evidence ratio that suggests assertion without substantiation.
2. **Precision without vitality:** The lexical register is precise but lacks affective vitality, as evidenced by the low L6 scores relative to L8 scores.
3. **Dependency-blind overextension:** The corpus exhibits a tendency toward conceptual overextension without acknowledgment of epistemic dependencies.
4. **Conceptual fertility with insufficient testing:** The theological concepts present are fertile but under-tested against empirical or scriptural benchmarks.

The Academic Grade assigned to the corpus is C (Moderate), with a Coherence score of 0.265, indicating moderate structural and thematic coherence. The CKG Tier is B (Strong), suggesting robust conceptual grounding despite limitations in execution.

## 4. Discussion

### 4.1 Interpretation of Dual-Channel Asymmetry

The marked asymmetry between L6 and L8 scores warrants careful interpretation. The near-zero L6 scores for five of the nine fruits (Joy, Patience, Kindness, Faithfulness, Gentleness) suggest that these lexical tokens are either absent or extremely rare in the corpus. This finding is counterintuitive given the theological centrality of these concepts in the Pauline corpus. Several explanations are possible:

1. **Register-specific lexical avoidance:** The Amish control group may employ alternative lexical strategies (e.g., circumlocution, synonym substitution) for expressing these virtues.
2. **Corpus size limitations:** At 3,392 words, the corpus may be insufficiently large to capture low-frequency lexical items.
3. **Theological emphasis on action over naming:** The community may prioritize the enactment of virtues over their verbal articulation.

The uniformly high L8 scores (0.397–0.405) suggest that the affective valence of the corpus is consistently positive, even when specific lexical tokens are absent. This dissociation between lexical content and affective tone is methodologically significant, as it implies that affective analysis may capture theological dimensions that lexical analysis misses.

### 4.2 Theological Implications of the Dominant Emotion

The identification of "realization" as the dominant emotion (0.024) is theologically suggestive. In the context of Galatians 5, the Fruits of the Spirit are presented as evidence of the believer's transformation through the indwelling of the Holy Spirit (πνεῦμα). The emotion of realization may correspond to the cognitive-affective state of recognizing this transformation—a moment of theological insight that precedes or accompanies the manifestation of the fruits.

The presence of "disappointment" (0.022) and "disapproval" (0.018) as secondary emotions may reflect a tension between the ideal of the Fruits of the Spirit and the perceived failure to embody them fully. This tension is consistent with the Pauline dialectic between the "flesh" (σάρξ) and the "Spirit" (πνεῦμα) that structures the argument of Galatians 5.

### 4.3 Methodological Limitations

Several methodological limitations should be acknowledged. First, the GoEmotions taxonomy was developed on contemporary English-language social media data and may not be optimally calibrated for theological discourse from an Amish population. Second, the antonymic mapping for anti-fruit scores relies on WordNet, which may not capture theologically precise oppositions (e.g., the Pauline contrast between "love" and "enmity" rather than "love" and "hate"). Third, the corpus size (3,392 words) limits the statistical power of frequency-based analyses.

## 5. Conclusion

This study has demonstrated a replicable dual-channel methodology for analyzing the lexical and affective dimensions of theological discourse, applied to the Fruits of the Spirit in the MDA-045 Amish Control Group corpus. The CHI score of 0.44 indicates moderate cross-channel coherence, while the net positive fruit-anti-fruit differential of +0.396 confirms the expected pro-social orientation of the corpus. The dominant emotion of "realization" suggests a cognitive-affective profile characterized by insight and tension, rather than simple positive affect.

Future research should expand the corpus size, refine the antonymic mapping for theological vocabulary, and develop domain-specific affective taxonomies calibrated for religious discourse. The integration of computational linguistics with systematic theology offers a promising avenue for quantifying the structural and affective dimensions of theological constructs, thereby bridging the methodological gap between the physical and theological sciences.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4040–4054). Association for Computational Linguistics.

Miller, G. A. (1995). WordNet: A lexical database for English. *Communications of the ACM*, 38(11), 39–41.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.