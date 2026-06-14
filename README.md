# pdf2plot

A web app and Claude skill to extract data from PDF figures.

Link to the web app: https://adamkucharski.github.io/pdf2plot/

Link to the Claude skill: [`skills/pdf2plot.md`](skills/pdf2plot.md) 

## How the web app works

1. **Upload**: Drop a PDF containing a figure with vector graphics
2. **Calibrate**: Select two X-axis tick marks and two Y-axis tick marks, entering their actual values
3. **Select Data**: Click on the lines/paths you want to extract
4. **Export**: Download the rescaled coordinates as CSV

The app uses PDF.js to parse PDF files directly in the browser and extract vector path coordinates. It then applies linear (or logarithmic) interpolation based on your calibration points to convert the raw PDF coordinates to the actual data values.

This new app was inspired by my previous discontinued package [scrapR](https://github.com/adamkucharski/scrapR/).

## How the Claude Code skill works

If you use [Claude Code](https://claude.com/claude-code), you can run the full extraction pipeline without any human clicking — Claude extracts axis labels and data coordinates purely from the PDF geometry — no image inspection required.

**Usage**

The skill is at [`skills/pdf2plot.md`](skills/pdf2plot.md) — it includes the helper script inline, which Claude writes to disk on first run.

Once the skill is loaded, call the skill and point to the relevant figure (e.g. `~/Documents/figure_name.pdf`):

```
/pdf2plot ~/Documents/figure_name.pdf
```

Claude extracts vector paths and axis labels from the PDF geometry, identifies calibration anchors, and writes a CSV to the same directory as the PDF. If matplotlib is installed, a line plot is also saved alongside the CSV.

## Limitations

- Only works with vector-based PDFs (not scanned/rasterized images)
- Complex PDFs with many elements may require pre-processing
- First page only is processed

## Validation

Extraction accuracy was benchmarked on 10 synthetic line plots generated across common R and Python plotting libraries (2–5 series each). Each plot was extracted using two methods: pdf2plot (geometry-based) and direct image extraction by a Claude Code agent using Claude Haiku. Error is measured in terms of normalised MAE (mean absolute error as a % of the true y-range).

| Library | Scenario | pdf2plot NMAE | Haiku NMAE |
|---|---|---:|---:|
| matplotlib | Sigmoid growth | 0.04% | 6.7% |
| seaborn | Damped oscillations | 0.08% | 13.3% |
| plotnine | SIR epidemic | 0.14% | 8.0% |
| pandas | Random walks | 0.05% | 15.6% |
| plotly | Predator-prey | 0.46% | 25.2% |
| ggplot2 | Logistic growth | 0.11% | 15.5% |
| base R | Seasonal patterns | 0.04% | 20.4% |
| lattice | Exponential growth | 0.17% | 31.5% |
| cowplot | Polynomial trends | 0.19% | 11.1% |
| ggpubr | Sinusoidal waves | 2.53% | 32.1% |
| **Mean** | | **0.38%** | **17.9%** |

Scripts to reproduce this benchmark are in [`scripts/`](scripts/). The `plot_01_*` to `plot_10_*` scripts generate each synthetic figure as a PDF; `compare_extraction.R` sources the pdf2plot and haiku extractions once complete and writes `outputs/extraction_comparison.csv`; `plot_extraction_comparison.R` produces the bar charts above.

## Technical details for the web app

- Built with vanilla JavaScript (no frameworks)
- Uses [PDF.js](https://mozilla.github.io/pdf.js/) for PDF parsing
- All computation happens client-side
- Works with modern browsers (Chrome, Firefox, Safari, Edge)

## Citation

If you use pdf2plot in your work, please cite:

```
Kucharski, A. (2026). pdf2plot: A web tool and skill for extracting data from PDF figures.
https://github.com/adamkucharski/pdf2plot
```
