import requests
from sqlalchemy.orm import Session

import models
import schemas


def get_films_info(db: Session):
    return db.query(models.Film).all()


def get_film(db: Session, film_id: int):
    return db.query(models.Film).get(film_id)


def create_film(db: Session, film: schemas.FilmCreate):
    if db.query(models.Film).filter(models.Film.name == film.name).first():
        return None
    db_user = models.Film(name=film.name, year=film.year, description=film.description)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_film(db: Session, id: int, film: schemas.FilmEdit):
    old_film: models.Film = db.query(models.Film).filter(models.Film.id == id).first()
    if old_film is None:
        return None
    old_film.name = film.name
    old_film.year = film.year
    old_film.description = film.description
    db.refresh(old_film)
    return old_film


def delete_film(db: Session, film_id: int):
    db.delete(db.get(models.Film, film_id))
    db.commit()


def add_comment(db: Session, film_id: int, comment: schemas.CommentCreate):
    if db.query(models.Film).filter(models.Film.id == film_id).first() is None:
        return None

    comment_db = db.query(models.Comment) \
        .filter(models.Comment.username == comment.username) \
        .first()

    if comment_db is not None:
        comment_db.comment = comment.comment
    else:
        comment_db = models.Comment(
            username=comment.username,
            comment=comment.comment,
            film_id=film_id
        )
        db.add(comment_db)

    db.commit()
    db.refresh(comment_db)

    return comment_db


def delete_comment(db: Session, comment_index: int):
    db.delete(db.get(models.Comment, comment_index))
    db.commit()


def get_from_ivi_by_id(db: Session, film_id: int):
    url = f"https://api2.ivi.ru/mobileapi/videoinfo/v7/?id={film_id}&fields=id,title,year,description&session_data=.eJxVjEsKwzAMBe_idTDyR5Ldy3jRmGBIiPEHCqV3j-gqWT14zMxXrbOPtLVz1pQ_tbS8qpch5EA"
    data = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36"
    })
    params = data.json()['result']
    if not db.query(models.Film).filter(models.Film.name == params['title']).first():
        film = models.Film(name=params['title'], year=params['year'], description=params['description'])
        db.add(film)
        db.commit()


def get_from_ivi_by_year(db: Session, year: int):
    url = f"https://api2.ivi.ru/mobileapi/catalogue/v7/?category=14&year_from={year}&year_to={year}&from=30&to=59&withpreorderable=true&app_version=870&session=31b256774785852540155946_1673692316-0ZskcU3rXzbQEFq-_KMVtrg&session_data=eyJkdXN0X2dyb3VwX2V4cGlyZWQiOjE2NTc4ODU1MTIuMTE3OTc5LCJ1aWQiOjQ3ODU4NTI1NDAxNTU5NDZ9.YtFFOA._XsX7rcCOaFhG8XRjvmZthpZyyc"
    data = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36"
    })
    params = data.json()['result']
    for i in params:
        if not db.query(models.Film).filter(models.Film.name == i['title']).first():
            film = models.Film(name=i['title'], year=year, description=i['description'])
            db.add(film)
        else:
            continue
    db.commit()
