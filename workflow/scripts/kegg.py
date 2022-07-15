import argparse
import sys

from bioservices import KEGG
from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = get_kegg_data(args.input)
    write_to_csv(args.output, data, row_count)


def get_kegg_data(data_path):
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
