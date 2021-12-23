from pandas._testing import assert_frame_equal
import pandas


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


def test_extract_ages():
    from preprocess import extract_ages

    assert (
        extract_ages(
            [
                "La santé des adolescents (11 à 17 ans)",
                "La santé des jeunes adultes (18 à 35 ans)",
                "La santé des adultes (35 à 55 ans)",
            ]
        )
        == (11, 55)
    )


def test_rewrite_canonical_url():
    from preprocess import rewrite_canonical_url

    assert (
        rewrite_canonical_url("https://santefr.production.asipsante.fr/endometriose-1")
        == "https://www.sante.fr/endometriose-1"
    )


def test_extract_ages_without_ages_returns_zeros():
    from preprocess import extract_ages

    assert extract_ages(["La santé des personnes âgées (85 ans et plus)"]) == (0, 0)


def test_transform_dataframe():
    from preprocess import transform_dataframe

    result = transform_dataframe(
        pandas.DataFrame(
            [
                {
                    "Centres d'intérêt santé": (
                        "La santé des adolescents (11 à 17 ans)|"
                        "La santé des jeunes adultes (18 à 35 ans)|"
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
                "Centres d'intérêt santé": (
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
    assert_frame_equal(result, expected)


def test_transform_dataframe_with_removed_columns():
    from preprocess import transform_dataframe

    result = transform_dataframe(
        pandas.DataFrame(
            [
                {
                    "Centres d'intérêt santé": (
                        "La santé des adolescents (11 à 17 ans)|"
                        "La santé des jeunes adultes (18 à 35 ans)|"
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
                "Centres d'intérêt santé": (
                    "["
                    '"La santé des adolescents (11 à 17 ans)",'
                    '"La santé des jeunes adultes (18 à 35 ans)",'
                    '"La santé des adultes (35 à 55 ans)"'
                    "]"
                ),
                "Age_min": 11,
                "Age_max": 55,
            }
        ]
    )
    assert_frame_equal(result, expected)


def test_transform_dataframe_without_keys_is_noop():
    from preprocess import transform_dataframe

    result = transform_dataframe(pandas.DataFrame([{"foo": "bar"}]))
    expected = pandas.DataFrame([{"foo": "bar"}])
    assert_frame_equal(result, expected)
