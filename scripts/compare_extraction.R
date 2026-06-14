# compare_extraction.R
# Compare pdf2plot and haiku image extraction against true simulated values.
# Run from project root: Rscript scripts/compare_extraction.R

suppressMessages({
  library(dplyr)
  library(tidyr)
  library(readr)
  library(tibble)
})

TRUE_DIR     <- "output"
PDF2PLOT_DIR <- "outputs/pdf2plot_extracted"
HAIKU_DIR    <- "outputs/haiku_image"

plots <- tribble(
  ~id, ~stem,                ~library,     ~scenario,           ~n_series,
  1L,  "plot_01_matplotlib", "matplotlib", "Sigmoid growth",     3L,
  2L,  "plot_02_seaborn",    "seaborn",    "Damped oscillations",4L,
  3L,  "plot_03_plotnine",   "plotnine",   "SIR epidemic",       3L,
  4L,  "plot_04_pandas",     "pandas",     "Random walks",       5L,
  5L,  "plot_05_plotly",     "plotly",     "Predator-prey",      2L,
  6L,  "plot_06_ggplot2",    "ggplot2",    "Logistic growth",    3L,
  7L,  "plot_07_base_r",     "base R",     "Seasonal patterns",  4L,
  8L,  "plot_08_lattice",    "lattice",    "Exponential growth", 3L,
  9L,  "plot_09_cowplot",    "cowplot",    "Polynomial trends",  4L,
  10L, "plot_10_ggpubr",     "ggpubr",     "Sinusoidal waves",   4L
)

# Load CSV and standardize to series (chr), x (dbl), y (dbl)
load_std <- function(path) {
  df <- suppressMessages(read_csv(path))
  names(df) <- gsub('"', '', names(df))
  if ("t"    %in% names(df)) df <- rename(df, x = t)
  if ("step" %in% names(df)) df <- rename(df, x = step)
  df |>
    mutate(
      series = trimws(gsub('"', '', gsub("\\s+", " ", as.character(series)))),
      x = as.numeric(x),
      y = as.numeric(y)
    ) |>
    select(series, x, y) |>
    filter(!is.na(x), !is.na(y))
}

# True series in order of first appearance in the CSV
series_appearance_order <- function(df) {
  df |>
    mutate(.row = row_number()) |>
    group_by(series) |>
    summarise(first_row = min(.row), .groups = "drop") |>
    arrange(first_row) |>
    pull(series)
}

# All permutations of 1:n as a list of integer vectors
all_permutations <- function(n) {
  if (n == 1L) return(list(1L))
  lapply(seq_len(n), function(i) {
    lapply(all_permutations(n - 1L), function(p) c(i, ifelse(p >= i, p + 1L, p)))
  }) |> unlist(recursive = FALSE)
}

# Interpolate extracted y at true x positions; return absolute errors
interp_abs_errors <- function(true_sub, ext_sub) {
  if (nrow(ext_sub) < 2) return(numeric(0))
  x_range <- range(ext_sub$x)
  t2 <- filter(true_sub, x >= x_range[1] - 1e-6, x <= x_range[2] + 1e-6)
  if (nrow(t2) < 2) return(numeric(0))
  y_pred <- approx(ext_sub$x, ext_sub$y, xout = t2$x, rule = 2)$y
  abs(t2$y - y_pred)
}

compute_mae <- function(stem, ext_dir, method) {
  ext_path <- file.path(ext_dir, paste0(stem, ".csv"))
  if (!file.exists(ext_path)) return(NA_real_)

  true_df <- load_std(file.path(TRUE_DIR, paste0(stem, ".csv")))
  ext_df  <- load_std(ext_path)

  true_order <- series_appearance_order(true_df)

  if (method == "pdf2plot") {
    # pdf2plot labels series 1,2,3 in drawing order, which may differ from
    # creation order when the plotting library re-sorts factor levels.
    # Use optimal matching: try all permutations and keep the lowest MAE.
    ext_order <- as.character(sort(as.integer(unique(ext_df$series))))
    n <- min(length(true_order), length(ext_order))
    true_order <- true_order[seq_len(n)]
    ext_order  <- ext_order[seq_len(n)]

    best_mae <- Inf
    for (perm in all_permutations(n)) {
      abs_errors <- numeric(0)
      for (i in seq_len(n)) {
        t_sub <- filter(true_df, series == true_order[i])          |> arrange(x)
        e_sub <- filter(ext_df,  series == ext_order[[perm[[i]]]]) |> arrange(x)
        abs_errors <- c(abs_errors, interp_abs_errors(t_sub, e_sub))
      }
      if (length(abs_errors) > 0) best_mae <- min(best_mae, mean(abs_errors))
    }
    if (is.infinite(best_mae)) NA_real_ else best_mae

  } else {
    # haiku: series named from legend labels — match by name, order-independent
    ext_names <- unique(ext_df$series)
    abs_errors <- numeric(0)
    for (ts in true_order) {
      matched <- ext_names[ext_names == ts]
      if (length(matched) == 0) next
      t_sub <- filter(true_df, series == ts)           |> arrange(x)
      e_sub <- filter(ext_df,  series == matched[[1]]) |> arrange(x)
      abs_errors <- c(abs_errors, interp_abs_errors(t_sub, e_sub))
    }
    if (length(abs_errors) == 0) NA_real_ else mean(abs_errors)
  }
}

# Normalised MAE as % of true y-range (scale-independent, for cross-plot summary)
nmae_pct <- function(stem, ext_dir, method) {
  true_df <- load_std(file.path(TRUE_DIR, paste0(stem, ".csv")))
  y_range <- diff(range(true_df$y, na.rm = TRUE))
  if (y_range == 0) return(NA_real_)
  mae <- compute_mae(stem, ext_dir, method)
  if (is.na(mae)) return(NA_real_)
  mae / y_range * 100
}

# Compute results
results <- plots |>
  rowwise() |>
  mutate(
    mae_pdf2plot  = compute_mae(stem, PDF2PLOT_DIR, "pdf2plot"),
    mae_haiku     = compute_mae(stem, HAIKU_DIR,    "haiku"),
    nmae_pdf2plot = nmae_pct(stem, PDF2PLOT_DIR, "pdf2plot"),
    nmae_haiku    = nmae_pct(stem, HAIKU_DIR,    "haiku")
  ) |>
  ungroup()

# Totals row: mean normalised MAE across all plots (comparable across scales)
totals <- tibble(
  id            = NA_integer_,
  library       = "All",
  scenario      = "mean normalised absolute error (%)",
  n_series      = sum(results$n_series),
  mae_pdf2plot  = NA_real_,
  mae_haiku     = NA_real_,
  nmae_pdf2plot = mean(results$nmae_pdf2plot, na.rm = TRUE),
  nmae_haiku    = mean(results$nmae_haiku,    na.rm = TRUE)
)

full_results <- bind_rows(results, totals)

# Save CSV (per-plot rows + totals row)
out_csv <- "outputs/extraction_comparison.csv"
write_csv(full_results, out_csv)
cat("Saved:", out_csv, "\n\n")

# Print table
fmt_mae <- function(x) {
  if (is.na(x))  return("—")
  if (x < 0.001) return(formatC(x, format = "e", digits = 2))
  if (x < 10)    return(formatC(x, format = "f", digits = 4))
  formatC(x, format = "f", digits = 2)
}
fmt_nmae <- function(x) if (is.na(x)) "—" else sprintf("%.2f%%", x)

table_rows <- results |>
  transmute(
    Plot              = sprintf("%02d", id),
    Library           = library,
    Scenario          = scenario,
    `N series`        = as.character(n_series),
    `pdf2plot MAE`    = sapply(mae_pdf2plot,  fmt_mae),
    `haiku MAE`       = sapply(mae_haiku,     fmt_mae),
    `pdf2plot NMAE`   = sapply(nmae_pdf2plot, fmt_nmae),
    `haiku NMAE`      = sapply(nmae_haiku,    fmt_nmae)
  )

totals_row <- tibble(
  Plot            = "All",
  Library         = "",
  Scenario        = "mean NMAE (%)",
  `N series`      = as.character(sum(results$n_series)),
  `pdf2plot MAE`  = "—",
  `haiku MAE`     = "—",
  `pdf2plot NMAE` = fmt_nmae(totals$nmae_pdf2plot),
  `haiku NMAE`    = fmt_nmae(totals$nmae_haiku)
)

final_table <- bind_rows(table_rows, totals_row)

cat("## Extraction accuracy: MAE vs true simulated values\n")
cat("## NMAE = MAE / y-range × 100 (scale-independent; All row shows mean across plots)\n\n")

widths <- c(5, 12, 22, 9, 14, 12, 15, 12)
cols   <- names(final_table)
header <- paste(mapply(formatC, cols, widths, MoreArgs = list(flag = "-")), collapse = " | ")
sep    <- paste(sapply(widths, function(w) strrep("-", w)), collapse = "-+-")
cat(header, "\n", sep, "\n", sep = "")

for (i in seq_len(nrow(final_table))) {
  r <- final_table[i, ]
  if (r$Plot == "All") cat(sep, "\n")
  cat(paste(mapply(formatC, unlist(r), widths, MoreArgs = list(flag = "-")), collapse = " | "), "\n")
}
cat("\n")
