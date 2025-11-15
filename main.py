from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from schemas import BandBase, GenreURLChoices, BandWithId, BandCreate

app = FastAPI(
    title="FastAPI",
    description="Sample FastAPI application",
    version="0.1.0",
)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/about")
async def about() -> str:
    return "Experimental fast API"


BANDS = [
    {"id": 1, "name": "Metallica", "genre": "Rock"},
    {"id": 2, "name": "AC/DC", "genre": "Electronic"},
    {"id": 3, "name": "The Beatles", "genre": "Hip-Hop"},
    {"id": 4, "name": "Queen", "genre": "Rock"},
    {
        "id": 5,
        "name": "Nirvana",
        "genre": "Rock",
        "albums": [
            {
                "title": "Nevermind",
                "release_date": "1991-09-24",
                "artist": "Nirvana",
                "price": 10.99,
                "is_available": True,
            }
        ],
    },
    {"id": 6, "name": "Red Hot Chili Peppers", "genre": "Metal"},
    {"id": 7, "name": "The Rolling Stones", "genre": "Electronic"},
    {"id": 8, "name": "The Who", "genre": "Metal"},
    {"id": 9, "name": "Led Zeppelin", "genre": "Rock"},
]


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool = False,
    q: Annotated[str | None, Query(max_length=10)] = None,
) -> list[BandWithId]:
    band_list = [BandWithId(**b) for b in BANDS]
    if genre:
        band_list = [b for b in band_list if b.genre.value.lower() == genre.value]
    if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0]
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list


@app.get("/bands/{band_id}")
async def band(
    band_id: Annotated[int, Path(title="The band ID", openapi_examples="1")],
) -> BandWithId:
    band_list = [BandWithId(**b) for b in BANDS]
    band = next((b for b in band_list if b.id == band_id), None)
    if band is None:
        return HTTPException(status_code=404, detail="Band not found")
    return band


@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandWithId:
    id = BANDS[-1]["id"] + 1
    band = BandWithId(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band
