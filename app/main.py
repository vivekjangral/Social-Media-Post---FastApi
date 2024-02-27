from fastapi import Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database = 'fastapi',
            user = 'postgres',
            password = '0p3n1t',
            cursor_factory = RealDictCursor
        )
        cursor = conn.cursor()
        print("Connected to the database successfully")
        break
    except Exception as error:
        print("Could not connect to the database", error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{post_id}", response_model=list[schemas.Post])
async def post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
    delete_post = cursor.fetchone()
    conn.commit()
    if not delete_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, update_post: schemas.UpdatePost, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # existing_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    existing_post = post_query.first()
    if not existing_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, post_id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)
    return existing_post

@app.get("/posts")
async def posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
