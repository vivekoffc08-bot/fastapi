from pydantic import BaseModel

class Blog(BaseModel):
    title : str
    body : str

class User(BaseModel):
    username : str
    role : str
    age : int
    password : str


class responseBlog(Blog):
    pass

class responseUser(User):
    pass
