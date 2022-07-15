from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    year = Column(Integer)
    description = Column(String)

    comments = relationship("Comment")

    class Config:
        orm_mode = True


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    comment = Column(String)
    film_id = Column(Integer, ForeignKey("films.id"))
