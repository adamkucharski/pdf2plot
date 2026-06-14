# pip install plotly kaleido pandas numpy
# Lotka-Volterra predator-prey cycles — 2 series
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

Path("output").mkdir(exist_ok=True)

alpha, beta_lv, delta, gamma_lv = 1.0, 0.1, 0.075, 1.5
prey, pred = [10.0], [5.0]
dt = 0.01

for _ in range(4999):
    x, y = prey[-1], pred[-1]
    prey.append(x + dt * (alpha * x - beta_lv * x * y))
    pred.append(y + dt * (delta * x * y - gamma_lv * y))

t = np.arange(5000) * dt
idx = np.arange(0, 5000, 10)
t, prey, pred = t[idx], np.array(prey)[idx], np.array(pred)[idx]

rows = (
    [{"t": ti, "series": "Prey",     "y": v} for ti, v in zip(t, prey)] +
    [{"t": ti, "series": "Predator", "y": v} for ti, v in zip(t, pred)]
)
pd.DataFrame(rows).to_csv("output/plot_05_plotly.csv", index=False)

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=prey, mode="lines", name="Prey",     line=dict(color="#1f77b4", width=2)))
fig.add_trace(go.Scatter(x=t, y=pred, mode="lines", name="Predator", line=dict(color="#d62728", width=2)))
fig.update_layout(
    title="Lotka-Volterra predator-prey (plotly)",
    xaxis_title="Time",
    yaxis_title="Population",
    template="simple_white",
    width=700, height=500,
)
fig.write_image("output/plot_05_plotly.pdf")
print("Saved output/plot_05_plotly.{pdf,csv}")
