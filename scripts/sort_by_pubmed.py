import argparse
import sys

from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = sort(args.input)
    write_to_csv(args.output, data, row_count)


def sort(data_path):
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
    parser = argparse.ArgumentParser(description="Sort the genes by the number of associated PubMed identifiers",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./output/uniprot.csv",
                        help="(absolute) path for file with PubMed identifiers. First row must be a header.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./output/sorted_by_pubmed.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
