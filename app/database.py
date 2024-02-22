from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import psycopg2
from psycopg2.extras import RealDictCursor


SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:"
                           f"{settings.database_password}@{settings.database_hostname}/{settings.database_name}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name,
#                             user=settings.database_username,
#                             password=settings.database_password)
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#     print("Database connection was successful!")
# except Exception as error:
#     print("Connection to database failed!")
#     print("Error: ", error)
