from pydantic import BaseModel


class FilmBase(BaseModel):
    title: str
    
    
class Film(FilmBase):
    class Config:
        orm_mode = True
