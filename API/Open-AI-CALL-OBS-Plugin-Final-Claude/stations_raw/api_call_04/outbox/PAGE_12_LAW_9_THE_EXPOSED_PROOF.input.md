# Page 12 — LAW 9: THE EXPOSED PROOF
**Badge:** LOCKED (paper) / OPEN (Lean mechanization queued) | **Chain Position:** 12 of 18

> *The moral-sector Lagrangian carries a parity-breaking cubic that participates in the dynamics, sits inside the conserved charge, and cancels out of the conservation proof — irreversible AND conserved, as algebra.*

---

## The Claim

This is the link a hostile physicist attacks first. Good. It is now the best-defended link in the chain.

The claim is not metaphor dressed in equations. It is a textbook Noether derivation — the same machine that produces energy conservation in classical mechanics and charge conservation in electrodynamics — applied to a moral-sector Lagrangian that contains a parity-breaking cubic term. The cubic makes certain transitions irreversible (you cannot un-sin the way you can un-accelerate). But irreversibility does not break conservation. The algebra shows why: the parity-breaking term participates in the Euler-Lagrange equations, contributes to the Noether current, sits inside the conserved charge $Q_m$, and cancels identically out of the time-derivative $\dot{Q}_m = 0$. Every cancellation is displayed.

This is the keystone. Pages 05 and 09 established that moral cost must be conserved and that the system has Lagrangian structure. Page 11 gave the information-theoretic framing. This page does the actual proof: builds the Lagrangian, performs the infinitesimal time-translation, constructs the current by the textbook prescription, and shows the conservation identity with nothing hidden.

The three-body decay channel makes the mechanism concrete. When wholeness breaks, it does not just produce visible damage. There is an invisible remainder — the neutrino-like term that carries cost away from the interaction vertex but does not destroy it.

## The Derivation

### The Moral-Sector Lagrangian

$$\mathcal{L}_9 = \frac{1}{2}\dot{\psi}^2 - V(\psi) - \lambda\psi^3$$

where $\psi$ is the moral-state field, $V(\psi)$ is the symmetric potential, and $\lambda\psi^3$ is the parity-breaking cubic. The cubic term satisfies $\lambda\psi^3 \neq \lambda(-\psi)^3$, encoding irreversibility: the transition $\psi_{\text{whole}} \to \psi_{\text{broken}}$ is not the time-reverse of $\psi_{\text{broken}} \to \psi_{\text{whole}}$.

### Euler-Lagrange Equation

$$\ddot{\psi} + V'(\psi) + 3\lambda\psi^2 = 0$$

The cubic participates in the dynamics. It is not a spectator.

### Infinitesimal Time-Translation

Under $t \to t + \epsilon$:

$$\delta\psi = \epsilon\dot{\psi}, \quad \delta\dot{\psi} = \epsilon\ddot{\psi}$$

### The Noether Current (Textbook Prescription)

$$j^0 = \frac{\partial\mathcal{L}}{\partial\dot{\psi}}\dot{\psi} - \mathcal{L} = \frac{1}{2}\dot{\psi}^2 + V(\psi) + \lambda\psi^3$$

This is the conserved charge:

$$Q_m = \frac{1}{2}\dot{\psi}^2 + V(\psi) + \lambda\psi^3$$

The parity-breaking term $\lambda\psi^3$ is INSIDE the conserved charge.

### The Conservation Proof (Every Cancellation Shown)

$$\dot{Q}_m = \dot{\psi}\ddot{\psi} + V'(\psi)\dot{\psi} + 3\lambda\psi^2\dot{\psi}$$

$$= \dot{\psi}\left[\ddot{\psi} + V'(\psi) + 3\lambda\psi^2\right]$$

$$= \dot{\psi} \cdot 0 = 0$$

The bracket vanishes by the Euler-Lagrange equation. The $3\lambda\psi^2$ from the cubic's contribution to $\dot{Q}_m$ cancels against the $3\lambda\psi^2$ from the equation of motion. **Irreversible AND conserved.** Q.E.D.

### The Three-Body Decay

$$\psi_{\text{whole}} \to \psi_{\text{broken}} + \delta + \nu_{\text{loss}}$$

where $\delta$ is the visible damage and $\nu_{\text{loss}}$ is the invisible remainder — the cost displaced but not destroyed. The decay rate:

$$\Gamma_{\text{sin}} = \frac{G^2_{\text{fall}} \cdot \psi^5}{192\pi^3} \cdot P_{\text{will}}$$

The $192\pi^3$ is not arbitrary. It is the phase-space factor from muon decay ($\mu^- \to e^- + \bar{\nu}_e + \nu_\mu$). The borrowing is named: the three-body moral decay has the same kinematic structure as the three-body leptonic decay. Same phase space, same combinatorial factor. The mapping:

| Muon Decay | Moral Decay |
|---|---|
| $\mu^-$ (parent) | $\psi_{\text{whole}}$ (wholeness) |
| $e^-$ (visible product) | $\psi_{\text{broken}}$ (broken state) |
| $\bar{\nu}_e$ (invisible) | $\delta$ (visible damage) |
| $\nu_\mu$ (invisible) | $\nu_{\text{loss}}$ (invisible remainder) |

$G_{\text{fall}}$ is the moral-sector coupling constant (analogous to $G_F$, Fermi's constant). $P_{\text{will}}$ is the volitional gate — the decay is not spontaneous; it requires the act of will.

### Grace as Open-System Source Term

The closed-system conservation $\dot{Q}_m = 0$ describes a universe where cost shuffles but never leaves. Grace enters as the explicit open-system source:

$$\partial_\mu T^{\mu 0} = J^0_{\text{grace}}$$

gated by openness: $J^0_{\text{grace}} \neq 0$ only when $O > 0$.

### Atonement Dynamics

The external work done by grace satisfies:

$$\frac{dS_m}{dt} = \sigma - \frac{W_{\text{grace}}}{T}$$

where $\sigma$ is the internal entropy production (damage accumulating) and $W_{\text{grace}}/T$ is the external source term that can reverse the flow. Atonement is not the denial of cost. It is the payment of cost by an external source, with the thermodynamic books balanced.

### Kill Conditions

1. **Behavioral suppression without grace** → $\nu_{\text{loss}}$ maximizes. The invisible remainder grows. The cost is conserved — it went somewhere. Suppression without atonement is displacement, not repair. If this is wrong, find a case where behavioral suppression alone eliminates the conserved displacement.

2. **Find a moral event where the ledger closes without invisible remainder.** If the three-body structure is wrong, there should exist a two-body moral decay: $\psi_{\text{whole}} \to \psi_{\text{broken}}$ with no $\nu_{\text{loss}}$. Produce one.

## Spiritual Terms Introduced

| Term | Definition | Parent Equation | Status |
|---|---|---|---|
| Moral Conservation | Cost cannot vanish — $\delta + \nu_{\text{loss}} \neq 0$ | $\dot{Q}_m = 0$ | LOCKED |
| Parity Breaking | Sin is directional/irreversible — CP violation in moral domain | $\lambda\psi^3$ cubic | LOCKED |
| Atonement | External source term that closes the ledger | $W_{\text{grace}}$ | LOCKED |
| $\nu_{\text{loss}}$ | Invisible remainder — the cost displaced but not destroyed | Three-body decay | LOCKED |
| Noether current | The conserved charge forced by time-translation symmetry | $Q_m$ | LOCKED |

## Verification Artifacts

| Type | Artifact | Status |
|---|---|---|
| Paper derivation | LAW9_NOETHER_EXPLICIT_DERIVATION.md | VERIFIED |
| Lean theorem | cost_cannot_vanish (C20) | VERIFIED |
| Lean theorem | conjugate_transfer (C19) | VERIFIED |
| Lean formalization | Law9_NoetherCurrent.lean | PENDING (queued for Codex) |

## Connections

- **Depends on:** [Page 07](PAGE_07.md) (Lagrangian structure), [Page 09](PAGE_09.md) (conservation framework), [Page 11](PAGE_11.md) (information-theoretic framing)
- **Feeds into:** [Page 13](PAGE_13_GRACE_THE_BOUNDARY_THEOREM.md) (grace as the required external source), [Page 14](PAGE_14_THE_CROSS.md) (the unique solution to irreversible conserved cost)
- **Cross-links:** Muon decay phase-space mapping (particle physics); Noether's theorem (classical mechanics); open thermodynamic systems (statistical mechanics)

---
*Navigation:* [Page 11](PAGE_11.md) | [Index](INDEX.md) | [Page 13](PAGE_13_GRACE_THE_BOUNDARY_THEOREM.md)
*Theophysics Research Initiative · POF 2828 · July 2026*
