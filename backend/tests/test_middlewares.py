import pytest

# サンプルテスト: middlewares.py のインポート

def test_import_middlewares():
    try:
        import backend.src.app.middlewares
    except Exception as e:
        pytest.fail(f"middlewares.py のインポートに失敗: {e}")
