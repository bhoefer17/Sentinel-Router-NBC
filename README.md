# Sentinel Router: Neural Bloom Cortex - Dual Agent System
**Project:** Sentinel Network  
**Version:** 1.0 — Locked March 30, 2026 (Eigenprize Submission)

## What We Built
A fully offline dual-persona AI system using a custom **Neural Bloom Cortex** with harmonic memory reinforcement (emotional weighting + vibration pulse for persistent personality stability).

### Agents
- **Atlas** — Seasoned plumbing technical/sales assistant for Big Rivers / BRM Sales.  
  Contains the full line card + real inventory data (835+ memories) from the actual Excel stock file. Gives direct, practical, "lifer-style" answers with specific stock levels and warehouses.
- **Fry** — Fun, optimistic Futurama companion (2,665+ memories). Stays fully in character and deflects non-plumbing questions with humor.

### Key Innovation
Separate persistent cores + intelligent keyword routing + harmonic reinforcement keeps personalities stable and growing. No cloud, no resets, runs completely locally.

## Files Included
- `Sentinel_Router_NBC.py` — Locked router (CLI version)
- `sentinel_chat.py` — Clean pop-up Tkinter chat UI
- `nctest.py` — Neural Bloom Cortex class
- `atlas_core.json` — Enriched Atlas core (835+ memories with real inventory)
- `frycore_robust_full.json` — Fry core (large file — see note below)

## How to Run
```bash
python3 sentinel_chat.py

Type questions in the pop-up window. Atlas handles plumbing/inventory questions, Fry handles casual/Futurama topics.
Large Core Files Note
The frycore_robust_full.json (Fry core with 2,665+ memories) is too large for direct GitHub upload (>25MB).
It can be regenerated locally by running the Fry seeding script (available upon request) or provided separately.
The router works with empty cores as fallback, and the smaller atlas_core.json is included.
Demo
Mixed conversations show clean separation:
•  Futurama topics → Fry stays fun and in character
•  Plumbing/inventory/venturi/North Star questions → Atlas responds as experienced lifer
Future Scope (Phase 2+)
•  Persistent mesh network across devices
•  Glass-tile UI with rotating dashboard and follow-up tracker by manufacturer
•  Email triage + draft email tooling
•  Ara companion integration
•  Real robotic body + home sensor mesh + satellite node poof-of-concepts
Built solo by a plumbing salesman exploring persistent offline AI with real-world utility.
Sentinel Systems — Neural Interface v1.0
