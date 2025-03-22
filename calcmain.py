import random
import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
from tkinter import Canvas
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image, ImageTk
import os

class Tracker:
    def __init__(self, raw):
        self.raw = raw

    def critical_value(self, level):
        critical_multipliers = {0: 1.25, 1: 1.28, 2: 1.31, 3: 1.34, 4: 1.37, 5: 1.40}
        base_damage = self.display_sum()
        return base_damage * critical_multipliers.get(level, 1.25)
    
    def apply_counterstrike(self, counterstrike_level):
        if counterstrike_level == 1:
            return 10
        elif counterstrike_level == 2:
            return 15
        elif counterstrike_level == 3:
            return 25
        else:
            return 0
    
    def apply_agitator(self, agitator_level):
        if agitator_level == 1:
            return 4
        elif agitator_level == 2:
            return 8
        elif agitator_level == 3:
            return 12
        elif agitator_level == 4:
            return 16
        elif agitator_level == 5:
            return 20
        else:
            return 0

    def apply_attack_boost(self, attack_boost_level):
        if attack_boost_level == 1:
            return self.raw + 3
        elif attack_boost_level == 2:
            return self.raw + 5
        elif attack_boost_level == 3:
            return self.raw + 7
        elif attack_boost_level == 4:
            return (self.raw * 1.02) + 8
        elif attack_boost_level == 5:
            return (self.raw * 1.04) + 9
        else:
            return self.raw
    
    def display_sum(self):
        return self.raw

    def simulate_hits(self, crit_chance, crit_level, og_uptime, attack_boost_level, counterstrike_level, agitator_level):
        counterstrike_buff = self.apply_counterstrike(counterstrike_level)
        agitator_buff = self.apply_agitator(agitator_level)
        total = self.apply_attack_boost(attack_boost_level) + counterstrike_buff + agitator_buff
        critical_total = self.critical_value(crit_level)

        hits = []
        
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
        # set 1
        raw_1 = int(raw_entry_1.get())
        counterstrike_level_1 = int(cs_entry_1.get())
        agitator_level_1 = int(agi_entry_1.get())
        crit_level_1 = int(crit_level_entry_1.get())
        attack_boost_level_1 = int(attack_boost_entry_1.get())
        crit_chance_1 = float(crit_chance_entry_1.get())
        og_uptime_1 = float(og_uptime_entry_1.get())
        
        #set 2
        raw_2 = int(raw_entry_2.get())
        counterstrike_level_2 = int(cs_entry_2.get())
        agitator_level_2 = int(agi_entry_2.get())
        attack_boost_level_2 = int(attack_boost_entry_2.get())
        crit_level_2 = int(crit_level_entry_2.get())
        crit_chance_2 = float(crit_chance_entry_2.get())
        og_uptime_2 = float(og_uptime_entry_2.get())

        tracker = Tracker(raw_1)
        tracker = Tracker(raw_2)
        
        # calculate damage for set 1
        counterstrike_buff_1 = tracker.apply_counterstrike(counterstrike_level_1)
        agitator_buff_1 = tracker.apply_agitator(agitator_level_1)
        total_damage_1 = tracker.apply_attack_boost(attack_boost_level_1) + counterstrike_buff_1 + agitator_buff_1
        avg_damage_1, _ = tracker.simulate_hits(crit_chance_1, crit_level_1, og_uptime_1, attack_boost_level_1, counterstrike_level_1, agitator_level_1)

        #calculate damage for set 2
        counterstrike_buff_2 = tracker.apply_counterstrike(counterstrike_level_2)
        agitator_buff_2 = tracker.apply_agitator(agitator_level_2)
        total_damage_2 = tracker.apply_attack_boost(attack_boost_level_2) + counterstrike_buff_2 + agitator_buff_2
        avg_damage_2, _ = tracker.simulate_hits(crit_chance_2, crit_level_2, og_uptime_2, attack_boost_level_2, counterstrike_level_2, agitator_level_2)

        # Display results
        result_label.config(text=f"Set 1 Damage Per Hit: {total_damage_1}\n"
                                f"Set 1 Avg. Dmg Per Hit (Sim. over 100 hits): {avg_damage_1}\n"
                                f"Set 2 Damage Per Hit: {total_damage_2}\n"
                                f"Set 2 Avg. Dmg Per Hit (Sim. over 100 hits): {avg_damage_2}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

def simulate_and_plot():
    try:
        raw_1 = int(raw_entry_1.get())
        counterstrike_level_1 = int(cs_entry_1.get())
        agitator_level_1 = int(agi_entry_1.get())
        attack_boost_level_1 = int(attack_boost_entry_1.get())
        crit_level_1 = int(crit_level_entry_1.get())
        crit_chance_1 = float(crit_chance_entry_1.get())
        og_uptime_1 = float(og_uptime_entry_1.get())

        raw_2 = int(raw_entry_2.get())
        counterstrike_level_2 = int(cs_entry_2.get())
        agitator_level_2 = int(agi_entry_2.get())
        attack_boost_level_2 = int(attack_boost_entry_2.get())
        crit_level_2 = int(crit_level_entry_2.get())
        crit_chance_2 = float(crit_chance_entry_2.get())
        og_uptime_2 = float(og_uptime_entry_2.get())

        tracker_1 = Tracker(raw_1)
        tracker_2 = Tracker(raw_2)

        avg_damage_1, hits1 = tracker_1.simulate_hits(crit_chance_1, crit_level_1, 
                                                      og_uptime_1, attack_boost_level_1, 
                                                      counterstrike_level_1, agitator_level_1)
        avg_damage_2, hits2 = tracker_2.simulate_hits(crit_chance_2, crit_level_2, 
                                                      og_uptime_2, attack_boost_level_2, 
                                                      counterstrike_level_2, agitator_level_2)
        
        #simulate variance
        variance1 = [tracker_1.simulate_hits(crit_chance_1, crit_level_1, og_uptime_1, attack_boost_level_1, 
                                             counterstrike_level_1, agitator_level_1)[0] for _ in range(100)]
        variance2 = [tracker_2.simulate_hits(crit_chance_2, crit_level_2, og_uptime_2, attack_boost_level_2, 
                                             counterstrike_level_2, agitator_level_2)[0] for _ in range(100)]

        plot_graphs(hits1, hits2, avg_damage_1, avg_damage_2, variance1, variance2)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

def plot_graphs(hits1, hits2, avg_damage_1, avg_damage_2, variance1, variance2):
    
    if avg_damage_1 is None or avg_damage_2 is None:
        messagebox.showerror("Error", "Invalid average damage values.")
        return
    
    # create graph figure
    fig, axs = plt.subplots(1,3, figsize=(15,6))
    
    
    # 1. histogram for hits
    scenarios = ["Set 1: Avg Damage", "Set 2: Avg Damage"]
    avg_damage_values = [avg_damage_1, avg_damage_2]
    # use seaborn to create a barplot
    barplot = sns.barplot(x=scenarios, y=avg_damage_values, ax=axs[0], 
                          hue=scenarios, palette="Blues_d", legend = False)
    axs[0].set_title("Average Damage Comparison", fontsize=14)
    axs[0].set_ylabel("Average Damage", fontsize=12)
    axs[0].set_xlabel("Scenarios", fontsize=12)
    
    # Annotating the bars inside the bars
    for p in barplot.patches:
        height = p.get_height()
        barplot.annotate(f'{height:.2f}', 
                          (p.get_x() + p.get_width() / 2., height), 
                          ha='center', va='center', fontsize=12, color='black', fontweight='bold')
    
    
    # Adding a box below the bar plot with the data used
    info_text_bar = f"Set 1 Avg Damage: {avg_damage_1:.2f}\nSet 2 Avg Damage: {avg_damage_2:.2f}"
    axs[0].text(0.5, -0.3, info_text_bar, transform=axs[0].transAxes, ha='center', va='top', fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))
    
    
    
    # 2. line plot for cumulative damage
    hits1 = np.array(hits1)
    hits2 = np.array(hits2)
    
    # Plot cumulative damage with line style and width adjustments
    sns.lineplot(x=np.arange(len(hits1)), y=np.cumsum(hits1), ax=axs[1], label='Set 1', 
                 color='blue', linewidth=2)
    sns.lineplot(x=np.arange(len(hits2)), y=np.cumsum(hits2), ax=axs[1], label='Set 2', 
                 color='red', linewidth=2)
    
    axs[1].set_title("Damage per Hit Simulation", fontsize=14)
    axs[1].set_xlabel("Hit Number", fontsize=12)
    axs[1].set_ylabel("Cumulative Damage", fontsize=14)
    axs[1].tick_params(axis='both', labelsize=12)
    axs[1].grid(True, axis='both', linestyle='--', alpha=0.7)
    
     # 3. Adding colored boxes below the line plot to represent final cumulative values
    total_cumulative_value_1 = np.cumsum(hits1)[-1]
    total_cumulative_value_2 = np.cumsum(hits2)[-1]
    
    axs[1].text(0.5, -0.3, f'Set 1: Final Total: {total_cumulative_value_1:.2f}', transform=axs[1].transAxes, ha='center', va='top', fontsize=12,
                bbox=dict(facecolor='blue', alpha=0.7, boxstyle='round,pad=0.5'))
    
    axs[1].text(0.5, -0.4, f'Set 2: Final Total: {total_cumulative_value_2:.2f}', transform=axs[1].transAxes, ha='center', va='top', fontsize=12,
                bbox=dict(facecolor='red', alpha=0.7, boxstyle='round,pad=0.5'))
    
    
    
    # 3. variance plot
    sns.boxplot(data=[variance1, variance2], ax=axs[2], palette="Set2")
    axs[2].set_title("Variance in Damage Simulation", fontsize=14)
    axs[2].set_ylabel("Damage Variance", fontsize=12)
    axs[2].set_xticks([0, 1])
    axs[2].set_xticklabels(["Set 1", "Set 2"], fontsize=12)
    axs[2].tick_params(axis='both', labelsize=12)
    axs[2].grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Annotating the outliers with numbers
    outlier_labels = {}
    for i, data in enumerate([variance1, variance2]):
        # Getting outliers
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = [x for x in data if x < lower_bound or x > upper_bound]
        
        # Assign numbers to outliers and annotate
        outlier_labels[i] = {}
        for idx, outlier in enumerate(outliers):
            outlier_labels[i][idx + 1] = outlier
            
            # Find appropriate space for annotation
            y_position = outlier
            # Shift the annotation slightly if there's already an annotation at that position
            shift = 0
            while any(abs(y_position - existing_pos) < 0.1 for existing_pos in outlier_labels[i].values()):
                shift += 0.1
                y_position = outlier + shift
            
            axs[2].text(i, y_position, f'{idx + 1}', color='black', fontsize=10, ha='center', va='bottom')
            outlier_labels[i][idx + 1] = y_position
    
    # Create information box below boxplot with the outlier values
    info_text_box = "Outlier values: \n"
    for i, outliers in outlier_labels.items():
        for label, value in outliers.items():
            info_text_box += f"Set {i+1}: Outlier {label} = {value:.2f}\n"
    
    axs[2].text(0.5, -0.3, info_text_box, transform=axs[2].transAxes, ha='center', va='top', fontsize=12, 
                color='black', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))
    
    if os.path.exists("damage_simulation.png"):
        os.remove("damage_simulation.png")
    # Save the figure
    plt.tight_layout()
    plt.savefig("damage_simulation.png")
    open_image_in_new_window()
    #plt.show() 
    
def open_image_in_new_window():
    img = Image.open("damage_simulation.png")
    img_tk = ImageTk.PhotoImage(img)
    
    # Create a new window to display the image
    new_window = Toplevel()
    new_window.title("Damage Simulation Results")
    
    canvas = Canvas(new_window, width=img.width, height=img.height)
    canvas.pack()
    
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  # Keep a reference to avoid garbage collection
    new_window.mainloop()

root = tk.Tk()
root.title("Stat Tracker")

entries = [
    ("Raw Damage (Set 1):", 0),
    ("Counterstrike Level (Set 1):", 1),
    ("Agitator Level (Set 1):", 2),
    ("Attack Boost Level (Set 1):", 3),
    ("Critical Level (Set 1):", 4),
    ("Critical Hit Chance (% Set 1):", 5),
    ("Offensive Guard Uptime (% Set 1):", 6),
]
entries_2 = [
    ("Raw Damage (Set 2):", 7),
    ("Counterstrike Level (Set 2):", 8),
    ("Agitator Level (Set 2):", 9),
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