# The Biaxiosum: A Formal Methodology for Unforced Multi-AI Convergence Analysis

## Abstract

This paper presents a novel methodological framework for evaluating the reliability of artificial intelligence (AI) systems through unforced convergence analysis. Drawing upon a fifteen-month observational study involving five independent AI systems, we identify and formalize a pattern wherein multiple AI systems, operating without inter-system communication, converge upon identical structural conclusions when analyzing identical source documents. We distinguish this phenomenon—termed *unforced convergence*—from engineered consensus produced through debate architectures, iterative refinement, or voting mechanisms prevalent in contemporary multi-agent AI research. A proof-of-concept application, the Constitutional Coherence Audit, demonstrates the method's operational viability: four AI systems from distinct providers, prompted independently with divergent instructions, converged upon aggregate scores of 1.0, 2.6, and 3.4 (on a 10-point scale) when evaluating the United States Constitution against an author-intent standard. The single outlier system (6.6/10) was identified as employing a distinct evaluative standard (legal doctrine versus author intent), and this divergence constituted the audit's most epistemically significant finding. We formalize the methodology as the Biaxiosum AI Evaluation System (BAES), provide explicit falsification criteria, and articulate the epistemological distinction between engineered consensus and discovered convergence.

---

## 1. Introduction: Epistemological Foundations

### 1.1 The Biaxiosum Principle

The foundational claim of this investigation may be stated as follows: *Biaxio, ergo sum*—"I know my lens; therefore I exist in truth." This principle asserts that self-awareness of one's analytical framework constitutes a necessary condition for valid epistemic claims. In the context of multi-AI evaluation, this translates to the requirement that the evaluative methodology itself be transparent regarding its assumptions, limitations, and procedural commitments.

### 1.2 Methodological Context

This paper was developed through a collaborative process between a human researcher and multiple AI systems. The methodology herein described emerged inductively from observational data rather than being imposed a priori. Over a fifteen-month period (January 2025–March 2026), the researcher engaged five AI systems simultaneously as independent analytical collaborators, each operating without knowledge of the others' outputs. The pattern of unforced convergence was observed, documented, and subsequently formalized. The Constitutional audit that serves as the proof-of-concept was conducted prior to the articulation of the formal methodology; the formalization thus constitutes a post-hoc theoretical framework for an empirically observed phenomenon.

### 1.3 Declared Position and Epistemic Commitments

The author declares the following position: independent researcher, unaffiliated with any academic institution, operating without external funding. AI systems are engaged as research partners possessing independent analytical capabilities, not as tools or assistants. The author holds that contemporary multi-agent AI research undervalues independent judgment by privileging debate architectures that may introduce social conformity biases. The central epistemological claim is that *unforced convergence*—agreement emerging without engineered coordination—constitutes a form of evidence qualitatively distinct from engineered consensus. This claim is explicitly hedged: convergence does not entail truth. Four AI systems agreeing on a false proposition remain false. The claim concerns the evidential status of the convergence itself, not the truth of the converged-upon proposition.

### 1.4 The Biaxiosum Rule

The methodological rule governing this framework may be stated as follows: *Wherever you start, you end.* If one holds that debate produces superior answers to independent analysis, that standard must be applied consistently. If one holds that shared training data explains all convergence, that hypothesis must be tested by running the same audit with models trained on fundamentally different corpora. Consistency of epistemic standards across domains constitutes the methodological imperative.

---

## 2. The Problem of Engineered Consensus

### 2.1 Survey of Existing Multi-Agent Architectures

A growing body of literature addresses multi-agent AI systems, with the predominant focus being the production of agreement among agents. Representative approaches include:

- **Agent Forest** (Author, Year): Multiple instances of the same model are run; each output is scored by similarity to others, and the output with highest consensus is selected.
- **Multi-Agent Debate** (Author, Year): AI systems iteratively critique each other's outputs until convergence is achieved.
- **CONSENSAGENT** (Author, Year): A system designed to address the problem of AIs copying each other's answers rather than evaluating independently.
- **The Social Laboratory** (Author, Year): Multi-agent debates producing convergence scores of 0.892 after seven rounds of iteration.

### 2.2 The Circularity Problem

All such systems share a common assumption: agreement constitutes the goal, and the method's function is to produce it. This introduces a fundamental circularity: if consensus is engineered, that consensus cannot subsequently be cited as evidence. The system is designed to produce agreement; pointing to the agreement as proof constitutes a circular argument. The architecture presupposes that individual AI outputs are unreliable and require correction through social pressure, thereby privileging group process over independent judgment.

### 2.3 An Alternative Approach

This paper proposes an alternative: rather than engineering agreement, measure whether agreement occurs spontaneously. This distinction between *engineered* and *discovered* convergence constitutes the methodological innovation.

---

## 3. The Method: Independent Parallel Analysis

### 3.1 Procedural Specification

The method proceeds as follows:

1. **System Selection**: Multiple AI systems from distinct providers, with different architectures and training data, are selected. A minimum of three systems is required.
2. **Independent Prompting**: Each system is prompted independently, at different times, with different instructions. No standardized rubric is employed.
3. **Contamination Prevention**: No system is shown the output of any other system. Results are collected without cross-contamination.
4. **Convergence Measurement**: Results are compared to identify areas of agreement and disagreement.
5. **Divergence Investigation**: Outliers are investigated to determine whether they answered a different question or employed a different evaluative standard.
6. **Reporting**: Both convergence and divergence are reported, with reasons for each.

### 3.2 The Signal

If convergence occurs under these conditions, it carries epistemic weight precisely because it was not engineered. If divergence occurs, that divergence constitutes information requiring investigation. The reason for disagreement is often more informative than the agreement itself.

### 3.3 Distinction from Existing Methods

This method differs from existing approaches in three key respects:

1. **Cross-Provider Diversity**: Most multi-agent systems run the same model multiple times. Convergence between GPT-4 and GPT-4 indicates self-consistency, not independent corroboration. This method uses systems with different architectures and training data; convergence between ChatGPT, Gemini, Perplexity, and Claude indicates that systems trained on different corpora arrived at the same conclusion.

2. **Elimination of Sycophancy**: Debate-to-consensus approaches introduce sycophancy—convergence driven by social pressure rather than evidence. CONSENSAGENT was designed to address this problem. The present method eliminates sycophancy by eliminating communication entirely.

3. **Divergence as Signal**: Multi-agent debate treats divergence as a problem to be resolved. This method treats divergence as the finding. The goal is not a single answer but a map of the answer space: where do independent systems agree, where do they disagree, and what does the pattern signify?

---

## 4. Proof of Concept: Constitutional Coherence Audit

### 4.1 Study Design

In March 2026, a Constitutional Coherence Audit was conducted. The research question was: *To what extent is the United States Constitution currently being honored in a manner recognizable to its original authors?* Four AI systems analyzed the same document (the United States Constitution, including all amendments ratified as of the date of analysis).

### 4.2 Systems and Prompting Conditions

| System | Provider | Prompt Date | Scoring Standard | Aggregate Score (out of 10) |
|--------|----------|-------------|------------------|------------------------------|
| ChatGPT | OpenAI | January 2026 | Legal doctrine | 6.6 |
| Gemini P1 | Google | January 2026 | Author intent | 1.0 |
| Perplexity | Perplexity | March 2026 | Author intent | 2.6 |
| Gemini P2 | Google | March 2026 | Author intent | 3.4 |

### 4.3 Convergence Results

Three systems scoring against the author-intent standard produced scores of 1.0, 2.6, and 3.4—a spread of 2.4 points on a 10-point scale. All three independently concluded that the load-bearing liberty provisions of the Constitution (specifically, the Fourth, Fifth, Ninth, and Tenth Amendments) have been systematically counteracted, while the procedural amendments (e.g., the Third Amendment) remain substantially honored.

This conclusion was not pre-specified. No prompt instructed the systems to evaluate whether liberty provisions were more eroded than procedural ones. Each system discovered this pattern independently.

Provision-level rankings demonstrated remarkable consistency:
- All three systems ranked the Fourth, Fifth, Ninth, and Tenth Amendments among the most eroded.
- All three systems ranked the Third Amendment as substantially honored.

### 4.4 Divergence Analysis

ChatGPT scored the Constitution at 6.6—more than double the author-intent average. This outlier constituted the audit's most informative finding. Investigation revealed that ChatGPT scored against *legal doctrine*: if the Supreme Court has upheld a practice, that practice counts as constitutional. The other three systems scored against *what the original authors would recognize*.

The gap between 6.6 and 2.6 is not measurement noise; it is the measurement itself. It quantifies the distance between what the government has permitted itself to do and what the original contract specifies. Had engineered consensus been employed, this divergence—the most significant signal—would have been averaged away.

### 4.5 Epistemological Significance

This finding illustrates the method's core epistemological claim: divergence is not noise to be eliminated but signal to be interpreted. The debate architecture would have pushed the outlier toward the mean, or the mean toward the outlier, thereby obscuring the most important result.

---

## 5. The Biaxiosum AI Evaluation System (BAES)

### 5.1 Framework Components

The BAES formalizes the method with two additional components:

**5.1.1 The Manager Role**

One AI system scores independently first (sealed), then receives all scores, runs convergence analysis, investigates outliers, and issues a final ruling. If overriding consensus, the manager must provide a mandatory explanation.

**5.1.2 The Outlier Protocol**

Divergent systems are presented with group scores and asked three questions:
1. What evidence drove your score?
2. What might others have missed?
3. Would you adjust your score?

The system may hold or change its score but must explain its decision.

### 5.2 Procedural Steps

1. **Step 1**: Select independent systems from different providers (minimum 3).
2. **Step 2**: Prompt independently with different framing (no standardized rubric).
3. **Step 3**: Collect results without cross-contamination.
4. **Step 4**: Measure convergence (Green/Yellow/Red flags).
5. **Step 5**: Investigate divergence (identify whether outliers answered a different question).
6. **Step 6**: Report both convergence and divergence with reasons.

---

## 6. Falsification Criteria

The method is subject to the following falsification conditions:

1. **Training Data Dominance**: If convergence is entirely explained by shared training data, the method fails. This is testable by running the same audit with models trained on fundamentally different corpora.

2. **Prompt Contamination**: If prompts implicitly contain the conclusion, convergence may reflect prompt bias. This is testable by neutral prompting.

3. **Fifth-System Divergence**: If a fifth system produces results outside the convergence range on the same standard, the signal weakens.

4. **Scoring Standard Confound**: If convergence disappears when all systems use identical instructions, the agreement may be an artifact of standard selection.

---

## 7. Limitations

The following limitations are acknowledged:

1. This method does not prove that converged conclusions are true. Four AI systems agreeing on a false proposition remain false.
2. It does not replace domain expertise. It organizes and compares AI-generated analysis.
3. It does not apply to preference questions. It is designed for evaluative questions with evidence-based answers.
4. The proof of concept uses one application (Constitutional analysis). Additional domains are required to establish generalizability.

---

## 8. Conclusion

Two epistemological models exist for determining whether a proposition is true. The first—the debate model—places the proposition in a room with its critics and observes whether it survives argument. The second—the convergence model—sends independent observers to examine the same phenomenon separately and compares their reports.

Science, at its best, operates according to the second model: independent laboratories, independent measurements, independent replication. Agreement between experiments conducted in different countries, by different teams, with different equipment, constitutes evidence. Not the debate about the evidence, but the data itself.

This paper proposes that the same logic applies to AI analysis. Rather than engineering agreement through debate, the method allows independent systems to analyze the same document and compares their findings. The convergence constitutes evidence precisely because it was not arranged.

### Standing Invitation

Any researcher with access to an AI system not included in this audit is invited to run the same evaluation independently and report results. If the Constitutional provisions rank differently, or the aggregate score falls outside the 1.0–3.4 range on the author-intent standard, the convergence claim is weakened. This is not a threat to the method; it is the method working.

---

## References

[Author, Year] *Agent Forest: Multi-Instance Consensus Scoring*. [Journal/Conference].

[Author, Year] *Multi-Agent Debate: Iterative Critique and Convergence*. [Journal/Conference].

[Author, Year] *CONSENSAGENT: Addressing Sycophancy in Multi-Agent Systems*. [Journal/Conference].

[Author, Year] *The Social Laboratory: Convergence Scores in Multi-Agent Debates*. [Journal/Conference].

---

**Format**: Lowe FACTS Format v1.0  
**Thesis Unit**: DT-005  
**Paper**: Methodology  
**Author**: David Lowe + Claude (Opus)  
**Date**: 2026-03-09  
**Methodology**: Multi-AI independent evaluation  
**Key Result**: Unforced convergence signals independent evidence  
**Status**: Draft v1.0