# check_tables.py
from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    inspector = inspect(conn)
    tables = inspector.get_table_names(schema="public")
    print("Tables in public schema:", tables)
