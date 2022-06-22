from abc import ABC
from typing import Any, Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import ARRAY
from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    participants_id: Column(ARRAY(Integer), default=[])
    duration: Column(Integer, default=30)