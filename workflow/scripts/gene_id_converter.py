import argparse
import sys

from bioservices import KEGG
from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = kegg_to_alt_id(args.input)
    write_to_csv(args.output, data, row_count)


def kegg_to_alt_id(data_path):
    """
    Function that parses a tabular file for KEGG IDs and appends the corresponding UniProt and NCBI IDs to the rows in
    the columns 'UniProt_ID' and 'NCBI_protein_ID'.
    :param data_path:
    text or byte string giving the name (and path) of the tabular file containing KEGG IDs.
    :return:
    nested list [[],[],etc] containing the contents of the input file along with the acquired UniProt and NCBI IDs.
    Integer representing the number of rows in the input file.
    """
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
    """
    Function that uses a KEGG ID to query the KEGG database for the corresponding entry from which it then takes the
    UniProt and NCBI Protein ID (if available) and returns them.
    :param kegg_id:
    string giving the identifier of a KEGG database entry.
    :return:
    two strings giving the identifiers for UniProt and NCBI respectively.
    """
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
    """
    Function that parses commandline strings. Has an --input and --output argument for an input file and output file
    respectively. The input file must be tabular with a header row and the first column must be called 'ID' and
    contain valid KEGG identifiers.
    :return:
    Argument parser object with the arguments 'input' and 'output'.
    """
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
                        default="./results/alternate_identifiers.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
