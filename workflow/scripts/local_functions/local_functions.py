import csv

from tqdm import tqdm


def count_lines(file):
    csvReader = csv.reader(file, dialect="excel", delimiter="\t")
    row_count = sum(1 for _ in csvReader)
    file.seek(0)
    return row_count


def write_to_csv(out_path, output, row_count):
    with open(out_path, mode="w") as file:
        csvWriter = csv.writer(file, dialect="excel", delimiter="\t")
        for line in tqdm(output, desc="Writing to file", total=row_count):
            csvWriter.writerow(line)
