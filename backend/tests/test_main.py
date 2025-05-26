import pytest

# サンプルテスト: main.py の FastAPI アプリがインポートできるか

def test_import_main():
    try:
        import backend.src.main
    except Exception as e:
        pytest.fail(f"main.py のインポートに失敗: {e}")
