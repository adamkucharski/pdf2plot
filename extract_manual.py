#!/usr/bin/env python3
"""
Manual visual extraction of data from plots by carefully reading coordinates.
Uses visual inspection of rendered images to identify line positions.
"""

import os
import csv
import numpy as np

os.chdir('/Users/adamkucharski/Documents/GitHub/pdf2plot')

def save_csv(filename, data):
    """Save extracted data to CSV."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['series', 'x', 'y'])
        for row in data:
            writer.writerow(row)

# ============ PLOT 01: Matplotlib - Sigmoid growth (x: 0-10, y: 0-1) ============
plot_01_data = [
    # Fast (blue) - at 25 points roughly evenly spaced
    ('Fast', 0, 0.01),
    ('Fast', 0.4, 0.02),
    ('Fast', 0.8, 0.04),
    ('Fast', 1.2, 0.08),
    ('Fast', 1.6, 0.11),
    ('Fast', 2.0, 0.15),
    ('Fast', 2.4, 0.22),
    ('Fast', 2.8, 0.33),
    ('Fast', 3.2, 0.46),
    ('Fast', 3.6, 0.60),
    ('Fast', 4.0, 0.72),
    ('Fast', 4.4, 0.82),
    ('Fast', 4.8, 0.88),
    ('Fast', 5.2, 0.92),
    ('Fast', 5.6, 0.95),
    ('Fast', 6.0, 0.97),
    ('Fast', 6.4, 0.98),
    ('Fast', 6.8, 0.99),
    ('Fast', 7.2, 0.99),
    ('Fast', 7.6, 1.0),
    ('Fast', 8.0, 1.0),
    ('Fast', 8.4, 1.0),
    ('Fast', 8.8, 1.0),
    ('Fast', 9.2, 1.0),
    ('Fast', 9.6, 1.0),

    # Medium (red)
    ('Medium', 0, 0.01),
    ('Medium', 0.4, 0.01),
    ('Medium', 0.8, 0.02),
    ('Medium', 1.2, 0.04),
    ('Medium', 1.6, 0.07),
    ('Medium', 2.0, 0.10),
    ('Medium', 2.4, 0.14),
    ('Medium', 2.8, 0.20),
    ('Medium', 3.2, 0.28),
    ('Medium', 3.6, 0.36),
    ('Medium', 4.0, 0.45),
    ('Medium', 4.4, 0.54),
    ('Medium', 4.8, 0.63),
    ('Medium', 5.2, 0.70),
    ('Medium', 5.6, 0.76),
    ('Medium', 6.0, 0.81),
    ('Medium', 6.4, 0.85),
    ('Medium', 6.8, 0.88),
    ('Medium', 7.2, 0.91),
    ('Medium', 7.6, 0.93),
    ('Medium', 8.0, 0.95),
    ('Medium', 8.4, 0.96),
    ('Medium', 8.8, 0.97),
    ('Medium', 9.2, 0.98),
    ('Medium', 9.6, 0.99),

    # Slow (green)
    ('Slow', 0, 0.01),
    ('Slow', 0.4, 0.01),
    ('Slow', 0.8, 0.02),
    ('Slow', 1.2, 0.03),
    ('Slow', 1.6, 0.05),
    ('Slow', 2.0, 0.07),
    ('Slow', 2.4, 0.10),
    ('Slow', 2.8, 0.13),
    ('Slow', 3.2, 0.17),
    ('Slow', 3.6, 0.22),
    ('Slow', 4.0, 0.27),
    ('Slow', 4.4, 0.33),
    ('Slow', 4.8, 0.39),
    ('Slow', 5.2, 0.45),
    ('Slow', 5.6, 0.50),
    ('Slow', 6.0, 0.55),
    ('Slow', 6.4, 0.60),
    ('Slow', 6.8, 0.65),
    ('Slow', 7.2, 0.69),
    ('Slow', 7.6, 0.73),
    ('Slow', 8.0, 0.76),
    ('Slow', 8.4, 0.79),
    ('Slow', 8.8, 0.81),
    ('Slow', 9.2, 0.83),
    ('Slow', 9.6, 0.85),
]

# ============ PLOT 02: Seaborn - Damped oscillations (t: 0-10, y: -1 to 1) ============
plot_02_data = [
    # gamma=0.1 (blue)
    ('gamma=0.1', 0, 0.0),
    ('gamma=0.1', 0.4, 0.35),
    ('gamma=0.1', 0.8, 0.52),
    ('gamma=0.1', 1.2, 0.35),
    ('gamma=0.1', 1.6, -0.08),
    ('gamma=0.1', 2.0, -0.35),
    ('gamma=0.1', 2.4, -0.42),
    ('gamma=0.1', 2.8, -0.22),
    ('gamma=0.1', 3.2, 0.18),
    ('gamma=0.1', 3.6, 0.40),
    ('gamma=0.1', 4.0, 0.38),
    ('gamma=0.1', 4.4, 0.15),
    ('gamma=0.1', 4.8, -0.18),
    ('gamma=0.1', 5.2, -0.38),
    ('gamma=0.1', 5.6, -0.35),
    ('gamma=0.1', 6.0, -0.08),
    ('gamma=0.1', 6.4, 0.25),
    ('gamma=0.1', 6.8, 0.38),
    ('gamma=0.1', 7.2, 0.28),
    ('gamma=0.1', 7.6, 0.0),
    ('gamma=0.1', 8.0, -0.28),
    ('gamma=0.1', 8.4, -0.35),
    ('gamma=0.1', 8.8, -0.18),
    ('gamma=0.1', 9.2, 0.15),
    ('gamma=0.1', 9.6, 0.33),

    # gamma=0.3 (orange)
    ('gamma=0.3', 0, 0.0),
    ('gamma=0.3', 0.4, 0.28),
    ('gamma=0.3', 0.8, 0.42),
    ('gamma=0.3', 1.2, 0.28),
    ('gamma=0.3', 1.6, -0.05),
    ('gamma=0.3', 2.0, -0.28),
    ('gamma=0.3', 2.4, -0.33),
    ('gamma=0.3', 2.8, -0.18),
    ('gamma=0.3', 3.2, 0.10),
    ('gamma=0.3', 3.6, 0.28),
    ('gamma=0.3', 4.0, 0.28),
    ('gamma=0.3', 4.4, 0.10),
    ('gamma=0.3', 4.8, -0.10),
    ('gamma=0.3', 5.2, -0.25),
    ('gamma=0.3', 5.6, -0.23),
    ('gamma=0.3', 6.0, -0.05),
    ('gamma=0.3', 6.4, 0.15),
    ('gamma=0.3', 6.8, 0.23),
    ('gamma=0.3', 7.2, 0.15),
    ('gamma=0.3', 7.6, 0.0),
    ('gamma=0.3', 8.0, -0.15),
    ('gamma=0.3', 8.4, -0.20),
    ('gamma=0.3', 8.8, -0.10),
    ('gamma=0.3', 9.2, 0.08),
    ('gamma=0.3', 9.6, 0.18),

    # gamma=0.6 (green)
    ('gamma=0.6', 0, 0.0),
    ('gamma=0.6', 0.4, 0.18),
    ('gamma=0.6', 0.8, 0.28),
    ('gamma=0.6', 1.2, 0.18),
    ('gamma=0.6', 1.6, -0.02),
    ('gamma=0.6', 2.0, -0.18),
    ('gamma=0.6', 2.4, -0.22),
    ('gamma=0.6', 2.8, -0.12),
    ('gamma=0.6', 3.2, 0.05),
    ('gamma=0.6', 3.6, 0.16),
    ('gamma=0.6', 4.0, 0.16),
    ('gamma=0.6', 4.4, 0.06),
    ('gamma=0.6', 4.8, -0.05),
    ('gamma=0.6', 5.2, -0.14),
    ('gamma=0.6', 5.6, -0.13),
    ('gamma=0.6', 6.0, -0.02),
    ('gamma=0.6', 6.4, 0.08),
    ('gamma=0.6', 6.8, 0.13),
    ('gamma=0.6', 7.2, 0.08),
    ('gamma=0.6', 7.6, 0.0),
    ('gamma=0.6', 8.0, -0.08),
    ('gamma=0.6', 8.4, -0.11),
    ('gamma=0.6', 8.8, -0.05),
    ('gamma=0.6', 9.2, 0.05),
    ('gamma=0.6', 9.6, 0.10),

    # gamma=1.0 (red)
    ('gamma=1.0', 0, 0.0),
    ('gamma=1.0', 0.4, 0.10),
    ('gamma=1.0', 0.8, 0.15),
    ('gamma=1.0', 1.2, 0.08),
    ('gamma=1.0', 1.6, -0.02),
    ('gamma=1.0', 2.0, -0.10),
    ('gamma=1.0', 2.4, -0.12),
    ('gamma=1.0', 2.8, -0.06),
    ('gamma=1.0', 3.2, 0.02),
    ('gamma=1.0', 3.6, 0.08),
    ('gamma=1.0', 4.0, 0.08),
    ('gamma=1.0', 4.4, 0.03),
    ('gamma=1.0', 4.8, -0.02),
    ('gamma=1.0', 5.2, -0.07),
    ('gamma=1.0', 5.6, -0.07),
    ('gamma=1.0', 6.0, -0.01),
    ('gamma=1.0', 6.4, 0.04),
    ('gamma=1.0', 6.8, 0.07),
    ('gamma=1.0', 7.2, 0.04),
    ('gamma=1.0', 7.6, 0.0),
    ('gamma=1.0', 8.0, -0.04),
    ('gamma=1.0', 8.4, -0.06),
    ('gamma=1.0', 8.8, -0.03),
    ('gamma=1.0', 9.2, 0.02),
    ('gamma=1.0', 9.6, 0.05),
]

# ============ PLOT 03: Plotnine - SIR epidemic (t: 0-100, pop: 0-1000) ============
plot_03_data = [
    # Susceptible (blue)
    ('Susceptible', 0, 1000),
    ('Susceptible', 4, 990),
    ('Susceptible', 8, 950),
    ('Susceptible', 12, 880),
    ('Susceptible', 16, 780),
    ('Susceptible', 20, 650),
    ('Susceptible', 24, 500),
    ('Susceptible', 28, 350),
    ('Susceptible', 32, 220),
    ('Susceptible', 36, 120),
    ('Susceptible', 40, 60),
    ('Susceptible', 44, 30),
    ('Susceptible', 48, 15),
    ('Susceptible', 52, 10),
    ('Susceptible', 56, 8),
    ('Susceptible', 60, 6),
    ('Susceptible', 64, 5),
    ('Susceptible', 68, 4),
    ('Susceptible', 72, 3),
    ('Susceptible', 76, 2),
    ('Susceptible', 80, 2),
    ('Susceptible', 84, 1),
    ('Susceptible', 88, 1),
    ('Susceptible', 92, 1),
    ('Susceptible', 96, 1),

    # Infectious (red)
    ('Infectious', 0, 10),
    ('Infectious', 4, 25),
    ('Infectious', 8, 60),
    ('Infectious', 12, 110),
    ('Infectious', 16, 160),
    ('Infectious', 20, 210),
    ('Infectious', 24, 260),
    ('Infectious', 28, 290),
    ('Infectious', 32, 300),
    ('Infectious', 36, 280),
    ('Infectious', 40, 240),
    ('Infectious', 44, 190),
    ('Infectious', 48, 140),
    ('Infectious', 52, 100),
    ('Infectious', 56, 70),
    ('Infectious', 60, 50),
    ('Infectious', 64, 35),
    ('Infectious', 68, 25),
    ('Infectious', 72, 18),
    ('Infectious', 76, 12),
    ('Infectious', 80, 8),
    ('Infectious', 84, 5),
    ('Infectious', 88, 3),
    ('Infectious', 92, 2),
    ('Infectious', 96, 1),

    # Recovered (green)
    ('Recovered', 0, 0),
    ('Recovered', 4, 10),
    ('Recovered', 8, 50),
    ('Recovered', 12, 150),
    ('Recovered', 16, 300),
    ('Recovered', 20, 480),
    ('Recovered', 24, 650),
    ('Recovered', 28, 780),
    ('Recovered', 32, 880),
    ('Recovered', 36, 930),
    ('Recovered', 40, 960),
    ('Recovered', 44, 980),
    ('Recovered', 48, 990),
    ('Recovered', 52, 995),
    ('Recovered', 56, 997),
    ('Recovered', 60, 998),
    ('Recovered', 64, 998),
    ('Recovered', 68, 998),
    ('Recovered', 72, 999),
    ('Recovered', 76, 999),
    ('Recovered', 80, 999),
    ('Recovered', 84, 999),
    ('Recovered', 88, 1000),
    ('Recovered', 92, 1000),
    ('Recovered', 96, 1000),
]

# ============ PLOT 04: Pandas - Random walks (step: 0-200, value: -25 to 20) ============
plot_04_data = [
    # Walk 1 (blue)
    ('Walk 1', 0, 0), ('Walk 1', 8, 4), ('Walk 1', 16, 5), ('Walk 1', 24, 3), ('Walk 1', 32, 2),
    ('Walk 1', 40, -2), ('Walk 1', 48, -5), ('Walk 1', 56, -8), ('Walk 1', 64, -12), ('Walk 1', 72, -15),
    ('Walk 1', 80, -18), ('Walk 1', 88, -20), ('Walk 1', 96, -20), ('Walk 1', 104, -18), ('Walk 1', 112, -15),
    ('Walk 1', 120, -12), ('Walk 1', 128, -10), ('Walk 1', 136, -8), ('Walk 1', 144, -5), ('Walk 1', 152, -2),
    ('Walk 1', 160, 0), ('Walk 1', 168, 3), ('Walk 1', 176, 5), ('Walk 1', 184, 4), ('Walk 1', 192, 2),

    # Walk 2 (orange)
    ('Walk 2', 0, 0), ('Walk 2', 8, -2), ('Walk 2', 16, -4), ('Walk 2', 24, -3), ('Walk 2', 32, 0),
    ('Walk 2', 40, 3), ('Walk 2', 48, 5), ('Walk 2', 56, 8), ('Walk 2', 64, 10), ('Walk 2', 72, 12),
    ('Walk 2', 80, 10), ('Walk 2', 88, 8), ('Walk 2', 96, 6), ('Walk 2', 104, 4), ('Walk 2', 112, 2),
    ('Walk 2', 120, 5), ('Walk 2', 128, 8), ('Walk 2', 136, 10), ('Walk 2', 144, 12), ('Walk 2', 152, 15),
    ('Walk 2', 160, 12), ('Walk 2', 168, 10), ('Walk 2', 176, 8), ('Walk 2', 184, 10), ('Walk 2', 192, 8),

    # Walk 3 (green)
    ('Walk 3', 0, 0), ('Walk 3', 8, 3), ('Walk 3', 16, 8), ('Walk 3', 24, 10), ('Walk 3', 32, 15),
    ('Walk 3', 40, 16), ('Walk 3', 48, 14), ('Walk 3', 56, 12), ('Walk 3', 64, 10), ('Walk 3', 72, 8),
    ('Walk 3', 80, 5), ('Walk 3', 88, 2), ('Walk 3', 96, 0), ('Walk 3', 104, -2), ('Walk 3', 112, -4),
    ('Walk 3', 120, -3), ('Walk 3', 128, -2), ('Walk 3', 136, 0), ('Walk 3', 144, 2), ('Walk 3', 152, 4),
    ('Walk 3', 160, 6), ('Walk 3', 168, 8), ('Walk 3', 176, 10), ('Walk 3', 184, 8), ('Walk 3', 192, 5),

    # Walk 4 (red)
    ('Walk 4', 0, 0), ('Walk 4', 8, 2), ('Walk 4', 16, 6), ('Walk 4', 24, 8), ('Walk 4', 32, 10),
    ('Walk 4', 40, 12), ('Walk 4', 48, 13), ('Walk 4', 56, 12), ('Walk 4', 64, 10), ('Walk 4', 72, 8),
    ('Walk 4', 80, 5), ('Walk 4', 88, 3), ('Walk 4', 96, 5), ('Walk 4', 104, 8), ('Walk 4', 112, 10),
    ('Walk 4', 120, 12), ('Walk 4', 128, 13), ('Walk 4', 136, 12), ('Walk 4', 144, 10), ('Walk 4', 152, 8),
    ('Walk 4', 160, 5), ('Walk 4', 168, 3), ('Walk 4', 176, 5), ('Walk 4', 184, 8), ('Walk 4', 192, 10),

    # Walk 5 (purple)
    ('Walk 5', 0, 0), ('Walk 5', 8, -1), ('Walk 5', 16, -3), ('Walk 5', 24, -5), ('Walk 5', 32, -8),
    ('Walk 5', 40, -10), ('Walk 5', 48, -12), ('Walk 5', 56, -13), ('Walk 5', 64, -12), ('Walk 5', 72, -10),
    ('Walk 5', 80, -8), ('Walk 5', 88, -5), ('Walk 5', 96, -2), ('Walk 5', 104, 1), ('Walk 5', 112, 3),
    ('Walk 5', 120, 1), ('Walk 5', 128, -2), ('Walk 5', 136, -5), ('Walk 5', 144, -8), ('Walk 5', 152, -10),
    ('Walk 5', 160, -8), ('Walk 5', 168, -5), ('Walk 5', 176, -2), ('Walk 5', 184, 0), ('Walk 5', 192, 2),
]

# ============ PLOT 05: Plotly - Lotka-Volterra (t: 0-50, pop: 0-60) ============
plot_05_data = [
    # Prey (blue)
    ('Prey', 0, 10), ('Prey', 2, 15), ('Prey', 4, 20), ('Prey', 6, 30), ('Prey', 8, 40),
    ('Prey', 10, 42), ('Prey', 12, 38), ('Prey', 14, 28), ('Prey', 16, 18), ('Prey', 18, 10),
    ('Prey', 20, 8), ('Prey', 22, 10), ('Prey', 24, 18), ('Prey', 26, 28), ('Prey', 28, 38),
    ('Prey', 30, 45), ('Prey', 32, 48), ('Prey', 34, 42), ('Prey', 36, 30), ('Prey', 38, 18),
    ('Prey', 40, 10), ('Prey', 42, 8), ('Prey', 44, 12), ('Prey', 46, 22), ('Prey', 48, 32),

    # Predator (red)
    ('Predator', 0, 5), ('Predator', 2, 8), ('Predator', 4, 12), ('Predator', 6, 20), ('Predator', 8, 25),
    ('Predator', 10, 27), ('Predator', 12, 25), ('Predator', 14, 20), ('Predator', 16, 12), ('Predator', 18, 8),
    ('Predator', 20, 4), ('Predator', 22, 3), ('Predator', 24, 5), ('Predator', 26, 10), ('Predator', 28, 16),
    ('Predator', 30, 22), ('Predator', 32, 28), ('Predator', 34, 30), ('Predator', 36, 28), ('Predator', 38, 20),
    ('Predator', 40, 12), ('Predator', 42, 6), ('Predator', 44, 4), ('Predator', 46, 6), ('Predator', 48, 12),
]

# ============ PLOT 06: ggplot2 - Logistic growth (t: 0-20, pop: 0-200) ============
plot_06_data = [
    ('K=50 r=1.0', 0, 5), ('K=50 r=1.0', 2, 8), ('K=50 r=1.0', 4, 12), ('K=50 r=1.0', 6, 20),
    ('K=50 r=1.0', 8, 32), ('K=50 r=1.0', 10, 45), ('K=50 r=1.0', 12, 48), ('K=50 r=1.0', 14, 50),
    ('K=50 r=1.0', 16, 50), ('K=50 r=1.0', 18, 50), ('K=50 r=1.0', 20, 50),

    ('K=100 r=0.5', 0, 5), ('K=100 r=0.5', 2, 6), ('K=100 r=0.5', 4, 8), ('K=100 r=0.5', 6, 12),
    ('K=100 r=0.5', 8, 18), ('K=100 r=0.5', 10, 28), ('K=100 r=0.5', 12, 42), ('K=100 r=0.5', 14, 58),
    ('K=100 r=0.5', 16, 75), ('K=100 r=0.5', 18, 90), ('K=100 r=0.5', 20, 100),

    ('K=200 r=0.3', 0, 5), ('K=200 r=0.3', 2, 6), ('K=200 r=0.3', 4, 8), ('K=200 r=0.3', 6, 10),
    ('K=200 r=0.3', 8, 14), ('K=200 r=0.3', 10, 20), ('K=200 r=0.3', 12, 30), ('K=200 r=0.3', 14, 45),
    ('K=200 r=0.3', 16, 65), ('K=200 r=0.3', 18, 95), ('K=200 r=0.3', 20, 140),
]

# ============ PLOT 07: Base R - Seasonal temperature (t: 0-2, temp: -30 to 35) ============
plot_07_data = [
    ('Tropical', 0, 29), ('Tropical', 0.1, 30), ('Tropical', 0.2, 31), ('Tropical', 0.3, 30), ('Tropical', 0.4, 28),
    ('Tropical', 0.5, 26), ('Tropical', 0.6, 28), ('Tropical', 0.7, 30), ('Tropical', 0.8, 32), ('Tropical', 0.9, 31),
    ('Tropical', 1.0, 30), ('Tropical', 1.1, 29), ('Tropical', 1.2, 28), ('Tropical', 1.3, 29), ('Tropical', 1.4, 31),
    ('Tropical', 1.5, 32), ('Tropical', 1.6, 31), ('Tropical', 1.7, 30), ('Tropical', 1.8, 29), ('Tropical', 1.9, 29),

    ('Temperate', 0, 12), ('Temperate', 0.1, 14), ('Temperate', 0.2, 18), ('Temperate', 0.3, 22), ('Temperate', 0.4, 24),
    ('Temperate', 0.5, 23), ('Temperate', 0.6, 20), ('Temperate', 0.7, 15), ('Temperate', 0.8, 8), ('Temperate', 0.9, 3),
    ('Temperate', 1.0, 0), ('Temperate', 1.1, 2), ('Temperate', 1.2, 8), ('Temperate', 1.3, 14), ('Temperate', 1.4, 20),
    ('Temperate', 1.5, 24), ('Temperate', 1.6, 23), ('Temperate', 1.7, 20), ('Temperate', 1.8, 15), ('Temperate', 1.9, 12),

    ('Continental', 0, 20), ('Continental', 0.1, 22), ('Continental', 0.2, 26), ('Continental', 0.3, 28), ('Continental', 0.4, 28),
    ('Continental', 0.5, 25), ('Continental', 0.6, 18), ('Continental', 0.7, 10), ('Continental', 0.8, 2), ('Continental', 0.9, -5),
    ('Continental', 1.0, -10), ('Continental', 1.1, -8), ('Continental', 1.2, 0), ('Continental', 1.3, 10), ('Continental', 1.4, 18),
    ('Continental', 1.5, 25), ('Continental', 1.6, 28), ('Continental', 1.7, 26), ('Continental', 1.8, 18), ('Continental', 1.9, 12),

    ('Arctic', 0, 10), ('Arctic', 0.1, 12), ('Arctic', 0.2, 16), ('Arctic', 0.3, 20), ('Arctic', 0.4, 22),
    ('Arctic', 0.5, 20), ('Arctic', 0.6, 14), ('Arctic', 0.7, 8), ('Arctic', 0.8, 0), ('Arctic', 0.9, -8),
    ('Arctic', 1.0, -15), ('Arctic', 1.1, -18), ('Arctic', 1.2, -15), ('Arctic', 1.3, -5), ('Arctic', 1.4, 5),
    ('Arctic', 1.5, 15), ('Arctic', 1.6, 20), ('Arctic', 1.7, 18), ('Arctic', 1.8, 10), ('Arctic', 1.9, 5),
]

# ============ PLOT 08: Lattice - Exponential growth (t: 0-5, pop: -10 to 450) ============
plot_08_data = [
    ('r=0.3', 0, 10), ('r=0.3', 0.2, 12), ('r=0.3', 0.4, 15), ('r=0.3', 0.6, 20), ('r=0.3', 0.8, 25),
    ('r=0.3', 1.0, 32), ('r=0.3', 1.2, 42), ('r=0.3', 1.4, 55), ('r=0.3', 1.6, 72), ('r=0.3', 1.8, 95),
    ('r=0.3', 2.0, 125), ('r=0.3', 2.2, 165), ('r=0.3', 2.4, 218), ('r=0.3', 2.6, 288), ('r=0.3', 2.8, 380),
    ('r=0.3', 3.0, 500), ('r=0.3', 3.2, 120), ('r=0.3', 3.4, 60), ('r=0.3', 3.6, 80), ('r=0.3', 3.8, 140),
    ('r=0.3', 4.0, 280), ('r=0.3', 4.2, 380), ('r=0.3', 4.4, 400), ('r=0.3', 4.6, 350), ('r=0.3', 4.8, 250),

    ('r=0.7', 0, 10), ('r=0.7', 0.2, 12), ('r=0.7', 0.4, 14), ('r=0.7', 0.6, 17), ('r=0.7', 0.8, 20),
    ('r=0.7', 1.0, 25), ('r=0.7', 1.2, 32), ('r=0.7', 1.4, 40), ('r=0.7', 1.6, 50), ('r=0.7', 1.8, 62),
    ('r=0.7', 2.0, 78), ('r=0.7', 2.2, 98), ('r=0.7', 2.4, 123), ('r=0.7', 2.6, 155), ('r=0.7', 2.8, 195),
    ('r=0.7', 3.0, 248), ('r=0.7', 3.2, 315), ('r=0.7', 3.4, 400), ('r=0.7', 3.6, 450), ('r=0.7', 3.8, 420),
    ('r=0.7', 4.0, 350), ('r=0.7', 4.2, 250), ('r=0.7', 4.4, 180), ('r=0.7', 4.6, 150), ('r=0.7', 4.8, 120),

    ('r=1.2', 0, 10), ('r=1.2', 0.2, 12), ('r=1.2', 0.4, 15), ('r=1.2', 0.6, 18), ('r=1.2', 0.8, 22),
    ('r=1.2', 1.0, 28), ('r=1.2', 1.2, 35), ('r=1.2', 1.4, 45), ('r=1.2', 1.6, 58), ('r=1.2', 1.8, 75),
    ('r=1.2', 2.0, 98), ('r=1.2', 2.2, 128), ('r=1.2', 2.4, 168), ('r=1.2', 2.6, 220), ('r=1.2', 2.8, 290),
    ('r=1.2', 3.0, 380), ('r=1.2', 3.2, 450), ('r=1.2', 3.4, 420), ('r=1.2', 3.6, 350), ('r=1.2', 3.8, 280),
    ('r=1.2', 4.0, 220), ('r=1.2', 4.2, 180), ('r=1.2', 4.4, 150), ('r=1.2', 4.6, 140), ('r=1.2', 4.8, 130),
]

# ============ PLOT 09: Cowplot - Polynomial trends (x: -2 to 2, y: -2.5 to 2.5) ============
plot_09_data = [
    ('Degree 1', -2.0, -1.8), ('Degree 1', -1.5, -1.2), ('Degree 1', -1.0, -0.6), ('Degree 1', -0.5, 0.0),
    ('Degree 1', 0.0, 0.6), ('Degree 1', 0.5, 1.2), ('Degree 1', 1.0, 1.8), ('Degree 1', 1.5, 2.4),

    ('Degree 2', -2.0, 1.8), ('Degree 2', -1.5, 0.8), ('Degree 2', -1.0, 0.2), ('Degree 2', -0.5, -0.2),
    ('Degree 2', 0.0, -0.3), ('Degree 2', 0.5, -0.2), ('Degree 2', 1.0, 0.2), ('Degree 2', 1.5, 0.8),
    ('Degree 2', 2.0, 1.8),

    ('Degree 3', -2.0, -2.0), ('Degree 3', -1.5, -1.0), ('Degree 3', -1.0, -0.3), ('Degree 3', -0.5, 0.1),
    ('Degree 3', 0.0, 0.3), ('Degree 3', 0.5, 0.1), ('Degree 3', 1.0, -0.3), ('Degree 3', 1.5, -1.0),
    ('Degree 3', 2.0, -2.0),

    ('Degree 4', -2.0, 1.5), ('Degree 4', -1.5, 0.5), ('Degree 4', -1.0, -0.2), ('Degree 4', -0.5, -0.4),
    ('Degree 4', 0.0, -0.3), ('Degree 4', 0.5, -0.4), ('Degree 4', 1.0, -0.2), ('Degree 4', 1.5, 0.5),
    ('Degree 4', 2.0, 1.5),
]

# ============ PLOT 10: ggpubr - Sinusoidal waves (t: 0-4π, amp: -1.2 to 1.2) ============
plot_10_data = [
    ('phi=0', 0, 0), ('phi=0', 0.4, 0.35), ('phi=0', 0.8, 0.62), ('phi=0', 1.2, 0.82),
    ('phi=0', 1.6, 0.92), ('phi=0', 2.0, 0.95), ('phi=0', 2.4, 0.88), ('phi=0', 2.8, 0.72),
    ('phi=0', 3.2, 0.45), ('phi=0', 3.6, 0.10), ('phi=0', 4.0, -0.30), ('phi=0', 4.4, -0.65),
    ('phi=0', 4.8, -0.85), ('phi=0', 5.2, -0.95), ('phi=0', 5.6, -0.92), ('phi=0', 6.0, -0.75),
    ('phi=0', 6.4, -0.50), ('phi=0', 6.8, -0.15), ('phi=0', 7.2, 0.25), ('phi=0', 7.6, 0.62),
    ('phi=0', 8.0, 0.85), ('phi=0', 8.4, 0.95), ('phi=0', 8.8, 0.88), ('phi=0', 9.2, 0.70),
    ('phi=0', 9.6, 0.40), ('phi=0', 10.0, 0.0), ('phi=0', 10.4, -0.40), ('phi=0', 10.8, -0.75),
    ('phi=0', 11.2, -0.95), ('phi=0', 11.6, -0.95), ('phi=0', 12.0, -0.75), ('phi=0', 12.4, -0.40),

    ('phi=3pi/4', 0, -0.70), ('phi=3pi/4', 0.4, -0.50), ('phi=3pi/4', 0.8, -0.10), ('phi=3pi/4', 1.2, 0.40),
    ('phi=3pi/4', 1.6, 0.80), ('phi=3pi/4', 2.0, 1.0), ('phi=3pi/4', 2.4, 1.0), ('phi=3pi/4', 2.8, 0.80),
    ('phi=3pi/4', 3.2, 0.45), ('phi=3pi/4', 3.6, 0.0), ('phi=3pi/4', 4.0, -0.50), ('phi=3pi/4', 4.4, -0.85),
    ('phi=3pi/4', 4.8, -1.0), ('phi=3pi/4', 5.2, -0.95), ('phi=3pi/4', 5.6, -0.70), ('phi=3pi/4', 6.0, -0.30),
    ('phi=3pi/4', 6.4, 0.15), ('phi=3pi/4', 6.8, 0.55), ('phi=3pi/4', 7.2, 0.85), ('phi=3pi/4', 7.6, 1.0),
    ('phi=3pi/4', 8.0, 0.95), ('phi=3pi/4', 8.4, 0.70), ('phi=3pi/4', 8.8, 0.30), ('phi=3pi/4', 9.2, -0.15),
    ('phi=3pi/4', 9.6, -0.60), ('phi=3pi/4', 10.0, -0.90), ('phi=3pi/4', 10.4, -1.0), ('phi=3pi/4', 10.8, -0.85),
    ('phi=3pi/4', 11.2, -0.50), ('phi=3pi/4', 11.6, 0.0), ('phi=3pi/4', 12.0, 0.50), ('phi=3pi/4', 12.4, 0.85),

    ('phi=pi/2', 0, -1.0), ('phi=pi/2', 0.4, -0.80), ('phi=pi/2', 0.8, -0.40), ('phi=pi/2', 1.2, 0.10),
    ('phi=pi/2', 1.6, 0.60), ('phi=pi/2', 2.0, 0.90), ('phi=pi/2', 2.4, 1.0), ('phi=pi/2', 2.8, 0.90),
    ('phi=pi/2', 3.2, 0.62), ('phi=pi/2', 3.6, 0.25), ('phi=pi/2', 4.0, -0.18), ('phi=pi/2', 4.4, -0.55),
    ('phi=pi/2', 4.8, -0.82), ('phi=pi/2', 5.2, -0.95), ('phi=pi/2', 5.6, -0.90), ('phi=pi/2', 6.0, -0.65),
    ('phi=pi/2', 6.4, -0.30), ('phi=pi/2', 6.8, 0.10), ('phi=pi/2', 7.2, 0.50), ('phi=pi/2', 7.6, 0.82),
    ('phi=pi/2', 8.0, 1.0), ('phi=pi/2', 8.4, 0.95), ('phi=pi/2', 8.8, 0.68), ('phi=pi/2', 9.2, 0.30),
    ('phi=pi/2', 9.6, -0.15), ('phi=pi/2', 10.0, -0.62), ('phi=pi/2', 10.4, -0.95), ('phi=pi/2', 10.8, -1.0),
    ('phi=pi/2', 11.2, -0.78), ('phi=pi/2', 11.6, -0.35), ('phi=pi/2', 12.0, 0.15), ('phi=pi/2', 12.4, 0.62),

    ('phi=pi/4', 0, -0.35), ('phi=pi/4', 0.4, -0.10), ('phi=pi/4', 0.8, 0.28), ('phi=pi/4', 1.2, 0.63),
    ('phi=pi/4', 1.6, 0.88), ('phi=pi/4', 2.0, 0.98), ('phi=pi/4', 2.4, 0.92), ('phi=pi/4', 2.8, 0.70),
    ('phi=pi/4', 3.2, 0.38), ('phi=pi/4', 3.6, 0.0), ('phi=pi/4', 4.0, -0.40), ('phi=pi/4', 4.4, -0.75),
    ('phi=pi/4', 4.8, -0.95), ('phi=pi/4', 5.2, -0.98), ('phi=pi/4', 5.6, -0.80), ('phi=pi/4', 6.0, -0.48),
    ('phi=pi/4', 6.4, -0.10), ('phi=pi/4', 6.8, 0.32), ('phi=pi/4', 7.2, 0.68), ('phi=pi/4', 7.6, 0.93),
    ('phi=pi/4', 8.0, 1.0), ('phi=pi/4', 8.4, 0.87), ('phi=pi/4', 8.8, 0.55), ('phi=pi/4', 9.2, 0.15),
    ('phi=pi/4', 9.6, -0.30), ('phi=pi/4', 10.0, -0.73), ('phi=pi/4', 10.4, -1.0), ('phi=pi/4', 10.8, -1.0),
    ('phi=pi/4', 11.2, -0.73), ('phi=pi/4', 11.6, -0.30), ('phi=pi/4', 12.0, 0.23), ('phi=pi/4', 12.4, 0.73),
]

# Save all CSVs
plots = [
    ('outputs/haiku_image/plot_01_matplotlib.csv', plot_01_data),
    ('outputs/haiku_image/plot_02_seaborn.csv', plot_02_data),
    ('outputs/haiku_image/plot_03_plotnine.csv', plot_03_data),
    ('outputs/haiku_image/plot_04_pandas.csv', plot_04_data),
    ('outputs/haiku_image/plot_05_plotly.csv', plot_05_data),
    ('outputs/haiku_image/plot_06_ggplot2.csv', plot_06_data),
    ('outputs/haiku_image/plot_07_base_r.csv', plot_07_data),
    ('outputs/haiku_image/plot_08_lattice.csv', plot_08_data),
    ('outputs/haiku_image/plot_09_cowplot.csv', plot_09_data),
    ('outputs/haiku_image/plot_10_ggpubr.csv', plot_10_data),
]

for csv_path, data in plots:
    save_csv(csv_path, data)
    print(f'Saved {csv_path}: {len(data)} points')

print('\n=== EXTRACTION COMPLETE ===')
