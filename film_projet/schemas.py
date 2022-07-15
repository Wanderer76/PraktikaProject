from typing import List, Optional

from pydantic import BaseModel


class CommentBase(BaseModel):
    id: int
    username: str
    comment: str

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    username: str
    comment: str

    class Config:
        orm_mode = True




class FilmCreate(BaseModel):
    name: str
    year: int
    description: str

    class Config:
        orm_mode = True

class FilmEdit(FilmCreate):
    comments: Optional[List[CommentBase]] = None

class FilmBase(BaseModel):
    id: int
    name: str
    year: int
    description: str

    class Config:
        orm_mode = True


class Film(FilmBase):
    comments: Optional[List[CommentBase]] = None

    class Config:
        orm_mode = True
