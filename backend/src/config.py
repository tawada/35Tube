from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """環境変数から設定を読み込む"""
    database_url: str  # 環境変数 DATABASE_URL から読み込まれる
    youtube_api_key: str
    project_id: str
    location: str
    google_application_credentials: str

    class Config:
        env_file = ".env"  # 開発時には.envファイルからも読み込み可能

settings = Settings()
