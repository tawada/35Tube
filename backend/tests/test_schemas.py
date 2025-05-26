import pytest

# サンプルテスト: schemas.py のインポート

def test_import_schemas():
    try:
        import backend.src.app.schemas
    except Exception as e:
        pytest.fail(f"schemas.py のインポートに失敗: {e}")
