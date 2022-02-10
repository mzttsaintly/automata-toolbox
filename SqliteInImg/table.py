import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, BLOB
from .sqlite_link import Base


class Setu(Base):
    __tablename__ = "setu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Group_id = Column(Integer)
    user_id = Column(Integer)
    image = Column(String(32))
    type = Column(String(32))
    time = Column(DateTime, default=datetime.datetime.now())


class ImageInformation(Base):
    __tablename__ = "image_information"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_name = Column(String(32))
    character = Column(String(32))
    work_name = Column(String(32))
    tags = Column(String(32))
    ero = Column(Integer)
