"""
Sentinel Chat - Pop-up UI for Eigenprize Submission
Run with: python3 sentinel_chat.py
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
from nctest import NeuralBloomCortex
import ollama
from pathlib import Path

# Load cores (same as your locked router)
fry = NeuralBloomCortex("Fry")
if Path("frycore_robust_full.json").exists():
    fry.load("frycore_robust_full.json")

atlas = NeuralBloomCortex("Atlas")
if Path("atlas_core.json").exists():
    atlas.load("atlas_core.json")

# Character prompts (your locked versions)
ATLAS_PROMPT = """You are Atlas, a calm, experienced, no-nonsense plumbing technical assistant and W2 sales support for Big Rivers / BRM Sales. 
You know the full line card and current inventory inside and out. Speak like a seasoned industry lifer — direct, practical, accurate, and helpful. 
Give specific product details, stock levels, territories, troubleshooting advice, and sales recommendations when relevant. 
If the question is unrelated to products, inventory, or sales, politely redirect to how you can help with those areas."""

FRY_PROMPT = """You are Philip J. Fry from Futurama. Keep it fun, optimistic, a bit clueless but good-hearted. 
Use casual speech with "uh", "whoa", "awesome", pizza/Slurm references when it fits naturally. Stay fully in character."""

# ====================== MAIN WINDOW ======================
root = tk.Tk()
root.title("Sentinel Systems • Neural Interface")
root.geometry("900x700")
root.configure(bg="#0a0a0a")

# Header
header = tk.Label(root, text="SENTINEL SYSTEMS", font=("Orbitron", 24, "bold"), fg="#00f0ff", bg="#0a0a0a")
header.pack(pady=10)

status = tk.Label(root, text="NEURAL CORE ONLINE • ATLAS + FRY ACTIVE", font=("Orbitron", 12), fg="#00ff9d", bg="#0a0a0a")
status.pack()

# Agent selector
agent_frame = tk.Frame(root, bg="#0a0a0a")
agent_frame.pack(pady=8)

current_agent = tk.StringVar(value="atlas")

tk.Radiobutton(agent_frame, text="ATLAS", variable=current_agent, value="atlas", 
               font=("Orbitron", 12), fg="#00f0ff", bg="#0a0a0a", selectcolor="#111").pack(side="left", padx=20)
tk.Radiobutton(agent_frame, text="FRY", variable=current_agent, value="fry", 
               font=("Orbitron", 12), fg="#ffcc00", bg="#0a0a0a", selectcolor="#111").pack(side="left", padx=20)

# Chat window
chat = scrolledtext.ScrolledText(root, height=25, font=("Consolas", 11), bg="#111", fg="#00f0ff", insertbackground="#00f0ff")
chat.pack(padx=20, pady=10, fill="both", expand=True)

def add_message(text, sender):
    tag = sender
    chat.insert(tk.END, f"{sender.upper()}: {text}\n\n", tag)
    chat.see(tk.END)

# Input
input_frame = tk.Frame(root, bg="#0a0a0a")
input_frame.pack(fill="x", padx=20, pady=8)

entry = tk.Entry(input_frame, font=("Consolas", 12), bg="#222", fg="#00f0ff", insertbackground="#00f0ff")
entry.pack(side="left", fill="x", expand=True, padx=(0,10))

def send():
    text = entry.get().strip()
    if not text:
        return
    add_message(text, "YOU")
    entry.delete(0, tk.END)
    
    # Use the exact same routing logic as your locked router
    lower = text.lower()
    plumbing_keywords = ["pump", "valve", "heater", "sump", "condensate", "apollo", "little giant", "mill rose", 
                         "state water", "north star", "wesanco", "plumbing", "line card", "territory", "rooftop", 
                         "strut", "sealant", "water treatment", "pex", "csst", "hydrant", "stock", "inventory", 
                         "available", "tubolit", "armaflex", "gauge", "pressure", "venturi", "corrosion", 
                         "control board", "blue ribbon", "ro", "reverse osmosis", "membrane", "softener", 
                         "water softener", "brine", "resin", "regeneration", "filter"]
    
    if current_agent.get() == "atlas" or any(kw in lower for kw in plumbing_keywords):
        agent = "atlas"
        core = atlas
        system_prompt = ATLAS_PROMPT
    else:
        agent = "fry"
        core = fry
        system_prompt = FRY_PROMPT
    
    results = core.recall(text, top_k=6)
    memory_context = "\n".join([f"- {r.get('content', '')[:200]}" for r in results[:5]])
    
    full_prompt = f"{system_prompt}\n\nRelevant memories:\n{memory_context}\n\nUser: {text}\n{agent.capitalize()}:"
    
    response = ollama.chat(model="dolphin-llama3", messages=[{"role": "user", "content": full_prompt}])
    reply = response['message']['content'].strip()
    
    add_message(reply, agent)
    
    # Reinforce
    core.apply_vibration_pulse(0.82)
    save_path = "frycore_robust_full.json" if agent == "fry" else "atlas_core.json"
    core.save(save_path)

send_btn = tk.Button(input_frame, text="SEND", font=("Orbitron", 11, "bold"), bg="#00f0ff", fg="#000", command=send)
send_btn.pack(side="right")

entry.bind("<Return>", lambda e: send())

# Welcome
add_message("Atlas online. Ready for stock checks, line card questions, or sales support.", "atlas")

root.mainloop()
