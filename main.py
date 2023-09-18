import psycopg2
from psycopg2.extras import RealDictCursor
import time
from database import engine
from typing import List
import models,schemas,utils,oauth
from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from schemas import Update_post
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


models.Base.metadata.create_all(bind=engine)


while True:
    try:
        connection = psycopg2.connect(host='localhost',database='API_Development',user='postgres'
                                      ,password='Lahari.2007',cursor_factory=RealDictCursor)
        cur = connection.cursor()
        print("Data Base is Successfully connected")
        break
    except Exception as error:
        print("Failed to connect to data base")
        print("Error : ",error)
        time.sleep(5)

app = FastAPI()



@app.get("/posts",response_model=List[schemas.Post],tags=["Posts"])
def get_post(db: Session = Depends(get_db), user_id : int = Depends(oauth.get_current_user)):
    #cur.execute("SELECT * FROM posts")
    #posts = cur.fetchall()
    print(user_id)
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=201,response_model=schemas.Post,tags=["Posts"])
def create_post(post: schemas.Cretet_post, db: Session = Depends(get_db), user_id : int = Depends(oauth.get_current_user)):
                #user: int = Depends(oauth.get_current_user(oauth.oauth2_scheme))):
    # cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #             (post.title,post.content,post.published))
    # new_post = cur.fetchone()
    # connection.commit()
    print(user_id)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model=schemas.Post,tags=["Posts"])
def get_post(id: int,db: Session = Depends(get_db), user_id : int = Depends(oauth.get_current_user)):
    # cur.execute("""Select * FROM posts WHERE post_id = %s """,(str(id),))
    # post = cur.fetchone()
    print(user_id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        print(post)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["Posts"])
def del_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oauth.get_current_user)):
    # cur.execute("""DELETE FROM posts WHERE post_id = %s RETURNING *""", (str(id),))
    # deleted_post = cur.fetchone()
    # connection.commit()
    print(user_id)
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.Post,tags=["Posts"])
def update_post(id: int,updated_post: Update_post ,db: Session = Depends(get_db), user_id : int = Depends(oauth.get_current_user)):
    # cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING *""",
    #             (post.title,post.content,post.published,str(id)))
    # updated_post = cur.fetchone()
    # connection.commit()
    print(user_id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post("/users", status_code=201,response_model=schemas.Userout,tags=["Users"])
def create_user(user: schemas.Create_user,db: Session = Depends(get_db)):
    # hash the password
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="The email is already in use")
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}",response_model=schemas.Userout,tags=["Users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    return user


@app.post("/login",response_model=schemas.Token)
def login(login_details: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login_details.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    if not utils.verify(login_details.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    access_token = oauth.get_access_token(data={"user_id": user.id })
    token = schemas.Token(access_token=access_token,token_type="bearer")
    return token



