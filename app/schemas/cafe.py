from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CafeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=2, max_length=80, examples=["Kopi Sudut"])
    area: str = Field(min_length=2, max_length=60, examples=["Samata"])
    address: str = Field(min_length=5, max_length=160)
    category: str = Field(min_length=3, max_length=40, examples=["Coffee Shop"])


class CafeRead(BaseModel):
    id: int
    name: str
    area: str
    address: str
    category: str
    review_count: int = 0
    average_rating: Optional[float] = None


class RatingCard(BaseModel):
    cafe_id: int
    cafe_name: str
    area: str
    review_count: int
    average_rating: Optional[float]
    rating_label: str
