import re
import sys
from typing import List, Optional, TextIO, Tuple, Union

import pandas
from pandas._libs.missing import NAType


IntOrNA = Union[int, NAType]


def rewrite_canonical_url(canonical_url: str) -> str:
    return canonical_url.replace("santefr.production.asipsante.fr", "www.sante.fr")


def transform_list(data: List[str]) -> str:
    return "[" + ",".join(f'"{cis}"' for cis in data) + "]"


def extract_age_range(item: str) -> Tuple[IntOrNA, IntOrNA]:
    if not item:
        return (pandas.NA, pandas.NA)

    # "La santé des adolescents (11 à 17 ans)" => (11, 17)
    # "Informations pour préserver sa santé (25 - 35 ans)" => (25, 35)
    match = re.search(r"(?P<min>\d+) (à|et|-) (?P<max>\d+) ans?", item)
    if match:
        return (int(match.group("min")), int(match.group("max")))

    # "Informations pour préserver sa santé à partir de 65 ans" => (65, pandas.NA)
    match = re.search(r"à partir de (?P<min>\d+) ans", item)
    if match:
        return (int(match.group("min")), pandas.NA)

    # "'La santé des personnes âgées (85 ans et plus)'" => (65, pandas.NA)
    match = re.search(r"(?P<min>\d+) ans et plus", item)
    if match:
        return (int(match.group("min")), pandas.NA)

    raise ValueError(item)


def extract_age_facets(data: List[str]) -> Tuple[IntOrNA, IntOrNA]:
    all_ages = [extract_age_range(item) for item in data]

    min_ages = [min_age for min_age, _ in all_ages]
    min_min_ages = min(age for age in min_ages if age is not pandas.NA)

    max_ages = [max_age for _, max_age in all_ages]
    max_max_ages = max(age for age in max_ages if age is not pandas.NA)

    return (
        pandas.NA if any(age is pandas.NA for age in min_ages) else min_min_ages,
        pandas.NA if any(age is pandas.NA for age in max_ages) else max_max_ages,
    )


def transform_dataframe(
    df: pandas.DataFrame, columns_to_remove: Optional[List[str]] = None
) -> pandas.DataFrame:
    df = df.copy()

    if columns_to_remove:
        df = df.drop(columns_to_remove, axis=1, errors="ignore")

    if "Canonical URL" in df.columns:
        df["Canonical URL"] = df["Canonical URL"].apply(rewrite_canonical_url)

    if "Séquence de vie" in df.columns:
        cis_list = df["Séquence de vie"].str.split(", ")
        df["Séquence de vie"] = cis_list.apply(transform_list)
        df[["Age_min", "Age_max"]] = (
            cis_list.apply(extract_age_facets)
            .apply(pandas.Series)
            .astype(dtype=pandas.Int64Dtype())
        )

    return df


COLUMNS_TO_REMOVE = [
    "Auteur courrier",
    "Auteur",
    "A retrouver sur",
    "Afficher dans le Bloc de tags associés",
    "Fuseau horaire",
]


def preprocess_excel(input_filename: str, output_file: TextIO) -> None:
    df = pandas.read_excel(input_filename).fillna("")
    df.rename(columns={"Unnamed: 1": "Canonical URL"}, inplace=True)
    df = transform_dataframe(df, COLUMNS_TO_REMOVE)
    df.to_csv(output_file, header=True, index=False)


def main(file_name: str) -> None:
    preprocess_excel(file_name, sys.stdout)


if __name__ == "__main__":
    main(sys.argv[1])
