from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from .db import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    intent = Column(String, nullable=False)
    user_story = Column(Text, nullable=False)
    acceptance_criteria = Column(JSON, nullable=False)
