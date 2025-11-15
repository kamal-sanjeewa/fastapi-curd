from datetime import date
from enum import Enum
from pydantic import BaseModel, field_validator


class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'


class GenreChoices(Enum):
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    METAL = 'Metal'
    HIP_HOP = 'Hip-Hop'


class Album(BaseModel):
    title: str
    release_date: date
    artist: str
    price: float
    is_available: bool = True


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []


class BandCreate(BandBase):
    @field_validator("genre", mode="before")
    def title_case_genre(cls, value) -> str:
        return value.title() if isinstance(value, str) else value.value


class BandWithId(BandBase):
    id: int