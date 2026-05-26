---
title: "Vigil"
description: "Vigil is the Plainsight Systems edge-intelligence runtime — the substrate beneath Type, Valet, StationZero, and the rest of the catalogue. Built once, amortised across the company."
---

Vigil is the Plainsight Systems edge-intelligence runtime: a custom inference engine, built in-house, that runs capable models on the operator's own hardware. No cloud round-trip, no per-token meter, no telemetry pipe.

It is not a product. It is the layer every Plainsight Systems product stands on.

## Measured, not promised

Vigil is real, and it is instrumented. The runtime currently averages **93.8 tokens per second** of decode across all prompt lengths, on an Apple M3 — under coresident load, on silicon that is not current-generation, with the performance runs documented internally. Multi-token prediction and memory-layout optimisation, both on the near roadmap, target sustained decode of 100 tokens per second across all normal prompt lengths.

The current number is the average the engine actually reaches under load. The target is sustained — every prompt length, not just the mean. The distinction is load-bearing.

## Architecture

A product-neutral C++23 runtime, extracted from the Valet harness and a Gemma 4 mixture-of-experts implementation and now in active optimisation.

Backends are silicon-specific by design, not abstracted away. Apple Silicon, against MLX, is the first concrete backend — the one the published numbers come from. AMD Strix Halo, the target for StationZero on the home edge, is the next backend under active research. Each backend is written to the silicon it serves; honesty about hardware is part of the contract.

## What rides on it

Vigil is built once, and every Plainsight Systems instrument that needs intelligence rides on it. The marginal cost of the intelligence layer for each additional product trends toward zero — the hard part is already paid for. That is what makes the portfolio a portfolio, and not a sequence of unrelated bets.

The three proof surfaces of the company sit directly on Vigil:

- **Type** — a writing instrument for long-form work, with editorial intelligence that runs on the device rather than in a vendor's data center.
- **Valet** — ambient personal intelligence on the edge, learning its operator over time and running entirely on the operator's machine.
- **StationZero** — home edge safety hardware, watching and reasoning on the property without footage or inference leaving it.

Vigil also backs the rest of the catalogue: Appario's local-application path for merchants, and Plainsight Edge, the catalogue of single-purpose on-device utilities.

## A substrate, not a product

Vigil never ships as a standalone release. It has no customer-facing app of its own. It is consumed only through the products built on it.

That is deliberate. A runtime that has to defend its own roadmap, billing, and support surface stops compounding for the products that depend on it. Keeping Vigil internal — owned by the company, maintained as infrastructure — is what lets every product above it inherit the work without paying for it again.

The substrate is the durable asset. The products are how the substrate reaches a user.
