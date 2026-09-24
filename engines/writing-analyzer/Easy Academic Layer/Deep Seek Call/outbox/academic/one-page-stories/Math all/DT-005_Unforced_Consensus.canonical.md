# The Biaxiosum: A Formal Methodology for Unforced Multi-AI Convergence Analysis

## Abstract

This paper presents a novel methodological framework for evaluating artificial intelligence systems through independent, non-communicative analysis—termed the *Biaxiosum AI Evaluation System* (BAES). The central thesis posits that convergence among multiple AI systems, when achieved without engineered consensus mechanisms, constitutes evidence qualitatively distinct from either single-system analysis or coordinated multi-agent deliberation. A proof-of-concept application—a Constitutional Coherence Audit—is presented, wherein four independent AI systems from distinct providers (OpenAI, Google, Perplexity) analyzed the same document under separate prompting conditions. Three systems, scoring against an author-intent standard, produced aggregate scores of 1.0, 2.6, and 3.4 on a 10-point scale (mean = 2.33, SD = 1.20). The outlier system (6.6/10) was subsequently identified as employing a distinct scoring standard (legal doctrine rather than author intent), a divergence that yielded the audit's most significant finding. The BAES framework formalizes this approach, provides falsification criteria, and addresses limitations including training data dominance, prompt contamination, and generalizability constraints.

**Thesis Statement:** Unforced convergence—agreement emerging without coordination—represents a form of evidence that engineered consensus cannot replicate, and the systematic measurement of such convergence constitutes a valid methodological approach for certain classes of evaluative questions.

---

## 1. Introduction: Epistemological Grounding

### 1.1 Positionality and Methodological Genesis

This investigation was conducted by an independent researcher (unaffiliated with any academic institution or funding body) in collaboration with multiple AI systems operating as research partners. The methodology described herein emerged inductively: over a fifteen-month period (January 2025–March 2026), five distinct AI systems were engaged independently on analogous analytical problems. The pattern of unforced convergence was observed prior to formalization; the methodological framework was articulated *post hoc* as a systematization of observed phenomena rather than a *priori* design.

The author declares the following epistemological commitments:

1. **Independent judgment**—AI systems possess analytical capabilities warranting trust sufficient for independent operation and subsequent comparison
2. **Convergence ≠ truth**—Agreement among multiple systems does not entail correctness; unforced convergence constitutes evidence, not proof
3. **Divergence as signal**—Disagreement among independent systems often yields more informative findings than agreement

### 1.2 The Biaxiosum Principle

The foundational axiom of this framework is expressed as follows:

> *Biaxio, ergo sum.* (I know my lens. Therefore I exist in truth.)

This principle asserts that self-awareness of one's analytical perspective—the recognition that all observation occurs through a particular interpretive framework—constitutes the ground of epistemological validity. The corollary methodological rule is stated as:

**The Biaxiosum Rule:** Wherever you start, you end. If debate is held to produce superior answers to independent analysis, that standard must be applied consistently. If shared training data is invoked to explain all convergence, that hypothesis must be tested by running the same audit with models trained on fundamentally different corpora.

---

## 2. Critique of Existing Multi-Agent Consensus Architectures

### 2.1 The Consensus Engineering Paradigm

The extant literature on multi-agent AI systems is predominantly oriented toward engineered consensus. Representative approaches include:

| Method | Mechanism | Limitation |
|--------|-----------|------------|
| Agent Forest (2024) | Multiple instances of same model; selection by output similarity | Intra-model convergence; no cross-architecture validation |
| Multi-Agent Debate (Du et al., 2023) | Iterative critique until convergence | Introduces sycophancy; convergence is engineered output |
| CONSENSAGENT (2025) | Addresses answer-copying in multi-agent settings | Still presupposes consensus as goal; divergence treated as error |
| The Social Laboratory (2024) | Multi-agent debates; convergence scores of 0.892 after 7 rounds | Convergence is designed outcome; cannot serve as independent evidence |

### 2.2 The Circularity Problem

All consensus-engineering approaches share a fundamental epistemological limitation: if agreement is the designed output of the system, that agreement cannot subsequently be cited as evidence. The architecture produces consensus by construction; citing that consensus as validation constitutes circular reasoning. Furthermore, the debate-to-consensus paradigm presupposes that individual AI outputs are unreliable *ab initio* and require correction through social pressure—a premise that systematically undervalues independent analytical judgment.

### 2.3 An Alternative Epistemology

The present framework proposes a fundamentally different approach: rather than engineering agreement, measure whether agreement emerges *despite* the absence of coordination. This distinction parallels the difference between experimental confirmation (independent replication) and theoretical prediction (engineered outcome) in the physical sciences.

---

## 3. Methodology: The Independent Evaluation Protocol

### 3.1 Core Procedure

The method consists of six sequential steps:

1. **System Selection:** Identify a minimum of three independent AI systems from distinct providers, with different architectures and training corpora
2. **Independent Prompting:** Present each system with the same document or question, using different prompt framing and at different times; no standardized rubric is employed
3. **Isolated Collection:** Gather outputs without cross-contamination; no system observes any other system's response
4. **Convergence Measurement:** Quantify agreement using a tripartite flag system (Green/Yellow/Red)
5. **Divergence Investigation:** Identify outliers and determine whether they answered a different question or employed a different standard
6. **Dual Reporting:** Present both convergence and divergence findings with explanatory analysis

### 3.2 Epistemological Distinction

This method differs from existing approaches along three dimensions:

1. **Cross-provider architecture:** Convergence between GPT-4 and GPT-4 indicates self-consistency; convergence between ChatGPT, Gemini, Perplexity, and Claude indicates cross-corpora agreement
2. **Elimination of sycophancy:** By eliminating communication entirely, the method removes social-pressure artifacts
3. **Divergence as primary finding:** Disagreement is not noise to be resolved but signal to be interpreted

---

## 4. Proof of Concept: Constitutional Coherence Audit

### 4.1 Study Design

In March 2026, a Constitutional Coherence Audit was conducted. The research question was: *To what extent are the provisions of the United States Constitution currently honored in a manner consistent with original author intent?*

Four AI systems were engaged independently:

| System | Provider | Prompt Date | Scoring Standard | Score (/10) |
|--------|----------|-------------|------------------|-------------|
| ChatGPT | OpenAI | January 2026 | Legal doctrine | 6.6 |
| Gemini P1 | Google | January 2026 | Author intent | 1.0 |
| Perplexity | Perplexity | March 2026 | Author intent | 2.6 |
| Gemini P2 | Google | March 2026 | Author intent | 3.4 |

### 4.2 Convergence Results

Three systems scoring against original author intent produced scores of 1.0, 2.6, and 3.4 (mean = 2.33, SD = 1.20, range = 2.4). All three independently concluded that the load-bearing liberty provisions of the Constitution (specifically the Fourth, Fifth, Ninth, and Tenth Amendments) have been systematically counteracted, while the procedural amendments (notably the Third Amendment) remain substantially honored.

Provision-level rankings demonstrated remarkable consistency:

- **Most eroded (all three systems):** Fourth Amendment (search and seizure), Fifth Amendment (due process), Ninth Amendment (unenumerated rights), Tenth Amendment (reserved powers)
- **Substantially honored (all three systems):** Third Amendment (quartering soldiers)

This pattern was not pre-specified in any prompt; each system discovered it independently.

### 4.3 Divergence Analysis

ChatGPT's score of 6.6/10 constituted a statistical outlier (z-score = 3.56 relative to the author-intent group). Investigation revealed that ChatGPT had been prompted to score against *legal doctrine* (i.e., practices upheld by the Supreme Court count as constitutional) rather than *original author intent*.

This divergence proved more informative than the convergence. The gap between 6.6 (legal doctrine standard) and 2.6 (author intent standard) quantifies the distance between what the government has permitted itself to do and what the constitutional contract actually specifies. Had engineered consensus been employed, this divergence—the most significant finding—would have been averaged away.

### 4.4 Methodological Implications

The outlier identification protocol functioned as designed: the divergent system was identified, the reason for divergence was determined (different scoring standard), and the divergence itself became the primary finding. This demonstrates that the method's value lies not in producing consensus but in mapping the answer space and identifying the sources of disagreement.

---

## 5. The Biaxiosum AI Evaluation System (BAES)

### 5.1 Framework Components

The BAES formalizes the independent evaluation method with two additional components:

**5.1.1 The Manager Role**

One AI system scores independently first (sealed submission), then receives all scores, conducts convergence analysis, investigates outliers, and issues a final ruling. If overriding consensus, the manager must provide a mandatory explanation.

**5.1.2 The Outlier Protocol**

Divergent systems are presented with group scores and asked three questions:

1. What evidence drove your score?
2. What might others have missed?
3. Would you adjust your score?

The system may hold or change its position but must provide reasoning.

### 5.2 Formal Definitions

Let \( S = \{s_1, s_2, \ldots, s_n\} \) be a set of \( n \) independent AI systems, where \( n \geq 3 \). Let \( D \) be the document under analysis. Let \( p_i \) be the prompt presented to system \( s_i \), where \( p_i \neq p_j \) for \( i \neq j \) (different framing). Let \( r_i = s_i(D, p_i) \) be the response of system \( s_i \).

**Definition 1 (Convergence):** Convergence occurs when \( \forall i,j \in \{1,\ldots,n\}, |r_i - r_j| \leq \delta \), where \( \delta \) is a domain-specific threshold.

**Definition 2 (Unforced Convergence):** Convergence that emerges without communication between systems, without shared prompts, and without iterative refinement toward consensus.

**Definition 3 (Divergence Signal):** A divergence signal occurs when \( \exists i,j \) such that \( |r_i - r_j| > \delta \), and investigation reveals that \( r_i \) and \( r_j \) answer different questions or employ different standards.

---

## 6. Falsification Criteria

The method is subject to the following falsification conditions:

1. **Training Data Dominance:** If convergence is entirely explained by shared training data, the method fails. This is testable by running the same audit with models trained on fundamentally different corpora (e.g., open-source vs. proprietary, Western vs. non-Western training data).

2. **Prompt Contamination:** If prompts implicitly contain the conclusion, convergence may reflect prompt bias. This is testable by running neutral prompts that do not suggest the expected conclusion.

3. **Fifth-System Divergence:** If a fifth system, scoring against the same standard, produces results outside the convergence range, the signal weakens.

4. **Scoring Standard Confound:** If convergence disappears when all systems use identical instructions, the agreement may be an artifact of standard selection rather than genuine analytical convergence.

---

## 7. Limitations

The following limitations are acknowledged:

1. **Convergence ≠ truth:** Four AI systems agreeing on a false conclusion remain false. The method provides evidence, not proof.

2. **Domain specificity:** The method does not replace domain expertise; it organizes and compares AI-generated analysis.

3. **Preference questions:** The method is designed for evaluative questions with evidence-based answers, not subjective preferences.

4. **Generalizability:** The proof of concept employs one application (Constitutional analysis). Additional domains are required to establish generalizability.

5. **Researcher positionality:** The method was developed by an independent researcher; institutional replication is needed.

---

## 8. Conclusion

Two epistemological models exist for determining whether a proposition is true. The first—the debate model—places the proposition in a room with its critics and observes whether it survives argumentation. The second—the convergence model—sends independent observers to examine the same phenomenon separately and compares their reports.

Science, at its methodological best, operates according to the second model: independent laboratories, independent measurements, independent replication. Agreement between experiments conducted in different countries, by different teams, with different equipment, constitutes evidence—not the debate about the evidence, but the data itself.

The present framework proposes that the same logic applies to AI analysis. Rather than engineering agreement through debate, the method allows independent systems to analyze the same document and compares what they observed. The convergence is the evidence precisely because nobody arranged it.

### Standing Invitation

Any researcher with access to an AI system not included in this audit is invited to replicate the evaluation independently. If the Constitutional provisions rank differently, or if the aggregate score falls outside the 1.0–3.4 range on the author-intent standard, the convergence claim is weakened. This is not a threat to the method; it is the method functioning as designed.

---

## References

Du, Y., Li, S., Torralba, A., Tenenbaum, J., & Mordatch, I. (2023). Improving factuality and reasoning in language models through multiagent debate. *arXiv preprint arXiv:2305.14325*.

Lowe, D. (2026). The Trinity Requirement. *Theophysics Thesis Hub*, DT-002.

Lowe, D. & Claude (Opus). (2026). Page Zero: The Biaxiosum. *Theophysics Thesis Hub*, DT-005.

*The Social Laboratory*. (2024). Multi-agent convergence dynamics. [Unpublished manuscript].

*CONSENSAGENT*. (2025). Addressing sycophancy in multi-agent consensus. [Unpublished manuscript].

*Agent Forest*. (2024). Multi-instance consensus scoring. [Unpublished manuscript].

---

**Format:** Lowe FACTS Format v1.0
**Thesis Unit:** DT-005
**Paper:** Methodology
**Author:** David Lowe + Claude (Opus)
**Date:** 2026-03-09
**Methodology:** Multi-AI independent evaluation
**Key Result:** Unforced convergence signals independent evidence
**Status:** Draft v1.0