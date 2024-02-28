from fastapi import Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine
from .routers import post, user, auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

