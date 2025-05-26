import pytest

# サンプルテスト: routers.py のインポート

def test_import_routers():
    try:
        import backend.src.app.routers
    except Exception as e:
        pytest.fail(f"routers.py のインポートに失敗: {e}")
