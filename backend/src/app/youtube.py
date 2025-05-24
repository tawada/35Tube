from googleapiclient.discovery import build

from config import settings


async def get_youtube_client():
    """
    YouTube Data API のクライアントを取得する関数
    """
    youtube = build('youtube', 'v3', developerKey=settings.youtube_api_key)
    return youtube


async def get_comments(
    youtube,
    video_id: str,
    next_page_token: str = None,
):
    """
    動画のコメントを取得する関数
    """
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,
        pageToken=next_page_token
    ).execute()
    return response
