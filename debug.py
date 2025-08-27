# debug.py
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print("DATABASE_URL =", database_url)

engine = create_engine(database_url)
with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    db_name = result.fetchone()[0]
    print("Connected to DB:", db_name)
