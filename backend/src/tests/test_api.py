import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Set dummy environment variables to avoid pydantic ValidationError
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["YOUTUBE_API_KEY"] = "dummy"
os.environ["PROJECT_ID"] = "dummy"
os.environ["LOCATION"] = "dummy"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dummy.json"

from app import app
from app.database import Base, engine
from fastapi_pagination import add_pagination
from app.models import Channel, Video
from sqlalchemy.orm import Session

# テスト用DBにテーブル作成
Base.metadata.create_all(bind=engine)
# テスト用DBにダミーデータを挿入
with Session(engine) as session:
    channel = Channel(channel_id="test_channel", title="Test Channel", description="desc", published_at=None, thumbnail="thumb.png")
    video = Video(video_id="test_video", title="Test Video", description="desc", published_at=None, thumbnail="thumb.png", channel_id="test_channel", channel_title="Test Channel")
    session.add(channel)
    session.add(video)
    session.commit()
# FastAPI appにpaginationを追加
add_pagination(app)

import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_channels():
    response = client.get("/api/channels")
    assert response.status_code == 200
    assert "items" in response.json()

def test_get_sponsored_videos():
    response = client.get("/api/sponsoredVideos")
    assert response.status_code == 200
    assert "items" in response.json()

def test_get_recommended_videos():
    response = client.get("/api/recommendedVideos")
    assert response.status_code == 200
    assert "items" in response.json()
