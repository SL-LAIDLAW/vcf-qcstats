#!/usr/bin/env Rscript
library(ggplot2)

args = commandArgs(trailingOnly=TRUE)

# data = read.table(datatable, ";")
data = read.table(args[1], header=TRUE)
ggplot(data, aes(x=quality, color=category)) + geom_freqpoly()
ggplot(data, aes(x=quality, fill=category)) + geom_density(alpha=.3)
# dev.print(png, 'variant_COUNT.png',width = 600)
# dev.print(png, 'variant-DENSITY.png',width = 600)

file <- tempfile()
ggsave(file, device = "pdf")
unlink(file)