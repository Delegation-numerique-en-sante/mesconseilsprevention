import csv
import re
import sys
from typing import List, Tuple


def remove_columns(row: dict, columns_to_remove: list) -> dict:
    for fieldname in columns_to_remove:
        row.pop(fieldname)
    return row


def rewrite_canonical_url(canonical_url: str) -> str:
    return canonical_url.replace("santefr.production.asipsante.fr", "www.sante.fr")


def transform_list(data: List[str]) -> str:
    return "[" + ",".join(f'"{cis}"' for cis in data) + "]"


def extract_ages(data: List[str]) -> Tuple[int, int]:
    def _extract_ages(item: str) -> Tuple[int, int]:
        # "La santé des adolescents (11 à 17 ans)" => (11, 17)
        match = re.search(r"\((\d+) à (\d+) ans\)", item)
        if match is None:
            # TODO if the case occurs.
            return (0, 0)
        return (int(match.group(1)), int(match.group(2)))

    all_ages = [_extract_ages(item) for item in data]

    return (
        min(min_age for min_age, _ in all_ages),
        max(max_age for _, max_age in all_ages),
    )


def transform_row(row: dict, columns_to_remove: list) -> dict:
    row = remove_columns(row, columns_to_remove)
    if "Canonical URL" in row:
        row["Canonical URL"] = rewrite_canonical_url(row.get("Canonical URL", ""))
    if "Centres d'intérêt santé" in row:
        cis_list = row["Centres d'intérêt santé"].split("|")
        row["Centres d'intérêt santé"] = transform_list(cis_list)
        age_min, age_max = extract_ages(cis_list)
        row["Age_min"] = age_min
        row["Age_max"] = age_max
    return row


def main(file_name: str) -> None:
    columns_to_remove = [
        "Auteur courrier",
        "Auteur",
        "A retrouver sur",
        "Afficher dans le Bloc de tags associés",
        "Fuseau horaire",
    ]

    with open(file_name) as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or []) + ["Age_min", "Age_max"]
        fieldnames = [
            fieldname for fieldname in fieldnames if fieldname not in columns_to_remove
        ]
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            row = transform_row(row, columns_to_remove)
            writer.writerow(row)


if __name__ == "__main__":
    main(sys.argv[1])
