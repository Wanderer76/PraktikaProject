from typing import List

from fastapi import FastAPI
from fastapi import status, Response, Depends
from sqlalchemy.orm import Session

import models
import schemas
import service
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=List[schemas.FilmBase])
def get_films(db: Session = Depends(get_db)):
    return service.get_films_info(db)


@app.get("/{index}", response_model=schemas.Film)
def get_by_index(index: int, db: Session = Depends(get_db)):
    try:
        return service.get_film(db, index)
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/create")
def create_film(film: schemas.FilmCreate, db: Session = Depends(get_db)):
    film = service.create_film(db, film)
    if film is None:
        return Response("Film with same name already exists", status_code=status.HTTP_400_BAD_REQUEST)
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/from_ivi/{film_id}")
def get_from_ivi_by_film_id(film_id: int, db: Session = Depends(get_db)):
    service.get_from_ivi_by_id(db, film_id)
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/from_ivi/year/{year}")
def get_from_ivi_by_year(year: int, db: Session = Depends(get_db)):
    service.get_from_ivi_by_year(db, year)
    return Response(status_code=status.HTTP_201_CREATED)


@app.put("/update/{index}")
def update_film(index: int, film: schemas.FilmEdit, db: Session = Depends(get_db)):
    service.update_film(db, index, film)
    return Response(status_code=status.HTTP_201_CREATED)


@app.put("/comment/add/{index}")
def add_comment_to_film(index: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    try:
        comment = service.add_comment(db, index, comment)
        if comment is None:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        return Response(status_code=status.HTTP_201_CREATED)
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)


@app.delete("/comment/delete/{comment_index}")
def delete_comment(comment_index: int, db: Session = Depends(get_db)):
    service.delete_comment(db, comment_index)
    return Response(status_code=status.HTTP_200_OK)


@app.delete("/delete/{index}")
def delete_film(index: int, db: Session = Depends(get_db)):
    try:
        service.delete_film(db, index)
        return Response(status_code=status.HTTP_200_OK)
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)
