from typing import Optional, Tuple

from app.repositories import memory


def cafe_review_summary(cafe_id: int) -> Tuple[int, Optional[float]]:
    matching = [item for item in memory.reviews.values() if item["cafe_id"] == cafe_id]
    if not matching:
        return 0, None
    average = sum(item["overall_rating"] for item in matching) / len(matching)
    return len(matching), round(average, 2)


def rating_label(average: Optional[float]) -> str:
    if average is None:
        return "Belum ada ulasan"
    if average >= 4.5:
        return "Favorit pengunjung"
    if average >= 3.5:
        return "Layak dicoba"
    if average >= 2.5:
        return "Perlu dipertimbangkan"
    return "Butuh evaluasi"
