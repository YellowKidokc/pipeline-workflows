```yaml
---
claims:
  - "Evidence must be classified into tiers from T1 (physical/forensic) to T5 (hearsay) so weak and strong claims are not treated equally"
  - "Each evidence item must be tested against F1-F10 forgery constraints to compute the compound probability of successful fabrication"
  - "Final verdict scoring combines evidence quality, falsification resistance, population density, soft signals, and protocol completion into one case score"
domains:
  Evidence Analysis: 40
  Verification Protocol: 30
  Probability Theory: 15
  Software Architecture: 15
---
```

# OpenIntel Platform

A step-by-step truth-finding system for settling disputes. It uses evidence tiers, fakery checks, population-density checks, timeline verification, soft signals, protocol status, and a final verdict score.

[**Open OpenIntel App](./) [**View Source Package](source-app/README.md) [**About / Protocol](about.html) [**Package Manifest](source-app/package.json)

### Evidence Tiers

Evidence gets sorted into levels from T1 (physical/forensic material) down to T5 (hearsay). This makes sure weak claims and strong claims are not treated the same way.

### Fakery Matrix

Each piece of evidence gets tested against F1 through F10 forgery constraints. The system then calculates the combined probability that the evidence could have been faked successfully.

### Verdict Scoring

The final score combines how good the evidence is, how hard it is to fake, how many people are involved, soft signals, and whether the full protocol was followed. All of this adds up to one case score.

## Deployment Note

The Kimi package is a Vite/React application with a Node/TRPC backend and database layer. The static site can host this Rigor entry and the source package, but the full interactive app needs its backend service and database deployed before the live UI can compute case data.

## Local Run Path

Source is staged at `subdomains/rigor/openintel-platform/source-app/`. From that folder, the app expects the normal Node workflow: install dependencies, configure environment variables from `.env.example`, seed/migrate the database, then run the Vite/API server.