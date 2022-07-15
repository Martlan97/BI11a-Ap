# BI11a-Ap
A workflow for the analysis of Lactobacillus plantarum.

## I - Installation
In order to execute the workflow make sure the following dependencies are installed:

Software:
- python version 3.9.10
- R version 3.6.3

R libraries (installed automatically if not already present):
- argparser
- data.table

Python modules:
- bioservices
- tqdm

## II - Usage
This workflow can be used to gather and generate data for (KEGG) genes:
- Retrieving the associated UniProt and NCBI protein identifiers
- Retrieving the NT sequences
- Retrieving the pathways 
- Retrieving the gene functions
- Retrieving the associated PubMed identifiers
- Creating an overview of genes that appear in the same PubMed articles
- Calculating the GC contents of the gene sequences
- Creating plots to visualize the GC contents

### IIa - Data
The files in the 'data' folder where used while developing this workflow, other files may be used as well however. Make sure these files follow the following format:
- The first row must contain a header
- The first column must be labeled 'ID' and contain at least 1 valid KEGG ID.
- Columns must be tab seperated
- Multiple values in the same cell must be seperated with a semicolon ';' (without additional whitespace)

| ID        | Attribute 1 | Attribute ... |
|-----------|-------------|---------------|
| lp_0001   | {value}     | ...           |
| lp_0002   | {value}     | ...           |
| ...       | ...         | ...           |

### IIb - Running the workflow
The entire workflow can be executed with the 'snakemake' command from within the BI11a-Ap directory.
```commandline
snakemake
```
To only run a part of the workflow specify the desired output file(s) or folder.
```commandline
snakemake results/{filename}.csv

snakemake results/gc_plots
```
Alternatively the python can also be run directly from the commandline. All scripts have the same optional ```--input``` and ```--output``` options.
```commandline
python workflow/scripts/{script}.py --input path/to/{inputfile}.csv --output path/to/{outputfile}.csv

Rscript workflow/scripts/plot_GC.R --input path/to/{inputfile}.csv --output path/to/{outputfolder}
```
## III - Workflow

![Workflow](.github/images/dag.svg?raw=true)

## IV - Functions
|             | gene_id_converter.py                                                                       |
|-------------|:-------------------------------------------------------------------------------------------|
| Description | Get UniProt and NCBI protein identifiers for given gene                                    |
| Returns     | .csv file containing the original input with the retrieved IDs appended in two new columns |

|             | kegg.py                                                                                     |
|-------------|:--------------------------------------------------------------------------------------------|
| Description | Get NT sequence and pathways for given gene                                                 |
| Returns     | .csv file containing the original input with the retrieved data appended in two new columns |

|             | uniprot.py                                                                                  |
|-------------|:--------------------------------------------------------------------------------------------|
| Description | Get function and PubMed identifiers for given gene                                          |
| Returns     | .csv file containing the original input with the retrieved data appended in two new columns |

|             | sorted_by_pubmed.py                                                               |
|-------------|:----------------------------------------------------------------------------------|
| Description | Sort the the input file in descending order by the number PubMed IDs of each gene |
| Returns     | Sorted .csv file                                                                  |

|             | cluster_pubmed.py                                        |
|-------------|:---------------------------------------------------------|
| Description | Creates a list of genes per PubMed ID that share that ID |
| Returns     | .csv with PubMed IDs and their associated KEGG IDs       |

|             | calculate_gc_content.py                                                              |
|-------------|:-------------------------------------------------------------------------------------|
| Description | Calculates the total and windowed GC content of the NT sequence of each gene         |
| Returns     | .csv file containing the original input with the GC data appended in two new columns |

|             | plot_GC.R                                                   |
|-------------|:------------------------------------------------------------|
| Description | Plot the GC content of each gene                            |
| Returns     | .png file for each gene containing a plot of the GC content |

## V - Credits
Martijn Landman
