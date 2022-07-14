import argparse
import sys

from bioservices import KEGG
from local_functions import *


def main():
    args = parse_args()
    data, row_count = kegg_to_alt_id(args.input)
    write_to_csv(args.output, data, row_count)


def kegg_to_alt_id(data_path):
    data = []
    with open(data_path, mode="r") as file:
        row_count = count_lines(file)
        csvReader = csv.reader(file, dialect="excel", delimiter="\t")

        header = csvReader.__next__()
        if header[0] == "ID":
            header[0] = "KEGG_ID"
            header.extend(["UniProt_ID", "NCBI_protein_ID"])
            data.append(header)
        else:
            sys.exit("The file does not contain a valid header, quitting.")

        for line in tqdm(csvReader, desc="Retrieving data", total=row_count-1):
            uniprot_id, ncbi_protein_id = get_alt_id(line[0])
            line.extend([uniprot_id, ncbi_protein_id])
            data.append(line)

    return data, row_count


def get_alt_id(kegg_id):
    kegg = KEGG()
    response = kegg.get("lpl:{}".format(kegg_id))
    kegg_entry = kegg.parse(response)

    try:
        uniprot = kegg_entry["DBLINKS"]["UniProt"]
    except KeyError:
        uniprot = ""

    try:
        NCBIProteinID = kegg_entry["DBLINKS"]["NCBI-ProteinID"]
    except KeyError:
        NCBIProteinID = ""

    return uniprot, NCBIProteinID


def parse_args():
    parser = argparse.ArgumentParser(description="Get UniProt ID and NCBI protein ID.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./data/RNA-Seq-counts.txt",
                        help="(absolute) path for file with KEGG identifiers. First row must be a header and first "
                             "column must contain KEGG identifiers.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./output/alternate_identifiers.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
