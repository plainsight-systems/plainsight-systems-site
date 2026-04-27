---
title: "Licensing"
description: "Plainsight Systems' licensing doctrine: how every system shipped by an operating brand is licensed, and why. Derived directly from the company thesis."
---

Plainsight Systems applies a single doctrine to everything its operating brands ship. The doctrine flows from the company thesis — that the operator retains authority that does not depend on our continued cooperation — and produces four distinct license postures for four distinct categories of artifact.

This page is the canonical statement. Individual products may add terms consistent with it; they may not add terms in conflict with it.

## Governance and coordination systems — Apache 2.0

Systems that sit in a position of judgment over the operator's work — change-control, agent coordination, governance protocols, rule enforcement — are released under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). A proprietary governor is a contradiction in terms: the operator cannot verify what they cannot read.

**Irrevocability.** Once a release of a governance or coordination system has been published under Apache 2.0, Plainsight Systems does not relicense, re-close, or withdraw that release. The operator's right to fork, modify, and redistribute persists regardless of subsequent company decisions, acquisitions, or dissolutions.

**Enterprise additions are permitted.** Plainsight Systems reserves the right to release proprietary enterprise editions of governance and coordination systems — typically containing support contracts, compliance packs, managed integrations, or hardening — alongside the Apache 2.0 base. The open base is not affected.

Current artifacts in this category: [Factory](https://github.com/CustodyZero/factory). Future governance artifacts released by PlainSight Lab's derivative entities fall under this posture unless explicitly stated.

## End-user instruments — perpetual license, free security patches

End-user instruments — applications the operator runs on their own hardware to produce work, process data, or administer a system — are sold under a perpetual license. The terms are uniform across brands:

- Purchase grants a permanent, non-revocable right to use the licensed version of the software.
- An active subscription grants access to feature updates during the subscription period. Updates released during an active subscription remain licensed to the operator permanently.
- Expiration or cancellation of the subscription does not revoke function. The last licensed version continues to operate indefinitely.
- Security patches for supported major versions are provided free of charge, regardless of subscription status, for as long as maintaining them remains reasonably manageable. End-of-life for a given major version requires documented public notice with a reasonable transition window.
- Local-first architecture, where applicable, removes dependency on company-operated servers for core function.

Current and near-term instruments under this posture include [Type](https://custodyzero.com/type/), [StationZero](https://custodyzero.com/), Valet, and [Appario](https://getappario.com) (transitioning from SaaS).

## Canonical specifications and written content — CC BY 4.0

Specifications, invariants, governance frameworks, mission documents, and other canonical written artifacts produced by PlainSight Lab and its derivative entities are released under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). The operator is free to use, adapt, and redistribute these materials with attribution, for any purpose including commercial.

Plurality of implementation is permitted. Plurality of canonical truth is not: implementations that claim conformance to a PlainSight Lab specification must remain faithful to its stated invariants.

## Brand assets — all rights reserved

The names "Plainsight Systems", "PlainSight Lab", "Appario", "CustodyZero", "StationZero", "Type", "Valet", "Factory", "Archon", and all associated wordmarks, logomarks, icons, and visual identity elements are trademarks or service marks of Plainsight Systems LLC. They are explicitly excluded from the Apache 2.0, CC BY 4.0, and perpetual license terms above.

Use of brand assets — including in derivative works, forks, or re-distributions — requires written permission.

## Summary

| Category | License | Irrevocable release? | Notes |
|---|---|---|---|
| Governance & coordination systems | Apache 2.0 | Yes | Enterprise additions permitted alongside |
| End-user instruments | Perpetual license + subscription feature updates | Yes (use right) | Free security patches for supported versions |
| Canonical specs and written content | CC BY 4.0 | Yes | Attribution required |
| Brand assets | All rights reserved | N/A | Written permission required |

## Contact

Licensing questions, enterprise enquiries, and permissions requests: [legal@plainsight-systems.com](mailto:legal@plainsight-systems.com).
