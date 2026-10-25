from itertools import count
from typing import Any, Dict

cafes: Dict[int, Dict[str, Any]] = {}
reviews: Dict[int, Dict[str, Any]] = {}
_cafe_ids = count(1)
_review_ids = count(1)


def next_cafe_id() -> int:
    return next(_cafe_ids)


def next_review_id() -> int:
    return next(_review_ids)


def reset_store() -> None:
    """Digunakan oleh test agar setiap tes mulai dari kondisi bersih."""
    global cafes, reviews, _cafe_ids, _review_ids
    cafes = {}
    reviews = {}
    _cafe_ids = count(1)
    _review_ids = count(1)
