import argparse
import sys

from bioservices import KEGG
from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = get_kegg_data(args.input)
    write_to_csv(args.output, data, row_count)


def get_kegg_data(data_path):
    """
    Function that parses a tabular file for KEGG IDs and appends the corresponding nucleotide sequence and pathways to
    the rows in the columns 'nt_seq' and 'pathways'.
    :param data_path:
    text or byte string giving the name (and path) of the tabular file containing KEGG IDs.
    :return:
    nested list [[],[],etc] containing the contents of the input file along with the acquired sequences and pathways.
    Integer representing the number of rows in the input file.
    """
    data = []
    with open(data_path, mode="r") as file:
        row_count = count_lines(file)
        csvReader = csv.reader(file, dialect="excel", delimiter="\t")

        header = csvReader.__next__()
        if header[0] == "KEGG_ID":
            header.extend(["nt_seq", "pathways"])
            data.append(header)
        else:
            sys.exit("The file does not contain a valid header, quitting.")

        for line in tqdm(csvReader, desc="Retrieving data", total=row_count-1):
            nt_seq, pathways = get_data(line[0])
            line.extend([nt_seq.lower(), ";".join(pathways)])
            data.append(line)

    return data, row_count


def get_data(kegg_id):
    """
    Function that uses a KEGG ID to query the KEGG database for the corresponding entry from which it then takes the
    nucleotide sequence and the pathways (if available) and returns them.
    :param kegg_id:
    string giving the identifier of a KEGG database entry.
    :return:
    a string giving the nucleotide sequence and a list containing the pathways.
    """
    kegg = KEGG()
    kegg_entry = kegg.get("lpl:{}".format(kegg_id))
    data = kegg.parse(kegg_entry)

    try:
        nt_seq = data["NTSEQ"]
    except KeyError:
        nt_seq = ""

    try:
        pathways = []
        for pathway in data["PATHWAY"]:
            s = "{0}: {1}".format(pathway, data["PATHWAY"][pathway])
            pathways.append(s.replace(";", "."))
    except KeyError:
        pathways = ""

    return nt_seq, pathways


def parse_args():
    """
    Function that parses commandline strings. Has an --input and --output argument for an input file and output file
    respectively. The input file must be tabular with a header row and the first column must be called 'KEGG_ID' and
    contain valid KEGG identifiers.
    :return:
    Argument parser object with the arguments 'input' and 'output'.
    """
    parser = argparse.ArgumentParser(description="Get NT sequence and KEGG pathways.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./results/alternate_identifiers.csv",
                        help="(absolute) path for file with KEGG identifiers. First row must be a header and first "
                             "column must contain KEGG identifiers.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./results/kegg.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
