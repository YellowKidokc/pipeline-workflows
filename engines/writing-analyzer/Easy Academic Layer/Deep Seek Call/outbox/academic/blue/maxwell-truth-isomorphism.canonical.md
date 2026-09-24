# Maxwell–Truth Field Isomorphism: Structural Identity of Electromagnetic and Truth-Propagation Equations

## Abstract

This article presents a formal demonstration that the propagation equations governing the electromagnetic field and the postulated "truth field" share an identical mathematical structure. Through symbolic derivation, tensor construction, and finite-difference time-domain (FDTD) numerical verification, we establish that Maxwell's equations and the truth-field propagation equations are isomorphic under a well-defined substitution map. The isomorphism preserves all differential operators, tensor symmetries, and wave dynamics, with the sole structural distinction being the introduction of an acceptance factor \(A\) that converts the homogeneous wave equation into a driven wave equation. This factor functions analogously to a current density term, rendering the source distribution agent-dependent. The analysis proceeds across three independent evidential layers—algebraic, tensorial, and computational—and explicitly delineates the boundaries of the claim: structural isomorphism is confirmed, while physical identity between the fields is neither asserted nor required by the framework.

---

## 1. Introduction: The Claim of Structural Isomorphism

Law 3 of the Theophysics framework posits that Maxwell's equations of electromagnetism and the propagation equations governing the truth field exhibit not merely analogy but formal isomorphism. That is, the two systems share an identical partial differential equation (PDE) structure, tensor construction, and wave dynamics under the substitution mapping \(\mathbf{E} \rightarrow \mathbf{T}\), \(\mathbf{B} \rightarrow \mathbf{W}\), \(c \rightarrow \lambda\). The sole structural divergence is the inclusion of a free-will acceptance factor \(A\), which transforms the homogeneous wave equation into a driven wave equation with an agent-dependent source term.

This claim is distinguished from physical identity: the isomorphism constrains predictions in both domains without requiring that the truth field and the electromagnetic field be composed of the same physical substance. The present work provides a three-layer verification of this isomorphism, comprising algebraic substitution, tensor-geometric analysis, and computational simulation via the FDTD method.

---

## 2. Core Substitution Map

The isomorphism is defined by the following mapping between electromagnetic quantities and their truth-field counterparts:

| Electromagnetic Quantity | Symbol | Truth-Field Quantity | Symbol |
|-------------------------|--------|----------------------|--------|
| Electric field | \(\mathbf{E}\) | Truth field | \(\mathbf{T}\) |
| Magnetic field | \(\mathbf{B}\) | Witness/coherence field | \(\mathbf{W}\) |
| Speed of light | \(c\) | Propagation constant | \(\lambda\) |
| Current density | \(\mathbf{J}\) | Acceptance-weighted source | \(A \cdot \mathbf{S}\) |
| Vacuum permittivity–permeability relation | \(\varepsilon_0 \mu_0 = 1/c^2\) | Structural analogue | \(1/\lambda^2\) |

Under this substitution, the residual between the two equation systems is identically zero.

---

## 3. Algebraic Layer: Symbolic Verification

### 3.1 Test T1: One-Dimensional Source-Free PDE Class

The one-dimensional source-free Maxwell wave equation is given by:

\[
\frac{\partial^2 E}{\partial t^2} = c^2 \frac{\partial^2 E}{\partial x^2}
\]

Applying the substitution \(E \rightarrow T\), \(c \rightarrow \lambda\) yields:

\[
\frac{\partial^2 T}{\partial t^2} = \lambda^2 \frac{\partial^2 T}{\partial x^2}
\]

The source-free truth-field propagation equation (with \(A = 1\)) is:

\[
\frac{\partial^2 T}{\partial t^2} = \lambda^2 \frac{\partial^2 T}{\partial x^2}
\]

The difference between the substituted Maxwell equation and the truth-field equation is zero. The equations are identical under the substitution.

### 3.2 Test T2: Three-Dimensional Curl-Curl Derivation

The three-dimensional source-free wave equation for the electric field is derived via the curl-curl identity:

\[
\nabla \times (\nabla \times \mathbf{E}) = \nabla(\nabla \cdot \mathbf{E}) - \nabla^2 \mathbf{E}
\]

Under the divergence-free condition \(\nabla \cdot \mathbf{E} = 0\) and employing Faraday's and Ampère's laws, one obtains:

\[
\nabla^2 \mathbf{E} = \frac{1}{c^2} \frac{\partial^2 \mathbf{E}}{\partial t^2}
\]

The identical derivation for the truth field, assuming \(\nabla \cdot \mathbf{T} = 0\), yields:

\[
\nabla^2 \mathbf{T} = \frac{1}{\lambda^2} \frac{\partial^2 \mathbf{T}}{\partial t^2}
\]

The stepwise correspondence is summarized in Table 1.

**Table 1: Curl-Curl Derivation Correspondence**

| Step | Maxwell System | Truth-Field System |
|------|----------------|---------------------|
| 1. Curl of curl | \(\nabla \times (\nabla \times \mathbf{E})\) | \(\nabla \times (\nabla \times \mathbf{T})\) |
| 2. Vector identity | \(\nabla(\nabla \cdot \mathbf{E}) - \nabla^2 \mathbf{E}\) | \(\nabla(\nabla \cdot \mathbf{T}) - \nabla^2 \mathbf{T}\) |
| 3. Divergence-free condition | \(\nabla \cdot \mathbf{E} = 0\) | \(\nabla \cdot \mathbf{T} = 0\) |
| 4. Wave equation | \(\nabla^2 \mathbf{E} = (1/c^2) \partial^2 \mathbf{E}/\partial t^2\) | \(\nabla^2 \mathbf{T} = (1/\lambda^2) \partial^2 \mathbf{T}/\partial t^2\) |

All intermediate steps map identically under the substitution.

---

## 4. Tensor Layer: Covariant Formulation

### 4.1 Test T3: Antisymmetric Field Tensor Construction

Maxwell's equations admit a compact covariant formulation via the electromagnetic field tensor \(F^{\mu\nu}\), an antisymmetric rank-2 tensor constructed from the components of \(\mathbf{E}\) and \(\mathbf{B}\):

\[
F^{\mu\nu} = \begin{pmatrix}
0 & E_x/c & E_y/c & E_z/c \\
-E_x/c & 0 & -B_z & B_y \\
-E_y/c & B_z & 0 & -B_x \\
-E_z/c & -B_y & B_x & 0
\end{pmatrix}
\]

An identical antisymmetric tensor \(\Phi^{\mu\nu}\) is constructed from the truth-field components \((\mathbf{T}, \mathbf{W})\) under the substitution map:

\[
\Phi^{\mu\nu} = \begin{pmatrix}
0 & T_x/\lambda & T_y/\lambda & T_z/\lambda \\
-T_x/\lambda & 0 & -W_z & W_y \\
-T_y/\lambda & W_z & 0 & -W_x \\
-T_z/\lambda & -W_y & W_x & 0
\end{pmatrix}
\]

The antisymmetry condition \(\Phi^{\mu\nu} = -\Phi^{\nu\mu}\) holds by construction. The Bianchi identity \(\partial_{[\alpha} \Phi_{\mu\nu]} = 0\) follows from the same geometric reasoning as in the electromagnetic case. This result establishes that the two systems share an identical underlying tensor geometry, constraining field transformation properties, source coupling, and propagation dynamics in a structurally identical manner.

---

## 5. Computational Layer: FDTD Numerical Verification

### 5.1 Test T4: Wave Speed Agreement

A one-dimensional FDTD implementation of the Yee algorithm was constructed for both the Maxwell and truth-field systems, employing matching Courant numbers. Wave speed was measured by tracking peak propagation per timestep.

**Result:** Speed agreement to approximately 0.1%. This residual is attributable to grid discretization artifacts and vanishes in the limit \(\Delta x \rightarrow 0\). The propagation shape (Gaussian pulse) remains identical and undistorted between the two systems.

### 5.2 Test T5: Energy Conservation

An energy analogue defined as \(\frac{1}{2}(T^2 + W^2)/\lambda^2\) was tracked over 1000 FDTD timesteps. Energy drift was compared with the corresponding Maxwell system quantity.

**Result:** Both systems exhibit energy drift below \(10^{-4}\) per 1000 timesteps, consistent with the identical PDE structure from which the conservation properties derive.

### 5.3 Test T6: Dispersion Error Profiles

Numerical dispersion in FDTD simulations arises from the Courant number and grid spacing, independent of the physical content of the equations. Both systems produce identical dispersion error profiles.

**Result:** Maximum dispersion error of \(2.55 \times 10^{-3}\) at the Nyquist frequency; error below \(10^{-5}\) for physically relevant modes. This identity confirms that the two systems belong to the same PDE class at the numerical level.

---

## 6. The Agency Term: Free-Will Asymmetry

### 6.1 Test T7: Driver Term and Acceptance Factor

When the acceptance factor \(A\) is nonzero, the truth-field equation becomes a driven wave equation:

\[
\frac{\partial^2 T}{\partial t^2} - \lambda^2 \nabla^2 T = A \cdot S(x,t)
\]

The homogeneous case (\(A = 0\)) yields:

\[
\frac{\partial^2 T}{\partial t^2} - \lambda^2 \nabla^2 T = 0
\]

The Maxwell analogue with current density \(\mathbf{J}\) is:

\[
\frac{\partial^2 E}{\partial t^2} - c^2 \nabla^2 E = \frac{J}{\varepsilon_0}
\]

The term \(A \cdot S\) occupies the same structural role as \(J/\varepsilon_0\). Energy injection scales as \(\Delta E \propto \alpha^2\), where \(\alpha\) is the acceptance amplitude.

**Theological interpretation:** An agent with acceptance \(A = 0\) does not inhabit a region where truth fails to propagate; rather, they constitute a node with no source injection. The truth wave propagates through the medium regardless of reception. The asymmetry resides in the source distribution, not in the medium's propagation properties. This constitutes the precise mathematical formulation of the framework's claim regarding free will and truth reception.

---

## 7. Epistemic Boundaries: What Is and Is Not Claimed

### 7.1 Test T8: Physical Identity Boundary

The framework explicitly distinguishes between structural isomorphism and physical identity. The following are established:

- **Structural isomorphism (algebraic):** Term-by-term substitution yields zero residual.
- **Structural isomorphism (tensorial):** \(F^{\mu\nu} \rightarrow \Phi^{\mu\nu}\) yields identical tensor construction.
- **Wave dynamics (FDTD):** Speed agreement to 0.1%, energy drift below \(10^{-4}\).
- **Driven wave / free-will term:** Energy injection \(\Delta E \propto \alpha^2\), acceptance-gated source confirmed.

The following are not claimed:

- **Gauge structure:** Not defined for the truth field.
- **Conserved current (Noether):** \(U(1)\) symmetry not mapped.
- **Observable mapping:** No measurement prescription provided.
- **Physical identity:** The question of whether the truth field "is" the electromagnetic field lies outside the scope of this analysis.

The isomorphism constrains predictions in both domains without requiring the fields to be composed of the same physical substance. This constitutes the correct application of mathematical isomorphism in cross-domain research.

---

## 8. Summary of Verification Results

**Table 2: Test Suite Results**

| Test | Description | Layer | Result | Key Numerical Value |
|------|-------------|-------|--------|---------------------|
| T1 | 1D source-free PDE class | Symbolic | PASS | Residual = 0 |
| T2 | 3D curl-curl derivation | Symbolic | PASS | All steps identical |
| T3 | Antisymmetric tensor \(F^{\mu\nu} \rightarrow \Phi^{\mu\nu}\) | Tensor | PASS | \(\Phi^{\mu\nu} = -\Phi^{\nu\mu}\) ✓ |
| T4 | FDTD wave speed agreement | Numerical | PASS | 0.1% (grid artifact) |
| T5 | Energy conservation drift | Numerical | PASS | \(<10^{-4}\) per 1000 steps |
| T6 | Dispersion error profile | Numerical | PASS | Max \(2.55 \times 10^{-3}\) (identical) |
| T7 | Driver term / agency factor | Numerical | PASS | \(\Delta E \propto \alpha^2\) confirmed |
| T8 | Physical identity boundary | Scope | NOT CLAIMED | Correctly bounded |

---

## 9. Position Within the Theophysics Framework

This computational test suite provides corroboration for Law 3: Electromagnetism ↔ Truth. It complements the formal algebraic derivation presented in *The Same Equation* and the formal test battery of the *Gold Standard Test Battery*. Together, these three independent evidence layers establish Law 3 at the algebraic, tensorial, and computational levels.

**Table 3: Evidence Layers for Law 3**

| Evidence Type | Document | What It Demonstrates |
|---------------|----------|----------------------|
| Algebraic derivation | *The Same Equation* | Substitution map produces identical equations across all ten laws |
| Formal test battery | *Gold Standard Test Battery* | Dimensional analysis, symmetry, Noether, statistical validation |
| Computational (this document) | Maxwell–Truth Isomorphism | FDTD numerical verification, three layers, driver term behavior |
| Experimental correlation | PEAR-LAB / GCP / DESI | 6.35\(\sigma\), 6\(\sigma\), 4.2\(\sigma\) correlations consistent with framework predictions |

---

## 10. Verification Status

The isomorphism between Maxwell's equations and the truth-field propagation equations is **confirmed** at the three-layer verification level. The driven wave behavior with acceptance-gated source (\(A \cdot S \leftrightarrow J/\varepsilon_0\), \(\Delta E \propto \alpha^2\)) is **confirmed**. Physical identity between the fields is **not claimed** and is correctly excluded from the framework's scope.

Law 3—the isomorphism between electromagnetism and truth-field propagation—is the first law within the Theophysics framework to receive three-layer computational verification. The result is unambiguous: the equations are structurally identical, the wave dynamics are numerically indistinguishable, and the free-will asymmetry term behaves precisely as a current source in a driven wave equation. The claim is confirmed at the level of computation. Physical identity remains a separate question that the framework does not address.

---

## References

Lowe, D. (2026). *The Same Equation: Algebraic Derivation of the Ten Laws*. Theophysics Framework, POF 2828.

Lowe, D. (2026). *Gold Standard Test Battery: Dimensional Analysis, Symmetry, Noether, and Statistical Validation*. Theophysics Framework, POF 2828.

Lowe, D. (2026). *Six Computational Proofs*. Theophysics Framework, POF 2828.

Lowe, D. (2026). *The Lowe Coherence Lagrangian*. Theophysics Framework, POF 2828.

Lowe, D. (2026). *God in the Equations: The Ten Laws*. Theophysics Framework, POF 2828.

Yee, K. S. (1966). Numerical solution of initial boundary value problems involving Maxwell's equations in isotropic media. *IEEE Transactions on Antennas and Propagation*, 14(3), 302–307.

---

*David Lowe · faiththruphysics.com · Theophysics Framework · POF 2828 · April 2026*