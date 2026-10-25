from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    visitor_alias: str = Field(min_length=2, max_length=40)
    service_rating: int = Field(ge=1, le=5)
    taste_rating: int = Field(ge=1, le=5)
    ambience_rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=5, max_length=500)


class ReviewRead(BaseModel):
    id: int
    cafe_id: int
    visitor_alias: str
    service_rating: int
    taste_rating: int
    ambience_rating: int
    overall_rating: float
    comment: str
