import re
import sys
from typing import List, Optional, TextIO, Tuple

import pandas


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


def transform_dataframe(
    df: pandas.DataFrame, columns_to_remove: Optional[List[str]] = None
) -> pandas.DataFrame:
    df = df.copy()

    if columns_to_remove:
        df = df.drop(columns_to_remove, axis=1, errors="ignore")

    if "Canonical URL" in df.columns:
        df["Canonical URL"] = df["Canonical URL"].apply(rewrite_canonical_url)

    if "Centres d'intérêt santé" in df.columns:
        cis_list = df["Centres d'intérêt santé"].str.split("|")
        df["Centres d'intérêt santé"] = cis_list.apply(transform_list)
        df[["Age_min", "Age_max"]] = cis_list.apply(extract_ages).apply(pandas.Series)

    return df


COLUMNS_TO_REMOVE = [
    "Auteur courrier",
    "Auteur",
    "A retrouver sur",
    "Afficher dans le Bloc de tags associés",
    "Fuseau horaire",
]


def preprocess_csv(input_file: TextIO, output_file: TextIO) -> None:
    # Hack for reading CSV with duplicate column names
    df = pandas.read_csv(input_file, header=None)
    df = df.rename(columns=df.iloc[0], copy=False).iloc[1:].reset_index(drop=True)
    df = transform_dataframe(df, COLUMNS_TO_REMOVE)
    df.to_csv(output_file, header=True, index=False)


def main(file_name: str) -> None:
    with open(file_name) as input_file:
        preprocess_csv(input_file, sys.stdout)


if __name__ == "__main__":
    main(sys.argv[1])
