# The Lean 4 Corpus: Formal Verification of Theophysical Claims via Machine-Checkable Structures

## Abstract

This article presents a systematic analysis of the formal verification status of claims within the Theophysics Research Initiative, as instantiated in the Lean 4 theorem prover corpus. The investigation delineates which propositions possess machine-checkable structural proofs, which remain unverified, and where formal gaps persist. By constructing a layered scorecard across sixteen Lean files, the analysis establishes a rigorous evidentiary framework that distinguishes between fully verified theorems, partially formalized claims, and structurally unaddressed propositions. The methodology employs a four-move structural exposition—comprising the seven lanes of analysis, the sixteen-file layer scorecard, a filterable theorem inventory, and a false-positive detection queue—to render the verification status transparent and reproducible. This work constitutes an interlude within the broader corpus, directing readers to the canonical treatment for complete derivations while providing an accessible summary of the formal evidentiary landscape.

## 1. Introduction: The Formal Evidence Layer

The present investigation addresses a foundational epistemological question within theophysics: *What has Lean actually proved, and what has it not proved?* The formal evidence layer, as instantiated in the Lean 4 theorem prover (de Moura et al., 2015), provides a mechanism for determining which claims possess machine-checkable structural verification and where unresolved gaps remain. This framework treats proof, limits, and gaps as co-constitutive elements of the evidentiary structure, rather than as binary oppositions.

The analysis proceeds under the auspices of the Faith Through Physics research program, which posits that formal verification methods can be applied to theophysical claims without collapsing the distinct epistemological domains of physics and theology. The present document serves as a reader-facing interlude; the full canonical treatment, including complete arguments, tables, proofs, and source structure, remains linked for scholarly reference.

## 2. The Four-Move Structural Exposition

The verification status of the Lean 4 corpus is rendered accessible through a four-move structural exposition, each move corresponding to a distinct analytical layer:

### 2.1 Move One: The Seven Lanes

The seven lanes constitute the primary analytical categories through which the formal evidence is organized. These lanes delineate distinct domains of theophysical claims, each subject to independent verification protocols within the Lean 4 framework. The lanes function as load-bearing structural elements that support the subsequent scorecard analysis.

### 2.2 Move Two: The Sixteen-File Layer Scorecard

The sixteen Lean files are subjected to a layer scorecard analysis, which assigns verification status to each file based on the proportion of machine-checkable theorems contained therein. This scorecard names the load-bearing structure of the corpus before requiring the reader to follow the full derivation. The scorecard methodology is designed to provide an immediate assessment of verification completeness while acknowledging that partial verification constitutes meaningful evidentiary information.

### 2.3 Move Three: All Theorems—Filterable Inventory

A filterable inventory of all theorems within the corpus is provided, enabling selective examination of verification status by lane, file, or claim type. This inventory treats proof, limits, and gaps as equally informative categories within the evidentiary framework. The filterable structure permits researchers to isolate specific claims for detailed scrutiny while maintaining awareness of the broader verification landscape.

### 2.4 Move Four: False Positive Detection Queue

A dedicated queue identifies potential false positives—claims that appear verified but may contain undetected structural errors or implicit assumptions. This queue functions as a quality-control mechanism within the formal verification pipeline, acknowledging that machine-checkable structure does not guarantee epistemological soundness in the absence of correct specification.

## 3. Verification Status and Canonical Reference

The present document constitutes a short interlude within the broader Theophysics Research Initiative. It is designed to orient the reader to the verification landscape without replacing the canonical treatment. For complete derivations, source code, and full theorem statements, the reader is directed to the canonical page within the Lean 4 Corpus—Theophysics Research Initiative (Lowe, 2023). Following examination of the canonical source, the analysis continues to the bilateral audit of the Lean 4 verification framework.

## 4. Conclusion

The formal evidence layer, as instantiated in the Lean 4 corpus, provides a structured mechanism for assessing the verification status of theophysical claims. By distinguishing between fully proved theorems, partially formalized propositions, and structurally unaddressed claims, this analysis contributes to a rigorous evidentiary framework for interdisciplinary physics-theology research. The four-move structural exposition renders the verification landscape accessible while preserving the technical depth required for scholarly evaluation.

---

## References

de Moura, L., Kong, S., Avigad, J., van Doorn, F., & von Raumer, J. (2015). The Lean theorem prover (system description). In *Proceedings of the 25th International Conference on Automated Deduction* (pp. 378–388). Springer.

Lowe, D. (2023). *The Lean 4 Corpus—Theophysics Research Initiative* (Technical Report POF 2828). Faith Through Physics Research Initiative.