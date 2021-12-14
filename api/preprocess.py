import csv
import sys


def transform_list(data: str) -> str:
    return "[" + ",".join(f'"{cis}"' for cis in data.split("|")) + "]"


def main(file_name):
    with open(file_name) as f:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            row["Centres d'intérêt santé"] = transform_list(
                row.get("Centres d'intérêt santé")
            )
            writer.writerow(row)


if __name__ == "__main__":
    main(sys.argv[1])
