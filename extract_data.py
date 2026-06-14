#!/usr/bin/env python3
"""
Visually extract data from PDF line plots by analyzing rendered PNG images.
This script reads pixel positions of line curves and converts them to data coordinates.
"""

import os
import csv
from PIL import Image
import numpy as np
from pathlib import Path

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def find_line_pixels(img_array, target_color, tolerance=20):
    """Find all pixels matching a color (with tolerance) in the image."""
    target_rgb = hex_to_rgb(target_color)
    diff = np.abs(img_array[:,:,:3].astype(int) - np.array(target_rgb))
    matches = np.where(np.all(diff <= tolerance, axis=2))
    return list(zip(matches[1], matches[0]))  # (x, y) format

def pixels_to_data(pixel_x, pixel_y, plot_bounds, data_bounds):
    """Convert pixel coordinates to data coordinates."""
    px_min, px_max, py_min, py_max = plot_bounds
    dx_min, dx_max, dy_min, dy_max = data_bounds

    # Normalize pixel coords to [0, 1]
    norm_x = (pixel_x - px_min) / (px_max - px_min)
    norm_y = (pixel_y - py_min) / (py_max - py_min)

    # Map to data coordinates
    data_x = dx_min + norm_x * (dx_max - dx_min)
    data_y = dy_max - norm_y * (dy_max - dy_min)  # y is inverted in images

    return data_x, data_y

def extract_plot_01():
    """Extract data from plot_01_matplotlib.pdf - Sigmoid growth."""
    img = Image.open('outputs/haiku_image/plot_01_matplotlib_preview.png')
    img_array = np.array(img)

    # Plot bounds in pixels (approximate from visual inspection)
    plot_bounds = (133, 1019, 180, 620)  # (x_min, x_max, y_min, y_max)
    data_bounds = (0, 10, 0, 1)  # (x_min, x_max, y_min, y_max)

    # Series colors: blue, red, green
    series_colors = [
        ('#1f77b4', 'Fast'),
        ('#ff7f0e', 'Medium'),
        ('#2ca02c', 'Slow')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        # Group pixels by x position (within clusters)
        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 5) * 5  # Group nearby x coords
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        # Extract ~25 points across x range
        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_values = x_positions[px]
            py_avg = np.mean(py_values)  # Average y values at this x

            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 10 and 0 <= data_y <= 1:
                all_data.append((label, round(data_x, 3), round(data_y, 3)))

    return all_data

def extract_plot_02():
    """Extract data from plot_02_seaborn.pdf - Damped oscillations."""
    img = Image.open('outputs/haiku_image/plot_02_seaborn_preview.png')
    img_array = np.array(img)

    plot_bounds = (128, 1024, 155, 685)
    data_bounds = (0, 10, -1, 1)

    series_colors = [
        ('#1f77b4', 'gamma=0.1'),
        ('#ff7f0e', 'gamma=0.3'),
        ('#2ca02c', 'gamma=0.6'),
        ('#d62728', 'gamma=1.0')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 4) * 4
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 10 and -1 <= data_y <= 1:
                all_data.append((label, round(data_x, 3), round(data_y, 3)))

    return all_data

def extract_plot_03():
    """Extract data from plot_03_plotnine.pdf - SIR epidemic."""
    img = Image.open('outputs/haiku_image/plot_03_plotnine_preview.png')
    img_array = np.array(img)

    plot_bounds = (122, 970, 152, 845)
    data_bounds = (0, 100, 0, 1000)

    series_colors = [
        ('#1f77b4', 'Susceptible'),
        ('#ff7f0e', 'Infectious'),
        ('#2ca02c', 'Recovered')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 5) * 5
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 100 and 0 <= data_y <= 1000:
                all_data.append((label, round(data_x, 1), round(data_y, 1)))

    return all_data

def extract_plot_04():
    """Extract data from plot_04_pandas.pdf - Random walks."""
    img = Image.open('outputs/haiku_image/plot_04_pandas_preview.png')
    img_array = np.array(img)

    plot_bounds = (118, 990, 155, 825)
    data_bounds = (0, 200, -25, 20)

    series_colors = [
        ('#1f77b4', 'Walk 1'),
        ('#ff7f0e', 'Walk 2'),
        ('#2ca02c', 'Walk 3'),
        ('#d62728', 'Walk 4'),
        ('#9467bd', 'Walk 5')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 4) * 4
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 200:
                all_data.append((label, round(data_x, 1), round(data_y, 1)))

    return all_data

def extract_plot_05():
    """Extract data from plot_05_plotly.pdf - Lotka-Volterra."""
    img = Image.open('outputs/haiku_image/plot_05_plotly_preview.png')
    img_array = np.array(img)

    plot_bounds = (105, 868, 85, 560)
    data_bounds = (0, 50, 0, 60)

    series_colors = [
        ('#1f77b4', 'Prey'),
        ('#ff7f0e', 'Predator')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=30)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 3) * 3
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 50 and 0 <= data_y <= 60:
                all_data.append((label, round(data_x, 2), round(data_y, 1)))

    return all_data

def extract_plot_06():
    """Extract data from plot_06_ggplot2.pdf - Logistic growth."""
    img = Image.open('outputs/haiku_image/plot_06_ggplot2_preview.png')
    img_array = np.array(img)

    plot_bounds = (118, 995, 155, 815)
    data_bounds = (0, 20, 0, 200)

    series_colors = [
        ('#440154', 'K=50 r=1.0'),
        ('#31688e', 'K=100 r=0.5'),
        ('#35b779', 'K=200 r=0.3')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 4) * 4
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 20 and 0 <= data_y <= 200:
                all_data.append((label, round(data_x, 2), round(data_y, 1)))

    return all_data

def extract_plot_07():
    """Extract data from plot_07_base_r.pdf - Seasonal temperature."""
    img = Image.open('outputs/haiku_image/plot_07_base_r_preview.png')
    img_array = np.array(img)

    plot_bounds = (85, 930, 135, 810)
    data_bounds = (0, 2, -30, 35)

    series_colors = [
        ('#f8766d', 'Tropical'),
        ('#00ba38', 'Temperate'),
        ('#619cff', 'Continental'),
        ('#e79f00', 'Arctic')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=30)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 3) * 3
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 2:
                all_data.append((label, round(data_x, 3), round(data_y, 1)))

    return all_data

def extract_plot_08():
    """Extract data from plot_08_lattice.pdf - Exponential growth."""
    img = Image.open('outputs/haiku_image/plot_08_lattice_preview.png')
    img_array = np.array(img)

    plot_bounds = (90, 775, 120, 605)
    data_bounds = (0, 5, -10, 450)

    series_colors = [
        ('#0072b2', 'r=0.3'),
        ('#e69f00', 'r=0.7'),
        ('#009e73', 'r=1.2')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 3) * 3
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 5:
                all_data.append((label, round(data_x, 2), round(data_y, 1)))

    return all_data

def extract_plot_09():
    """Extract data from plot_09_cowplot.pdf - Polynomial trends."""
    img = Image.open('outputs/haiku_image/plot_09_cowplot_preview.png')
    img_array = np.array(img)

    plot_bounds = (110, 980, 138, 760)
    data_bounds = (-2, 2, -2.5, 2.5)

    series_colors = [
        ('#0072b2', 'Degree 1'),
        ('#d55e00', 'Degree 2'),
        ('#009e73', 'Degree 3'),
        ('#e69f00', 'Degree 4')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 4) * 4
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if -2 <= data_x <= 2 and -2.5 <= data_y <= 2.5:
                all_data.append((label, round(data_x, 3), round(data_y, 3)))

    return all_data

def extract_plot_10():
    """Extract data from plot_10_ggpubr.pdf - Sinusoidal waves."""
    img = Image.open('outputs/haiku_image/plot_10_ggpubr_preview.png')
    img_array = np.array(img)

    plot_bounds = (108, 1100, 135, 755)
    data_bounds = (0, 4 * np.pi, -1.2, 1.2)

    series_colors = [
        ('#0072b2', 'phi=0'),
        ('#d55e00', 'phi=3pi/4'),
        ('#009e73', 'phi=pi/2'),
        ('#e69f00', 'phi=pi/4')
    ]

    all_data = []

    for color, label in series_colors:
        pixels = find_line_pixels(img_array, color, tolerance=25)
        if not pixels:
            continue

        x_positions = {}
        for px, py in pixels:
            x_key = round(px / 4) * 4
            if x_key not in x_positions:
                x_positions[x_key] = []
            x_positions[x_key].append(py)

        sorted_x = sorted(x_positions.keys())
        step = max(1, len(sorted_x) // 25)

        for px in sorted_x[::step]:
            py_avg = np.mean(x_positions[px])
            data_x, data_y = pixels_to_data(px, py_avg, plot_bounds, data_bounds)
            if 0 <= data_x <= 4 * np.pi and -1.2 <= data_y <= 1.2:
                all_data.append((label, round(data_x, 3), round(data_y, 3)))

    return all_data

def save_csv(filename, data):
    """Save extracted data to CSV."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['series', 'x', 'y'])
        for row in data:
            writer.writerow(row)

def main():
    os.chdir('/Users/adamkucharski/Documents/GitHub/pdf2plot')

    plots = [
        (extract_plot_01, 'outputs/haiku_image/plot_01_matplotlib.csv', 'plot_01_matplotlib'),
        (extract_plot_02, 'outputs/haiku_image/plot_02_seaborn.csv', 'plot_02_seaborn'),
        (extract_plot_03, 'outputs/haiku_image/plot_03_plotnine.csv', 'plot_03_plotnine'),
        (extract_plot_04, 'outputs/haiku_image/plot_04_pandas.csv', 'plot_04_pandas'),
        (extract_plot_05, 'outputs/haiku_image/plot_05_plotly.csv', 'plot_05_plotly'),
        (extract_plot_06, 'outputs/haiku_image/plot_06_ggplot2.csv', 'plot_06_ggplot2'),
        (extract_plot_07, 'outputs/haiku_image/plot_07_base_r.csv', 'plot_07_base_r'),
        (extract_plot_08, 'outputs/haiku_image/plot_08_lattice.csv', 'plot_08_lattice'),
        (extract_plot_09, 'outputs/haiku_image/plot_09_cowplot.csv', 'plot_09_cowplot'),
        (extract_plot_10, 'outputs/haiku_image/plot_10_ggpubr.csv', 'plot_10_ggpubr'),
    ]

    summaries = []

    for extract_fn, csv_path, plot_name in plots:
        print(f'Extracting {plot_name}...')
        try:
            data = extract_fn()
            if data:
                save_csv(csv_path, data)

                # Get summary stats
                unique_series = set(row[0] for row in data)
                x_values = [row[1] for row in data]
                y_values = [row[2] for row in data]

                summary = f'{plot_name}: {len(unique_series)} series, x=[{min(x_values):.1f}, {max(x_values):.1f}], y=[{min(y_values):.1f}, {max(y_values):.1f}]'
                summaries.append(summary)
                print(f'  Saved {len(data)} points to {csv_path}')
            else:
                print(f'  Warning: No data extracted')
        except Exception as e:
            print(f'  Error: {e}')

    print('\n=== SUMMARY ===')
    for summary in summaries:
        print(summary)

if __name__ == '__main__':
    main()
