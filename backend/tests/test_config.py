import pytest

# サンプルテスト: config.py のインポート

def test_import_config():
    import os
    # 必須環境変数をダミーでセット
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["YOUTUBE_API_KEY"] = "dummy"
    os.environ["PROJECT_ID"] = "dummy"
    os.environ["LOCATION"] = "dummy"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dummy.json"
    try:
        import importlib
        import backend.src.config
        importlib.reload(backend.src.config)  # 環境変数反映のためリロード
    except Exception as e:
        pytest.fail(f"config.py のインポートに失敗: {e}")
