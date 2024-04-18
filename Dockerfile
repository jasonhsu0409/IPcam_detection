# 使用官方Python映像檔作為基礎
FROM python:3.8-slim

# 設定工作目錄
WORKDIR /app

# 將當前目錄下的所有檔案複製到工作目錄
COPY . /app

# 安裝requirements.txt中定義的所有依賴包
RUN pip install --no-cache-dir -r requirements.txt

# 開放端口
EXPOSE 5000

# 執行app/main.py
CMD ["python", "./app/main.py"]