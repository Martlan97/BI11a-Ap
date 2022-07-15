require(argparser) || install.packages("argparser")
require(data.table) || install.packages("data.table")

# Parses commandline strings. Has an --input and --output argument for an input file and output path respectively.
# The input file must be tabular with a header row and the columns 'KEGG_ID', 'gc_conent' and 'gc_content_subsections'
# containing valid KEGG identifiers, an integer representing the total gc percentage and a line of integers representing
# the gc percentage of subsections seperated by semicolons respectively.
# The output must be a string representing a file path, not a file.
p <- arg_parser("create plots for GC content")
p <- add_argument(parse = p,
                  arg = "--input",
                  help = "(absolute) path for file with GC content of sequences. First row must be a header.",
                  default = "./results/gc_content.csv")
p <- add_argument(parse = p,
                  arg = "--output",
                  help = "(absolute) path for directory where the plots should be put.",
                  default = "./results/gc_plots")
argv <- parse_args(p)

# Function plots the subsectioned gc content and adds the total gc percentage (gc_content) as a straight line.
# The KEGG ID is used for the name of the output file which is placed in the location specified by the file path.
plot_a_plot <- function(file_path, kegg_id, gc_content, gc_content_subsections) {
  seq_length <- length(gc_content_subsections)*10
  x <- seq(10, seq_length, by = 10)
  
  png(paste0(file_path, "/", kegg_id, ".png", collapse = NULL),
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

# Checks if the specified output directory exists and creates it if it doesn not.
if (!file.exists(argv$output)){
  dir.create(argv$output)
}

# Uses the fast read function from data.table to read the input file into a data frame, then removes unneeded columns
# by overriding the variable while only keeping the specified columns.
df <- as.data.frame(fread(file = argv$input, sep = "\t", header = TRUE))
df <- df[c("KEGG_ID", "gc_content", "gc_content_subsections")]

# Iterates over the rows of the data frame and stores the KEGG ID, total gc percentage and gc subsections in variables.
# The gc subsections are converted from a string to a list of integers by seperating them on the semicolon.
# The plot_a_plot function is then called for each row in the data frame resulting in n number of plots being created
# and stored in the specified output directory.
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
