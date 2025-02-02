import os
from googleapiclient.discovery import build

API_KEY = os.environ['YOUTUBE_API_KEY']


async def get_youtube_client():
    """
    YouTube Data API のクライアントを取得する関数
    """
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    return youtube
