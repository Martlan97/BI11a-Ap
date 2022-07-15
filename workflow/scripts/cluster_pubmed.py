import argparse
import sys

from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = cluster_pubmed(args.input)
    write_to_csv(args.output, data, row_count)


def cluster_pubmed(data_path):
    """
    Function that takes a tabular file containing PubMed and KEGG identifiers and creates a clustering where each PubMed
    ID in the file is listed with all the genes that are associated with it.
    :param data_path:
    text or byte string giving the name (and path) of the tabular file containing PubMed and KEGG identifiers.
    :return:
    nested list [[],[],etc] containing the header and the PubMed identifiers with their associated KEGG identifiers.
    integer representing the number of inner lists in the returned nested list.
    """
    data = [["PubMed_ID", "KEGG_ID"]]
    with open(data_path, mode="r") as file:
        row_count = count_lines(file)
        csvReader = csv.reader(file, dialect="excel", delimiter="\t")

        header = csvReader.__next__()
        if header[0] == "KEGG_ID":
            pubmed_id_index = header.index("PubMed_ID")
        else:
            sys.exit("The file does not contain a valid header, quitting.")

        pubmed_cluster = build_dictionary(csvReader, pubmed_id_index, row_count)
        for key in pubmed_cluster.keys():
            line = [key, ";".join(pubmed_cluster[key])]
            data.append(line)

    return data, len(data)


def build_dictionary(csv_reader, pubmed_id_index, row_count):
    """
    Function that parses a tabular file and builds a dictionary where each key is a PubMed identifier and each value is
    a list of KEGG identifiers.
    :param csv_reader:
    iterator object where each iteration returns a row of the input file.
    :param pubmed_id_index:
    integer representing the location of the PubMed identifier in the row.
    :param row_count:
    integer representing the number of rows in the input file.
    :return:
    dictionary where each key is a PubMed identifier and each value is a list of KEGG identifiers.
    """
    pubmed_cluster = {}
    for line in tqdm(csv_reader, desc="Clustering", total=row_count - 1):
        kegg_id = line[0]
        pubmed_ids = line[pubmed_id_index].split(";")
        for pubmed_id in pubmed_ids:
            if pubmed_id == "":
                pubmed_id = "No articles available"
            if pubmed_cluster.get(pubmed_id):
                pubmed_cluster[pubmed_id].append(kegg_id)
            else:
                pubmed_cluster[pubmed_id] = [kegg_id]

    return pubmed_cluster


def parse_args():
    """
    Function that parses commandline strings. Has an --input and --output argument for an input file and output file
    respectively. The input file must be tabular with a header row and a column called 'PubMed_ID' containing valid
    PubMed identifiers (cells can be left empty).
    :return:
    Argument parser object with the arguments 'input' and 'output'.
    """
    parser = argparse.ArgumentParser(description="Create a summary of which genes appear "
                                                 "in the same PubMed publication",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./results/uniprot.csv",
                        help="(absolute) path for file with PubMed identifiers. First row must be a header.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./results/pubmed_clusters.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
