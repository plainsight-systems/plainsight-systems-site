---
title: "AI governance posture"
description: "How Plainsight Systems and its operating brands govern AI systems they ship — across data, model provenance, evaluation, telemetry, and the operator's authority to leave."
---

This page restates the thesis in operational terms. It is the answer to "how do you govern AI?" for reviewers, regulators, grant officers, and anyone working backwards from a product to its parent company.

The full thesis is at [About](/about/). The licensing doctrine that makes these commitments enforceable is at [Licensing](/licensing/). The artifacts that demonstrate the work is real are indexed at [Research](/research/). This page is the bridge — what governance commitments hold across every AI system shipped under Plainsight Systems LLC.

## Foundational position

The prevailing assumption is that intelligence is a service: rented from someone else's computer, metered by the token, withdrawn at the vendor's discretion. Plainsight Systems is built on the refutation. Intelligence belongs on the device — owned outright by the operator, on hardware they have already paid for. That bet binds the company to a single commitment: every system shipped is licensed, architected, and maintained so the person using it retains authority over it. Three claims follow:

- **The operator can see how the instrument functions.** Systems that sit in judgment positions — change-control, agent coordination, governance enforcement — are released open-source. A proprietary governor is a contradiction in terms.
- **The operator can change what the instrument does.** Canonical specifications are public. Scoring methodologies are explained. File formats are open. Local-first architectures put the substrate inside the operator's reach.
- **The operator can leave without losing what they built.** End-user instruments are perpetually licensed. Apache 2.0 releases of governance and coordination code are irrevocable. Local-first design eliminates dependence on company-operated servers.

The rest of this page documents how those claims hold at each layer of an AI system.

## Data minimisation

Operating brands are designed so that categories of personal data never reach our infrastructure.

- **CustodyZero** products run on the operator's hardware. Documents, agent activity, governance decisions, voice files, semantic indexes — all stay on the operator's machine. CustodyZero does not have visibility into them. This is an architectural property, not a policy promise.
- **PlainSight Lab** is a publication and stewardship layer. The site is a static publication; it does not collect user data.
- **Appario** collects what is necessary to deliver scans (email, store URL submitted, payment via Stripe — Appario does not store card numbers). It does not collect store contents beyond what is publicly accessible at the URL the operator provides.
- **The holding-company site** collects only role-address email correspondence and standard infrastructure logs. Documented in [Privacy](/privacy/).

Where data is not collected, it cannot be misused, breached, surrendered, or repurposed. This is the strongest form of data protection: architectural non-collection.

## Model provenance and execution

- **Open-weights models executed on the operator's hardware** are the default for operator-facing inference (Valet, Type's editorial assistant). When closed-weights APIs are involved (e.g., for editorial enhancement), the operator supplies their own API keys; the operating brand does not aggregate, broker, or proxy operator interactions with third-party model providers.
- **No operator data is used to train models** held by Plainsight Systems or its operating brands. We do not train models on customer data.
- **Model provenance** — which weights, what training-data discipline, what eval regime — is documented at the operating-brand level for each instrument that ships inference.

## Evaluation discipline

- **PlainSight Lab** publishes invariants and adversarial assumptions for systems that operate under coordinated misuse. These are public CC BY 4.0 artifacts; see [Research](/research/).
- **Factory** (Apache 2.0) enforces change-control discipline for AI-assisted development inside Plainsight Systems and is available to anyone shipping AI-assisted code: every change declares its intent; every acceptance is risk-proportional; every decision is auditable.
- **The standard for whether an instrument is shippable** is documented at the operating-brand level. There is no shippable threshold of "looks plausible" — outputs are bounded by enforceable invariants and constraint-based correction, not by post-hoc human override. (See, in the founder's published work, [Human Override Is Not Governance](https://andrewphunter.com/applications/human-override-is-not-governance/).)

## Telemetry and observation

- **CustodyZero products forbid telemetry by architectural design.** There is no covert observation pipe — even a dormant one — that Plainsight Systems could activate. Reports that any such pipe exists are treated as a security incident at the highest severity.
- Operating brands that **do** collect operational telemetry (Appario, the holding-company site) document exactly what is collected, why, the legal basis, retention, and processors. See respective privacy policies.
- **Architectural non-contingency**: where the brand's documentation states that data of a given type cannot reach our systems, that statement is enforceable in code and infrastructure, not by policy alone.

## Authority to leave

This is the load-bearing commitment. It is the difference between governance that is asserted and governance that is structural.

- **End-user instruments are licensed perpetually.** Purchase grants permanent right to use the licensed version. Subscription expiration does not revoke function.
- **Security patches for supported major versions are provided free of charge** regardless of subscription status, for as long as maintaining them remains reasonably manageable. End-of-life for a given major version requires documented public notice with a reasonable transition window.
- **Apache 2.0 releases of governance and coordination code are irrevocable.** The operator's right to fork, modify, and redistribute persists regardless of subsequent company decisions, acquisitions, or dissolutions.
- **Local-first architectures**, where applicable, remove the operator's dependency on the company's continued operation. If Plainsight Systems disappeared tomorrow, end-user instruments running on operator hardware would continue to function.

## Contact

- For governance, regulator, or research-collaboration enquiries: [legal@plainsight-systems.com](mailto:legal@plainsight-systems.com).
- For security or vulnerability reports: [security@plainsight-systems.com](mailto:security@plainsight-systems.com) — see [Security](/security/).
- For research collaboration around the published artifacts: see [Research](/research/).
