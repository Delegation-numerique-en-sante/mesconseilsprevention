from pandas._testing import assert_frame_equal
import pandas
import pytest


def test_transform_list():
    from preprocess import transform_list

    assert transform_list(
        [
            "La santé des adolescents (11 à 17 ans)",
            "La santé des jeunes adultes (18 à 35 ans)",
            "La santé des adultes (35 à 55 ans)",
        ]
    ) == (
        "["
        '"La santé des adolescents (11 à 17 ans)",'
        '"La santé des jeunes adultes (18 à 35 ans)",'
        '"La santé des adultes (35 à 55 ans)"'
        "]"
    )


def test_extract_age_facets():
    from preprocess import extract_age_facets

    assert (
        extract_age_facets(
            [
                "La santé des adolescents (11 à 17 ans)",
                "La santé des jeunes adultes (18 à 35 ans)",
                "La santé des adultes (35 à 55 ans)",
            ]
        )
        == (11, 55)
    )


@pytest.mark.parametrize(
    "text,min_,max_",
    [
        ("", pandas.NA, pandas.NA),
        ("Sur la santé entre 11 et 12 ans", 11, 12),
        ("Informations pour préserver sa santé (11 - 12 ans / Femme)", 11, 12),
        ("Informations pour préserver sa santé (59 - 64 ans)", 59, 64),
        ("Informations dédiées à la santé des nourrissons (0 - 1 an)", 0, 1),
        ("Informations pour préserver sa santé à partir de 65 ans", 65, pandas.NA),
        ("La santé des personnes âgées (85 ans et plus)", 85, pandas.NA),
    ],
)
def test_extract_ages_range(text, min_, max_):
    from preprocess import extract_age_range

    assert extract_age_range(text) == (min_, max_)


def test_rewrite_canonical_url():
    from preprocess import rewrite_canonical_url

    assert (
        rewrite_canonical_url("https://santefr.production.asipsante.fr/endometriose-1")
        == "https://www.sante.fr/endometriose-1"
    )


def test_transform_dataframe():
    from preprocess import transform_dataframe

    result = transform_dataframe(
        pandas.DataFrame(
            [
                {
                    "Séquence de vie": (
                        "La santé des adolescents (11 à 17 ans), "
                        "La santé des jeunes adultes (18 à 35 ans), "
                        "La santé des adultes (35 à 55 ans)"
                    ),
                    "Canonical URL": "https://santefr.production.asipsante.fr/endometriose-1",
                }
            ]
        )
    )
    expected = pandas.DataFrame(
        [
            {
                "Séquence de vie": (
                    "["
                    '"La santé des adolescents (11 à 17 ans)",'
                    '"La santé des jeunes adultes (18 à 35 ans)",'
                    '"La santé des adultes (35 à 55 ans)"'
                    "]"
                ),
                "Canonical URL": "https://www.sante.fr/endometriose-1",
                "Age_min": 11,
                "Age_max": 55,
            }
        ]
    )
    expected["Age_min"] = expected["Age_min"].astype("Int64")
    expected["Age_max"] = expected["Age_max"].astype("Int64")
    assert_frame_equal(result, expected)


def test_transform_dataframe_with_removed_columns():
    from preprocess import transform_dataframe

    result = transform_dataframe(
        pandas.DataFrame(
            [
                {
                    "Séquence de vie": (
                        "La santé des adolescents (11 à 17 ans), "
                        "La santé des jeunes adultes (18 à 35 ans), "
                        "La santé des adultes (35 à 55 ans)"
                    ),
                    "Canonical URL": "https://santefr.production.asipsante.fr/endometriose-1",
                }
            ]
        ),
        columns_to_remove=["Canonical URL"],
    )
    expected = pandas.DataFrame(
        [
            {
                "Séquence de vie": (
                    "["
                    '"La santé des adolescents (11 à 17 ans)",'
                    '"La santé des jeunes adultes (18 à 35 ans)",'
                    '"La santé des adultes (35 à 55 ans)"'
                    "]"
                ),
                "Age_min": 11,
                "Age_max": 55,
            }
        ],
    )
    expected["Age_min"] = expected["Age_min"].astype("Int64")
    expected["Age_max"] = expected["Age_max"].astype("Int64")
    assert_frame_equal(result, expected)


def test_transform_dataframe_without_keys_is_noop():
    from preprocess import transform_dataframe

    result = transform_dataframe(pandas.DataFrame([{"foo": "bar"}]))
    expected = pandas.DataFrame([{"foo": "bar"}])
    assert_frame_equal(result, expected)
