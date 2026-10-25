from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.auth import verify_api_key
from app.repositories import memory
from app.schemas.review import ReviewCreate, ReviewRead

router = APIRouter(
    prefix="",
    tags=["Ulasan Pengunjung"],
    dependencies=[Depends(verify_api_key)],
)


@router.post(
    "/cafes/{cafe_id}/reviews",
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_review(cafe_id: int, payload: ReviewCreate):
    if cafe_id not in memory.cafes:
        raise HTTPException(status_code=404, detail="Kafe tidak ditemukan.")

    values = payload.model_dump()
    overall = round(
        (values["service_rating"] + values["taste_rating"] + values["ambience_rating"]) / 3,
        2,
    )
    review = {
        "id": memory.next_review_id(),
        "cafe_id": cafe_id,
        **values,
        "overall_rating": overall,
    }
    memory.reviews[review["id"]] = review
    return review


@router.get("/cafes/{cafe_id}/reviews", response_model=List[ReviewRead])
def list_cafe_reviews(cafe_id: int):
    if cafe_id not in memory.cafes:
        raise HTTPException(status_code=404, detail="Kafe tidak ditemukan.")
    return [
        review for review in memory.reviews.values()
        if review["cafe_id"] == cafe_id
    ]


@router.get("/reviews/{review_id}", response_model=ReviewRead)
def get_review(review_id: int):
    review = memory.reviews.get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Ulasan tidak ditemukan.")
    return review


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int):
    if review_id not in memory.reviews:
        raise HTTPException(status_code=404, detail="Ulasan tidak ditemukan.")
    del memory.reviews[review_id]
    return None
