---
title: "Security"
description: "How to report security vulnerabilities affecting Plainsight Systems or any of its operating brands. Responsible disclosure policy."
date: 2026-04-21
---

Security is treated as a first-order concern across all Plainsight Systems operating brands. This page describes how to report vulnerabilities and how reports are handled.

Machine-readable contact metadata is published at [/.well-known/security.txt](/.well-known/security.txt) per RFC 9116.

## How to report

If you have identified a security vulnerability in plainsight-systems.com, in any operating brand's product, or in infrastructure operated on behalf of Plainsight Systems, email [security@plainsight-systems.com](mailto:security@plainsight-systems.com) with the subject line **"Security Report"**.

Please include, to the extent practical:

- the affected product, site, version, or endpoint;
- a description of the vulnerability;
- reproduction steps and any proof-of-concept materials;
- the potential impact as you understand it;
- your preferred contact address for follow-up.

You do not need to solve the vulnerability for us to consider the report valid. A clear demonstration is sufficient.

## What happens after you report

We will acknowledge receipt within three business days. We will confirm whether the report is in scope, request any clarifying information, and provide a reasonable expected timeline for remediation. You will be kept informed through remediation and public disclosure, where applicable.

## Scope

In scope:

- plainsight-systems.com and its supporting infrastructure;
- products shipped by PlainSight Lab, Appario, and CustodyZero, including public-facing applications, client software, firmware, APIs, and open-source releases under the company's stewardship;
- configuration of services operated on our behalf (DNS, CDN, email).

Out of scope:

- vulnerabilities in third-party services and dependencies that we do not operate (please report those to the responsible vendor);
- denial of service testing against production infrastructure;
- social engineering of employees, contractors, or customers;
- physical security of offices or facilities.

## Good-faith testing

We will not initiate legal action against researchers acting in good faith who:

- make a reasonable effort to avoid privacy violations, data destruction, and service disruption;
- do not access, modify, or retain data belonging to others beyond what is necessary to demonstrate the vulnerability;
- do not publicly disclose the vulnerability before we have had a reasonable opportunity to remediate (we aim for 90 days; extensions are available where remediation is non-trivial);
- comply with applicable law.

## Architectural non-contingency

Certain of our operating brands — notably CustodyZero — are designed so that categories of data never reach our systems. Where this is the case, the relevant brand's documentation describes the architectural guarantee. Reports that such a guarantee is not being upheld in practice are treated with the highest severity.

## Security updates

Security patches for supported major versions of Plainsight Systems products are provided **free of charge, regardless of subscription or license status**, for as long as producing them remains reasonably manageable. End-of-life for any major version is announced publicly with a transition window. This policy is documented in the [Licensing](/licensing/) doctrine.

## Contact

[security@plainsight-systems.com](mailto:security@plainsight-systems.com) · [/.well-known/security.txt](/.well-known/security.txt)

A PGP key may be made available on request.
