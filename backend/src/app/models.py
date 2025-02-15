import datetime
from sqlalchemy import Column, String, DateTime

from .database import Base


class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    published_at = Column(DateTime)
    thumbnail = Column(String)


class Video(Base):
    __tablename__ = 'videos'
    video_id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    published_at = Column(DateTime)
    thumbnail = Column(String)
    channel_id = Column(String)
    channel_title = Column(String)
