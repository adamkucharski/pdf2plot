# install.packages(c("cowplot", "ggplot2", "dplyr", "tidyr"))
# Polynomial trend lines — 4 series (degree 1 to 4) on the same axes
library(ggplot2)
library(cowplot)
library(dplyr)
library(tidyr)

dir.create("output", showWarnings = FALSE)
set.seed(9)

x <- seq(-2, 2, length.out = 80)
df <- tibble(
  x,
  "Degree 1" = 0.8 * x                                 + rnorm(length(x), 0, 0.15),
  "Degree 2" = 0.5 * x^2 - 0.3                         + rnorm(length(x), 0, 0.15),
  "Degree 3" = 0.4 * x^3 - 0.6 * x                     + rnorm(length(x), 0, 0.15),
  "Degree 4" = 0.3 * x^4 - 0.8 * x^2 + 0.2             + rnorm(length(x), 0, 0.15),
) |>
  pivot_longer(-x, names_to = "series", values_to = "y") |>
  arrange(series, x)

write.csv(df, "output/plot_09_cowplot.csv", row.names = FALSE)

p <- ggplot(df, aes(x, y, color = series)) +
  geom_line(linewidth = 0.9) +
  scale_color_manual(values = c("#1f77b4", "#d62728", "#2ca02c", "#ff7f0e")) +
  labs(x = "x", y = "y", title = "Polynomial trends (cowplot)", color = NULL) +
  theme_cowplot(font_size = 12)

save_plot("output/plot_09_cowplot.pdf", p, base_width = 7, base_height = 5)
cat("Saved output/plot_09_cowplot.{pdf,csv}\n")
