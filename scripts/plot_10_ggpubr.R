# install.packages(c("ggpubr", "ggplot2", "dplyr", "tidyr"))
# Sinusoidal waves with phase offsets — 4 series
library(ggplot2)
library(ggpubr)
library(dplyr)
library(tidyr)

dir.create("output", showWarnings = FALSE)
set.seed(10)

t <- seq(0, 4 * pi, length.out = 120)
phases <- c(0, pi / 4, pi / 2, 3 * pi / 4)
names  <- c("phi=0", "phi=pi/4", "phi=pi/2", "phi=3pi/4")

df <- tibble(t = t)
for (i in seq_along(phases)) {
  df[[names[i]]] <- sin(t + phases[i]) + rnorm(length(t), 0, 0.08)
}
df <- pivot_longer(df, -t, names_to = "series", values_to = "y") |>
  arrange(series, t)

write.csv(df, "output/plot_10_ggpubr.csv", row.names = FALSE)

p <- ggline(df, x = "t", y = "y", color = "series",
            plot_type = "l",
            palette = c("#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"),
            xlab = "t", ylab = "Amplitude",
            title = "Sinusoidal waves (ggpubr)",
            ggtheme = theme_pubr()) +
  geom_hline(yintercept = 0, linewidth = 0.4, linetype = "dashed")

ggexport(p, filename = "output/plot_10_ggpubr.pdf", width = 7, height = 5)
cat("Saved output/plot_10_ggpubr.{pdf,csv}\n")
