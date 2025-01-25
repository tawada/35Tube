from datetime import datetime
from pydantic import BaseModel

class IdSchema(BaseModel):
    kind: str
    videoId: str

class ThumbnailSchema(BaseModel):
    url: str
    width: int
    height: int

class ThumbnailsSchema(BaseModel):
    default: ThumbnailSchema
    medium: ThumbnailSchema
    high: ThumbnailSchema

class SnippetSchema(BaseModel):
    # 時刻を文字列で扱う場合は str に変更する
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: ThumbnailsSchema
    channelTitle: str
    liveBroadcastContent: str
    # 時刻を文字列で扱う場合は str に変更する
    publishTime: datetime

class YouTubeSearchResultSchema(BaseModel):
    kind: str
    etag: str
    id: IdSchema
    snippet: SnippetSchema
