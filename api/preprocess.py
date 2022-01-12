import operator
import re
import sys
from functools import reduce
from typing import Iterable, List, Optional, Set, TextIO, Tuple, Union

import pandas
from pandas._libs.missing import NAType


IntOrNA = Union[int, NAType]
# On définit un âge maximal pour pouvoir faire des requêtes bornées.
MAX_AGE = 999


def rewrite_canonical_url(canonical_url: str) -> str:
    return canonical_url.replace("santefr.production.asipsante.fr", "www.sante.fr")


def format_list(data: Iterable[str]) -> str:
    return "[" + ",".join(f'"{item}"' for item in data) + "]"


def extract_age_range(item: str) -> Tuple[IntOrNA, IntOrNA]:
    if not item:
        return (pandas.NA, pandas.NA)

    # "La santé des adolescents (11 à 17 ans)" => (11, 17)
    # "Informations pour préserver sa santé (25 - 35 ans)" => (25, 35)
    match = re.search(r"(?P<min>\d+) (à|et|-) (?P<max>\d+) ans?", item)
    if match:
        return (int(match.group("min")), int(match.group("max")))

    # "Informations pour préserver sa santé à partir de 65 ans" => (65, MAX_AGE)
    match = re.search(r"à partir de (?P<min>\d+) ans", item)
    if match:
        return (int(match.group("min")), MAX_AGE)

    # "'La santé des personnes âgées (85 ans et plus)'" => (65, MAX_AGE)
    match = re.search(r"(?P<min>\d+) ans et plus", item)
    if match:
        return (int(match.group("min")), MAX_AGE)

    raise ValueError(item)


def extract_age_facets(data: List[str]) -> Tuple[IntOrNA, IntOrNA]:
    all_ages = [extract_age_range(item) for item in data]

    min_ages = [min_age for min_age, _ in all_ages]
    numeric_min_ages = [age for age in min_ages if age is not pandas.NA]
    min_min_age = (
        pandas.NA
        if any(age is pandas.NA for age in min_ages)
        else min(numeric_min_ages)
    )

    max_ages = [max_age for _, max_age in all_ages]
    numeric_max_ages = [age for age in max_ages if age is not pandas.NA]
    max_max_age = (
        pandas.NA
        if any(age is pandas.NA for age in max_ages)
        else max(numeric_max_ages)
    )

    return (min_min_age, max_max_age)


def extract_sex_facet(data: List[str]) -> str:
    return format_list(sorted(union(extract_sex(label) for label in data)))


def union(sets: Iterable[Set]) -> Set:
    return reduce(operator.or_, sets, set())


def extract_sex(text: str) -> Set[str]:
    match = re.search(r"\b([Ff]emmes?|adolescentes|grossesse)\b", text)
    if match:
        return {"femmes"}
    match = re.search(r"\b([Hh]ommes?|adolescents)", text)
    if match:
        return {"hommes"}
    return {"femmes", "hommes"}


def transform_dataframe(
    df: pandas.DataFrame, columns_to_remove: Optional[List[str]] = None
) -> pandas.DataFrame:
    df = df.copy()

    if columns_to_remove:
        df = df.drop(columns_to_remove, axis=1, errors="ignore")

    if "Canonical URL" in df.columns:
        df["Canonical URL"] = df["Canonical URL"].apply(rewrite_canonical_url)

    if "Séquence de vie" in df.columns:
        sdv_list = df["Séquence de vie"].str.split(", ")
        df["Séquence de vie"] = sdv_list.apply(format_list)
        df[["Age_min", "Age_max"]] = (
            sdv_list.apply(extract_age_facets)
            .apply(pandas.Series)
            .astype(dtype=pandas.Int64Dtype())
        )
        df["Sexe"] = sdv_list.apply(extract_sex_facet).apply(pandas.Series)

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
