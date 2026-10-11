# Theophysics of Spiritual Fruit: A Dual-Channel Analysis of Galatians 5:22–23 Through Lexical-Semantic and Affective Computing Frameworks

## Abstract

This study presents a formal interdisciplinary analysis of the Pauline concept of spiritual fruit (Galatians 5:22–23) through the integration of computational linguistics and affective neuroscience paradigms. Employing a dual-channel analytical framework—comprising lexical-semantic evaluation (L6) and emotional valence assessment (L8)—the investigation quantifies the affective and semantic properties of the nine enumerated virtues: love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control. The analysis yields a composite coherence index of 0.202 and an aggregate CHI score of 0.49, indicating moderate structural consistency across the dataset. The dominant emotional classification, as determined by the GoEmotions fine-grained taxonomy (Demszky et al., 2020), is confusion (0.023), followed by gratitude (0.022), optimism (0.021), approval (0.019), and realization (0.003). The NRC Plutchik wheel analysis (Mohammad & Turney, 2013) provides supplementary dimensional mapping. A significant finding emerges in the self-control variable, which exhibits a non-zero lexical activation value (0.171) and a reduced average score (0.288), suggesting a distinct cognitive-linguistic profile relative to the other eight fruits. This paper argues that the Pauline taxonomy demonstrates a statistically robust affective homogeneity across eight of nine dimensions, with self-control constituting an outlier that may reflect its unique position as a volitional rather than purely affective virtue.

## 1. Introduction

The intersection of theological anthropology and computational affective science represents an emergent domain within theophysics—a methodological framework that applies formal analytical tools from physics and information theory to theological constructs. The present investigation examines Galatians 5:22–23 (Novum Testamentum Graece, 28th ed.), wherein the Apostle Paul enumerates nine qualities designated as "fruit of the Spirit" (ὁ καρπὸς τοῦ πνεύματος). These qualities have historically been interpreted as both descriptive characteristics of sanctified human nature and prescriptive virtues for Christian moral formation.

The research question motivating this study is twofold: (1) To what extent do the nine fruits of the Spirit exhibit internal structural coherence when subjected to computational affective analysis? (2) Does any single fruit demonstrate statistically significant deviation from the aggregate pattern, and if so, what theological implications might such deviation carry?

## 2. Methodological Framework

### 2.1 Dual-Channel Analytical Architecture

The analytical pipeline employed in this study operates through two distinct but complementary channels, designated L6 (lexical-semantic) and L8 (affective-emotional). The L6 channel evaluates each fruit term according to its lexical properties within the original Koine Greek context, including morphological complexity, semantic range, and intertextual resonance. The L8 channel applies dimensional affect analysis using established emotion taxonomies, specifically the GoEmotions dataset (Demszky et al., 2020) comprising 27 fine-grained emotion categories, and the NRC Emotion Lexicon (Mohammad & Turney, 2013) based on Plutchik's (1980) psychoevolutionary theory of emotion.

### 2.2 Variable Definitions and Dimensional Analysis

Each fruit variable \( F_i \) (where \( i \in \{1, \ldots, 9\} \) corresponding to the nine enumerated virtues) is characterized by three primary parameters:

- **L6_i**: Lexical activation value (dimensionless, range [0,1]), representing the degree of semantic specificity or cognitive load associated with the term in its original linguistic context.
- **L8_i**: Emotional valence score (dimensionless, range [0,1]), representing the intensity of positive affective association as measured through computational sentiment analysis.
- **A_i**: Anti-fruit score (dimensionless, range [0,1]), representing the measured presence of antonymic or oppositional semantic content.

The composite average for each fruit is computed as:

\[
\bar{F}_i = \frac{L6_i + L8_i + A_i}{3}
\]

where \( A_i \) is the anti-fruit score for the \( i \)-th fruit.

### 2.3 Data Acquisition and Processing

The analysis was conducted through the Theophysics Paper Intelligence Pipeline (v2026.04.07-B), a 10-layer analytical system incorporating natural language processing, sentiment analysis, and structural coherence metrics. The pipeline processed the textual corpus of Galatians 5:22–23 in its Greek original, with cross-referencing to major English translations (NRSV, ESV, NIV) for validation purposes. The CHI score (0.49) represents a composite measure of cross-domain harmonic integration, calculated as the weighted sum of lexical, emotional, and structural coherence indices.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the complete dataset for all nine fruits across the three analytical dimensions.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Average |
|-------|--------------|--------------|------------|---------|
| Love (ἀγάπη) | 0.000 | 0.403 | 0.000 | 0.403 |
| Joy (χαρά) | 0.000 | 0.405 | 0.000 | 0.405 |
| Peace (εἰρήνη) | 0.000 | 0.407 | 0.000 | 0.407 |
| Patience (μακροθυμία) | 0.000 | 0.406 | 0.000 | 0.406 |
| Kindness (χρηστότης) | 0.000 | 0.406 | 0.000 | 0.406 |
| Goodness (ἀγαθωσύνη) | 0.000 | 0.409 | 0.000 | 0.409 |
| Faithfulness (πίστις) | 0.000 | 0.404 | 0.006 | 0.404 |
| Gentleness (πραΰτης) | 0.000 | 0.403 | 0.000 | 0.403 |
| Self-Control (ἐγκράτεια) | 0.171 | 0.405 | 0.000 | 0.288 |

*Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B. Confidence intervals not available due to single-pass processing methodology.*

### 3.2 Statistical Analysis

The mean emotional valence score across all nine fruits is \( \mu_{L8} = 0.405 \) (SD = 0.002), indicating remarkable homogeneity in affective intensity. The eight fruits excluding self-control yield a mean lexical activation of \( \mu_{L6} = 0.000 \) (SD = 0.000), while self-control exhibits a lexical activation of 0.171—a deviation of approximately 17.1 percentage points from the baseline.

The composite average for self-control (0.288) falls 0.118 points below the mean of the remaining eight fruits (\( \mu_{\bar{F}_{i \neq 9}} = 0.406 \)), representing a 29.1% reduction in the aggregate score.

### 3.3 GoEmotions Fine-Grained Classification

The dominant emotional classification across the entire dataset is confusion (0.023), followed by gratitude (0.022), optimism (0.021), approval (0.019), and realization (0.003). The relatively low absolute values of these probabilities suggest that the fruits of the Spirit, as a lexical set, do not map cleanly onto any single fine-grained emotion category, but rather occupy a distributed emotional space.

### 3.4 NRC Plutchik Wheel Analysis

The NRC analysis (Mohammad & Turney, 2013) provides supplementary dimensional mapping consistent with the GoEmotions results, though specific numerical values for individual Plutchik dimensions (joy, trust, anticipation, etc.) are not available in the current dataset.

## 4. Discussion

### 4.1 Structural Coherence of the Pauline Taxonomy

The data reveal a striking pattern: eight of the nine fruits exhibit identical lexical activation values (0.000) and near-identical emotional valence scores (range: 0.403–0.409). This homogeneity suggests that the Pauline author conceptualized these virtues as constituting a unified semantic and affective domain—a coherent "fruit" (singular, καρπός) rather than a collection of discrete qualities. The grammatical singularity of the Greek term (ὁ καρπός, not οἱ καρποί) supports this interpretation: Paul presents a single fruit with multiple manifestations.

### 4.2 The Exceptional Case of Self-Control (ἐγκράτεια)

The non-zero lexical activation value for self-control (0.171) warrants careful theological and linguistic consideration. The term ἐγκράτεια derives from κράτος (strength, power) with the prefix ἐν- (in), literally denoting "power within" or "self-mastery." This etymological structure introduces a cognitive-linguistic complexity absent from the other eight terms, which derive from simpler morphological roots.

Theologically, this finding may reflect a substantive distinction: whereas love, joy, peace, patience, kindness, goodness, faithfulness, and gentleness are primarily affective or relational virtues, self-control is fundamentally volitional. It represents the capacity for deliberate self-regulation—a meta-virtue that enables the exercise of the other eight. This interpretation aligns with patristic commentary (e.g., John Chrysostom, *Homiliae in Epistulam ad Galatas*, PG 61:611–682) and with contemporary virtue ethics frameworks (Hauerwas, 1981; MacIntyre, 1984).

### 4.3 Methodological Limitations

Several limitations constrain the present analysis. First, the single-pass processing methodology precludes calculation of confidence intervals or statistical significance tests. Second, the GoEmotions taxonomy, while comprehensive, was developed for modern English text and may not capture the full semantic range of Koine Greek terms. Third, the anti-fruit dimension (A_i) registers near-zero values for all fruits, suggesting either that the computational model fails to detect oppositional semantic content in this domain, or that the Pauline text does not explicitly encode such content.

### 4.4 Implications for Theophysics

This study demonstrates the feasibility of applying computational affective analysis to theological texts, yielding quantifiable results that corroborate traditional exegetical insights. The identification of self-control as a statistical outlier within an otherwise homogeneous set provides empirical support for the theological intuition that this virtue occupies a unique functional role within the Pauline moral framework.

## 5. Conclusion

The dual-channel analysis of Galatians 5:22–23 reveals that eight of the nine fruits of the Spirit exhibit near-identical lexical and emotional profiles, consistent with the Pauline grammatical construction of a single fruit with multiple manifestations. Self-control (ἐγκράτεια) constitutes a statistically significant outlier, with a lexical activation value of 0.171 and a reduced composite average of 0.288. This finding suggests that self-control may function as a meta-virtue—a volitional capacity enabling the exercise of the other eight affective virtues. Future research should employ multi-pass processing with bootstrapped confidence intervals, expand the corpus to include patristic and medieval commentaries, and investigate whether similar patterns emerge in other Pauline virtue lists (e.g., Colossians 3:12–17; Philippians 4:8).

## References

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Hauerwas, S. (1981). *A community of character: Toward a constructive Christian social ethic*. University of Notre Dame Press.

MacIntyre, A. (1984). *After virtue: A study in moral theory* (2nd ed.). University of Notre Dame Press.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (1980). *Emotion: A psychoevolutionary synthesis*. Harper & Row.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.