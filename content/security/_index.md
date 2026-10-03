---
title: "Security"
description: "How to report security vulnerabilities in plainsight-systems.com and the Plainsight Systems open-source projects."
date: 2026-10-03
---

*Last updated: October 3, 2026.*

This page describes how to report a security vulnerability in plainsight-systems.com or in a Plainsight Systems open-source project, and how reports are handled. Machine-readable contact metadata is published at [/.well-known/security.txt](/.well-known/security.txt) per RFC 9116.

## How to report

Email [security@plainsight-systems.com](mailto:security@plainsight-systems.com) with the subject line **"Security Report"**.

Please include, to the extent practical:

- the affected site, repository, version, or endpoint;
- a description of the vulnerability;
- reproduction steps and any proof-of-concept materials;
- the potential impact as you understand it;
- your preferred contact address for follow-up.

You do not need to solve the vulnerability for the report to be valid. A clear demonstration is sufficient.

## What happens after you report

We will acknowledge receipt within three business days. We will confirm whether the report is in scope, request any clarifying information, and give a reasonable expected timeline for a fix. You will be kept informed through the fix and public disclosure, where applicable.

## Scope

In scope:

- plainsight-systems.com and its supporting infrastructure;
- the public repositories in the [plainsight-systems GitHub organization](https://github.com/plainsight-systems) and the demo pages published from them at plainsight-systems.github.io;
- configuration of services operated on our behalf (DNS, CDN, email).

Out of scope:

- vulnerabilities in third-party services and dependencies that we do not operate, including GitHub itself (please report those to the responsible vendor);
- denial-of-service testing against production infrastructure;
- social engineering of anyone associated with Plainsight Systems;
- physical security.

## Good-faith testing

We will not initiate legal action against researchers acting in good faith who:

- make a reasonable effort to avoid privacy violations, data destruction, and service disruption;
- do not access, modify, or retain data belonging to others beyond what is necessary to demonstrate the vulnerability;
- do not publicly disclose the vulnerability before we have had a reasonable opportunity to fix it (we aim for 90 days; extensions are available where a fix is non-trivial);
- comply with applicable law.

## Fixes

Fixes are made in the affected repository or site and noted in its history. The open-source projects are not sold or supported under contract, so there are no supported versions or patch schedules; the current default branch of each repository is the version that receives fixes.

## Contact

[security@plainsight-systems.com](mailto:security@plainsight-systems.com) · [/.well-known/security.txt](/.well-known/security.txt)

A PGP key may be made available on request.
