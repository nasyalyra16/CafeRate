from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.dependencies.auth import verify_api_key
from app.repositories import memory
from app.schemas.cafe import CafeCreate, CafeRead, RatingCard
from app.services.rating import cafe_review_summary, rating_label

router = APIRouter(
    prefix="/cafes",
    tags=["Katalog Kafe"],
    dependencies=[Depends(verify_api_key)],
)


def _cafe_read(cafe: dict) -> CafeRead:
    count, average = cafe_review_summary(cafe["id"])
    return CafeRead(**cafe, review_count=count, average_rating=average)


@router.post("", response_model=CafeRead, status_code=status.HTTP_201_CREATED)
def create_cafe(payload: CafeCreate):
    duplicate = any(
        item["name"].casefold() == payload.name.casefold()
        and item["area"].casefold() == payload.area.casefold()
        for item in memory.cafes.values()
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Kafe dengan nama yang sama sudah terdaftar di area tersebut.",
        )

    cafe = {"id": memory.next_cafe_id(), **payload.model_dump()}
    memory.cafes[cafe["id"]] = cafe
    return _cafe_read(cafe)


@router.get("", response_model=List[CafeRead])
def list_cafes(area: Optional[str] = Query(default=None, min_length=2, max_length=60)):
    items = list(memory.cafes.values())
    if area:
        items = [c for c in items if c["area"].casefold() == area.strip().casefold()]
    return [_cafe_read(cafe) for cafe in items]


@router.get("/{cafe_id}", response_model=CafeRead)
def get_cafe(cafe_id: int):
    cafe = memory.cafes.get(cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="Kafe tidak ditemukan.")
    return _cafe_read(cafe)


@router.get("/{cafe_id}/rating-card", response_model=RatingCard)
def get_rating_card(cafe_id: int):
    cafe = memory.cafes.get(cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="Kafe tidak ditemukan.")
    count, average = cafe_review_summary(cafe_id)
    return RatingCard(
        cafe_id=cafe_id,
        cafe_name=cafe["name"],
        area=cafe["area"],
        review_count=count,
        average_rating=average,
        rating_label=rating_label(average),
    )
