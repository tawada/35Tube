import os
from googleapiclient.discovery import build

# ここに取得したAPIキーを貼り付けてください
API_KEY = os.environ['YOUTUBE_API_KEY']


def search_youtube_videos(query, max_results=5):
    """
    指定したクエリ（検索キーワード）で YouTube の動画を検索し、
    タイトルと動画URLを表示する関数
    """
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # 検索リクエストの作成
    request = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=max_results,
        type='video'
    )

    # API へリクエストを送信
    response = request.execute()

    # 結果を整形して出力
    for item in response.get('items', []):
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"タイトル: {title}")
        print(f"URL: {video_url}")
        print("-----")

if __name__ == "__main__":
    # 検索キーワード
    keyword = "猫 動画"
    # 動画を検索して結果を表示
    search_youtube_videos(query=keyword, max_results=5)
