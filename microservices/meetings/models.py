from time import time
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY, DateTime
from database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category_id = Column(Integer)
    category_name = Column(Integer)
    participanges_username: Column(ARRAY(str))
    duration_min = Column(Integer, default=60)
    date: Column(DateTime(timezone=True))

