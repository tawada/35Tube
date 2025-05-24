import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine
from app import models

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # テスト用DBにテーブルを作成
    Base.metadata.create_all(bind=engine)
    yield
    # テスト後にテーブルを削除したい場合は下記を有効化
    # Base.metadata.drop_all(bind=engine)

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
