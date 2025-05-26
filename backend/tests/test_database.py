import pytest

# サンプルテスト: database.py のインポート

def test_import_database():
    try:
        import backend.src.app.database
    except Exception as e:
        pytest.fail(f"database.py のインポートに失敗: {e}")
