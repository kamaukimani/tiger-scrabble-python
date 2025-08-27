from app.db import Base
from sqlalchemy import Column, String, BIGINT, DateTime, func

class Player(Base):
    __tablename__ = "player"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    country = Column(String, nullable=False)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
