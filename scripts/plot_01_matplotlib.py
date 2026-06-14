# pip install matplotlib numpy pandas
# Sigmoid growth curves — 3 series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("output").mkdir(exist_ok=True)
rng = np.random.default_rng(1)

x = np.linspace(0, 10, 60)
params = [
    ("Fast",   2.0, 3.0, "#1f77b4"),
    ("Medium", 1.0, 5.0, "#d62728"),
    ("Slow",   0.5, 7.0, "#2ca02c"),
]

rows = []
fig, ax = plt.subplots(figsize=(7, 5))
for name, k, x0, col in params:
    y = 1 / (1 + np.exp(-k * (x - x0))) + rng.normal(0, 0.02, len(x))
    ax.plot(x, y, label=name, color=col, linewidth=1.8)
    rows += [{"x": xi, "series": name, "y": yi} for xi, yi in zip(x, y)]

pd.DataFrame(rows).to_csv("output/plot_01_matplotlib.csv", index=False)

ax.set_xlabel("x")
ax.set_ylabel("Proportion")
ax.set_title("Sigmoid growth (matplotlib)")
ax.legend()
plt.tight_layout()
plt.savefig("output/plot_01_matplotlib.pdf")
plt.close()
print("Saved output/plot_01_matplotlib.{pdf,csv}")
