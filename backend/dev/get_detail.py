import os
from googleapiclient.discovery import build

# ここに取得したAPIキーを貼り付けてください
API_KEY = os.environ['YOUTUBE_API_KEY']


def get_youtube_video(video_id, max_results=5):
    """
    videoIdから
    """
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # 検索リクエストの作成
    request = youtube.videos().list(
        part='snippet',
        id=video_id,
    )

    # API へリクエストを送信
    response = request.execute()

    # 結果を整形して出力
    for item in response.get('items', []):
        print('Video ID:', item['id'])
        print(item)

if __name__ == "__main__":
    # 動画ID
    video_id = "VW8Ul4HqwSg"
    # 動画を検索して結果を表示
    get_youtube_video(video_id)
