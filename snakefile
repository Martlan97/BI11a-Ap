import argparse
import csv
from bioservices import KEGG
from bioservices import UniProt
from tqdm import tqdm

rule get_alt_ids:
    input:
        "./data/RNA-Seq-counts.txt"
    output:
        "./output/alternate_identifiers.csv"
    shell:
        "python ./scripts/GeneIDConverter.py --input {input[0]} --output {output[0]}"

rule kegg:
    input:
        "./output/alternate_identifiers.csv"
    output:
        "./output/kegg.csv"
    shell:
        "python ./scripts/kegg.py --input {input[0]} --output {output[0]}"

rule uniprot:
    input:
        "./output/kegg.csv"
    output:
        "./output/uniprot.csv"
    shell:
        "python ./scripts/uniprot.py --input {input[0]} --output {output[0]}"

rule sort_by_pubmed:
    input:
        "./output/uniprot.csv"
    output:
        "./output/sorted_by_pubmed.csv"
    shell:
        "python ./scripts/sort_by_pubmed.py --input {input[0]} --output {output[0]}"

rule calculate_gc_content:
    input:
        "./output/sorted_by_pubmed.csv"
    output:
        "./output/gc_content.csv"
    shell:
        "python ./scripts/calculate_gc_content.py --input {input[0]} --output {output[0]}"

rule plot_gc_content:
    input:
        "./output/gc_content.csv"
    output:
        "./output/gc_plots/"
    shell:
        "Rscript ./scripts/plot_GC.R --input {input[0]} --output {output[0]}"