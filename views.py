import datetime
import fastapi
from fastapi import status, Response
from fastapi import FastAPI

from models import Film, Comment

app = FastAPI()

COMMENTS = [
    Comment(username="user1", comment="ASDFFDASASDFADSADS"),
    Comment(username="user2", comment="AHAHAHAHAHAH"),
    Comment(username="user3", comment="sfad"),
    Comment(username="user4", comment="AHAHAsassssHAHAHAH"),
]

FILMS = [
    Film(name="test film1", year=datetime.date(2000, 1, 1), description="adsffads", comments=COMMENTS[:2]),
    Film(name="test film2", year=datetime.date(2000, 1, 1), description="adsffads", comments=COMMENTS[:3]),
    Film(name="test film3", year=datetime.date(2000, 1, 1), description="adsffads"),
]


@app.get("/")
def get_films():
    return FILMS


@app.get("/{index}")
def get_by_index(index: int):
    try:
        return FILMS[index]
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/create")
def create_film(film: Film):
    for i in FILMS:
        if film.name == i.name:
            return Response("Film with same name already exists", status_code=status.HTTP_400_BAD_REQUEST)
    FILMS.append(film)
    return Response(status_code=status.HTTP_201_CREATED)


@app.put("/update/{index}")
def update_film(index: int, film: Film):
    try:
        old_film = FILMS[index]
        old_film.name = film.name
        old_film.year = film.year
        old_film.description = film.description
        return Response(status_code=status.HTTP_201_CREATED)
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)


@app.put("/comment/add/{index}")
def add_comment_to_film(index: int, comment: Comment):
    try:
        film = FILMS[index]
        if film.comments is None:
            film.comments = [comment]
        else:
            for i in film.comments:
                if i.username == comment.username:
                    i.comment = comment.comment
                    return Response(status_code=status.HTTP_201_CREATED)
            film.comments.append(comment)
        return Response(status_code=status.HTTP_201_CREATED)
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)


@app.delete("/comment/delete/{film_index}/{comment_index}")
def delete_comment(film_index: int, comment_index: int):
    try:
        del FILMS[film_index].comments[comment_index]
        return Response(status_code=status.HTTP_200_OK)
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)


@app.delete("/delete{index}")
def delete_film(index: int):
    try:
        del FILMS[index]
        return Response(status_code=status.HTTP_200_OK)
    except IndexError as e:
        return Response(str(e), status_code=status.HTTP_400_BAD_REQUEST)
