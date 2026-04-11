from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings

import psycopg2
from psycopg2.extras import RealDictCursor
import time


# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pokemongo89@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""The code below is an alternative way to connect to the database using psycopg2,
  which is a lower-level library for interacting with PostgreSQL databases.
  However, since we are using SQLAlchemy as our ORM (Object-Relational Mapping) tool,
  we don't need to use psycopg2 directly in our application code.
  SQLAlchemy will handle the database connections and queries for us,
  allowing us to work with Python objects instead of raw SQL queries.
  Therefore, the code for connecting to the database using psycopg2
  has been commented out and is not necessary for our application to function properly."""

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                             password='pokemongo89', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as error:
#         print ('Connection to database failed!')
#         print('Error:', error)
#         time.sleep(3)