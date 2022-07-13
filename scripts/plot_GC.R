require(argparser) || install.packages("argparser")
require(data.table) || install.packages("data.table")

p <- arg_parser("create plots for GC content")
p <- add_argument(parse = p,
                  arg = "--input",
                  help = "(absolute) path for file with GC content of sequences. First row must be a header.",
                  default = "./output/gc_content.csv")
p <- add_argument(parse = p,
                  arg = "--output",
                  help = "(absolute) path for directory where the plots should be put.",
                  default = "./output/gc_plots/")
argv <- parse_args(p)


plot_a_plot <- function(file_path, kegg_id, gc_content, gc_content_subsections) {
  seq_length <- length(gc_content_subsections)*10
  x <- seq(10, seq_length, by = 10)
  
  png(paste0(file_path, kegg_id, ".png", collapse = NULL),
      height = 480, width = seq_length)
  
  plot(x, gc_content_subsections, type = "o",
       xlim = c(0, tail(x, n = 1)), ylim = c(0, 100),
       xaxt = "n", yaxt = "n",
       xlab = "Sequence position", ylab = "GC percentage")
  axis(side = 1, at = seq(0, seq_length, by = 10))
  axis(side = 2, at = c(0,25,50,75,100))
  abline(h = gc_content, lty = 2)
  
  dev.off()
}


df <- as.data.frame(fread(file = argv$input, sep = "\t", header = TRUE))
df <- df[c("KEGG_ID", "gc_content", "gc_content_subsections")]

for(iterator in seq_len(nrow(df))) {
  kegg_id <- df[iterator, "KEGG_ID"]
  gc_content <- df[iterator, "gc_content"]
  gc_content_subsections <- as.list(as.integer(scan(text = df[iterator, "gc_content_subsections"],
                                                    what = "",
                                                    sep = ";")))
  plot_a_plot(file_path = argv$output,
              kegg_id = kegg_id,
              gc_content = gc_content,
              gc_content_subsections = gc_content_subsections)
}
