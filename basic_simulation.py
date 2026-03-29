import random
import time
from collections import defaultdict

# -------------------------------
# Simulated Transaction Class
# -------------------------------
class Transaction:
    def __init__(self, tx_id, tx_type, complexity):
        self.tx_id = tx_id
        self.tx_type = tx_type          # e.g., "transfer", "defi", "nft"
        self.complexity = complexity    # arbitrary cost units


# -------------------------------
# Energy Model (Simplified)
# -------------------------------
def estimate_energy(tx, cache_hit=True):
    """
    Simulate energy consumption.
    - Higher complexity = more energy
    - Cache hits reduce energy
    """
    base_energy = tx.complexity * 1.5

    if cache_hit:
        return base_energy * 0.7  # 30% savings
    else:
        return base_energy * 1.2  # penalty


# -------------------------------
# Baseline Execution (Random Order)
# -------------------------------
def baseline_execution(transactions):
    total_energy = 0
    cache = None

    for tx in transactions:
        cache_hit = (tx.tx_type == cache)
        energy = estimate_energy(tx, cache_hit)
        total_energy += energy

        cache = tx.tx_type

    return total_energy


# -------------------------------
# Energy-Aware Scheduling
# -------------------------------
def energy_aware_execution(transactions):
    """
    Group transactions by type to improve locality (simulate cache efficiency)
    """
    grouped = defaultdict(list)

    for tx in transactions:
        grouped[tx.tx_type].append(tx)

    optimized_order = []
    for tx_type in grouped:
        optimized_order.extend(grouped[tx_type])

    total_energy = 0
    cache = None

    for tx in optimized_order:
        cache_hit = (tx.tx_type == cache)
        energy = estimate_energy(tx, cache_hit)
        total_energy += energy

        cache = tx.tx_type

    return total_energy


# -------------------------------
# Workload Generator
# -------------------------------
def generate_transactions(n=100):
    tx_types = ["transfer", "defi", "nft"]

    transactions = []
    for i in range(n):
        tx_type = random.choice(tx_types)
        complexity = random.randint(1, 10)

        transactions.append(Transaction(i, tx_type, complexity))

    return transactions


# -------------------------------
# Main Experiment
# -------------------------------
def run_simulation():
    transactions = generate_transactions(200)

    # Shuffle for baseline randomness
    random.shuffle(transactions)

    baseline_energy = baseline_execution(transactions)
    optimized_energy = energy_aware_execution(transactions)

    print("==== Simulation Results ====")
    print(f"Baseline Energy:   {baseline_energy:.2f}")
    print(f"Optimized Energy:  {optimized_energy:.2f}")

    reduction = ((baseline_energy - optimized_energy) / baseline_energy) * 100
    print(f"Energy Reduction:  {reduction:.2f}%")


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    run_simulation()
