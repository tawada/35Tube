import datetime
from pydantic import BaseModel


class Channel(BaseModel):
    channel_id: str
    title: str
    description: str
    thumbnail: str


class Comment(BaseModel):
    comment_id: str
    text_display: str
    like_count: int
    published_at: datetime.datetime
    author_display_name: str
    author_profile_image_url: str


class Video(BaseModel):
    video_id: str
    title: str
    description: str
    thumbnail: str
    channel_title: str

