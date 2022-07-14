import argparse
import sys

from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = cluster_pubmed(args.input)
    write_to_csv(args.output, data, row_count)


def cluster_pubmed(data_path):
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
    parser = argparse.ArgumentParser(description="Create a summary of which genes appear "
                                                 "in the same PubMed publication",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./output/uniprot.csv",
                        help="(absolute) path for file with PubMed identifiers. First row must be a header.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./output/pubmed_clusters.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
