---
title: "Research"
description: "The Plainsight Systems research thesis and current threads — an audit of cargo-cult technology choices, with on-device LLMs, agentic-era code editors, transformer theory, and low-power device control as the live work."
---

The exploration audits cargo-cult technology choices — the defaults adopted by momentum rather than fit. Different domains, same lens: characterise the received default, name the problem it solved when it was adopted, measure whether that problem is still the binding constraint, and — if not — ask what a fresh choice would look like made today. Where the finding is *"the default is still right,"* that is also a result.

## Current threads

**On-device LLMs.** Hand-rolled C++ inference harnesses targeting the silicon they actually run on, no ML frameworks in the hot path. Air-gapped mixture-of-experts inference on Apple Silicon is reaching 80–90 tokens per second on an M3; higher-VRAM operator-owned hardware (AMD Strix Halo) is under research. The defaults being tested are that capable inference has to be a service rented from the cloud, and that framework portability is worth more than fit to the specific machine you're running on.

**Agentic-era code editor architecture.** What a code editor becomes when coding agents are first-class participants rather than plugins retrofitted onto a human's editor. Work-object models, operator-first interaction, and evaluation harnesses for measuring agentic editor performance against a defined task surface.

**Transformer theory from first principles.** Full implementation of the arc from Rosenblatt's Perceptron (1957) to Vaswani's Transformer (2017), in C#, without a machine-learning framework. The interesting question isn't which framework trains fastest — it's what is actually happening. Related work: [NeuralAscent](https://github.com/AndrewPHunter/NeuralAscent) (personal repository).

**Low-power device control.** Sub-GHz radios and wakeup-receiver architectures for scenarios where Bluetooth is the assumption but the range, power, or latency profile is wrong for the actual use case. Wireless accent lighting is the concrete example being characterised now.

## Where the work lives

- Open source: [github.com/plainsight-systems](https://github.com/plainsight-systems)
- Related personal work: [github.com/AndrewPHunter](https://github.com/AndrewPHunter)
- Longer-form writing: [andrewphunter.com](https://andrewphunter.com/)
