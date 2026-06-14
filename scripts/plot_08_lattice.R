# install.packages("lattice")
# Exponential growth with noise — 3 growth rates
library(lattice)

dir.create("output", showWarnings = FALSE)
set.seed(8)

t <- seq(0, 5, length.out = 80)
params <- data.frame(
  series = c("r=0.3", "r=0.7", "r=1.2"),
  r      = c(0.3, 0.7, 1.2),
  col    = c("#1f77b4", "#d62728", "#2ca02c")
)

rows <- do.call(rbind, lapply(seq_len(nrow(params)), function(i) {
  y <- exp(params$r[i] * t) + rnorm(length(t), 0, 0.05 * exp(params$r[i] * max(t)))
  data.frame(t = t, series = params$series[i], y = y)
}))
write.csv(rows, "output/plot_08_lattice.csv", row.names = FALSE)

p <- xyplot(y ~ t, groups = series, data = rows, type = "l", lwd = 1.8,
            col = params$col,
            xlab = "Time", ylab = "Population",
            main = "Exponential growth (lattice)",
            auto.key = list(lines = TRUE, points = FALSE, space = "right"))

pdf("output/plot_08_lattice.pdf", width = 7, height = 5)
print(p)
dev.off()
cat("Saved output/plot_08_lattice.{pdf,csv}\n")
