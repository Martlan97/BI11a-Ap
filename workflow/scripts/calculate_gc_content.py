import argparse
import sys

from local_functions.local_functions import *


def main():
    args = parse_args()
    data, row_count = calculate_gc_content(args.input)
    write_to_csv(args.output, data, row_count)


def calculate_gc_content(data_path):
    """
    Function that parses a tabular file for nucleotide sequences and appends the calculated overall GC percentage and
    windowed GC percentages of the sequences to the rows in the columns 'gc_content' and 'gc_content_subsections'.
    :param data_path:
    text or byte string giving the name (and path) of the tabular file containing nucleotide sequences.
    :return:
    nested list [[],[],etc] containing the contents of the input file along with the acquired GC percentages.
    Integer representing the number of rows in the input file.
    """
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
    """
    Function that calculates the windowed GC percentages of a nucleotide sequence by dividing the sequence in
    subsections and then calling get_gc_content() for each subsection and storing the results in a list.
    :param seq:
    string representing a nucleotide sequence.
    :param window:
    integer representing the size the subsections in which the supplied sequence will be divided.
    :return:
    list of integers where each integer represents the GC percentage of a subsection of the supplied sequence.
    """
    result = []
    for i in range(0, len(seq) - window + 1, window):
        subseq = seq[i:i + window]
        result.append(get_gc_content(subseq))
    return result


def get_gc_content(seq):
    """
    Function that calculates the overall GC percentage of a nucleotide sequence by counting the number of 'c' and 'g'
    characters in the input string and then dividing this number by the total number of characters in the string before
    multiplying it by a hundred.
    :param seq:
    string representing a nucleotide sequence.
    :return:
    integer representing the overall GC percentage of the supplied sequence.
    """
    return round((seq.count("c") + seq.count("g")) / len(seq) * 100)


def parse_args():
    """
    Function that parses commandline strings. Has an --input and --output argument for an input file and output file
    respectively. The input file must be tabular with a header row and column called 'nt_seq' containing valid
    nucleotide sequences (cells can be left empty).
    :return:
    Argument parser object with the arguments 'input' and 'output'.
    """
    parser = argparse.ArgumentParser(description="Calculate and visualize the GC content of (a) sequence(s).",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--input",
                        type=str,
                        required=False,
                        default="./results/sorted_by_pubmed.csv",
                        help="(absolute) path for file with NT sequences. First row must be a header.")
    parser.add_argument("--output",
                        type=str,
                        required=False,
                        default="./results/gc_content.csv",
                        help="(absolute) path for the output file.")

    args = parser.parse_args()

    return args


main()
