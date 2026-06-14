# pip install seaborn matplotlib numpy pandas
# Damped oscillations — 4 series with different damping coefficients
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

Path("output").mkdir(exist_ok=True)
rng = np.random.default_rng(2)

t = np.linspace(0, 10, 120)
omega = 2 * np.pi * 0.8
params = [
    ("gamma=0.1", 0.1),
    ("gamma=0.3", 0.3),
    ("gamma=0.6", 0.6),
    ("gamma=1.0", 1.0),
]

rows = []
for name, gamma in params:
    y = np.exp(-gamma * t) * np.cos(omega * t) + rng.normal(0, 0.03, len(t))
    rows += [{"t": ti, "series": name, "y": yi} for ti, yi in zip(t, y)]

df = pd.DataFrame(rows)
df.to_csv("output/plot_02_seaborn.csv", index=False)

fig, ax = plt.subplots(figsize=(7, 5))
sns.lineplot(data=df, x="t", y="y", hue="series", ax=ax, linewidth=1.6)
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.set_title("Damped oscillations (seaborn)")
ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
plt.tight_layout()
plt.savefig("output/plot_02_seaborn.pdf")
plt.close()
print("Saved output/plot_02_seaborn.{pdf,csv}")
