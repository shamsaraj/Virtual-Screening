# ROC curve(s) and enrichment factor calculation using ROCR + enrichvs.
#
# Requires: ROCR, enrichvs (install.packages(c("ROCR", "enrichvs")))
#
# For each score column in `header`, reads actives_file and decoys_file,
# computes AUC + enrichment factors, appends results to output_file, and
# writes a per-column ROC curve PDF.
#
# Input files: semicolon-separated CSVs with columns matching `header` below.

library(ROCR)
library(enrichvs)

# ---- Configuration: edit for your data ----
working_dir <- "."
actives_file <- "actives.csv"
decoys_file <- "decoys.csv"
header <- c("energy")   # score column name(s) in actives_file / decoys_file -- NOT the id column
output_file <- "output.txt"

setwd(working_dir)

write(paste("Scoring", "AUC", "EF100%", "EF20%", "EF10%", "EF2%", "EF1%", "EF0.2%", "EF0.1%", sep = ","),
      file = output_file, append = TRUE)

for (i in seq_along(header)) {
  title <- header[i]

  actives_table <- read.csv(actives_file, sep = ";", header = TRUE)
  actives_scores <- actives_table[[title]]
  actives_scores <- actives_scores[!is.na(actives_scores)]

  decoys_table <- read.csv(decoys_file, sep = ";", header = TRUE)
  decoys_scores <- decoys_table[[title]]
  decoys_scores <- decoys_scores[!is.na(decoys_scores)]

  scores <- c(actives_scores, decoys_scores)
  rocr_labels <- rep(c("actives", "decoys"), c(length(actives_scores), length(decoys_scores)))
  enrich_labels <- rep(c(1, 0), c(length(actives_scores), length(decoys_scores)))

  # Enrichment factors and AUC via enrichvs
  ef100 <- enrichment_factor(scores, enrich_labels, top = 1.0, decreasing = FALSE)
  ef20  <- enrichment_factor(scores, enrich_labels, top = 0.2, decreasing = FALSE)
  ef10  <- enrichment_factor(scores, enrich_labels, top = 0.1, decreasing = FALSE)
  ef2   <- enrichment_factor(scores, enrich_labels, top = 0.02, decreasing = FALSE)
  ef1   <- enrichment_factor(scores, enrich_labels, top = 0.01, decreasing = FALSE)
  ef0.2 <- enrichment_factor(scores, enrich_labels, top = 0.002, decreasing = FALSE)
  ef0.1 <- enrichment_factor(scores, enrich_labels, top = 0.001, decreasing = FALSE)
  auc_enrichvs <- auc(scores, enrich_labels, decreasing = FALSE, top = 1.0)

  write(paste(title, auc_enrichvs, ef100, ef20, ef10, ef2, ef1, ef0.2, ef0.1, sep = ","),
        file = output_file, append = TRUE)

  # ROC curve via ROCR
  pred <- prediction(scores, rocr_labels)
  perf <- performance(pred, "tpr", "fpr")

  par(mar = c(5, 5, 2, 2), xaxs = "i", yaxs = "i", cex.axis = 1.3, cex.lab = 1.4)
  pdf(paste(actives_file, title, "pdf", sep = "."))
  plot(perf, col = "black", lty = 3, lwd = 3)

  auc_rocr <- unlist(slot(performance(pred, "auc"), "y.values"))
  auc_label <- paste0("AUC = ", round(auc_rocr, digits = 2))
  legend(0.5, 0.3, c(auc_label), border = "white", cex = 1.7, box.col = "white")
  dev.off()
}
