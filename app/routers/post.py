from typing import Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from .. import schemas, models
from ..database import  get_db
from sqlalchemy.orm import Session
from . import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print("current_user: ", current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model=schemas.Post)
async def post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return post

@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
    # delete_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == post_id).delete()
    if not delete_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    if post.owner_id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, update_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # existing_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    existing_post = post_query.first()
    if not existing_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, post_id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    if existing_post.owner_id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)
    return existing_post

@router.get("/")
async def posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
                limit: int = 3, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


