from app.db import Base
from sqlalchemy import Column, BIGINT, Boolean, DateTime, func, ForeignKey, Integer
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import JSONB

class Game(Base):
    __tablename__ = "game"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    player_id = Column(BIGINT, ForeignKey("player.id"), unique=True, nullable=False)

    is_player_turn = Column(Boolean, nullable=False, default=True)

    board = Column(JSONB, nullable=False)
    player1_rack = Column(JSONB, nullable=True)
    player2_rack = Column(JSONB, nullable=True)
    is_human_vs_human = Column(Boolean, nullable=False, default=False)
    human_score = Column(Integer, default=0)
    computer_score = Column(Integer, default=0)
    
    played_words = Column(MutableList.as_mutable(JSONB), default=list)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
