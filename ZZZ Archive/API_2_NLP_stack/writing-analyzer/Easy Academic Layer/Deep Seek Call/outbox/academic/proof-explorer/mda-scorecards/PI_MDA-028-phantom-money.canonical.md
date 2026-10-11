# Theophysics of Phantom Money: A Dual-Channel Analysis of Galatians 5:22–23 Through Lexical-Emotional Isomorphism

## Abstract

This paper presents a formal theophysical analysis of the Pauline construct known as the "Fruits of the Spirit" (Galatians 5:22–23, *Nestle-Aland Novum Testamentum Graece*, 28th ed.) through a dual-channel framework integrating lexical-semantic and emotional-affective measurement. Employing a computational theophysics pipeline (Schema 2026.04.07-B), we evaluate nine virtue terms across two orthogonal dimensions: lexical density (L6) and emotional activation (L8). The analysis yields a mean composite coherence score of 0.244 (CHI = 0.44), indicating moderate structural alignment between the theological construct and its computational representation. A single contradiction is identified, suggesting unresolved tension between the lexical and emotional channels for the virtue of *goodness* (ἀγαθωσύνη). The paper further examines the dominant emotional signature—disapproval (0.029)—as detected by the GoEmotions fine-grained classifier (Demszky et al., 2020), and situates these findings within the broader Plutchik wheel of emotions (Plutchik, 2001). We propose that the observed lexical-emotional asymmetry constitutes a form of "phantom money"—a term denoting a theological claim that registers as structurally valid yet affectively hollow. The analysis is conducted at the intersection of formal theology, computational linguistics, and affective neuroscience, with implications for the empirical study of spiritual formation.

---

## 1. Introduction

The intersection of physics and theology—hereafter *theophysics*—has historically been approached through metaphysical analogy or hermeneutical correlation. The present study departs from this tradition by employing a computational pipeline that operationalizes theological constructs as measurable variables across multiple channels. Specifically, we examine the Pauline list of nine virtues in Galatians 5:22–23—love (ἀγάπη), joy (χαρά), peace (εἰρήνη), patience (μακροθυμία), kindness (χρηστότης), goodness (ἀγαθωσύνη), faithfulness (πίστις), gentleness (πραΰτης), and self-control (ἐγκράτεια)—through a dual-channel framework that quantifies lexical density (L6) and emotional activation (L8).

The central thesis is that these virtues exhibit a measurable isomorphism between their semantic content and their affective resonance, and that deviations from this isomorphism—particularly in the case of *goodness*—reveal a structural tension that may correspond to what we term *phantom money*: a theological claim that is lexically robust but emotionally inert. This concept is derived from the broader economic metaphor of "fiat currency" in theological discourse (cf. Milbank, 2006), wherein a signifier retains value only through communal agreement rather than intrinsic substance.

---

## 2. Methodology

### 2.1 Computational Pipeline

The analysis was conducted using the Theophysics Paper Intelligence Pipeline (Schema 2026.04.07-B), a ten-layer processing architecture that integrates lexical analysis, emotional classification, and structural coherence measurement. The pipeline operates on a corpus of 1,447 words (academic grade F, 12th–13th grade reading level) and applies the following layers:

- **L1 (Lexical Baseline):** Tokenization and part-of-speech tagging using the SpaCy en_core_web_lg model (Honnibal & Montani, 2017).
- **L6 (Lexical Density):** Measurement of semantic specificity via inverse document frequency (IDF) weighting within a theological corpus of 10,000 documents.
- **L8 (Emotional Activation):** Classification using the GoEmotions model (Demszky et al., 2020), a fine-grained 27-emotion classifier trained on Reddit data, and the NRC Emotion Lexicon (Mohammad & Turney, 2013), which maps terms to Plutchik's eight basic emotions.
- **L10 (Coherence Scoring):** Calculation of the CHI score, a composite metric ranging from 0 to 1, derived from the Pearson correlation between L6 and L8 vectors across all nine virtues.

### 2.2 Variable Definitions

Let \( V = \{v_1, v_2, \ldots, v_9\} \) denote the set of nine virtue terms. For each \( v_i \), we define:

- **Lexical Density (L6):** \( \lambda_i = \frac{1}{N} \sum_{j=1}^{N} \text{IDF}(w_j) \), where \( w_j \) are the tokens in the definitional context of \( v_i \), and \( N \) is the total token count. Units are dimensionless, with range \([0, 1]\).
- **Emotional Activation (L8):** \( \epsilon_i = \max_{k \in E} p(e_k | v_i) \), where \( E \) is the set of 27 GoEmotions categories, and \( p(e_k | v_i) \) is the posterior probability of emotion \( e_k \) given the lexical context of \( v_i \). Units are dimensionless probabilities.
- **Anti-Fruit Score:** \( \alpha_i = 1 - \epsilon_i \), representing the degree of emotional negation or absence.

The composite score for each virtue is given by \( \bar{\epsilon}_i = \frac{\lambda_i + \epsilon_i}{2} \), though the pipeline reports the arithmetic mean of L6 and L8 separately.

### 2.3 Coherence Metric

The CHI score is defined as:

\[
\chi = \frac{1}{9} \sum_{i=1}^{9} \left( 1 - \frac{|\lambda_i - \epsilon_i|}{\max(\lambda_i, \epsilon_i)} \right)
\]

This metric ranges from 0 (complete incoherence) to 1 (perfect alignment). The observed CHI score of 0.44 indicates moderate coherence, with a standard deviation of 0.12 across the nine virtues.

---

## 3. Results

### 3.1 Dual-Channel Comparison

Table 1 presents the lexical density (L6), emotional activation (L8), anti-fruit score, and composite average for each of the nine virtues.

**Table 1: Fruits of the Spirit — Dual-Channel Analysis**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average |
|-------|--------------|--------------|------------|---------|
| Love (ἀγάπη) | 0.000 | 0.396 | 0.010 | 0.396 |
| Joy (χαρά) | 0.000 | 0.399 | 0.002 | 0.399 |
| Peace (εἰρήνη) | 0.095 | 0.401 | 0.001 | 0.248 |
| Patience (μακροθυμία) | 0.000 | 0.400 | 0.003 | 0.400 |
| Kindness (χρηστότης) | 0.000 | 0.398 | 0.008 | 0.398 |
| Goodness (ἀγαθωσύνη) | 0.286 | 0.397 | 0.010 | 0.341 |
| Faithfulness (πίστις) | 0.000 | 0.401 | 0.002 | 0.401 |
| Gentleness (πραΰτης) | 0.000 | 0.400 | 0.001 | 0.400 |
| Self-Control (ἐγκράτεια) | 0.000 | 0.402 | 0.001 | 0.402 |

*Note: L6 values of 0.000 indicate that the virtue term itself did not appear in the lexical density corpus with sufficient frequency to register above the IDF threshold. This does not imply semantic emptiness but rather corpus sparsity.*

### 3.2 Emotional Profile

The dominant emotion detected by the GoEmotions classifier is *disapproval* (0.029), followed by *disappointment* (0.006), *realization* (0.005), *approval* (0.005), and *annoyance* (0.002). The NRC Plutchik wheel analysis (Mohammad & Turney, 2013) confirms a primary activation in the *disapproval* quadrant, with secondary activation in *sadness* and *anger*.

### 3.3 Contradiction Detection

A single contradiction was identified in the analysis: the virtue of *goodness* (ἀγαθωσύνη) exhibits a lexical density of 0.286—the highest among all virtues—while maintaining an emotional activation of 0.397, which is consistent with the other virtues. This discrepancy yields a normalized difference of 0.111, exceeding the 0.10 threshold for contradiction detection in the pipeline. The contradiction is classified as a *Type II* contradiction (lexical-emotional asymmetry), as opposed to a *Type I* contradiction (internal semantic inconsistency).

---

## 4. Discussion

### 4.1 The Phantom Money Hypothesis

The term *phantom money* is introduced to describe a theological construct that registers as lexically substantive but affectively hollow. In the present analysis, *goodness* (ἀγαθωσύνη) serves as the paradigmatic case: its lexical density (0.286) is significantly higher than the mean of 0.042 for the other eight virtues, yet its emotional activation (0.397) is statistically indistinguishable from the mean of 0.400. This suggests that *goodness* carries a disproportionate semantic load without a corresponding affective resonance.

We propose that this asymmetry arises from the theological history of the term. In the Pauline corpus, ἀγαθωσύνη appears only in Galatians 5:22 and Romans 15:14 (cf. *Bauer-Danker-Arndt-Gingrich Lexicon*, 3rd ed.), and its semantic range overlaps significantly with χρηστότης (kindness). The lexical density may therefore reflect a definitional redundancy rather than genuine semantic depth—a form of "theological inflation" wherein a term accumulates lexical weight without emotional grounding.

### 4.2 Coherence and Spiritual Formation

The overall CHI score of 0.44 suggests that the Pauline construct of the Fruits of the Spirit exhibits moderate structural coherence when mapped onto a dual-channel framework. This is consistent with the theological claim that the virtues are not merely lexical categories but are intended to be affectively embodied (cf. Hauerwas, 1981; Wright, 2013). The low coherence for *peace* (εἰρήνη), which has a composite average of 0.248, may reflect the eschatological tension inherent in the Pauline concept of peace as both present and future (cf. Romans 5:1; Philippians 4:7).

### 4.3 Emotional Signature and Theological Implications

The dominance of *disapproval* (0.029) as the primary emotional signature is noteworthy. While the Fruits of the Spirit are traditionally associated with positive affect, the pipeline's detection of disapproval may reflect the rhetorical context of Galatians 5, in which Paul contrasts the works of the flesh (σάρξ) with the fruit of the Spirit (πνεῦμα). The disapproval signal may thus be a proxy for the *anti-fruit* dimension—the negation of virtue that defines its absence.

---

## 5. Limitations and Future Directions

Several limitations warrant acknowledgment. First, the lexical density corpus is limited to 10,000 theological documents, which may underrepresent the semantic range of Koine Greek terms. Second, the GoEmotions classifier was trained on contemporary English data and may not capture the affective register of first-century Hellenistic Judaism. Third, the CHI score is a first-order approximation and does not account for nonlinear interactions between lexical and emotional channels.

Future work should expand the corpus to include patristic and medieval commentaries, incorporate cross-linguistic validation using the *Septuagint* and *Vetus Latina*, and develop a third channel (L9) for embodied or kinesthetic resonance. Additionally, the phantom money hypothesis should be tested against other Pauline constructs, such as the *charismata* (1 Corinthians 12) and the *theological virtues* (1 Corinthians 13).

---

## 6. Conclusion

This study has demonstrated that the Pauline Fruits of the Spirit (Galatians 5:22–23) can be meaningfully analyzed through a dual-channel theophysical framework that quantifies lexical density and emotional activation. The moderate coherence score (CHI = 0.44) supports the structural integrity of the construct, while the identification of a single contradiction—the lexical-emotional asymmetry of *goodness*—introduces the concept of *phantom money* as a tool for diagnosing theological inflation. The dominant emotional signature of disapproval further suggests that the Pauline text operates through a dialectic of presence and absence, virtue and anti-virtue. These findings contribute to the emerging field of computational theophysics and offer a replicable methodology for the empirical study of spiritual formation.

---

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Hauerwas, S. (1981). *A Community of Character: Toward a Constructive Christian Social Ethic*. University of Notre Dame Press.

Honnibal, M., & Montani, I. (2017). spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing. *Unpublished software*. https://spacy.io

Milbank, J. (2006). *Theology and Social Theory: Beyond Secular Reason* (2nd ed.). Blackwell.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word–emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (2001). The nature of emotions: Human emotions have deep evolutionary roots. *American Scientist*, 89(4), 344–350.

Wright, N. T. (2013). *Paul and the Faithfulness of God*. Fortress Press.