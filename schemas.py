from datetime import date
from enum import Enum
from pydantic import BaseModel


class GenerateURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip_hop'


class Album(BaseModel):
    title: str
    release_date: date
    artist: str
    price: float
    is_available: bool = True


class Band(BaseModel):
    band_id: int
    name: str
    genre: str
    albums: list[Album] = []
