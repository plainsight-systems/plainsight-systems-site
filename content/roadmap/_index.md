---
title: "Roadmap"
description: "Plainsight Systems is one company with one substrate and three proof surfaces. Forward milestones — Type, StationZero, Valet — and the dependency chain that links them."
---

Plainsight Systems is one company with one substrate and three proof surfaces. The forward plan below picks up from March 2026, when the LLC was formed; the operating history is on [About](/about/).

## Timeline

| Window | Product | Milestone |
|---|---|---|
| **Q3 2026** | Type for Mac | Launch target |
| **Q4 2026** | StationZero | POC target |
| **Q1 2027** | Valet | Closed-alpha target |
| **2027** | StationZero | Investor-demo / beta path |

## How the milestones compound

Plainsight Systems is structured to amortise engineering work across the portfolio along two axes.

**Across products: one substrate.** Vigil is the shared edge-intelligence runtime — built once, consumed by every product that needs inference. Each new product takes a share of Vigil work and pays it forward to the next.

**Within a product: one core, native shells.** Every Plainsight Systems product is a central C++ business-logic core exposed across a stable ABI to thin platform-native UI shells. Each shell is *designed for* its target — Mac, Windows, iPad, custom hardware — not ported or wrapped. A new platform is a new shell, not a new product.

The forward sequence reflects both axes:

- **Type for Mac (Q3 2026)** ships against Vigil's Apple Silicon + MLX backend (already working) and a Swift shell over the Type core.
- **StationZero POC (Q4 2026)** is the first hardware target on AMD. The Vigil AMD backend built for StationZero is the same backend Type for Windows and Valet's Windows alpha need.
- **Type for Windows (Q1 2027, most likely)** is unlocked once the AMD backend is real; Intel may run on the same path, pending verification. The C++ core does not change — only the shell and the runtime under it.
- **Valet closed-alpha (Q1 2027)** ships on macOS and Windows simultaneously. Vigil supports both backends by then; Valet's core is consumed by a Swift shell on Mac and a native shell on Windows.

Vigil work paid for StationZero amortises across two Type variants and the Windows side of Valet's alpha. That is what the shared substrate buys — and what the per-target-shell architecture lets the company actually realise rather than promise.

## Type — Q3 2026 launch target (Mac)

Type is a keyboard-first writing instrument for long-form work. It is in **closed alpha** today; Q3 2026 is the alpha-to-publicly-purchasable transition for the Mac variant.

Three positioning wedges, deliberately broken trade-offs the field has treated as inevitable: **rich *and* fast** — full rich text without a markdown source layer or a preview toggle; **power without clutter** — a command palette as the spine, no panels, no mouse needed; **intelligence that is yours** — editorial assistance that runs on the device, on the Vigil substrate, with no telemetry and no cloud round-trip.

The Type product line continues on the same Type core:

- **Type for iPad** — committed, unscheduled. The iPad screens are already design-approved; the remaining work is the touch shell over the existing Apple-side Swift substrate.
- **Type for Windows** — Q1 2027, most likely. A new Windows shell over the same Type core, gated on Vigil's x86 backend (built for StationZero, per the section above). Intel pending verification on the same path.
- **Note — A Type companion** — committed, unscheduled. The phone companion app to Type.

Perpetual license, no telemetry, no kill switch. Free security patches for supported versions, regardless of subscription status — the [licensing doctrine](/licensing/) is uniform across the portfolio.

## StationZero — Q4 2026 POC target; 2027 investor-demo / beta path

StationZero is home edge safety, not cloud surveillance — a compute node that watches and reasons on the property, with footage and inference that never leave it.

**Q4 2026 — POC target.** Initial demo hardware is in hand. The POC is one safety scenario, end-to-end, on real hardware: camera feed in, local inference and context evaluation on the device, correct escalation decision out. No cloud dependency in the inference path. The decision must be observable, the logs must be honest, and the scenario must hold without simulation tricks.

**2027 — investor-demo / beta path.** What follows the POC, in sequence: one investor-grade demo chassis around existing hardware; a small batch of hand-built beta units; OEM and design-for-manufacture exploration with prospective hardware partners; beta BOM validation. This is *not* a manufacturing or shipping milestone — the round funds the path to a manufacturable product, not the manufacturing itself.

## Valet — Q1 2027 closed-alpha target

Valet is lifelong local personal intelligence on the operator's own silicon: an assistant that knows the user over time through temporal-aware semantic memory, runs entirely on the user's own hardware, and acts through substrate the user already controls (iCloud on Mac, Drive or OneDrive on Windows). Nothing leaves the device.

**Q1 2027 is a closed-alpha target — not a launch.** The alpha proves the local-intelligence loop on the user's compute: Vigil-backed inference, deterministic memory, composed shell, and action through the user's own cloud-storage substrate. Resident, not roving — the cross-device phone-marshalling lands at v1-launch.

A binding constraint carried from product definition: *the user installs the app, that's it.* No command line, no setup wizard, no first-launch script. Apple-philosophy elegance treated as a structural property of the install flow, not a polish step at the end.

**v1-launch — unscheduled.** Commercial cross-platform deliverable. Compute expands to Linux on a defensible subset; the phone side (iOS + Android) lands together for cross-device marshalling. The architecture admits all of this — the Valet core is the same; v1-launch is the work of two more native shells and Vigil on a third compute target.

---

The engine that makes the sequence possible is on [Vigil](/vigil/). Conversations with investors, operators, and collaborators who share the local-first thesis are welcome at [hello@plainsight-systems.com](mailto:hello@plainsight-systems.com).
