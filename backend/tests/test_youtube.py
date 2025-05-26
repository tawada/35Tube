import pytest

# サンプルテスト: youtube.py のインポート

def test_import_youtube():
    try:
        import backend.src.app.youtube
    except Exception as e:
        pytest.fail(f"youtube.py のインポートに失敗: {e}")
