import csv

from tqdm import tqdm


def count_lines(file):
    """
    Function that counts the lines in a tabular file and returns the result as an integer.
    :param file:
    file object
    :return:
    integer
    """
    csvReader = csv.reader(file, dialect="excel", delimiter="\t")
    row_count = sum(1 for _ in csvReader)
    file.seek(0)
    return row_count


def write_to_csv(out_path, output, row_count):
    """
    Function that creates a tabular file of the supplied data. Uses row_count to provide a progressbar.
    :param out_path:
    text or byte string giving the name (and path) of the file that should be written to.
    :param output:
    nested list [[],[],etc] of the data that is to be written to a file.
    :param row_count:
    integer representing the number of row that will be written (number of nested lists in output).
    :return:
    """
    with open(out_path, mode="w") as file:
        csvWriter = csv.writer(file, dialect="excel", delimiter="\t")
        for line in tqdm(output, desc="Writing to file", total=row_count):
            csvWriter.writerow(line)
