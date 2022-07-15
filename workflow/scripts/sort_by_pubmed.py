import argparse
import sys

from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = sort(args.input)
    write_to_csv(args.output, data, row_count)


def sort(data_path):
    """
    Function that parses a tabular file for PubMed identifiers and sorts the rows by descending order of the number of
    PubMed identifiers of each gene.
    :param data_path:
    text or byte string giving the name (and path) of the tabular file containing PubMed identifiers.
    :return:
    nested list [[],[],etc] containing the contents of the input file with the inner lists being sorted from most PubMed
    identifiers to least (excluding the header which remains the first inner list in the outer list).
    Integer representing the number of rows in the input file.
    """
    data = []
    to_sort = []
    with open(data_path, mode="r") as file:
        row_count = count_lines(file)
        csvReader = csv.reader(file, dialect="excel", delimiter="\t")

        header = csvReader.__next__()
        if header[0] == "KEGG_ID":
            header.extend(["PubMed_ID_count"])
            data.append(header)
            pubmed_id_index = header.index("PubMed_ID")
        else:
            sys.exit("The file does not contain a valid header, quitting.")

        for line in tqdm(csvReader, desc="Reading file", total=row_count - 1):
            pubmed_ids = line[pubmed_id_index]
            if pubmed_ids:
                pubmed_count = len(pubmed_ids.split(";"))
                line.extend([pubmed_count])
            else:
                line.extend([0])
            to_sort.append(line)

    sorted_data = sorted(to_sort, key=lambda x: x[data[0].index("PubMed_ID_count")], reverse=True)
    data.extend(sorted_data)

    for row in data:
        row.pop(-1)

    return data, row_count


def parse_args():
    """
    Function that parses commandline strings. Has an --input and --output argument for an input file and output file
    respectively. The input file must be tabular with a header row and a column called 'PubMed_ID' containing valid
    PubMed identifiers (cells can be left empty).
    :return:
    Argument parser object with the arguments 'input' and 'output'.
    """
    parser = argparse.ArgumentParser(description="Sort the genes by the number of associated PubMed identifiers",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./results/uniprot.csv",
                        help="(absolute) path for file with PubMed identifiers. First row must be a header.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./results/sorted_by_pubmed.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
