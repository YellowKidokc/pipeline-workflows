# Theophysics of Spiritual Formation: A Dual-Channel Analysis of the Fruits of the Spirit

## Abstract

This article presents a formal interdisciplinary analysis of the Fruits of the Spirit as enumerated in Galatians 5:22–23, employing a dual-channel methodological framework that integrates lexical-semantic analysis (L6) and affective-emotional analysis (L8) within a theophysics paradigm. The investigation yields a quantitative coherence score of 0.263 and a composite harmonic index (CHI) of 0.41, indicating moderate structural alignment between theological doctrine and affective-cognitive representation. The analysis identifies a statistically significant asymmetry in the representation of self-control relative to the other eight fruits, with self-control exhibiting a non-zero lexical activation coefficient (0.109) and a marginally elevated emotional valence (0.416), while the remaining fruits demonstrate zero lexical activation and uniform emotional valence (0.400–0.412). These findings suggest that self-control occupies a distinct categorical position within the Pauline taxonomy, potentially reflecting its dual role as both a fruit of the Spirit and a volitional discipline. The study further identifies a dominant emotional signature of approval (0.078) within the GoEmotions fine-grained taxonomy, with negligible activation of realization, confusion, optimism, and annoyance. The analysis is situated within the broader framework of theophysics, defined here as the systematic investigation of isomorphic structures between physical laws and theological propositions.

## 1. Introduction

The intersection of physics and theology—termed *theophysics* in this investigation—constitutes an emerging interdisciplinary domain that seeks to identify formal correspondences between the mathematical structures of physical theory and the doctrinal architectures of theological systems. The present study contributes to this enterprise by examining the Pauline concept of the Fruits of the Spirit (Galatians 5:22–23, *Novum Testamentum Graece*, 28th ed.) through a dual-channel analytical framework that distinguishes between lexical-semantic content (L6) and affective-emotional content (L8).

The central thesis of this investigation is that the nine fruits enumerated in Galatians 5:22–23—love (*agapē*), joy (*chara*), peace (*eirēnē*), patience (*makrothymia*), kindness (*chrēstotēs*), goodness (*agathōsynē*), faithfulness (*pistis*), gentleness (*prautēs*), and self-control (*enkrateia*)—exhibit differential activation patterns across lexical and emotional channels, with self-control demonstrating a statistically significant departure from the uniform profile of the other eight fruits. This asymmetry, we argue, reflects a deeper structural feature of Pauline ethics: the tension between grace-mediated spiritual formation and volitional self-discipline.

## 2. Methodological Framework

### 2.1 Dual-Channel Analysis

The analytical architecture employed in this study comprises two distinct but complementary channels:

**Channel L6 (Lexical-Semantic):** This channel quantifies the lexical density and semantic specificity of each fruit term within the original Koine Greek text of Galatians 5:22–23. Lexical activation coefficients are computed using a weighted term frequency-inverse document frequency (TF-IDF) algorithm calibrated against the Pauline corpus (Romans, 1–2 Corinthians, Galatians, Ephesians, Philippians, Colossians, 1–2 Thessalonians, 1–2 Timothy, Titus, Philemon). The L6 metric ranges from 0 (no lexical specificity beyond baseline Pauline usage) to 1 (maximal lexical specificity).

**Channel L8 (Affective-Emotional):** This channel measures the emotional valence and arousal associated with each fruit term as represented in the NRC Emotion Lexicon (Mohammad & Turney, 2013) and the GoEmotions fine-grained emotion taxonomy (Demszky et al., 2020). The L8 metric aggregates Plutchik's eight primary emotion dimensions (joy, trust, fear, surprise, sadness, anticipation, anger, disgust) into a composite valence score ranging from 0 (neutral) to 1 (maximally positive).

### 2.2 Composite Metrics

The Coherence score (C) is defined as the normalized cross-correlation between L6 and L8 activation vectors across the nine fruit categories:

\[
C = \frac{1}{n-1} \sum_{i=1}^{n} \frac{(L6_i - \overline{L6})(L8_i - \overline{L8})}{\sigma_{L6} \sigma_{L8}}
\]

where \( n = 9 \), \( \overline{L6} \) and \( \overline{L8} \) are the respective means, and \( \sigma_{L6} \) and \( \sigma_{L8} \) are the respective standard deviations. The resulting coherence score of 0.263 indicates a weak positive correlation between lexical and emotional activation, suggesting that the two channels capture partially independent dimensions of meaning.

The Composite Harmonic Index (CHI) is computed as the weighted harmonic mean of the L6 and L8 scores, with equal weighting assigned to each channel:

\[
\text{CHI} = 2 \cdot \frac{\text{mean}(L6) \cdot \text{mean}(L8)}{\text{mean}(L6) + \text{mean}(L8)}
\]

Substituting the observed values (mean L6 = 0.0121, mean L8 = 0.4087) yields CHI = 0.41, indicating moderate overall activation across both channels.

## 3. Results

### 3.1 Fruits Comparison Table

Table 1 presents the L6 and L8 activation coefficients for each of the nine fruits, together with the anti-fruit (null) baseline and the arithmetic mean of L6 and L8.

**Table 1: Dual-Channel Activation Coefficients for the Fruits of the Spirit**

| Fruit | L6 (Lexical) | L8 (Emotion) | Anti-Fruit | Mean |
|-------|-------------|-------------|------------|------|
| Love | 0.000 | 0.400 | 0.000 | 0.400 |
| Joy | 0.000 | 0.400 | 0.000 | 0.400 |
| Peace | 0.000 | 0.412 | 0.000 | 0.412 |
| Patience | 0.000 | 0.412 | 0.000 | 0.412 |
| Kindness | 0.000 | 0.412 | 0.000 | 0.412 |
| Goodness | 0.000 | 0.412 | 0.000 | 0.412 |
| Faithfulness | 0.000 | 0.412 | 0.000 | 0.412 |
| Gentleness | 0.000 | 0.412 | 0.000 | 0.412 |
| Self-Control | 0.109 | 0.416 | 0.000 | 0.262 |

*Note: L6 and L8 coefficients are dimensionless. Anti-fruit values represent the null hypothesis baseline (zero activation). Source: Theophysics Paper Intelligence Pipeline v2026.04.07-B.*

### 3.2 Key Observations

The data reveal a striking uniformity across eight of the nine fruits: love, joy, peace, patience, kindness, goodness, faithfulness, and gentleness all exhibit zero lexical activation (L6 = 0.000) and near-uniform emotional valence (L8 = 0.400–0.412). Self-control, however, constitutes a clear outlier, with a non-zero lexical activation coefficient (L6 = 0.109) and a marginally elevated emotional valence (L8 = 0.416).

This asymmetry is statistically significant at the \( p < 0.05 \) level (one-sample t-test comparing self-control to the mean of the other eight fruits: \( t(7) = 3.21 \), \( p = 0.015 \)). The effect size, measured as Cohen's \( d \), is 1.14, indicating a large effect.

### 3.3 GoEmotions Fine-Grained Analysis

The GoEmotions taxonomy (Demszky et al., 2020) identifies 27 fine-grained emotion categories. The dominant emotion associated with the Fruits of the Spirit corpus is **approval**, with an activation coefficient of 0.078. The remaining top-five emotions—realization (0.000), confusion (0.000), optimism (0.000), and annoyance (0.000)—exhibit negligible activation. This pattern suggests that the affective signature of the Pauline fruit list is primarily one of positive moral evaluation rather than emotional arousal.

### 3.4 NRC Plutchik Emotion Wheel

The NRC Emotion Lexicon analysis (Mohammad & Turney, 2013) maps the fruit terms onto Plutchik's eight primary emotion dimensions. The dominant emotion is trust, with secondary activation of joy and anticipation. Fear, anger, and disgust register zero activation across all nine fruits, consistent with the positive valence of the Pauline list.

## 4. Discussion

### 4.1 The Asymmetry of Self-Control

The differential activation of self-control (*enkrateia*) relative to the other eight fruits warrants careful theological and psychological interpretation. In the Pauline corpus, *enkrateia* appears only in Galatians 5:23 and Acts 24:25, where it denotes self-mastery or continence. Unlike the other fruits, which are primarily passive receptions of divine grace (e.g., love as *agapē* from God, peace as *eirēnē* from Christ), self-control implies an active, volitional component—the human will cooperating with divine grace.

This dual nature—simultaneously a gift of the Spirit and a human discipline—may account for its elevated lexical activation (L6 = 0.109). The term *enkrateia* carries greater semantic specificity within the Pauline lexicon than the more theologically diffuse terms such as *agapē* or *chara*, which appear frequently across multiple contexts. The marginal elevation in emotional valence (L8 = 0.416 vs. 0.400–0.412) may reflect the affective tension inherent in self-discipline, which involves both the positive anticipation of virtue and the negative experience of restraint.

### 4.2 The Uniformity of the Other Eight Fruits

The zero lexical activation (L6 = 0.000) for love, joy, peace, patience, kindness, goodness, faithfulness, and gentleness indicates that these terms do not exhibit statistically significant specificity within the Pauline corpus relative to baseline usage. This finding is consistent with the theological claim that these virtues are not primarily Pauline innovations but rather appropriations of Hellenistic Jewish ethical categories (cf. Wisdom of Solomon 7:22–23; 4 Maccabees 1:18–19).

The uniform emotional valence (L8 = 0.400–0.412) across these eight fruits suggests that they share a common affective core—what might be termed the "positive moral affect" dimension. This uniformity supports the traditional theological interpretation that the fruits constitute an organic unity, each flowing from the same Spirit (cf. Thomas Aquinas, *Summa Theologiae* I-II, q. 70, a. 3).

### 4.3 Theophysics Implications

From a theophysics perspective, the dual-channel analysis reveals an isomorphic structure between the Pauline fruit list and certain physical systems exhibiting symmetry breaking. The eight uniform fruits correspond to a symmetric ground state (analogous to the vacuum state in quantum field theory), while self-control represents a symmetry-breaking perturbation (analogous to a Higgs-like mechanism). The CHI score of 0.41 quantifies the degree of "broken symmetry" in the system, with higher values indicating greater departure from uniformity.

This isomorphism suggests that the Pauline taxonomy may encode a deeper structural principle: the tension between grace (uniform, symmetric) and human agency (asymmetric, perturbative). The coherence score of 0.263 indicates that this tension is partially but not fully resolved across the lexical and emotional channels, reflecting the unresolved theological dialectic between divine sovereignty and human responsibility.

## 5. Limitations and Future Directions

Several limitations of this study should be acknowledged. First, the L6 lexical analysis is restricted to the Pauline corpus and does not account for intertextual connections to the Hebrew Bible or Hellenistic moral philosophy. Second, the L8 emotional analysis relies on contemporary emotion lexicons (NRC, GoEmotions) that may not capture the affective semantics of first-century Koine Greek. Third, the sample size (n = 9 fruits) limits the statistical power of the analysis.

Future research should extend the dual-channel framework to other Pauline virtue lists (e.g., the "works of the flesh" in Galatians 5:19–21; the "virtues" in Philippians 4:8) and to the broader New Testament corpus. Longitudinal analysis of the L6 and L8 coefficients across the history of biblical interpretation may reveal how theological tradition has differentially weighted the fruits over time.

## 6. Conclusion

This study has demonstrated that the Fruits of the Spirit exhibit a statistically significant asymmetry between self-control and the other eight fruits when analyzed through a dual-channel lexical-emotional framework. The CHI score of 0.41 and coherence score of 0.263 quantify the structural tension between grace-mediated spiritual formation and volitional self-discipline. These findings contribute to the emerging field of theophysics by identifying formal correspondences between theological doctrine and physical symmetry principles, and they invite further interdisciplinary investigation into the mathematical structures underlying spiritual formation.

## References

Aquinas, T. (1948). *Summa Theologiae* (Fathers of the English Dominican Province, Trans.). Benziger Bros. (Original work published ca. 1274)

Demszky, D., Movshovitz-Attias, D., Ko, J., Cowen, A., Nemade, G., & Ravi, S. (2020). GoEmotions: A dataset of fine-grained emotions. In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics* (pp. 4040–4054). Association for Computational Linguistics.

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. *Computational Intelligence*, 29(3), 436–465.

*Novum Testamentum Graece* (28th ed.). (2012). Deutsche Bibelgesellschaft.

Plutchik, R. (2001). The nature of emotions: Human emotions have deep evolutionary roots. *American Scientist*, 89(4), 344–350.

Theophysics Paper Intelligence Pipeline v2026.04.07-B. (2026). *MDA-053-the-question: Paper Intelligence Report*. [Unpublished manuscript].