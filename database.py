# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database
from constants import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = Database(DATABASE_URL)


# You can import get_db in other modules where you need it.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
