from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..config import settings

from . import database, models, schemas, youtube

if settings.database_url.startswith("sqlite"):
    # SQLite
    func_random = func.random
else:
    # MySQL
    func_random = func.rand

router = APIRouter(
    prefix="/api",
    tags=["videos"],
)


@router.get("/channels", response_model=Page[schemas.Channel])
async def get_channels(
    db: Session = Depends(database.get_db),
):
    return {
        "items": [db.query(models.Channel).order_by(func_random()).first()],
        "total": None,
        "page": None,
        "size": None,
    }


@router.get("/sponsoredVideos", response_model=Page[schemas.Video])
async def get_sponsored_videos(
    db: Session = Depends(database.get_db),
):
    return {
        "items": db.query(models.Video).order_by(func_random()).limit(1).all(),
        "total": None,
        "page": None,
        "size": None,
    }


@router.get("/recommendedVideos", response_model=Page[schemas.Video])
async def get_recommended_videos(
    db: Session = Depends(database.get_db),
):
    return {
        "items": db.query(models.Video).order_by(func_random()).limit(3).all(),
        "total": None,
        "page": None,
        "size": None,
    }


@router.get("/search", response_model=Page[schemas.Video])
async def search(
    query: str,
    youtube_client=Depends(youtube.get_youtube_client),
    db: Session = Depends(database.get_db),
):
    response = youtube_client.search().list(
        part='snippet',
        q=query,
        maxResults=5,
        type='video'
    ).execute()

    total = response.get('pageInfo', {}).get('totalResults', 0)
    size = response.get('pageInfo', {}).get('resultsPerPage', 0)
    page = 1

    items = []

    next_page_token = response.get('nextPageToken')
    videos = []
    channels = []
    for item in response.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            video = models.Video(
                video_id=item['id']['videoId'],
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                thumbnail=item['snippet']['thumbnails']['high']['url'],
                channel_title=item['snippet']['channelTitle'],
            )
            videos.append(video)
        elif item['id']['kind'] == 'youtube#channel':
            channel = models.Channel(
                channel_id=item['id']['channelId'],
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                thumbnail=item['snippet']['thumbnails']['high']['url'],
            )
            channels.append(channel)
        else:
            continue


    # すでに登録されている動画とチャンネルを取得
    videos_in_db = db.query(models.Video).filter(models.Video.video_id.in_([video.video_id for video in videos])).all()
    channels_in_db = db.query(models.Channel).filter(models.Channel.channel_id.in_([channel.channel_id for channel in channels])).all()

    # 未登録の動画を登録
    unregistered_videos = [video for video in videos if video.video_id not in [video_in_db.video_id for video_in_db in videos_in_db]]
    # 未登録のチャンネルを登録
    unregistered_channels = [channel for channel in channels if channel.channel_id not in [channel_in_db.channel_id for channel_in_db in channels_in_db]]

    db.add_all(unregistered_videos)
    db.add_all(unregistered_channels)
    db.commit()
    for video in unregistered_videos:
        db.refresh(video)

    items.extend(videos_in_db)
    items.extend(unregistered_videos)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
    }


@router.get("/video", response_model=schemas.Video)
async def get_video(
    video_id: str,
    db: Session = Depends(database.get_db),
):
    video = db.query(models.Video).filter(models.Video.video_id == video_id).first()
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return video


@router.get("/loadVideo", response_model=schemas.Video)
async def get_video(
    video_id: str,
    db: Session = Depends(database.get_db),
):
    video = db.query(models.Video).filter(models.Video.video_id == video_id).first()
    if video is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return video


@router.get("/comments", response_model=Page[schemas.Comment])
async def get_comments(
    video_id: str,
    next_page_token: str = None,
    youtube_client=Depends(youtube.get_youtube_client),
):
    response = await youtube.get_comments(youtube_client, video_id, next_page_token)
    total = response.get('pageInfo', {}).get('totalResults', 0)
    size = response.get('pageInfo', {}).get('resultsPerPage', 0)
    page = 1
    items = response.get('items', [])

    # キャメルケースをスネークケースに変換
    for item in items:
        item['comment_id'] = item['id']
        item['like_count'] = item['snippet']['topLevelComment']['snippet']['likeCount']
        item['published_at'] = item['snippet']['topLevelComment']['snippet']['publishedAt']
        item['text_display'] = item['snippet']['topLevelComment']['snippet']['textDisplay']
        item['author_display_name'] = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        item['author_profile_image_url'] = item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
        del item['id']
        del item['snippet']

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
    }
