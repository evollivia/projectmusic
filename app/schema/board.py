from pydantic import BaseModel


class BoardCreate(BaseModel):
    userid: str
    title: str
    contents: str
