import datetime
from pydantic import BaseModel


class Video(BaseModel):
    video_id: str
    title: str
    description: str
    thumbnail: str
    channel_title: str

