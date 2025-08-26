from app.db import Base
from sqlalchemy import Column, JSON, BIGINT, Boolean, DateTime, func, ForeignKey

class Game(Base):
    __tablename__ = "game"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    player_id = Column(BIGINT, ForeignKey("player.id"), unique=True, nullable=False)

    is_player_turn = Column(Boolean, nullable=False, default=True)

    board = Column(JSON, nullable=False)
    player1_rack = Column(JSON, nullable=True)
    player2_rack = Column(JSON, nullable=True)
    is_human_vs_human = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
