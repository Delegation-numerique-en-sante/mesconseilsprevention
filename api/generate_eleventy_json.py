import json
from itertools import product
from pathlib import Path
from typing import Literal

import httpx


def make_row(sexe: str, age: int) -> dict:
    r = httpx.get(
        "http://127.0.0.1:8001/SanteFr/Articles.json",
        params={
            "_shape": "objects",
            "_labels": "on",
            "Age_max__gte": age,
            "Age_min__lte": age,
            "Sexe__arraycontains": sexe,
        },
    )
    return {"sexe": sexe, "age": age, "data": r.json()}


data = [make_row(sexe, age) for sexe, age in product(["femmes", "hommes"], range(99))]
eleventy_data = Path("../html/_data")
eleventy_data.mkdir(exist_ok=True)
(eleventy_data / "profiles.json").write_text(json.dumps(data))
