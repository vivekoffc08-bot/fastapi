from typing import List
from fastapi import FastAPI , Depends , status , Response , HTTPException
from . import schemas
from . import models    
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
 
app = FastAPI()



models.Base.metadata.create_all(engine)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally : 
        db.close()
    

@app.post('/blog', status_code = status.HTTP_201_CREATED, response_model=schemas.responseBlog)
def create(request : schemas.Blog, db : Session = Depends(get_db)):
 
    new_blog = models.Blog(title= request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return f'New blog successfully added {request.title}'



@app.get('/blogs', response_model=List[schemas.responseBlog])
def getAllBlogs(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
    


@app.get('/blog/{id}', status_code = 200)
def getBlog(id : int ,response : Response ,db : Session = Depends(get_db)):

     blog =  db.query(models.Blog).filter(models.Blog.id == id).first()
     if blog :
        return blog
     else :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id  {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f"Blog not found with id {id}"}




@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED)
def update(request : schemas.Blog,  id : int , db : Session = Depends(get_db)):
    blog_query =  db.query(models.Blog).filter(models.Blog.id == id)
    if blog_query.first():
        blog_query.update(request.dict())
        db.commit()
    else :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog with id  {id} is not available")
    return f'updated blog with id {id} successfully'




@app.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT)
def destroy(id: int, db :Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return f"blog {blog} successfully deleted "



@app.post('/user', status_code = status.HTTP_201_CREATED)
def createUser(request : schemas.User, db : Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)

    newUser = models.User(username = request.username, age = request.age, role = request.role, password = hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return  f"User {newUser.username} successfully created"


@app.get('/user', status_code= status.HTTP_200_OK, response_model= List[schemas.responseUser])
def getAllUsers( db : Session = Depends(get_db)):
    Users = db.query(models.User).all()
    if not Users :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Users not available")
    else :
        return Users




@app.delete('/user/{id}')
def deleteUser(id : int ,db :Session= Depends(get_db)):
    userQuery = db.query(models.User).filter(models.User.id == id)
    if not userQuery.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "No users found!")
    else :
        userQuery.delete(synchronize_session= False)
        db.commit()
        return f"User {id} successfully deleted"




