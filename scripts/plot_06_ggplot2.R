# install.packages(c("ggplot2", "dplyr", "tidyr"))
# Logistic population growth — 3 species with different carrying capacities
library(ggplot2)
library(dplyr)
library(tidyr)

dir.create("output", showWarnings = FALSE)
set.seed(6)

logistic <- function(t, r, K, N0) K / (1 + ((K - N0) / N0) * exp(-r * t))

t <- seq(0, 20, length.out = 100)
df <- tibble(
  t      = t,
  "K=100 r=0.5" = logistic(t, 0.5, 100, 5) + rnorm(length(t), 0, 1.5),
  "K=200 r=0.3" = logistic(t, 0.3, 200, 5) + rnorm(length(t), 0, 2.5),
  "K=50  r=1.0" = logistic(t, 1.0,  50, 5) + rnorm(length(t), 0, 1.0),
) |>
  pivot_longer(-t, names_to = "series", values_to = "y") |>
  arrange(series, t)

write.csv(df, "output/plot_06_ggplot2.csv", row.names = FALSE)

p <- ggplot(df, aes(t, y, color = series)) +
  geom_line(linewidth = 0.9) +
  scale_color_manual(values = c("#1f77b4", "#d62728", "#2ca02c")) +
  labs(x = "Time", y = "Population", title = "Logistic population growth (ggplot2)", color = NULL) +
  theme_bw()

ggsave("output/plot_06_ggplot2.pdf", p, width = 7, height = 5)
cat("Saved output/plot_06_ggplot2.{pdf,csv}\n")
