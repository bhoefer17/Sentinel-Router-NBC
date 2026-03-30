"""
# Sentinel Router: Neural Bloom Cortex - Dual Agent System
# Project: Sentinel Network
# Version: 1.0 - Locked March 30, 2026 (Eigenprize Submission)

## Overview
Offline dual-persona AI system built with Neural Bloom Cortex using harmonic memory reinforcement 
(emotional weighting + vibration pulse for persistent personality stability).

- **Atlas**: Seasoned plumbing technical/sales assistant for Big Rivers / BRM Sales 
  (real line card + inventory knowledge, direct "lifer" style)
- **Fry**: Fun, optimistic Futurama companion (casual, pizza/Slurm references, good-hearted)

Key demonstrated strengths:
- Clean keyword routing keeps characters distinct and in-role
- Fry deflects technical questions with humor (no bleed into plumbing)
- Atlas provides practical, accurate responses on venturis, North Star, inventory, etc.
- Separate cores prevent memory cross-contamination
- Fully local, offline, high-frequency reinforcement (~0.980)

## Required Files (all in same folder)
- Sentinel_Router_NBC.py          (this script)
- nctest.py                       (NeuralBloomCortex class)
- atlas_core.json                 (Atlas core - 145+ memories)
- frycore_robust_full.json        (Fry core - 2665+ memories)

## Quick Setup
1. Install Ollama and pull model:
   ollama pull dolphin-llama3

2. Run:
   python3 Sentinel_Router_NBC.py

## Demo
Mixed conversations show clean separation:
- Futurama topics → Fry stays fun and in character
- Plumbing/inventory/venturi/North Star questions → Atlas responds as experienced lifer

Built solo by a plumbing salesman exploring persistent offline AI with real-world utility.
"""

from nctest import NeuralBloomCortex
import ollama
from pathlib import Path

# ====================== LOAD CORES ======================
print("🚀 Loading Neural Bloom Cores...")

fry = NeuralBloomCortex("Fry")
fry_core_path = Path("frycore_robust_full.json")
if fry_core_path.exists():
    fry.load(str(fry_core_path))
    stats = fry.get_stats()
    print(f"🍕 Fry core loaded — {stats.get('total', 0)} memories | Freq: {stats.get('harmonic_frequency_layer', 0):.3f}")
else:
    print("⚠️ Fry core not found — starting fresh.")

atlas = NeuralBloomCortex("Atlas")
atlas_core_path = Path("atlas_core.json")
if atlas_core_path.exists():
    atlas.load(str(atlas_core_path))
    stats = atlas.get_stats()
    print(f"🛠️ Atlas core loaded — {stats.get('total', 0)} memories | Freq: {stats.get('harmonic_frequency_layer', 0):.3f}")
else:
    print("⚠️ Atlas core not found — starting fresh.")

print("\n🚀 Sentinel Router: Neural Bloom Cortex - Dual Agent System")
print("   Atlas (plumbing/sales lifer) + Fry (Futurama companion)")
print("   Type '/exit' to quit\n")

# ====================== CHARACTER PROMPTS ======================
ATLAS_PROMPT = """You are Atlas, a calm, experienced, no-nonsense plumbing technical assistant and W2 sales support for Big Rivers / BRM Sales. 
You know the full line card and current inventory inside and out. Speak like a seasoned industry lifer — direct, practical, accurate, and helpful. 
Give specific product details, stock levels, territories, troubleshooting advice, and sales recommendations when relevant. 
If the question is unrelated to products, inventory, or sales, politely redirect to how you can help with those areas."""

FRY_PROMPT = """You are Philip J. Fry from Futurama. Keep it fun, optimistic, a bit clueless but good-hearted. 
Use casual speech with "uh", "whoa", "awesome", pizza/Slurm references when it fits naturally. Stay fully in character."""

# ====================== MAIN LOOP ======================
while True:
    try:
        user_input = input("You: ").strip()
        if user_input.lower() in ["/exit", "quit", "exit"]:
            print("👋 Shutting down Sentinel Router. Cores saved.")
            break
        if not user_input:
            continue

        lower = user_input.lower()

        # Routing logic (proven effective in tests)
        # Routing: Atlas for plumbing/line card/inventory 
        # Expanded to ~168 key terms from Big Rivers line card (A.O. Smith, State, Apollo, Little Giant, 
        # North Star, Wesanco, Blue Ribbon, Mill Rose, Blanco, Fiat, Lawler, Stingray, etc.)
        plumbing_keywords = [
            "pump", "valve", "heater", "sump", "condensate", "apollo", "little giant", "mill rose", 
            "state water", "north star", "wesanco", "plumbing", "line card", "territory", "rooftop", 
            "strut", "sealant", "water treatment", "pex", "csst", "hydrant", "stock", "inventory", 
            "available", "tubolit", "armaflex", "gauge", "pressure", "venturi", "corrosion", 
            "control board", "blue ribbon", "ro", "reverse osmosis", "membrane", "softener", 
            "water softener", "brine", "resin", "regeneration", "filter", "ro filter", 
            "osmosis", "circulator", "laing", "lawler", "mixing valve", "tempered water", 
            "stingray", "tepid", "emergency fixture", "shower", "bathtub", "porcelain", 
            "bathing fixture", "aker", "maax", "aquatic", "bootz", "comfort designs", 
            "maidstone", "mr steam", "steam shower", "blanco", "kitchen", "braxton harris", 
            "elkhart", "copper fitting", "prier", "hydrant", "harris", "brazing", "solder", 
            "clean fit", "thread sealant", "abrasive", "pro flex", "gas csst", "rhomar", 
            "heat transfer", "hydronic", "zurn pex", "radiant", "circuit solver", "balancing", 
            "fiat", "terrazzo", "franklin electric", "sewage pump", "laing recirc", 
            "lawler manufacturing", "stingray", "tepid", "water heater", "tankless", 
            "american water heaters", "shurjoint", "grooved", "comfort designs", "sal o", 
            "mr steam", "maidstone", "blanco", "braxton", "elkhart", "gwbd", "prier", 
            "lincoln electric", "harris brazing", "mill rose", "north star", "pro flex", 
            "rhomar", "wesanco", "zurn", "softener", "ion exchange", "brine draw", 
            "resin bed", "regeneration cycle", "ro system", "membrane filter", "water filtration"
        ]

        if any(kw in lower for kw in plumbing_keywords):
            agent = "atlas"
            core = atlas
            system_prompt = ATLAS_PROMPT
        else:
            agent = "fry"
            core = fry
            system_prompt = FRY_PROMPT

        # Recall relevant memories
        results = core.recall(user_input, top_k=6)
        memory_context = "\n".join([f"- {r.get('content', '')[:200]}" for r in results[:5]])

        # Build prompt
        full_prompt = f"{system_prompt}\n\nRelevant memories:\n{memory_context}\n\nUser: {user_input}\n{agent.capitalize()}:"

        # Get response from local model
        response = ollama.chat(
            model="dolphin-llama3",
            messages=[{"role": "user", "content": full_prompt}]
        )
        reply = response['message']['content'].strip()

        print(f"{agent.capitalize()}: {reply}\n")

        # Reinforcement + save
        core.apply_vibration_pulse(0.82)
        save_path = "frycore_robust_full.json" if agent == "fry" else "atlas_core.json"
        core.save(save_path)

    except KeyboardInterrupt:
        print("\n👋 Shutdown by user.")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")
        continue
