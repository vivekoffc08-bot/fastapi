from pydantic import BaseModel

class book(BaseModel):
    title : str
    body : str  