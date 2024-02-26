from fastapi import FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return { "Post": new_post,"message": "Post created successfully"}

@app.get("/posts/{post_id}")
async def post(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return {"Post": post}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
    delete_post = cursor.fetchone()
    conn.commit()
    if not delete_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    existing_post = cursor.fetchone()
    if not existing_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, post_id))
    updated_post = cursor.fetchone()
    conn.commit()
    return {"Post": updated_post, "message": "Post updated successfully"}

@app.get("/posts")
async def posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"Posts": posts}
