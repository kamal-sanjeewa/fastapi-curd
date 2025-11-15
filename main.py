from fastapi import FastAPI
from schemas import Band, GenerateURLChoices
from fastapi import HTTPException

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
    {"band_id": 1, "name": "Metallica", "genre": "Rock"},
    {"band_id": 2, "name": "AC/DC", "genre": "Electronic"},
    {"band_id": 3, "name": "The Beatles", "genre": "Hip-Hop"},
    {"band_id": 4, "name": "Queen", "genre": "Rock"},
    {"band_id": 5, "name": "Nirvana", "genre": "Rock", "albums": [{
        "title": "Nevermind",
        "release_date": "1991-09-24",
        "artist": "Nirvana",
        "price": 10.99,
        "is_available": True
    }]},
    {"band_id": 6, "name": "Red Hot Chili Peppers", "genre": "Metal"},
    {"band_id": 7, "name": "The Rolling Stones", "genre": "Electronic"},
    {"band_id": 8, "name": "The Who", "genre": "Metal"},
    {"band_id": 9, "name": "Led Zeppelin", "genre": "Rock"},
]


@app.get("/bands")
async def bands(genre: GenerateURLChoices | None = None, has_albums: bool = False ) -> list[Band]:
    band_list = [Band(**b) for b in BANDS]
    if genre:
        band_list = [b for b in band_list if b.genre.lower() == genre.value]
    if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0]

    return band_list


@app.get("/band/{band_id}")
async def band(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b["band_id"] == band_id), None)
    if band is None:
        return HTTPException(status_code=404, detail="Band not found")
    return band