import pytest

# サンプルテスト: models.py のインポート

def test_import_models():
    try:
        import backend.src.app.models
    except Exception as e:
        pytest.fail(f"models.py のインポートに失敗: {e}")
