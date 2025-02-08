from googleapiclient.discovery import build

from ..config import settings


async def get_youtube_client():
    """
    YouTube Data API のクライアントを取得する関数
    """
    youtube = build('youtube', 'v3', developerKey=settings.youtube_api_key)
    return youtube
