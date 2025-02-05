# ベースイメージとして Python スリム版を利用（必要に応じて Node.js なども追加）
FROM python:3.13-slim

# 必要パッケージのインストール
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
 && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# FastAPI アプリと必要なファイルをコンテナにコピー
COPY app/ /app/app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Nginx の設定ファイルをコンテナへコピー
COPY nginx.conf /etc/nginx/nginx.conf

# Supervisor の設定ファイルをコンテナへコピー
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# フロントエンドの静的ファイル（事前ビルド済み）を配置
COPY frontend/ /app/frontend/

# Cloud Run が利用するポート 8080 を公開
EXPOSE 8080

# コンテナ起動時は supervisord を実行
CMD ["/usr/bin/supervisord", "-n"]
