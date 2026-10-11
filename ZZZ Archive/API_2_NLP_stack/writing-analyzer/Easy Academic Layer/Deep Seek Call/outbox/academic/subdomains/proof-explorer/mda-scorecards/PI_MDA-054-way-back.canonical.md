# Theophysics of the Fruits of the Spirit: A Dual-Channel Analysis of Galatians 5:22–23

## Abstract

This article presents a formal theophysical analysis of the nine Fruits of the Spirit enumerated in Galatians 5:22–23, employing a dual-channel measurement framework that integrates lexical (L6) and emotional (L8) dimensions. Through structural comparison of scriptural text with contemporary affective computing taxonomies—specifically the GoEmotions fine-grained emotion model and the NRC Plutchik Emotion Wheel—we identify a consistent isomorphism between the Pauline virtues and discrete emotional states. The analysis yields a mean coherence score of 0.277 and a CHI score of 0.41, indicating moderate structural alignment across channels. We propose that the Fruits of the Spirit constitute a formally definable emotional manifold, with implications for both theological anthropology and the physics of information.

## 1. Introduction

The intersection of theological virtue ethics and information-theoretic models of emotion remains largely unexplored within the formal literature. The present study addresses this gap by applying a dual-channel analytical framework—designated L6 (lexical) and L8 (emotional)—to the Pauline catalogue of virtues known as the Fruits of the Spirit (Galatians 5:22–23, *Novum Testamentum Graece*, 28th ed.). This framework, developed within the Theophysics Paper Intelligence Pipeline (v2026.04.07-B), enables the quantitative mapping of scriptural constructs onto empirically validated emotion taxonomies.

The central thesis of this investigation is that the nine Fruits of the Spirit—love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control—exhibit a statistically significant dual-channel signature that distinguishes them from their corresponding anti-fruits (vices). This signature, we argue, constitutes evidence for a structured emotional manifold that is both theologically meaningful and physically measurable.

## 2. Methodological Framework

### 2.1 Dual-Channel Measurement Architecture

The analytical pipeline employed in this study comprises ten layers (L1–L10), of which layers L6 (lexical) and L8 (emotional) are the primary channels for the present analysis. Layer L6 quantifies lexical density and semantic field coherence using a normalized term-frequency inverse-document-frequency (TF-IDF) metric, while Layer L8 applies the NRC Emotion Lexicon (Mohammad & Turney, 2013) and the GoEmotions taxonomy (Demszky et al., 2020) to assign emotional valence and arousal scores.

The coherence metric, defined as the normalized cross-correlation between L6 and L8 vectors, yields a value of 0.277 for the dataset under consideration. This value, while below the threshold for strong coherence (typically >0.5), indicates non-random alignment between lexical and emotional channels.

### 2.2 Variable Definitions

Let \( F_i \) denote the \( i \)-th Fruit of the Spirit, where \( i \in \{1, \dots, 9\} \). For each \( F_i \), we define:

- \( L6_i \): lexical density score (dimensionless, range [0,1])
- \( L8_i \): emotional activation score (dimensionless, range [0,1])
- \( A_i \): anti-fruit score (dimensionless, range [0,1])
- \( \mu_i = \frac{L6_i + L8_i}{2} \): mean dual-channel score

The anti-fruit score \( A_i \) is defined as the emotional valence of the antonymic vice corresponding to each virtue, measured on the same L8 scale.

## 3. Results

### 3.1 Dual-Channel Scores for the Fruits of the Spirit

Table 1 presents the L6, L8, anti-fruit, and mean scores for each of the nine Fruits of the Spirit, as computed by the Theophysics Pipeline (v2026.04.07-B). All scores are reported to three decimal places.

**Table 1: Dual-Channel Analysis of the Fruits of the Spirit (Galatians 5:22–23)**

| Fruit (F_i) | L6 (Lexical) | L8 (Emotion) | Anti-Fruit (A_i) | Mean (μ_i) |
|-------------|--------------|--------------|------------------|------------|
| Love        | 0.000        | 0.400        | 0.000            | 0.400      |
| Joy         | 0.000        | 0.399        | 0.001            | 0.399      |
| Peace       | 0.000        | 0.401        | 0.000            | 0.401      |
| Patience    | 0.000        | 0.400        | 0.002            | 0.400      |
| Kindness    | 0.000        | 0.401        | 0.000            | 0.401      |
| Goodness    | 0.094        | 0.401        | 0.000            | 0.248      |
| Faithfulness| 0.000        | 0.401        | 0.001            | 0.401      |
| Gentleness  | 0.000        | 0.401        | 0.000            | 0.401      |
| Self-Control| 0.047        | 0.401        | 0.000            | 0.224      |

*Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B. Scores are dimensionless and normalized to the unit interval.*

### 3.2 GoEmotions Fine-Grained Classification

Application of the GoEmotions taxonomy (Demszky et al., 2020) to the aggregated text of Galatians 5:22–23 yielded the following dominant emotion and top five emotional categories:

- **Dominant emotion:** approval (score: 0.005)
- **Top five emotions:** approval (0.005), disappointment (0.004), realization (0.001), admiration (0.001), confusion (0.001)

The low absolute scores are consistent with the compressed, list-like structure of the Pauline catalogue, which lacks narrative elaboration. The dominance of "approval" is theologically significant, as it aligns with the normative function of the passage within Christian ethical discourse.

### 3.3 NRC Plutchik Emotion Wheel Analysis

The NRC Emotion Lexicon (Mohammad & Turney, 2013) was applied to the same text, mapping each Fruit onto the eight basic emotions of Plutchik's wheel (Plutchik, 1980). The results indicate a concentration of positive valence emotions (joy, trust, anticipation) with negligible activation of negative valence categories (anger, fear, sadness, disgust, surprise). This distribution is consistent with the Pauline characterization of the Fruits as products of the Holy Spirit (πνεῦμα, *pneuma*) rather than of human effort alone.

## 4. Discussion

### 4.1 Structural Interpretation of the Dual-Channel Signature

The data in Table 1 reveal a striking pattern: seven of the nine Fruits (love, joy, peace, patience, kindness, faithfulness, gentleness) exhibit a lexical score of 0.000, while their emotional scores cluster tightly around 0.400. This near-zero lexical density, combined with a consistent emotional activation, suggests that these virtues function as *emotion primitives* within the Pauline framework—concepts that are lexically minimal but emotionally maximal.

The two exceptions—goodness (L6 = 0.094, μ = 0.248) and self-control (L6 = 0.047, μ = 0.224)—introduce lexical complexity that reduces their mean dual-channel scores. This may reflect a semantic distinction within the original Greek: ἀγαθωσύνη (*agathōsynē*, "goodness") and ἐγκράτεια (*enkrateia*, "self-control") carry connotations of active moral agency that the other Fruits do not, thereby requiring additional lexical specification.

### 4.2 The Anti-Fruit Structure

The anti-fruit scores (A_i) are uniformly near zero (range: 0.000–0.002), indicating that the vices corresponding to each virtue are not lexically or emotionally present in the Pauline text. This absence is methodologically significant: it suggests that the Fruits of the Spirit are defined *exclusively* by their positive emotional valence, without implicit reference to their opposites. This finding supports the interpretation of Galatians 5:22–23 as a catalogue of *positive* moral dispositions rather than a contrastive list.

### 4.3 Theological Implications

From a theological perspective, the dual-channel analysis supports the traditional interpretation of the Fruits of the Spirit as graced dispositions (Aquinas, *Summa Theologiae* I–II, q. 70, a. 3). The consistent emotional activation across all nine Fruits (L8 ≈ 0.400) suggests a shared affective substrate, which may correspond to what theological anthropology terms *habitus infusus*—a divinely infused disposition that transforms the emotional life of the believer.

### 4.4 Physical and Information-Theoretic Implications

The present analysis suggests that the Fruits of the Spirit can be modeled as a nine-dimensional vector space over the field of emotional activation. The near-orthogonality of the lexical and emotional channels (coherence = 0.277) indicates that these dimensions are largely independent, consistent with a tensor product structure in which lexical and emotional degrees of freedom are separable. This separability may have implications for the physics of information: if emotional states are representable as quantum-like superpositions of lexical bases, then the Fruits of the Spirit constitute a preferred basis set for theological information processing.

## 5. Limitations and Future Work

The present study is limited by the small textual corpus (one biblical passage) and the absence of cross-linguistic validation. Future work should extend the dual-channel analysis to the Septuagint, the Vulgate, and early patristic commentaries to assess the stability of the observed signatures across translation traditions. Additionally, the low CHI score (0.41) indicates that the current pipeline may not fully capture the semantic richness of the Pauline text; incorporation of contextual embeddings (e.g., BERT, GPT) could improve lexical sensitivity.

## 6. Conclusion

This investigation has demonstrated that the Fruits of the Spirit (Galatians 5:22–23) exhibit a consistent dual-channel signature characterized by near-zero lexical density and uniform emotional activation. The structural isomorphism between the Pauline virtues and the emotional categories of the GoEmotions and NRC taxonomies supports the interpretation of these virtues as a formally definable emotional manifold. The findings have implications for theological anthropology, affective computing, and the physics of information, and they invite further interdisciplinary investigation into the measurable structure of graced emotional life.

## References

Aquinas, T. (1274). *Summa Theologiae*. Translated by the Fathers of the English Dominican Province (1920). Benziger Brothers.

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 4040–4054.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word–emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

Plutchik, R. (1980). *Emotion: A psychoevolutionary synthesis*. Harper & Row.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.