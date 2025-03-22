import random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

class Tracker:
    def __init__(self, raw, cs, agi):
        self.raw = raw
        self.cs = cs
        self.agi = agi
    
    def display_sum(self):
        return self.raw + self.cs + self.agi

    def critical_value(self, level):
        critical_multipliers = {0: 1.25, 1: 1.28, 2: 1.31, 3: 1.34, 4: 1.37, 5: 1.40}
        base_damage = self.display_sum()
        return base_damage * critical_multipliers.get(level, 1.25)

    def apply_attack_boost(self, attack_boost_level):
        if attack_boost_level == 1:
            total_raw = self.raw + 3
        elif attack_boost_level == 2:
            total_raw = self.raw + 5
        elif attack_boost_level == 3:
            total_raw = self.raw + 7
        elif attack_boost_level == 4:
            total_raw = (self.raw * 1.02) + 8
        elif attack_boost_level == 5:
            total_raw = (self.raw * 1.04) + 9
        else:
            total_raw = self.raw
        return total_raw

    def simulate_hits(self, crit_chance, crit_level, og_uptime, attack_boost_level):
        total = self.apply_attack_boost(attack_boost_level)
        critical_total = self.critical_value(crit_level)

        hits = []
        cumulative_hits = []
        cumulative_sum = 0
        
        for _ in range(100):
            offensive_guard_active = random.random() < (og_uptime / 100)
            critical_active = random.random() < (crit_chance / 100)

            if offensive_guard_active:
                total_with_og = total * 1.15
            else:
                total_with_og = total

            if critical_active:
                hits.append(total_with_og * critical_total / total)
            else:
                hits.append(total_with_og)
                
        return sum(hits) / len(hits), hits

    def offensive_guard_boost(self):
        return self.display_sum() * 0.15

def calculate():
    try:
        raw = int(raw_entry_1.get())
        cs = int(cs_entry_1.get())
        agi = int(agi_entry_1.get())
        crit_level = int(crit_level_entry_1.get())
        attack_boost_level = int(attack_boost_entry_1.get())
        crit_chance = float(crit_chance_entry_1.get())
        og_uptime = float(og_uptime_entry_1.get())

        tracker = Tracker(raw, cs, agi)

        total_damage_per_hit = tracker.apply_attack_boost(attack_boost_level) + tracker.cs + tracker.agi
        avg_damage, total_damage = tracker.simulate_hits(crit_chance, crit_level, og_uptime, attack_boost_level)

        og_boost = tracker.offensive_guard_boost()

        result_label.config(text=f"Damage Per Hit: {total_damage_per_hit}\n"
                                f"Average Damage Per Hit (Simulated over 100 hits): {avg_damage}\n"
                                f"Offensive Guard Damage Boost: {og_boost}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

def simulate_and_plot():
    try:
        raw_1 = int(raw_entry_1.get())
        cs_1 = int(cs_entry_1.get())
        agi_1 = int(agi_entry_1.get())
        attack_boost_level_1 = int(attack_boost_entry_1.get())
        crit_level_1 = int(crit_level_entry_1.get())
        crit_chance_1 = float(crit_chance_entry_1.get())
        og_uptime_1 = float(og_uptime_entry_1.get())

        raw_2 = int(raw_entry_2.get())
        cs_2 = int(cs_entry_2.get())
        agi_2 = int(agi_entry_2.get())
        attack_boost_level_2 = int(attack_boost_entry_2.get())
        crit_level_2 = int(crit_level_entry_2.get())
        crit_chance_2 = float(crit_chance_entry_2.get())
        og_uptime_2 = float(og_uptime_entry_2.get())

        tracker_1 = Tracker(raw_1, cs_1, agi_1)
        tracker_2 = Tracker(raw_2, cs_2, agi_2)

        avg_damage_1, hits1 = tracker_1.simulate_hits(crit_chance_1, crit_level_1, og_uptime_1, attack_boost_level_1)
        avg_damage_2, hits2 = tracker_2.simulate_hits(crit_chance_2, crit_level_2, og_uptime_2, attack_boost_level_2)
        
        #simulate variance
        variance1 = [tracker_1.simulate_hits(crit_chance_1, crit_level_1, og_uptime_1, attack_boost_level_1)[0] for _ in range(100)]
        variance2 = [tracker_2.simulate_hits(crit_chance_2, crit_level_2, og_uptime_2, attack_boost_level_2)[0] for _ in range(100)]

        plot_histogram(hits1, hits2, avg_damage_1, avg_damage_2, variance1, variance2)
        #plot_line_graph(hits1, hits2, avg_damage_1, avg_damage_2)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

def plot_histogram(hits1, hits2, avg_damage_1, avg_damage_2, variance1, variance2):
    
    if avg_damage_1 is None or avg_damage_2 is None:
        messagebox.showerror("Error", "Invalid average damage values.")
        return
    
    # create graph figure
    fig, axs = plt.subplots(1,3, figsize=(15,6))
    
    # 1. histogram for hits
    scenarios = ["Set 1: Avg Damage", "Set 2: Avg Damage"]
    avg_damage_values = [avg_damage_1, avg_damage_2]
    axs[0].bar(scenarios, avg_damage_values, color=['blue', 'red'])
    axs[0].set_title("Average Damage Comparison", fontsize=14)
    axs[0].set_ylabel("Average Damage", fontsize=12)
    axs[0].set_xlabel("Scenarios", fontsize=12)
    axs[0].legend()
    
    # 2. line plot
    cumulative_hits1 = np.cumsum(hits1)
    cumulative_hits2 = np.cumsum(hits2)
    axs[1].plot(cumulative_hits1, label='Set 1', color='blue')
    axs[1].plot(cumulative_hits2, label='Set 2', color='red')
    axs[1].set_title("Damage per Hit Simulation", fontsize=14)
    axs[1].set_xlabel("Hit Number", fontsize=12)
    axs[1].set_ylabel("Damage", fontsize=12)
    axs[1].legend()
    
    # 3. variance plot
    #axs[2].boxplot([variance1, variance2], label=["Set 1", "Set 2"], patch_artist=True)
    #axs[2].set_title("Variance in Damage Simulation", fontsize=14)
    #axs[2].set_ylabel("Avg Damage", fontsize=12)
    
    
    plt.tight_layout()
    plt.show() 

root = tk.Tk()
root.title("Stat Tracker")

entries = [
    ("Raw Damage (Set 1):", 0),
    ("Counterstrike Damage Buff (Set 1):", 1),
    ("Agitator Damage Buff (Set 1):", 2),
    ("Attack Boost Level (Set 1):", 3),
    ("Critical Level (Set 1):", 4),
    ("Critical Hit Chance (% Set 1):", 5),
    ("Offensive Guard Uptime (% Set 1):", 6),
]
entries_2 = [
    ("Raw Damage (Set 2):", 7),
    ("Counterstrike Damage Buff (Set 2):", 8),
    ("Agitator Damage Buff (Set 2):", 9),
    ("Attack Boost Level (Set 2):", 10),
    ("Critical Level (Set 2):", 11),
    ("Critical Hit Chance (% Set 2):", 12),
    ("Offensive Guard Uptime (% Set 2):", 13),
]

entry_vars = []
for text, row in entries:
    tk.Label(root, text=text).grid(row=row, column=0)
    entry = tk.Entry(root)
    entry.grid(row=row, column=1)
    entry_vars.append(entry)

for text, row in entries_2:
    tk.Label(root, text=text).grid(row=row, column=0)
    entry = tk.Entry(root)
    entry.grid(row=row, column=1)
    entry_vars.append(entry)

(raw_entry_1, cs_entry_1, agi_entry_1, attack_boost_entry_1, crit_level_entry_1, crit_chance_entry_1, og_uptime_entry_1,
 raw_entry_2, cs_entry_2, agi_entry_2, attack_boost_entry_2, crit_level_entry_2, crit_chance_entry_2, og_uptime_entry_2) = entry_vars

tk.Button(root, text="Calculate", command=calculate).grid(row=14, column=0, columnspan=4)
tk.Button(root, text="Simulate and Plot", command=simulate_and_plot).grid(row=15, column=0, columnspan=4)
tk.Button(root, text="Exit", command=root.quit).grid(row=16, column=0, columnspan=4)

result_label = tk.Label(root, text="")
result_label.grid(row=17, column=0, columnspan=4)

root.mainloop()
# This code creates a GUI application for tracking and simulating damage calculations in a game.