import argparse
import sys
import re

from bioservices import UniProt
from local_functions import *


def main():
    args = parse_args()
    data, row_count = uniprot(args.input)
    write_to_csv(args.output, data, row_count)


def uniprot(data_path):
    data = []
    with open(data_path, mode="r") as file:
        row_count = count_lines(file)
        csvReader = csv.reader(file, dialect="excel", delimiter="\t")

        header = csvReader.__next__()
        if header[0] == "KEGG_ID":
            header.extend(["gene_function", "PubMed_ID"])
            data.append(header)
            uniprot_id_index = header.index("UniProt_ID")
        else:
            sys.exit("The file does not contain a valid header, quitting.")

        for line in tqdm(csvReader, desc="Retrieving data", total=row_count-1):
            uniprot_id = line[uniprot_id_index]
            if uniprot_id:
                gene_function, pubmed_ids = get_uniprot_data(uniprot_id)
                line.extend([gene_function, ";".join(pubmed_ids)])
            else:
                line.extend(["", ""])
            data.append(line)

    return data, row_count


regex_function = re.compile("(?<=CC   -!- FUNCTION: )(?s:.*?)(?=CC   -!-)")
regex_pubmed = re.compile("(?<=RX   PubMed=)(\\d*)(?=;)")


def get_uniprot_data(uniprot_id):
    data = UniProt().retrieve("{0}".format(uniprot_id), frmt="txt")

    try:
        pubmed_ids = re.findall(regex_pubmed, data)
        match = re.search(regex_function, data)
        if match:
            gene_function = match.group()
            gene_function = re.sub("\nCC", "", gene_function)
            gene_function = re.sub(" +", " ", gene_function)
            gene_function = gene_function.strip().replace(";", ".")
        else:
            gene_function = ""
    except TypeError:
        gene_function = ""
        pubmed_ids = ""

    return gene_function, pubmed_ids


def parse_args():
    parser = argparse.ArgumentParser(description="Get gene functionality and PubMed identifiers.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./output/kegg.csv",
                        help="(absolute) path for file with UniProt identifiers. First row must be a header.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./output/uniprot.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
