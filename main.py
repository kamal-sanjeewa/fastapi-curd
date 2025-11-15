from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query, Depends
from models import BandBase, GenreURLChoices, BandCreate, Album, Band
from contextlib import asynccontextmanager
from db import init_db, get_session
from sqlmodel import Session, select


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="FastAPI",
    description="Sample FastAPI application",
    version="0.1.0",
    lifespan=lifespan
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
    session: Session = Depends(get_session)
) -> list[Band]:
    band_list = session.exec(select(Band)).all()
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
) -> Band:
    band_list = [Band(**b) for b in BANDS]
    band = next((b for b in band_list if b.id == band_id), None)
    if band is None:
        return HTTPException(status_code=404, detail="Band not found")
    return band


@app.post("/bands")
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title=album.title, release_date=album.release_date, band=band
            )
            session.add(album_obj)

    session.commit()
    session.refresh(band)

    return band
