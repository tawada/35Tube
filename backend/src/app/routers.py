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

router = APIRouter()


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
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        video = db.query(models.Video).filter(models.Video.video_id == video_id).first()
        if video is None:
            video = models.Video(
                video_id=item['id']['videoId'],
                title=item['snippet']['title'],
                description=item['snippet']['description'],
                thumbnail=item['snippet']['thumbnails']['high']['url'],
            )
            db.add(video)
            db.commit()
            db.refresh(video)
        items.append(video)

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
