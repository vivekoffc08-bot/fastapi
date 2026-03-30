from fastapi import FastAPI , Depends , status , Response , HTTPException
from . import schemas
from . import models    
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
 
app = FastAPI() 

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally : 
        db.close()
    

@app.post('/blog', status_code = status.HTTP_201_CREATED)
def create(request : schemas.Blog, db : Session = Depends(get_db)):
 
    new_blog = models.Blog(title= request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return f'New blog successfully added {request.title}'



@app.get('/blogs')
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

