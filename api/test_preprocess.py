def test_transform_list():
    from preprocess import transform_list

    assert (
        transform_list(
            [
                "La santé des adolescents (11 à 17 ans)",
                "La santé des jeunes adultes (18 à 35 ans)",
                "La santé des adultes (35 à 55 ans)",
            ]
        )
        == '["La santé des adolescents (11 à 17 ans)","La santé des jeunes adultes (18 à 35 ans)","La santé des adultes (35 à 55 ans)"]'
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
