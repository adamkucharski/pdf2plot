# pip install pandas matplotlib numpy
# Random walks — 5 series
import numpy as np
import pandas as pd
from pathlib import Path

Path("output").mkdir(exist_ok=True)
rng = np.random.default_rng(4)

n = 200
steps = rng.normal(0, 1, (n, 5))
walks = pd.DataFrame(
    np.cumsum(steps, axis=0),
    columns=[f"Walk {i+1}" for i in range(5)],
)
walks.index.name = "step"

long = walks.reset_index().melt(id_vars="step", var_name="series", value_name="y")
long.rename(columns={"step": "x"}).to_csv("output/plot_04_pandas.csv", index=False)

ax = walks.plot(figsize=(7, 5), linewidth=1.4)
ax.set_xlabel("Step")
ax.set_ylabel("Value")
ax.set_title("Random walks (pandas)")
ax.legend(loc="upper left")
fig = ax.get_figure()
fig.tight_layout()
fig.savefig("output/plot_04_pandas.pdf")
import matplotlib.pyplot as plt
plt.close()
print("Saved output/plot_04_pandas.{pdf,csv}")
