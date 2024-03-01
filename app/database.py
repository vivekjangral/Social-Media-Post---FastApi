import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database = 'fastapi',
#             user = 'postgres',
#             password = '0p3n1t',
#             cursor_factory = RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Connected to the database successfully")
#         break
#     except Exception as error:
#         print("Could not connect to the database", error)
#         time.sleep(2)