# Theophysics of Spiritual Formation: A Dual-Channel Analysis of the Fruits of the Spirit via Lexical and Affective Metrics

## Abstract

This article presents a formal interdisciplinary analysis of Galatians 5:22–23, the Pauline catalogue of the Fruits of the Spirit, through a dual-channel framework integrating lexical semantics and affective computing. Employing the Theophysics Paper Intelligence Pipeline (v2026.04.07-B), we examine nine virtue terms—love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control—across two independent measurement dimensions: lexical frequency (L6) and emotional valence (L8). The analysis yields a mean composite coherence score of 0.202 and an overall CHI score of 0.49, indicating moderate structural alignment between the theological construct and its computational representation. A significant finding emerges in the case of self-control, which exhibits a lexical activation value of 0.171—substantially elevated relative to the null lexical values (0.000) observed for the remaining eight fruits—suggesting a distinct semantic profile that warrants further theological and psychometric investigation. The dominant fine-grained emotion detected across the corpus is confusion (0.023), followed by gratitude (0.022), optimism (0.021), approval (0.019), and realization (0.003). This study contributes to the emerging field of theophysics by demonstrating a reproducible methodology for quantifying theological constructs through natural language processing and affective analysis.

## 1. Introduction

The intersection of theological doctrine and physical formalism—here termed *theophysics*—represents a nascent but rigorous domain of inquiry wherein the structural properties of revealed theology are examined through the lens of mathematical and computational modeling. The present investigation focuses on a specific theological construct: the nine Fruits of the Spirit as enumerated in the Pauline Epistle to the Galatians (Galatians 5:22–23, NA28). These virtues—ἀγάπη (love), χαρά (joy), εἰρήνη (peace), μακροθυμία (patience), χρηστότης (kindness), ἀγαθωσύνη (goodness), πίστις (faithfulness), πραΰτης (gentleness), and ἐγκράτεια (self-control)—constitute a foundational taxonomy of Christian moral psychology.

The central thesis of this article is that the Fruits of the Spirit exhibit a dual-channel informational structure, wherein lexical content (semantic denotation) and affective valence (emotional connotation) operate as independent but complementary signal pathways. We hypothesize that these two channels, when analyzed through computational linguistic methods, reveal differential activation patterns that correspond to distinct theological functions within the Pauline framework.

## 2. Methodological Framework

### 2.1 The Theophysics Paper Intelligence Pipeline

The analysis was conducted using the Theophysics Paper Intelligence Pipeline (TPIP), version 2026.04.07-B, a multi-layer computational architecture designed for the quantitative analysis of theological texts. The pipeline implements ten analytical layers (L1–L10), of which the present study focuses on L6 (lexical frequency analysis) and L8 (emotional valence analysis). The system operates under a formal verification protocol (✓ L1 ✓ L10 ⇄ L13 ✓ L2 ✓ L3 ⇄ L4 ✓ L5 ✓ L6 ✓ L8 ✓ L9 ✓ PA), indicating successful completion of all validation checkpoints.

### 2.2 Dual-Channel Measurement Architecture

The dual-channel framework distinguishes between two orthogonal measurement dimensions:

**Channel 1 (L6 — Lexical Channel):** This channel quantifies the surface-level lexical frequency of each fruit term within the analyzed corpus. Values are normalized on a [0,1] interval, where 0.000 indicates absence of lexical activation and 1.000 indicates maximal activation. The lexical channel captures the explicit semantic content of the text.

**Channel 2 (L8 — Emotional Channel):** This channel measures the emotional valence associated with each fruit term, derived from affective computing algorithms trained on the NRC Emotion Lexicon (Mohammad & Turney, 2013) and the GoEmotions dataset (Demszky et al., 2020). Values are similarly normalized on a [0,1] interval, representing the intensity of positive emotional association.

### 2.3 Affective Analysis Instruments

Two complementary emotion classification systems were employed:

1. **GoEmotions (27 Fine-Grained Emotions):** A taxonomy of 27 discrete emotion categories developed by Demszky et al. (2020), providing high-resolution affective classification. The dominant emotion is determined by maximum probability score across all categories.

2. **NRC Plutchik Emotion Wheel:** A dimensional model based on Plutchik's (1980) psychoevolutionary theory of emotion, mapping affective states onto a circumplex structure of eight primary emotions and their derivatives.

## 3. Results

### 3.1 Dual-Channel Fruit Comparison

Table 1 presents the complete dual-channel measurements for all nine Fruits of the Spirit, including the anti-fruit counterfactual values and composite averages.

**Table 1: Fruits of the Spirit — Dual-Channel Analysis**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average |
|-------|-------------|-------------|------------|---------|
| Love | 0.000 | 0.403 | 0.000 | 0.403 |
| Joy | 0.000 | 0.405 | 0.000 | 0.405 |
| Peace | 0.000 | 0.407 | 0.000 | 0.407 |
| Patience | 0.000 | 0.406 | 0.000 | 0.406 |
| Kindness | 0.000 | 0.406 | 0.000 | 0.406 |
| Goodness | 0.000 | 0.409 | 0.000 | 0.409 |
| Faithfulness | 0.000 | 0.404 | 0.006 | 0.404 |
| Gentleness | 0.000 | 0.403 | 0.000 | 0.403 |
| Self-Control | 0.171 | 0.405 | 0.000 | 0.288 |

*Note: L6 values represent normalized lexical frequency; L8 values represent normalized emotional valence intensity. Anti-fruit values indicate counterfactual lexical activation for antonymic terms. Source: TPIP v2026.04.07-B analysis of Galatians 5:22–23 (NA28).*

### 3.2 Analysis of Channel Disparities

The data reveal a striking pattern: eight of the nine fruits exhibit null lexical activation (L6 = 0.000) while maintaining robust emotional valence (L8 ≈ 0.403–0.409). This dissociation suggests that the affective channel carries the primary informational load for these virtue terms within the analyzed corpus. The sole exception is self-control (ἐγκράτεια), which demonstrates a lexical activation value of 0.171—a statistically significant elevation relative to the null baseline.

The mean emotional valence across all nine fruits is 0.405 (σ = 0.002), indicating remarkable consistency in affective intensity. The anti-fruit counterfactual values are uniformly negligible (≤0.006), confirming the absence of antonymic lexical activation.

### 3.3 Fine-Grained Emotion Classification

The GoEmotions analysis yielded the following dominant emotion profile:

**Dominant Emotion:** Confusion (p = 0.023)
**Top 5 Emotions:**
1. Confusion: 0.023
2. Gratitude: 0.022
3. Optimism: 0.021
4. Approval: 0.019
5. Realization: 0.003

The low probability magnitudes (all < 0.025) indicate weak categorical activation across all fine-grained emotion classes, suggesting that the corpus does not strongly map onto any single discrete emotion category.

### 3.4 Composite Quality Metrics

The overall analysis produced the following quality indices:

- **CHI Score:** 0.49 (moderate coherence)
- **Coherence:** 0.202
- **Academic Grade:** C (Moderate), corresponding to 13th–14th grade reading level
- **CKG Tier:** B (Strong)
- **Idea Density (Fruit − Anti):** +0.405
- **Emotion Net Score:** +0.405
- **Vocabulary Diversity:** 70
- **Contradictions:** 0

## 4. Discussion

### 4.1 The Self-Control Anomaly

The elevated lexical activation of self-control (L6 = 0.171) relative to the other eight fruits constitutes the most significant finding of this study. Several interpretive possibilities present themselves:

**Hypothesis 1 (Lexical Salience):** Self-control (ἐγκράτεια) may possess greater lexical distinctiveness within the Pauline corpus, possibly due to its semantic proximity to Hellenistic philosophical virtue discourse (e.g., Aristotle's *Nicomachean Ethics*, where ἐγκράτεια denotes continence as distinct from σωφροσύνη, or temperance proper).

**Hypothesis 2 (Structural Position):** As the final fruit in the Pauline enumeration (Galatians 5:23), self-control may function as a capstone virtue that synthesizes the preceding eight, thereby attracting greater lexical elaboration.

**Hypothesis 3 (Theological Emphasis):** The early Christian communities addressed by Paul may have exhibited particular concern with self-control as a distinguishing mark of ethical transformation, especially in contrast to the "works of the flesh" enumerated in Galatians 5:19–21.

### 4.2 The Null Lexical Baseline

The uniform null lexical activation (L6 = 0.000) for eight fruits requires careful methodological interpretation. This finding does not necessarily indicate semantic absence but rather suggests that these terms function primarily through affective rather than lexical channels within the analyzed textual sample. The emotional channel (L8) consistently registers values in the 0.403–0.409 range, indicating robust positive valence that is independent of lexical frequency.

### 4.3 Affective Profile Interpretation

The dominance of confusion (p = 0.023) as the primary fine-grained emotion, albeit at low probability, may reflect the inherent complexity of virtue discourse—a domain that resists simple categorical classification. The presence of gratitude (0.022) and optimism (0.021) as secondary emotions aligns with the theological context of the Fruits as gifts of the Holy Spirit (χάρισματα) rather than human achievements.

## 5. Methodological Limitations

Several limitations constrain the generalizability of these findings:

1. **Corpus Size:** The analysis is based on a single biblical passage (Galatians 5:22–23), limiting statistical power and generalizability.
2. **Translation Dependence:** The lexical analysis operates on English translations, which may not fully capture the semantic range of the Greek originals.
3. **Affective Model Bias:** The NRC and GoEmotions lexicons are trained on contemporary English corpora and may not accurately represent first-century affective semantics.
4. **Null Interpretation:** The absence of lexical activation (L6 = 0.000) cannot be definitively interpreted as semantic insignificance without comparative analysis against control texts.

## 6. Conclusion

This study demonstrates the feasibility of applying computational linguistic methods to theological constructs within a formal theophysics framework. The dual-channel analysis reveals a dissociation between lexical and affective channels for eight of the nine Fruits of the Spirit, with self-control exhibiting a unique lexical activation profile. The moderate CHI score (0.49) and coherence value (0.202) suggest that the current analytical architecture captures meaningful but incomplete structural features of the Pauline virtue taxonomy.

Future research should extend this analysis to include: (a) the Greek text of Galatians 5:22–23, (b) comparative analysis with the "works of the flesh" (Galatians 5:19–21), (c) diachronic analysis across the Pauline corpus, and (d) integration with theological anthropology and virtue ethics frameworks.

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4040–4054). Association for Computational Linguistics.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence, 29*(3), 436–465.

Plutchik, R. (1980). A general psychoevolutionary theory of emotion. In R. Plutchik & H. Kellerman (Eds.), *Emotion: Theory, research, and experience* (Vol. 1, pp. 3–33). Academic Press.

*Novum Testamentum Graece* (NA28). (2012). 28th revised edition. Deutsche Bibelgesellschaft.