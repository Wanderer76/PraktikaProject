import datetime
from typing import List, Union, Optional

from pydantic import BaseModel


class Comment(BaseModel):
    username: str
    comment: str


class Film(BaseModel):
    name: str
    year: datetime.date
    description: str
    comments: Optional[List[Comment]] = None

    class Config:
        orm_mode = True
