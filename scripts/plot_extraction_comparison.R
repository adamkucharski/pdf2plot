# plot_extraction_comparison.R
# Horizontal bar chart: extraction accuracy by library, haiku vs pdf2plot
# Run from project root: Rscript scripts/plot_extraction_comparison.R

library(ggplot2)
library(dplyr)
library(readr)

df <- read_csv("output/extraction_comparison.csv", show_col_types = FALSE) |>
  filter(!is.na(id)) |>
  mutate(library = reorder(library, -nmae_haiku))

p <- ggplot(df) +
  geom_col(aes(x = nmae_haiku,    y = library, fill = "haiku"),    width = 0.7) +
  geom_col(aes(x = nmae_pdf2plot, y = library, fill = "pdf2plot"), width = 0.7) +
  geom_text(aes(x = nmae_haiku,    y = library, label = sprintf("%.1f%%", nmae_haiku)),
            hjust = -0.15, size = 3, colour = "#888888") +
  geom_text(aes(x = nmae_pdf2plot, y = library, label = sprintf("%.2f%%", nmae_pdf2plot)),
            hjust = -0.15, size = 3, colour = "#0072B2") +
  scale_fill_manual(
    values = c(haiku = "#cccccc", pdf2plot = "#0072B2"),
    labels = c(haiku = "claude haiku (image)", pdf2plot = "pdf2plot (geometry)"),
    name   = NULL
  ) +
  scale_x_continuous(labels = function(x) paste0(x, "%"), expand = expansion(mult = c(0, 0.2))) +
  labs(
    x = "Normalised mean absolute error (%)",
    y = NULL,
    title = "Data extraction error by library\nused to originally create plot"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position       = c(0.98, 0.8),
    legend.justification  = c("right", "bottom"),
    legend.background     = element_rect(fill = "white", colour = NA),
    panel.grid.major.y    = element_blank(),
    panel.grid.minor      = element_blank(),
    axis.line.x           = element_line(colour = "#333333", linewidth = 0.3),
    axis.ticks.x          = element_line(colour = "#333333", linewidth = 0.3),
    plot.title            = element_text(face = "bold")
  )

out <- "output/extraction_comparison_bars.pdf"
ggsave(out, p, width = 4, height = 5)
cat("Saved:", out, "\n")

# Overall summary: single bar per method
totals <- read_csv("output/extraction_comparison.csv", show_col_types = FALSE) |>
  filter(is.na(id))

df_overall <- data.frame(
  method = c("claude haiku\n(image)", "pdf2plot\n(geometry)"),
  nmae   = c(totals$nmae_haiku, totals$nmae_pdf2plot),
  fill   = c("haiku", "pdf2plot")
)
df_overall$method <- factor(df_overall$method, levels = df_overall$method)

p_overall <- ggplot(df_overall, aes(x = nmae, y = method, fill = fill)) +
  geom_col(width = 0.5) +
  geom_text(aes(label = sprintf("%.2f%%", nmae)), hjust = -0.15, size = 4) +
  scale_fill_manual(values = c(haiku = "#cccccc", pdf2plot = "#0072B2"), guide = "none") +
  scale_x_continuous(labels = function(x) paste0(x, "%"), expand = expansion(mult = c(0, 0.25))) +
  labs(
    x     = "Mean normalised absolute error",
    y     = NULL,
    title = "Overall extraction accuracy"
  ) +
  theme_minimal(base_size = 13) +
  theme(
    panel.grid.major.y = element_blank(),
    panel.grid.minor   = element_blank(),
    axis.line.x        = element_line(colour = "#333333", linewidth = 0.3),
    axis.ticks.x       = element_line(colour = "#333333", linewidth = 0.3),
    plot.title         = element_text(face = "bold")
  )

out_overall <- "output/extraction_comparison_overall.pdf"
ggsave(out_overall, p_overall, width = 5, height = 2.5)
cat("Saved:", out_overall, "\n")
