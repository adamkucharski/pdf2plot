# pip install plotnine pandas numpy
# SIR epidemic model — 3 series (Susceptible, Infectious, Recovered)
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_line, labs, theme_bw, scale_color_manual
from pathlib import Path

Path("output").mkdir(exist_ok=True)

N = 1000
beta, gamma = 0.4, 0.07
S, I, R = [990.0], [10.0], [0.0]
dt = 0.25

for _ in range(399):
    s, i, r = S[-1], I[-1], R[-1]
    S.append(s + dt * (-beta * s * i / N))
    I.append(i + dt * (beta * s * i / N - gamma * i))
    R.append(r + dt * (gamma * i))

t = np.arange(400) * dt
rows = (
    [{"t": ti, "series": "Susceptible",  "y": s} for ti, s in zip(t, S)] +
    [{"t": ti, "series": "Infectious",   "y": i} for ti, i in zip(t, I)] +
    [{"t": ti, "series": "Recovered",    "y": r} for ti, r in zip(t, R)]
)
df = pd.DataFrame(rows)
df.to_csv("output/plot_03_plotnine.csv", index=False)

colors = {"Susceptible": "#1f77b4", "Infectious": "#d62728", "Recovered": "#2ca02c"}
p = (
    ggplot(df, aes("t", "y", color="series"))
    + geom_line(size=0.9)
    + scale_color_manual(values=colors)
    + labs(x="Time (days)", y="Population", title="SIR epidemic model (plotnine)", color="")
    + theme_bw()
)
p.save("output/plot_03_plotnine.pdf", width=7, height=5)
print("Saved output/plot_03_plotnine.{pdf,csv}")
