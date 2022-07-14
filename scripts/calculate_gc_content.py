import argparse
import sys

from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = calculate_gc_content(args.input)
    write_to_csv(args.output, data, row_count)


def calculate_gc_content(data_path):
    data = []
    with open(data_path, mode="r") as file:
        row_count = count_lines(file)
        csvReader = csv.reader(file, dialect="excel", delimiter="\t")

        header = csvReader.__next__()
        if header[0] == "KEGG_ID":
            header.extend(["gc_content", "gc_content_subsections"])
            data.append(header)
            nt_seq_index = header.index("nt_seq")
        else:
            sys.exit("The file does not contain a valid header, quitting.")

        for line in tqdm(csvReader, desc="Calculating GC", total=row_count - 1):
            seq = line[nt_seq_index]
            if seq:
                gc_content = get_gc_content(seq)
                gc_content_subsections = get_gc_content_subsection(seq)
                line.extend([gc_content, ";".join("{0}".format(n) for n in gc_content_subsections)])
            else:
                line.extend(["", ""])
            data.append(line)

    return data, row_count


def get_gc_content_subsection(seq, window=10):
    result = []
    for i in range(0, len(seq) - window + 1, window):
        subseq = seq[i:i + window]
        result.append(get_gc_content(subseq))
    return result


def get_gc_content(seq):
    return round((seq.count("c") + seq.count("g")) / len(seq) * 100)


def parse_args():
    parser = argparse.ArgumentParser(description="Calculate and visualize the GC content of (a) sequence(s).",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./output/sorted_by_pubmed.csv",
                        help="(absolute) path for file with NT sequences. First row must be a header.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./output/gc_content.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
