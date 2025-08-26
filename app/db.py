from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

db_credentials = {
    "drivername": os.getenv("drivername"),
    "host": os.getenv("host"),
    "username": os.getenv("username"),
    "password": os.getenv("password"),
    "port": os.getenv("port"),
    "database": os.getenv("database")
}

DATABASE_URL = URL.create(**db_credentials)

engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
