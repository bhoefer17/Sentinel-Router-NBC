import json
import time
import numpy as np
import threading
import os
from sentence_transformers import SentenceTransformer

class NeuralBloomCortex:
    def __init__(self, name="Fry", max_memories=5000):
        self.name = name
        self.max_memories = max_memories

        self.bloom_graph = {}
        self.memory_order = []
        self.memory_id_counter = 0

        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        # Core tuning
        self.memory_coherence = 0.82
        self.signal_amplification = 0.75
        self.emotional_retention = 0.85

        # Harmonic system 
        self.harmonic_resonance = 0.76
        self.brain_fine_tuning = 0.78
        self.harmonic_frequency_layer = 0.79

        # Dynamics
        self.reinforcement_rate = 0.11
        self.emotion_boost = 0.29
        self.decay_rate = 0.985
        self.decay_floor = 0.05

        self.recency_bias = 0.18
        self.diversity_pressure = 0.22

        self._embedding_cache = None

        self.lock = threading.Lock()

        print(f"🧠 {self.name} Neural Bloom Cortex v7.8 — Testing")

    def _rebuild_cache(self):
        if not self.memory_order:
            self._embedding_cache = None
            return
        embeddings = [self.bloom_graph[mid]["embedding"] for mid in self.memory_order]
        self._embedding_cache = np.array(embeddings, dtype=np.float32)

    def add_memory(self, content: str, memory_type: str = "personal", emotion_score: float = 0.5):
        with self.lock:
            mem_id = self.memory_id_counter
            self.memory_id_counter += 1

            embedding = self.embedder.encode(content).astype(np.float32)

            local_resonance = min(1.0, emotion_score * 0.85 + self.harmonic_resonance * 0.15)

            base = 0.60 + (emotion_score * self.emotion_boost)
            coherence_boost = self.memory_coherence * 0.32
            amplification_boost = self.signal_amplification * 0.24
            retention_boost = self.emotional_retention * (emotion_score ** 1.18)

            global_factor = (self.brain_fine_tuning + self.harmonic_resonance) / 2.0
            frequency_boost = self.harmonic_frequency_layer * 0.35

            final_strength = min(
                1.0,
                base + coherence_boost + amplification_boost + retention_boost + (global_factor * 0.42) + frequency_boost
            )

            self.bloom_graph[mem_id] = {
                "content": content,
                "embedding": embedding.tolist(),
                "strength": final_strength,
                "emotion": emotion_score,
                "resonance": local_resonance,
                "timestamp": time.time(),
                "type": memory_type,
                "last_similarity": 0.0
            }

            self.memory_order.append(mem_id)

            if len(self.memory_order) > self.max_memories:
                self._smart_prune()

            self._rebuild_cache()
            print(f"💾 Memory added | Strength: {final_strength:.3f}")
            return mem_id

    def _smart_prune(self):
        if not self.memory_order:
            return
        now = time.time()
        scores = []
        for mid in self.memory_order:
            mem = self.bloom_graph[mid]
            harmonic_weight = (mem["resonance"] + self.harmonic_frequency_layer) / 2.0
            age_hours = (now - mem["timestamp"]) / 3600
            recency = 1.0 / (1.0 + age_hours * self.recency_bias)
            score = mem["strength"] * harmonic_weight * recency * (0.6 + mem["emotion"] * 0.4)
            scores.append((mid, score))

        scores.sort(key=lambda x: x[1])
        to_remove = scores[0][0]
        del self.bloom_graph[to_remove]
        self.memory_order.remove(to_remove)

    def recall(self, query: str, top_k: int = 6):
        if not self.memory_order:
            return []

        if self._embedding_cache is None:
            self._rebuild_cache()

        query_vec = self.embedder.encode(query).astype(np.float32)

        with self.lock:
            now = time.time()
            similarities = self._embedding_cache @ query_vec

            results = []
            for i, mem_id in enumerate(self.memory_order):
                mem = self.bloom_graph[mem_id]
                semantic = similarities[i]

                age_hours = (now - mem["timestamp"]) / 3600
                recency = 1.0 / (1.0 + age_hours * self.recency_bias)

                global_factor = 0.72 + ((self.brain_fine_tuning + self.harmonic_resonance) / 2.0 * 0.28)
                frequency_factor = 0.75 + (self.harmonic_frequency_layer * 0.25)

                score = mem["strength"] * semantic * global_factor * frequency_factor * (0.85 + recency * 0.15)

                reinforcement = self.reinforcement_rate * semantic * (1.0 - mem["strength"] * 0.7)
                mem["strength"] = min(1.0, mem["strength"] + reinforcement)

                results.append((mem, score))

            results.sort(key=lambda x: x[1], reverse=True)

            selected = []
            seen = []
            for mem, score in results:
                if len(selected) >= top_k:
                    break
                vec = np.array(mem["embedding"], dtype=np.float32)
                if any(np.dot(vec, s) > (1.0 - self.diversity_pressure) for s in seen):
                    continue
                selected.append(mem)
                seen.append(vec)

            return selected

    def apply_vibration_pulse(self, intensity: float = 0.65):
        with self.lock:
            global_factor = 0.75 + ((self.brain_fine_tuning + self.harmonic_resonance) / 2.0 * 0.25)
            frequency_factor = 0.8 + (self.harmonic_frequency_layer * 0.2)

            for mem in self.bloom_graph.values():
                mem["strength"] = min(1.0, mem["strength"] + intensity * 0.085 * global_factor * frequency_factor)

            self.harmonic_frequency_layer = min(0.98, self.harmonic_frequency_layer + 0.022)
            self.harmonic_resonance = min(0.98, self.harmonic_resonance + 0.016)
            self.brain_fine_tuning = min(0.96, self.brain_fine_tuning + 0.011)

            self._rebuild_cache()
            print(f"⚡ Vibration pulse | Frequency Layer: {self.harmonic_frequency_layer:.3f}")

    def daily_maintenance(self):
        with self.lock:
            now = time.time()
            for mem in self.bloom_graph.values():
                age_days = (now - mem["timestamp"]) / 86400
                decay = self.decay_rate ** age_days
                retention = 0.80 + ((self.brain_fine_tuning + self.harmonic_resonance + self.harmonic_frequency_layer) / 3.0 * 0.20)
                mem["strength"] *= decay * retention
                mem["strength"] = max(self.decay_floor, mem["strength"])

            if len(self.bloom_graph) > 50 and len(self.bloom_graph) % 20 == 0:
                self._light_consolidation()

            self.harmonic_resonance *= 0.9992
            self.brain_fine_tuning *= 0.9993
            self.harmonic_frequency_layer *= 0.9994

            self._rebuild_cache()

        print(f"🌿 Maintenance complete | Memories: {len(self.bloom_graph)}")

    def _light_consolidation(self):
        print("🔄 Light consolidation running... (placeholder for future episodic summaries)")

    def get_stats(self):
        if not self.bloom_graph:
            return {"total": 0}

        strengths = [m["strength"] for m in self.bloom_graph.values()]
        return {
            "total": len(self.bloom_graph),
            "avg_strength": round(np.mean(strengths), 3),
            "high_emotion": sum(1 for m in self.bloom_graph.values() if m["emotion"] > 0.7),
            "harmonic_resonance": round(self.harmonic_resonance, 3),
            "brain_fine_tuning": round(self.brain_fine_tuning, 3),
            "harmonic_frequency_layer": round(self.harmonic_frequency_layer, 3)
        }

    def save(self, filename="frycore.json"):
        temp_file = filename + ".tmp"
        data = {
            "name": self.name,
            "memories": self.bloom_graph,
            "order": self.memory_order,
            "counter": self.memory_id_counter,
            "brain_fine_tuning": self.brain_fine_tuning,
            "harmonic_resonance": self.harmonic_resonance,
            "harmonic_frequency_layer": self.harmonic_frequency_layer
        }
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_file, filename)
        print(f"💾 Saved safely to {filename}")

    def load(self, filename="frycore.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.name = data.get("name", self.name)
            self.bloom_graph = {int(k): v for k, v in data.get("memories", {}).items()}
            self.memory_order = data.get("order", [])
            self.memory_id_counter = data.get("counter", len(self.bloom_graph))
            self.brain_fine_tuning = data.get("brain_fine_tuning", 0.78)
            self.harmonic_resonance = data.get("harmonic_resonance", 0.76)
            self.harmonic_frequency_layer = data.get("harmonic_frequency_layer", 0.79)
            self._rebuild_cache()
            print(f"📂 Loaded {len(self.bloom_graph)} memories | Frequency Layer: {self.harmonic_frequency_layer:.3f}")
            return True
        except FileNotFoundError:
            print("⚠️ No save file found — starting fresh.")
            return False
        except Exception as e:
            print(f"⚠️ Load error: {e}")
            return False


# ========================
# TEST ON MACBOOK
# ========================
if __name__ == "__main__":
    print("🚀 Starting Neurocore v7.8 test on MacBook...")
    cortex = NeuralBloomCortex("Fry")

    # Quick test memories
    cortex.add_memory("Your best friend is Bender, a bending robot. .", emotion_score=0.88)
    cortex.add_memory("you won a trio to the Slurm factory and learned the truth.", emotion_score=0.92)

    print("\n=== Recall Test ===")
    results = cortex.recall("best friend or slurm factory")
    for r in results:
        print(f"→ {r['content']} (Strength: {r.get('strength', 0):.3f})")

    cortex.apply_vibration_pulse(0.75)
    print("\nStats after vibration:", cortex.get_stats())

    cortex.daily_maintenance()
    cortex.save()

    print("\n✅ MacBook test complete. Ready for 3.1 MB import or Kratos seeding next.")
