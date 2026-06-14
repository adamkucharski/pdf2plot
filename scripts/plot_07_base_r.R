# Base R graphics — no packages required
# Seasonal temperature patterns — 4 cities (simple harmonic model)
dir.create("output", showWarnings = FALSE)
set.seed(7)

t <- seq(0, 2, length.out = 104)  # 2 years, weekly
seasonal <- function(t, mean, amp, phase, sd) {
  mean + amp * sin(2 * pi * t + phase) + rnorm(length(t), 0, sd)
}

series <- list(
  "Tropical"    = seasonal(t, 28,  3,  0.0, 0.8),
  "Temperate"   = seasonal(t, 12, 10,  0.0, 1.2),
  "Continental" = seasonal(t,  8, 18,  0.1, 1.5),
  "Arctic"      = seasonal(t, -5, 22,  0.2, 2.0)
)

rows <- do.call(rbind, lapply(names(series), function(nm) {
  data.frame(t = t, series = nm, y = series[[nm]])
}))
write.csv(rows, "output/plot_07_base_r.csv", row.names = FALSE)

colors <- c("#e6550d", "#31a354", "#3182bd", "#756bb1")
ylim   <- range(unlist(series))

pdf("output/plot_07_base_r.pdf", width = 7, height = 5)
plot(NA, xlim = range(t), ylim = ylim,
     xlab = "Year", ylab = "Temperature (°C)",
     main = "Seasonal temperature patterns (base R)")
for (i in seq_along(series)) {
  lines(t, series[[i]], col = colors[i], lwd = 1.8)
}
legend("topright", legend = names(series), col = colors, lwd = 1.8, bty = "n")
dev.off()
cat("Saved output/plot_07_base_r.{pdf,csv}\n")
