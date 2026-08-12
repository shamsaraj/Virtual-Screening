# ROC curve comparison across multiple targets, using ROCR.
#
# Requires: ROCR, enrichvs (install.packages(c("ROCR", "enrichvs")))
#
# Input files: <actives>/<decoys> CSVs, semicolon-separated, with a header
# row and the score in the 2nd column.

library(ROCR)
library(enrichvs)

# ---- Configuration: edit this list for your data ----
targets <- list(
  list(name = "3F17", actives = "E:/SP/3F17/actives.csv", decoys = "E:/SP/3F17/decoys.csv"),
  list(name = "3F19", actives = "E:/SP/3F19/actives.csv", decoys = "E:/SP/3F19/decoys.csv"),
  list(name = "3N2V", actives = "E:/SP/3N2V/actives.csv", decoys = "E:/SP/3N2V/decoys.csv"),
  list(name = "3NX7", actives = "E:/SP/3NX7/actives.csv", decoys = "E:/SP/3NX7/decoys.csv")
)
output_pdf <- "cross.pdf"
plot_styles <- list(
  list(lty = 1, lwd = 1),
  list(lty = 3, lwd = 3),
  list(lty = 2, lwd = 2),
  list(lty = 3, lwd = 5)
)

# ---- Load scores and build ROCR performance objects ----
perf_list <- list()
auc_list <- numeric(length(targets))

for (i in seq_along(targets)) {
  target <- targets[[i]]
  actives_scores <- read.csv(target$actives, sep = ";", header = TRUE)[, 2]
  actives_scores <- actives_scores[!is.na(actives_scores)]
  decoys_scores <- read.csv(target$decoys, sep = ";", header = TRUE)[, 2]
  decoys_scores <- decoys_scores[!is.na(decoys_scores)]

  scores <- c(actives_scores, decoys_scores)
  labels <- rep(c("actives", "decoys"), c(length(actives_scores), length(decoys_scores)))

  pred <- prediction(scores, labels)
  perf_list[[i]] <- performance(pred, "tpr", "fpr")
  auc_list[i] <- unlist(slot(performance(pred, "auc"), "y.values"))
}

# ---- Plot overlaid ROC curves ----
par(mar = c(5, 5, 2, 2), xaxs = "i", yaxs = "i", cex.axis = 1.3, cex.lab = 1.4)
pdf(output_pdf)

plot(perf_list[[1]], col = "black", lty = plot_styles[[1]]$lty, lwd = plot_styles[[1]]$lwd)
for (i in 2:length(perf_list)) {
  plot(perf_list[[i]], add = TRUE, col = "black",
       lty = plot_styles[[i]]$lty, lwd = plot_styles[[i]]$lwd)
}
abline(a = 0, b = 1, lty = 3, lwd = 1)

# Legend key showing line styles
legend_y <- seq(0.36, by = -0.08, length.out = length(targets))
for (i in seq_along(targets)) {
  segments(0.8, legend_y[i], 0.92, legend_y[i], col = "black",
           lty = plot_styles[[i]]$lty, lwd = plot_styles[[i]]$lwd)
}

# AUC labels
for (i in seq_along(targets)) {
  auc_label <- paste0("AUC for ", targets[[i]]$name, " = ", round(auc_list[i], digits = 3))
  legend(0.4, 0.4 - (i - 1) * 0.08, c(auc_label), border = "white", cex = 1, box.col = "white")
}

dev.off()
